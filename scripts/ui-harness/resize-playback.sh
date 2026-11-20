#!/bin/sh
# Play a project in the standalone and drag its window sizer meanwhile, then
# count the audio underruns before, during and after the drag (Linux).
#
#   scripts/ui-harness/resize-playback.sh <project> [app options...]
#
# Environment: BIN (the app, default ~/.local/share/Dreist/Dreist), RUNS (3),
# GROW ("600 300": how far the drag grows the window, in pixels), START
# (the window size each run starts at, "1150,747"). The window's saved size
# is put back afterwards. The pointer moves for real during the drag; keep
# the window uncovered (xui.py stops when it is covered).
set -eu

here=$(cd "$(dirname "$0")" && pwd)
project=${1:?usage: $0 <project> [app options...]}
shift
bin=${BIN:-$HOME/.local/share/Dreist/Dreist}
app=$(basename "$bin")
runs=${RUNS:-3}
grow=${GROW:-600 300}
start=${START:-1150,747}
options=${XDG_CONFIG_HOME:-$HOME/.config}/$app/Options.txt
work=$(mktemp -d "${TMPDIR:-/tmp}/resize-playback.XXXXXX")
saved=$(grep '^LastEditorSize=' "$options" 2>/dev/null || true)
restore() {
    if [ -n "$saved" ] && [ -f "$options" ]; then
        sed -i "s/^LastEditorSize=.*/$saved/" "$options"
    fi
    rm -rf "$work"
}
trap restore EXIT

count() { grep -ciE 'underrun|xrun' "$1" || true; }

i=1
while [ "$i" -le "$runs" ]; do
    [ -f "$options" ] && sed -i "s/^LastEditorSize=.*/LastEditorSize=$start/" "$options"
    err=$work/run$i.err
    DREIST_BACKGROUND_GUI=1 DREIST_GUI_STATS=1 "$bin" --debug --debug-json --play "$project" --duration 45 "$@" >/dev/null 2>"$err" &
    pid=$!
    sleep 15
    before=$(count "$err")
    # shellcheck disable=SC2086 # grow holds two numbers
    drag=$(python3 -I "$here/xui.py" sizer "$app" 10 60 $grow)
    during=$(count "$err")
    wait "$pid" || true
    after=$(count "$err")
    load=$(grep '^gui:' "$err" | grep -v ' 0 resizes' | grep -v whole | sed 's/.*resizes, //' | sort -n | tail -1)
    echo "run $i: underruns quiet 0-15 s: $before | drag 15-25 s: $((during - before)) | quiet 25-45 s: $((after - during)) | UI at most ${load:-?} | $drag"
    i=$((i + 1))
done
grep -m1 'Audio output:' "$work/run1.err" | sed 's/^[^]]*] //' || true
