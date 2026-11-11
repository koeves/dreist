#!/usr/bin/env bash
# Build Dreist on Linux (x86_64, X11): VST3 + CLAP and the standalone app.
#
#   scripts/build-linux.sh            release build into target/bundled/
#   scripts/build-linux.sh --debug    debug build
#   scripts/build-linux.sh --install  also install for this user (below)
#
# Output: target/bundled/Dreist.vst3 (Contents/x86_64-linux/Dreist.so,
# resources in Contents/Resources), target/bundled/Dreist-CLAP/
# (Dreist.clap + Resources/) and target/bundled/Dreist-App/ (Dreist +
# Resources/ + dreist.desktop). The .clap and the app are bare files, so
# Dreist's profile looks for `Resources/` next to them (as on Windows).
#
# --install: ~/.vst3/Dreist.vst3, ~/.clap/Dreist/ (hosts search ~/.clap
# recursively), the app in ~/.local/share/Dreist/ with ~/.local/bin/dreist
# linking to it, and a desktop entry and icon under ~/.local/share.
#
# Needs pkg-config and the ALSA, X11, XCB and OpenGL headers (README).
set -euo pipefail

cd "$(dirname "$0")/.."

profile=release
install=0
for a in "$@"; do
    case "$a" in
        --debug) profile=debug ;;
        --install) install=1 ;;
        -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
        *) echo "unknown option: $a" >&2; exit 2 ;;
    esac
done
flag=$([ "$profile" = release ] && echo --release || true)
out=target/bundled
mkdir -p "$out"

echo "==> VST3 / CLAP ($profile)"
cargo run --package xtask --release -- bundle dreist-plugin $flag

echo "==> Standalone app ($profile)"
cargo build -p dreist-plugin --features standalone --bin dreist-standalone $flag

clap="$out/Dreist-CLAP"
app="$out/Dreist-App"
rm -rf "$clap" "$app"
mkdir -p "$clap/Resources" "$app/Resources" "$out/Dreist.vst3/Contents/Resources"
mv "$out/Dreist.clap" "$clap/Dreist.clap"
cp "target/$profile/dreist-standalone" "$app/Dreist"
cp assets/ui/AppIcon.png "$app/dreist.png"
cat > "$app/dreist.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Dreist
Comment=Drum sampler, sequencer and performance instrument
Exec=dreist
Icon=dreist
Terminal=false
Categories=AudioVideo;Audio;Music;
DESKTOP

echo "==> Resources"
for r in "$out/Dreist.vst3/Contents/Resources" "$clap/Resources" "$app/Resources"; do
    rm -rf "$r/Factory" "$r/Dreist"
    cp -R assets/factory "$r/Factory"
    cp -R assets/ui "$r/Dreist"
    rm -f "$r/Dreist/preview.png" "$r/Dreist/AppIcon.png" "$r/Dreist/AppIcon.icns"
done
for d in "$out/Dreist.vst3/Contents/Resources" "$clap" "$app"; do
    cp LICENSE LICENSE-GPL-3.0 THIRD_PARTY_NOTICES.md "$d/"
done

if [ "$install" = 1 ]; then
    echo "==> Installing"
    share="${XDG_DATA_HOME:-$HOME/.local/share}"
    mkdir -p "$HOME/.vst3" "$HOME/.clap" "$share" "$HOME/.local/bin" "$share/applications" "$share/icons/hicolor/256x256/apps"
    rm -rf "$HOME/.vst3/Dreist.vst3" "$HOME/.clap/Dreist" "$share/Dreist"
    cp -R "$out/Dreist.vst3" "$HOME/.vst3/"
    cp -R "$clap" "$HOME/.clap/Dreist"
    cp -R "$app" "$share/Dreist"
    ln -sf "$share/Dreist/Dreist" "$HOME/.local/bin/dreist"
    cp "$app/dreist.desktop" "$share/applications/dreist.desktop"
    cp "$app/dreist.png" "$share/icons/hicolor/256x256/apps/dreist.png"
fi

echo "==> Done"
ls -d "$out"/Dreist*
