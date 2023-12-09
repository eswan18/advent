use super::history::History;


pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let histories = contents.lines().map(|l| History::new_from_line(l)).collect::<Result<Vec<_>, _>>()?;
    let prev_values = histories.iter().map(|h| h.find_previous()).collect::<Result<Vec<_>, _>>()?;
    let prev_sum = prev_values.iter().sum::<i32>();
    Ok(prev_sum.to_string())
}