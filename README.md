# Dreist

- A drum sampler, step sequencer and performance instrument: pads, layers, song mode,
  47 effects.
- Rebuilt in Rust from the reverse-engineered behaviour of FXpansion **Geist2** 2.1.2.13.
- Loads Geist2 `.geist` projects, kits and patterns; saves its own `.dreist` family
  (`.dreist`, `.dreistkit`, ...) in Geist2's XML.
- VST3, CLAP and a standalone app for macOS (Apple Silicon), Windows (x64) and Linux (x86_64,
  X11 / XWayland); minimums under [Installation](#installation).
- Settings: `~/Library/Application Support/Dreist` (Windows: `%APPDATA%\Dreist`, Linux:
  `~/.config/Dreist`, or `$XDG_CONFIG_HOME/Dreist`).
- Plugin IDs: CLAP `rs.dreist.dreist`, VST3 class `DreistRsDrumSmp1`.

| | |
|---|---|
| ![Pattern editor](docs/screens/readme/dreist-pattern.png) | ![Scenes](docs/screens/readme/dreist-scenes.png) |
| ![Song mode](docs/screens/readme/dreist-song.png) | ![Transmod](docs/screens/readme/dreist-transmod.png) |

## Installation

Download the archives for your system from the
[releases page](https://github.com/koeves/dreist/releases) (latest:
[v0.2.3](https://github.com/koeves/dreist/releases/tag/v0.2.3), macOS and Windows; Linux builds
come with the next release).

Supported systems:

- macOS 11 or newer on Apple Silicon.
- Windows 10 or newer, x64.
- Linux x86_64 with glibc 2.39 or newer (Ubuntu 24.04, Fedora 40 or newer), X11 or XWayland.

Release downloads, per system (`<tag>` is the release, say `v0.2.3`):

| System | VST3 | CLAP | App |
|---|---|---|---|
| macOS | `Dreist-<tag>-macOS-VST3.zip` | `Dreist-<tag>-macOS-CLAP.zip` | `Dreist-<tag>-macOS-App.zip` |
| Windows | `Dreist-<tag>-Windows-VST3.zip` | `Dreist-<tag>-Windows-CLAP.zip` | `Dreist-<tag>-Windows-App.zip` |
| Linux | `Dreist-<tag>-Linux-VST3.tar.gz` | `Dreist-<tag>-Linux-CLAP.tar.gz` | `Dreist-<tag>-Linux-App.tar.gz` |

**macOS**

- VST3: unzip and move `Dreist.vst3` to `~/Library/Audio/Plug-Ins/VST3/`.
- CLAP: move `Dreist.clap` to `~/Library/Audio/Plug-Ins/CLAP/`.
- App: move `Dreist.app` to `/Applications` (or `~/Applications`).

The builds are not signed or notarised. Open the app the first time with
right-click (or Control-click) › Open › Open. If a host refuses to load the
plugins, clear the quarantine flag:

```bash
xattr -dr com.apple.quarantine ~/Library/Audio/Plug-Ins/VST3/Dreist.vst3 ~/Library/Audio/Plug-Ins/CLAP/Dreist.clap
```

**Windows**

- VST3: unzip and move the `Dreist.vst3` folder to `C:\Program Files\Common Files\VST3\`.
- CLAP: move the `Dreist` folder (holding `Dreist.clap` and its `Resources`) to
  `C:\Program Files\Common Files\CLAP\`.
- App: unzip the `Dreist` folder anywhere and run `Dreist.exe`. Keep the
  `Resources` folder next to it. SmartScreen may warn on first launch, because
  the build is unsigned: More info › Run anyway.

**Linux** (x86_64, glibc 2.39+; X11, Wayland desktops run it through XWayland)

- VST3: unpack and move `Dreist.vst3` to `~/.vst3/` (or `/usr/lib/vst3/`).
- CLAP: unpack and move the `Dreist` folder (holding `Dreist.clap` and its `Resources`) to
  `~/.clap/` (or `/usr/lib/clap/`).
- App: unpack the `Dreist` folder anywhere (say `~/.local/share/Dreist`) and run `Dreist`; keep
  `Resources` next to it. A symlink to it (`ln -s ~/.local/share/Dreist/Dreist ~/.local/bin/dreist`)
  works, and `dreist.desktop` / `dreist.png` are a desktop entry and icon for
  `~/.local/share/applications` and `~/.local/share/icons/hicolor/256x256/apps`.
- Runtime needs: ALSA (`libasound2`), X11 / XCB (`libx11-6`, `libx11-xcb1`, `libxcb1`,
  `libxcursor1`) and OpenGL (`libgl1`), present on desktop systems. The standalone app plays
  through ALSA (with PipeWire or PulseAudio, through their ALSA plugin); file dialogs use the XDG
  desktop portal (`xdg-desktop-portal`, or `zenity` without one).

**Known limitations**

- Windows and Linux: REX files (`.rx2`, `.rex`) do not load, and samples cannot be dragged out
  of Dreist into a host or the file manager (both macOS only).
- Linux: X11 only; Wayland desktops run Dreist through XWayland.
- The builds are unsigned on every system (see above for the first launch on macOS and Windows).

**Content**

Dreist does not include sample content. Get Geist2 content (such as the
starter pack) from FXpansion; Geist2 kits, presets and expansions load as they are. Dreist looks in
`~/Documents/FXpansion/Geist2` (Windows: `%USERPROFILE%\Documents\FXpansion\Geist2`, Linux:
`~/Documents/FXpansion/Geist2` too);
change the location under Preferences.

## Build

Needs a Rust toolchain.

```bash
scripts/build.sh            # macOS: target/bundled/Dreist.{app,vst3,clap}
scripts/build.sh --install  # also copies them to ~/Library and /Applications
scripts/build-windows.sh    # Windows (Git Bash): target/bundled/Dreist.vst3, Dreist-CLAP/, Dreist-App/
scripts/build-linux.sh      # Linux: target/bundled/Dreist.vst3, Dreist-CLAP/, Dreist-App/
scripts/build-linux.sh --install  # also into ~/.vst3, ~/.clap/Dreist, ~/.local/share/Dreist (+ ~/.local/bin/dreist)
cargo test --workspace
```

On Linux the build needs (Debian / Ubuntu names; Fedora: `alsa-lib-devel libX11-devel
libxcb-devel libXcursor-devel mesa-libGL-devel`):

```bash
sudo apt-get install pkg-config libasound2-dev libx11-dev libx11-xcb-dev libxcb1-dev libxcursor-dev libgl1-mesa-dev
```

Merging a release pull request (`dev` -> `main`) releases: `.github/workflows/release-on-main.yml`
takes the version from the commits, tags the merge `vX.Y.Z`, tests and builds on macOS, Windows and
Linux, publishes the GitHub release with the zips (Linux: tarballs) and opens the changelog pull request into `dev`
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Layout

Dreist is an app on [dreist-commons](https://github.com/koeves/dreist-commons), the crates it
shares with Einst (a Geist v1 rebuild): `dreist-formats`, `dreist-dsp`, `dreist-engine`,
`dreist-gui`, `dreist-testkit`. This repository has:

| Crate | Role |
|---|---|
| `dreist-editor` | Dreist's editor: panels, dialogs, settings, effect menu, document readers |
| `dreist-plugin` | nih-plug VST3 / CLAP / standalone, and Dreist's app profile |
| `dreist-cli` | `dreist-inspect`: summarise a project file, check its samples; render and comparison tools |
| `xtask` | nih-plug bundler |

`assets/ui` (Dreist's own UI) is generated by `scripts/uigen/uigen.py` and committed;
`assets/factory` holds Geist2's factory presets, chains and templates, bundled with the builds.

## Contributing

- Commits follow Conventional Commits (`feat(scope): ...`); the changelog and release notes
  are generated from them ([CONTRIBUTING.md](CONTRIBUTING.md)).
- Checks: `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`,
  `cargo test --workspace`.
- dreist-commons is a submodule at `commons`: clone with `--recursive`.
- Code and git conventions for contributors: [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Related projects

- [dreist-commons](https://github.com/koeves/dreist-commons): the shared library (formats, DSP,
  engine, GUI toolkit) that both apps are built on.
- [Dreist](https://github.com/koeves/dreist): the Geist2 rebuild, an app on dreist-commons.
- [Einst](https://github.com/koeves/einst): the Geist v1 rebuild, an app on dreist-commons.

## Licence

The crates are MIT OR Apache-2.0. `dreist-plugin` and the binaries built from
it are GPL-3.0-or-later. See [`LICENSE`](LICENSE) and
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Dreist is not affiliated
with or endorsed by FXpansion.
