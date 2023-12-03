use clap::Parser;

const YEARS: [&str; 1] = ["2023"];
const PARTS: [&str; 2] = ["a", "b"];

const USAGE_MESSAGE: &str = "
Usage: python main.py [year] [day] [a/b] <--test>
python main.py 2023 1 a --test
If --test is passed, the input file will be test_input.txt
Custom input files can also be passed, like so:
python main.py 2023 1 a --file custom_input.txt
";

#[derive(Debug, Parser)]
#[command(long_about = USAGE_MESSAGE)]
pub struct Args {
    pub year: String,
    pub day: String,
    pub part: String,
    #[clap(short, long)]
    pub test: bool,
    #[clap(short, long)]
    pub file: Option<String>,
}

pub fn parse() -> Args {
    let args = Args::parse();
    // Validate
    if !YEARS.contains(&&*args.year) {
        panic!("Invalid year: {}", args.year);
    }
    if !PARTS.contains(&&*args.part) {
        panic!("Invalid part: {}", args.part);
    }
    return args;
}
