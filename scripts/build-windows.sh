#!/usr/bin/env bash
# Build Dreist on Windows (Git Bash): VST3 + CLAP and the standalone .exe.
#
#   scripts/build-windows.sh            release build into target/bundled/
#   scripts/build-windows.sh --debug    debug build
#
# Output: target/bundled/Dreist.vst3 (resources in Contents/Resources),
# target/bundled/Dreist-CLAP/ (Dreist.clap + Resources/) and
# target/bundled/Dreist-App/ (Dreist.exe + Resources/). The .clap and .exe
# are bare files, so geist_formats::paths looks for `Resources/` next to them.
set -euo pipefail

cd "$(dirname "$0")/.."

profile=release
for a in "$@"; do
    case "$a" in
        --debug) profile=debug ;;
        -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
        *) echo "unknown option: $a" >&2; exit 2 ;;
    esac
done
flag=$([ "$profile" = release ] && echo --release || true)
out=target/bundled
mkdir -p "$out"

echo "==> VST3 / CLAP ($profile)"
cargo run --package xtask --release -- bundle geist-plugin $flag

echo "==> Standalone app ($profile)"
cargo build -p geist-plugin --features standalone --bin geist-standalone $flag

clap="$out/Dreist-CLAP"
app="$out/Dreist-App"
rm -rf "$clap" "$app"
mkdir -p "$clap/Resources" "$app/Resources" "$out/Dreist.vst3/Contents/Resources"
mv "$out/Dreist.clap" "$clap/Dreist.clap"
cp "target/$profile/geist-standalone.exe" "$app/Dreist.exe"

echo "==> Resources"
for r in "$out/Dreist.vst3/Contents/Resources" "$clap/Resources" "$app/Resources"; do
    rm -rf "$r/Geist2" "$r/Dreist"
    cp -R assets/geist2 "$r/Geist2"
    cp -R assets/dreist "$r/Dreist"
    rm -f "$r/Dreist/preview.png" "$r/Dreist/AppIcon.png" "$r/Dreist/AppIcon.icns"
done
for d in "$out/Dreist.vst3/Contents/Resources" "$clap" "$app"; do
    cp LICENSE LICENSE-GPL-3.0 THIRD_PARTY_NOTICES.md "$d/"
done

echo "==> Done"
ls -d "$out"/Dreist*
