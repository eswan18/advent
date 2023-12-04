use super::card::Card;

struct CardAndCopies<'a> {
    card: &'a Card,
    copies: usize,
}

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let cards = Card::new_from_input(contents)?;
    let mut cards_and_copies: Vec<CardAndCopies> = cards.iter().map(|card| CardAndCopies{card, copies: 1}).collect();
    let mut processed_count = 0;
    while cards_and_copies.len() > 0 {
        // Pop off the first item.
        let card_and_copies = cards_and_copies.remove(0);
        processed_count += card_and_copies.copies;
        let match_count = card_and_copies.card.match_count();
        // iterate over the next "match_count" items in cards_and copies
        for c_and_cs in cards_and_copies.iter_mut().take(match_count) {
            c_and_cs.copies += card_and_copies.copies;
        }
    }
    Ok(processed_count.to_string())
}
