use std::{fmt::Display, collections::HashSet};

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub struct Point {
    pub x: i32,
    pub y: i32,
}

impl Point {
    pub fn to(&self, d: &Direction) -> Point {
        match d {
            Direction::North => Point { x: self.x, y: self.y - 1 },
            Direction::South => Point { x: self.x, y: self.y + 1 },
            Direction::East => Point { x: self.x + 1, y: self.y },
            Direction::West => Point { x: self.x - 1, y: self.y },
        }
    }
}

pub enum Direction { 
    North,
    South,
    East,
    West
}

pub struct Platform {
    width: usize,
    height: usize,
    rounded_rocks: Vec<Point>,
    cube_rocks: Vec<Point>,
}

impl Platform {
    pub fn new_from_str(s: &str) -> Platform {
        let mut rounded_rocks = Vec::new();
        let mut cube_rocks = Vec::new();
        let mut height = 0;
        let mut width = 0;
        for (y, line) in s.lines().enumerate() {
            height = height.max(y);
            for (x, c) in line.chars().enumerate() {
                width = width.max(x);
                match c {
                    'O' => rounded_rocks.push(Point { x: x as i32, y: y as i32 }),
                    '#' => cube_rocks.push(Point { x: x as i32, y: y as i32 }),
                    _ => (),
                }
            }
        }
        Platform {
            height: height + 1,
            width: width + 1,
            rounded_rocks,
            cube_rocks,
        }
    }

    pub fn tilt(&mut self, d: Direction) {
        // For whatever direction we're rolling the rocks, we want to start with rocks that are already
        // closest to that direction (to clear space for the later ones).
        match d {
            Direction::North => {
                self.rounded_rocks.sort_by(|a, b| { a.y.cmp(&b.y) })
            },
            Direction::South => {
                self.rounded_rocks.sort_by(|a, b| { b.y.cmp(&a.y) })
            },
            Direction::West => {
                self.rounded_rocks.sort_by(|a, b| { a.x.cmp(&b.x) })
            },
            Direction::East => {
                self.rounded_rocks.sort_by(|a, b| { b.x.cmp(&a.x) })
            },
        };
        let mut new_rounded_rocks = self.rounded_rocks.clone();
        let mut occupied_positions = self.cube_rocks.iter().collect::<HashSet<_>>();
        for rock in &mut new_rounded_rocks {
            let new_position = self.first_open_in(&rock, &d, &occupied_positions);
            rock.x = new_position.x;
            rock.y = new_position.y;
            occupied_positions.insert(rock);
        }
        self.rounded_rocks = new_rounded_rocks;
    }

    fn first_open_in(&self, start: &Point, d: &Direction, occupied: &HashSet<&Point>) -> Point {
        let mut p: Point = (*start).clone();
        loop {
            let maybe_next = p.to(d);
            if occupied.contains(&maybe_next) { break }
            match d {
                Direction::North => {
                    if maybe_next.y < 0 { break }
                },
                Direction::South => {
                    if maybe_next.y >= self.height as i32 { break }
                },
                Direction::East => {
                    if maybe_next.x >= self.width as i32 { break }
                },
                Direction::West => {
                    if maybe_next.x < 0 { break }
                },
            }
            // If we got here without breaking out, the next point is valid.
            p = maybe_next;
        }
        p
    }
    
    pub fn load(&self) -> usize {
        self.rounded_rocks.iter().map(|rock| { self.height - rock.y as usize }).sum::<usize>()
    }

    pub fn cycle(&mut self) {
        self.tilt(Direction::North);
        self.tilt(Direction::West);
        self.tilt(Direction::South);
        self.tilt(Direction::East);
    }

    pub fn rounded_rock_hash(&self) -> u64 {
        let mut hash = 0;
        for rock in &self.rounded_rocks {
            hash += rock.x as u64;
            hash += rock.y as u64 * 1000;
        }
        hash
    }
}

impl Display for Platform {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.height as i32 {
            for x in 0..self.width as i32 {
                let c = if self.rounded_rocks.contains(&Point { x, y }) {
                    'O'
                } else if self.cube_rocks.contains(&Point { x, y }) {
                    '#'
                } else {
                    '.'
                };
                write!(f, "{}", c)?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}