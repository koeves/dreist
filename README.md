<div align="center">

# Dreist

[![Release](https://img.shields.io/github/v/release/koeves/dreist)](https://github.com/koeves/dreist/releases/latest)
[![Release](https://github.com/koeves/dreist/actions/workflows/release-on-main.yml/badge.svg?branch=main)](https://github.com/koeves/dreist/actions/workflows/release-on-main.yml?query=branch%3Amain)
[![CI](https://github.com/koeves/dreist/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/koeves/dreist/actions/workflows/ci.yml?query=branch%3Adev)
[![CodeQL](https://github.com/koeves/dreist/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/koeves/dreist/actions/workflows/codeql.yml?query=branch%3Amain)
[![License](https://img.shields.io/badge/license-GPL--3.0%20%7C%20MIT%2FApache--2.0-blue)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)](#install)
[![Formats](https://img.shields.io/badge/formats-VST3%20%7C%20CLAP%20%7C%20standalone-lightgrey)](#install)

</div>

Dreist is a drum sampler, step sequencer and performance instrument: a Rust rebuild of FXpansion
**Geist2** 2.1.2.13.

| | |
|---|---|
| ![Pattern editor](docs/screens/readme/dreist-pattern.png) | ![Scenes](docs/screens/readme/dreist-scenes.png) |
| ![Song mode](docs/screens/readme/dreist-song.png) | ![Transmod](docs/screens/readme/dreist-transmod.png) |

## Features

- **Instrument**: pads, layers, patterns, scenes, song mode and 47 effects.
- **Opens**: Geist2 `.geist` projects, kits and patterns.
- **Saves**: its own `.dreist` family (`.dreist`, `.dreistkit`, ...) in Geist2's XML.
- **Runs as**: VST3, CLAP and a standalone app on macOS, Windows and Linux.

## Install

Download the archive for your system from the [latest release](https://github.com/koeves/dreist/releases/latest), unpack it and run its install script in the unpacked folder.

| System | Requirements | Archive |
|---|---|---|
| macOS | 11+, Apple Silicon | `Dreist-<tag>-macOS-AppleSilicon.zip` |
| macOS | 11+, Intel | `Dreist-<tag>-macOS-Intel.zip` |
| Windows | 10+, x64 | `Dreist-<tag>-Windows.zip` |
| Linux | x86_64, glibc 2.39+, X11 or XWayland | `Dreist-<tag>-Linux.tar.gz` |

### macOS

```bash
./install.sh                # this user
sudo ./install.sh --system  # all users
```

- **First launch**: the builds are unsigned, so open the app with right-click › Open › Open.
- **Plugins blocked by a host**: `xattr -dr com.apple.quarantine ~/Library/Audio/Plug-Ins/VST3/Dreist.vst3 ~/Library/Audio/Plug-Ins/CLAP/Dreist.clap`.
- **REX files**: need the REX Shared Library (Reason Studios), and Rosetta 2 on Apple Silicon.

### Windows

```powershell
.\install.ps1          # all users, in an administrator PowerShell
.\install.ps1 --user   # this user
```

- **Blocked scripts**: `powershell -ExecutionPolicy Bypass -File .\install.ps1`.
- **First launch**: if SmartScreen warns about the unsigned build, choose More info › Run anyway.

### Linux

```bash
./install.sh                # this user
sudo ./install.sh --system  # all users
```

- **Launcher**: the app shows in the desktop's app list, and `dreist` starts it.
- **Runtime**: ALSA, OpenGL, X11 and XCB.

## Uninstall

```bash
./install.sh --uninstall           # macOS, Linux (sudo and --system for an all-users install)
.\install.ps1 --uninstall          # Windows (--user for a per-user install)
```

- **Kept**: settings, content and the diagnostics log, unless `--purge` is added.

## Files

| | macOS | Windows | Linux |
|---|---|---|---|
| App | `/Applications/Dreist.app` | `%ProgramFiles%\Dreist\` | `~/.local/share/Dreist/` |
| VST3 | `~/Library/Audio/Plug-Ins/VST3/Dreist.vst3` | `%CommonProgramFiles%\VST3\Dreist.vst3` | `~/.vst3/Dreist.vst3` |
| CLAP | `~/Library/Audio/Plug-Ins/CLAP/Dreist.clap` | `%CommonProgramFiles%\CLAP\Dreist\` | `~/.clap/Dreist/` |
| Settings | `~/Library/Application Support/Dreist` | `%APPDATA%\Dreist` | `~/.config/Dreist` |
| Log | `~/Library/Logs/Dreist/dreist.log` | `%LOCALAPPDATA%\Dreist\Logs\dreist.log` | `~/.local/state/Dreist/dreist.log` |

- **Other installs**: all-users paths on macOS and Linux and per-user paths on Windows are in the [locations table](https://github.com/koeves/dreist-commons/blob/dev/packaging/README.md#locations).
- **Sharing a problem**: main menu › Export diagnostics saves a copy of the log without your user name and private paths.

## Limitations

- **Samples**: none included. Dreist plays Geist2 content (kits, presets, expansions).
- **Drags out of the window**: macOS and Windows.
- **Drops into the window**: macOS and Windows only.
- **REX files**: macOS only.
- **Wayland**: through XWayland.
- **Unsigned builds**: macOS and Windows ask once before the first start.

## Building

```bash
git clone --recursive https://github.com/koeves/dreist
scripts/build.sh --install          # macOS
scripts/build-linux.sh --install    # Linux
scripts/build-windows.sh            # Windows, in Git Bash
```

- **Tools**: Rust through [rustup](https://rustup.rs), plus the Xcode Command Line Tools on macOS and Visual Studio Build Tools (C++) with LLVM on Windows.
- **Linux packages** (Debian / Ubuntu): `sudo apt-get install build-essential clang libclang-dev pkg-config libasound2-dev libjack-jackd2-dev libx11-dev libx11-xcb-dev libxcb1-dev libxcb-icccm4-dev libxcb-dri2-0-dev libxcursor-dev libgl1-mesa-dev`.
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md).

## Related projects

- [dreist-commons](https://github.com/koeves/dreist-commons): the shared formats, DSP, engine and GUI crates.
- [Einst](https://github.com/koeves/einst): the Geist v1 rebuild on the same crates.

## Licence

- **Crates**: MIT OR Apache-2.0.
- **`dreist-plugin` and the binaries built from it**: GPL-3.0-or-later.
- **Details**: [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- Dreist is not affiliated with or endorsed by FXpansion.
