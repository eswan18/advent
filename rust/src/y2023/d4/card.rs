use std::{collections::HashSet, num::ParseIntError};

pub struct Card {
    winning_numbers: HashSet<u32>,
    your_numbers: HashSet<u32>,
}

impl Card {
    pub fn new_from_line(line: &str) -> Result<Card, Box<dyn std::error::Error>> {
        let numbers = line.split(": ").last().ok_or("No numbers")?;
        let number_parts: Vec<&str> = numbers.split(" | ").collect();
        let winning_numbers = number_parts[0]
            .split(' ')
            .filter(|n| n.len() > 0)
            .map(|n| n.parse::<u32>())
            .collect::<Result<HashSet<u32>, ParseIntError>>()?;
        let your_numbers = number_parts[1]
            .split(' ')
            .filter(|n| n.len() > 0)
            .map(|n| n.parse::<u32>())
            .collect::<Result<HashSet<u32>, ParseIntError>>()?;
        Ok(Card {
            winning_numbers,
            your_numbers,
        })
    }

    pub fn new_from_input(input: &str) -> Result<Vec<Card>, Box<dyn std::error::Error>> {
        input
            .lines()
            .map(|line| Card::new_from_line(line))
            .collect()
    }

    pub fn match_count(&self) -> usize {
        self.winning_numbers
            .intersection(&self.your_numbers)
            .count()
    }

    pub fn points(&self) -> usize {
        let match_count = self.match_count();
        if match_count >= 1 {
            let base: u32 = 2;
            let exponent = (match_count - 1) as u32;
            return base.pow(exponent) as usize;
        }
        0
    }
}
