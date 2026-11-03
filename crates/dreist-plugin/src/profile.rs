//! Dreist's app profile (`dreist_formats::profile`): the workspace's
//! reference profile with Dreist's own resources (this repository's
//! `assets/ui` and `assets/factory` in development builds) and its earlier
//! settings folder name.

use dreist_formats::profile::{BASE, Profile, Resources};

/// The settings folder name of Dreist's beta (moved to "Dreist" on first launch).
pub const LEGACY_SETTINGS_DIR: &str = "Geist-rs";

pub static DREIST: Profile = Profile {
    legacy_settings_dirs: &[LEGACY_SETTINGS_DIR],
    ui: Resources { dev_dirs: &[concat!(env!("CARGO_MANIFEST_DIR"), "/../../assets/ui")], ..BASE.ui },
    factory: Resources { dev_dirs: &[concat!(env!("CARGO_MANIFEST_DIR"), "/../../assets/factory")], ..BASE.factory },
    ..BASE
};

/// Install Dreist's profile (before any window, document or settings use).
pub fn install() {
    dreist_formats::profile::install(&DREIST);
}

#[cfg(test)]
mod tests {
    #[test]
    fn dreist_finds_its_own_resources() {
        super::install();
        let p = dreist_formats::profile::get();
        assert_eq!((p.product, p.save.project), ("Dreist", "dreist"));
        assert!(dreist_formats::paths::ui_dir().join("Skin/HeaderBar.skin").is_file());
        assert!(dreist_formats::paths::resources_dir().join("Effects").is_dir());
    }
}
