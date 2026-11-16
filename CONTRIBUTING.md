# Contributing

## Commits

- **Format**: [Conventional Commits](https://www.conventionalcommits.org/), `type(scope): summary`, with `!` after the type for a breaking change.
- **Types**: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `revert`.
- **Scope and body**: a short scope (a crate or area); a body only when the why is not obvious, wrapped at 72 columns.
- **Checked**: by the `conventional` check; the changelog and release notes are generated from the commits.

## Branches and pull requests

- **Work**: on `feature/<name>`, one worktree per branch in `.claude/worktrees/<name>`.
- **Into `dev`**: a pull request, squash-merged; its title is the Conventional Commit.
- **Drafts**: longer work opens as a draft pull request, marked ready once its testing is done; short work goes from a local branch straight to a ready pull request.
- **Issues**: for features, bug reports and work spanning several pull requests or repos; the pull request links it with `Closes #N`.
- **No issue**: small fixes, docs, chores and dependency bumps go straight to a pull request with a conventional title.
- **Board**: features and larger work for all three repos are tracked on [Dreist & Einst](https://github.com/users/koeves/projects/1).
- **Rules**: `dev` and `main` take changes only through pull requests with green checks.
- **Dependabot**: targets `dev`; patch, minor, Actions and submodule updates merge on their own when green.

## Checks

Run them before pushing:

```bash
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
python3 scripts/uigen/uigen.py --check
```

- **CI**: pull requests into `dev` run `checks` and `linux-build` (builds, tests and bundles on Linux); the release pull request and the release also run `macos`.
- **Docs only**: a pull request that changes only Markdown skips the build and test jobs; a skipped job counts as passed.
- **CodeQL**: runs on every pull request into `dev` and `main`.
- **Goldens**: `commons/crates/*/tests/golden/` and `crates/dreist-editor/tests/golden/screens.txt` stay identical unless a change means to alter them.
- **Updating goldens**: `UPDATE_GOLDEN=1`, and say why in the commit.

## Development

```bash
scripts/build.sh                  # target/bundled/Dreist.{app,vst3,clap}; --debug, --install
cargo run -p dreist-plugin --features standalone --bin dreist-standalone --release
DREIST_UI=$PWD/assets/ui DREIST_RESOURCES=$PWD/assets/factory cargo test --manifest-path commons/Cargo.toml --workspace
```

- **Resources**: found through `DREIST_RESOURCES` / `DREIST_UI`, the bundle, then `assets/`.
- **Content**: tests that need the original's content packs skip without them (`DREIST_CONTENT` sets the location).
- **Code style**: `cargo fmt` (200 columns) and clippy clean.
- **Behaviour**: matches the original; cite reverse-engineering evidence by `[re:xxxxxx]` tag.
- **Names**: no original product or vendor names outside README files.
- **Audio path**: does not allocate once warmed up (`realtime.rs`, `fx_realtime.rs`).
- **Files**: file code returns `Result` and degrades on damaged files.

## UI

- **Generated**: everything in `assets/ui` comes from `scripts/uigen/uigen.py` (`skia-python==144.1`, `fonttools==4.68.0`).
- **Edits**: change the generator, never the generated files; `--check` fails when they are stale.
- **Look**: layouts, sizes and labels follow the original's skin; graphics are Dreist's own vector art.

## Releases

- **Release pull request into `dev`**: after every push to `dev` with releasable commits, `release-pr.yml` opens or updates `chore(release): vX.Y.Z` with the version and its CHANGELOG section; approving and merging it decides the release.
- **By hand**: `.github/release/prepare.sh` writes the same pull request (`--as X.Y.Z` sets the version, `--dry-run` tries it locally).
- **Version**: from the commits since the last tag: fix → patch, feat → minor, breaking → major (minor while on 0.x); `--as X.Y.Z` or a `Release-As: X.Y.Z` line in a commit sets it.
- **Releasable**: feat, fix, perf, refactor, revert, breaking and dependency commits; `ci`, `docs`, `test`, `style` and other commits alone release nothing.
- **Release**: once that is merged, `release-pr.yml` opens the pull request from `dev` into `main`, merged with a merge commit; its `release-version` check needs the prepared version and changelog and no releasable commit after them.
- **Automatic**: the merge tags `vX.Y.Z`, builds macOS, Windows and Linux and publishes the GitHub release; the changelog and version are already in `dev`.
- **Rebuild assets**: `gh workflow run release.yml --ref <tag> -f tag=<tag> -f upload=true`.

## dreist-commons

- **Submodule**: the shared crates are at `commons`; clone with `--recursive`.
- **Changes**: land in dreist-commons first, then bump the pointer here as `build: dreist-commons <sha or vX.Y.Z>`.
- **One app's behaviour**: stays behind its profile or opt-in style attributes; run both apps' tests against the change.
- **Releases**: `commons` must be at a dreist-commons release tag; release dreist-commons first.

## Builds

- **Signing**: `scripts/build.sh` signs ad hoc on macOS; `DREIST_SIGN_IDENTITY` (Developer ID) signs with the hardened runtime, `DREIST_NOTARY_PROFILE` also notarises.
- **Release builds**: unsigned on every system.
- **Third-party notices**: `THIRD_PARTY_NOTICES.md` is generated by `python3 scripts/notices.py`; CI runs `--check`.
