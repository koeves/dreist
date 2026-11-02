# Dreist: guide for contributors and coding agents

Dreist is a drum sampler, step sequencer and performance instrument written in
Rust. It is compatible with FXpansion Geist2 (2.1.2.13): it loads Geist2
`.geist` projects, kits and patterns and plays them the same way. It builds as
VST3, CLAP and a standalone app for macOS (Apple Silicon) and Windows (x64).

The UI is branded "Dreist" (`geist_editor::PRODUCT`): no Geist or FXpansion
names in UI text. Crates and file formats keep their `geist` names.

## Crates

| Crate | Purpose |
|---|---|
| `geist-formats` | Geist2 file formats (projects, kits, patterns, presets) and resource paths |
| `geist-dsp` | voices, filters, modulators, timestretch, the 47 effects |
| `geist-engine` | sequencer, mixer, modulation, song, scenes, sampler, MIDI, export |
| `geist-gui` | skin-driven UI toolkit (baseview + softbuffer + tiny-skia) |
| `geist-editor` | the editor panels and their behaviour |
| `geist-plugin` | nih-plug VST3 / CLAP plugin and the standalone app |
| `geist-cli` | command-line tools: `geist-inspect` (check a file's samples), `geist-render` (offline render to WAV), `geist-nulltest` / `geist-stemfit` / `geist-bands` (compare renders) |
| `geist-testkit` | test helpers: golden fingerprints, signal checks, allocation counting |
| `xtask` | nih-plug bundler (`cargo xtask bundle geist-plugin`) |

`vendor/` holds patched baseview and signalsmith-stretch. `assets/dreist` is
Dreist's generated UI. `assets/geist2` holds Geist2's factory effect presets,
effect chains and pattern/swing templates (FXpansion's files, bundled).

## Quick commands

    cargo test --workspace
    cargo fmt --all --check
    cargo clippy --workspace --all-targets -- -D warnings
    scripts/build.sh                  # macOS bundles into target/bundled/
    scripts/build-windows.sh          # Windows (Git Bash)

## Commits

- No AI attribution of any kind: no `Co-Authored-By: Claude`, no
  `Claude-Session:` trailer, no "Generated with ..." lines, in commits, PRs,
  tags or release notes.
- Author and committer are the repository's configured git identity; do not
  override `--author`.
- Short imperative subject; a body only when the why is not obvious.
- Keep the repository private (`koeves/dreist`).

## More

- [building.md](building.md): build, test and run on macOS and Windows; content; test goldens.
- [ui.md](ui.md): the generated skins, styles and icons; UI screenshots.
- [release.md](release.md): the release workflow, signing, third-party notices.
- [conventions.md](conventions.md): formatting, lints, realtime safety, errors, comments.

Private reverse-engineering notes for Geist2 live in `koeves/dreist-re`, for
those with access.
