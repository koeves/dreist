# Git conventions

## Commits

- Subjects follow [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): summary`, imperative, lower-case summary, no trailing period.
  Types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`,
  `style`, `revert`; `!` after the type (or a `BREAKING CHANGE:` footer) for a breaking change.
- Scopes are optional and short: a crate or area (`dreist-plugin`, `dreist-cli`, `ui`, `notices`, `ci`).
- A body only when the why is not obvious; wrap at 72 columns.
- The release workflow checks every commit subject since the previous tag
  (`.github/workflows/commits.yml`).
- No AI attribution of any kind: no `Co-Authored-By` for an assistant, no session trailers, no
  "Generated with ..." lines, in commits, PRs, tags or release notes. Author and committer are
  the repository's configured identity.

## Changelog and releases

- `CHANGELOG.md` is generated with [git-cliff](https://git-cliff.org) (`cliff.toml`) from the
  commit subjects: `git cliff --unreleased --tag vX.Y.Z --prepend CHANGELOG.md`, then edit the
  new section by hand where it helps.
- Release: bump `version` in `Cargo.toml`, commit `chore(release): vX.Y.Z`, tag `vX.Y.Z`
  (annotated) and push the tag. The release workflow publishes the tag's `CHANGELOG.md`
  section as the release notes and attaches the macOS and Windows zips.

## dreist-commons submodule

The shared crates are the submodule at `commons` (Cargo uses them by path). Clone with
`--recursive`, or run `git submodule update --init`. To change them:

1. Commit and push in `commons/` (its own Conventional Commits), on its `main`.
2. Here: `git add commons` and commit `build: dreist-commons <short sha or vX.Y.Z>`.
3. Run this repository's checks; goldens must stay identical unless the change means to alter
   them (say why in the commit).

## Worktrees and cleanup

- Worktrees go next to the repository or in a scratch folder, never inside a checkout: the
  bundler builds the outermost workspace it finds, so a nested worktree bundles the outer
  checkout's code.
- Remove a worktree and its local branch once the branch is merged.
- When a task ends, delete what it built and no longer needs: `target/` directories
  (`cargo clean`), scratch builds, test copies and downloads. Keep only what is still in use.

## Branches and CI

GitHub Actions minutes are limited, so:

- All work goes to the `dev` branch; `main` only moves when the owner says a release is ready
  (merge `dev` into `main`, then tag).
- GitHub Actions run only when a release is made: pushing a `vX.Y.Z` tag runs the release workflow
  (the commit-subject check and the CI suite, then the builds and tests on macOS and Windows, then
  the release), and any workflow can be run by hand (`workflow_dispatch`). No workflow runs on a
  push to any branch (`main` included) or on pull requests (none are opened). So run the checks
  locally before every push: tests, clippy (with the standalone feature in the apps, with
  `dreist-gui/window` in commons) and `cargo fmt --check`.
- macOS jobs use the `macos-15` runner (GitHub no longer accepts `macos-14`).
- Until a release, the apps' `commons` submodule may point at dreist-commons `dev` commits. At
  release: merge dreist-commons `dev` into its `main` first, then point the apps at that commit
  and merge them.

## Shared code (dreist-commons)

One project's agents work on Dreist, Einst and dreist-commons, so no coordination log is kept.
Before changing commons: `git fetch` and rebase on its `dev`; keep one app's behaviour behind
that app's profile, rules or hooks; run both apps' tests and goldens against the change.
