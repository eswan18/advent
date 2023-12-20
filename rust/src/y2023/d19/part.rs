#[derive(Debug)]
pub struct Part {
    pub x: u64,
    pub m: u64,
    pub a: u64,
    pub s: u64,
}

impl Part {
    pub fn get(&self, f: &Field) -> u64 {
        match f {
            Field::X => self.x,
            Field::M => self.m,
            Field::A => self.a,
            Field::S => self.s,
        }
    }

    pub fn new_from_line(s: &str) -> Result<Part, Box<dyn std::error::Error>> {
        // Input lines look like "{x=787,m=2655,a=1222,s=2876}"
        let s = s.strip_prefix("{").ok_or("No opening brace")?.strip_suffix("}").ok_or("No closing brace")?;
        let parts = s.split(",").collect::<Vec<&str>>();
        if parts.len() != 4 {
            return Err("Not enough parts".into());
        }
        let values = parts.iter().map(|s| s.split("=").collect::<Vec<&str>>()[1]).collect::<Vec<&str>>();
        let x = values[0].parse::<u64>()?;
        let m = values[1].parse::<u64>()?;
        let a = values[2].parse::<u64>()?;
        let s = values[3].parse::<u64>()?;
        Ok(Part { x, m, a, s })
    }
    
    pub fn total(&self) -> u64 {
        self.x + self.m + self.a + self.s
    }
}

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum Field {
    X,
    M,
    A,
    S,
}

impl Field {
    pub fn from_str(s: &str) -> Result<Field, Box<dyn std::error::Error>> {
        match s {
            "x" => Ok(Field::X),
            "m" => Ok(Field::M),
            "a" => Ok(Field::A),
            "s" => Ok(Field::S),
            _ => Err("Invalid field".into()),
        }
    }

    pub fn all() -> Vec<Field> {
        vec![Field::X, Field::M, Field::A, Field::S]
    }
}

// An inclusive range.
#[derive(Debug, PartialEq)]
pub struct Range {
    pub start: u64,
    pub end: u64,
}

impl Range {
    pub fn len(&self) -> u64 {
        self.end - self.start + 1
    }
}