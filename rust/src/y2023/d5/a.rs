use super::game::Game;
use super::seeds::SeedsType;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let game = Game::new_from_str(contents, SeedsType::List);
    let final_translations = game.final_translations();
    let min_final_translation = final_translations.iter().min().unwrap();
    Ok(min_final_translation.to_string())
}