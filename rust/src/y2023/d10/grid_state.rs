use crate::y2023::d10::grid::{Grid, Tile};
use crate::y2023::d10::pipe::Direction;
use crate::y2023::d10::position::Position;
use crate::y2023::d10::shape::Shape;
use std::collections::{HashMap, HashSet};
use std::fmt::Display;

pub struct GridState<'a> {
    grid: &'a Grid,
    path_a: Path,
    path_b: Path,
    seen_count: HashMap<Position, u32>,
}

impl<'a> GridState<'a> {
    pub fn new(grid: &'a Grid) -> Result<GridState<'a>, Box<dyn std::error::Error>> {
        let start = grid.start;
        let start_directions = match grid.at(start) {
            Some(Tile::Pipe(pipe)) => pipe.connections(),
            _ => return Err("Start position is empty".into()),
        };
        let path_a = Path {
            positions: vec![start],
            facing: start_directions[0],
        };
        let path_b = Path {
            positions: vec![start],
            facing: start_directions[1],
        };
        let mut seen_count = HashMap::new();
        seen_count.insert(start, 1);
        Ok(GridState {
            grid,
            path_a,
            path_b,
            seen_count,
        })
    }

    pub fn step(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        let new_a = self.path_a.step(self.grid)?;
        let new_b = self.path_b.step(self.grid)?;
        // Update the seen counts.
        let count_a = self.seen_count.entry(new_a).or_insert(0);
        *count_a += 1;
        let count_b = self.seen_count.entry(new_b).or_insert(0);
        *count_b += 1;
        Ok(())
    }

    pub fn has_loop(&self) -> bool {
        self.seen_count.values().any(|&count| count > 1)
    }

    pub fn step_count(&self) -> usize {
        self.path_a.positions.len() - 1
    }

    pub fn build_loop(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        while !self.has_loop() {
            self.step()?;
        }
        Ok(())
    }

    pub fn to_shape(&self) -> Shape {
        let points = self
            .seen_count
            .keys()
            .cloned()
            .collect::<HashSet<Position>>();
        Shape::new(self.grid, points)
    }
}

impl Display for GridState<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let grid = self.grid;
        let n_rows = grid.n_rows();
        let n_cols = grid.n_cols();
        let path_positions = self
            .path_a
            .positions
            .iter()
            .chain(self.path_b.positions.iter())
            .collect::<HashSet<&Position>>();
        for y in 0..n_rows {
            for x in 0..n_cols {
                let on_path = path_positions.contains(&&Position { x, y });
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

struct Path {
    positions: Vec<Position>,
    facing: Direction,
}

impl Path {
    pub fn step(&mut self, grid: &Grid) -> Result<Position, Box<dyn std::error::Error>> {
        let last_position = self.positions.last().unwrap();
        let next_position = last_position.to(self.facing);
        self.positions.push(next_position);

        let Position { x, y } = next_position;
        if y >= grid.n_rows() || x >= grid.n_cols() {
            return Err("Out of bounds".into());
        }
        let next_pipe = match &grid.at(next_position) {
            Some(Tile::Pipe(pipe)) => pipe,
            _ => return Err("Empty tile".into()),
        };
        let new_facing = next_pipe.next_direction(self.facing.opposite());
        self.facing = new_facing;
        Ok(next_position)
    }
}
