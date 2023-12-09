pub struct History {
    values: Vec<i32>,
}

impl History {
    pub fn new_from_line(line: &str) -> Result<History, Box<dyn std::error::Error>> {
        let values = line.split(" ").map(|s| s.parse::<i32>()).collect::<Result<Vec<_>, _>>()?;
        Ok(History {
            values,
        })
    }

    pub fn find_next(&self) -> Result<i32, Box<dyn std::error::Error>> {
        if self.values.is_empty() {
            return Err("History values are empty".into());
        }

        let mut delta_lines: Vec<Vec<i32>> = Vec::new();
        let mut deltas = self.values.clone();

        // Build out the deltas until they are all equal (the step before they're all 0).
        while deltas.len() > 1 {
            deltas = deltas.windows(2).map(|w| w[1] - w[0]).collect();
            delta_lines.push(deltas.clone());

            if deltas.iter().all(|&x| x == deltas[0]) {
                break;
            }
        }

        if delta_lines.is_empty() {
            return Err("No delta lines were generated".into());
        }

        // Now work backwards to find the next value for each list of deltas.
        while delta_lines.len() > 1 {
            let deltas = delta_lines.pop().ok_or("Failed to pop from delta_lines")?;
            let last_value_in_previous = *delta_lines.last_mut()
                .ok_or("No last element in delta_lines")?
                .last().ok_or("No last element in last delta_lines")?;
            let last_delta = *deltas.last().ok_or("No last delta value")?;
            let next_value = last_value_in_previous + last_delta;
            delta_lines.last_mut().unwrap().push(next_value);  // Safe unwrap as we just checked it
        }

        let last_values_delta = delta_lines[0].last().ok_or("No last value in deltas")?;
        Ok(*self.values.last().unwrap() + *last_values_delta)  // Safe unwrap as we checked values is not empty
    }

    pub fn find_previous(&self) -> Result<i32, Box<dyn std::error::Error>> {
        if self.values.is_empty() {
            return Err("History values are empty".into());
        }

        let mut delta_lines: Vec<Vec<i32>> = Vec::new();
        let mut deltas = self.values.clone();

        // Build out the deltas until they are all equal (the step before they're all 0).
        while deltas.len() > 1 {
            deltas = deltas.windows(2).map(|w| w[1] - w[0]).collect();
            delta_lines.push(deltas.clone());

            if deltas.iter().all(|&x| x == deltas[0]) {
                break;
            }
        }

        if delta_lines.is_empty() {
            return Err("No delta lines were generated".into());
        }

        // Now work backwards to find the previous value for each list of deltas.
        while delta_lines.len() > 1 {
            let deltas = delta_lines.pop().ok_or("Failed to pop from delta_lines")?;
            let first_value_in_previous = *delta_lines.last_mut()
                .ok_or("No last element in delta_lines")?
                .first().ok_or("No first element in last delta_lines")?;
            let first_delta = *deltas.first().ok_or("No first delta value")?;
            let prev_value = first_value_in_previous - first_delta;
            delta_lines.last_mut().unwrap().insert(0, prev_value);  // Safe unwrap as we just checked it
        }

        let first_values_delta = delta_lines[0].first().ok_or("No first value in deltas")?;
        Ok(*self.values.first().unwrap() - *first_values_delta)  // Safe unwrap as we checked values is not empty
    }
}