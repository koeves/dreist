# Dreist: guide for contributors and coding agents

Dreist is a drum sampler, step sequencer and performance instrument written in
Rust. It is compatible with FXpansion Geist2 (2.1.2.13): it loads Geist2
`.geist` projects, kits and patterns and plays them the same way. It builds as
VST3, CLAP and a standalone app for macOS (Apple Silicon) and Windows (x64).

The UI is branded "Dreist" (Dreist's app profile, `dreist-plugin/src/profile.rs`).
Outside README files, code, comments and docs carry no original product, vendor
or class names; legacy on-disk names live in `dreist_formats::legacy`, and RE
evidence is cited by tag (`[re:xxxxxx]`, map in `koeves/dreist-re`).

Dreist is a thin app on **dreist-commons** (`../dreist-commons`, private
`koeves/dreist-commons`): the shared crates below except `dreist-plugin` and
`dreist-cli` live there. Dreist installs its profile (names, resources,
`.dreist*` save family, settings folder `Dreist`, migrated from `Geist-rs`) at
start-up.

## Crates

| Crate | Purpose |
|---|---|
| `dreist-formats` (commons) | file formats (projects, kits, patterns, presets), resource paths, the app profile |
| `dreist-dsp` (commons) | voices, filters, modulators, timestretch, the 47 effects |
| `dreist-engine` (commons) | sequencer, mixer, modulation, song, scenes, sampler, MIDI, export |
| `dreist-gui` (commons) | skin-driven UI toolkit (baseview + softbuffer + tiny-skia) |
| `dreist-editor` (commons) | the editor panels and their behaviour |
| `dreist-plugin` | nih-plug VST3 / CLAP plugin and the standalone app |
| `dreist-cli` | command-line tools: `dreist-inspect` (check a file's samples), `dreist-render` (offline render to WAV), `dreist-nulltest` / `dreist-stemfit` / `dreist-bands` (compare renders) |
| `dreist-testkit` (commons) | test helpers: golden fingerprints, signal checks, allocation counting |
| `xtask` | nih-plug bundler (`cargo xtask bundle dreist-plugin`) |

dreist-commons' `vendor/` holds patched baseview and signalsmith-stretch
(`[patch]` entries in `Cargo.toml`). `assets/ui` is Dreist's generated UI.
`assets/factory` holds the original's factory effect presets, effect chains and
pattern/swing templates (bundled).

## Quick commands

    cargo test --workspace            # app crates; the shared crates test in ../dreist-commons
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

Private reverse-engineering notes live in `koeves/dreist-re` (`dreist/`), for
those with access. The shared crates' tests and goldens run in dreist-commons.
