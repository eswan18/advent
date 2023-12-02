use super::draw::Draw;

#[derive(Debug)]
pub struct Game {
    pub id: u32,
    draws: Vec<Draw>,
}

impl Game {
    pub fn new_from_line(line: &str) -> Game {
        let parts = line.split(": ").collect::<Vec<&str>>();
        let id = parts[0].split(' ').collect::<Vec<&str>>()[1].parse::<u32>().unwrap();
        let draws = parts[1].split("; ").map(|s| Draw::new_from_str(s)).collect::<Vec<Draw>>();
        Game { id, draws }
    }

    pub fn possible_from_draw(&self, draw: &Draw) -> bool {
        self.draws.iter().all(|d| d.possible_from_draw(draw))
    }
}