use super::schematic::Schematic;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let schematic = Schematic::parse(contents)?;
    let stars = schematic.symbols.iter().filter(|sym| sym.symbol == '*');
    let mut running_sum = 0;
    stars.for_each(|star| {
        let mut touching_nums = vec![];
        schematic.numbers.iter().for_each(|num| {
            if num.adjacent(&star.coord) { touching_nums.push(num) }
        });
        if touching_nums.len() == 2 {
            // This means we're at a "gear", so we compute the gear ratio and add it to our running sum.
            let ratio = touching_nums[0].value * touching_nums[1].value;
            running_sum += ratio;
        }
    });
    Ok(running_sum.to_string())
}
