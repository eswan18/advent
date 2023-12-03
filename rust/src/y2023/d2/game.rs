use super::draw::Draw;

#[derive(Debug)]
pub struct Game {
    pub id: u32,
    draws: Vec<Draw>,
}

impl Game {
    pub fn new_from_line(line: &str) -> Game {
        let parts = line.split(": ").collect::<Vec<&str>>();
        let id = parts[0].split(' ').collect::<Vec<&str>>()[1]
            .parse::<u32>()
            .unwrap();
        let draws = parts[1]
            .split("; ")
            .map(|s| Draw::new_from_str(s))
            .collect::<Vec<Draw>>();
        Game { id, draws }
    }

    pub fn possible_from_draw(&self, draw: &Draw) -> bool {
        self.draws.iter().all(|d| d.possible_from_draw(draw))
    }

    fn minimal_draw(&self) -> Draw {
        let mut red = 0;
        let mut green = 0;
        let mut blue = 0;
        for draw in &self.draws {
            red = std::cmp::max(red, draw.red);
            green = std::cmp::max(green, draw.green);
            blue = std::cmp::max(blue, draw.blue);
        }
        Draw { red, green, blue }
    }

    pub fn power_of_minimal_draw(&self) -> i32 {
        let minimal_draw = self.minimal_draw();
        minimal_draw.red * minimal_draw.green * minimal_draw.blue
    }
}
