from pathlib import Path
from dogma_data import PackedDataset, read_awkward, write_awkward
from dogma_data.utils import timer

OUT_PATH = Path('/lfs/local/0/roed/projects/dogma-data/ak_data')
IN_PATH = Path('/lfs/local/0/roed/projects/dogma-data/blosc_data')

for file in IN_PATH.iterdir():
    with timer(f'Reading {file}'):
        ds = PackedDataset.from_file(file).as_awkward()
    out_path = OUT_PATH / file.name
    with timer(f'Writing {out_path}'):
        write_awkward(ds, out_path)