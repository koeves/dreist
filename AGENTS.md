# Dreist

Dreist is a drum sampler, step sequencer and performance instrument written in Rust. It loads the
original's `.geist` projects, kits and patterns and plays them the same way, and builds as VST3, CLAP
and a standalone app for macOS (Apple Silicon), Windows (x64) and Linux (x86_64). It is a thin app on
**dreist-commons** (submodule at `commons`, used by path): Dreist installs its profile (names,
resources, `.dreist*` save family, settings folder `Dreist`) at start-up. Shared behaviour belongs in
dreist-commons, Dreist specifics here.

- Outside README files: no original product, vendor or class names in code, comments or docs; legacy
  on-disk names live in `dreist_formats::legacy`. Cite reverse-engineering evidence by tag
  (`[re:xxxxxx]`, map and notes in the private `koeves/dreist-re`, `dreist/`) and keep the tags when
  editing. Behaviour matches the original, including its integer wrapping and rounding.
- Commits, changelog, releases, branches and the commons submodule:
  `CONTRIBUTING.md`.
- Nothing may come to the front while the desktop is in use: tests and harnesses set
  `DREIST_BACKGROUND_GUI=1`, apps start with `open -g`.
- Branches: `feature/<name>` (one worktree each, outside the checkout) -> pull request into
  `dev` (squash only; the PR title is the Conventional Commit; checks green) -> release pull request `dev` -> `main` (merge commit). The
  merge releases: version from the commits (`Release-As: X.Y.Z` overrides), tag, build, GitHub
  release and a follow-up changelog / version pull request into `dev` happen on their own; never
  tag or bump by hand. `commons` must be at a dreist-commons release tag (CONTRIBUTING.md).
- After any code change here or in commons, rebuild and reinstall the VST3
  (`scripts/build.sh --install`, or copy `target/bundled/Dreist.vst3` to
  `~/Library/Audio/Plug-Ins/VST3`) and say which commit is installed.

## Crates

| Crate | Purpose |
|---|---|
| `dreist-formats` (commons) | file formats, resource paths, the app profile |
| `dreist-dsp` (commons) | voices, filters, modulators, timestretch, the 47 effects |
| `dreist-engine` (commons) | sequencer, mixer, modulation, song, scenes, sampler, MIDI, export |
| `dreist-gui` (commons) | skin-driven UI toolkit (baseview + softbuffer + tiny-skia) |
| `dreist-editor` | the editor panels and their behaviour (`src/app.rs`: About text, settings folder, effect menu, document readers) |
| `dreist-plugin` | nih-plug VST3 / CLAP plugin and the standalone app |
| `dreist-cli` | `dreist-inspect`, `dreist-render`, `dreist-nulltest` / `dreist-stemfit` / `dreist-bands` |
| `dreist-testkit` (commons) | golden fingerprints, signal checks, allocation counting |
| `xtask` | nih-plug bundler |

`assets/ui` is the generated UI; `assets/factory` holds the original's factory effect presets,
chains and pattern / swing templates (bundled).

Security alerts: check the open code scanning and Dependabot alerts at the start and end of any
work here (`gh api repos/koeves/dreist/code-scanning/alerts?state=open`, same for
`dependabot/alerts`); fix real findings through an issue and a PR, dismiss false positives
with the reason.

## Docs

- Human docs (README, CONTRIBUTING, other `.md` for readers) follow the fzf README style: a centred title with release, build, CodeQL, licence and platform badges under it.
- Short bullets of one sentence, two at most; no walls of text, and detail goes in its own section or file.
- Describe the project as it is: no status updates, no "now", "previously", "since" or "next release" wording, and nothing the reader doesn't need.
- This file is the agent instructions for every agent; `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` only point here, so edit this file.
- Agent notes stay in this file or in dreist-re; CHANGELOG.md and THIRD_PARTY_NOTICES.md are left to their generators.

## Build, run, test

    export PATH=$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:$PATH
    scripts/build.sh                  # release: target/bundled/Dreist.{app,vst3,clap}; --debug, --install
    scripts/build-windows.sh          # Windows (Git Bash)
    scripts/build-linux.sh            # Linux
    cargo run -p dreist-plugin --features standalone --bin dreist-standalone --release
    cargo run -p dreist-editor --features window --example editor -- [project.geist]
    cargo test --workspace
    DREIST_UI=$PWD/assets/ui DREIST_RESOURCES=$PWD/assets/factory cargo test --manifest-path commons/Cargo.toml --workspace
    cargo clippy --workspace --all-targets -- -D warnings
    cargo fmt --all --check

Resources resolve through `dreist_formats::paths`: `DREIST_RESOURCES` / `DREIST_UI`, then the bundle,
then the repository's `assets/`. Content (no samples are shipped) comes from the original's packs:
`DREIST_CONTENT`, else `Content` in the documents folder; tests that need it skip without it.

Goldens: `commons/crates/*/tests/golden/` and `crates/dreist-editor/tests/golden/screens.txt`. They
stay identical unless a change means to alter them; then `UPDATE_GOLDEN=1 cargo test -p dreist-editor
--lib screens_match_fingerprints` and say why in the commit. `effects_match_fingerprints` matches only
on macOS.

## Conventions

- `cargo fmt` (200 columns), clippy clean; the workspace allows a few lints on purpose because the DSP
  keeps the original's constants and operation order.
- Realtime safety: once warmed up, the audio path does not allocate or free (`realtime.rs`,
  `fx_realtime.rs` enforce it with `CountingAlloc`).
- File and format code returns `Result` and degrades on damaged or missing files; no `unwrap` on user
  data. macOS specifics behind `cfg(target_os = "macos")` with a fallback; paths via
  `dreist_formats::paths`.

## UI

Everything in `assets/ui` is generated by `scripts/uigen/uigen.py` (skins in `scripts/uigen/skins/`,
styles and themes in `theme.py`; needs `skia-python==144.1`, `fonttools==4.68.0`); edit the generator,
never the generated files, and check with `uigen.py --check`. Layouts, sizes and labels follow the
shipped original's skin; graphics are Dreist's own vector art, never copied bitmaps. Look at the
result with `cargo run -p dreist-editor --example editorshot -- [project] [out.png] [scale] [tab]`
(options at the top of `crates/dreist-editor/examples/editorshot.rs`).
