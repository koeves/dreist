# Dreist UI graphics

Dreist's own artwork, licensed like the rest of the workspace (MIT OR Apache-2.0).

- **Generated**: by `scripts/uigen/uigen.py` (needs skia-python and fontTools); edit the code there, never the files here.
- **Stale check**: `python3 scripts/uigen/uigen.py --check` fails when the files are out of date.
- **`Skin/`**: every panel layout (`.skin`), the stylesheets and the themes; layouts come from `scripts/uigen/skins/`, stylesheets from `scripts/uigen/theme.py`.
- **Control names**: what the editor binds to; geometry, captions and tooltips are Dreist's own.
- **`Fonts/Dreist-Icons.ttf`**: the icon font, at the skins' icon code points (U+E900..U+E92B).
- **`Cursors/`**: the named image cursors and their hotspots.
- **`AppIcon.icns`, `AppIcon.png`**: the app icon, a blue "D" on a dark rounded square (`scripts/icon.py`).
- **`Metronomes/`**: synthesised click sets (`scripts/uigen/sounds.py`).
- **`preview.png`**: a contact sheet, not bundled.
