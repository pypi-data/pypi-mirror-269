use std::{collections::HashSet, fs, path::Path};

use crate::parse::imports_from_file;

pub fn process_path(path: &Path) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    if path.is_dir() {
        let imports = process_directory(path)?;
        Ok(imports)
    } else if path.is_file() {
        let imports = imports_from_file(path);
        Ok(imports)
    } else {
        Err(From::from(
            "The provided path is neither a file nor a directory.",
        ))
    }
}

fn process_directory(path: &Path) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let mut imports = HashSet::new();
    for entry in fs::read_dir(path)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_file() && path.extension().and_then(std::ffi::OsStr::to_str) == Some("py") {
            let file_imports = imports_from_file(&path);
            imports.extend(file_imports);
        }
    }
    Ok(imports.into_iter().collect())
}
