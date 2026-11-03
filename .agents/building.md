# Building, testing, running

A Rust stable toolchain. On macOS with Homebrew rustup, cargo may not be on
`PATH`: `export PATH=$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:$PATH`.

## Build

macOS:

    scripts/build.sh              # release: target/bundled/Dreist.{app,vst3,clap}
    scripts/build.sh --debug
    scripts/build.sh --install    # also into ~/Library/Audio/Plug-Ins and ~/Applications

Windows (Git Bash, as CI runs it):

    scripts/build-windows.sh      # target/bundled/Dreist.vst3, Dreist-CLAP/, Dreist-App/

The `.exe` and `.clap` are bare files on Windows, so their resources sit in a
`Resources/` folder beside them (`dreist_formats::paths`).

## Run

    cargo run -p dreist-plugin --features standalone --bin dreist-standalone --release
    cargo run -p dreist-editor --features window --example editor -- [project.geist]   # editor window, no audio
    cargo run -p dreist-cli --bin dreist-inspect -- <file.geist|file.geistkit>
    cargo run -p dreist-cli --bin dreist-render --release -- <file.geist> <out.wav> [seconds]

Resources resolve through `dreist_formats::paths`: `DREIST_RESOURCES` /
`DREIST_UI`, then the bundle's [re:3b3416] (or
`Resources/` beside a Windows binary), then the repository's `assets/`.

## Content

Dreist ships no samples. Content comes from the original's packs (the
factory/starter content). The browser reads `DREIST_CONTENT`, else
`Content` in the documents folder (default `dreist_formats::legacy::DOCUMENTS_DIR`
under the home folder, option `LocalDocumentsPath`). Many tests use the factory content when it is
installed and skip quietly when it is not (CI has none).

Keep the content outside iCloud-synced folders, or mark it "Keep
Downloaded": evicted files are downloaded on first read, which turns the
editor suite's seconds into many minutes.

## Tests

The shared crates (and their goldens) are the `commons` submodule's own
workspace; this repository tests the plugin and CLI, and runs the shared suite
against Dreist's assets:

    cargo test --workspace
    DREIST_UI=$PWD/assets/ui DREIST_RESOURCES=$PWD/assets/factory cargo test --manifest-path commons/Cargo.toml --workspace
    cargo test --manifest-path commons/Cargo.toml -p dreist-engine --test realtime  # no heap use on the audio path
    cargo test --manifest-path commons/Cargo.toml -p dreist-dsp --test fx_harness   # effect fingerprints

Golden fingerprints live in `commons/crates/*/tests/golden/` (`fx.txt`,
`engine.txt`) and `crates/dreist-editor/tests/golden/screens.txt`. After an intended change to audio or rendering,
regenerate them and review the diff:

    UPDATE_GOLDEN=1 cargo test -p dreist-editor --lib screens_match_fingerprints

`effects_match_fingerprints` hashes float output and only matches on macOS;
CI runs it as a separate, non-fatal step elsewhere. `ALLOC_TRACE=1` makes the
realtime tests report where allocations happen.
