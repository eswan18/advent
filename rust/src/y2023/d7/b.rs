use super::hand::Hand;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let hands = contents
        .lines()
        .map(|line| Hand::new_from_line(line, true))
        .collect::<Result<Vec<Hand>, _>>()?;
    // sort the hands with a custom sorting function
    let mut hands = hands;
    hands.sort_by(|a, b| {
        let a_score = a.type_score();
        let b_score = b.type_score();

        if a_score > b_score {
            return std::cmp::Ordering::Greater;
        }
        if a_score < b_score {
            return std::cmp::Ordering::Less;
        }
        if a.wins_ties_over(b) {
            return std::cmp::Ordering::Greater;
        }
        return std::cmp::Ordering::Less;
    });
    let mut winnings = 0;
    for (i, hand) in hands.iter().enumerate() {
        let hand_score = hand.bid * (i as u32 + 1);
        winnings += hand_score;
    }
    Ok(winnings.to_string())
}
