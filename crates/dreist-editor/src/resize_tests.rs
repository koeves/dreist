//! Live resizing: window resizes (the host's frame, the window sizer, step
//! by step, through a degenerate size) and splitter moves lay every panel
//! out from its container, so the frame after any sequence equals an editor
//! opened at the final size and splitter positions, and every size and
//! splitter state keeps the panels inside their containers without
//! overlapping rows.

use crate::options::Options;
use crate::{Editor, Model};
use dreist_gui::{Ctrl, Rect};

/// Window sizes: the smallest the window sizer and the host allow, the
/// skin's, a user's saved one, a large one.
const SIZES: [(i32, i32); 4] = crate::screens::SIZES;

/// Splitter states (saved positions, clamped as the editor restores them):
/// the skin's, a user's, the left column at its widest / narrowest, the
/// pads at their tallest / shortest, the editor tabs at their shortest /
/// tallest.
const SPLITS: [&[(&str, i32)]; 8] = [
    &[],
    &[("mainSplitAS", 288), ("padSplitterAS", 371), ("utilitySplitAS", 315)],
    &[("utilitySplitAS", 600)],
    &[("utilitySplitAS", 250)],
    &[("padSplitterAS", 66)],
    &[("padSplitterAS", 5000)],
    &[("mainSplitAS", 190)],
    &[("mainSplitAS", 5000)],
];

/// The demo project's editor opened with `layout` (as the plugin opens it
/// with the user's options); `None` without the content.
fn opened(layout: &Options, tab: usize, sampler: bool) -> Option<Editor> {
    let p = std::path::PathBuf::from(std::env::var("HOME").ok()?).join(dreist_formats::legacy::CONTENT_DIR).join(dreist_formats::legacy::DEMO_FACTORY).join("Presets/Hollow.geist");
    let doc = dreist_formats::Project::load(&p).ok()?.raw;
    let mut model = Model::new(doc);
    model.samples = Some(dreist_formats::model::samples_dir(&p));
    model.name = Some("Hollow".into());
    model.editor_tab = tab;
    if sampler {
        let e = model.engine;
        model.engine_mut(e).set("EnginePadMode", "Sampler");
    }
    let mut ed = Editor::with_layout(dreist_gui::skin::default_theme(), model, layout).ok()?;
    ed.sync();
    Some(ed)
}

fn layout(size: (i32, i32), splits: &[(&str, i32)]) -> Options {
    let mut o = Options::default();
    o.set("LastEditorSize", format!("{},{}", size.0, size.1));
    for (k, v) in splits {
        o.set(k, v);
    }
    o
}

/// Path of the splitter saved as `key`.
fn splitter(ed: &Editor, key: &str) -> Vec<usize> {
    fn find(c: &Ctrl, key: &str, p: &mut Vec<usize>) -> bool {
        if c.attr("strAutoSaveName") == Some(key) {
            return true;
        }
        for (i, k) in c.children.iter().enumerate() {
            p.push(i);
            if find(k, key, p) {
                return true;
            }
            p.pop();
        }
        false
    }
    let mut p = Vec::new();
    assert!(find(&ed.app.root, key, &mut p), "no splitter {key}");
    p
}

/// Splitter positions by save name.
fn splits(ed: &Editor) -> Vec<(&'static str, i32)> {
    ["utilitySplitAS", "padSplitterAS", "mainSplitAS"].into_iter().map(|k| (k, dreist_gui::splitter::position(ed.app.ctrl(&splitter(ed, k)).unwrap()))).collect()
}

fn pointer(ed: &mut Editor, x: f32, y: f32) {
    for ev in ed.app.mouse_move(x, y) {
        ed.handle(&ev);
    }
    let _ = ed.render_frame(1.0);
}

fn press(ed: &mut Editor, down: bool) {
    let b = dreist_gui::app::MouseButton::Left;
    for ev in if down { ed.app.mouse_down(b) } else { ed.app.mouse_up(b) } {
        ed.handle(&ev);
    }
    let _ = ed.render_frame(1.0);
}

/// Drag the splitter saved as `key` towards `pos` by its bar, a frame per
/// pointer move.
fn drag_split(ed: &mut Editor, key: &str, pos: i32) {
    let path = splitter(ed, key);
    let c = ed.app.ctrl(&path).unwrap();
    let vertical = dreist_gui::splitter::vertical(c);
    let from = dreist_gui::splitter::position(c);
    let (ox, oy) = ed.app.origin(&path);
    let half = dreist_gui::splitter::dim(c) as f32 / 2.0;
    let at = |p: i32| if vertical { (ox as f32 + 40.0, oy as f32 + p as f32 + half) } else { (ox as f32 + p as f32 + half, oy as f32 + 40.0) };
    let (x, y) = at(from);
    pointer(ed, x, y);
    press(ed, true);
    for i in 1..=5 {
        let (x, y) = at(from + (pos - from) * i / 5);
        pointer(ed, x, y);
    }
    press(ed, false);
}

/// Drag the window sizer (bottom right corner) to make the window `w` x `h`.
fn drag_sizer(ed: &mut Editor, w: i32, h: i32) {
    let (w0, h0) = ed.app.size();
    let (x, y) = (w0 as f32 - 7.0, h0 as f32 - 7.0);
    pointer(ed, x, y);
    press(ed, true);
    for i in 1..=6 {
        pointer(ed, x + ((w - w0) * i / 6) as f32, y + ((h - h0) * i / 6) as f32);
    }
    press(ed, false);
    ed.animate();
}

/// The host resizing the window (or the sizer's request coming back), then
/// a frame.
fn resize(ed: &mut Editor, w: i32, h: i32) {
    ed.app.resize(w, h);
    ed.app.dirty = true;
    let _ = ed.render_frame(1.0);
}

/// From the current size to `to` in `n` steps.
fn resize_steps(ed: &mut Editor, to: (i32, i32), n: i32) {
    let (w0, h0) = ed.app.size();
    for i in 1..=n {
        resize(ed, w0 + (to.0 - w0) * i / n, h0 + (to.1 - h0) * i / n);
    }
}

/// Pixels differing by more than the tolerance: count, worst and the box
/// around them.
fn diff(a: &dreist_gui::tiny_skia::Pixmap, b: &dreist_gui::tiny_skia::Pixmap) -> (usize, u8, Rect) {
    assert_eq!((a.width(), a.height()), (b.width(), b.height()));
    let w = a.width() as i32;
    let (mut n, mut worst) = (0, 0u8);
    let (mut x0, mut y0, mut x1, mut y1) = (i32::MAX, i32::MAX, -1, -1);
    for (i, (p, q)) in a.data().chunks(4).zip(b.data().chunks(4)).enumerate() {
        let d = p.iter().zip(q).map(|(x, y)| x.abs_diff(*y)).max().unwrap_or(0);
        if d > 4 {
            n += 1;
            worst = worst.max(d);
            let (x, y) = (i as i32 % w, i as i32 / w);
            (x0, y0, x1, y1) = (x0.min(x), y0.min(y), x1.max(x), y1.max(y));
        }
    }
    (n, worst, Rect::new(x0, y0, x1 - x0 + 1, y1 - y0 + 1))
}

/// `DREIST_STAGE=dir` keeps the frames for review.
fn stage(name: &str, pm: &dreist_gui::tiny_skia::Pixmap) {
    if let Ok(d) = std::env::var("DREIST_STAGE") {
        let _ = std::fs::create_dir_all(&d);
        let _ = pm.save_png(std::path::Path::new(&d).join(format!("{name}.png")));
    }
}

/// After a sequence of live resizes and splitter drags, the frame equals
/// that of an editor opened at the final size and splitter positions.
#[test]
fn live_resizes_match_a_fresh_editor() {
    let user = layout(crate::screens::RESIZED, SPLITS[1]);
    for tab in 0..7 {
        for sampler in [false, true] {
            let Some(mut ed) = opened(&user, tab, sampler) else { return };
            let _ = ed.render_frame(1.0);
            // Shrink to the minimum step by step; a degenerate size on the
            // way (a host hiding or docking the view); grow large; the
            // left column wide, then shrink again; the window sizer; the
            // other splitters; a last host resize.
            resize_steps(&mut ed, dreist_gui::app::MIN_WINDOW, 8);
            resize(&mut ed, 0, 0);
            resize(&mut ed, 1, 1);
            resize(&mut ed, 200, 120);
            resize_steps(&mut ed, (1920, 1200), 6);
            drag_split(&mut ed, "utilitySplitAS", 600);
            resize_steps(&mut ed, dreist_gui::app::MIN_WINDOW, 6);
            drag_sizer(&mut ed, 1500, 900);
            assert_eq!(ed.app.size(), (1500, 900), "the window sizer");
            drag_split(&mut ed, "padSplitterAS", 200);
            drag_split(&mut ed, "mainSplitAS", 300);
            drag_split(&mut ed, "utilitySplitAS", 430);
            resize_steps(&mut ed, crate::screens::RESIZED, 3);
            let live = ed.render(1.0);
            let s = splits(&ed);
            let mut fresh = opened(&layout(ed.app.size(), &s), tab, sampler).unwrap();
            let want = fresh.render(1.0);
            let (n, worst, at) = diff(&live, &want);
            if n > 4 {
                stage(&format!("live-{tab}-{sampler}"), &live);
                stage(&format!("fresh-{tab}-{sampler}"), &want);
            }
            assert!(n <= 4, "tab {tab}, sampler {sampler}: {n} pixels off (worst by {worst} in {at:?}), splitters {s:?}");
        }
    }
}

/// Visible controls (by path of names) sticking out of their parent by
/// more than a few pixels.
fn outside(ed: &Editor) -> Vec<(String, String)> {
    fn walk(c: &Ctrl, path: &str, out: &mut Vec<(String, String)>) {
        // Collapsed (a splitter panel snapped shut): nothing in it shows.
        if c.rect.w <= 0 || c.rect.h <= 0 {
            return;
        }
        for k in &c.children {
            if !k.visible {
                continue;
            }
            let r = k.rect;
            let p = format!("{path}/{}{}", k.name, if k.overload.is_empty() { String::new() } else { format!("[{}]", k.overload) });
            let slack = 3;
            // Scrolled content is larger than its viewport by design.
            let scrolled = c.class.contains("Scroll") || c.class.contains("TableView");
            // Wholly past the far edge of a parent squeezed below the
            // skin's room for it (the scenes' engine table under the
            // smallest editor tabs, as in the original): hidden, not cut.
            let gone = r.x >= c.rect.w || r.y >= c.rect.h;
            if !scrolled && !gone && r.w > 0 && r.h > 0 && (r.x < -slack || r.y < -slack || r.x + r.w > c.rect.w + slack || r.y + r.h > c.rect.h + slack) {
                out.push((p.clone(), format!("{r:?} in {:?}", (c.rect.w, c.rect.h))));
            }
            walk(k, &p, out);
        }
    }
    let mut out = Vec::new();
    walk(&ed.app.root, "", &mut out);
    out
}

fn shown<'a>(ed: &'a Editor, name: &str) -> Vec<&'a Ctrl> {
    fn walk<'a>(c: &'a Ctrl, name: &str, out: &mut Vec<&'a Ctrl>) {
        if !c.visible {
            return;
        }
        if c.name == name || c.overload == name {
            out.push(c);
        }
        for k in &c.children {
            walk(k, name, out);
        }
    }
    let mut out = Vec::new();
    walk(&ed.app.root, name, &mut out);
    out
}

fn overlap(a: &Rect, b: &Rect) -> bool {
    a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h
}

/// Cells inside their container, none overlapping another.
fn grid(what: &str, cells: &[Rect], within: Rect) {
    for (i, a) in cells.iter().enumerate() {
        assert!(a.w > 0 && a.h > 0 && a.x >= 0 && a.y >= 0 && a.x + a.w <= within.w && a.y + a.h <= within.h, "{what}: cell {i} {a:?} outside {within:?}");
        for b in &cells[i + 1..] {
            assert!(!overlap(a, b), "{what}: cells {a:?} and {b:?} overlap");
        }
    }
}

fn set_view(ed: &mut Editor, tab: usize, sampler: bool) {
    ed.model.editor_tab = tab;
    let e = ed.model.engine;
    ed.model.engine_mut(e).set("EnginePadMode", if sampler { "Sampler" } else { "Normal" });
    ed.sync();
    let _ = ed.render_frame(1.0);
}

/// Every size and splitter state: nothing visible sticks out of its parent
/// more than at the skin's size; the pads fill their area, the pad strip's
/// buttons and the song headers, layer rows, scene tiles and mixer strips
/// keep to their grids; the main column keeps its minimum width.
#[test]
fn layout_holds_at_every_size_and_splitter_state() {
    // What sticks out by the skin's design at the skin's size.
    let mut known = std::collections::HashSet::new();
    let Some(mut ed) = opened(&layout((1400, 850), &[]), 0, false) else { return };
    for sampler in [false, true] {
        for tab in 0..7 {
            set_view(&mut ed, tab, sampler);
            known.extend(outside(&ed).into_iter().map(|o| o.0));
        }
    }
    for size in SIZES {
        for sp in SPLITS {
            let mut ed = opened(&layout(size, sp), 0, false).unwrap();
            assert_eq!(ed.app.size(), size);
            for sampler in [false, true] {
                for tab in 0..7 {
                    set_view(&mut ed, tab, sampler);
                    let what = format!("{size:?} {sp:?} tab {tab} sampler {sampler}");
                    if std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| check_layout(&ed, &what, &known))).is_err() {
                        stage("layout-failure", &ed.render(1.0));
                        panic!("{what}: see above");
                    }
                }
            }
        }
    }
}

fn check_layout(ed: &Editor, what: &str, known: &std::collections::HashSet<String>) {
    let new: Vec<_> = outside(ed).into_iter().filter(|o| !known.contains(&o.0)).collect();
    assert!(new.is_empty(), "{what}: outside their parents: {new:#?}");
    // The main column keeps the width it has in the smallest window beside
    // the skin's left column, however wide the left column is dragged.
    let main = shown(ed, "MainPanel")[0].rect;
    let min_main = dreist_gui::app::MIN_WINDOW.0 - 10 - 300 - 8;
    assert!(main.w >= min_main, "{what}: main column {main:?} narrower than {min_main}");
    // The pads fill their area (no empty band beside or below them).
    // (Unless the pads splitter snapped them shut.)
    let m = shown(ed, "PadsMatrix")[0];
    if m.rect.h > 40 {
        let cells: Vec<Rect> = m.children.iter().filter(|c| c.visible).map(|c| c.rect).collect();
        grid(&format!("{what}: pads"), &cells, m.rect);
        let right = cells.iter().map(|c| c.x + c.w).max().unwrap_or(0);
        let bottom = cells.iter().map(|c| c.y + c.h).max().unwrap_or(0);
        assert!(right >= m.rect.w - 4 && bottom >= m.rect.h - 4, "{what}: pads end at {right}, {bottom} in {:?}", m.rect);
    }
    // The pad strip: its shown buttons inside it, side by side.
    let strip = shown(ed, "PadControl")[0];
    let buttons: Vec<Rect> = strip.children.iter().filter(|c| c.visible && c.rect.w > 0).map(|c| c.rect).collect();
    let mut within = strip.rect;
    within.h += 2;
    grid(&format!("{what}: pad strip"), &buttons, within);
    // Song track headers: a fixed column, one header per row.
    if let Some(hp) = shown(ed, "TrackHeaderPanel").first() {
        assert_eq!(hp.rect.w, 80, "{what}: song header column {:?}", hp.rect);
        let rows: Vec<Rect> = hp.children.iter().map(|c| c.rect).collect();
        assert_eq!(rows.len(), crate::model::ENGINES);
        grid(&format!("{what}: song headers"), &rows, hp.rect);
        for p in rows.windows(2) {
            assert_eq!(p[1].y, p[0].y + p[0].h, "{what}: song headers {rows:?} not one per row");
        }
    }
    // Layer rows stacked.
    let rows: Vec<Rect> = shown(ed, "LayerRow").iter().map(|c| c.rect).collect();
    for (i, a) in rows.iter().enumerate() {
        for b in &rows[i + 1..] {
            assert!(!overlap(a, b), "{what}: layer rows {a:?} and {b:?} overlap");
        }
    }
    // The pad name row inside the inspector, not under the splitter bar.
    for c in shown(ed, "PadInspector") {
        for k in c.children.iter().flat_map(|k| k.children.iter()).flat_map(|k| k.children.iter()) {
            assert!(k.rect.y >= 0, "{what}: {:?} starts above the inspector", k.rect);
        }
    }
    // Scene tiles and mixer strips.
    if let Some(m) = shown(ed, "ScenesPanel").first() {
        let tiles: Vec<Rect> = m.children.iter().filter(|c| c.attr("cell").is_some()).map(|c| c.rect).collect();
        grid(&format!("{what}: scene tiles"), &tiles, m.rect);
    }
    for c in shown(ed, "ChannelScroller") {
        for s in &c.children {
            assert_eq!(s.rect.h, c.rect.h, "{what}: mixer strip {:?} in {:?}", s.rect, c.rect);
        }
    }
}

/// Review aid (`cargo test -- --ignored stage_view`): the editor at
/// `SIZE=WxH`, `SPLITS=key=pos,...`, `TAB=n`, `SAMPLER=1`, saved to
/// `DREIST_STAGE/view.png`.
#[test]
#[ignore]
fn stage_view() {
    let env = |k: &str| std::env::var(k).ok();
    let size = env("SIZE").and_then(|v| v.split_once('x').and_then(|(w, h)| Some((w.parse().ok()?, h.parse().ok()?)))).unwrap_or((1400, 850));
    let sp: Vec<(String, i32)> = env("SPLITS").unwrap_or_default().split(',').filter_map(|kv| kv.split_once('=')).filter_map(|(k, v)| Some((k.to_string(), v.parse().ok()?))).collect();
    let sp: Vec<(&str, i32)> = sp.iter().map(|(k, v)| (k.as_str(), *v)).collect();
    let tab = env("TAB").and_then(|v| v.parse().ok()).unwrap_or(0);
    let Some(mut ed) = opened(&layout(size, &sp), tab, env("SAMPLER").is_some()) else { return };
    let _ = ed.render_frame(1.0);
    stage(&env("NAME").unwrap_or_else(|| "view".into()), &ed.render(1.0));
}

/// Every scroll container under `c` (paths).
fn scrollables(ed: &Editor) -> Vec<Vec<usize>> {
    fn rec(c: &Ctrl, path: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if dreist_gui::scroll::scrollable(c) {
            out.push(path.clone());
        }
        for (i, k) in c.children.iter().enumerate() {
            path.push(i);
            rec(k, path, out);
            path.pop();
        }
    }
    let mut out = Vec::new();
    rec(&ed.app.root, &mut Vec::new(), &mut out);
    out
}

/// Each scroll container's offset within its range, and its children
/// spanning a one-axis view.
fn check_scrolled(ed: &Editor, what: &str) {
    for p in scrollables(ed) {
        let c = ed.app.ctrl(&p).unwrap();
        let (cw, ch) = dreist_gui::scroll::content(c);
        let v = dreist_gui::scroll::view(c);
        let (sx, sy) = dreist_gui::scroll::offset(c);
        assert!(sx <= (cw - v.w).max(0) && sy <= (ch - v.h).max(0), "{what}: {} offset ({sx},{sy}) past content {cw}x{ch} in view {v:?}", c.name);
    }
}

/// Click the shown mixer mode button `mode` (Mix / Sends / Effects).
fn mixer_mode(ed: &mut Editor, mode: usize) {
    let shown: Vec<Vec<usize>> = {
        fn rec(app: &dreist_gui::app::App, c: &Ctrl, path: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
            if c.name == "ModeGroup" && app.shown(path) {
                out.push(path.clone());
            }
            for (i, k) in c.children.iter().enumerate() {
                path.push(i);
                rec(app, k, path, out);
                path.pop();
            }
        }
        let mut v = Vec::new();
        rec(&ed.app, &ed.app.root, &mut Vec::new(), &mut v);
        v
    };
    if let Some(g) = shown.first() {
        let b = [g.clone(), vec![mode]].concat();
        if ed.app.ctrl(&b).is_some_and(|c| c.enabled) {
            ed.handle(&dreist_gui::app::UiEvent::Clicked { path: b, name: String::new(), id: 0, on: true });
        }
    }
    ed.sync();
    let _ = ed.render_frame(1.0);
}

/// Scrolled views follow live resizes and splitter drags: offsets stay in
/// range after every step, and scrolled back they look like an editor
/// opened at the final size (mixers in every mode, transmod, the layer
/// parameter row).
#[test]
fn scrolled_views_follow_live_resizes() {
    // Short editor tabs so the mixers are compact (Effects mode exists).
    let user = layout((1150, 650), &[("padSplitterAS", 200)]);
    for (tab, mode, ut) in [(5, 2, 1), (5, 1, 0), (5, 0, 0), (4, 2, 0), (4, 0, 1), (3, 2, 0), (3, 1, 0)] {
        let Some(mut ed) = opened(&user, tab, false) else { return };
        ed.model.utility_tab = ut;
        mixer_mode(&mut ed, mode);
        let what = format!("tab {tab} mode {mode} utility {ut}");
        let scroll_all = |ed: &mut Editor, x: i32, y: i32| {
            for p in scrollables(ed) {
                if let Some(c) = ed.app.ctrl_mut(&p) {
                    dreist_gui::scroll::scroll_to(c, x, y);
                }
            }
            ed.app.dirty = true;
            let _ = ed.render_frame(1.0);
        };
        scroll_all(&mut ed, 100_000, 100_000);
        for (w, h) in [(1400, 760), (1920, 1200), (1300, 700), (1150, 650)] {
            resize_steps(&mut ed, (w, h), 3);
            ed.sync();
            check_scrolled(&ed, &format!("{what} at {w}x{h}"));
            scroll_all(&mut ed, 100_000, 100_000);
        }
        drag_split(&mut ed, "utilitySplitAS", 420);
        drag_split(&mut ed, "padSplitterAS", 240);
        ed.sync();
        check_scrolled(&ed, &format!("{what} after splitters"));
        resize_steps(&mut ed, (1250, 700), 2);
        // A tall panel goes back to Mix; pick the mode again.
        mixer_mode(&mut ed, mode);
        scroll_all(&mut ed, 0, 0);
        let live = ed.render(1.0);
        let s = splits(&ed);
        let mut fresh = opened(&layout(ed.app.size(), &s), tab, false).unwrap();
        fresh.model.utility_tab = ut;
        mixer_mode(&mut fresh, mode);
        let want = fresh.render(1.0);
        let (n, worst, at) = diff(&live, &want);
        if n > 4 {
            stage(&format!("scrolled-live-{tab}-{mode}-{ut}"), &live);
            stage(&format!("scrolled-fresh-{tab}-{mode}-{ut}"), &want);
        }
        assert!(n <= 4, "{what}: {n} pixels off (worst by {worst} in {at:?}), splitters {s:?}");
    }
}
