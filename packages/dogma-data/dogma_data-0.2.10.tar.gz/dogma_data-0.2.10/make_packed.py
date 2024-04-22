# import polars as pl
# import pickle
from tqdm.auto import tqdm, trange
import h5py
from pathlib import Path
from contextlib import contextmanager
import numpy as np
from time import time
import pickle
from dogma_data._dogma_data import PackedDataset
# import pandas as pd
# from numba import njit
# import numpy as np

import os

os.environ['EXTRA_CLING_ARGS'] = '-O3'


import cppyy

cppyy.add_include_path(np.get_include())
cppyy.include("cpp_functions.hpp")

import cppyy.ll
with cppyy.ll.signals_as_exception():

    get_all_array_lengths = cppyy.gbl.get_all_array_lengths
    concatenate_arrays = cppyy.gbl.concatenate_arrays
    # concatenate_arrays.__release_gil__ = True

    in_list = [np.array([1,2,3,4], dtype=np.uint8), np.array([], dtype=np.uint8), np.array([1,2,3,4,5], dtype=np.uint8)]
    seqlens_out = np.zeros(len(in_list), dtype=np.int64)
    print('Running get_all_array_lengths...')
    get_all_array_lengths(in_list, seqlens_out)
    print(f'{seqlens_out=}')
    cu_seqlens = np.zeros(len(in_list) + 1, dtype=np.int64)
    cu_seqlens[1:] = np.cumsum(seqlens_out)
    print(f'{cu_seqlens=}')
    concat = np.zeros(9, dtype=np.uint8)
    concatenate_arrays(in_list, cu_seqlens, concat)
    print(concat)

    read_locs = {
        # 'ccds_rna_aa': "/lfs/local/0/yanay/dogma_datasets_pickle/ccds_rna_aa.pkl",
        # 'rnacentral_rna': "/lfs/local/0/yanay/dogma_datasets_pickle/rnacentral_rna.pkl",
        # 'refseq_rna': "/lfs/local/0/yanay/dogma_datasets_pickle/refseq_rna.pkl",
        # 'protref_90_protein': "/lfs/local/0/yanay/dogma_datasets_pickle/protref_90_protein.pkl",
        # 'ensembl_rna_aa': "/lfs/local/0/yanay/dogma_datasets_pickle/ensembl_rna_aa.pkl"
    }

    @contextmanager
    def timer(name):
        print(f'{name}...')
        start = time()
        yield
        print(f'{name} took {time() - start} seconds')


    def make_random_access_buffer(all_rows: list[np.ndarray]):
        num_sequences = len(all_rows)
        seqlens_out = np.zeros(num_sequences, dtype=np.int64)
        with timer('get_all_array_lengths'):
            get_all_array_lengths(all_rows, seqlens_out)
        cu_seqlens = np.empty(num_sequences + 1, dtype=np.int64)
        cu_seqlens[0] = 0
        cu_seqlens[1:] = np.cumsum(seqlens_out)
        assert len(cu_seqlens) == num_sequences + 1

        all_tokens = np.zeros(cu_seqlens[-1], dtype=np.uint8)
        with timer('concat'):
            concatenate_arrays(all_rows, cu_seqlens.data, all_tokens.data)
        return all_tokens, cu_seqlens

    print(make_random_access_buffer([np.array([1,2,3,4], dtype=np.uint8), np.array([1,2,3,4,5], dtype=np.uint8)]))

    for name, path in tqdm(list(read_locs.items())):
        path = Path(path)
        with open(path, 'rb') as f:
            with timer(f'load {path.name}'):
                all_tokens = pickle.load(f)
            print(len(all_tokens))
            with timer(f'Compute buffers'):
                packed_tokens, cu_seqlens = make_random_access_buffer(all_tokens)
            packed_data = PackedDataset(packed_tokens, cu_seqlens)

            # for i in trange(len(all_tokens)):
            #     assert np.all(all_tokens[i] == packed_data[i])

            out_filename = f'blosc_data/{path.stem}.blosc.pkl'
            with timer(f'Write to {out_filename}'):
                packed_data.to_file(out_filename)
            # with timer(f'Load from {out_filename}'):
            #     reconstructed_data = PackedDataset.from_file(out_filename)

            del all_tokens
            
            # h5_path = Path('lightning_data') / f'{path.stem}2.h5'
            # with h5py.File(h5_path, 'w') as f, timer(f'Write to {h5_path}'):
            #     f.create_dataset('all_tokens', data=packed_tokens, **hdf5plugin.Blosc2(), chunks=(min(packed_tokens.shape[0], 2**32 - 1), ))
            #     f.create_dataset('cu_seqlens', data=cu_seqlens, **hdf5plugin.Blosc2(), chunks=(min(cu_seqlens.shape[0], 2**32 - 1), ))
            # del packed_tokens, cu_seqlens