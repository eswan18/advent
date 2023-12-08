pub mod parse;
pub mod y2023;

pub fn main() {
    let args = parse::parse();
    let filename = choose_filename(args.test, args.file).unwrap_or_else(|e| {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    });

    let path = format!(
        "../inputs/{}/{}/{}/{}",
        args.year, args.day, args.part, filename
    );
    // Error if the file doesn't exist.
    let contents = std::fs::read_to_string(path).expect("Failed to read input file");

    let answer = dispatch(&args.year, &args.day, &args.part, &contents).unwrap_or_else(|e| {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    });
    println!("Answer: {}", answer);
}

fn choose_filename(
    test: bool,
    filename: Option<String>,
) -> Result<String, Box<dyn std::error::Error>> {
    let filename = match (test, filename) {
        // The user passed no file-related options.
        (false, None) => String::from("input.txt"),
        // The user passed a custom input file.
        (false, Some(filename)) => filename,
        // The user passed the --test flag.
        (true, None) => String::from("test_input.txt"),
        // The user passed both --test and --file (invalid).
        (true, Some(_)) => return Err("Cannot pass both --test and --file".into()),
    };
    return Ok(filename);
}

fn dispatch(
    year: &str,
    day: &str,
    part: &str,
    contents: &str,
) -> Result<String, Box<dyn std::error::Error>> {
    return match year {
        "2023" => match day {
            "1" => match part {
                "a" => y2023::d1::a::run_a(contents),
                "b" => y2023::d1::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "2" => match part {
                "a" => y2023::d2::a::run_a(contents),
                "b" => y2023::d2::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "3" => match part {
                "a" => y2023::d3::a::run_a(contents),
                "b" => y2023::d3::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "4" => match part {
                "a" => y2023::d4::a::run_a(contents),
                "b" => y2023::d4::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "5" => match part {
                "a" => y2023::d5::a::run_a(contents),
                "b" => y2023::d5::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "6" => match part {
                "a" => y2023::d6::a::run_a(contents),
                "b" => y2023::d6::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            _ => panic!("Invalid day: {}", day),
        },
        _ => panic!("Invalid year: {}", year),
    };
}
