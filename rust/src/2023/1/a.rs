pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    print!("contents: {}", contents);
    return Ok(String::from("a"));
}