from streaming import MDSWriter
import numpy as np
from pathlib import Path
from tqdm.auto import tqdm, trange

DATA_DIR = Path('data/')
OUT_DIR = Path('mds_data/')

assert DATA_DIR.exists() and DATA_DIR.is_dir()
assert OUT_DIR.exists() and OUT_DIR.is_dir()

compression = 'zstd'  # Generally a safe choice -- quite fast
hashes = ['sha1']

columns = {
    'tokens': 'ndarray'
}

data_file = DATA_DIR / 'protref_90_179471324_1026_seqs.npz'

data_memmap = np.memmap(
    filename=str(data_file),
    dtype='int8',
    mode='r',
    shape=(179471324, 1026)
)

def write_dataset():
    with MDSWriter(out=str(OUT_DIR / f'{data_file.stem}.mds'), columns=columns, compression=compression, hashes=hashes) as writer:
        for line in tqdm(data_memmap, desc='Writing dataset...'):
            writer.write(sample={'tokens': line})

if __name__ == '__main__':
    write_dataset()