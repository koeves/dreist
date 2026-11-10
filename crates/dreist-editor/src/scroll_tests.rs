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
    hover(&mut ed, &ps);
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
    wheel(&mut ed, -40.0, 0.0, false);
    assert_eq!(offset(&ed, &fx), (40, 0));
    wheel(&mut ed, 0.0, -10_000.0, true);
    assert_eq!(offset(&ed, &fx), (max, 0));
    // The "+" slot ends at the view's right edge.
    let v = scroll::view(ed.app.ctrl(&fx).unwrap());
    let right = ed.app.ctrl(&fx).unwrap().children.iter().filter(|k| k.attr(scroll::BAR).is_none()).map(|k| k.rect.right()).max().unwrap();
    assert_eq!(right, v.w);
}
