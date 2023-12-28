use super::range::Range;

pub enum SeedSet {
    List(Vec<i64>),
    RangeList(Vec<Range>),
}

impl SeedSet {
    pub fn new_from_line(line: &str, seeds_type: SeedsType) -> Self {
        let value_str = line.split(": ").collect::<Vec<&str>>()[1];
        let values = value_str
            .split(' ')
            .map(|s| s.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();
        return match seeds_type {
            SeedsType::List => Self::List(values),
            SeedsType::RangeList => {
                let mut ranges = Vec::new();
                // Take values in pairs.
                for i in 0..values.len() / 2 {
                    let start = values[i * 2];
                    let length = values[i * 2 + 1];
                    ranges.push(Range::new(start, start + length - 1));
                }
                Self::RangeList(ranges)
            }
        };
    }

    pub fn contains(&self, value: i64) -> bool {
        match self {
            Self::List(ref seeds) => seeds.contains(&value),
            Self::RangeList(ref ranges) => {
                for range in ranges {
                    if range.contains(value) {
                        return true;
                    }
                }
                false
            }
        }
    }
}

pub enum SeedsType {
    List,
    RangeList,
}
