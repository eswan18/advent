use super::draw::Draw;
use super::game::Game;


const TEST_DRAW: Draw = Draw { red: 12, green: 13, blue: 14 };

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let games = contents.lines().map(|line| Game::new_from_line(line)).collect::<Vec<Game>>();
    // Filter down to games that have are possible from "test_draw"
    let possible_games = games.iter().filter(|game| game.possible_from_draw(&TEST_DRAW)).collect::<Vec<&Game>>();

    let id_sum = possible_games.iter().map(|game| game.id).sum::<u32>();
    Ok(id_sum.to_string())
}