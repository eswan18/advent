use crate::y2023::d18::instruction::{Instruction, Direction};


#[derive(Debug, PartialEq, Eq, Clone)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct Segment {
    start: Point,
    end: Point,
}


#[derive(Debug)]
pub struct Path {
    segments: Vec<Segment>,    
}

impl Path {
    pub fn new() -> Path {
        Path {
            segments: Vec::new(),
        }
    }

    pub fn execute(&mut self, instruction: Instruction) {
        let start = self.segments.last().map(|s| s.end.clone()).unwrap_or(Point { x: 0, y: 0 });
        let end = match instruction.direction {
            Direction::Up => Point { x: start.x, y: start.y - instruction.distance as i32 },
            Direction::Down => Point { x: start.x, y: start.y + instruction.distance as i32 },
            Direction::Left => Point { x: start.x - instruction.distance as i32, y: start.y },
            Direction::Right => Point { x: start.x + instruction.distance as i32, y: start.y },
        };
        self.segments.push(Segment { start, end });
    }

    pub fn execute_all(&mut self, instructions: Vec<Instruction>) {
        for i in instructions {
            self.execute(i);
        }
    }

    fn is_closed(&self) -> bool {
        let last = match self.segments.last() {
            Some(s) => s,
            None => return false,
        };
        let first = match self.segments.first() {
            Some(s) => s,
            None => return false,
        };
        first.start == last.end
    }

    pub fn calculate_area(&self) -> u64 {
        let interior_area = self.calculate_interior_area();
        let perimeter = self.calculate_perimeter();
        interior_area + (perimeter / 2) as u64 + 1
    }

    fn calculate_interior_area(&self) -> u64 {
        if !self.is_closed() {
            return 0;
        }
        // The "shoelace formula".
        let mut sum: i64 = 0;
        for i in 0..self.segments.len() {
            let segment = &self.segments[i];
            let next_segment = &self.segments[(i + 1) % self.segments.len()];
            sum += segment.start.x as i64 * next_segment.start.y as i64;
            sum -= segment.start.y as i64 * next_segment.start.x as i64;
        }
        sum.abs() as u64 / 2
    }

    fn calculate_perimeter(&self) -> i32 {
        if !self.is_closed() {
            return 0;
        }
        let mut sum = 0;
        for segment in &self.segments {
            sum += (segment.start.x - segment.end.x).abs();
            sum += (segment.start.y - segment.end.y).abs();
        }
        sum
    }
}