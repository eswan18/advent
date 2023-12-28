use std::collections::HashMap;

use crate::y2023::d19::part::{Field, Part, Range};

type Rulename = String;

#[derive(Debug, Clone)]
enum Destination {
    Rule(Rulename),
    Accept,
    Reject,
}

#[derive(Debug)]
pub struct Test {
    field: Field,
    threshold: u64,
    is_gt: bool,
    destination: Destination,
}

impl Test {
    pub fn new_from_str(s: &str) -> Result<Test, Box<dyn std::error::Error>> {
        // Input strings look like "s<1351:px". "px" is the destination, 1351 is the threshold, and "s" is the field.
        let parts = s.split(":").collect::<Vec<&str>>();
        if parts.len() != 2 {
            return Err("Not enough parts".into());
        }
        let dest = match parts[1] {
            "A" => Destination::Accept,
            "R" => Destination::Reject,
            s => Destination::Rule(s.to_string()),
        };

        let test = parts[0];
        if test.contains(">") {
            let parts = test.split(">").collect::<Vec<&str>>();
            if parts.len() != 2 {
                return Err("Not enough parts".into());
            }
            let field = Field::from_str(parts[0])?;
            let threshold = parts[1].parse::<u64>()?;
            Ok(Test {
                field,
                threshold,
                is_gt: true,
                destination: dest,
            })
        } else if test.contains("<") {
            let parts = test.split("<").collect::<Vec<&str>>();
            if parts.len() != 2 {
                return Err("Not enough parts".into());
            }
            let field = Field::from_str(parts[0])?;
            let threshold = parts[1].parse::<u64>()?;
            Ok(Test {
                field,
                threshold,
                is_gt: false,
                destination: dest,
            })
        } else {
            Err("No comparison operator".into())
        }
    }

    pub fn test(&self, part: &Part) -> bool {
        let val = part.get(&self.field);
        if self.is_gt {
            val > self.threshold
        } else {
            val < self.threshold
        }
    }
}

#[derive(Debug)]
pub struct Rule {
    name: Rulename,
    tests: Vec<Test>,
    fallback: Destination,
}

impl Rule {
    pub fn new_from_line(line: &str) -> Result<Rule, Box<dyn std::error::Error>> {
        // Input lines look like "in{s<1351:px,qqz}"
        let parts = line.split("{").collect::<Vec<&str>>();
        if parts.len() != 2 {
            return Err("Not enough parts".into());
        }
        let name: Rulename = parts[0].to_string();
        let tests_etc = parts[1].strip_suffix("}").ok_or("No closing brace")?;
        let test_parts = tests_etc.split(",").collect::<Vec<&str>>();
        let tests = test_parts[0..test_parts.len() - 1]
            .iter()
            .map(|s| Test::new_from_str(s))
            .collect::<Result<Vec<Test>, Box<dyn std::error::Error>>>()?;
        let fallback = match test_parts.last() {
            Some(&"A") => Destination::Accept,
            Some(&"R") => Destination::Reject,
            Some(c) => Destination::Rule(c.to_string()),
            _ => return Err("No fallback".into()),
        };
        Ok(Rule {
            name,
            tests,
            fallback,
        })
    }

    pub fn test(&self, part: &Part) -> Destination {
        for test in &self.tests {
            if test.test(part) {
                return test.destination.clone();
            }
        }
        self.fallback.clone()
    }
}

pub struct Ruleset {
    rules: HashMap<Rulename, Rule>,
}

impl Ruleset {
    pub fn new_from_str(lines: &str) -> Result<Ruleset, Box<dyn std::error::Error>> {
        let mut rules = HashMap::new();
        for line in lines.lines() {
            let rule = Rule::new_from_line(line)?;
            let name = rule.name.clone();
            rules.insert(name, rule);
        }
        Ok(Ruleset { rules })
    }

    pub fn test(&self, part: &Part) -> Result<bool, Box<dyn std::error::Error>> {
        let mut rule = self.rules.get("in").ok_or("no starting rule")?;
        loop {
            let dest = rule.test(part);
            match dest {
                Destination::Rule(name) => {
                    rule = self.rules.get(&name).ok_or("no rule")?;
                }
                Destination::Accept => return Ok(true),
                Destination::Reject => return Ok(false),
            }
        }
    }

    fn all_tests(&self) -> Vec<&Test> {
        let mut tests = Vec::new();
        for rule in self.rules.values() {
            tests.extend(rule.tests.iter());
        }
        tests
    }

    // All the ranges that resolve to the same answer.
    pub fn ranges(&self) -> HashMap<Field, Vec<Range>> {
        let mut ranges: HashMap<Field, Vec<Range>> = HashMap::new();
        let all_tests = self.all_tests();
        for field in Field::all() {
            let mut field_ranges: Vec<Range> = Vec::new();
            // Get all tests for this field.
            let mut tests: Vec<&&Test> = all_tests.iter().filter(|t| t.field == field).collect();
            // Sort them by threshold, then by whether they're greater than or less than.
            tests.sort_by(|a, b| {
                let cmp = a.threshold.cmp(&b.threshold);
                if cmp == std::cmp::Ordering::Equal {
                    a.is_gt.cmp(&b.is_gt)
                } else {
                    cmp
                }
            });
            for t in tests {
                // Start at 1, or 1 after the last range's end.
                let start = match field_ranges.last() {
                    Some(r) => r.end + 1,
                    None => 1,
                };
                // End at the threshold. Account for differences in whether the threshold is inclusive.
                let end = match t.is_gt {
                    true => t.threshold,
                    false => t.threshold - 1,
                };
                if end < start {
                    continue;
                }
                field_ranges.push(Range { start, end });
            }
            // Add one final range to get us to 4000.
            let last_range = field_ranges.last().unwrap();
            if last_range.end < 4000 {
                field_ranges.push(Range {
                    start: last_range.end + 1,
                    end: 4000,
                });
            }
            ranges.insert(field, field_ranges);
        }
        ranges
    }
}
