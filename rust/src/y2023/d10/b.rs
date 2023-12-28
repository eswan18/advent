use crate::y2023::d10::grid::Grid;
use crate::y2023::d10::grid_state::GridState;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let grid = Grid::new_from_str(contents)?;
    println!("{:}", grid);
    let mut state = GridState::new(&grid)?;
    state.build_loop()?;
    println!("{:}", state);
    let shape = state.to_shape();
    let points_inside = shape.points_inside();
    Ok(format!("{}", points_inside.len()))
}
