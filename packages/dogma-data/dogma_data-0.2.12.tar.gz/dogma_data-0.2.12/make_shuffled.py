from pathlib import Path

import awkward as ak
import numpy as np

from dogma_data import read_awkward, fast_permute_and_pack, write_awkward, parse_fasta, shard_awkward

name_idxs = {
    'rnacentral_rna':4,
    'refseq_rna':3,
    'protref_90_protein':2,
    'ccds_rna_aa':1,
    'ensembl_rna_aa':0
}

IN_PATH = Path('.') / 'canonical_data'

alldata = IN_PATH.glob('*.blosc.pkl')
protein_data = IN_PATH.glob('*protein*.blosc.pkl')

# in_files = Path('rna_taxon_fastas').rglob('*.fa')
# in_files = Path('canonical_data').rglob('clustered_rna.blosc.pkl')

datasets = []

for in_file in alldata:
    data = read_awkward(in_file, nthreads=64)
    if 'ccds' in in_file.name:
        dataset_index = 1
    elif 'ensembl' in in_file.name:
        dataset_index = 0
    elif 'protein' in in_file.name:
        dataset_index = 2
    elif 'clustered_rna' in in_file.name:
        dataset_index = 3
    else:
        raise ValueError()
    data['dataset_index'] = dataset_index
    datasets.append(data)

print('Starting concatenate')
combined_data = ak.concatenate(datasets)
print('Finished concatenate')

permutation = np.arange(len(combined_data))
np.random.shuffle(permutation)

train_size = int(0.9 * len(combined_data))
test_size = int(0.05 * len(combined_data))
val_size = len(combined_data) - train_size - test_size

train_idcs = permutation[:train_size]
test_idcs = permutation[train_size:train_size + test_size]
val_idcs = permutation[train_size + test_size:]

for split, idcs in zip(['train', 'test', 'val'], [train_idcs, test_idcs, val_idcs]):
    print('Permuting and packing data')
    split_data = fast_permute_and_pack(combined_data, idcs)
    print('Writing to shards')
    shard_awkward(split_data, f'alldata_{split}')
    # write_awkward(split_data, f'protein_shuffled_{split}.blosc.pkl')