use std::fmt::Display;

#[derive(Debug, Clone)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

#[derive(Debug, Clone)]
pub struct PointWithDirection {
    pub point: Point,
    pub direction: Direction,
}

impl Point {
    fn to(&self, direction: &Direction) -> Point {
        match direction {
            Direction::Up => Point { x: self.x - 1, y: self.y },
            Direction::Down => Point { x: self.x + 1, y: self.y },
            Direction::Left => Point { x: self.x, y: self.y - 1 },
            Direction::Right => Point { x: self.x, y: self.y + 1 },
        }
    }
}

#[derive(Debug, Clone)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug)]
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
        Ok(Self { spaces, width, height })
    }

    pub fn at(&self, point: &Point) -> Option<&Space> {
        self.spaces.get(point.x as usize)?.get(point.y as usize)
    }

    pub fn dimensions(&self) -> (usize, usize) {
        (self.width, self.height)
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

#[derive(Debug)]
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
            Self::Empty => vec![PointWithDirection{point: at.to(direction), direction: direction.clone()}],
            Self::Mirror(mirror) => mirror.next_points(at, direction),
            Self::Splitter(splitter) => splitter.next_points(at, direction),
        }

    }
}

#[derive(Debug)]
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
        vec![PointWithDirection{point: at.to(&to), direction: to}]
    }
}

#[derive(Debug)]
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
        to_directions.iter().map(|to| PointWithDirection{point: at.to(to), direction: to.clone()}).collect()
    }
}