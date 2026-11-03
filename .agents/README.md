# Dreist: guide for contributors and coding agents

Dreist is a drum sampler, step sequencer and performance instrument written in
Rust. It is compatible with FXpansion Geist2 (2.1.2.13): it loads Geist2
`.geist` projects, kits and patterns and plays them the same way. It builds as
VST3, CLAP and a standalone app for macOS (Apple Silicon) and Windows (x64).

The UI is branded "Dreist" (Dreist's app profile, `dreist-plugin/src/profile.rs`).
Outside README files, code, comments and docs carry no original product, vendor
or class names; legacy on-disk names live in `dreist_formats::legacy`, and RE
evidence is cited by tag (`[re:xxxxxx]`, map in `koeves/dreist-re`).

Dreist is a thin app on **dreist-commons** (`koeves/dreist-commons`, a git
submodule at `commons`, used by path): the shared crates below marked
"commons" live there. Dreist installs its profile (names, resources,
`.dreist*` save family, settings folder `Dreist`, migrated from `Geist-rs`) at
start-up.

## Crates

| Crate | Purpose |
|---|---|
| `dreist-formats` (commons) | file formats (projects, kits, patterns, presets), resource paths, the app profile |
| `dreist-dsp` (commons) | voices, filters, modulators, timestretch, the 47 effects |
| `dreist-engine` (commons) | sequencer, mixer, modulation, song, scenes, sampler, MIDI, export |
| `dreist-gui` (commons) | skin-driven UI toolkit (baseview + softbuffer + tiny-skia) |
| `dreist-editor` | the editor panels and their behaviour (Dreist's own; `src/app.rs` holds the About text, settings folder, effect menu and document readers) |
| `dreist-plugin` | nih-plug VST3 / CLAP plugin and the standalone app |
| `dreist-cli` | command-line tools: `dreist-inspect` (check a file's samples), `dreist-render` (offline render to WAV), `dreist-nulltest` / `dreist-stemfit` / `dreist-bands` (compare renders) |
| `dreist-testkit` (commons) | test helpers: golden fingerprints, signal checks, allocation counting |
| `xtask` | nih-plug bundler (`cargo xtask bundle dreist-plugin`) |

dreist-commons' `vendor/` holds patched baseview and signalsmith-stretch
(`[patch]` entries in `Cargo.toml`). `assets/ui` is Dreist's generated UI.
`assets/factory` holds the original's factory effect presets, effect chains and
pattern/swing templates (bundled).

## Quick commands

    cargo test --workspace            # app crates
    cargo test --manifest-path commons/Cargo.toml --workspace   # shared crates, against assets/ via DREIST_UI / DREIST_RESOURCES
    cargo fmt --all --check
    cargo clippy --workspace --all-targets -- -D warnings
    scripts/build.sh                  # macOS bundles into target/bundled/
    scripts/build-windows.sh          # Windows (Git Bash)

## Commits

[git.md](git.md): Conventional Commits, no AI attribution, the changelog,
releases and commons submodule bumps. Keep the repository private
(`koeves/dreist`).

## More

- [building.md](building.md): build, test and run on macOS and Windows; content; test goldens.
- [ui.md](ui.md): the generated skins, styles and icons; UI screenshots.
- [git.md](git.md): commits, changelog, releases, the commons submodule.
- [release.md](release.md): the release workflow, signing, third-party notices.
- [conventions.md](conventions.md): formatting, lints, realtime safety, errors, comments.

Private reverse-engineering notes live in `koeves/dreist-re` (`dreist/`), for
those with access. The shared crates' tests and goldens run in dreist-commons
and, against Dreist's assets, in Dreist's CI.
