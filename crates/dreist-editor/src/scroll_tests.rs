//! Scroll containers in the editor: the transmod list, the layer parameter
//! row and the effect chain row scroll with the wheel, shift + wheel and
//! trackpad swipes, clamp at their ends and show their bars.
use super::*;
use dreist_gui::app::{MouseButton, UiEvent};
use dreist_gui::scroll;

/// The Hollow demo at the small window size of the report (1000 x 555);
/// `None` without the factory content.
fn hollow(editor_tab: usize, utility_tab: usize) -> Option<Editor> {
    hollow_at(editor_tab, utility_tab, (1000, 555))
}

fn hollow_at(editor_tab: usize, utility_tab: usize, size: (i32, i32)) -> Option<Editor> {
    let p = dreist_formats::legacy::demo("Presets/Hollow.geist");
    let proj = dreist_formats::Project::load(&p).ok()?;
    let mut ed = Editor::new(dreist_gui::skin::default_theme(), Model::new(proj.raw)).ok()?;
    ed.model.editor_tab = editor_tab;
    ed.model.utility_tab = utility_tab;
    ed.app.resize(size.0, size.1);
    ed.sync();
    Some(ed)
}

/// The shown scroll container named `name` (its path).
fn container(ed: &Editor, name: &str) -> Vec<usize> {
    fn rec(app: &dreist_gui::app::App, c: &Ctrl, name: &str, path: &mut Vec<usize>) -> Option<Vec<usize>> {
        if c.name == name && scroll::scrollable(c) && app.shown(path) {
            return Some(path.clone());
        }
        for (i, k) in c.children.iter().enumerate() {
            path.push(i);
            if let Some(p) = rec(app, k, name, path) {
                return Some(p);
            }
            path.pop();
        }
        None
    }
    rec(&ed.app, &ed.app.root, name, &mut Vec::new()).unwrap_or_else(|| panic!("{name} shown and scrollable"))
}

/// Point the mouse at the centre of the container's view.
fn hover(ed: &mut Editor, path: &[usize]) {
    let r = ed.app.abs_rect(path);
    let v = scroll::view(ed.app.ctrl(path).unwrap());
    ed.app.mouse_move((r.x + v.w / 2) as f32, (r.y + v.h / 2) as f32);
}

/// Point the mouse at a spot of the container's view off its transmod
/// knobs and value boxes (those take the wheel themselves, [re:c7e2d4]).
fn hover_off_controls(ed: &mut Editor, path: &[usize]) {
    let r = ed.app.abs_rect(path);
    let v = scroll::view(ed.app.ctrl(path).unwrap());
    for y in (2..v.h).step_by(3) {
        for x in (2..v.w).step_by(3) {
            let (px, py) = ((r.x + x) as f32, (r.y + y) as f32);
            let hit = ed.app.hit(px, py);
            let takes = (0..=hit.len()).any(|n| ed.app.ctrl(&hit[..n]).is_some_and(|c| matches!(c.class.as_str(), "CtrlTransmodKnob" | "CtrlValueBox")));
            if hit.starts_with(path) && !takes {
                ed.app.mouse_move(px, py);
                return;
            }
        }
    }
    panic!("no free spot in the view");
}

fn offset(ed: &Editor, path: &[usize]) -> (i32, i32) {
    scroll::offset(ed.app.ctrl(path).unwrap())
}

fn range(ed: &Editor, path: &[usize]) -> (i32, i32) {
    let c = ed.app.ctrl(path).unwrap();
    let (cw, ch) = scroll::content(c);
    let v = scroll::view(c);
    ((cw - v.w).max(0), (ch - v.h).max(0))
}

fn bar<'a>(ed: &'a Editor, path: &[usize], axis: &str) -> &'a Ctrl {
    ed.app.ctrl(path).unwrap().children.iter().find(|k| k.attr(scroll::BAR) == Some(axis)).unwrap()
}

fn wheel(ed: &mut Editor, dx: f32, dy: f32, lines: bool) {
    for ev in ed.app.mouse_scroll(dx, dy, lines) {
        ed.handle(&ev);
    }
}

#[test]
fn transmod_list_scrolls_with_wheel_and_trackpad() {
    let Some(mut ed) = hollow(5, 1) else { return };
    let sv = container(&ed, "ScrollView");
    let (_, max) = range(&ed, &sv);
    assert!(max > 0, "the slots overflow at 1000 x 555");
    assert!(bar(&ed, &sv, "v").visible);
    let step = ed.app.ctrl(&sv).unwrap().attr_i32("scrollStep", 0);
    let content = scroll::content(ed.app.ctrl(&sv).unwrap()).1;
    assert_eq!(step, (content as f32 / 16.0).round() as i32);
    hover(&mut ed, &sv);
    let first = ed.app.ctrl(&sv).unwrap().children[0].rect.y;
    // A wheel notch down (platform y negative) moves the list up.
    wheel(&mut ed, 0.0, -1.0, true);
    assert_eq!(offset(&ed, &sv), (0, step));
    assert_eq!(ed.app.ctrl(&sv).unwrap().children[0].rect.y, first - step);
    // Up past the top clamps at 0.
    wheel(&mut ed, 0.0, 50.0, true);
    assert_eq!(offset(&ed, &sv), (0, 0));
    // Trackpad pixels move by their pixels.
    wheel(&mut ed, 0.0, -7.0, false);
    assert_eq!(offset(&ed, &sv), (0, 7));
    // A sideways swipe does nothing to a vertical list.
    wheel(&mut ed, -30.0, 0.0, false);
    assert_eq!(offset(&ed, &sv), (0, 7));
    // Down past the end clamps at content − view; the thumb sits at the end.
    wheel(&mut ed, 0.0, -10_000.0, false);
    assert_eq!(offset(&ed, &sv), (0, max));
    assert_eq!(bar(&ed, &sv, "v").value, 1.0);
    // The last slot ends at the view's bottom.
    let v = scroll::view(ed.app.ctrl(&sv).unwrap());
    let bottom = ed.app.ctrl(&sv).unwrap().children.iter().filter(|k| k.attr(scroll::BAR).is_none()).map(|k| k.rect.bottom()).max().unwrap();
    assert_eq!(bottom, v.h);
    // A press on the track above the thumb pages up.
    let b = ed.app.abs_rect(&[sv.clone(), vec![ed.app.ctrl(&sv).unwrap().children.iter().position(|k| k.attr(scroll::BAR) == Some("v")).unwrap()]].concat());
    ed.app.mouse_move((b.x + b.w / 2) as f32, (b.y + 2) as f32);
    ed.app.mouse_down(MouseButton::Left);
    ed.app.mouse_up(MouseButton::Left);
    assert_eq!(offset(&ed, &sv), (0, (max - v.h).max(0)));
}

#[test]
fn transmod_thumb_drag_scrolls() {
    let Some(mut ed) = hollow(5, 1) else { return };
    let sv = container(&ed, "ScrollView");
    let (_, max) = range(&ed, &sv);
    let i = ed.app.ctrl(&sv).unwrap().children.iter().position(|k| k.attr(scroll::BAR) == Some("v")).unwrap();
    let bp = [sv.clone(), vec![i]].concat();
    let b = ed.app.abs_rect(&bp);
    let page = ed.app.ctrl(&bp).unwrap().attr_f32("realPage", 1.0);
    // Grab the thumb at the top and drag it to the bottom.
    ed.app.mouse_move((b.x + b.w / 2) as f32, (b.y + 3) as f32);
    for ev in ed.app.mouse_down(MouseButton::Left) {
        ed.handle(&ev);
    }
    let travel = b.h as f32 * (1.0 - page);
    for ev in ed.app.mouse_move((b.x + b.w / 2) as f32, b.y as f32 + 3.0 + travel / 2.0) {
        assert!(!matches!(ev, UiEvent::ValueChanged { .. }), "the bar's own value stays inside the toolkit");
        ed.handle(&ev);
    }
    let half = offset(&ed, &sv).1;
    assert!((half - max / 2).abs() <= 2, "{half} vs {}", max / 2);
    ed.app.mouse_move((b.x + b.w / 2) as f32, (b.y + b.h + 200) as f32);
    ed.app.mouse_up(MouseButton::Left);
    assert_eq!(offset(&ed, &sv), (0, max));
}

#[test]
fn layer_parameter_row_scrolls_sideways() {
    let Some(mut ed) = hollow(0, 0) else { return };
    let ps = container(&ed, "ParamScroller");
    let (max, vmax) = range(&ed, &ps);
    assert!(max > 0, "the parameter row overflows at 1000 x 555");
    assert_eq!(vmax, 0);
    assert!(bar(&ed, &ps, "h").visible);
    assert!(!ed.app.ctrl(&ps).unwrap().children.iter().any(|k| k.attr(scroll::BAR) == Some("v") && k.visible));
    hover_off_controls(&mut ed, &ps);
    // Trackpad: a swipe left (platform x negative) shows more on the right.
    wheel(&mut ed, -25.0, 0.0, false);
    assert_eq!(offset(&ed, &ps), (25, 0));
    // The plain wheel scrolls the only axis, shift + wheel too.
    wheel(&mut ed, 0.0, 1.0, true);
    assert_eq!(offset(&ed, &ps), (5, 0));
    ed.app.mods.shift = true;
    wheel(&mut ed, 0.0, -2.0, true);
    ed.app.mods.shift = false;
    assert_eq!(offset(&ed, &ps), (45, 0));
    wheel(&mut ed, -10_000.0, 0.0, false);
    assert_eq!(offset(&ed, &ps), (max, 0));
    wheel(&mut ed, 10_000.0, 0.0, false);
    assert_eq!(offset(&ed, &ps), (0, 0));
    // A wider window shows more; the offset clamps to the new range.
    wheel(&mut ed, -10_000.0, 0.0, false);
    ed.app.resize(1200, 555);
    ed.sync();
    let ps = container(&ed, "ParamScroller");
    let (max2, _) = range(&ed, &ps);
    assert!(max2 < max);
    assert_eq!(offset(&ed, &ps), (max2, 0));
}

#[test]
fn global_mixer_effect_row_scrolls_sideways() {
    // Tall enough to show the editor tabs above the pad editor.
    let Some(mut ed) = hollow_at(5, 0, (1000, 720)) else { return };
    // The compact mixer's Effects mode.
    let group = ed.app.root.path_of("ModeGroup");
    let groups: Vec<Vec<usize>> = {
        let mut v = Vec::new();
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
        rec(&ed.app, &ed.app.root, &mut Vec::new(), &mut v);
        v
    };
    let g = groups.into_iter().next().or(group).expect("mode group");
    ed.handle(&UiEvent::Clicked { path: [g, vec![2]].concat(), name: String::new(), id: 0, on: true });
    ed.sync();
    let fx = container(&ed, "FXScroller");
    let (max, _) = range(&ed, &fx);
    assert!(max > 0, "four effects overflow the compact chain");
    // The chain's bar styles are empty: no bar is drawn.
    assert!(!ed.app.ctrl(&fx).unwrap().children.iter().any(|k| k.attr(scroll::BAR).is_some() && k.visible));
    hover(&mut ed, &fx);
    wheel(&mut ed, -30.0, 0.0, false);
    assert_eq!(offset(&ed, &fx), (30, 0));
    wheel(&mut ed, 0.0, -10_000.0, true);
    assert_eq!(offset(&ed, &fx), (max, 0));
    // The "+" slot ends at the view's right edge.
    let v = scroll::view(ed.app.ctrl(&fx).unwrap());
    let right = ed.app.ctrl(&fx).unwrap().children.iter().filter(|k| k.attr(scroll::BAR).is_none()).map(|k| k.rect.right()).max().unwrap();
    assert_eq!(right, v.w);
}

/// The demo at the smallest window with saved splitter positions.
fn hollow_small(editor_tab: usize, utility_tab: usize, splits: &[(&str, i32)]) -> Option<Editor> {
    let p = dreist_formats::legacy::demo("Presets/Hollow.geist");
    let proj = dreist_formats::Project::load(&p).ok()?;
    let mut o = crate::options::Options::default();
    let (w, h) = dreist_gui::app::MIN_WINDOW;
    o.set("LastEditorSize", format!("{w},{h}"));
    for (k, v) in splits {
        o.set(k, v);
    }
    let mut model = Model::new(proj.raw);
    model.editor_tab = editor_tab;
    model.utility_tab = utility_tab;
    let mut ed = Editor::with_layout(dreist_gui::skin::default_theme(), model, &o).ok()?;
    ed.sync();
    Some(ed)
}

/// Splitters at their limits (left column widest / narrowest, editor tabs
/// tallest / shortest) and the skin's.
const LIMITS: [&[(&str, i32)]; 5] = [&[], &[("utilitySplitAS", 600)], &[("utilitySplitAS", 250)], &[("padSplitterAS", 66)], &[("padSplitterAS", 5000)]];

/// Every shown scroll container named `name`.
fn containers(ed: &Editor, name: &str) -> Vec<Vec<usize>> {
    fn rec(app: &dreist_gui::app::App, c: &Ctrl, name: &str, path: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if c.name == name && scroll::scrollable(c) && app.shown(path) && c.rect.w > 0 && c.rect.h > 0 {
            out.push(path.clone());
        }
        for (i, k) in c.children.iter().enumerate() {
            path.push(i);
            rec(app, k, name, path, out);
            path.pop();
        }
    }
    let mut out = Vec::new();
    rec(&ed.app, &ed.app.root, name, &mut Vec::new(), &mut out);
    out
}

/// Scroll `path` to both ends with the trackpad and the wheel; true when
/// it overflowed.
fn exercise(ed: &mut Editor, path: &[usize], what: &str) -> bool {
    let (mx, my) = range(ed, path);
    if mx == 0 && my == 0 {
        return false;
    }
    hover_off_controls(ed, path);
    let r = ed.app.abs_rect(path);
    let (px, py) = ed.app.mouse_pos();
    assert!(r.contains(px as i32, py as i32), "{what}: pointer inside");
    let hit = ed.app.hit(px, py);
    assert!(hit.starts_with(path), "{what}: the container is under the pointer ({hit:?})");
    wheel(ed, -100_000.0, -100_000.0, false);
    assert_eq!(offset(ed, path), (mx, my), "{what}: far end");
    let c = ed.app.ctrl(path).unwrap();
    let v = scroll::view(c);
    let content: Vec<&Ctrl> = c.children.iter().filter(|k| k.attr(scroll::BAR).is_none() && k.visible).collect();
    if mx > 0 {
        assert_eq!(content.iter().map(|k| k.rect.right()).max().unwrap(), v.w, "{what}: last item at the right edge");
    }
    if my > 0 {
        assert_eq!(content.iter().map(|k| k.rect.bottom()).max().unwrap(), v.h, "{what}: last item at the bottom");
    }
    wheel(ed, 0.0, 100.0, true);
    ed.app.mods.shift = true;
    wheel(ed, 0.0, 100.0, true);
    ed.app.mods.shift = false;
    assert_eq!(offset(ed, path), (0, 0), "{what}: back at the start");
    true
}

#[test]
fn mixers_scroll_in_every_view_at_the_smallest_window() {
    let mut overflowed = std::collections::BTreeSet::new();
    for splits in LIMITS {
        for tab in [3, 4, 5] {
            for mode in 0..3 {
                let Some(mut ed) = hollow_small(tab, 0, splits) else { return };
                let groups: Vec<Vec<usize>> = {
                    let mut v = Vec::new();
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
                    rec(&ed.app, &ed.app.root, &mut Vec::new(), &mut v);
                    v
                };
                if let Some(g) = groups.first() {
                    let b = [g.clone(), vec![mode]].concat();
                    if ed.app.ctrl(&b).is_some_and(|c| c.enabled) {
                        ed.handle(&UiEvent::Clicked { path: b, name: String::new(), id: 0, on: true });
                        ed.sync();
                    }
                }
                for name in ["ChannelScroller", "FXScroller"] {
                    for p in containers(&ed, name) {
                        let what = format!("{splits:?} tab {tab} mode {mode} {name}");
                        if exercise(&mut ed, &p, &what) {
                            overflowed.insert(format!("tab {tab} {name}"));
                        }
                    }
                }
            }
        }
    }
    // The pad and global mixers' strips and the chains overflow somewhere.
    for k in ["tab 4 ChannelScroller", "tab 5 ChannelScroller", "tab 5 FXScroller"] {
        assert!(overflowed.contains(k), "{k} never overflowed: {overflowed:?}");
    }
}

#[test]
fn transmod_and_layer_rows_scroll_at_the_smallest_window() {
    for splits in LIMITS {
        let Some(mut ed) = hollow_small(0, 1, splits) else { return };
        for p in containers(&ed, "ScrollView") {
            exercise(&mut ed, &p, &format!("{splits:?} transmod"));
        }
        for p in containers(&ed, "ParamScroller") {
            assert!(exercise(&mut ed, &p, &format!("{splits:?} layer parameters")), "the parameter row overflows at the smallest window");
        }
    }
}

#[test]
fn browser_sources_scroll_when_they_overflow() {
    let Some(mut ed) = hollow_small(0, 0, &[("padSplitterAS", 330)]) else { return };
    let Some(sp) = ed.app.root.path_of("SourceList").or_else(|| {
        fn rec(c: &Ctrl, path: &mut Vec<usize>) -> Option<Vec<usize>> {
            if c.overload == "BrowserSourceList" {
                return Some(path.clone());
            }
            for (i, k) in c.children.iter().enumerate() {
                path.push(i);
                if let Some(p) = rec(k, path) {
                    return Some(p);
                }
                path.pop();
            }
            None
        }
        rec(&ed.app.root, &mut Vec::new())
    }) else {
        panic!("source list")
    };
    let r = ed.app.abs_rect(&sp);
    assert!(r.h > 50 && (ed.browser.as_ref().unwrap().sources_len() as i32) * 25 > r.h, "the sources overflow {r:?}");
    let _ = ed.render_frame(1.0);
    ed.app.mouse_move((r.x + r.w / 2) as f32, (r.y + r.h / 2) as f32);
    wheel(&mut ed, 0.0, -100.0, true);
    let _ = ed.render_frame(1.0);
    let off = ed.browser.as_ref().unwrap().source_scroll();
    let rows = ed.browser.as_ref().unwrap().sources_len() as f32 * 25.0;
    assert_eq!(off, (rows - r.h as f32).max(0.0), "clamped at the last row");
    wheel(&mut ed, 0.0, 100.0, true);
    assert_eq!(ed.browser.as_ref().unwrap().source_scroll(), 0.0);
}

#[test]
fn device_tables_scroll_long_lists() {
    struct Many;
    impl crate::devices::DeviceHost for Many {
        fn audio(&self, _: &str, _: &str) -> crate::devices::AudioSetup {
            crate::devices::AudioSetup::default()
        }
        fn midi(&self) -> crate::devices::MidiSetup {
            crate::devices::MidiSetup { inputs: (0..40).map(|i| format!("Port {i}")).collect(), outputs: vec!["Out".into()] }
        }
        fn restart(&self, _: &dreist_formats::Node, _: Option<&std::path::Path>) {}
    }
    let Ok(mut ed) = Editor::new(dreist_gui::skin::default_theme(), Model::new(dreist_formats::Node::new("root", None))) else { return };
    ed.devices.host = Some(Box::new(Many));
    ed.show_modal("midi");
    std::thread::sleep(std::time::Duration::from_millis(600));
    ed.animate();
    ed.sync();
    let _ = ed.render_frame(1.0);
    let t = {
        fn rec(c: &Ctrl, path: &mut Vec<usize>) -> Option<Vec<usize>> {
            if c.overload == "DeviceTable:InputTable" {
                return Some(path.clone());
            }
            for (i, k) in c.children.iter().enumerate() {
                path.push(i);
                if let Some(p) = rec(k, path) {
                    return Some(p);
                }
                path.pop();
            }
            None
        }
        rec(&ed.app.root, &mut Vec::new()).expect("input table")
    };
    let r = ed.app.abs_rect(&t);
    ed.app.mouse_move((r.x + r.w / 2) as f32, (r.y + r.h / 2) as f32);
    wheel(&mut ed, 0.0, -3.0, true);
    assert_eq!(ed.devices.first_row("InputTable"), 3);
    wheel(&mut ed, 0.0, -1000.0, true);
    let fit = ((r.h as f32 - 20.0) / 18.0).floor() as usize;
    assert_eq!(ed.devices.first_row("InputTable"), 40 - fit);
    wheel(&mut ed, 0.0, 1000.0, true);
    assert_eq!(ed.devices.first_row("InputTable"), 0);
}

#[test]
fn scene_engine_table_scrolls_when_squeezed() {
    let Some(mut ed) = hollow_at(1, 0, (1000, 720)) else { return };
    let t = {
        fn rec(c: &Ctrl, path: &mut Vec<usize>) -> Option<Vec<usize>> {
            if c.overload == "SceneDetailsTable" {
                return Some(path.clone());
            }
            for (i, k) in c.children.iter().enumerate() {
                path.push(i);
                if let Some(p) = rec(k, path) {
                    return Some(p);
                }
                path.pop();
            }
            None
        }
        rec(&ed.app.root, &mut Vec::new()).expect("details table")
    };
    // Squeezed to 70 px: 14 px rows, 9 of them (header + 8 engines).
    ed.app.ctrl_mut(&t).unwrap().rect.h = 70;
    let _ = ed.render(1.0);
    let r = ed.app.abs_rect(&t);
    ed.app.mouse_move((r.x + r.w / 2) as f32, (r.y + r.h / 2) as f32);
    wheel(&mut ed, 0.0, -2.0, true);
    assert_eq!(ed.scenes.as_ref().unwrap().details_scroll(), 28.0);
    wheel(&mut ed, 0.0, -100.0, true);
    assert_eq!(ed.scenes.as_ref().unwrap().details_scroll(), (9 * 14 - 70) as f32);
    wheel(&mut ed, 0.0, 100.0, true);
    assert_eq!(ed.scenes.as_ref().unwrap().details_scroll(), 0.0);
}
