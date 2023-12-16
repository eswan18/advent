use std::collections::HashMap;

use crate::y2023::d14::platform::Platform;

const N: usize = 1000000000;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut platform = Platform::new_from_str(contents);
    // Keep track of which cycles have which hash values, so we know when we've hit a cycle.
    let mut hash_cycle_map = HashMap::new();
    let mut i: usize = 0;
    let cycle_length: usize;
    loop {
        platform.cycle();
        i += 1;
        let hash = platform.rounded_rock_hash();
        if hash_cycle_map.contains_key(&hash) {
            let cycle_start = hash_cycle_map[&hash];
            cycle_length = i - cycle_start;
            break;
        }
        hash_cycle_map.insert(hash, i);
    }
    println!("Found a cycle at {} with length {}", i, cycle_length);
    let cycles_remaining = N - i;
    let cycles_needed = cycles_remaining % cycle_length as usize;
    for _ in 0..cycles_needed {
        platform.cycle();
    }
    Ok(platform.load().to_string())
}