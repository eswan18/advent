#[derive(Debug)]
pub struct Draw {
    pub red: i32,
    pub green: i32,
    pub blue: i32,
}

impl Draw {
    pub fn new_from_str(s: &str) -> Draw {
        // Split the string on commas
        let split = s.split(", ");
        let mut red = 0;
        let mut green = 0;
        let mut blue = 0;
        // Loop over the split string
        for s in split {
            let parts = s.split(" ").collect::<Vec<&str>>();
            match parts[1] {
                "red" => red = parts[0].parse::<i32>().unwrap(),
                "green" => green = parts[0].parse::<i32>().unwrap(),
                "blue" => blue = parts[0].parse::<i32>().unwrap(),
                _ => panic!("Invalid color"),
            }
        }
        Draw { red, green, blue }
    }

    pub fn possible_from_draw(&self, draw: &Draw) -> bool {
        self.red <= draw.red && self.green <= draw.green && self.blue <= draw.blue
    }
}