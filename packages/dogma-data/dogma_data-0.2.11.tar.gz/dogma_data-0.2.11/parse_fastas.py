from collections import OrderedDict
from torchtext import vocab
from dogma_data import parse_fasta, write_awkward, DatasetIndex
from pathlib import Path

IN_PATH = Path('.') / 'rna_taxon_fastas'
OUT_PATH = Path('.') / 'canonical_data'


AA_VOCAB = vocab.vocab(
    OrderedDict(
        [
            (token, 1)
            for token in [
                "a", "g", "c", "t",
                # Amino acids
                "A",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "K",
                "L",
                "M",
                "N",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "V",
                "W",
                "Y",
                "<stop>",  # Both selenocysteine and pyrrolysine
                "<aaunk>",

                "<rna_mask>",
                "<aa_mask>",
                # Indicators of the type of masking used in the sequence
                "<seq_triple_masked>",
                "<seq_third_masked>",
                "<seq_rna_masked>",
                "<seq_protein_masked>",
            ]
        ]
    ),
    specials=["<pad>", "<sos>", "<eos>", "<unk>"],
)
AA_VOCAB.set_default_index(AA_VOCAB["<aaunk>"])

def get_dataset_index(filename):
    if 'ccds' in filename:
        return DatasetIndex.ccds_rna_aa
    if 'ensembl' in filename:
        return DatasetIndex.ensembl_rna_aa
    if 'protein' in filename and 'ref' in filename:
        return DatasetIndex.protref_90_protein
    if 'clustered_rna' in filename:
        return DatasetIndex.merged_rna
    else:
        raise ValueError(f'Unknown dataset {filename}')

for file in IN_PATH.glob('*.fa'):
    print(f'Parsing fasta for {file.name}')
    arr = parse_fasta(str(file), vocab=AA_VOCAB, fasta_type='rna' if 'rna' in file.name else 'protein')
    arr['dataset_index'] = get_dataset_index(file.stem)
    if not OUT_PATH.exists():
        OUT_PATH.mkdir()
    out_filepath = OUT_PATH / f'{file.stem.split(".")[0]}.blosc.pkl'
    print(f'Writing to {out_filepath}')
    write_awkward(arr, out_filepath, nthreads=64)