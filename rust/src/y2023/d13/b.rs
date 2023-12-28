use crate::y2023::d13::pattern::Pattern;

const MISMATCHES: usize = 1;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let patterns = contents
        .split("\n\n")
        .map(Pattern::new_from_str)
        .collect::<Vec<_>>();
    let scores: Vec<usize> = patterns
        .iter()
        .map(|p| p.find_reflect_score(MISMATCHES))
        .collect::<Result<Vec<usize>, _>>()?;
    let score_sum: usize = scores.iter().sum();
    Ok(score_sum.to_string())
}
