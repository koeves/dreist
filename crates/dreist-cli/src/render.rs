//! `dreist-render <file.geist> <out.wav> [seconds] [--sr N] [--block N] [--no-aux] [--multi-out] [--idle S]`:
//! render a project offline from the start (song length when the song is
//! active, else `seconds`, default 8) to a 32-bit float stereo WAV.
//! `--multi-out` also writes each non-silent "Sub output k" to `<out>.subk.wav`.
//! `--idle S` first runs S seconds with the transport stopped, as a host does
//! before playback (free-running modulators keep their state).

use std::path::Path;
use std::process::ExitCode;

use dreist_engine::{Dreist, RenderOptions, SUB_OUTPUTS, render_multi, write_wav};

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut pos = Vec::new();
    let mut sr = 44100u32;
    let mut block = 512usize;
    let mut options = RenderOptions::default();
    let mut multi = false;
    let mut idle = 0.0f64;
    let mut it = args.iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "--sr" => sr = it.next().and_then(|v| v.parse().ok()).unwrap_or(sr),
            "--block" => block = it.next().and_then(|v| v.parse().ok()).unwrap_or(block),
            "--no-aux" => options.aux_returns = false,
            "--multi-out" => multi = true,
            "--idle" => idle = it.next().and_then(|v| v.parse().ok()).unwrap_or(idle),
            _ => pos.push(a.clone()),
        }
    }
    if pos.len() < 2 {
        eprintln!("usage: dreist-render <file.geist> <out.wav> [seconds] [--sr N] [--block N] [--no-aux] [--multi-out]");
        return ExitCode::FAILURE;
    }
    let mut g = match Dreist::load(Path::new(&pos[0]), sr as f32, options) {
        Ok(g) => g,
        Err(e) => {
            eprintln!("{}: {e}", pos[0]);
            return ExitCode::FAILURE;
        }
    };
    for m in &g.missing_samples {
        eprintln!("missing sample: {m}");
    }
    let seconds: f64 = pos.get(2).and_then(|s| s.parse().ok()).unwrap_or(8.0);
    let frames = match (pos.get(2), g.song_length_samples()) {
        (None, Some(n)) => n as usize + sr as usize * 2,
        _ => (seconds * sr as f64) as usize,
    };
    println!("tempo {} BPM, song {}, rendering {:.2} s", g.tempo(), if g.song_active() { "on" } else { "off" }, frames as f64 / sr as f64);
    if idle > 0.0 {
        let (mut l, mut r) = (vec![0.0f32; block], vec![0.0f32; block]);
        for _ in 0..((idle * sr as f64) as usize).div_ceil(block) {
            g.process(&mut l, &mut r);
            l.fill(0.0);
            r.fill(0.0);
        }
    }
    let t = std::time::Instant::now();
    let (l, r, subs) = render_multi(&mut g, frames, block, if multi { SUB_OUTPUTS } else { 0 });
    let peak = l.iter().chain(&r).fold(0.0f32, |a, b| a.max(b.abs()));
    println!("rendered in {:.2} s, peak {:.3} ({:.1} dBFS)", t.elapsed().as_secs_f64(), peak, 20.0 * peak.max(1e-9).log10());
    if let Err(e) = write_wav(Path::new(&pos[1]), sr, &l, &r) {
        eprintln!("{}: {e}", pos[1]);
        return ExitCode::FAILURE;
    }
    for (k, [sl, sr_]) in subs.iter().enumerate() {
        if sl.iter().chain(sr_).all(|x| *x == 0.0) {
            continue;
        }
        let path = Path::new(&pos[1]).with_extension(format!("sub{}.wav", k + 1));
        if let Err(e) = write_wav(&path, sr, sl, sr_) {
            eprintln!("{}: {e}", path.display());
            return ExitCode::FAILURE;
        }
        println!("sub output {} -> {}", k + 1, path.display());
    }
    ExitCode::SUCCESS
}
