use super::range::Range;

#[derive(Debug)]
pub struct Mapping {
    source_range: Range,
    delta: i64,
}

impl Mapping {
    fn destination_range(&self) -> Range {
        self.source_range.transform(self.delta)
    }

    pub fn map(&self, source: i64) -> Option<i64> {
        if self.source_range.contains(source) {
            return Some(source + self.delta);
        }
        None
    }

    pub fn back_map(&self, target: i64) -> Option<i64> {
        let dest_range = self.destination_range();
        if dest_range.contains(target) {
            return Some(target - self.delta);
        }
        None
    }

    pub fn new_from_line(line: &str) -> Self {
        let parts: Vec<&str> = line.split(' ').collect();
        let destination_start = parts[0].parse::<i64>().unwrap();
        let source_start = parts[1].parse::<i64>().unwrap();
        let delta = destination_start - source_start;
        let length = parts[2].parse::<i64>().unwrap();
        Mapping { source_range: Range::new(source_start, source_start + length - 1), delta}
    }
}