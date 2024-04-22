use crate::utils::fallback::read_fallback_stdlib;
use std::{collections::HashMap, process};

fn find_python_command() -> Option<String> {
    let commands = ["python3", "python", "py"];
    for &command in commands.iter() {
        if process::Command::new(command)
            .arg("--version")
            .output()
            .is_ok()
        {
            return Some(command.to_string());
        }
    }
    None
}

pub fn get_stdlib() -> Vec<String> {
    let python_command = find_python_command().unwrap_or_else(|| {
        println!("Python interpreter not found. Ensure Python is installed and in your PATH.");
        "python".to_string()
    });

    let python_code = "from sys import builtin_module_names as b, stdlib_module_names as s; print('\\n'.join(sorted(set(b) | s)))";
    let output = process::Command::new(python_command)
        .arg("-c")
        .arg(python_code)
        .output();

    match output {
        Ok(output) if output.status.success() => match String::from_utf8(output.stdout) {
            Ok(stdlib_str) => stdlib_str.lines().map(|s| s.to_string()).collect(),
            Err(_) => {
                println!("Error converting Python command output to UTF-8; using file fallback.");
                read_fallback_stdlib()
            }
        },
        _ => {
            println!("Python command failed or encountered an error; using file fallback.");
            read_fallback_stdlib()
        }
    }
}

pub fn get_import_package_map() -> HashMap<String, Vec<String>> {
    let python_command = find_python_command().unwrap_or_else(|| {
        println!("Python interpreter not found. Ensure Python is installed and in your PATH.");
        "python".to_string()
    });

    let python_code = "import importlib.metadata as i;print(i.packages_distributions())";
    let output = process::Command::new(python_command)
        .arg("-c")
        .arg(python_code)
        .output();

    if let Ok(output) = output {
        if let Ok(stdout) = String::from_utf8(output.stdout) {
            let cleaned_json = stdout.trim_end().replace("'", "\"");
            if let Ok(map) = serde_json::from_str::<HashMap<String, Vec<String>>>(&cleaned_json) {
                return map;
            }
        }
    }

    println!("Command failed to run or output was invalid.");
    HashMap::new()
}

pub fn get_package_version(package: &str) -> Option<String> {
    let python_command = find_python_command().unwrap_or_else(|| {
        println!("Python interpreter not found. Ensure Python is installed and in your PATH.");
        "python".to_string()
    });

    let python_code = format!(
        "import importlib.metadata as i;print(i.version('{}'))",
        package
    );
    let output = process::Command::new(python_command)
        .arg("-c")
        .arg(python_code)
        .output();

    if let Ok(output) = output {
        if let Ok(stdout) = String::from_utf8(output.stdout) {
            return Some(stdout.trim().to_string());
        }
    }

    println!("Command failed to run or output was invalid.");
    None
}
