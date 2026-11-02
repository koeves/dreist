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
`Resources/` folder beside them (`geist_formats::paths`).

## Run

    cargo run -p geist-plugin --features standalone --bin geist-standalone --release
    cargo run -p geist-editor --features window --example editor -- [project.geist]   # editor window, no audio
    cargo run -p geist-cli --bin geist-inspect -- <file.geist|file.geistkit>
    cargo run -p geist-cli --bin geist-render --release -- <file.geist> <out.wav> [seconds]

Resources resolve through `geist_formats::paths`: `GEIST2_RESOURCES` /
`DREIST_UI`, then the bundle's `Contents/Resources/{Geist2,Dreist}` (or
`Resources/` beside a Windows binary), then the repository's `assets/`.

## Content

Dreist ships no samples. Content comes from FXpansion's Geist2 packs (the
factory/starter content). The browser reads `GEIST2_CONTENT`, else
`Content` in the documents folder (default `~/Documents/FXpansion/Geist2`,
option `LocalDocumentsPath`). Many tests use the factory content when it is
installed and skip quietly when it is not (CI has none).

Keep the content outside iCloud-synced folders, or mark it "Keep
Downloaded": evicted files are downloaded on first read, which turns the
editor suite's seconds into many minutes.

## Tests

    cargo test --workspace
    cargo test -p geist-engine --test realtime     # no heap use on the audio path
    cargo test -p geist-dsp --test fx_harness      # effect fingerprints

Golden fingerprints live in `crates/*/tests/golden/` (`fx.txt`,
`engine.txt`, `screens.txt`). After an intended change to audio or rendering,
regenerate them and review the diff:

    UPDATE_GOLDEN=1 cargo test -p geist-editor --lib screens_match_fingerprints

`effects_match_fingerprints` hashes float output and only matches on macOS;
CI runs it as a separate, non-fatal step elsewhere. `ALLOC_TRACE=1` makes the
realtime tests report where allocations happen.
