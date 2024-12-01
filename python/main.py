import argparse
from pathlib import Path

YEARS = ['2023', '2024']
PARTS = ['a', 'b']

USAGE_MESSAGE = """
Usage: python main.py [year] [day] [a/b] <--test>
python main.py 2023 1 a --test
If --test is passed, the input file will be test_input.txt
Custom input files can also be passed, like so:
python main.py 2023 1 a --file custom_input.txt
"""

parser = argparse.ArgumentParser()
parser.add_argument("year", type=str, choices=YEARS)
parser.add_argument("day", type=str, choices=[str(i) for i in range(1, 26)])
parser.add_argument("part", type=str, choices=PARTS)
parser.add_argument("--test", action="store_true")
parser.add_argument("--file", type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    year = args.year
    day = args.day
    part = args.part
    test = args.test
    file = args.file

    # Validation
    if str(year) not in YEARS:
        raise ValueError("year must be 2023")
    if part not in PARTS:
        raise ValueError("part must be either 'a' or 'b'")
    
    filename = "input.txt"
    if test:
        filename = "test_input.txt"
    elif file:
        filename = file
    
    # Try to find the input file.
    filepath = Path('../inputs') / year / day / part / filename
    if not filepath.exists():
        raise ValueError(f"file {filepath} does not exist")
    contents = filepath.read_text()
    
    # Try to magically import the correct module
    try:
        module = __import__(f'{year}.{day}', fromlist=[part])
    except ModuleNotFoundError:
        raise ValueError(f"no module {year}.{day} found")
    if part == 'a':
        result = module.a(contents)
    else:
        result = module.b(contents)
    print(f'Result: {result}')
    
    print(f'running year {year}, day {day}, part {part}, with input file {filename}')