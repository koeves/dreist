//! What this editor knows about its app beyond the shared profile
//! (`dreist_formats::profile`): the About text, the settings folder, the
//! effect menu and how documents are read.

use std::path::Path;

use dreist_formats::Node;

/// The About text.
pub const ABOUT: &str = "Dreist: drum sampler, sequencer and performance instrument.\nNative for macOS, Windows and Linux, written in Rust.";

/// Settings folder name (`~/Library/Application Support/<name>`,
/// `%APPDATA%\<name>`, `$XDG_CONFIG_HOME/<name>`).
pub const SETTINGS_DIR: &str = "Dreist";

/// Earlier settings folder names: the first one found is moved to
/// [`SETTINGS_DIR`] when that does not exist yet (the beta's).
pub const LEGACY_SETTINGS_DIRS: &[&str] = &["Geist-rs"];

/// Environment variable naming a separate settings folder.
pub const SETTINGS_ENV: &str = "DREIST_SETTINGS_DIR";

/// Further extensions the Open dialog offers besides projects (files
/// [`read_project`] turns into a project).
pub const OPEN_ALSO: &[&str] = &[];

/// The effect types offered in effect menu category `c` (0..6), in menu order.
pub fn effect_menu(c: usize) -> Vec<usize> {
    dreist_formats::params::effect_menu(c)
}

/// A document file's root element (the editor's part loads); `None` when
/// it cannot be read.
pub fn read_document(path: &Path) -> Option<Node> {
    Node::parse(&std::fs::read_to_string(path).ok()?).ok()
}

/// A project to open and whether it was converted from another format (a
/// converted project is saved through Save As).
pub fn read_project(path: &Path) -> Option<(Node, bool)> {
    dreist_formats::Project::load(path).ok().map(|p| (p.raw, false))
}

/// The Open dialog's extensions: projects of every family (the app's own
/// first), then [`OPEN_ALSO`].
pub fn open_extensions() -> Vec<&'static str> {
    let mut v = dreist_formats::profile::extensions_of(dreist_formats::profile::DocKind::Project);
    v.extend(OPEN_ALSO);
    v
}
