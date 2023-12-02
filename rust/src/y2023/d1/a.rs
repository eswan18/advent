pub fn run_a(contents: &str) -> Result<String, Box<dyn std::error::Error>> {
    let mut sum = 0;
    let lines = contents.lines();
    for line in lines {
        let mut first_num: Option<u32> = None;
        let mut last_num: Option<u32> = None;
        for char in line.chars() {
            match char.to_digit(10) {
                Some(num) => {
                    if first_num.is_none() {
                        first_num = Some(num);
                    }
                    last_num = Some(num);
                },
                None => {},
            }
        }
        match (first_num, last_num) {
            (Some(first), Some(last)) => sum += 10 * first + last,
            _ => return Err("Invalid line - missing a digit".into()),
        }
    }
    Ok(sum.to_string())
}