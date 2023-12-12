use crate::y2023::d10::grid::Grid;
use crate::y2023::d10::grid_state::GridState;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let grid = Grid::new_from_str(contents)?;
    let mut state = GridState::new(&grid)?;
    state.build_loop()?;
    let path_len = state.step_count();
    Ok(path_len.to_string())
}