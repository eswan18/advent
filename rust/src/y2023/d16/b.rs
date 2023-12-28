use crate::y2023::d16::beam::BeamState;
use crate::y2023::d16::contraption::{Contraption, Direction, Point, PointWithDirection};

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let contraption = Contraption::new_from_str(contents)?;
    let all_entrances = contraption.all_entrances();

    let mut max_energized_count = 0;
    for entrance in all_entrances {
        let mut beam_state = BeamState::new(
            contraption.clone(),
            entrance,
        );

        loop {
            let found_children = beam_state.step();
            if !found_children {
                max_energized_count = max_energized_count.max(beam_state.energized_count());
                break
            }
        }
    }

    Ok(max_energized_count.to_string())
}
