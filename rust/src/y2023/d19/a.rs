use crate::y2023::d19::part::Part;
use crate::y2023::d19::rule::Ruleset;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let (test_section, parts_section) = contents.split_once("\n\n").ok_or("No blank line")?;
    let ruleset = Ruleset::new_from_str(test_section)?;
    let parts = parts_section
        .lines()
        .map(Part::new_from_line)
        .collect::<Result<Vec<Part>, Box<dyn std::error::Error>>>()?;
    let mut running_sum = 0;
    for part in parts {
        let t = ruleset.test(&part)?;
        if t {
            running_sum += part.total();
        }
    }
    Ok(running_sum.to_string())
}
