//! `dreist-inspect <file.geist|file.geistkit>`: summarize a Geist2 file and
//! check that every referenced sample resolves.

use std::path::Path;
use std::process::ExitCode;

use dreist_formats::model::samples_dir;
use dreist_formats::{Kit, Pad, Project};

fn main() -> ExitCode {
    let Some(arg) = std::env::args().nth(1) else {
        eprintln!("usage: dreist-inspect <file.geist|file.geistkit>");
        return ExitCode::FAILURE;
    };
    let path = Path::new(&arg);
    let samples = samples_dir(path);
    let mut missing = 0;
    let result = match path.extension().and_then(|e| e.to_str()) {
        Some("geistkit") => Kit::load(path).map(|kit| {
            println!("kit: {} pads", kit.pads.len());
            missing += print_pads(&kit.pads, &samples, "  ");
        }),
        _ => Project::load(path).map(|p| {
            println!("project v{:?}: tempo {:?}, {} audio files, {} engines", p.version, p.tempo, p.audio_files.len(), p.engines.len());
            for e in &p.engines {
                let patterns = e.patterns.iter().filter(|p| p.tracks.iter().any(|t| t.steps.iter().any(|s| s.on))).count();
                println!("engine {} {:?}: {} pads, {} patterns ({} with steps)", e.index, e.label.as_deref().unwrap_or(""), e.pads.len(), e.patterns.len(), patterns);
                missing += print_pads(&e.pads, &samples, "  ");
            }
        }),
    };
    if let Err(e) = result {
        eprintln!("{arg}: {e}");
        return ExitCode::FAILURE;
    }
    if missing > 0 {
        eprintln!("{missing} sample(s) not found under {}", samples.display());
        return ExitCode::FAILURE;
    }
    ExitCode::SUCCESS
}

fn print_pads(pads: &[Pad], samples: &Path, indent: &str) -> usize {
    let mut missing = 0;
    for pad in pads {
        for l in &pad.layers {
            let file = l.audio_file.as_deref().unwrap_or("-");
            let found = l.audio_file.as_ref().is_some_and(|f| samples.join(f).exists());
            if l.audio_file.is_some() && !found {
                missing += 1;
            }
            println!("{indent}pad {:>3} layer {}: {} {}", pad.index, l.index, file, if found { "" } else { "(missing)" });
        }
    }
    missing
}
