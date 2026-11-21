//! Popup buttons and their menus: pad mode, layer playback mode, choke (cut
//! mode), layer filter algorithm and type, and pattern step length. Labels come from the original's name maps
//! ([re:ceabd7]: layer cut mode,
//! layer playback mode; `RESOLUTION_NAMES`).

use dreist_dsp::voice::{PLAYBACK_MODE_LABELS, PLAYBACK_MODE_NAMES};
use dreist_dsp::voices::{CUT_MODE_LABELS, CUT_MODE_NAMES};
use dreist_engine::binding::id;
use dreist_engine::live::PadMode;
use dreist_engine::pattern::RESOLUTION_NAMES;
use dreist_formats::LayerParam;
use dreist_gui::app::{App, PathCache, UiEvent};

use crate::command::{Command, msg};
use crate::model::Model;

/// Layer filter algorithms (`round(FilterAlgorithm · 3)`, [re:9f92ff]).
pub const FILTER_ALGORITHM_LABELS: [&str; 4] = ["Japan", "SVF", "MS20", "Comb"];
/// [re:6f3ef7].
pub const SVF_MODES: [&str; 10] = ["L2", "L4", "H2", "H4", "B2", "B4", "N2", "N4", "P2", "P4"];
/// The comb core's two polarities (`mode < 0.5` negative).
const COMB_MODES: [&str; 2] = ["Negative", "Positive"];

/// The filter type names of algorithm `a` (an index into
/// [`FILTER_ALGORITHM_LABELS`]); the menu's items are spread evenly over
/// 0..=1, which each core rounds back to its mode.
pub fn filter_types(a: usize) -> &'static [&'static str] {
    match a {
        0 => &dreist_dsp::sh101::SH101_MODES,
        1 => &SVF_MODES,
        2 => &dreist_dsp::ms20::MS20_MODES,
        _ => &COMB_MODES,
    }
}

/// The selected layer's filter algorithm index.
fn filter_algorithm(model: &Model) -> usize {
    let e = model.engine;
    ((model.layer_param(e, model.pad[e], model.layer[e], LayerParam::FilterAlgorithm) * 3.0).round().max(0.0) as usize).min(3)
}

/// The selected layer's filter type index within its algorithm's types.
fn filter_type(model: &Model) -> usize {
    let e = model.engine;
    let n = filter_types(filter_algorithm(model)).len() - 1;
    ((model.layer_param(e, model.pad[e], model.layer[e], LayerParam::FilterType) * n as f32).round().max(0.0) as usize).min(n)
}

pub const PAD_MODE_LABELS: [&str; 6] = ["Normal", "Chromatic", "Velocity", "Engine M+S", "Sampler", "x0x"];

/// Index of a layer's stored mode (display name, or enum name from older
/// port builds) in `labels` / `names`.
fn layer_attr_index(model: &Model, key: &str, labels: &[&str], names: &[&str], default: usize) -> usize {
    let e = model.engine;
    let v = model.layer_node(e, model.pad[e], model.layer[e]).and_then(|n| n.attr(key)).map(str::trim);
    v.and_then(|v| labels.iter().position(|x| *x == v).or_else(|| names.iter().position(|x| *x == v))).unwrap_or(default)
}

/// Items and checked index for a popup control, if it is one we drive.
fn menu_for(model: &Model, name: &str) -> Option<(&'static [&'static str], usize)> {
    let e = model.engine;
    Some(match name {
        "PadMode" => (&PAD_MODE_LABELS, model.pad_mode(e).index() as usize),
        "PlayMode" => (&PLAYBACK_MODE_LABELS, layer_attr_index(model, "PlaybackMode", &PLAYBACK_MODE_LABELS, &PLAYBACK_MODE_NAMES, 0)),
        "Choke" => (&CUT_MODE_LABELS, layer_attr_index(model, "CutMode", &CUT_MODE_LABELS, &CUT_MODE_NAMES, 1)),
        "StepLengthCombo" => (&RESOLUTION_NAMES, model.pattern_resolution(e, model.current_pattern(e)).min(13)),
        "FilterAlgorithm" => (&FILTER_ALGORITHM_LABELS, filter_algorithm(model)),
        "FilterType" => (filter_types(filter_algorithm(model)), filter_type(model)),
        _ => return None,
    })
}

pub fn sync(app: &mut App, model: &Model, paths: &PathCache) {
    for name in ["PadMode", "PlayMode", "Choke", "StepLengthCombo", "FilterAlgorithm", "FilterType"] {
        let Some((items, i)) = menu_for(model, name) else { continue };
        if let Some(c) = paths.ctrl_mut(app, name) {
            c.text = items.get(i).map(|s| s.to_string()).unwrap_or_default();
        }
    }
}

pub fn handle(app: &mut App, model: &mut Model, ev: &UiEvent, out: &mut Vec<Command>) -> bool {
    match ev {
        UiEvent::Clicked { path, name, .. } => {
            if app.ctrl(path).map(|c| c.class.as_str()) != Some("CtrlPopupButton") {
                return false;
            }
            if let Some((items, checked)) = menu_for(model, name) {
                app.open_menu(path, items.iter().map(|s| s.to_string()).collect(), Some(checked));
            }
            false
        }
        UiEvent::MenuSelected { name, index, .. } => {
            let e = model.engine;
            let (p, l) = (model.pad[e], model.layer[e]);
            match name.as_str() {
                "PadMode" => {
                    let label = PAD_MODE_LABELS[(*index).min(5)];
                    out.push(Command::SetPadMode { engine: e, mode: PadMode::from_name(label) });
                    if let Some(n) = model.doc.children.iter_mut().find(|c| c.class == "Engine" && c.name.as_deref() == Some(&format!("Engine{e}"))) {
                        n.set("EnginePadMode", label);
                    }
                }
                "PlayMode" => out.push(msg(id::SET_LAYER_PLAY_MODE, &[e as i32, p as i32, l as i32], &[*index as f32])),
                "Choke" => out.push(msg(id::SET_LAYER_CUT_MODE, &[e as i32, p as i32, l as i32], &[*index as f32])),
                "FilterAlgorithm" => out.push(msg(id::SET_LAYER_PARAMETER, &[e as i32, p as i32, l as i32], &[LayerParam::FilterAlgorithm as u8 as f32, (*index).min(3) as f32 / 3.0, 0.0])),
                "FilterType" => {
                    let n = (filter_types(filter_algorithm(model)).len() - 1).max(1) as f32;
                    out.push(msg(id::SET_LAYER_PARAMETER, &[e as i32, p as i32, l as i32], &[LayerParam::FilterType as u8 as f32, (*index as f32 / n).min(1.0), 0.0]))
                }
                "StepLengthCombo" => out.push(msg(id::SET_PATTERN_STEP_LENGTH, &[e as i32, -1, -1, model.current_pattern(e) as i32], &[*index as f32])),
                _ => return false,
            }
            true
        }
        _ => false,
    }
}
