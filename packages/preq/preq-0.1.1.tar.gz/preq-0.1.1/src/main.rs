use clap::Parser;
mod cli;
mod input;
mod map;
mod parse;
mod utils;
mod write;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = cli::Args::parse();

    let imports = input::process_path(&cli.path)?;
    let packages = map::imports_to_packages(&imports);
    let versions = map::packages_to_versions(&packages);
    match write::to_requirements(versions) {
        Ok(_) => println!("Successfully wrote requirements.txt"),
        Err(e) => eprintln!("Error writing requirements.txt: {}", e),
    }

    Ok(())
}
