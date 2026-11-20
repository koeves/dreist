# UI harness (Linux)

Scripts that drive the standalone's window on X11 or XWayland the way a hand does, for tests that need real UI input.

- `xui.py` finds the window, drags its window sizer, clicks and presses keys, using only libX11 and libXtst.
- `resize-playback.sh <project>` plays a project and drags the sizer at 15–25 s, then prints the underruns before, during and after the drag.

## Running

    scripts/ui-harness/resize-playback.sh ~/Documents/Content/<pack>/Presets/<project>.geist
    BIN=target/bundled/Dreist-App/Dreist RUNS=5 scripts/ui-harness/resize-playback.sh <project> --period-size 1024

- The pointer moves for real while a command runs, so run it when nobody is using the desktop.
- The app starts with `DREIST_BACKGROUND_GUI=1` and is never raised; a covered window makes `xui.py` stop before it presses anything.
- The window's saved size is set to `START` (1150,747) before each run and put back at the end.
- One or two isolated underruns in a run are fine; several in a row are audible crackles.
- A window that does not resize during the drag (no window sizer in that corner) stops the run with an error.
