//! [re:28a1ae] ([re:bd0c5b]..) and the [re:1402db] zoom logic
//! shared by the layer wave display: the view is (start, size) as fractions
//! of the file. See the dreist-re GUI notes (Zoom slider, Wave display zoom).

use dreist_gui::colour::Colour;
use dreist_gui::paint::{Painter, RectF};
use dreist_gui::style::StyleSheet;

pub use dreist_editor_core::zoomslider::*;

/// [re:867658]: the thumb in colFill, then the slider's whole-file
/// waveform ([re:51bcb1]: a child wave display filling the slider in
/// `WaveDisplayZoomSliderWaveStyle`), then 2 px white edge lines and white
/// 10 px discs with black 6 px centres. `overview` is the file's (min,
/// max) per bucket, start to end (empty: no file).
pub fn draw(p: &mut Painter, s: &StyleSheet, style: &str, w: f32, h: f32, view: (f32, f32), overview: &[(f32, f32)]) {
    let (tx, tw) = thumb(view, w);
    p.fill_rect(RectF::new(tx, 0.0, tw, h), s.colour(style, "colFill", Colour::rgba(255, 192, 203, 255)));
    draw_overview(p, s, w, h, overview);
    for ex in [tx, tx + tw] {
        p.fill_rect(RectF::new(ex - 1.0, 0.0, 2.0, h), Colour::WHITE);
    }
    let cy = (h as i32 / 2) as f32;
    for ex in [tx, tx + tw] {
        p.fill_ellipse(RectF::new(ex - 5.0, cy - 5.0, 10.0, 10.0), Colour::WHITE);
        p.fill_ellipse(RectF::new(ex - 3.0, cy - 3.0, 6.0, 6.0), Colour::BLACK);
    }
}

/// The slider's waveform: the whole file without markers ([re:5d27b8]),
/// drawn as a wave channel ([re:d2ec05]): the centre line in colLine at
/// α0.5, then per pixel column the min/max envelope in colLine
/// ([re:5d9cb1]: colour 0x20).
fn draw_overview(p: &mut Painter, s: &StyleSheet, w: f32, h: f32, buckets: &[(f32, f32)]) {
    let n = buckets.len();
    if n == 0 || w < 1.0 {
        return;
    }
    let line = s.colour(WAVE_STYLE, "colLine", Colour::rgba(255, 192, 203, 255));
    let mid = (h / 2.0).floor();
    p.fill_rect(RectF::new(0.0, mid, w, 1.0), line.with_alpha(0.5));
    let cols = w as usize;
    for x in 0..cols {
        let a = (x * n / cols).min(n - 1);
        let b = ((x + 1) * n / cols).clamp(a + 1, n);
        let (lo, hi) = buckets[a..b].iter().fold((f32::MAX, f32::MIN), |(l0, h0), &(l1, h1)| (l0.min(l1), h0.max(h1)));
        let y0 = h / 2.0 - hi.clamp(-1.0, 1.0) * h / 2.0;
        let y1 = h / 2.0 - lo.clamp(-1.0, 1.0) * h / 2.0;
        p.fill_rect(RectF::new(x as f32, y0, 1.0, (y1 - y0).max(1.0)), line);
    }
}

/// The slider waveform's style.
const WAVE_STYLE: &str = "WaveDisplayZoomSliderWaveStyle";
