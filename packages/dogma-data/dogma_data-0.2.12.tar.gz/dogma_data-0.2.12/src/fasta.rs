use std::fs::File;
use std::io::Read;
use std::ops::Index;
use rayon::prelude::*;
use crate::data::AwkwardArray;
use crate::parallel::parallel_concatenate_buffers;
use indicatif::ProgressBar;


// Any fasta mapping can be stored in a vector of 256 elements
struct CharMapping {
    mappings: [u8; 256],
}

impl CharMapping {
    fn from_pairs(mapping_pairs: &[(u8, u8)], default_value: u8) -> Self {
        let mut mappings = [default_value; 256];
        for (k, v) in mapping_pairs {
            mappings[*k as usize] = *v;
        }
        CharMapping {
            mappings,
        }
    }
}

impl Index<u8> for CharMapping {
    type Output = u8;

    fn index(&self, index: u8) -> &Self::Output {
        &self.mappings[index as usize]
    }
}

pub struct ParsedFasta {
    pub sequences: AwkwardArray<'static, u8>,
    pub taxon_ids: Vec<u64>,
}

fn parse_fasta_chunk(text: &[u8], start_i: usize, end_i: usize, mapping: &CharMapping) -> ParsedFasta {
    let use_progress = start_i == 0;
    let progress_bar = if use_progress { Some(ProgressBar::new(end_i as u64).with_message("Parsing FASTA")) } else { None };
    let mut out_content = vec![];
    let mut out_cu_seqlens = vec![0];
    let mut out_taxon_ids = vec![];
    let mut i = start_i;

    let text_length = text.len();
    while i < text_length && unsafe { *text.get_unchecked(i) } != b'>' {
        // Move to first header
        i += 1;
    }

    let parse_char = |c| {
        mapping[c]
    };

    let mut current_taxon_id: Option<u64> = None;

    while i < text.len() {
        let c = unsafe { *text.get_unchecked(i) };

        if c == b'>' { // New header
            if let Some(progress_bar) = &progress_bar {
                progress_bar.update(|s| s.set_pos(i as u64))
            }
            if i >= end_i { // Continue until a header shows up that has been handled by a later chunk.
                break;
            }
            let taxon_id_start = i + 1;
            // Maybe parse the header in the future?
            while i < text.len() && unsafe { *text.get_unchecked(i) } != b'\n' {
                i += 1;
            }
            let taxon_id_end = i;
            let taxon_str = std::str::from_utf8(&text[taxon_id_start..taxon_id_end]).unwrap();
            current_taxon_id = Some(taxon_str.parse::<u64>().unwrap());
            i += 1; // Move to next line
            continue;
        } else { // Parse one line
            while i < text_length && unsafe { *text.get_unchecked(i) } != b'\n' {
                unsafe {
                    out_content.push(parse_char(*text.get_unchecked(i)));
                }
                i += 1;
            } // Ends if newline or end of file
            i += 1;
            out_cu_seqlens.push(out_content.len() as isize);
            out_taxon_ids.push(current_taxon_id.unwrap());
        }
    }

    if let Some(progress_bar) = progress_bar {
        progress_bar.finish();
    }

    ParsedFasta {
        sequences: AwkwardArray::new(out_content, out_cu_seqlens),
        taxon_ids: out_taxon_ids,
    }
    
}


pub(crate) fn parse_fasta(path: &str, mapping: &[u8], is_rna: bool) -> ParsedFasta{
    assert!(mapping.len() == 5);

    // Read file
    println!("Reading file");
    let source = File::open(path).unwrap();
    let pb = ProgressBar::new(source.metadata().unwrap().len()).with_message("Reading fasta");
    let mut data = vec![];
    pb.wrap_read(source).read_to_end(&mut data).unwrap();

    let mut n_threads = rayon::current_num_threads();

    let total_length = data.len();

    if total_length < 100_000 {
        n_threads = 1;
    }

    let chunk_size = total_length.div_ceil(n_threads);

    let mapping_pairs = if is_rna {vec![
        (b'A', 4),
        (b'G', 5),
        (b'C', 6),
        (b'T', 7),
        (b'U', 7),
    ]} else { vec![
        (b'A', 8 ),
        (b'C', 9 ),
        (b'D', 10),
        (b'E', 11),
        (b'F', 12),
        (b'G', 13),
        (b'H', 14),
        (b'I', 15),
        (b'K', 16),
        (b'L', 17),
        (b'M', 18),
        (b'N', 19),
        (b'P', 20),
        (b'Q', 21),
        (b'R', 22),
        (b'S', 23),
        (b'T', 24),
        (b'V', 25),
        (b'W', 26),
        (b'Y', 27),
    ]};

    let char_mapping = CharMapping::from_pairs(&mapping_pairs, if is_rna {3} else {29});

    println!("Parsing file {path} in chunks");

    let chunk_results: Vec<ParsedFasta> = (0..n_threads).par_bridge().map(|i| {
        let start_i = i * chunk_size;
        let end_i = std::cmp::min((i + 1) * chunk_size, total_length);
        parse_fasta_chunk(&data, start_i, end_i, &char_mapping)
    }).collect();


    println!("Merging result");
    let sequences_refs = chunk_results.iter().map(|pf| &pf.sequences).collect::<Vec<_>>();
    let taxon_ids = chunk_results.iter().map(|pf| pf.taxon_ids.as_slice()).collect::<Vec<_>>();

    let (merged_taxon_ids, _cu) = parallel_concatenate_buffers(&taxon_ids);
    let merged_sequences = AwkwardArray::parallel_concatenate(&sequences_refs);
    drop(chunk_results);

    ParsedFasta {
        sequences: merged_sequences,
        taxon_ids: merged_taxon_ids,
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_big_fasta() {
        let fasta_path = "/lfs/local/0/roed/projects/dogma-data/fasta_data/result_rep_seq.fasta";
        let result = parse_fasta(fasta_path, &[1, 2, 3, 4, 5], true);

        println!("Parsed fasta with {} sequences and {} tokens", result.sequences.cu_seqlens.len() - 1, result.sequences.content.len());
        println!("Got the following taxon ids: {:?}", result.taxon_ids);
        std::hint::black_box(&result);
    }
}