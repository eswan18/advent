use super::card::Card;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let cards = Card::new_from_input(contents)?;
    let sum: usize = cards.iter().map(|c| c.points()).sum();
    Ok(sum.to_string())
}
