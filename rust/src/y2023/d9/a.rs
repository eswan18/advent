use super::history::History;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let histories = contents
        .lines()
        .map(|l| History::new_from_line(l))
        .collect::<Result<Vec<_>, _>>()?;
    let next_values = histories
        .iter()
        .map(|h| h.find_next())
        .collect::<Result<Vec<_>, _>>()?;
    let next_sum = next_values.iter().sum::<i32>();
    Ok(next_sum.to_string())
}
