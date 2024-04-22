use crate::utils::pyfuncs::get_stdlib;
use lazy_static::lazy_static;
use regex::Regex;
use std::{
    collections::HashSet,
    fs::File,
    io::{self, BufRead, BufReader},
    path::Path,
};

pub fn open_file(path: &Path) -> io::Result<BufReader<File>> {
    let file = File::open(path)?;
    Ok(BufReader::new(file))
}

lazy_static! {
    static ref IMPORT_REGEX: Regex = Regex::new(r"^\s*(from\s+[\w\.]+|import\s+[\w\.]+)").unwrap();
}

fn parse_import_line(line: &str, stdlib: &Vec<String>) -> Option<String> {
    if IMPORT_REGEX.is_match(line) {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if let Some(module) = parts.get(1) {
            let module_name = module.trim().to_string();
            if !stdlib.contains(&module_name) && !module_name.is_empty() {
                return Some(module_name);
            }
        }
    }
    None
}

pub fn imports_from_file(path: &Path) -> Vec<String> {
    let stdlib = get_stdlib();
    let reader = match open_file(path) {
        Ok(reader) => reader,
        Err(_) => {
            println!("Failed to read file '{:?}'; returning empty list.", path);
            return Vec::new();
        }
    };

    let modules: HashSet<String> = reader
        .lines()
        .filter_map(Result::ok)
        .filter_map(|line| parse_import_line(&line, &stdlib))
        .collect();

    modules.into_iter().collect()
}
