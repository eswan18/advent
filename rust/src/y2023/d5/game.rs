use super::range::Range;
use super::mapping::Mapping;

pub struct Game {
    seeds: SeedSet,
    layers: Vec<Layer>,
}

impl Game {
    fn new(seeds: SeedSet, layers: Vec<Layer>) -> Self {
        Self { seeds, layers }
    }

    pub fn map(&self, source: i64 ) -> i64 {
        let mut result = source;
        for layer in &self.layers {
            result = layer.map(result);
        }
        result
    }

    pub fn new_from_str(contents: &str, seeds_type: SeedsType) -> Self {
        let lines = contents.split("\n\n").collect::<Vec<&str>>();
        let seeds_line = lines[0];
        let seed_set = SeedSet::new_from_line(seeds_line, seeds_type);

        let layers: Vec<Layer> = lines[1..].iter().map(|layer_str| Layer::new_from_str(layer_str)).collect();
        Self::new(seed_set, layers)
    }

    pub fn final_translations(&self) -> Vec<i64> {
        match self.seeds {
            SeedSet::List(ref seeds) => {
                return seeds.iter().map(|seed| self.map(*seed)).collect()
            },
            _ => panic!("final_locations() only works for SeedSet::List"),
        }
    }
}

enum SeedSet {
    List(Vec<i64>),
    RangeList(Vec<Range>),
}

impl SeedSet {
    pub fn new_from_line(line: &str, seeds_type: SeedsType) -> Self {
        let value_str = line.split(": ").collect::<Vec<&str>>()[1];
        let values = value_str.split(' ').map(|s| s.parse::<i64>().unwrap()).collect::<Vec<i64>>();
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
        }
    }
}

pub enum SeedsType { List, RangeList }

#[derive(Debug)]
struct Layer {
    mappings: Vec<Mapping>,
}

impl Layer {
    fn map(&self, source: i64 ) -> i64 {
        for mapping in &self.mappings {
            let result = mapping.map(source);
            if let Some(val) = result {
                return val;
            }
        }
        source
    }

    pub fn new_from_str(contents: &str) -> Self {
        let mut lines = contents.lines();
        // The first line is just a text name.
        lines.next();
        // The remaining lines are mappings.
        let mappings = lines.map(|line| Mapping::new_from_line(line)).collect::<Vec<Mapping>>();
        Self { mappings }
    }
}
