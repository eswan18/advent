use crate::y2023::d16::beam::BeamState;
use crate::y2023::d16::contraption::{Contraption, Direction, Point, PointWithDirection};

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let contraption = Contraption::new_from_str(contents)?;

    let mut beam_state = BeamState::new(
        contraption,
        PointWithDirection {
            point: Point { x: 0, y: 0 },
            direction: Direction::Right,
        },
    );
    let visual = beam_state.visualize();
    println!("{}", visual);

    loop {
        let found_children = beam_state.step();
        if !found_children {
            return Ok(beam_state.energized_count().to_string())
        }
    }
}
