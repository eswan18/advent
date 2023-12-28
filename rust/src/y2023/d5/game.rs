use super::mapping::Mapping;
use super::seeds::{SeedSet, SeedsType};

pub struct Game {
    pub seeds: SeedSet,
    layers: Vec<Layer>,
}

impl Game {
    fn new(seeds: SeedSet, layers: Vec<Layer>) -> Self {
        Self { seeds, layers }
    }

    pub fn map(&self, source: i64) -> i64 {
        let mut result = source;
        for layer in &self.layers {
            result = layer.map(result);
        }
        result
    }

    pub fn back_map(&self, target: i64) -> i64 {
        let mut result = target;
        for layer in self.layers.iter().rev() {
            result = layer.back_map(result);
        }
        result
    }

    pub fn new_from_str(contents: &str, seeds_type: SeedsType) -> Self {
        let lines = contents.split("\n\n").collect::<Vec<&str>>();
        let seeds_line = lines[0];
        let seed_set = SeedSet::new_from_line(seeds_line, seeds_type);

        let layers: Vec<Layer> = lines[1..]
            .iter()
            .map(|layer_str| Layer::new_from_str(layer_str))
            .collect();
        Self::new(seed_set, layers)
    }

    pub fn final_translations(&self) -> Vec<i64> {
        match self.seeds {
            SeedSet::List(ref seeds) => return seeds.iter().map(|seed| self.map(*seed)).collect(),
            _ => panic!("final_locations() only works for SeedSet::List"),
        }
    }

    pub fn max_final_destination(&self) -> i64 {
        self.layers.iter().last().unwrap().max_destination()
    }
}

#[derive(Debug)]
struct Layer {
    mappings: Vec<Mapping>,
}

impl Layer {
    fn map(&self, source: i64) -> i64 {
        for mapping in &self.mappings {
            let result = mapping.map(source);
            if let Some(val) = result {
                return val;
            }
        }
        source
    }

    fn back_map(&self, target: i64) -> i64 {
        for mapping in &self.mappings {
            let result = mapping.back_map(target);
            if let Some(val) = result {
                return val;
            }
        }
        target
    }

    pub fn new_from_str(contents: &str) -> Self {
        let mut lines = contents.lines();
        // The first line is just a text name.
        lines.next();
        // The remaining lines are mappings.
        let mappings = lines
            .map(|line| Mapping::new_from_line(line))
            .collect::<Vec<Mapping>>();
        Self { mappings }
    }

    pub fn max_destination(&self) -> i64 {
        self.mappings
            .iter()
            .map(|mapping| mapping.destination_range().end)
            .max()
            .unwrap()
    }
}
