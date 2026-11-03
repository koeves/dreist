//! `dreist-stemfit <reference.wav> <window-seconds> <stem.wav>...`: per
//! window, least-squares fit the reference as a weighted sum of port stems
//! (one per engine, rendered solo) and print each stem's gain, energy and
//! the null depth before / after the fit. A gain far from 1 points at a
//! level difference in that stem; a poor null after the fit points at a
//! timing or timbre difference.

use std::path::Path;
use std::process::ExitCode;

use dreist_engine::audio;

fn load(p: &str) -> Option<(Vec<f32>, Vec<f32>)> {
    match audio::load(Path::new(p)) {
        Ok(d) => {
            let r = d.right.unwrap_or_else(|| d.left.clone());
            Some((d.left, r))
        }
        Err(e) => {
            eprintln!("{e}");
            None
        }
    }
}

/// Solve `a x = b` (symmetric, small) with Gaussian elimination and a
/// little ridge for silent stems.
fn solve(mut a: Vec<Vec<f64>>, mut b: Vec<f64>) -> Vec<f64> {
    let n = b.len();
    let tr: f64 = (0..n).map(|i| a[i][i]).sum::<f64>() / n as f64;
    for (i, row) in a.iter_mut().enumerate() {
        row[i] += 1e-9 * tr + 1e-12;
    }
    for c in 0..n {
        let p = (c..n).max_by(|&x, &y| a[x][c].abs().total_cmp(&a[y][c].abs())).unwrap();
        a.swap(c, p);
        b.swap(c, p);
        for r in c + 1..n {
            let f = a[r][c] / a[c][c];
            for k in c..n {
                a[r][k] -= f * a[c][k];
            }
            b[r] -= f * b[c];
        }
    }
    let mut x = vec![0.0; n];
    for c in (0..n).rev() {
        let s: f64 = (c + 1..n).map(|k| a[c][k] * x[k]).sum();
        x[c] = (b[c] - s) / a[c][c];
    }
    x
}

fn db(x: f64) -> f64 {
    10.0 * x.max(1e-20).log10()
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 3 {
        eprintln!("usage: dreist-stemfit <reference.wav> <window-seconds> <stem.wav>...");
        return ExitCode::FAILURE;
    }
    let Some(r) = load(&args[0]) else { return ExitCode::FAILURE };
    let win: f64 = args[1].parse().unwrap_or(4.0);
    let stems: Vec<_> = match args[2..].iter().map(|p| load(p)).collect::<Option<Vec<_>>>() {
        Some(s) => s,
        None => return ExitCode::FAILURE,
    };
    let n = stems.len();
    let len = r.0.len();
    let w = (win * 44100.0) as usize;
    let at = |v: &[f32], i: usize| v.get(i).copied().unwrap_or(0.0) as f64;
    print!("  t(s)  null  fit |");
    for k in 0..n {
        print!(" s{k:<2} gain   dB |");
    }
    println!();
    for start in (0..len).step_by(w) {
        let end = (start + w).min(len);
        let mut a = vec![vec![0.0f64; n]; n];
        let mut b = vec![0.0f64; n];
        let mut rr = 0.0;
        let mut sum_e = 0.0;
        for i in start..end {
            for ch in 0..2 {
                let y = if ch == 0 { at(&r.0, i) } else { at(&r.1, i) };
                let xs: Vec<f64> = stems.iter().map(|s| if ch == 0 { at(&s.0, i) } else { at(&s.1, i) }).collect();
                rr += y * y;
                let tot: f64 = xs.iter().sum();
                sum_e += (tot - y) * (tot - y);
                for p in 0..n {
                    b[p] += xs[p] * y;
                    for q in 0..n {
                        a[p][q] += xs[p] * xs[q];
                    }
                }
            }
        }
        let x = solve(a.clone(), b.clone());
        // Residual after fit: rr - 2 x·b + x·A·x.
        let xb: f64 = x.iter().zip(&b).map(|(x, b)| x * b).sum();
        let xax: f64 = (0..n).map(|p| (0..n).map(|q| x[p] * a[p][q] * x[q]).sum::<f64>()).sum();
        let res = (rr - 2.0 * xb + xax).max(0.0);
        print!("{:6.1} {:5.1} {:5.1} |", start as f64 / 44100.0, db(sum_e / rr.max(1e-20)), db(res / rr.max(1e-20)));
        let cnt = (2 * (end - start)) as f64;
        for k in 0..n {
            if a[k][k] / cnt < 1e-9 {
                print!("    -       - |");
            } else {
                print!(" {:6.2} {:6.1} |", x[k], db(a[k][k] / cnt));
            }
        }
        println!();
    }
    ExitCode::SUCCESS
}
