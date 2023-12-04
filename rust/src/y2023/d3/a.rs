use super::schematic::Schematic;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let schematic = Schematic::parse(contents)?;
    // numbers that are adjacent to any symbol
    let part_numbers = schematic
        .numbers
        .iter()
        .filter(|num| schematic.symbols.iter().any(|sym| num.adjacent(&sym.coord)));
    let sum: u32 = part_numbers.map(|num| num.value).sum();
    Ok(sum.to_string())
}
