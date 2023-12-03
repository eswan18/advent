#[derive(Debug)]
pub struct Coord {
    x: usize,
    y: usize,
}

impl Coord {
    pub fn adjacent(&self, other: &Coord) -> bool {
        self.x.abs_diff(other.x) <= 1 && self.y.abs_diff(other.y) <= 1
    }
}

#[derive(Debug)]
pub struct Symbol {
    pub coord: Coord,
    pub symbol: char,
}

#[derive(Debug)]
pub struct Number {
    coords: Vec<Coord>,
    pub value: u32,
}

impl Number {
    pub fn adjacent(&self, c: &Coord) -> bool {
        for coord in &self.coords {
            if coord.adjacent(c) {
                return true;
            }
        }
        false
    }
}

pub struct Schematic {
    pub symbols: Vec<Symbol>,
    pub numbers: Vec<Number>,
}

impl Schematic {
    pub fn parse(contents: &str) -> Result<Schematic, Box<dyn std::error::Error>> {
        let mut symbols = Vec::new();
        let mut numbers = Vec::new();
        for (y, line) in contents.lines().enumerate() {
            let mut x = 0;
            while x < line.len() {
                let c = line.chars().nth(x).unwrap();
                match c {
                    '.' => x += 1,
                    c if c.is_digit(10) => {
                        // Incrementally build the number and its coordinates by iterating until we stop seeing digits.
                        let mut digits = c.to_string();
                        let mut coords = vec![Coord { x, y }];
                        x += 1;
                        while x < line.len() {
                            let c = line.chars().nth(x).unwrap();
                            if c.is_digit(10) {
                                digits.push(c);
                                coords.push(Coord { x, y });
                                x += 1;
                            } else {
                                break;
                            }
                        }
                        let value = digits.parse::<u32>()?;
                        numbers.push(Number { coords, value })
                    }
                    sym => {
                        symbols.push(Symbol {
                            coord: Coord { x, y },
                            symbol: sym,
                        });
                        x += 1;
                    }
                }
            }
        }
        Ok(Schematic { symbols, numbers })
    }
}
