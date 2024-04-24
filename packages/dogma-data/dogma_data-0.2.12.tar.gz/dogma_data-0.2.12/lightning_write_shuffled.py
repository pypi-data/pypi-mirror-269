import os

from lightning.data import optimize
import random
import numpy as np

from tqdm.auto import tqdm, trange
from dogma_data._dogma_data import PackedDataset
from contextlib import contextmanager
from time import time
import awkward as ak
from dogma_data._dogma_data import write_awkward, fast_permute_and_pack

name_idxs = {
    'rnacentral_rna':4,
    'refseq_rna':3,
    'protref_90_protein':2,
    'ccds_rna_aa':1,
    'ensembl_rna_aa':0
}

from numba import njit, prange

# @njit(parallel=True)
# def split_indices(idcs: np.ndarray, dataset_lengths: np.ndarray) -> list[np.ndarray]:
#     out_masks = [np.zeros(idcs.shape, dtype=np.bool_) for _ in dataset_lengths]
#     i_base = 0
#     for i, l in enumerate(dataset_lengths):
#         out_masks[i] = (0 < idcs) & (idcs < l)
#         i_base += l
#     return out_masks

# @njit(parallel=True)
# def gather_tokens(idcs: np.ndarray, datasets: list[ak.Array]) -> np.ndarray:






# class hierarchicalmergeddataset:
#     def __init__(self, datasets: dict[str, packeddataset]):
#         self.datasets = datasets
#         self.lengths = np.array([len(ds) for ds in datasets.items()], dtype=np.int64)
    
#     def __getitem__(self, idcs):
#         assert isinstance(idcs, np.ndarray)
#         # vectorized version
#         print('splitting indices')
#         masks = split_indices(idcs, self.lengths)
#         dataset_idcs = np.zeros_like(idcs, dtype=np.uint8)
#         print('finding dataset indices')
#         for key, mask in zip(self.datasets.keys(), masks):
#             dataset_idcs[mask] = name_idxs[key]
#         print('gathering tokens')
#         for (key, ds), mask in zip(self.datasets.items(), masks):
#             tokens = ds[idcs[mask]]
            

        
#         return {'tokens': tokens, 'dataset_index': dataset_idcs}

    
#     def __len__(self):
#         return int(np.sum(self.lengths))


@contextmanager
def timer(name):
    print(f'{name}...')
    start = time()
    yield
    print(f'{name} took {time() - start} seconds')

# with timer('loading dataset'):
#     dataset = packeddataset.from_h5file('lightning_data/rnacentral_rna2.h5')



# # test random hdf5 access
# with h5py.File('lightning_data/ccds_rna_aa.h5', 'r') as f:
#     cu_seqlens = f['cu_seqlens'][:]
#     all_tokens = f['all_tokens'][:]
#     packed_access = PackedAccess(all_tokens, cu_seqlens)


# total_seqs = len(dataset)
# for _ in trange(100_000):
#     random_seq = random.randrange(0, total_seqs)
#     seq = dataset[random_seq]


read_locs = {
    'ccds_rna_aa':"/lfs/local/0/roed/projects/dogma-data/blosc_data/ccds_rna_aa.blosc.pkl",
    'rnacentral_rna':"/lfs/local/0/roed/projects/dogma-data/blosc_data/rnacentral_rna.blosc.pkl",
    'refseq_rna':"/lfs/local/0/roed/projects/dogma-data/blosc_data/refseq_rna.blosc.pkl",
    'protref_90_protein':"/lfs/local/0/roed/projects/dogma-data/blosc_data/protref_90_protein.blosc.pkl",
    'ensembl_rna_aa':"/lfs/local/0/roed/projects/dogma-data/blosc_data/ensembl_rna_aa.blosc.pkl"
}


# all_seqs = []
# all_idxs = []
# all_lens = []
# token_count = 0

SPLITS = {
    'rna_aa': [
        'ccds_rna_aa',
        'ensembl_rna_aa',
    ],
    'protein_only': [
        'protref_90_protein',
    ],
    'rna_aa_and_rna': [
        'ccds_rna_aa',
        'ensembl_rna_aa',
        'rnacentral_rna',
        'refseq_rna',
    ],
    'rna_aa_and_protein': [
        'ccds_rna_aa',
        'ensembl_rna_aa',
        'protref_90_protein'
    ],
    'all_data': [
        'ccds_rna_aa',
        'ensembl_rna_aa',
        'protref_90_protein',
        'rnacentral_rna',
        'refseq_rna',
    ]
}

# SPLIT_NAME = "rna_aa"
# split_items = [
#     # 'rnacentral_rna',
#     # 'refseq_rna',
#     # 'protref_90_protein',
#     'ccds_rna_aa',
#     'ensembl_rna_aa',
# ]

for split_name, split_items in SPLITS.items():

    all_dss = []
    all_dataset_idcs = []
    token_count = 0

    for name, loc in read_locs.items():
        if name in split_items:
            with timer(f'Loading {name}'):
                ds = PackedDataset.from_file(loc).as_awkward()
            dataset_idx = name_idxs[name]
            dataset_idx_arr = np.full((len(ds),), fill_value=dataset_idx, dtype=np.uint8)
            ds = ak.Array({
                'tokens': ds,
                'dataset_index': dataset_idx_arr,
            })

            seq_lens = ak.num(ds['tokens'], axis=1)
            token_count_seq = ak.sum(seq_lens)

            token_count += token_count_seq
            all_dataset_idcs.append(dataset_idx_arr)
            all_dss.append(ds)
            print("*************************************")
            print(f"{name} added, {len(ds):_} seqs, {token_count_seq:_} tokens")
            print(f"{name} Sumary Stats")
            print(f"Total Number of tokens: {token_count_seq:_}")
            print(f"Total Number of sequences: {len(ds):_}")
            print(f"Mean length: {np.mean(seq_lens):.2f}")
            print(f"Max length: {np.max(seq_lens):.2f}")
            print(f"Min length: {np.min(seq_lens):.2f}")
            print(f"Median length: {np.median(seq_lens):.2f}")
            print("*************************************")
                
    with timer('Merging datasets'):
        all_dss = ak.concatenate(all_dss, axis=0)


    all_lens = ak.num(all_dss['tokens'], axis=1)

    n_sequences = len(all_dss)
                
    print("Done adding")
    print("Summary Stats All:")
    print(f"Total Number of tokens: {token_count:_}")
    print(f"Total Number of sequences: {len(all_lens):_}")
    print(f"Mean length: {np.mean(all_lens):.2f}")
    print(f"Max length: {np.max(all_lens):.2f}")
    print(f"Min length: {np.min(all_lens):.2f}")
    print(f"Median length: {np.median(all_lens):.2f}")


    TRAIN_WRITE_LOC = f"/lfs/local/0/roed/projects/dogma-data/ak_data/{split_name}_train_shuffled_dataset"
    TEST_WRITE_LOC = f"/lfs/local/0/roed/projects/dogma-data/ak_data/{split_name}_test_shuffled_dataset"
    VALIDATION_WRITE_LOC = f"/lfs/local/0/roed/projects/dogma-data/ak_data/{split_name}_validation_shuffled_dataset"


    np.random.seed(8)
    permutation = np.arange(n_sequences)
    np.random.shuffle(permutation)
    print(f'{n_sequences=}')

    TEST_LEN = int(0.05 * n_sequences)
    VAL_LEN = TEST_LEN
    TRAIN_LEN = n_sequences - TEST_LEN - VAL_LEN
    print(f"SPLIT NAME: {split_name}")
    print(f"TEST SIZE: {TEST_LEN}")
    print(f"VAL SIZE: {VAL_LEN}")
    print(f"TRAIN SIZE: {TRAIN_LEN}")


    # from multiprocessing.managers import SharedMemoryManager

    # smm = SharedMemoryManager()
    # smm.start()

    # shared_tokens = smm.SharedMemory(size=all_dss.all_tokens.nbytes)
    # shared_tokens_np = np.ndarray(all_dss.all_tokens.shape, dtype=all_dss.all_tokens.dtype, buffer=shared_tokens.buf)
    # shared_tokens_np[:] = all_dss.all_tokens[:]
    # shared_cu_seqlens = smm.SharedMemory(size=all_dss.cu_seqlens.nbytes)
    # shared_cu_seqlens_np = np.ndarray(all_dss.cu_seqlens.shape, dtype=all_dss.cu_seqlens.dtype, buffer=shared_cu_seqlens.buf)
    # shared_cu_seqlens_np[:] = all_dss.cu_seqlens[:]

    # # Awkward array that's accessible as shared memory!
    # shared_dataset = PackedDataset(all_tokens=shared_tokens_np, cu_seqlens=shared_cu_seqlens_np).as_awkward()

    # dataset_idcs_shm = smm.SharedMemory(size=all_dataset_idcs.nbytes)
    # dataset_idcs_shm_np = np.ndarray(all_dataset_idcs.shape, dtype=all_dataset_idcs.dtype, buffer=dataset_idcs_shm.buf)

    # def format(idx):
    #     tokens = shared_dataset[idx]
    #     dataset_idx = dataset_idcs_shm_np[idx]
    #     return {'tokens': tokens, 'dataset_index': dataset_idx}

    test_choices = permutation[TRAIN_LEN:(TRAIN_LEN + TEST_LEN)]

    with timer('making test dataset'):
        test_ds = fast_permute_and_pack(all_dss, test_choices)
    with timer('writing test dataset'):
        write_awkward(test_ds, f'{TEST_WRITE_LOC}.blosc.pkl')
    del test_ds

    # optimize(
    #     fn=format,
    #     inputs=test_choices.tolist(),
    #     num_workers=100,
    #     output_dir=TEST_WRITE_LOC,
    #     chunk_bytes="500MB",
    # )


    # print("Writing validation dataset...")


    val_choices = permutation[(TRAIN_LEN + TEST_LEN):]
    with timer('making validation dataset'):   
        val_ds = fast_permute_and_pack(all_dss, val_choices)
    with timer('writing validation dataset'):
        write_awkward(val_ds, f'{VALIDATION_WRITE_LOC}.blosc.pkl')
    del val_ds

    # optimize(
    #     fn=format,
    #     inputs=val_choices.tolist(),
    #     num_workers=100,
    #     output_dir=VALIDATION_WRITE_LOC,
    #     chunk_bytes="500MB",
    # )


    # print("Writing train dataset...")
    train_choices = permutation[:TRAIN_LEN]
    # optimize(
    #     fn=format,
    #     inputs=train_choices.tolist(),
    #     num_workers=100,
    #     output_dir=TRAIN_WRITE_LOC,
    #     chunk_bytes="500MB",
    # )
    with timer('making train dataset'):
        train_ds = fast_permute_and_pack(all_dss, train_choices)
    with timer('writing train dataset'):
        write_awkward(train_ds, f'{TRAIN_WRITE_LOC}.blosc.pkl')
    
    del train_ds