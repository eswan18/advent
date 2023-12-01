extern crate rust;

fn main() {
    let args = rust::parse();
    println!("args: {:?}", args);
    let filename = match (args.test, args.file) {
        // The user passed no file-related options.
        (false, None) => String::from("input.txt"),
        // The user passed a custom input file.
        (false, Some(filename)) => filename,
        // The user passed the --test flag.
        (true, None) => String::from("test_input.txt"),
        // The user passed both --test and --file (invalid).
        (true, Some(_)) => panic!("Cannot pass both --test and --file"),
    };
    println!("filename: {}", filename);
}
