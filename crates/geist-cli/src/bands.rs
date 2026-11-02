//! `geist-bands <reference.wav> <port.wav> [window-seconds]`: compare the
//! spectral envelope of two renders that need not cancel (random
//! modulation, phase-shifted LFOs, reverbs): per window, the energy in ten
//! octave bands (31 Hz .. 16 kHz, band-pass biquads) of each file and the
//! port − reference difference in dB.

use std::path::Path;
use std::process::ExitCode;

use geist_engine::audio;

const CENTRES: [f64; 10] = [31.25, 62.5, 125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0];

/// RBJ band-pass (constant 0 dB peak), Q = √2 (one octave).
struct Bp {
    b: [f64; 3],
    a: [f64; 2],
    z: [f64; 2],
}

impl Bp {
    fn new(fc: f64, sr: f64) -> Bp {
        let w = std::f64::consts::TAU * fc / sr;
        let alpha = w.sin() / (2.0 * std::f64::consts::SQRT_2);
        let a0 = 1.0 + alpha;
        Bp { b: [alpha / a0, 0.0, -alpha / a0], a: [-2.0 * w.cos() / a0, (1.0 - alpha) / a0], z: [0.0; 2] }
    }

    fn run(&mut self, x: f64) -> f64 {
        let y = self.b[0] * x + self.z[0];
        self.z[0] = self.b[1] * x - self.a[0] * y + self.z[1];
        self.z[1] = self.b[2] * x - self.a[1] * y;
        y
    }
}

fn band_energies(path: &str, win: usize) -> Option<(Vec<[f64; 10]>, f32)> {
    let d = match audio::load(Path::new(path)) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("{e}");
            return None;
        }
    };
    let sr = d.sample_rate;
    let right = d.right.as_ref().unwrap_or(&d.left);
    let mut f: Vec<Bp> = CENTRES.iter().map(|&c| Bp::new(c.min(sr as f64 * 0.45), sr as f64)).collect();
    let mut out = Vec::new();
    let mut acc = [0.0f64; 10];
    for i in 0..d.left.len() {
        let x = 0.5 * (d.left[i] as f64 + right[i] as f64);
        for (b, flt) in f.iter_mut().enumerate() {
            let y = flt.run(x);
            acc[b] += y * y;
        }
        if (i + 1) % win == 0 {
            out.push(acc.map(|e| e / win as f64));
            acc = [0.0; 10];
        }
    }
    Some((out, sr))
}

fn db(x: f64) -> f64 {
    10.0 * x.max(1e-20).log10()
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 2 {
        eprintln!("usage: geist-bands <reference.wav> <port.wav> [window-seconds]");
        return ExitCode::FAILURE;
    }
    let secs: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2.0);
    let win = (secs * 44100.0) as usize;
    let (Some((r, _)), Some((p, _))) = (band_energies(&args[0], win), band_energies(&args[1], win)) else {
        return ExitCode::FAILURE;
    };
    print!("  t(s)   ref dB |");
    for c in CENTRES {
        print!(" {:>5}", if c < 1000.0 { format!("{c:.0}") } else { format!("{:.0}k", c / 1000.0) });
    }
    println!("   (port − ref, dB; · = both below −80 dB)");
    let mut tot = ([0.0f64; 10], [0.0f64; 10]);
    for (w, (a, b)) in r.iter().zip(&p).enumerate() {
        let sum: f64 = a.iter().sum();
        print!("{:6.1} {:8.1} |", w as f64 * secs, db(sum));
        for k in 0..10 {
            tot.0[k] += a[k];
            tot.1[k] += b[k];
            if db(a[k]) < -80.0 && db(b[k]) < -80.0 {
                print!("     ·");
            } else {
                print!(" {:+5.1}", db(b[k]) - db(a[k]));
            }
        }
        println!();
    }
    print!(" total          |");
    for k in 0..10 {
        print!(" {:+5.1}", db(tot.1[k]) - db(tot.0[k]));
    }
    println!();
    ExitCode::SUCCESS
}
