# Changelog

## [0.1.0] - 2026-11-06

First release: the original v2 instrument rebuilt in Rust as a thin app on dreist-commons
v0.1.0 (VST3, CLAP and standalone for macOS on Apple Silicon and Windows x64).

### What was ported

- Projects, kits, engines, patterns, banks and effect presets load from the original's files;
  Dreist saves its own `.dreist` family in the same XML.
- The instrument: 8 engines of pads and layers, the sampler voice with envelopes, filters,
  modulation and transmod, slicing and REX import, timestretch.
- Step sequencer with graph lanes, swing templates, song mode and scenes; MIDI in, MIDI file
  export, host automation and MIDI learn bindings; standalone sync to MIDI clock.
- Mixer with sends, master and global effect chains, and all 47 effects with their factory
  presets and chains.
- The editor: every panel of the original UI with Dreist's own skin, icon font, cursors and
  the manual's labels; browser, undo, drag and drop, offline render and export.
- Plays in hosts that leave the 16 sub outputs inactive (such as Live).
- Plugin IDs: CLAP `rs.dreist.dreist`, VST3 `DreistRsDrumSmp1`; settings in `Dreist`.

### Features

- Dreist beta 1
- New app icon, a blue D on a dark rounded square
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
- New app icon from the in-app logo

### Fixes

- **notices:** Leave out the dreist-* crates, this project's own code
- **dreist-editor:** Give each test thread its own settings folder
- **dreist-editor:** Clear pad resets the whole pad, name included
- **dreist-editor:** Lane menus list the shared lanes only

### Performance

- **dreist-editor:** Browser previews decode off the editor thread

### Refactoring

- Make Dreist a thin app on dreist-commons
- Refer to evidence by tag; rename the skin's legacy names
- **editor:** Dreist owns its editor (moved from dreist-commons)

### Documentation

- Update README and agent docs for dreist-commons
- Plain words that are not references stay words in comments
- **license:** Name the factory data as the original instrument's
- **readme:** How the three projects relate
- README without beta notes; contributing section; git conventions for agents
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

- Depend on dreist-commons at a pinned revision
- Pin dreist-commons 8a03d51 (porting fixes, voice-filter and effect 2^x hooks, rules)
- Take dreist-commons as a submodule at commons, by path
- dreist-commons v0.1.0
- Conventional-commit check, git-cliff changelog, tag-triggered release
- **deps:** Repoint commons after history rewrite
- **deps:** dreist-commons 0a7cb89 (v1 controls, opt-in; screens unchanged)
- **deps:** dreist-commons 4e2e504 (opt-in gradients and controls; screens unchanged)
- **deps:** dreist-commons d872395 (opt-in radial gradients, glow, noise; screens unchanged)
- **deps:** dreist-commons 673bb4c (end fade from the triggering sample; screens unchanged)
- **deps:** dreist-commons 5559d30 (end fade trigger and clamp as the original; screens unchanged)
- dreist-commons 230f34e (vendored nih-plug with CLAP state fixes; goldens unchanged)
- dreist-commons fcf90a4 (editor crash fixes, background GUI mode, preview loader; goldens unchanged)
- Run on main, tags and by hand only; work goes to dev
- dreist-commons 9584edc (dev; sample memory and its readout text; goldens unchanged)
- dreist-commons 5462f7c (dev; v1 routing-depth lanes and routing slots; goldens unchanged)
- Run workflows only on release tags
- dreist-commons v0.1.1
- dreist-commons 4be0295 (agent notes removed; no code change)
- dreist-commons df06666 (inactive sub outputs no longer silence the plugin)

### Other

- **dreist-editor:** Editorshot lets the slicer slide in
- Remove agent notes and unused files
