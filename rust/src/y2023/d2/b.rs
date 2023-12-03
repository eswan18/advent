use super::game::Game;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let games = contents
        .lines()
        .map(|line| Game::new_from_line(line))
        .collect::<Vec<Game>>();
    let powers: Vec<i32> = games
        .iter()
        .map(|game| game.power_of_minimal_draw())
        .collect();

    // Filter down to games that have are possible from "test_draw"
    Ok(powers.iter().sum::<i32>().to_string())
}
