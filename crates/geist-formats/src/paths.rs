//! Where the bundled resources live: Geist2's factory data (`assets/geist2`:
//! effect presets, effect chains, pattern and swing templates) and Dreist's
//! own UI (`assets/dreist`: skins, stylesheets, fonts, cursors, metronomes).
//!
//! Lookup order for each:
//! 1. an override (`GEIST2_RESOURCES`, `DREIST_UI`);
//! 2. `Contents/Resources/<Geist2|Dreist>` of the bundle this code was
//!    loaded from (`Dreist.app`, `Dreist.vst3`, `Dreist.clap`; found from our
//!    own image path, since a plugin's process is the host), or `Resources/`
//!    next to a bare Windows `.exe` / `.clap`;
//! 3. the repository's `assets/` (development builds and tests).

use std::path::PathBuf;

/// Name of the resources folder inside a bundle's `Contents/Resources`.
pub const BUNDLE_DIR: &str = "Geist2";

/// Geist2's factory data folder, laid out like the VST2's
/// `Contents/Resources` (`Effects/`, `Effect Chains/`, `Pattern Templates/`,
/// `Swing Templates/`).
pub fn resources_dir() -> PathBuf {
    if let Ok(p) = std::env::var("GEIST2_RESOURCES") {
        return PathBuf::from(p);
    }
    if let Some(p) = bundled() {
        return p;
    }
    repo_assets()
}

/// Where the VST2 kept its skins (`Resources/` inside [`resources_dir`]).
/// Dreist's skins live in [`ui_dir`]; this path only anchors the factory
/// data beside it (callers take its parent).
pub fn skin_dir() -> PathBuf {
    resources_dir().join("Resources")
}

/// Name of Dreist's own UI graphics folder inside a bundle's
/// `Contents/Resources`.
pub const UI_BUNDLE_DIR: &str = "Dreist";

/// Dreist's own UI graphics (`assets/dreist`: the icon font in `Fonts/`,
/// image cursors in `Cursors/`), drawn for this project by
/// `scripts/uigen/uigen.py`. Same lookup order as [`resources_dir`]:
/// `DREIST_UI`, the bundle's `Contents/Resources/Dreist`, then the
/// repository.
pub fn ui_dir() -> PathBuf {
    if let Ok(p) = std::env::var("DREIST_UI") {
        return PathBuf::from(p);
    }
    if let Some(p) = bundled_dir(UI_BUNDLE_DIR) {
        return p;
    }
    repo_ui()
}

/// The user's home folder (`HOME`; `USERPROFILE` on Windows).
pub fn home() -> PathBuf {
    std::env::var_os("HOME").or_else(|| std::env::var_os("USERPROFILE")).map(PathBuf::from).unwrap_or_default()
}

/// `assets/dreist` in the source tree.
pub fn repo_ui() -> PathBuf {
    PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/../../assets/dreist"))
}

/// `assets/geist2` in the source tree.
pub fn repo_assets() -> PathBuf {
    PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/../../assets/geist2"))
}

/// `<bundle>/Contents/Resources/Geist2` next to the image containing this
/// function, when it exists.
fn bundled() -> Option<PathBuf> {
    bundled_dir(BUNDLE_DIR)
}

/// `<bundle>/Contents/Resources/<name>` of the bundle holding this image.
fn bundled_dir(name: &str) -> Option<PathBuf> {
    let image = own_image()?;
    // <bundle>/Contents/MacOS/<binary>
    let bundle = image.parent()?.parent().map(|c| c.join("Resources").join(name));
    // Windows `.exe` and `.clap` are bare files: `Resources/` sits next to them.
    let beside = image.parent().map(|d| d.join("Resources").join(name));
    bundle.into_iter().chain(beside).find(|p| p.is_dir())
}

#[cfg(unix)]
fn own_image() -> Option<PathBuf> {
    #[repr(C)]
    struct DlInfo {
        dli_fname: *const std::os::raw::c_char,
        dli_fbase: *mut std::ffi::c_void,
        dli_sname: *const std::os::raw::c_char,
        dli_saddr: *mut std::ffi::c_void,
    }
    unsafe extern "C" {
        fn dladdr(addr: *const std::ffi::c_void, info: *mut DlInfo) -> std::os::raw::c_int;
    }
    let mut info = DlInfo { dli_fname: std::ptr::null(), dli_fbase: std::ptr::null_mut(), dli_sname: std::ptr::null(), dli_saddr: std::ptr::null_mut() };
    let addr = own_image as *const std::ffi::c_void;
    // SAFETY: dladdr only reads the address and fills `info`.
    let ok = unsafe { dladdr(addr, &mut info) };
    if ok == 0 || info.dli_fname.is_null() {
        return std::env::current_exe().ok();
    }
    // SAFETY: dli_fname is a NUL-terminated path owned by the loader.
    let s = unsafe { std::ffi::CStr::from_ptr(info.dli_fname) };
    Some(PathBuf::from(s.to_string_lossy().into_owned()))
}

#[cfg(windows)]
fn own_image() -> Option<PathBuf> {
    use std::os::windows::ffi::OsStringExt;
    const FROM_ADDRESS: u32 = 0x4;
    const UNCHANGED_REFCOUNT: u32 = 0x2;
    unsafe extern "system" {
        fn GetModuleHandleExW(flags: u32, name: *const u16, module: *mut *mut std::ffi::c_void) -> i32;
        fn GetModuleFileNameW(module: *mut std::ffi::c_void, name: *mut u16, size: u32) -> u32;
    }
    let mut module = std::ptr::null_mut();
    let addr = own_image as *const u16;
    // SAFETY: looks up the module containing this function; no refcount taken.
    if unsafe { GetModuleHandleExW(FROM_ADDRESS | UNCHANGED_REFCOUNT, addr, &mut module) } == 0 {
        return std::env::current_exe().ok();
    }
    let mut buf = vec![0u16; 32768];
    // SAFETY: `buf` holds `buf.len()` UTF-16 units.
    let n = unsafe { GetModuleFileNameW(module, buf.as_mut_ptr(), buf.len() as u32) } as usize;
    if n == 0 || n >= buf.len() {
        return std::env::current_exe().ok();
    }
    Some(PathBuf::from(std::ffi::OsString::from_wide(&buf[..n])))
}

#[cfg(not(any(unix, windows)))]
fn own_image() -> Option<PathBuf> {
    std::env::current_exe().ok()
}

#[cfg(test)]
mod tests {
    #[test]
    fn repo_ui_holds_the_skins() {
        assert!(super::repo_ui().join("Skin").join("HeaderBar.skin").is_file());
    }

    #[test]
    fn repo_ui_holds_the_icons_and_cursors() {
        assert!(super::repo_ui().join("Fonts").join("Dreist-Icons.ttf").is_file());
        assert!(super::repo_ui().join("Cursors").join("Cursors.hotspots").is_file());
    }
}
