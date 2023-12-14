use std::fmt::Display;
use std::collections::HashSet;

use crate::y2023::d10::grid::{Tile, Grid};
use crate::y2023::d10::position::Position;
use crate::y2023::d10::pipe::{Pipe, Direction};

pub struct Shape<'a> {
    grid: &'a Grid,
    points: HashSet<Position>,
}

impl<'a> Shape<'a> {
    pub fn new(grid: &'a Grid, points: HashSet<Position>) -> Shape<'a> {
        Shape { grid, points }
    }

    pub fn is_inside(&self, point: Position) -> bool {
        if self.points.contains(&point) {
            return false;
        }
        let intersections = self.raycast_intersection_count(point);
        match intersections % 2 {
            0 => false,
            1 => true,
            _ => unreachable!(),
        }
    }

    pub fn points_inside(&self) -> HashSet<Position> {
        let mut points = HashSet::new();
        for y in 0..self.grid.n_rows() {
            for x in 0..self.grid.n_cols() {
                let point = Position { x, y };
                if self.is_inside(point) {
                    points.insert(point);
                }
            }
        }
        points
    }

    fn raycast_intersection_count(&self, position: Position) -> usize {
        // Raycast straight downward (it's the simplest direction) and count the intersections.
        let mut position = position;
        let mut intersection_count = 0;
        let mut last_seen_bend_direction = None;
        loop {
            position = position.to(Direction::Down);
            if position.y >= self.grid.n_rows() {
                break;
            }
            if !self.points.contains(&position) {
                // Only consider points that are on the shape path (ignore random pipes
                // that are not part of the shape).
                continue;
            }

            if let Some(Tile::Pipe(pipe)) = self.grid.at(position) {
                match *pipe {
                    Pipe::Horizontal => intersection_count += 1,
                    Pipe::Vertical => {},
                    bend @ (Pipe::Bend7 | Pipe::BendF | Pipe::BendJ | Pipe::BendL) => {
                        let direction = match bend {
                            Pipe::BendF | Pipe::BendL => Direction::Right,
                            Pipe::Bend7 | Pipe::BendJ => Direction::Left,
                            _ => unreachable!(),
                        };
                        match last_seen_bend_direction {
                            None => {
                                last_seen_bend_direction = Some(direction);
                            },
                            Some(last_seen_bend) => {
                                // Only count cases where the two bends caused us to "cross over" this square.
                                if last_seen_bend != direction {
                                    intersection_count += 1;
                                }
                                last_seen_bend_direction = None;
                            }
                        }
                    }
                }
            }
        }
        intersection_count
    }

    #[allow(dead_code)]
    pub fn to_str_w_labeled_points(&self, points: HashSet<Position>) -> String {
        let grid = self.grid;
        let n_rows = grid.n_rows();
        let n_cols = grid.n_cols();
        let mut s = String::new();
        for y in 0..n_rows {
            for x in 0..n_cols {
                let on_path = self.points.contains(&&Position { x, y });
                if let Some(tile) = grid.at(Position { x, y }) {
                    if points.contains(&Position { x, y }) {
                        s.push_str("X");
                        continue;
                    }
                    match tile {
                        Tile::Pipe(pipe) if on_path => s.push_str(&pipe.to_string()),
                        _ => s.push_str(" "),
                    }
                }
            }
            s.push_str("\n");
        }
        s
    }
}

impl Display for Shape<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let grid = self.grid;
        let n_rows = grid.n_rows();
        let n_cols = grid.n_cols();
        for y in 0..n_rows {
            for x in 0..n_cols {
                let on_path = self.points.contains(&&Position { x, y });
                if let Some(tile) = grid.at(Position { x, y }) {
                    match tile {
                        Tile::Pipe(pipe) if on_path => write!(f, "{}", pipe)?,
                        _ => write!(f, " ")?,
                    }
                }
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}
