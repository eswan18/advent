use crate::y2023::d11::universe::Universe;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let universe = Universe::new_from_str(contents);
    let expanded_universe = universe.expand(1_000_000);
    let pair_distances = expanded_universe.pair_distances();
    Ok(pair_distances.iter().sum::<usize>().to_string())
}
