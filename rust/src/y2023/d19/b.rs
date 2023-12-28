use crate::y2023::d19::part::{Field, Part};
use crate::y2023::d19::rule::Ruleset;

pub fn run_b(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let test_section = contents.split("\n\n").next().ok_or("No blank line")?;
    let ruleset = Ruleset::new_from_str(test_section)?;
    let ranges = ruleset.ranges();

    let mut good_combos: u64 = 0;
    // Test the every combination of ranges, using the starting point of each range as the part to test.
    for x_range in &ranges[&Field::X] {
        let x = x_range.start;
        for m_range in &ranges[&Field::M] {
            let m = m_range.start;
            for a_range in &ranges[&Field::A] {
                let a = a_range.start;
                for s_range in &ranges[&Field::S] {
                    let s = s_range.start;
                    let part = Part { x, m, a, s };
                    if ruleset.test(&part)? {
                        good_combos +=
                            x_range.len() * m_range.len() * a_range.len() * s_range.len();
                    }
                }
            }
        }
    }
    Ok(good_combos.to_string())
}
