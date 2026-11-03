# Changelog

## [0.1.0] - 2026-11-03

First release (after beta 1): the Geist2 2.1.2.13 rebuild as a thin app on dreist-commons.

### Ported from Geist2

- Projects, kits, engines, patterns, banks and effect presets load from Geist2's files; Dreist
  saves its own `.dreist` family in the same XML.
- The instrument: 8 engines of pads and layers, the sampler voice with envelopes, filters,
  modulation and transmod, slicing and REX import, timestretch.
- Step sequencer with graph lanes, swing templates, song mode and scenes; MIDI in, MIDI file
  export, host automation and MIDI learn bindings.
- Mixer with sends, master and global effect chains, and all 47 effects with their factory
  presets and chains.
- The editor: every panel of Geist2's UI with Dreist's own skin, icon font and cursors; browser,
  undo, drag and drop, offline render and export.
- VST3, CLAP and standalone builds for macOS (Apple Silicon) and Windows (x64).

### Changed since beta 1

- New plugin IDs (CLAP `rs.dreist.dreist`, VST3 `DreistRsDrumSmp1`): hosts see a new plugin.
- Settings move from `Geist-rs` to `Dreist` on first launch.
- New app icon.
- The shared crates live in [dreist-commons](https://github.com/koeves/dreist-commons) (a
  submodule), with its porting fixes (Modulated Filter FM, Tune to BPM, voice filter drive).
