use std::{collections::HashMap, fmt::Display};

pub enum Instruction {
    R,
    L,
}

impl Instruction {
    pub fn new_vec_from_line(line: &str) -> Result<Vec<Instruction>, Box<dyn std::error::Error>> {
        line.chars()
            .map(|c| match c {
                'R' => Ok(Instruction::R),
                'L' => Ok(Instruction::L),
                _ => Err(format!("Invalid instruction: {}", c).into()),
            })
            .collect::<Result<_, _>>()
    }
}

impl Display for Instruction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Instruction::R => write!(f, "R"),
            Instruction::L => write!(f, "L"),
        }
    }
}

#[derive(Clone)]
pub struct Node {
    name: String,
    left: String,
    right: String,
}

impl Display for Node {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} = ({}, {})", self.name, self.right, self.left)
    }
}

impl Node {
    pub fn new_from_line(line: &str) -> Result<Node, Box<dyn std::error::Error>> {
        // a node line looks like 'AAA = (BBB, CCC)'
        let mut parts = line.split(" = ");
        let name = parts
            .next()
            .ok_or(format!("Invalid node line: '{}'", line))?;
        let mut parts = parts
            .next()
            .ok_or(format!("Invalid node line: '{}'", line))?
            .split(", ");
        let left = parts
            .next()
            .ok_or("Invalid node line")?
            .strip_prefix("(")
            .ok_or("missing paren")?;
        let right = parts
            .next()
            .ok_or("Invalid node line")?
            .strip_suffix(")")
            .ok_or("missing paren")?;
        Ok(Node {
            name: name.to_string(),
            left: left.to_string(),
            right: right.to_string(),
        })
    }
}

pub struct Map {
    instructions: Vec<Instruction>,
    nodes: HashMap<String, Node>,
}

impl Map {
    pub fn new_from_text(text: &str) -> Result<Map, Box<dyn std::error::Error>> {
        let lines = text.lines().collect::<Vec<_>>();

        let instructions = Instruction::new_vec_from_line(lines[0])?;
        let nodes: Vec<Node> = lines[2..]
            .iter()
            .map(|line| Node::new_from_line(line))
            .collect::<Result<_, _>>()?;
        let node_map = nodes
            .into_iter()
            .map(|node| (node.name.clone(), node.clone()))
            .collect::<HashMap<_, _>>();
        Ok(Map {
            instructions,
            nodes: node_map,
        })
    }

    // Traverse until hitting ZZZ and return the number of steps taken.
    pub fn traverse(&self) -> Result<i32, Box<dyn std::error::Error>> {
        let mut state = GameState {
            current_node: "AAA".to_string(),
            steps: 0,
        };
        while state.current_node != "ZZZ" {
            let node = self.nodes.get(&state.current_node).ok_or("Invalid node")?;
            let instr_idx = state.steps as usize % self.instructions.len();
            let instruction = self
                .instructions
                .get(instr_idx)
                .ok_or("Invalid instruction")?;
            match instruction {
                Instruction::R => state.current_node = node.right.clone(),
                Instruction::L => state.current_node = node.left.clone(),
            }
            state.steps += 1;
        }
        Ok(state.steps)
    }
}

struct GameState {
    current_node: String,
    steps: i32,
}

impl Display for Map {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for instruction in &self.instructions {
            write!(f, "{}", instruction)?;
        }
        write!(f, "\n")?;
        for node in self.nodes.values() {
            write!(f, "{}\n", node)?;
        }
        Ok(())
    }
}
