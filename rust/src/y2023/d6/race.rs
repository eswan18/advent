use std::{iter::zip, str::Lines};

pub struct Race {
    time: u64,
    distance: u64,
}

impl Race {
    pub fn new(time: u64, distance: u64) -> Self {
        Self { time, distance }
    }

    pub fn new_vec_from_lines(lines: Lines) -> Vec<Self> {
        let lines: Vec<&str> = lines.collect();
        if lines.len() != 2 {
            panic!("Invalid input: expected 2 lines");
        }
        let time_strs: &str = lines[0].split(":").map(|s| s.trim()).last().unwrap();
        let distance_strs: &str = lines[1].split(":").map(|s| s.trim()).last().unwrap();
        let times: Vec<u64> = time_strs
            .split(' ')
            .filter(|s| !s.is_empty())
            .map(|s| s.parse::<u64>().unwrap())
            .collect();
        let distances: Vec<u64> = distance_strs
            .split(' ')
            .filter(|s| !s.is_empty())
            .map(|s| s.parse::<u64>().unwrap())
            .collect();
        zip(times, distances)
            .map(|(t, d)| Self::new(t, d))
            .collect()
    }

    pub fn new_from_lines(lines: Lines) -> Self {
        let lines: Vec<&str> = lines.collect();
        if lines.len() != 2 {
            panic!("Invalid input: expected 2 lines");
        }
        let time_str = lines[0]
            .split(":")
            .map(|s| s.trim())
            .last()
            .unwrap()
            .replace(" ", "");
        let distance_str = lines[1]
            .split(":")
            .map(|s| s.trim())
            .last()
            .unwrap()
            .replace(" ", "");
        let time = time_str.parse::<u64>().unwrap();
        let distance = distance_str.parse::<u64>().unwrap();
        Self::new(time, distance)
    }

    pub fn ways_to_win(&self) -> u64 {
        let mut ways = 0;
        let mut has_won = false;
        for speed in 0..self.time {
            let remaining_time = self.time - speed;
            let distance = speed * remaining_time;
            if distance > self.distance {
                ways += 1;
                has_won = true;
            } else {
                if has_won {
                    break;
                }
            }
        }
        ways
    }
}
