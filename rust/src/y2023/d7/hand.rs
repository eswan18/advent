use std::iter;
use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
enum Card {
    A,
    K,
    Q,
    J,
    T,
    Value(u8), // 2-9
}

impl fmt::Display for Card {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let card: String = match self {
            Card::A => "A".to_string(),
            Card::K => "K".to_string(),
            Card::Q => "Q".to_string(),
            Card::J => "J".to_string(),
            Card::T => "T".to_string(),
            Card::Value(v) => v.to_string(),
        };
        write!(f, "{}", card)
    }
}

impl Card {
    pub fn value(&self, jokers_wild: bool) -> u8 {
        match self {
            Card::A => 14,
            Card::K => 13,
            Card::Q => 12,
            Card::J => if jokers_wild { 1 } else { 11 },
            Card::T => 10,
            Card::Value(v) => *v,
        }
    }

    pub fn new_from_char(c: &char) -> Result<Card, Box<dyn std::error::Error>> {
        let card = match c {
            'A' => Card::A,
            'K' => Card::K,
            'Q' => Card::Q,
            'J' => Card::J,
            'T' => Card::T,
            '2' => Card::Value(2),
            '3' => Card::Value(3),
            '4' => Card::Value(4),
            '5' => Card::Value(5),
            '6' => Card::Value(6),
            '7' => Card::Value(7),
            '8' => Card::Value(8),
            '9' => Card::Value(9),
            _ => return Err(format!("Invalid card: {}", c).into()),
        };
        return Ok(card);
    }
}

pub struct Hand {
    cards: Vec<Card>,
    pub bid: u32,
    jokers_wild: bool,
}

impl Hand {
    pub fn new_from_line(line: &str, jokers_wild: bool) -> Result<Self, Box<dyn std::error::Error>> {
        let parts: Vec<&str> = line.split(" ").collect();
        if parts.len() != 2 {
            return Err(format!("Invalid line: {}", line).into());
        }
        let cards = parts[0].chars().map(|c| Card::new_from_char(&c)).collect::<Result<Vec<Card>, _>>()?;
        let bid = parts[1].parse::<u32>()?;
        Ok(Hand { cards, bid, jokers_wild })
    }

    pub fn wins_ties_over(&self, other: &Self) -> bool {
        for (card, other_card) in iter::zip(&self.cards, &other.cards) {
            let self_value = card.value(self.jokers_wild);
            let other_value = other_card.value(other.jokers_wild);
            if self_value > other_value {
                return true;
            }
            if self_value < other_value {
                return false;
            }
        }
        panic!("tie!!")
    }

    pub fn type_score(&self) -> u32 {
        // Group self.hand cards by value
        let mut card_counts = HashMap::new();
        let mut cards = self.cards.clone();
        let mut joker_count  = 0;
        if self.jokers_wild {
            joker_count = cards.iter().filter(|card| **card == Card::J).count();
            cards = cards.into_iter().filter(|card| *card != Card::J).collect();
            // The strange case where we have only jokers: return the score for five-of-a-kind.
            if cards.len() == 0 {
                return 7;
            }
        }

        for card in &self.cards {
            let card_value = card.value(self.jokers_wild);
            if let Some(count) = card_counts.get_mut(&card_value) {
                *count += 1;
            } else {
                card_counts.insert(card_value, 1);
            }
        }
        let mut counts = card_counts.into_values().collect::<Vec<u32>>();
        counts.sort();
        counts.reverse();

        // If there were jokers, add them to the largest count.
        if joker_count > 0 {
            counts[0] += joker_count as u32;
        }

        // Calculate the score.
        if counts[0] == 5 {
            // five of a kind
            return 7;
        }
        if counts[0] == 4 {
            // four of a kind
            return 6;
        }
        if counts[0] == 3 {
            if counts[1] == 2 {
                // full house
                return 5;
            } else {
                // three of a kind
                return 4;
            }
        }
        if counts[0] == 2 {
            if counts[1] == 2 {
                // two pair
                return 3;
            } else {
                // one pair
                return 2;
            }
        }
        // high card
        return 1;
    }
}

impl fmt::Display for Hand {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let cards = self.cards.iter().map(|card| match card {
            Card::A => String::from("A"),
            Card::K => String::from("K"),
            Card::Q => String::from("Q"),
            Card::J => String::from("J"),
            Card::T => String::from("T"),
            Card::Value(v) => format!("{}", v)
        }).collect::<Vec<String>>().join("");
        write!(f, "{} {}", cards, self.bid)
    }
}
