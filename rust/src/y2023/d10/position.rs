use crate::y2023::d10::pipe::Direction;

#[derive(PartialEq, Eq, Hash, Clone, Copy, Debug)]
pub struct Position {
    pub x: usize,
    pub y: usize,
}

impl Position {
    pub fn to(&self, direction: Direction) -> Self {
        match direction {
            Direction::Left => Position { x: self.x - 1, y: self.y },
            Direction::Right => Position { x: self.x + 1, y: self.y },
            Direction::Up => Position { x: self.x, y: self.y - 1 },
            Direction::Down => Position { x: self.x, y: self.y + 1 },
        }
    }
}
