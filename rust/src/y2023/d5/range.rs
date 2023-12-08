// Ranges are inclusive.
#[derive(Debug)]
pub struct Range {
    start: i64,
    end: i64,
}

impl Range {
    pub fn new(start: i64, end: i64) -> Self {
        Self { start, end }
    }

    pub fn contains(&self, value: i64) -> bool {
        value >= self.start && value <= self.end
    }

    pub fn transform(&self, delta: i64) -> Self {
        Self { start: self.start + delta, end: self.end + delta }
    }
}