#!/usr/bin/env bash
# Build Dreist: VST3 + CLAP bundles and the standalone macOS app.
#
#   scripts/build.sh            release build into target/bundled/
#   scripts/build.sh --debug    debug build
#   scripts/build.sh --install  also install for this user (target/bundled/install.sh)
#   scripts/build.sh --uninstall  remove that install
#
# Output: target/bundled/Dreist.vst3, Dreist.clap, Dreist.app and install.sh
# (commons/packaging/install.sh, which the release archive also carries;
# commons/packaging/README.md lists what goes where).
#
# Signing: ad-hoc by default. With DREIST_SIGN_IDENTITY set (a "Developer
# ID Application: ..." identity in the keychain) the bundles are signed
# with the hardened runtime and a timestamp; with DREIST_NOTARY_PROFILE
# also set (a `xcrun notarytool store-credentials` profile) they are
# notarised and stapled.
set -euo pipefail

cd "$(dirname "$0")/.."
export PATH="$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:$HOME/.cargo/bin:$PATH"

profile=release
install=0
uninstall=0
for a in "$@"; do
    case "$a" in
        --debug) profile=debug ;;
        --install) install=1 ;;
        --uninstall) uninstall=1 ;;
        -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
        *) echo "unknown option: $a" >&2; exit 2 ;;
    esac
done
if [ "$uninstall" = 1 ]; then
    exec sh commons/packaging/install.sh --app Dreist --uninstall
fi
flag=$([ "$profile" = release ] && echo --release || true)
# The version the bundles and the About panel show (scripts/version.sh).
export BUILD_VERSION=$(scripts/version.sh)
version=${BUILD_VERSION%%+*}
out=target/bundled
mkdir -p "$out"

echo "==> VST3 / CLAP ($profile)"
cargo run --package xtask --release -- bundle dreist-plugin $flag

echo "==> Standalone app ($profile)"
cargo build -p dreist-plugin --features standalone --bin dreist-standalone $flag
app="$out/Dreist.app"
rm -rf "$app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp "target/$profile/dreist-standalone" "$app/Contents/MacOS/Dreist"
cat > "$app/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key><string>Dreist</string>
    <key>CFBundleDisplayName</key><string>Dreist</string>
    <key>CFBundleExecutable</key><string>Dreist</string>
    <key>CFBundleIdentifier</key><string>rs.dreist.standalone</string>
    <key>CFBundleIconFile</key><string>AppIcon</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleShortVersionString</key><string>$version</string>
    <key>CFBundleVersion</key><string>$version</string>
    <key>LSMinimumSystemVersion</key><string>11.0</string>
    <key>NSHighResolutionCapable</key><true/>
    <key>NSMicrophoneUsageDescription</key><string>Dreist records audio input with its sampler.</string>
</dict>
</plist>
PLIST
# App icon (assets/ui/AppIcon.icns, drawn by scripts/icon.py).
cp assets/ui/AppIcon.icns "$app/Contents/Resources/AppIcon.icns"

# Bundle the resources (assets/factory: the factory presets, effect chains
# and templates) into every bundle's Contents/Resources/Factory, and
# Dreist's own UI graphics (assets/ui: skin, fonts, cursors, metronomes)
# into Contents/Resources/Dreist, where Dreist's profile looks first.
echo "==> Resources"
for b in "$app" "$out/Dreist.vst3" "$out/Dreist.clap"; do
    mkdir -p "$b/Contents/Resources"
    rm -rf "$b/Contents/Resources/Factory" "$b/Contents/Resources/Dreist"
    cp -R assets/factory "$b/Contents/Resources/Factory"
    cp -R assets/ui "$b/Contents/Resources/Dreist"
    rm -f "$b/Contents/Resources/Dreist/preview.png" "$b/Contents/Resources/Dreist/AppIcon.png" "$b/Contents/Resources/Dreist/AppIcon.icns"
done
# Licence and notices travel with every bundle.
for b in "$app" "$out/Dreist.vst3" "$out/Dreist.clap"; do
    cp LICENSE LICENSE-GPL-3.0 THIRD_PARTY_NOTICES.md "$b/Contents/Resources/"
done
for b in "$app" "$out/Dreist.vst3" "$out/Dreist.clap"; do
    if [ -n "${DREIST_SIGN_IDENTITY:-}" ]; then
        echo "==> Signing $b"
        codesign --force --deep --options runtime --timestamp --sign "$DREIST_SIGN_IDENTITY" "$b"
    else
        codesign --force --deep --sign - "$b" >/dev/null 2>&1 || echo "warning: ad-hoc codesign failed for $b" >&2
    fi
done
if [ -n "${DREIST_SIGN_IDENTITY:-}" ] && [ -n "${DREIST_NOTARY_PROFILE:-}" ]; then
    for b in "$app" "$out/Dreist.vst3" "$out/Dreist.clap"; do
        echo "==> Notarising $b"
        zip="$out/$(basename "$b").zip"
        rm -f "$zip"
        ditto -c -k --keepParent "$b" "$zip"
        xcrun notarytool submit "$zip" --keychain-profile "$DREIST_NOTARY_PROFILE" --wait
        xcrun stapler staple "$b"
        rm -f "$zip"
    done
fi

cp commons/packaging/install.sh "$out/install.sh"
chmod +x "$out/install.sh"

if [ "$install" = 1 ]; then
    echo "==> Installing"
    sh "$out/install.sh"
fi

echo "==> Done"
ls -d "$out"/Dreist.*
