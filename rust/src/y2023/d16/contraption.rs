use std::fmt::Display;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct PointWithDirection {
    pub point: Point,
    pub direction: Direction,
}

impl Point {
    fn to(&self, direction: &Direction) -> Point {
        match direction {
            Direction::Up => Point {
                x: self.x,
                y: self.y - 1,
            },
            Direction::Down => Point {
                x: self.x,
                y: self.y + 1,
            },
            Direction::Left => Point {
                x: self.x - 1,
                y: self.y,
            },
            Direction::Right => Point {
                x: self.x + 1,
                y: self.y,
            },
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug, Clone)]
pub struct Contraption {
    spaces: Vec<Vec<Space>>,
    width: usize,
    height: usize,
}

impl Contraption {
    pub fn new_from_str(s: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let mut spaces = Vec::new();
        let mut height = 0;
        let mut width = 0;
        for line in s.lines() {
            let mut row = Vec::new();
            for c in line.chars() {
                let space = Space::new_from_char(&c)?;
                row.push(space);
            }
            width = width.max(row.len());
            spaces.push(row);
            height += 1;
        }
        Ok(Self {
            spaces,
            width,
            height,
        })
    }

    pub fn at(&self, point: &Point) -> Option<&Space> {
        self.spaces.get(point.y as usize)?.get(point.x as usize)
    }

    pub fn dimensions(&self) -> (usize, usize) {
        (self.width, self.height)
    }

    pub fn display_at(&self, at: &Point) -> char {
        let space = self.at(at).unwrap();
        match space {
            Space::Empty => '.',
            Space::Mirror(mirror) => match mirror {
                Mirror::Slash => '/',
                Mirror::Backslash => '\\',
            },
            Space::Splitter(splitter) => match splitter {
                Splitter::Horizontal => '-',
                Splitter::Vertical => '|',
            },
        }
    }

    pub fn all_entrances(&self) -> Vec<PointWithDirection> {
        let mut entrances = Vec::new();
        for y in 0..self.height {
            entrances.push(PointWithDirection {
                point: Point { x: 0, y: y as i32 },
                direction: Direction::Right,
            });
            entrances.push(PointWithDirection {
                point: Point {
                    x: (self.width - 1) as i32,
                    y: y as i32,
                },
                direction: Direction::Left,
            });
        }
        for x in 0..self.width {
            entrances.push(PointWithDirection {
                point: Point { x: x as i32, y: 0 },
                direction: Direction::Down,
            });
            entrances.push(PointWithDirection {
                point: Point {
                    x: x as i32,
                    y: (self.height - 1) as i32,
                },
                direction: Direction::Up,
            });
        }
        entrances
    }
}

impl Display for Contraption {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in &self.spaces {
            for space in row {
                match space {
                    Space::Empty => write!(f, ".")?,
                    Space::Mirror(mirror) => match mirror {
                        Mirror::Slash => write!(f, "/")?,
                        Mirror::Backslash => write!(f, "\\")?,
                    },
                    Space::Splitter(splitter) => match splitter {
                        Splitter::Horizontal => write!(f, "-")?,
                        Splitter::Vertical => write!(f, "|")?,
                    },
                }
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

#[derive(Debug, Clone)]
pub enum Space {
    Empty,
    Mirror(Mirror),
    Splitter(Splitter),
}

impl Space {
    pub fn new_from_char(c: &char) -> Result<Self, Box<dyn std::error::Error>> {
        let mirror_result = Mirror::new_from_char(c);
        if let Ok(mirror) = mirror_result {
            return Ok(Self::Mirror(mirror));
        }
        let splitter_result = Splitter::new_from_char(c);
        if let Ok(splitter) = splitter_result {
            return Ok(Self::Splitter(splitter));
        }
        Ok(Self::Empty)
    }

    pub fn next_points(&self, at: &Point, direction: &Direction) -> Vec<PointWithDirection> {
        match self {
            Self::Empty => vec![PointWithDirection {
                point: at.to(direction),
                direction: direction.clone(),
            }],
            Self::Mirror(mirror) => mirror.next_points(at, direction),
            Self::Splitter(splitter) => splitter.next_points(at, direction),
        }
    }
}

#[derive(Debug, Clone)]
enum Mirror {
    Slash,
    Backslash,
}

impl Mirror {
    fn new_from_char(c: &char) -> Result<Self, Box<dyn std::error::Error>> {
        match c {
            '/' => Ok(Self::Slash),
            '\\' => Ok(Self::Backslash),
            _ => Err(format!("Invalid splitter: {}", c).into()),
        }
    }

    fn next_points(&self, at: &Point, direction: &Direction) -> Vec<PointWithDirection> {
        let to: Direction = match self {
            Self::Slash => match direction {
                Direction::Up => Direction::Right,
                Direction::Down => Direction::Left,
                Direction::Left => Direction::Down,
                Direction::Right => Direction::Up,
            },
            Self::Backslash => match direction {
                Direction::Up => Direction::Left,
                Direction::Down => Direction::Right,
                Direction::Left => Direction::Up,
                Direction::Right => Direction::Down,
            },
        };
        vec![PointWithDirection {
            point: at.to(&to),
            direction: to,
        }]
    }
}

#[derive(Debug, Clone)]
enum Splitter {
    Horizontal,
    Vertical,
}

impl Splitter {
    fn new_from_char(c: &char) -> Result<Self, Box<dyn std::error::Error>> {
        match c {
            '-' => Ok(Self::Horizontal),
            '|' => Ok(Self::Vertical),
            _ => Err(format!("Invalid splitter: {}", c).into()),
        }
    }

    fn next_points(&self, at: &Point, direction: &Direction) -> Vec<PointWithDirection> {
        let to_directions: Vec<Direction> = match self {
            Self::Horizontal => match direction {
                Direction::Up => vec![Direction::Left, Direction::Right],
                Direction::Down => vec![Direction::Left, Direction::Right],
                Direction::Left => vec![Direction::Left],
                Direction::Right => vec![Direction::Right],
            },
            Self::Vertical => match direction {
                Direction::Up => vec![Direction::Up],
                Direction::Down => vec![Direction::Down],
                Direction::Left => vec![Direction::Up, Direction::Down],
                Direction::Right => vec![Direction::Up, Direction::Down],
            },
        };
        to_directions
            .iter()
            .map(|to| PointWithDirection {
                point: at.to(to),
                direction: to.clone(),
            })
            .collect()
    }
}
