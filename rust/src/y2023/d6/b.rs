use super::race::Race;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let race = Race::new_from_lines(contents.lines());
    let ways_to_win = race.ways_to_win();
    Ok(ways_to_win.to_string())
}
