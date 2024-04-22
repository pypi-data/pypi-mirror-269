use std::{
    fs,
    io::{self, BufRead},
};

pub fn read_fallback_stdlib() -> Vec<String> {
    let file_path = "./assets/stdlib";
    let file = fs::File::open(file_path);

    match file {
        Ok(file) => {
            let buf_reader = io::BufReader::new(file);
            buf_reader.lines().filter_map(Result::ok).collect()
        }
        Err(e) => {
            println!(
                "Failed to read fallback data file '{}'; Error: {}; returning empty list.",
                file_path, e
            );
            Vec::new()
        }
    }
}
