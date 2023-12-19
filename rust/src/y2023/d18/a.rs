use crate::y2023::d18::instruction::{InstructionMode, Instruction};
use crate::y2023::d18::path::Path;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let instructions = contents
        .lines()
        .map(|line| Instruction::from_line(line, InstructionMode::Naive))
        .collect::<Option<Vec<Instruction>>>()
        .ok_or("Invalid input")?;
    let mut path = Path::new();
    path.execute_all(instructions);
    let area = path.calculate_area();
    Ok(area.to_string())
}