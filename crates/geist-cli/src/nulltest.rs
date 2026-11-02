//! `geist-nulltest <reference.wav> <port.wav> [--residual out.wav] [--max-lag N]`:
//! align a port render with a reference render of the original (integer
//! lag by cross-correlation), report the residual per second and overall,
//! and optionally write the aligned residual (port − reference).

use std::path::Path;
use std::process::ExitCode;

use geist_engine::audio;

struct Stereo {
    left: Vec<f32>,
    right: Vec<f32>,
}

fn mono(l: &[f32], r: &[f32]) -> Vec<f32> {
    l.iter().zip(r).map(|(a, b)| 0.5 * (a + b)).collect()
}

/// Lag `d` such that `port[i + d] ≈ reference[i]`, searched in ±`max`
/// over the first `span` samples.
fn best_lag(reference: &[f32], port: &[f32], max: i64, span: usize) -> (i64, f64) {
    let n = span.min(reference.len()).min(port.len());
    let mut best = (0, f64::MIN);
    for d in -max..=max {
        let mut acc = 0.0f64;
        for i in 0..n {
            let j = i as i64 + d;
            if j >= 0 && (j as usize) < port.len() {
                acc += reference[i] as f64 * port[j as usize] as f64;
            }
        }
        if acc > best.1 {
            best = (d, acc);
        }
    }
    best
}

fn db(x: f64) -> f64 {
    10.0 * x.max(1e-20).log10()
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut pos = Vec::new();
    let mut residual_path = None;
    let mut max_lag = 4096i64;
    let mut it = args.iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--residual" => residual_path = it.next().cloned(),
            "--max-lag" => max_lag = it.next().and_then(|v| v.parse().ok()).unwrap_or(max_lag),
            _ => pos.push(a.clone()),
        }
    }
    if pos.len() < 2 {
        eprintln!("usage: geist-nulltest <reference.wav> <port.wav> [--residual out.wav] [--max-lag N]");
        return ExitCode::FAILURE;
    }
    let (a, b) = match (audio::load(Path::new(&pos[0])), audio::load(Path::new(&pos[1]))) {
        (Ok(a), Ok(b)) => (a, b),
        (Err(e), _) | (_, Err(e)) => {
            eprintln!("{e}");
            return ExitCode::FAILURE;
        }
    };
    let sr = a.sample_rate;
    let stereo = |d: geist_dsp::voice::SampleData| {
        let r = d.right.unwrap_or_else(|| d.left.clone());
        (d.left, r)
    };
    let b_sr = b.sample_rate;
    let (a, b) = (stereo(a), stereo(b));
    let (a, b) = (Stereo { left: a.0, right: a.1 }, Stereo { left: b.0, right: b.1 });
    if (sr - b_sr).abs() > 0.5 {
        eprintln!("sample rates differ: {} vs {}", sr, b_sr);
        return ExitCode::FAILURE;
    }
    let (ma, mb) = (mono(&a.left, &a.right), mono(&b.left, &b.right));
    // Correlate over the first stretch that has signal in the reference.
    let start = ma.iter().position(|x| x.abs() > 1e-4).unwrap_or(0);
    let (lag, _) = best_lag(&ma[start..], &mb[(start as i64 - max_lag).max(0) as usize..], max_lag * 2, sr as usize * 4);
    let lag = lag + (start as i64 - max_lag).max(0) - start as i64;
    println!("lag {lag} samples ({:.2} ms), reference starts at {:.3} s", lag as f64 * 1000.0 / sr as f64, start as f64 / sr as f64);

    let n = a.left.len();
    let at = |v: &[f32], i: usize| -> f32 {
        let j = i as i64 + lag;
        if j >= 0 && (j as usize) < v.len() { v[j as usize] } else { 0.0 }
    };
    // Least-squares gain of port against reference (reported, not applied).
    let (mut xy, mut yy) = (0.0f64, 0.0f64);
    for i in 0..n {
        for (x, y) in [(a.left[i], at(&b.left, i)), (a.right[i], at(&b.right, i))] {
            xy += x as f64 * y as f64;
            yy += y as f64 * y as f64;
        }
    }
    println!("best gain port→ref {:.4} ({:+.2} dB)", xy / yy.max(1e-20), 20.0 * (xy / yy.max(1e-20)).abs().max(1e-10).log10());

    let mut rl = vec![0.0f32; n];
    let mut rr = vec![0.0f32; n];
    for i in 0..n {
        rl[i] = at(&b.left, i) - a.left[i];
        rr[i] = at(&b.right, i) - a.right[i];
    }
    let sec = sr as usize;
    println!("  sec   ref dB   port dB   resid dB   null dB");
    let (mut te, mut tr) = (0.0f64, 0.0f64);
    for s in 0..n.div_ceil(sec) {
        let r = s * sec..((s + 1) * sec).min(n);
        let (mut e, mut p, mut d) = (0.0f64, 0.0f64, 0.0f64);
        for i in r.clone() {
            e += (a.left[i] as f64).powi(2) + (a.right[i] as f64).powi(2);
            p += (at(&b.left, i) as f64).powi(2) + (at(&b.right, i) as f64).powi(2);
            d += (rl[i] as f64).powi(2) + (rr[i] as f64).powi(2);
        }
        te += e;
        tr += d;
        let len = (2 * r.len()) as f64;
        println!("{s:5} {:8.1} {:9.1} {:10.1} {:9.1}", db(e / len), db(p / len), db(d / len), db(d / e.max(1e-20)));
    }
    println!("overall null depth {:.1} dB (residual energy / reference energy)", db(tr / te.max(1e-20)));
    if let Some(p) = residual_path {
        if let Err(e) = geist_engine::write_wav(Path::new(&p), sr as u32, &rl, &rr) {
            eprintln!("{p}: {e}");
            return ExitCode::FAILURE;
        }
    }
    ExitCode::SUCCESS
}
