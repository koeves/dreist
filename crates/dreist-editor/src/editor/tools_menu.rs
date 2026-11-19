//! The Tools and Help menus.

use crate::*;

/// Options key: the CPU and memory readout is on (off by default).
pub(crate) const PERF_OPTION: &str = "ShowPerformance";

/// Options key: hold the performance power profile while the standalone
/// plays (Linux; on by default).
pub(crate) const POWER_OPTION: &str = "HoldPerformanceWhilePlaying";

impl Editor {
    /// The power-profile hold is offered: the Linux standalone.
    fn power_hold_offered(&self) -> bool {
        cfg!(target_os = "linux") && self.devices.host.is_some()
    }

    /// Its menu item, checked while on.
    fn power_hold_item(&self) -> String {
        let label = "Keep the CPU at full speed while playing";
        if self.modals.options.bool(POWER_OPTION, true) { format!("{}{label}", dreist_gui::menu::CHECK) } else { label.into() }
    }

    fn toggle_power_hold(&mut self) {
        let on = !self.modals.options.bool(POWER_OPTION, true);
        self.modals.options.set(POWER_OPTION, on);
        if !cfg!(test) {
            self.modals.options.save();
        }
        if let Some(h) = &self.devices.host {
            h.power_hold(on);
        }
    }

    /// The diagnostics export (`dreist_engine::diag::export`): the log's
    /// report with the settings, to a file shown in the file manager or to
    /// the clipboard. Paths outside the settings and log folders are left
    /// out.
    pub(crate) fn diagnostics(&self, copy: bool) {
        let settings: Vec<(String, String)> = self.modals.options.entries().map(|(k, v)| (k.to_string(), v.to_string())).collect();
        let keep: Vec<std::path::PathBuf> = options::settings_dir().into_iter().collect();
        if cfg!(test) {
            return;
        }
        if copy {
            dreist_host::shell::copy_text(&dreist_engine::diag::report(&settings, &keep));
        } else if let Ok(p) = dreist_engine::diag::export(&settings, &keep) {
            dreist_host::shell::reveal(&[&p]);
        }
    }

    /// The CPU and memory readout is on.
    pub fn perf_shown(&self) -> bool {
        self.modals.options.bool(PERF_OPTION, false)
    }

    /// Show `r` in the readout, adding or removing it to match the option
    /// (the app calls this about once a second).
    pub fn performance(&mut self, r: &dreist_gui::perf::Reading) {
        self.place_perf();
        if self.perf_shown() {
            dreist_gui::perf::update(&mut self.app, r);
        }
    }

    /// Add or remove the readout to match the option, in a strip taken
    /// from the bottom of the browser's list area (kept every frame through
    /// splitters and window sizes); hidden while that area is not shown.
    pub fn place_perf(&mut self) {
        let on = self.perf_shown();
        let list = self.browser.as_ref().map(|b| b.page().to_vec()).and_then(|page| Some([&page[..], &self.app.ctrl(&page)?.path_of("SplitView")?[..]].concat()));
        let strip = list.and_then(|p| dreist_gui::perf::reserve_below(&mut self.app, &p, on));
        dreist_gui::perf::show(&mut self.app, on);
        if on {
            dreist_gui::perf::place(&mut self.app, strip.unwrap_or_default());
        }
    }

    /// Tools ([re:4139f8] [re:a00968]) and Help ([re:0316e2])
    /// menus.
    pub(crate) fn tools_help_menu(&mut self, ev: &UiEvent) -> bool {
        let reset = format!("Reset {}", crate::product());
        // [re:4139f8]: the last item is the check for option
        // `SaveSamplesWithChunks`.
        let embed = if project::embed_samples() { format!("{}Save samples with presets", dreist_gui::menu::CHECK) } else { "Save samples with presets".into() };
        let tools: [&str; 11] = ["Preferences", "", &reset, "Save as default preset", "Clear default preset", "", "Find missing files...", "", "Export as audio...", "", &embed];
        let perf = if self.perf_shown() { "Hide CPU and memory" } else { "Show CPU and memory" };
        let power = self.power_hold_item();
        let mut help: Vec<&str> = vec!["About", "", "Reset UI size to default", "Reset UI scale to 100%", "Show MIDI Console", perf, "", "Export diagnostics...", "Copy diagnostics"];
        if self.power_hold_offered() {
            help.push(&power);
        }
        match ev {
            UiEvent::Clicked { path, name, .. } if (name == "ToolButton" || name == "HelpButton") && !self.browser.as_ref().is_some_and(|b| path.starts_with(b.page())) => {
                let items = if name == "ToolButton" { &tools[..] } else { &help[..] };
                self.app.open_menu(path, items.iter().map(|s| s.to_string()).collect(), None);
                false
            }
            UiEvent::MenuSelected { anchor, name, index } if name == "ToolButton" && !self.browser.as_ref().is_some_and(|b| anchor.starts_with(b.page())) => {
                let default = options::default_preset();
                match *index {
                    0 => self.modals.show(&mut self.app, modal::Kind::Preferences),
                    // Reset: the default preset if saved, else a new document.
                    2 => {
                        let loaded = default.as_ref().filter(|p| p.is_file()).and_then(|p| crate::app::read_project(p).map(|(raw, _)| (raw, p.clone())));
                        self.project_path = None;
                        match loaded {
                            Some((raw, p)) => self.open_document(raw, Some(dreist_formats::model::samples_dir(&p)), None),
                            None => self.open_document(project::new_document(), None, None),
                        }
                        self.outbox.push(self.model.rebuild_command());
                    }
                    3 => {
                        if let Some(p) = default {
                            if let Some(d) = p.parent() {
                                let _ = std::fs::create_dir_all(d);
                            }
                            let _ = project::save(&self.model.doc, self.model.samples.as_deref(), &p, project::embed_samples());
                        }
                    }
                    4 => {
                        if let Some(p) = default {
                            let _ = std::fs::remove_file(&p);
                            let _ = std::fs::remove_dir_all(dreist_formats::model::samples_dir(&p));
                        }
                    }
                    // [re:af38f1].
                    6 => self.filefind.show(filefind::missing_files(&self.model)),
                    // [re:c7a8f1].
                    8 => self.modals.show(&mut self.app, modal::Kind::Export),
                    10 => {
                        let mut o = options::Options::load();
                        o.set("SaveSamplesWithChunks", !project::embed_samples());
                        o.save();
                    }
                    _ => {}
                }
                true
            }
            UiEvent::MenuSelected { name, index, .. } if name == "HelpButton" => {
                match *index {
                    0 => self.modals.show(&mut self.app, modal::Kind::About),
                    // [re:4139f8]: the host resizes
                    // to the default window size.
                    2 => {
                        let (w, h) = self.window_size.0;
                        self.app.resize(w, h);
                        self.app.resize_request = true;
                    }
                    // Lambda #8: scale 1 (when not already), the window at
                    // the root's size; LastEditorScaleFactor 100,
                    // LastEditorSize = that size.
                    3 => {
                        if (self.app.ui_scale - 1.0).abs() > 1e-6 {
                            self.modals.options.set("LastEditorScaleFactor", 100);
                            let (w, h) = self.app.size();
                            self.modals.options.set("LastEditorSize", format!("{w},{h}"));
                            if !cfg!(test) {
                                self.modals.options.save();
                            }
                            self.window_size.1 = (w, h);
                            self.app.ui_scale = 1.0;
                            self.app.resize_request = true;
                        }
                    }
                    4 => self.midiconsole.open = true,
                    7 => self.diagnostics(false),
                    8 => self.diagnostics(true),
                    9 if self.power_hold_offered() => self.toggle_power_hold(),
                    5 => {
                        let on = !self.perf_shown();
                        self.modals.options.set(PERF_OPTION, on);
                        if !cfg!(test) {
                            self.modals.options.save();
                        }
                        self.place_perf();
                    }
                    _ => {}
                }
                true
            }
            _ => false,
        }
    }
}
