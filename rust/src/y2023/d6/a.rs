use super::race::Race;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let races = Race::new_vec_from_lines(contents.lines());
    let ways_to_win = races.iter().map(|r| r.ways_to_win());
    let product = ways_to_win.fold(1, |acc, x| acc * x);
    Ok(product.to_string())
}
