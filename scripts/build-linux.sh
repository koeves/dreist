#!/usr/bin/env bash
# Build Dreist on Linux (x86_64, X11): VST3 + CLAP and the standalone app.
#
#   scripts/build-linux.sh            release build into target/bundled/
#   scripts/build-linux.sh --debug    debug build
#   scripts/build-linux.sh --install  also install for this user (below)
#   scripts/build-linux.sh --uninstall  remove what --install put in place
#
# Output: target/bundled/Dreist.vst3 (Contents/x86_64-linux/Dreist.so,
# resources in Contents/Resources), target/bundled/Dreist-CLAP/
# (Dreist.clap + Resources/), target/bundled/Dreist-App/ (Dreist +
# Resources/ + dreist.desktop + icons/) and target/bundled/install.sh. The
# .clap and the app are bare files, so Dreist's profile looks for
# `Resources/` next to them (as on Windows).
#
# --install and --uninstall run that install.sh (scripts/linux-install.sh,
# which the release tarball also carries; it lists what goes where).
#
# Needs pkg-config and the ALSA, X11, XCB and OpenGL headers (README).
set -euo pipefail

cd "$(dirname "$0")/.."

profile=release
install=0
uninstall=0
for a in "$@"; do
    case "$a" in
        --debug) profile=debug ;;
        --install) install=1 ;;
        --uninstall) uninstall=1 ;;
        -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
        *) echo "unknown option: $a" >&2; exit 2 ;;
    esac
done

if [ "$uninstall" = 1 ]; then
    exec sh scripts/linux-install.sh --uninstall
fi
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
cp -R assets/linux/icons "$app/icons"
cp scripts/linux-install.sh "$out/install.sh"
chmod +x "$out/install.sh"
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
    sh "$out/install.sh"
fi

echo "==> Done"
ls -d "$out"/Dreist*
