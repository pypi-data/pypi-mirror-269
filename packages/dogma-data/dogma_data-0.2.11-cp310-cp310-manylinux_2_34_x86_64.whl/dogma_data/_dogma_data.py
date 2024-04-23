import io
import warnings

import numpy as np
import blosc2
from io import BytesIO, StringIO
import pickle
from pathlib import Path
from typing import IO, Any
import awkward as ak
from numpy.typing import DTypeLike, NDArray
from typing import TypeVar
from enum import IntEnum

from numba import njit, prange

from dogma_data.utils import check_equality, timer, ceildiv
from smart_open import open as smart_open

from .dogma_rust import awkward_from_list_of_numpy, concatenate_awkward as rust_concatenate_awkward, concatenate_numpy as concatenate_arrays

_T = TypeVar("_T", bound=np.generic, covariant=True)

def concatenate_numpy(l: list[NDArray[_T]]) -> tuple[NDArray[_T], NDArray[np.int64]]:
    arr, cu = concatenate_arrays(l)
    dtype: DTypeLike = l[0].dtype
    arr = arr.view(dtype)
    cu //= dtype.itemsize
    return arr, cu

def find_chunk_size(total_size):
    assert total_size >= 0
    # Each chunk needs to be at most 2**32 - 1, so keep dividing by 2 until we get a valid chunk size 
    current = total_size
    while current > 2**32 - 1:
        current //= 2
    return current


def _compress_leaves(node: dict | tuple | list | Any) -> dict | tuple | list | bytes:
    if isinstance(node, dict):
        return {k: _compress_leaves(v) for k, v in node.items()}
    elif isinstance(node, (tuple, list)):
        return [_compress_leaves(v) for v in node]
    elif isinstance(node, np.ndarray):
        return blosc2.pack_array2(node)
    else:
        return node

def _decompress_leaves(node: dict | tuple | list | bytes) -> dict | tuple | list | Any:
    if isinstance(node, dict):
        return {k: _decompress_leaves(v) for k, v in node.items()}
    elif isinstance(node, (tuple, list)):
        return [_decompress_leaves(v) for v in node]
    elif isinstance(node, bytes):
        return blosc2.unpack_array2(node)
    else:
        return node


def write_blosc_pickle(node: dict | tuple | list, path_or_fileobj: Path | str | IO):
    compressed = _compress_leaves(node)
    if isinstance(path_or_fileobj, (str, Path)):
        with smart_open(path_or_fileobj, 'wb') as f:
            pickle.dump(compressed, f)
    else:
        pickle.dump(compressed, path_or_fileobj)

def read_blosc_pickle(path_or_fileobj: Path | str | IO) -> dict | tuple | list:
    if isinstance(path_or_fileobj, (str, Path)):
        with smart_open(path_or_fileobj, 'rb') as f, timer('Reading blosc pickle'):
            compressed = pickle.load(f)
    elif isinstance(path_or_fileobj, io.IOBase):
        with timer('Reading blosc pickle'):
            compressed = pickle.load(path_or_fileobj)
    else:
        raise ValueError(f'path_or_fileobj must be a Path, str, or IO object, not {type(path_or_fileobj)}')
    with timer('Decompressing'):
        return _decompress_leaves(compressed)


def write_awkward(arr: ak.Array, path_or_fileobj: Path | str | IO, nthreads: int | None = None):
    """
    Write any awkward array to file.
    Compresses the underlying buffers with Blosc2 blosclz for efficient storage and very fast reading/writing with multiple threads.
    """
    try:
        if nthreads:
            prev_nthreads = blosc2.set_nthreads(nthreads)
        tree = ak.to_buffers(arr)
        write_blosc_pickle(tree, path_or_fileobj)
    finally:
        if nthreads:
            blosc2.set_nthreads(prev_nthreads)

def read_awkward(path_or_fileobj: Path | str | IO, nthreads=None) -> ak.Array:
    """
    Read any awkward array from file.
    Decompresses using Blosc2 blosclz for very fast reading with multiple threads.
    """
    try:
        if nthreads:
            prev_nthreads = blosc2.set_nthreads(nthreads)
        tree = read_blosc_pickle(path_or_fileobj)
        return ak.from_buffers(*tree)
    finally:
        if nthreads:
            blosc2.set_nthreads(prev_nthreads)

@njit(parallel=True)
def _fast_pack(seqlens, starts, stops, content):
    """
    Helper function to quickly pack content into a new Awkward array buffer.
    """
    cu_seqlens = np.zeros((len(seqlens) + 1,), dtype=np.int64)
    cu_seqlens[1:] = np.cumsum(seqlens)
    n_seqs = len(seqlens)
    out_size = np.sum(seqlens)
    out_arr = np.zeros((out_size,), dtype=content.dtype)
    for i in prange(n_seqs):
        start = starts[i]
        stop = stops[i]
        data = content[start:stop]
        out_arr[cu_seqlens[i]:cu_seqlens[i + 1]] = data
    return out_arr, cu_seqlens

def fast_permute_and_pack(arr: ak.Array, permutation: np.ndarray) -> ak.Array:
    """
    Index the array with the indices given by `permutation`, and pack the resulting Awkward array into contiguous buffers.

    arr: ak.Array - A RecordArray
    permutation: np.ndarray - An array of indices of the rows of the RecordArray to keep, not necessarily in order.

    Returns: ak.Array - A new RecordArray with the rows permuted and packed into contiguous buffers. Ready to write.
    """
    assert len(arr.fields) > 0
    assert isinstance(arr.layout, ak.contents.RecordArray)
    new_fields = {}
    for field_name in arr.fields:
        field = arr[field_name]
        if isinstance(field.layout, ak.contents.listoffsetarray.ListOffsetArray):
            seqlens = ak.num(field).layout.data[permutation]
            starts = field.layout.offsets[permutation].data
            stops = field.layout.offsets[permutation + 1].data
            content = field.layout.content.data
            packed_arr, cu_seqlens = _fast_pack(seqlens, starts, stops, content)
            new_field = ak.contents.ListOffsetArray(ak.index.Index64(cu_seqlens), ak.contents.NumpyArray(packed_arr))
            new_fields[field_name] = new_field
        elif isinstance(field.layout, ak.contents.NumpyArray):
            new_field = field.layout.data[permutation]
            new_fields[field_name] = ak.contents.NumpyArray(new_field)
        else:
            raise NotImplementedError(f'Cannot handle layout {field.layout}')
    return ak.Array(ak.contents.RecordArray(new_fields.values(), new_fields.keys()))
    

def awkward_from_flat(all_tokens: np.ndarray, cu_seqlens: np.ndarray) -> ak.Array:
    assert all_tokens.shape[0] == cu_seqlens[-1], 'Mismatched cu_seqlens and all_tokens shapes'
    assert cu_seqlens.dtype == np.int64
    if all_tokens.dtype != np.uint8:
        warnings.warn('The input tokens are not of type np.uint8. This can mean massive amounts of wasted space. Make sure this was intentional.', RuntimeWarning)
    offsets = ak.index.Index64(cu_seqlens)
    tokens = ak.contents.NumpyArray(all_tokens)
    return ak.Array(ak.contents.ListOffsetArray(offsets, tokens))





class PackedDataset:
    all_tokens: np.ndarray
    cu_seqlens: np.ndarray

    def __init__(self, all_tokens, cu_seqlens):
        self.all_tokens = all_tokens
        self.cu_seqlens = cu_seqlens
    
    def __getitem__(self, idx):
        index = self.cu_seqlens[idx:idx+2]
        return self.all_tokens[index[0]:index[1]]
    
    def __len__(self):
        return len(self.cu_seqlens) - 1
    
    def as_awkward(self):
        import awkward as ak
        offsets = ak.index.Index64(self.cu_seqlens)
        tokens = ak.contents.NumpyArray(self.all_tokens)
        return ak.Array(ak.contents.ListOffsetArray(offsets, tokens))
    
    def seq_lens(self):
        return np.diff(self.cu_seqlens)
    
    def to_file(self, path, verify_file=False):

        blosc2.set_nthreads(64)
        tokens_packed = blosc2.pack_array2(self.all_tokens)
        cu_seqlens_packed = blosc2.pack_array2(self.cu_seqlens)
        with open(path, 'wb') as f:
            pickle.dump({
                'all_tokens': tokens_packed,
                'cu_seqlens': cu_seqlens_packed
            }, f)
        if verify_file:
            with open(path, 'rb') as f:
                with timer('reading pickle'):
                    d = pickle.load(f)
                with timer('Unpacking all_tokens'):
                    all_tokens = blosc2.unpack_array2(d['all_tokens'])
                with timer('Unpacking cu_seqlens'):
                    cu_seqlens = blosc2.unpack_array2(d['cu_seqlens'])
                
                with timer('Checking equality'):
                    check_equality(all_tokens, self.all_tokens)
                    check_equality(cu_seqlens, self.cu_seqlens)

    @classmethod
    def from_file(cls, path: str | Path):
        """
        The file should be a pickle of blosc packed arrays.
        """
        blosc2.set_nthreads(64)
        with open(path, 'rb') as f:
            d = pickle.load(f)
        all_tokens = blosc2.unpack_array2(d['all_tokens'])
        cu_seqlens = blosc2.unpack_array2(d['cu_seqlens'])
        return cls(all_tokens, cu_seqlens)


class DatasetIndex(IntEnum):
    ensembl_rna_aa = 0
    ccds_rna_aa = 1
    protref_90_protein = 2
    refseq_rna = 3
    rnacentral_rna = 4
    merged_rna = 5