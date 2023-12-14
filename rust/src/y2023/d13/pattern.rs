use std::collections::HashSet;

#[derive(PartialEq, Eq, Hash)]
pub struct Point {
    pub x: usize,
    pub y: usize,
}

pub struct Pattern {
    pub points: HashSet<Point>,
}

impl Pattern {
    pub fn new_from_str(s: &str) -> Self {
        let mut points = HashSet::new();
        for (y, line) in s.lines().enumerate() {
            for (x, c) in line.chars().enumerate() {
                if c == '#' {
                    points.insert(Point { x, y });
                }
            }
        }
        Self { points }
    }

    pub fn to_str(&self) -> String {
        let mut s = String::new();
        let max_x = self.points.iter().map(|p| p.x).max().unwrap();
        let max_y = self.points.iter().map(|p| p.y).max().unwrap();
        for y in 0..=max_y {
            for x in 0..=max_x {
                if self.points.contains(&Point { x, y }) {
                    s.push('#');
                } else {
                    s.push('.');
                }
            }
            s.push('\n');
        }
        return s;
    }

    pub fn find_horizontal_symmetry(&self, mismatches: usize) -> Option<usize> {
        // Where is the line over which this pattern is symmetrical?
        let max_x = self.points.iter().map(|p| p.x).max().unwrap();
        let max_y = self.points.iter().map(|p| p.y).max().unwrap();
        for x_line in 0..max_x {
            // The line actually runs *between* two points.
            let x_line = x_line as f64 + 0.5;
            // Start at this point and work to the right.
            let mut x = (x_line + 0.5) as usize;
            let mut reflected_x = (x_line - 0.5) as i32;
            let mut mismatches_found = 0;
            while x <= max_x && reflected_x >= 0 {
                for y in 0..=max_y {
                    let is_rock = self.points.contains(&Point { x, y });
                    let is_reflected_rock = self.points.contains(&Point {
                        x: reflected_x as usize,
                        y,
                    });
                    if is_rock != is_reflected_rock {
                        mismatches_found += 1;
                        if mismatches_found > mismatches {
                            // Once we've found too many mismatches, there's no point finding more.
                            break;
                        }
                    }
                }
                x += 1;
                reflected_x -= 1;
            }
            if mismatches_found == mismatches {
                return Some((x_line - 0.5) as usize);
            }
        }
        None
    }

    pub fn find_vertical_symmetry(&self, mismatches: usize) -> Option<usize> {
        // Where is the line over which this pattern is symmetrical?
        let max_x = self.points.iter().map(|p| p.x).max().unwrap();
        let max_y = self.points.iter().map(|p| p.y).max().unwrap();
        for y_line in 0..max_y {
            // The line actually runs *between* two points.
            let y_line = y_line as f64 + 0.5;
            // Start at this point and work to the right.
            let mut y = (y_line + 0.5) as usize;
            let mut reflected_y = (y_line - 0.5) as i32;
            let mut mismatches_found = 0;
            while y <= max_y && reflected_y >= 0 {
                for x in 0..=max_x {
                    let is_rock = self.points.contains(&Point { x, y });
                    let is_reflected_rock = self.points.contains(&Point {
                        x,
                        y: reflected_y as usize,
                    });
                    if is_rock != is_reflected_rock {
                        mismatches_found += 1;
                        if mismatches_found > mismatches {
                            // Once we've found too many mismatches, there's no point finding more.
                            break;
                        }
                    }
                }
                y += 1;
                reflected_y -= 1;
            }
            if mismatches_found == mismatches {
                return Some((y_line - 0.5) as usize);
            }
        }
        None
    }

    pub fn find_reflect_score(&self, mismatches: usize) -> Result<usize, Box<dyn std::error::Error>> {
        let vert_score = self.find_vertical_symmetry(mismatches);
        if let Some(vert_score) = vert_score {
            return Ok((vert_score + 1) * 100);
        }
        let horiz_score = self.find_horizontal_symmetry(mismatches);
        if let Some(horiz_score) = horiz_score {
            return Ok(horiz_score + 1);
        }
        Err("no symmetry".into())
    }
}