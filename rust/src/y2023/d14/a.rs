use crate::y2023::d14::platform::{Platform, Direction};


pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut platform = Platform::new_from_str(contents);
    platform.tilt(Direction::North);
    Ok(platform.load().to_string())
}