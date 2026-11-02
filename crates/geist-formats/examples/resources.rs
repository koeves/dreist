//! Print where the bundled resources resolve to (diagnostics).
fn main() {
    println!("{}", geist_formats::paths::resources_dir().display());
}
