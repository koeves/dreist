//! The standalone app's side of the audio / MIDI settings panels
//! (`dreist_editor::devices`): audio devices and MIDI ports through
//! `dreist_host` (cpal, midir), an audio restart that relaunches the app with the
//! current document (nih-plug opens its devices once, at start-up), and
//! Sync to clock ([`clock`]).

use dreist_editor::devices::{AudioSetup, DeviceHost, MidiSetup};

/// Environment variable naming a session file (`Session` as JSON) the
/// relaunched app starts from.
pub const SESSION_ENV: &str = "DREIST_SESSION_FILE";

pub struct Host;

impl DeviceHost for Host {
    fn audio(&self, output: &str, input: &str) -> AudioSetup {
        dreist_host::audio::setup(output, input)
    }

    fn midi(&self) -> MidiSetup {
        dreist_host::midi::setup("Dreist")
    }

    fn clock_sync(&self, port: &str, on: bool) {
        clock::set(port, on);
    }

    fn restart(&self, doc: &dreist_formats::Node, samples: Option<&std::path::Path>) {
        let session = crate::Session { doc: doc.to_xml(), samples: samples.map(|p| p.to_string_lossy().into_owned()) };
        dreist_host::session::relaunch(SESSION_ENV, "dreist-session", &session);
    }
}

/// The session a relaunch handed over (read once, then removed).
pub fn take_session() -> Option<crate::Session> {
    dreist_host::session::take(SESSION_ENV)
}

/// Sync to clock: the enabled MIDI input's clock, read through a MIDI
/// input connection of its own (nih-plug passes no clock messages). The audio
/// thread follows it with [`ClockFollow`].
pub mod clock {
    use std::sync::Mutex;
    use std::sync::atomic::{AtomicBool, AtomicU64, Ordering::Relaxed};

    /// Clock ticks per beat.
    const PPQN: f64 = 24.0;
    /// Tick intervals averaged for the tempo.
    const AVERAGE: usize = 24;

    /// What the clock says, shared with the audio thread.
    pub struct Clock {
        active: AtomicBool,
        running: AtomicBool,
        /// Ticks since the song start (song position pointer included).
        ticks: AtomicU64,
        /// Tempo in BPM (`f64` bits; 0 until measured).
        tempo: AtomicU64,
        /// When the last tick came (nanoseconds since [`epoch`]).
        last_tick: AtomicU64,
    }

    pub static CLOCK: Clock = Clock { active: AtomicBool::new(false), running: AtomicBool::new(false), ticks: AtomicU64::new(0), tempo: AtomicU64::new(0), last_tick: AtomicU64::new(0) };

    static CONNECTION: Mutex<Option<dreist_host::midi::InputConnection>> = Mutex::new(None);

    fn epoch() -> std::time::Instant {
        static E: std::sync::OnceLock<std::time::Instant> = std::sync::OnceLock::new();
        *E.get_or_init(std::time::Instant::now)
    }

    fn now_ns() -> u64 {
        epoch().elapsed().as_nanos() as u64
    }

    /// Tick timing for the tempo (midir timestamps, microseconds).
    #[derive(Default)]
    pub struct Parser {
        last: Option<u64>,
        intervals: std::collections::VecDeque<u64>,
    }

    impl Parser {
        /// One MIDI message at `stamp` µs.
        pub fn message(&mut self, clock: &Clock, stamp: u64, m: &[u8]) {
            match m.first() {
                Some(0xf8) => {
                    if let Some(prev) = self.last.filter(|p| stamp > *p) {
                        self.intervals.push_back(stamp - prev);
                        if self.intervals.len() > AVERAGE {
                            self.intervals.pop_front();
                        }
                        let avg = self.intervals.iter().sum::<u64>() as f64 / self.intervals.len() as f64;
                        if avg > 0.0 {
                            clock.tempo.store((60e6 / (avg * PPQN)).to_bits(), Relaxed);
                        }
                    }
                    self.last = Some(stamp);
                    if clock.running.load(Relaxed) {
                        clock.ticks.fetch_add(1, Relaxed);
                        clock.last_tick.store(now_ns(), Relaxed);
                    }
                }
                Some(0xfa) => {
                    clock.ticks.store(0, Relaxed);
                    clock.last_tick.store(now_ns(), Relaxed);
                    clock.running.store(true, Relaxed);
                }
                Some(0xfb) => {
                    clock.last_tick.store(now_ns(), Relaxed);
                    clock.running.store(true, Relaxed);
                }
                Some(0xfc) => clock.running.store(false, Relaxed),
                // Song position pointer: sixteenths (6 ticks each).
                Some(0xf2) if m.len() >= 3 => {
                    let pos = (m[1] as u64 & 0x7f) | ((m[2] as u64 & 0x7f) << 7);
                    clock.ticks.store(pos * 6, Relaxed);
                    clock.last_tick.store(now_ns(), Relaxed);
                }
                _ => {}
            }
        }
    }

    impl Clock {
        /// (running, tempo, position in beats) while following a clock
        /// that has a tempo.
        pub fn transport(&self) -> Option<(bool, f64, f64)> {
            if !self.active.load(Relaxed) {
                return None;
            }
            let tempo = f64::from_bits(self.tempo.load(Relaxed));
            if tempo <= 0.0 {
                return None;
            }
            let running = self.running.load(Relaxed);
            // Between ticks: at most one tick further at the tempo.
            let since = now_ns().saturating_sub(self.last_tick.load(Relaxed)) as f64 * 1e-9;
            let frac = if running { (since * tempo / 60.0 * PPQN).min(1.0) } else { 0.0 };
            Some((running, tempo, (self.ticks.load(Relaxed) as f64 + frac) / PPQN))
        }
    }

    /// Follow the clock of MIDI input `port` (`on`), or stop following.
    pub fn set(port: &str, on: bool) {
        let mut conn = CONNECTION.lock().unwrap_or_else(std::sync::PoisonError::into_inner);
        if let Some(c) = conn.take() {
            c.close();
        }
        CLOCK.active.store(false, Relaxed);
        CLOCK.running.store(false, Relaxed);
        CLOCK.tempo.store(0, Relaxed);
        if !on || port.is_empty() {
            return;
        }
        let mut parser = Parser::default();
        if let Some(c) = dreist_host::midi::connect_input("Dreist clock", "Dreist clock", port, move |stamp, m| parser.message(&CLOCK, stamp, m)) {
            *conn = Some(c);
            CLOCK.active.store(true, Relaxed);
        }
    }

    /// The audio thread's side: the engine slaved to the clock as to a
    /// host, re-located when it drifts a little from the clock.
    #[derive(Default)]
    pub struct ClockFollow {
        /// Where the engine should be by its own count (beats).
        pos: Option<f64>,
    }

    /// Drift (beats) that re-locates the engine.
    const DRIFT: f64 = 0.02;

    impl ClockFollow {
        /// The transport for a block of `frames` at `sr`: (playing, tempo,
        /// a position when the engine must jump there).
        pub fn block(&mut self, frames: usize, sr: f64) -> Option<(bool, f64, Option<f64>)> {
            let Some((running, tempo, at)) = CLOCK.transport() else {
                self.pos = None;
                return None;
            };
            if !running {
                self.pos = None;
                return Some((false, tempo, Some(at)));
            }
            let jump = match self.pos {
                Some(p) if (p - at).abs() <= DRIFT => None,
                _ => Some(at),
            };
            let start = jump.unwrap_or_else(|| self.pos.unwrap_or(at));
            self.pos = Some(start + frames as f64 / sr.max(1.0) * tempo / 60.0);
            Some((true, tempo, jump))
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn clock_messages_set_tempo_position_and_run_state() {
            let c = Clock { active: AtomicBool::new(true), running: AtomicBool::new(false), ticks: AtomicU64::new(0), tempo: AtomicU64::new(0), last_tick: AtomicU64::new(0) };
            let mut p = Parser::default();
            // 120 BPM: a tick every 20.833 ms.
            let tick = 20_833;
            p.message(&c, 0, &[0xf2, 16, 0]);
            assert_eq!(c.ticks.load(Relaxed), 96, "song position: 16 sixteenths");
            p.message(&c, 0, &[0xfb]);
            for i in 1..=48u64 {
                p.message(&c, i * tick, &[0xf8]);
            }
            let (running, tempo, pos) = c.transport().unwrap();
            assert!(running);
            assert!((tempo - 120.0).abs() < 0.1, "{tempo}");
            assert!((pos - 6.0).abs() < 0.05, "{pos}");
            p.message(&c, 49 * tick, &[0xfc]);
            assert!(!c.transport().unwrap().0);
            p.message(&c, 50 * tick, &[0xfa]);
            assert_eq!(c.ticks.load(Relaxed), 0, "start: from the top");
        }
    }
}
