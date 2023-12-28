#[derive(Debug)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    pub fn from_char(s: &str) -> Option<Direction> {
        match s {
            "U" => Some(Direction::Up),
            "D" => Some(Direction::Down),
            "L" => Some(Direction::Left),
            "R" => Some(Direction::Right),
            _ => None,
        }
    }

    pub fn from_code(s: &str) -> Option<Direction> {
        match s {
            "3" => Some(Direction::Up),
            "1" => Some(Direction::Down),
            "2" => Some(Direction::Left),
            "0" => Some(Direction::Right),
            _ => None,
        }
    }
}

#[derive(Debug)]
pub struct Instruction {
    pub direction: Direction,
    pub distance: u32,
}

pub enum InstructionMode {
    Naive,
    Swapped,
}

impl Instruction {
    pub fn from_line(line: &str, mode: InstructionMode) -> Option<Instruction> {
        let parts = line.split(" ").collect::<Vec<&str>>();
        match mode {
            InstructionMode::Naive => {
                let direction = parts.get(0).and_then(|s| Direction::from_char(*s))?;
                let distance = parts.get(1).and_then(|s| s.parse::<u32>().ok())?;
                Some(Instruction {
                    direction,
                    distance,
                })
            }
            InstructionMode::Swapped => {
                let code = parts.last()?;
                let code = code.strip_prefix("(#")?.strip_suffix(")")?;
                // The first five digits are the distance, in hex.
                let distance = u32::from_str_radix(&code[0..5], 16).ok()?;
                // The last digit is the direction.
                let direction = Direction::from_code(&code[5..6])?;
                Some(Instruction {
                    direction,
                    distance,
                })
            }
        }
    }
}
