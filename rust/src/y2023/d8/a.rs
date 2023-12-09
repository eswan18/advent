use super::map::Map;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let map = Map::new_from_text(contents)?;
    let steps = map.traverse()?;
    Ok(steps.to_string())
}