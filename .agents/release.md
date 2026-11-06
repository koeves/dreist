# Releases

1. Make sure `main` is green (`.github/workflows/ci.yml`: fmt, clippy, tests,
   `uigen --check`, notices check on Linux; plugin and app build on macOS).
2. Update `CHANGELOG.md` and the version, commit `chore(release): vX.Y.Z`,
   tag `vX.Y.Z` and push the tag ([git.md](git.md)).
3. The tag triggers `.github/workflows/release.yml`: on macOS and Windows it
   runs the tests, builds VST3, CLAP and the standalone app, zips them as
   `Dreist-<tag>-<macOS|Windows>-<VST3|CLAP|App>.zip`, then publishes the
   release with the tag's `CHANGELOG.md` section and the zips.

To rebuild a release's assets, run the workflow by hand:
`gh workflow run release.yml --ref <tag> -f tag=<tag> -f upload=true`
(without `upload=true` it only builds and keeps the zips as run artifacts).

## Signing

Builds are unsigned. On macOS `scripts/build.sh` signs ad hoc; with
`DREIST_SIGN_IDENTITY` (a Developer ID Application identity) it signs with the
hardened runtime, and with `DREIST_NOTARY_PROFILE` too it notarises and
staples. The release workflow sets neither, so users right-click › Open the
app (see the README). Windows binaries are unsigned (SmartScreen warns).

## Third-party notices

`THIRD_PARTY_NOTICES.md` is generated from `cargo metadata` plus the vendored
code and fonts listed in `scripts/notices.py`:

    python3 scripts/notices.py            # rewrite after dependency changes
    python3 scripts/notices.py --check    # CI

Licences: the crates are MIT OR Apache-2.0; `dreist-plugin` and the binaries
are GPL-3.0-or-later (nih-plug's VST3 bindings). See `LICENSE`.
