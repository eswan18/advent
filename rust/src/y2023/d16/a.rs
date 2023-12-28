use crate::y2023::d16::contraption::Contraption;

pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let contraption = Contraption::new_from_str(contents)?;
    println!("{}", contraption);
    Err("Not yet implemented".into())
}