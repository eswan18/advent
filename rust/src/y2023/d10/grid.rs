use std::{fmt::Display, collections::HashSet};

use crate::y2023::d10::pipe::{Direction, Pipe};
use crate::y2023::d10::position::Position;

pub enum Tile {
    Empty,
    Pipe(Pipe),
}

impl Tile {
    pub fn new_from_char(c: char) -> Result<Tile, Box<dyn std::error::Error>> {
        // Try to parse the char as a pipe and fall back if it fails.
        match Pipe::new_from_char(c) {
            Ok(pipe) => return Ok(Tile::Pipe(pipe)),
            Err(_) => return Ok(Tile::Empty),
        }
    }
}

pub struct Grid {
    tiles: Vec<Vec<Tile>>,
    pub start: Position,
}

impl Grid {
    pub fn new_from_str(contents: &str) -> Result<Grid, Box<dyn std::error::Error>> {
        let mut tiles: Vec<Vec<Tile>> = Vec::new();
        let mut start: Option<Position> = None;
        for (y, line) in contents.lines().enumerate() {
            let mut row: Vec<Tile> = Vec::new();
            for (x, c) in line.chars().enumerate() {
                row.push(Tile::new_from_char(c)?);
                // When we encounter the start position, leave it as an empty space for now and mark it.
                // We'll come back later and impute which pipe belongs there.
                if c == 'S' {
                    start = Some(Position { x, y });
                }
            }
            tiles.push(row);
        }
        let start = match start {
            Some(start) => start,
            None => return Err("No start position found".into()),
        };
        // Impute the pipe that belongs at the start position.
        // TODO
        let tiles = Grid::impute_start_pipe(tiles, start)?;

        Ok(Grid { tiles, start })
    }

    fn impute_start_pipe(tiles: Vec<Vec<Tile>>, start: Position) -> Result<Vec<Vec<Tile>>, Box<dyn std::error::Error>> {
        let mut tiles = tiles;
        let mut connections = HashSet::new();
        let n_rows = tiles.len();
        let n_cols = tiles[0].len();
        let Position { x, y } = start;
        // Look at the tiles around this position and figure out which pipe belongs here.
        let connects_left = x > 0 && match &tiles[y][x - 1] {
            Tile::Pipe(pipe) => pipe.connections().contains(&Direction::Right),
            Tile::Empty => false,
        };
        if connects_left {
            connections.insert(&Direction::Left);
        }
        let connects_right = x < (n_cols - 1) && match &tiles[y][x + 1] {
            Tile::Pipe(pipe) => pipe.connections().contains(&Direction::Left),
            Tile::Empty => false,
        };
        if connects_right {
            connections.insert(&Direction::Right);
        }
        let connects_up = y > 0 && match &tiles[start.y - 1][start.x] {
            Tile::Pipe(pipe) => pipe.connections().contains(&Direction::Down),
            Tile::Empty => false,
        };
        if connects_up {
            connections.insert(&Direction::Up);
        }
        let connects_down = y < (n_rows - 1) && match &tiles[start.y + 1][start.x] {
            Tile::Pipe(pipe) => pipe.connections().contains(&Direction::Up),
            Tile::Empty => false,
        };
        if connects_down {
            connections.insert(&Direction::Down);
        }
        // Find a pipe that has the correct connections.
        let pipe = Pipe::new_from_connections(connections)?;
        tiles[start.y][start.x] = Tile::Pipe(pipe);

        Ok(tiles)
    }

    pub fn at(&self, position: Position) -> Option<&Tile> {
        let Position { x, y } = position;
        match self.tiles.get(y) {
            Some(row) => row.get(x),
            None => None,
        }
    }

    pub fn n_rows(&self) -> usize {
        self.tiles.len()
    }

    pub fn n_cols(&self) -> usize {
        self.tiles[0].len()
    }
}

impl Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in &self.tiles {
            for tile in row {
                match tile {
                    Tile::Empty => write!(f, " ")?,
                    Tile::Pipe(pipe) => write!(f, "{}", pipe)?,
                }
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}
