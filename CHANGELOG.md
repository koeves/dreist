# Changelog

## [0.1.1] - 2026-11-06

Second release: Dreist now follows the Geist2 manual section by section, on dreist-commons
v0.1.1. Main's history was cleaned up: `main` now holds the beta 1 commit and one merge per
release (`git log --first-parent main`); every change stays on `dev`, unchanged. The v0.1.0 tag
and release are kept as they were. GitHub Actions now run only on release tags (and by hand).

### What was ported

- The manual's names for controls, sections and preferences, and the header's sample memory
  readout.
- Pattern editor: the step context menu, selection drags, and right clicks while drawing a
  series to cycle the Insert patterns.
- Slicer: the context menu and tool modifiers, a ruler in the chosen units, region markers, its
  own undo, live Auto load, and dragging a slice onto a pad.
- Browser: column headings with View, Columns and Sort by; previews decoded off the editor
  thread.
- Effects: drag an effect's header to move it in the chain.
- Tools › Save samples with presets, and Sync to MIDI clock in the standalone app.
- Fixes: Clear pad resets the whole pad, name included; lane menus list the shared lanes only.

### Features

- **dreist:** Header shows the engine's sample memory
- **ui:** Controls, sections and preferences use the manual's names
- **dreist-editor:** Step context menu and selection drags in the pattern editor
- **dreist-editor:** Slice context menu and the manual's slicer tool modifiers
- **dreist-editor:** Slicer ruler units, region markers, undo, live Auto load and slice drag to pads
- **dreist-editor:** Right clicks while drawing a series cycle the Insert patterns
- **dreist-editor:** Browser column headings with View, Columns and Sort by
- **dreist-editor:** Tools › Save samples with presets
- **dreist-editor:** Drag an effect's header to move it in the chain
- **dreist-plugin:** Standalone Sync to MIDI clock

### Fixes

- **dreist-editor:** Give each test thread its own settings folder
- **dreist-editor:** Clear pad resets the whole pad, name included
- **dreist-editor:** Lane menus list the shared lanes only

### Performance

- **dreist-editor:** Browser previews decode off the editor thread

### Refactoring

- **editor:** Dreist owns its editor (moved from dreist-commons)

### Documentation

- **readme:** Commons holds the GUI toolkit, not the editor
- Worktree placement and cleanup after a task
- Coordinate shared-code changes with Einst through the commons log
- README screenshots of the Hollow and Blister demo projects
- **readme:** Screenshot grid as in Einst

### Tests

- **editor:** Pattern-key drag highlight waits for its first tick on slow machines
- **editor:** Shading-mode test leaves the renderer's global mode alone
- **dreist-plugin:** Host the CLAP state extension in-process
- **dreist-editor:** Screen goldens for the manual's labels
- **dreist-editor:** Screen goldens for the browser headings, Tools and effect header changes

### Build and CI

- **deps:** Dreist-commons 0a7cb89 (v1 controls, opt-in; screens unchanged)
- **deps:** Dreist-commons 4e2e504 (opt-in gradients and controls; screens unchanged)
- **deps:** Dreist-commons d872395 (opt-in radial gradients, glow, noise; screens unchanged)
- **deps:** Dreist-commons 673bb4c (end fade from the triggering sample; screens unchanged)
- **deps:** Dreist-commons 5559d30 (end fade trigger and clamp as the original; screens unchanged)
- Dreist-commons 230f34e (vendored nih-plug with CLAP state fixes; goldens unchanged)
- Dreist-commons fcf90a4 (editor crash fixes, background GUI mode, preview loader; goldens unchanged)
- Run on main, tags and by hand only; work goes to dev
- Dreist-commons 9584edc (dev; sample memory and its readout text; goldens unchanged)
- Dreist-commons 5462f7c (dev; v1 routing-depth lanes and routing slots; goldens unchanged)
- Run workflows only on release tags
- Dreist-commons v0.1.1

### Other

- **dreist-editor:** Editorshot lets the slicer slide in

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
