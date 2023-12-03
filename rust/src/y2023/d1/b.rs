use std::collections::HashMap;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut sum = 0;
    let lines = contents.lines();
    for line in lines {
        let mut first_num: Option<u32> = None;
        let mut last_num: Option<u32> = None;
        // a c-style i loop
        for i in 0..line.len() {
            let char = line.chars().nth(i).unwrap();
            // If it's a digit, parsing is straightforward.
            match char.to_digit(10) {
                Some(num) => {
                    if first_num.is_none() {
                        first_num = Some(num);
                    }
                    last_num = Some(num);
                }
                None => {}
            }
            match find_num_word(&line[i..]) {
                Some(num) => {
                    if first_num.is_none() {
                        first_num = Some(num as u32);
                    }
                    last_num = Some(num as u32);
                }
                None => {}
            }
        }
        match (first_num, last_num) {
            (Some(first), Some(last)) => sum += 10 * first + last,
            _ => return Err("Invalid line - missing a digit".into()),
        }
    }
    Ok(sum.to_string())
}

fn find_num_word(line: &str) -> Option<i32> {
    let map = word_to_num_map();
    // if the line starts with a word in the map, return it
    for (word, val) in map.iter() {
        if line.starts_with(word) {
            return Some(*val);
        }
    }
    None
}

fn word_to_num_map() -> HashMap<&'static str, i32> {
    HashMap::from([
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
        ("zero", 0),
    ])
}
