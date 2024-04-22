use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

pub fn to_requirements(requirements: HashMap<String, String>) -> Result<(), std::io::Error> {
    let formatted_requirements = requirements
        .into_iter()
        .map(|(k, v)| format!("{}=={}", k, v))
        .collect::<Vec<String>>()
        .join("\n");

    let mut file = File::create("requirements.txt")?;
    file.write_all(formatted_requirements.as_bytes())?;
    Ok(())
}
