#[derive(Debug)]
pub struct Part {
    x: u64,
    m: u64,
    a: u64,
    s: u64,
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

#[derive(Debug)]
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
}