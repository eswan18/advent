use indexmap::IndexMap;
use std::{collections::HashMap, fmt::Display};

use crate::y2023::d15::hash::hash;

#[derive(Debug)]
pub struct LensBoxContainer {
    boxes: HashMap<u32, LensBox>,
}

impl Display for LensBoxContainer {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut s = String::new();
        let mut box_nums = self.boxes.keys().collect::<Vec<_>>();
        box_nums.sort();
        for box_num in box_nums {
            let box_ = self.boxes.get(box_num).unwrap();
            if box_.empty() {
                continue;
            }
            s.push_str(&format!("Box {}: ", box_num));
            s.push_str(&format!("{}\n", box_));
        }
        write!(f, "{}", s)
    }
}

impl LensBoxContainer {
    pub fn new() -> Self {
        Self {
            boxes: HashMap::new(),
        }
    }

    pub fn execute(&mut self, i: &Instruction) {
        let box_num = i.box_num();
        match i {
            Instruction::SET { label, value } => {
                let box_ = match self.boxes.get_mut(&box_num) {
                    Some(box_) => box_,
                    None => {
                        let box_ = LensBox::new();
                        self.boxes.insert(box_num, box_);
                        self.boxes.get_mut(&box_num).unwrap()
                    }
                };
                box_.set(label.to_string(), *value)
            }
            Instruction::REMOVE { label } => match self.boxes.get_mut(&box_num) {
                Some(box_) => box_.remove(label),
                None => {}
            },
        }
    }

    pub fn focal_power(&self) -> u32 {
        let mut total = 0;
        for (box_num, box_) in &self.boxes {
            for (slot_num, focal_length) in box_.lenses.values().enumerate() {
                total += (box_num + 1) * (slot_num as u32 + 1) * (*focal_length as u32)
            }
        }
        total
    }
}

#[derive(Debug)]
struct LensBox {
    lenses: IndexMap<String, u32>,
}

impl Display for LensBox {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut s = String::new();
        for (label, value) in &self.lenses {
            s.push_str(&format!("[{} {}] ", label, value));
        }
        write!(f, "{}", s)
    }
}

impl LensBox {
    fn new() -> Self {
        Self {
            lenses: IndexMap::new(),
        }
    }

    fn set(&mut self, label: String, value: u32) {
        self.lenses.insert(label, value);
    }

    fn remove(&mut self, label: &str) {
        self.lenses.shift_remove(label);
    }

    fn empty(&self) -> bool {
        self.lenses.is_empty()
    }
}

pub enum Instruction {
    SET { label: String, value: u32 },
    REMOVE { label: String },
}

impl Display for Instruction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Instruction::SET { label, value } => write!(f, "{}={}", label, value),
            Instruction::REMOVE { label } => write!(f, "{}-", label),
        }
    }
}

impl Instruction {
    pub fn box_num(&self) -> u32 {
        match self {
            Instruction::SET { label, value: _ } => hash(label),
            Instruction::REMOVE { label } => hash(label),
        }
    }

    pub fn new_from_str(s: &str) -> Result<Instruction, Box<dyn std::error::Error>> {
        let parts = s.split("=").collect::<Vec<_>>();
        if parts.len() == 1 {
            let label = match s.strip_suffix("-") {
                Some(s) => s,
                None => return Err("Invalid label".into()),
            };
            return Ok(Instruction::REMOVE {
                label: label.to_string(),
            });
        }
        if parts.len() == 2 {
            let label = parts[0];
            let value = parts[1].parse::<u32>()?;
            return Ok(Instruction::SET {
                label: label.to_string(),
                value,
            });
        }
        Err("Invalid instruction".into())
    }
}
