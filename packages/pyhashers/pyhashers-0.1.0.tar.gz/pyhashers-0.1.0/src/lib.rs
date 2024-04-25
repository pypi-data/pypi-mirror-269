use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use walkdir::WalkDir;
use std::fs::File;
use std::io::{self, Read, Write};
use md5;
use rayon::prelude::*;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use regex::Regex; // Add this line to import the `Regex` type

/// This function reads the directory, computes MD5 hashes of files in parallel, and returns a Python dictionary
/// that includes each file's hash and the total number of files processed, while printing progress to the console.
#[pyfunction]
fn hash_directory_contents(dir_path: String, pattern: Option<String>, py: Python) -> PyResult<PyObject> {
    let dict = PyDict::new(py);
    let regex = match pattern {
        Some(p) => match Regex::new(&p) {
            Ok(r) => Some(r),
            Err(e) => {
                let message = format!("Invalid regex pattern: {}", e);
                return Err(PyValueError::new_err(message))
            }
        },
        None => None,
    };

    // Collect all valid file paths first
    let files: Vec<_> = WalkDir::new(dir_path)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| e.path().is_file())
        .filter(|e| match &regex {
            Some(r) => r.is_match(e.file_name().to_string_lossy().as_ref()),
            None => true,
        })
        .collect();

    let total_files = files.len();
    let processed_files = Arc::new(AtomicUsize::new(0));

    // Process each file in parallel
    let results: Vec<_> = files.into_par_iter().map(|entry| {
        let path = entry.path();
        let mut file = File::open(path).expect("Failed to open file");
        let mut contents = Vec::new();
        file.read_to_end(&mut contents).expect("Failed to read file");
        let hash = md5::compute(contents);
        let file_name = path.file_name().unwrap().to_str().unwrap().to_owned();
        let hash_str = format!("{:x}", hash);

        // Update progress
        let count = processed_files.fetch_add(1, Ordering::SeqCst) + 1;
        print!("\rProcessed {} of {} files", count, total_files);
        io::stdout().flush().unwrap();

        (file_name, hash_str)
    }).collect();

    println!(); // Move to the next line after finishing all files

    // Populate the dictionary with file hashes
    for (file_name, hash_str) in results {
        dict.set_item(file_name, hash_str)?;
    }

    Ok(dict.to_object(py))
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyhashers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hash_directory_contents, m)?)?;
    Ok(())
}
