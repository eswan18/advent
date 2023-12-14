#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Spring {
    Operational,
    Damaged,
}

impl Spring {
    pub fn new_from_char(c: &char) -> Result<Spring, Box<dyn std::error::Error>> {
        match c {
            '.' => Ok(Spring::Operational),
            '#' => Ok(Spring::Damaged),
            _ => Err(format!("Invalid spring character: {}", c).into()),
        }
    }
}

pub struct Row {
    springs: Vec<Spring>,
}

impl Row {
    pub fn damaged_counts(&self) -> Vec<usize> {
        let mut counts = vec![];
        let mut i = 0;
        while i < self.springs.len() {
            let mut spring = self.springs[i];
            let mut counter = 0;
            while spring == Spring::Damaged {
                counter += 1;
                i += 1;
                if i >= self.springs.len() {
                    break;
                }
                spring = self.springs[i];
            }
            if counter > 0 {
                counts.push(counter);
            }
            i += 1;
        }
        counts
    }
}

#[derive(Debug, Clone)]
pub enum SpringReading {
    Known(Spring),
    Unknown,
}

impl SpringReading {
    pub fn new_from_char(c: &char) -> Result<SpringReading, Box<dyn std::error::Error>> {
        if let Ok(spring) = Spring::new_from_char(c) {
            return Ok(SpringReading::Known(spring));
        }
        match c {
            '?' => Ok(SpringReading::Unknown),
            _ => Err(format!("Invalid spring character: {}", c).into()),
        }
    }
}

#[derive(Debug, Clone)]
pub struct RowReading {
    readings: Vec<SpringReading>,
    damaged_counts: Vec<usize>,
}

impl RowReading {
    pub fn new_from_line(s: &str) -> Result<RowReading, Box<dyn std::error::Error>> {
        let parts = s.split(" ").collect::<Vec<_>>();
        if parts.len() != 2 {
            println!("parts: {:?}", parts);
            return Err(format!("Invalid row reading: {}", s).into());
        }
        let readings = parts[0].chars().map(|c| SpringReading::new_from_char(&c)).collect::<Result<Vec<_>, _>>()?;

        let damaged_counts = parts[1].split(",").map(|s| s.parse::<usize>()).collect::<Result<Vec<_>, _>>()?;
        Ok(RowReading { readings, damaged_counts })
    }

    fn first_unknown(&self) -> Option<usize> {
        for (i, reading) in self.readings.iter().enumerate() {
            if let SpringReading::Unknown = reading {
                return Some(i);
            }
        }
        None
    }

    pub fn to_row(&self) -> Row {
        let springs = self.readings.iter().map(|r| match r {
            SpringReading::Known(spring) => spring.clone(),
            _ => panic!("Cannot convert row reading to row with unknowns"),
        }).collect::<Vec<_>>();
        Row { springs }
    }

    pub fn possibilities(&self) -> Vec<Row> {
        match self.first_unknown() {
            None => {
                let row = self.to_row();
                if row.damaged_counts() == self.damaged_counts {
                    vec![row]
                } else {
                    vec![]
                }
            }
            Some(i) => {
                let mut possibilities = vec![];
                for spring in vec![Spring::Operational, Spring::Damaged] {
                    let mut readings = self.readings.clone();
                    readings[i] = SpringReading::Known(spring);
                    let row_reading = RowReading { readings, damaged_counts: self.damaged_counts.clone() };
                    possibilities.extend(row_reading.possibilities());
                }
                possibilities
            }
        }
    }
}