//! Render effect cards to PNG: `fxshot <out_dir> [scale] [type...]` puts
//! the given effect types (index in `EFFECT_TYPES`; default all, 1..=47)
//! into the selected engine's chain of the demo project, six at a time,
//! shows the Global Mixer page and saves each card as `<out_dir>/<type>.png`
//! (250 x 182 points at `scale`). Each effect starts from its type's
//! `Default.fxpreset` (under `DREIST_RESOURCES`/`Effects`, else bare).
//! `FXSHOT_GR=v` feeds every slot the control output `v` (the
//! gain-reduction meters) before rendering.

use dreist_formats::params::{EFFECT_TYPES, effect_param_names};
use dreist_gui::tiny_skia::IntRect;

fn defaults(kind: usize) -> Option<dreist_formats::Node> {
    let dir = dreist_formats::paths::resources_dir().join("Effects");
    let path = dir.join(EFFECT_TYPES[kind]).join("Default.fxpreset");
    let root = dreist_formats::Node::parse(&std::fs::read_to_string(path).ok()?).ok()?;
    let mut n = root.children.into_iter().find(|c| c.class == "Effect")?;
    let names = effect_param_names(kind);
    for (k, _) in n.attrs.iter_mut() {
        if let Some(pn) = k.strip_prefix("Parameter").and_then(|i| i.parse::<usize>().ok()).and_then(|i| names.get(i)) {
            *k = pn.chars().filter(|c| !c.is_whitespace()).collect();
        }
    }
    Some(n)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let out = std::path::PathBuf::from(args.get(1).expect("out dir"));
    let scale: f32 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2.0);
    let mut kinds: Vec<usize> = args.iter().skip(3).filter_map(|s| s.parse().ok()).collect();
    if kinds.is_empty() {
        kinds = (1..EFFECT_TYPES.len()).collect();
    }
    let gr: Option<f32> = std::env::var("FXSHOT_GR").ok().and_then(|v| v.parse().ok());
    std::fs::create_dir_all(&out).unwrap();
    for group in kinds.chunks(6) {
        let mut ed = dreist_editor::screens::editor().expect("demo content");
        ed.app.resize(2600, 1000);
        ed.model.editor_tab = 5; // Global Mixer
        let e = ed.model.engine;
        let chain = ed.model.engine_mut(e).child_mut_or_insert("EffectChain", "EffectChain");
        chain.children.retain(|c| c.class != "Effect");
        for (slot, kind) in group.iter().enumerate() {
            let mut fx = defaults(*kind).unwrap_or_else(|| dreist_formats::Node::new("Effect", None));
            fx.name = Some(format!("Effect{slot}"));
            fx.set("EffectType", EFFECT_TYPES[*kind]).set("IsActive", "true");
            chain.children.push(fx);
        }
        ed.sync();
        if let Some(v) = gr {
            let mut m = dreist_engine::Meters::default();
            for slot in 0..group.len() {
                m.fx_out.push(dreist_engine::FxOut { at: [e as i8, -1, -1], slot: slot as u8, value: v });
            }
            ed.update_meters(&m);
        }
        let img = ed.render(scale);
        let mut cards = Vec::new();
        fn find(c: &dreist_gui::Ctrl, path: &mut Vec<usize>, out: &mut Vec<(Vec<usize>, usize)>) {
            if let Some(slot) = c.attr("fxSlot").and_then(|v| v.parse().ok()) {
                out.push((path.clone(), slot));
                return;
            }
            for (i, k) in c.children.iter().enumerate() {
                path.push(i);
                find(k, path, out);
                path.pop();
            }
        }
        find(&ed.app.root, &mut Vec::new(), &mut cards);
        for (path, slot) in cards {
            let Some(kind) = group.get(slot) else { continue };
            let r = ed.app.abs_rect(&path);
            let ir = IntRect::from_xywh((r.x as f32 * scale) as i32, (r.y as f32 * scale) as i32, (r.w as f32 * scale) as u32, (r.h as f32 * scale) as u32).unwrap();
            img.clone_rect(ir).unwrap().save_png(out.join(format!("{kind}.png"))).unwrap();
        }
    }
}
