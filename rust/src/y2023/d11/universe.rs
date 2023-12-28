use std::fmt::Display;

#[derive(Hash, PartialEq, Eq, Debug, Clone)]
struct Point {
    x: usize,
    y: usize,
}

impl Point {
    fn manhattan_distance(&self, other: &Point) -> usize {
        let dx = self.x.abs_diff(other.x);
        let dy = self.y.abs_diff(other.y);
        dx + dy
    }
}

pub struct Universe {
    galaxies: Vec<Point>,
}

impl Universe {
    pub fn new_from_str(s: &str) -> Universe {
        let mut galaxies = vec![];
        for (y, line) in s.lines().enumerate() {
            for (x, c) in line.chars().enumerate() {
                if c == '#' {
                    galaxies.push(Point { x, y });
                }
            }
        }
        Universe { galaxies }
    }

    fn pairs(&self) -> Vec<(&Point, &Point)> {
        // Get all unique pairs of galaxies.
        let mut pairs = vec![];
        for i in 0..self.galaxies.len() {
            for j in (i + 1)..self.galaxies.len() {
                let a = &self.galaxies[i];
                let b = &self.galaxies[j];
                pairs.push((a, b));
            }
        }
        pairs
    }

    pub fn pair_distances(&self) -> Vec<usize> {
        self.pairs()
            .iter()
            .map(|(a, b)| a.manhattan_distance(b))
            .collect()
    }

    pub fn expand(&self, factor: usize) -> Universe {
        self.expand_x(factor).expand_y(factor)
    }

    fn expand_x(&self, factor: usize) -> Universe {
        let max_x = self.galaxies.iter().map(|p| p.x).max().unwrap();
        let mut empty_x = vec![];
        for x in 0..(max_x + 1) {
            if !self.galaxies.iter().any(|p| p.x == x) {
                empty_x.push(x);
            }
        }
        let mut new_points = vec![];
        for point in self.galaxies.iter() {
            let empty_x_before = empty_x.iter().filter(|x| **x < point.x).count();
            let expand_factor = (factor - 1) * empty_x_before;
            new_points.push(Point {
                x: point.x + expand_factor,
                y: point.y,
            });
        }
        Universe {
            galaxies: new_points,
        }
    }

    fn expand_y(&self, factor: usize) -> Universe {
        let max_y = self.galaxies.iter().map(|p| p.y).max().unwrap();
        let mut empty_y = vec![];
        for y in 0..(max_y + 1) {
            if !self.galaxies.iter().any(|p| p.y == y) {
                empty_y.push(y);
            }
        }
        let mut new_points = vec![];
        for point in self.galaxies.iter() {
            let empty_y_before = empty_y.iter().filter(|y| **y < point.y).count();
            let expand_factor = (factor - 1) * empty_y_before;
            new_points.push(Point {
                x: point.x,
                y: point.y + expand_factor,
            });
        }
        Universe {
            galaxies: new_points,
        }
    }
}

impl Display for Universe {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut s = String::new();
        let max_x = self.galaxies.iter().map(|p| p.x).max().unwrap();
        let max_y = self.galaxies.iter().map(|p| p.y).max().unwrap();
        for y in 0..(max_y + 1) {
            for x in 0..(max_x + 1) {
                if self.galaxies.iter().any(|p| p.x == x && p.y == y) {
                    s.push('#');
                } else {
                    s.push('.');
                }
            }
            s.push('\n');
        }
        write!(f, "{}", s)
    }
}
