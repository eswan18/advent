use std::collections::HashSet;
use std::fmt::Display;
use std::slice::Iter;

#[derive(PartialEq, Eq, Debug, Hash, Clone, Copy)]
pub enum Direction {
    Left,
    Right,
    Up,
    Down,
}

impl Direction {
    pub fn opposite(&self) -> Direction {
        match self {
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
        }
    }
}

#[derive(PartialEq, Eq, Clone, Copy)]
pub enum Pipe {
    Vertical,
    Horizontal,
    BendL,
    BendJ,
    Bend7,
    BendF,
}

impl Pipe {
    pub fn all() -> Iter<'static, Pipe> {
        static PIPES: [Pipe; 6] = [
            Pipe::Vertical,
            Pipe::Horizontal,
            Pipe::BendL,
            Pipe::BendJ,
            Pipe::Bend7,
            Pipe::BendF,
        ];
        PIPES.iter()
    }

    pub fn new_from_connections(
        connections: HashSet<&Direction>,
    ) -> Result<Pipe, Box<dyn std::error::Error>> {
        if connections.len() != 2 {
            return Err(format!("Invalid number of connections: {}", connections.len()).into());
        }
        // Find a pipe that has the correct connections.
        for pipe in Pipe::all() {
            let pipe_connections = pipe.connections();
            let pipe_connections_set = pipe_connections.iter().collect::<HashSet<&Direction>>();
            if pipe_connections_set == connections {
                return Ok(*pipe);
            }
        }
        Err(format!("No pipe with connections {:?}", connections).into())
    }

    pub fn new_from_char(c: char) -> Result<Pipe, Box<dyn std::error::Error>> {
        let pipe = match c {
            '|' => Pipe::Vertical,
            '-' => Pipe::Horizontal,
            'L' => Pipe::BendL,
            'J' => Pipe::BendJ,
            '7' => Pipe::Bend7,
            'F' => Pipe::BendF,
            _ => return Err(format!("Invalid pipe character: {}", c).into()),
        };
        Ok(pipe)
    }

    #[allow(dead_code)]
    pub fn chars() -> Vec<char> {
        return vec!['|', '-', 'L', 'J', '7', 'F'];
    }

    pub fn connections(&self) -> Vec<Direction> {
        match self {
            Pipe::Vertical => vec![Direction::Up, Direction::Down],
            Pipe::Horizontal => vec![Direction::Left, Direction::Right],
            Pipe::BendL => vec![Direction::Up, Direction::Right],
            Pipe::BendJ => vec![Direction::Up, Direction::Left],
            Pipe::Bend7 => vec![Direction::Down, Direction::Left],
            Pipe::BendF => vec![Direction::Down, Direction::Right],
        }
    }

    pub fn next_direction(&self, from: Direction) -> Direction {
        let connections = self.connections();
        // Every pipe has only two connections, so whichever direction we didn't come from is the new direction.
        for connection in connections {
            if connection != from {
                return connection;
            }
        }
        unreachable!("Pipe has no connections")
    }
}

impl Display for Pipe {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let c = match self {
            Pipe::Vertical => '|',
            Pipe::Horizontal => '-',
            Pipe::BendL => '└',
            Pipe::BendJ => '┘',
            Pipe::Bend7 => '┐',
            Pipe::BendF => '┌',
        };
        write!(f, "{}", c)
    }
}
