# Conventions

- **Format**: `cargo fmt --all` (`rustfmt.toml`: 200 columns, "Max" small
  heuristics). CI fails on unformatted code.
- **Lints**: `cargo clippy --workspace --all-targets -- -D warnings`. The
  workspace allows a few lints on purpose (`[workspace.lints.clippy]` in
  `Cargo.toml`): the DSP is transcribed from the original, so it keeps the
  binary's constants and operation order, and explicit min/max where `clamp`
  would treat NaN differently. Keep that style in `geist-dsp` and
  `geist-engine`.
- **Fidelity**: behaviour matches Geist2, including its integer wrapping and
  rounding. Comments name the original function (and address) a piece of code
  follows, e.g. `` `Geist::SetupMetronome` 0x164b80 ``; keep them when editing.
- **Realtime safety**: once warmed up, the audio path (engine processing,
  effects, voices) must not allocate, reallocate or free. Prepare buffers when the engine is (re)built; hand work to the
  editor/worker side through the existing message queues.
  `crates/geist-engine/tests/realtime.rs` and
  `crates/geist-dsp/tests/fx_realtime.rs` enforce this with
  `geist_testkit::CountingAlloc`.
- **Errors**: file and format code returns `Result` (`geist_formats::Error`,
  via `thiserror`); loading a damaged or missing file degrades (missing
  samples are reported in the UI) rather than panicking. Avoid `unwrap` on
  anything read from user files.
- **Tests**: unit tests sit next to the code; integration tests in
  `crates/*/tests`. Tests that need the factory content return early when it
  is absent. Timing-based assertions must tolerate slow CI machines.
- **Platform code**: macOS specifics go behind `cfg(target_os = "macos")`
  (AppKit via `objc` in `geist-gui`), with a fallback for other platforms;
  paths go through `geist_formats::paths`, not hard-coded home folders.
