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
            "7" => match part {
                "a" => y2023::d7::a::run_a(contents),
                "b" => y2023::d7::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "8" => match part {
                "a" => y2023::d8::a::run_a(contents),
                "b" => y2023::d8::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "9" => match part {
                "a" => y2023::d9::a::run_a(contents),
                "b" => y2023::d9::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "10" => match part {
                "a" => y2023::d10::a::run_a(contents),
                "b" => y2023::d10::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "11" => match part {
                "a" => y2023::d11::a::run_a(contents),
                "b" => y2023::d11::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "12" => match part {
                "a" => y2023::d12::a::run_a(contents),
                "b" => y2023::d12::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "13" => match part {
                "a" => y2023::d13::a::run_a(contents),
                "b" => y2023::d13::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "14" => match part {
                "a" => y2023::d14::a::run_a(contents),
                "b" => y2023::d14::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "15" => match part {
                "a" => y2023::d15::a::run_a(contents),
                "b" => y2023::d15::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "16" => match part {
                "a" => y2023::d16::a::run_a(contents),
                "b" => y2023::d16::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "18" => match part {
                "a" => y2023::d18::a::run_a(contents),
                "b" => y2023::d18::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            "19" => match part {
                "a" => y2023::d19::a::run_a(contents),
                "b" => y2023::d19::b::run_b(contents),
                _ => panic!("Invalid part: {}", part),
            },
            _ => panic!("Invalid day: {}", day),
        },
        _ => panic!("Invalid year: {}", year),
    };
}
