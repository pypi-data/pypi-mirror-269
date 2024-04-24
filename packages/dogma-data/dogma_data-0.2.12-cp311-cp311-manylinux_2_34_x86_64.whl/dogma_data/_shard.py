from dataclasses import dataclass
from pathlib import Path
import numpy as np
import awkward as ak
from tqdm.auto import tqdm, trange
from contextlib import contextmanager
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.pool import Pool
from json import dump

from dogma_data._dogma_data import read_awkward, write_awkward, fast_permute_and_pack
from dogma_data.utils import ceildiv
import click


# SHUFFLED_PATH = Path("/lfs/local/0/roed/projects/dogma-data/ak_shuffled_data")
# SHARDED_PATH = Path("/lfs/local/0/roed/projects/dogma-data/ak_shuffled_sharded_data")

def _shared_awkward(arr: ak.Array, smm: SharedMemoryManager):
    form, size, buffers = ak.to_buffers(arr)
    shared_memory = {k: smm.SharedMemory(size=buf.nbytes) for k, buf in buffers.items()}
    shared_buffers = {k: (buffers[k].shape, buffers[k].dtype, v) for k, v in shared_memory.items()}
    for k, v in shared_buffers.items():
        np.ndarray(shape=v[0], dtype=v[1], buffer=v[2].buf)[:] = buffers[k]
    return form, size, shared_buffers

def _from_shared(form, size, shared_buffers):
    buffers = {k: np.ndarray(shape=v[0], dtype=v[1], buffer=v[2].buf) for k, v in shared_buffers.items()}
    return ak.from_buffers(form, size, buffers)

shared_arr = None
n_per_chunk = 1_000_000


@dataclass
class _WriteResult:
    out_file_path: Path
    num_sequences: int
    num_tokens: int

def _do_write(args):
    i, out_path = args
    global shared_arr

    return 


def write_split_index(out_path: Path, chunk_results: list[_WriteResult]) -> None:
    d = {
        'total_sequences': sum(r.num_sequences for r in chunk_results),
        'total_tokens': sum(r.num_tokens for r in chunk_results),
        'chunks': [
            {'filename': result.out_file_path.name,
             'num_sequences': result.num_sequences,
             'num_tokens': result.num_tokens,
             } for result in chunk_results
        ]
    }

    with open(out_path / 'index.json', 'w') as f:
        dump(d, f, indent=2)


@click.command()
@click.argument('in_path', type=Path)
@click.argument('out_path', type=Path, default=None)
def shard_file_cli(in_path: Path | str, out_path: str | None = None):
    in_path = Path(in_path)
    arr = read_awkward(in_path)

    if out_path is None:
        out_path = Path(in_path).parent / Path(in_path).name.split('.')[0]
    else:
        out_path = Path(out_path)

    shard_awkward(arr, out_path)




def shard_awkward(arr: ak.Array, out_path: str | Path):
    if isinstance(out_path, str):
        out_path = Path(out_path)

    n_splits = ceildiv(len(arr), n_per_chunk)
    out_path.mkdir(exist_ok=True)
    print(f'Starting mapping...')
    results = []
    for i in trange(n_splits, total=n_splits, desc='Sharding dataset'):
        split = np.arange(i * n_per_chunk, min((i + 1) * n_per_chunk, len(arr)))
        packed_slice = fast_permute_and_pack(arr, split)
        num_tokens = packed_slice['tokens'].layout.content.shape[0]
        out_file_path = out_path / f'{i:05d}.blosc.pkl'
        num_sequences = len(split)
        write_awkward(packed_slice, out_file_path)
        del packed_slice
        res = _WriteResult(out_file_path=out_file_path, num_sequences=num_sequences, num_tokens=num_tokens)
        results.append(res)
    print('Writing index file')
    write_split_index(out_path, results)



if __name__ == '__main__':
    # shard_file('protein_only_train_shuffled_dataset.blosc.pkl')
    shard_file_cli()