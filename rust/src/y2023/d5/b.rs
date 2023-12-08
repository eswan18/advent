use super::game::Game;
use super::seeds::SeedsType;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let game = Game::new_from_str(contents, SeedsType::RangeList);
    let max_final_destination = game.max_final_destination();
    for i in 0..max_final_destination {
        if i % 100_000 == 0 {
            println!("i: {}", i);
        }
        let source = game.back_map(i);
        if game.seeds.contains(source) {
            return Ok(i.to_string());
        }
    }
    Err("No solution found".into())
}