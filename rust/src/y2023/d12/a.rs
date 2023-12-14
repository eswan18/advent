use crate::y2023::d12::row::RowReading;


pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let readings = contents.lines().map(|line| RowReading::new_from_line(line)).collect::<Result<Vec<_>, _>>()?;
    let possibilities = readings.iter().map(|reading| reading.possibilities().len()).collect::<Vec<_>>();
    let possibilities_sum: usize = possibilities.iter().sum();
    Ok(possibilities_sum.to_string())
}