#![allow(clippy::type_complexity)]
mod fasta;
mod data;
pub mod parallel;

use fasta::ParsedFasta;
use pyo3::prelude::*;
use pyo3::types::{PyList, PyTuple};
use numpy::{IntoPyArray, PyArray1, PyArrayDescrMethods, PyReadonlyArray1, PyUntypedArray, PyUntypedArrayMethods};
use crate::data::{AwkwardArray, TreatAsByteSlice};


impl<'a, T: Clone + Sync> From<Bound<'a, PyTuple>> for AwkwardArray<'a, T> {
    fn from(value: Bound<'a, PyTuple>) -> Self {
        let _content = value.get_item(0);
        todo!()
    }
}

#[pyfunction]
fn parse_fasta<'py>(py: Python<'py>, path: &str, mapping: PyReadonlyArray1<'py, u8>, is_rna: bool) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>, Bound<'py, PyArray1<u64>>)> {
    let mapping = mapping.as_slice()?;

    let ParsedFasta{sequences: AwkwardArray {content, cu_seqlens}, taxon_ids} = fasta::parse_fasta(path, mapping, is_rna);

    let content = content.into_owned().into_pyarray_bound(py);
    let cu_seqlens = cu_seqlens.into_owned().into_pyarray_bound(py);
    let taxon_ids = taxon_ids.into_pyarray_bound(py);
    Ok((content, cu_seqlens, taxon_ids))
}

#[pyfunction]
fn concatenate_awkward<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>)> {
    let awkwards: Vec<AwkwardArray<_>> = arrays.iter().map(|obj| {
        let tuple = obj.downcast::<PyTuple>()?;
        let tup_content = tuple.get_item(0)?;
        let tup_cu_seqlens = tuple.get_item(1)?;
        let content = tup_content.downcast::<PyUntypedArray>()?;
        let cu_seqlens = tup_cu_seqlens.downcast::<PyUntypedArray>()?;

        let content: &[u8] = unsafe { content.as_slice() }?;
        let cu_seqlens: &[isize] = unsafe { cu_seqlens.as_slice() }?;
        Ok(AwkwardArray::<u8>::new(content, cu_seqlens))
    }).collect::<PyResult<_>>()?;

    let awkward_refs = awkwards.iter().collect::<Vec<_>>();

    let AwkwardArray {content, cu_seqlens} = AwkwardArray::parallel_concatenate(&awkward_refs);

    Ok((content.into_owned().into_pyarray_bound(py), cu_seqlens.into_owned().into_pyarray_bound(py)))
}


#[pyfunction]
fn concatenate_numpy<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<(Bound<'py, PyArray1<u8>>, Bound<'py, PyArray1<isize>>)> {
    // Takes in a list of numpy arrays of the same dtype, and concatenates them into a single numpy array
    // The output array is always of dtype u8, so must be casted to the correct dtype after concatenation using `numpy.ndarray.view(dtype)`
    
    let buf_refs: Vec<_> = arrays.iter().map(|obj| -> PyResult<_> {
        let arr = obj.downcast::<PyUntypedArray>()?;
        Ok((arr.dtype(), unsafe{let arr = *arr.as_array_ptr(); arr.data}, arr.len(), arr.is_contiguous()))
    }).collect::<PyResult<_>>()?;
    let first_dtype = &buf_refs[0].0;

    let all_dtypes_match = buf_refs.iter().all(|(dtype, _ptr, _len, contiguous)| first_dtype.is_equiv_to(dtype) && *contiguous);
    if !all_dtypes_match {
        return Err(pyo3::exceptions::PyValueError::new_err("All arrays must have the same dtype and be contiguous"));
    }

    let itemsize = first_dtype.itemsize();

    let slices: Vec<&[u8]> = buf_refs.iter().map(|(_dtype, ptr, len, _contiguous)| unsafe { std::slice::from_raw_parts(*ptr as *const u8, len * itemsize) }).collect();

    let (sequences, mut cu_seqlens) = parallel::parallel_concatenate_buffers(&slices);
    cu_seqlens.push(sequences.len() as isize);  // Add the final index
    
    let sequences = sequences.into_pyarray_bound(py);
    let cu_seqlens = cu_seqlens.into_pyarray_bound(py);

    Ok((sequences, cu_seqlens))
}

#[pyfunction]
fn awkward_from_list_of_numpy<'py>(py: Python<'py>, arrays: Bound<'py, PyList>) -> PyResult<Bound<'py, PyTuple>> {
    if arrays.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Must provide at least one array"));
    }
    struct ArrStorage {
        data: *const u8,
        len: usize,
    }
    unsafe impl Sync for ArrStorage {}

    let mut first_dtype = None;
    let buf_refs: Vec<_> = arrays.iter().map(|obj| -> PyResult<_> {
        let arr = obj.downcast::<PyUntypedArray>()?;
        let arrobj = unsafe {*arr.as_array_ptr()};
        match &mut first_dtype {
            None => {first_dtype = Some(arr.dtype());},
            Some(first) => {
                if !first.is_equiv_to(&arr.dtype()) {
                    return Err(pyo3::exceptions::PyValueError::new_err("All arrays must have the same dtype"));
                }
            }
        };
        if !arr.is_contiguous() {
            return Err(pyo3::exceptions::PyValueError::new_err("All arrays must be contiguous"));
        }
        Ok(ArrStorage{data: arrobj.data as *const u8, len: arr.len()})
    }).collect::<PyResult<_>>()?;

    let first_dtype = first_dtype.unwrap();

    let itemsize: usize = first_dtype.itemsize();

    let slices: Vec<&[u8]> = buf_refs.into_iter().map(|arr| unsafe { std::slice::from_raw_parts(arr.data, arr.len * itemsize) }).collect();

    let (content, mut cu_seqlens) = parallel::parallel_concatenate_buffers(&slices);
    cu_seqlens.push(content.len() as isize);  // Add the final index

    let content_arr = content.into_pyarray_bound(py);
    let cu_seqlens_arr = cu_seqlens.into_pyarray_bound(py);

    Ok(PyTuple::new_bound(py, &[content_arr.to_object(py), cu_seqlens_arr.to_object(py)]))
}


#[pyfunction]
fn fast_pack<'py>(
    py: Python<'py>,
    seqlens: PyReadonlyArray1<'py, isize>,
    starts: PyReadonlyArray1<'py, isize>,
    stops: PyReadonlyArray1<'py, isize>,
    content: Bound<'py, PyUntypedArray>, nthreads: usize
) -> PyResult<()> {
    let dtype_width = content.dtype().itemsize();
    
    Ok(())
}


/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name="dogma_rust")]
fn dogma_rust(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_fasta, m)?)?;
    m.add_function(wrap_pyfunction!(concatenate_numpy, m)?)?;
    m.add_function(wrap_pyfunction!(concatenate_awkward, m)?)?;
    m.add_function(wrap_pyfunction!(awkward_from_list_of_numpy, m)?)?;
    m.add_function(wrap_pyfunction!(fast_pack, m)?)?;
    // m.add_function
    Ok(())
}
