//! `CtrlSplitterPanel`: two panels either side of a draggable bar.
//!
//! - `Serialize` 0x60aa90: `optIsVertical` (default true: panels stacked
//!   top / bottom), `intMinSize0/1` (0), `intMaxSize0/1` (−1),
//!   `optSnapCollapse0/1` (true), `intSplitterDim` (5),
//!   `optDbClkCollapse1` (true), `optSplitterIsLocked` (false),
//!   `strAutoSaveName`, `optIsUserDraggable` (true), `intSplitPosition`.
//! - `GetClampedSplitterPosition` 0x609d00: with `total` = size − bar,
//!   past `total − min1` the position stops there, or snaps to `total`
//!   (panel 1 collapsed) beyond `total − min1/2` when `optSnapCollapse1`;
//!   below `min0` it stops at `min0`, or snaps to 0 below `min0/2` when
//!   `optSnapCollapse0`; then at most `intMaxSize0` (−1 none).
//!   `intMaxSize1` is never used.
//! - The bar (`SplitterPanelRenderer`): mouse down ($_0 0x60b5f0) unless
//!   locked keeps the position; `OnMouseMove` 0x609bb0 (draggable only)
//!   moves it by the pointer's travel, clamped; mouse up / `OnMouseLButtonUp`
//!   0x609dd0 writes the position to the registry under `strAutoSaveName`;
//!   double click ($_2 0x60b850, not locked) `InvertCollapseStatus`
//!   0x609550: at either end → back to the saved position, else save it
//!   and go to the end (`optDbClkCollapse1`) or 0, clamped and animated
//!   (`SetSplitterPosition` 0x609650: 250 ms Linear bounds animation).
//!   Enter ($_3 0x60b9a0, not locked, draggable): up / down cursor when
//!   vertical, left / right otherwise; exit ($_4): arrow.
//! - `SplitterPanelRenderer::Draw` 0x608400: the bar's style background,
//!   then (thin side > 3 px) seven 4×4 dots 6 px apart, centred, in the
//!   style's colAltBorder (default white).
//! - `Editor::open` 0x171b00 → `ReadStateFromRegistry` 0x60b4e0: a saved
//!   position ≥ 0 is clamped and applied.

use crate::ctrl::{Ctrl, Rect};

pub fn vertical(c: &Ctrl) -> bool {
    c.attr_bool("optIsVertical", true)
}

pub fn dim(c: &Ctrl) -> i32 {
    c.attr_i32("intSplitterDim", 5).max(1)
}

pub fn position(c: &Ctrl) -> i32 {
    c.attr_i32("intSplitPosition", 0)
}

pub fn locked(c: &Ctrl) -> bool {
    c.attr_bool("optSplitterIsLocked", false)
}

pub fn draggable(c: &Ctrl) -> bool {
    c.attr_bool("optIsUserDraggable", true)
}

/// The bar's rect (relative to the splitter panel).
pub fn bar(c: &Ctrl) -> Rect {
    let (p, d) = (position(c), dim(c));
    if vertical(c) { Rect::new(0, p, c.rect.w, d) } else { Rect::new(p, 0, d, c.rect.h) }
}

/// Whether (`x`, `y`) (relative to the panel) is on the bar.
pub fn on_bar(c: &Ctrl, x: i32, y: i32) -> bool {
    c.class == "CtrlSplitterPanel" && {
        let b = bar(c);
        x >= b.x && x < b.x + b.w && y >= b.y && y < b.y + b.h
    }
}

fn length(c: &Ctrl) -> i32 {
    if vertical(c) { c.rect.h } else { c.rect.w }
}

/// `GetClampedSplitterPosition`.
pub fn clamp(c: &Ctrl, p: i32) -> i32 {
    let total = length(c) - dim(c);
    let (min0, min1) = (c.attr_i32("intMinSize0", 0), c.attr_i32("intMinSize1", 0));
    let mut v = p;
    if v > total - min1 {
        v = if c.attr_bool("optSnapCollapse1", true) && v > total - min1 / 2 { total } else { total - min1 };
    }
    if v < min0 {
        v = if c.attr_bool("optSnapCollapse0", true) && v < min0 / 2 { 0 } else { min0 };
    }
    let max0 = c.attr_i32("intMaxSize0", -1);
    if max0 != -1 && v > max0 {
        v = max0;
    }
    v
}

/// Move the bar to `p` (unclamped) and lay the panels out.
pub fn set_position(c: &mut Ctrl, p: i32) {
    c.set_attr("intSplitPosition", p.to_string());
    c.layout_splitter();
}

/// `InvertCollapseStatus`: the position to animate to (remembers the
/// current one when collapsing).
pub fn invert_collapse(c: &mut Ctrl) -> i32 {
    let (p, end) = (position(c), length(c));
    let at_end = p == 0 || p + dim(c) == end;
    if at_end {
        return clamp(c, c.attr_i32("savedSplit", 0));
    }
    c.set_attr("savedSplit", p.to_string());
    clamp(c, if c.attr_bool("optDbClkCollapse1", true) { end } else { 0 })
}

/// A running `SetSplitterPosition` animation.
#[derive(Clone, Debug)]
pub struct Anim {
    pub path: Vec<usize>,
    pub from: i32,
    pub to: i32,
    pub start: std::time::Instant,
}

/// Animation length (`SetSplitterPosition`, Linear).
pub const ANIM_MS: f32 = 250.0;

#[cfg(test)]
mod tests {
    use super::*;

    fn split(attrs: &[(&str, &str)]) -> Ctrl {
        let mut c = Ctrl { class: "CtrlSplitterPanel".into(), rect: Rect::new(0, 0, 1390, 746), ..Ctrl::default() };
        for (k, v) in attrs {
            c.attrs.insert((*k).into(), (*v).into());
        }
        c
    }

    #[test]
    fn utility_splitter_clamps_and_snaps() {
        // RootSkin's UtilitySplitter.
        let c = split(&[("intMaxSize0", "600"), ("intMinSize0", "250"), ("intSplitPosition", "300"), ("intSplitterDim", "8"), ("optDbClkCollapse1", "false"), ("optIsVertical", "false")]);
        assert_eq!(clamp(&c, 400), 400);
        assert_eq!(clamp(&c, 900), 600);
        assert_eq!(clamp(&c, 200), 250);
        assert_eq!(clamp(&c, 100), 0);
        let mut c = c;
        let to = invert_collapse(&mut c);
        assert_eq!(to, 0);
        set_position(&mut c, to);
        assert_eq!(invert_collapse(&mut c), 300);
        assert_eq!(bar(&c), Rect::new(0, 0, 8, 746));
    }

    #[test]
    fn panel_one_snaps_shut() {
        let c = split(&[("intMinSize1", "220"), ("intSplitterDim", "8")]);
        // total = 746 − 8 = 738.
        assert_eq!(clamp(&c, 600), 518);
        assert_eq!(clamp(&c, 700), 738);
    }
}
