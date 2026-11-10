//! Control interactions as the original's stock controls behave: the
//! steps buttons' modifiers, the tempo box's drag / tap / double-click
//! edit, control-click menus and transmod knob wheel steps.
use super::*;
use dreist_engine::binding::id;
use dreist_gui::app::{MouseButton, UiEvent};

fn hollow() -> Option<Editor> {
    let proj = dreist_formats::Project::load(&dreist_formats::legacy::demo("Presets/Hollow.geist")).ok()?;
    let mut ed = Editor::new(dreist_gui::skin::default_theme(), Model::new(proj.raw)).ok()?;
    ed.sync();
    Some(ed)
}

fn feed(ed: &mut Editor, evs: Vec<UiEvent>) {
    for ev in evs {
        ed.handle(&ev);
    }
}

/// Move to the centre of the shown control `name` (offset by `dx`).
fn point_at(ed: &mut Editor, name: &str, dx: f32) -> Vec<usize> {
    let p = ed.app.root.path_of(name).unwrap_or_else(|| panic!("{name}"));
    let r = ed.app.abs_rect(&p);
    let ev = ed.app.mouse_move(r.x as f32 + r.w as f32 / 2.0 + dx, r.y as f32 + r.h as f32 / 2.0);
    feed(ed, ev);
    p
}

fn click(ed: &mut Editor) {
    let ev = ed.app.mouse_down(MouseButton::Left);
    feed(ed, ev);
    let ev = ed.app.mouse_up(MouseButton::Left);
    feed(ed, ev);
}

fn values(ed: &mut Editor, kind: u32) -> Vec<f32> {
    ed.take_commands().into_iter().filter_map(|c| if let Command::Message(m) = c { (m.kind == kind).then_some(m.value[0]) } else { None }).collect()
}

#[test]
fn steps_buttons_take_shift_and_option() {
    let Some(mut ed) = hollow() else { return };
    let lb = ed.app.root.path_of("LengthBox").unwrap();
    // (steps before, steps sent)
    let press = |ed: &mut Editor, name: &str, shift: bool, alt: bool| {
        let n: f32 = ed.app.ctrl(&lb).unwrap().text.parse().unwrap();
        point_at(ed, name, 0.0);
        ed.app.mods = dreist_gui::app::Mods { shift, alt, ..Default::default() };
        ed.take_commands();
        // Apart from the previous press (no double click).
        std::thread::sleep(std::time::Duration::from_millis(410));
        click(ed);
        ed.app.mods = Default::default();
        ed.sync();
        (n, values(ed, id::SET_PATTERN_STEP_COUNT))
    };
    let (n, v) = press(&mut ed, "PlusButton", false, false);
    assert_eq!(v, vec![n + 1.0]);
    let (n, v) = press(&mut ed, "PlusButton", true, false);
    assert_eq!(v, vec![n + 8.0]);
    let (n, v) = press(&mut ed, "PlusButton", false, true);
    assert_eq!(v, vec![2.0 * n]);
    let (n, v) = press(&mut ed, "MinusButton", true, false);
    assert_eq!(v, vec![n - 8.0]);
    let (n, v) = press(&mut ed, "MinusButton", false, true);
    assert_eq!(v, vec![n - (n as i32 / 2) as f32]);
    // Shift wins over option on minus.
    let (n, v) = press(&mut ed, "MinusButton", true, true);
    assert_eq!(v, vec![n - 8.0]);
}

#[test]
fn tempo_box_drags_taps_and_edits_on_double_click() {
    let Some(mut ed) = hollow() else { return };
    let t0 = ed.model.tempo() as f32;
    // A press on the left half and a 10 px drag up: the whole part.
    point_at(&mut ed, "BPMTextBox", -8.0);
    let ev = ed.app.mouse_down(MouseButton::Left);
    feed(&mut ed, ev);
    assert!(!ed.app.is_editing());
    let (x, y) = ed.app.mouse_pos();
    let ev = ed.app.mouse_move(x, y - 10.0);
    feed(&mut ed, ev);
    let ev = ed.app.mouse_up(MouseButton::Left);
    feed(&mut ed, ev);
    let sent = values(&mut ed, id::SET_TEMPO);
    let want = (((t0 - 20.0) / 230.0 + 10.0 / 200.0) * 230.0 + 20.0).floor() + t0.fract();
    assert!(sent.last().is_some_and(|v| (v - want).abs() < 1e-3), "{sent:?} {want}");
    // Option-clicks tap: four taps 0.25 s apart give 240 BPM.
    point_at(&mut ed, "BPMTextBox", 0.0);
    ed.app.mods.alt = true;
    for i in 0..4 {
        if i > 0 {
            std::thread::sleep(std::time::Duration::from_millis(250));
        }
        click(&mut ed);
    }
    ed.app.mods.alt = false;
    let sent = values(&mut ed, id::SET_TEMPO);
    assert_eq!(sent.len(), 1, "{sent:?}");
    assert!((sent[0] - 240.0).abs() < 15.0, "{sent:?}");
    assert!(!ed.app.is_editing());
    // A double click edits.
    std::thread::sleep(std::time::Duration::from_millis(410));
    click(&mut ed);
    let ev = ed.app.mouse_down(MouseButton::Left);
    feed(&mut ed, ev);
    assert!(ed.app.is_editing());
}

#[test]
fn control_click_opens_the_knob_menu() {
    let Some(mut ed) = hollow() else { return };
    point_at(&mut ed, "Macro0", 0.0);
    ed.app.mods.ctrl = true;
    let ev = ed.app.mouse_down(MouseButton::Left);
    assert!(ev.iter().any(|e| matches!(e, UiEvent::RightClicked { name, .. } if name == "Macro0")), "{ev:?}");
    feed(&mut ed, ev);
    let ev = ed.app.mouse_up(MouseButton::Left);
    feed(&mut ed, ev);
    assert!(ed.app.menu.as_ref().is_some_and(|m| m.items.iter().any(|i| i == "Reset")));
}

#[test]
fn transmod_knobs_take_wheel_steps() {
    let Some(mut ed) = hollow() else { return };
    // A layer knob with no transmod source selected.
    ed.model.source = 0;
    ed.sync();
    let p = point_at(&mut ed, "VoicePan", 0.0);
    let v0 = ed.app.ctrl(&p).unwrap().value;
    ed.take_commands();
    let ev = ed.app.mouse_scroll(0.0, 1.0, true);
    feed(&mut ed, ev);
    let v1 = ed.app.ctrl(&p).unwrap().value;
    assert!((v1 - (v0 + 1.0 / 150.0).min(1.0)).abs() < 1e-5, "{v0} {v1}");
    assert!(!ed.take_commands().is_empty());
}

/// [re:081d3e]: option-dragging a modulated knob's centre moves the base
/// and keeps the modulation end, sending the base and the source's depth
/// together; one undo step restores both.
#[test]
fn option_drag_of_the_base_keeps_the_modulation_end() {
    let Ok(mut ed) = Editor::new(dreist_gui::skin::default_theme(), Model::new(project::new_document())) else { return };
    ed.model.source = 5;
    ed.sync();
    let Some(k) = ed.app.root.path_of("VoicePan") else { return };
    let orig = ed.model.doc.clone();
    let c = ed.app.ctrl(&k).unwrap();
    let (b0, end) = (c.attr_f32("baseValue", 0.0), c.attr_f32("baseValue", 0.0) + c.value * 2.0 - 1.0);
    let r = ed.app.abs_rect(&k);
    let (x, y) = (r.x as f32 + r.w as f32 / 2.0, r.y as f32 + r.h as f32 / 2.0);
    let ev = ed.app.mouse_move(x, y);
    feed(&mut ed, ev);
    ed.app.mods.alt = true;
    ed.take_commands();
    let ev = ed.app.mouse_down(MouseButton::Left);
    feed(&mut ed, ev);
    // 40 px up: 0.2, less the snap's 0.1 lag off the end.
    let ev = ed.app.mouse_move(x, y - 40.0);
    feed(&mut ed, ev);
    let ev = ed.app.mouse_up(MouseButton::Left);
    feed(&mut ed, ev);
    ed.app.mods.alt = false;
    let sent: Vec<[f32; 3]> =
        ed.take_commands().into_iter().filter_map(|c| if let Command::Message(m) = c { (m.kind == id::SET_LAYER_PARAMETER).then(|| [m.value[0], m.value[1], m.value[2]]) } else { None }).collect();
    let base = sent.iter().rfind(|m| m[2] == 0.0).expect("base edit")[1];
    let depth = sent.iter().rfind(|m| m[2] == 5.0).expect("depth edit")[1];
    assert!((base - (b0 + 0.1).min(1.0)).abs() < 1e-5, "{sent:?}");
    assert!((base + depth - end).abs() < 1e-5, "end kept: {sent:?}");
    ed.sync();
    let c = ed.app.ctrl(&k).unwrap();
    assert!((c.attr_f32("baseValue", 0.0) - base).abs() < 1e-5 && (c.attr_f32("modDepth", 0.0) - depth).abs() < 1e-5);
    assert_ne!(ed.model.doc, orig);
    // One undo step for both.
    let undo = ed.app.root.path_of("UndoButton").unwrap();
    ed.handle(&UiEvent::Clicked { path: undo, name: "UndoButton".into(), id: 0, on: false });
    assert_eq!(ed.model.doc, orig);
}
