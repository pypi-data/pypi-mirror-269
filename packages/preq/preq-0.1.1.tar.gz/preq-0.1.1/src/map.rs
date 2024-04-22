use crate::utils::pyfuncs::{get_import_package_map, get_package_version};
use std::collections::HashMap;

pub fn imports_to_packages(imports: &Vec<String>) -> Vec<String> {
    let import_package_map = get_import_package_map();
    imports
        .iter()
        .filter_map(|import| {
            if let Some(packages) = import_package_map.get(import) {
                Some(packages.join(" "))
            } else {
                println!("No package found for import '{}'", import);
                None
            }
        })
        .collect()
}

pub fn packages_to_versions(packages: &Vec<String>) -> HashMap<String, String> {
    packages
        .iter()
        .filter_map(|package| {
            if let Some(version) = get_package_version(package) {
                Some((package.clone(), version))
            } else {
                println!("No version found for package '{}'", package);
                None
            }
        })
        .collect()
}
