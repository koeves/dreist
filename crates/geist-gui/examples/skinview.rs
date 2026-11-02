//! Open the root skin in a window: `cargo run -p geist-gui --features window --example skinview [theme]`.

use geist_gui::{Skin, app::App};

fn main() {
    let theme = std::env::args().nth(1).unwrap_or_else(|| geist_gui::skin::DEFAULT_THEME.into());
    let mut skin = Skin::load(&Skin::resources_dir(), &theme).expect("skin");
    let root = skin.load_skin("RootSkin.skin").expect("root skin");
    let app = App::new(skin, root);
    geist_gui::window::open_blocking(
        geist_gui::window::Hooked(
            app,
            Box::new(|_, e| {
                if let Some(e) = e {
                    println!("{e:?}")
                }
            }),
        ),
        "Skin viewer",
    );
}
