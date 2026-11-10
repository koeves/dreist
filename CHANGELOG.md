# Changelog

## [0.2.1] - 2026-11-10

v0.2.0's release run stopped at the generated-UI check; this release carries the same changes
(see 0.2.0) plus the fix.

### Fixes

- **ci:** Uigen --check skips the review contact sheet

## [0.2.0] - 2026-11-10

A parity pass from the vendor's Geist2 tutorial videos (each change checked against the shipped
plugin's binary), the shipped skin's layout and labels with Dreist's own art, resizing that holds
at every window size, and faster drawing.

### Summary

- **From the videos**: the slicer opens with slices (default sensitivity 0.75) and guesses loop
  tempo as the original; graph Offset/Comp/Rand act on the selected steps; filled selected steps;
  grouped graph lane menu; take names "<pad> Take n HH-MM-SS"; Places with the app folder and
  Sampler Captures; no-slice file alert; zoom slider overview waveform; per-layer zoom memory.
- **Look**: the shipped skin's layout, sizes and labels (header, mixer, transmod, scenes, song,
  dialogs, pattern, pads, inspector, layer params, browser, sampler, slicer), corner radii and
  arrows; transmod faders and knob rings drawn as the original.
- **Resizing**: every panel and splitter lays out again on any resize; the host can resize the
  editor down to its minimum; the main column keeps its minimum width.
- **Sound**: analog table reads floor like the original (voice filters, vintage path, analog
  filter effects), a porting bug shared with Einst.
- **Speed**: menu hover, clicks and panel updates redraw only what changed.

### Features

- **pattern:** Graph lane menu grouped into submenus
- **pattern:** Track length overlay follows a dragged marker
- **browser:** Places list the app folder and Sampler Captures
- **wave:** Whole-file waveform in the zoom sliders
- **inspector:** Per-layer zoom memory with auto zoom off
- **plugin:** The host can resize the editor, down to the window minimum

### Fixes

- **pattern:** Graph knobs act on the track's selected steps only
- **slicer:** Start at sensitivity 0.75 and guess loop tempo
- **sampler:** Name takes after the target pad, in local time
- **browser:** Alert when the no-slice file cannot be created
- **inspector:** Pad inspector layout follows its panel's size
- **inspector:** Zoom slider wheel moves the thumb 5 px both ways
- **song:** The song page fills its tab after a window resize
- **editor:** Scene tiles, song track headers and mixer strips follow a resize
- **ui:** Transmod cards and browser header roots anchored as shipped
- **pads:** The pad grid and strip follow their area as it resizes
- **song:** The track header column keeps its width as the page resizes
- **pattern:** Track rows and graph lanes stay one per row as the list resizes
- **ui:** The pad name row starts inside the pad inspector
- **ui:** A wider left column leaves the main column its minimum width
- **browser:** The file pane keeps room for its toolbar in a narrow column
- **transmod:** The four macro knobs fit the smallest window
- **scenes:** The engine table follows the panel's height
- **mixer:** Tall strips keep mute, solo and pre below the meter

### Performance

- **editor:** Time menu hovers and clicks in the render bench
- **editor:** Repaint only the code-drawn panels whose drawing changed
- **editor:** A knob reset repaints what changed, not the window

### Documentation

- Move contributor notes into CONTRIBUTING.md; drop .agents

### Tests

- **editor:** Refresh screen fingerprints for the original-layout pass
- **editor:** Refresh screen fingerprints after the pattern, pads, inspector, browser and sampler layout pass
- **editor:** Editorshot DREIST_SIZE renders at a given window size
- **editor:** Resized-window screens and cell geometry
- **editor:** Clicks repaint like full renders
- **editor:** Knob resets and panel buttons repaint like full renders
- **editor:** Live resizes match a fresh editor; layout holds at every size

### Build and CI

- Dreist-commons 88790de (opt-in renderer additions for Einst's v1 look)
- Dreist-commons fdc98df (resized splitters keep the far panel)
- Dreist-commons 11bd48a (splitter bar clamped on resize)
- Dreist-commons 7abfa72 (opt-in transmod slider strip)
- Dreist-commons 144fe38 (opt-in looks for Einst's effect panels and controls)
- Dreist-commons a4837fb (docs only)
- Dreist-commons e05a1b8 (faster menu hover repaints)
- Dreist-commons 149a70e (clicks repaint only what they change)
- Dreist-commons 99c3274 (analog table reads floor like the original)
- Dreist-commons 964c58b (graph record rule, panels repaint only when their drawing changes)
- Dreist-commons 0a810a3 (resize-path independent anchoring and splitters, mounted skins fill their host, host resizing in nih-plug)
- Dreist-commons v0.2.0

### Other

- **pattern:** Fill selected steps with the track style's colSelected
- **pattern:** Track rows' disclosure button shows an arrow
- **dreist-editor:** Editorshot clicks several controls and selects all
- **ui:** Plain labels as in the original's sampler and transmod
- **ui:** Original corner radii and drop arrows
- **header:** Original console labels, menu and selector geometry
- **mixer:** Light channel strips, transmod faders and the FX card
- **transmod:** Original card sizes, slot titles and source labels
- **scenes:** Original scene and song toolbars
- **dialogs:** Original captions, titles and preference columns
- **pattern:** Toolbar spinner, track rows and nav buttons at the shipped positions
- **pads:** Shipped toolbar layout, flat empty layer slots, 5 px tiles
- **inspector:** Empty layer rows, "Pad options... ▶", table at y 78
- **layer:** Shipped layout and labels, connector lines, mod track ring
- **browser:** Table colours, header bar, folding sources, icons
- **sampler:** Strip geometry as shipped
- **slicer:** Tool strip at (10, 8), 86 wide as shipped

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
