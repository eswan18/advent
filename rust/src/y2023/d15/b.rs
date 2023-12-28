use crate::y2023::d15::lens_box::{Instruction, LensBoxContainer};

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let parts = contents.trim().split(",").collect::<Vec<_>>();
    let instructions = parts
        .iter()
        .map(|p| Instruction::new_from_str(p))
        .collect::<Result<Vec<_>, _>>()?;
    let mut lens_box_container = LensBoxContainer::new();
    instructions
        .iter()
        .for_each(|i| lens_box_container.execute(i));
    Ok(lens_box_container.focal_power().to_string())
}
