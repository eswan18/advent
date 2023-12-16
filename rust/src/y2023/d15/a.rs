use crate::y2023::d15::hash::hash;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let parts = contents.trim().split(",").collect::<Vec<_>>();
    let total_hash_sum = parts.iter().map(|s| hash(s)).sum::<u32>();
    Ok(total_hash_sum.to_string())
}