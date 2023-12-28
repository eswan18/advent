use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::{Rc, Weak};

use super::contraption::{Contraption, Direction, Point, PointWithDirection};

pub struct Beam {
    at: PointWithDirection,
    parent: Option<Weak<RefCell<Beam>>>,
    children: Vec<Rc<RefCell<Beam>>>,
}

impl Beam {
    pub fn new(at: PointWithDirection) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Self {
            at,
            parent: None,
            children: Vec::new(),
        }))
    }

    // Function to add a child, taking Rc<RefCell<Beam>> for both parent and child
    fn add_child(parent: &Rc<RefCell<Beam>>, child: Rc<RefCell<Beam>>) {
        let mut parent_borrow = parent.borrow_mut();
        let mut child_borrow = child.borrow_mut();

        // Set the parent of the child as a weak reference to the parent
        child_borrow.parent = Some(Rc::downgrade(parent));

        // Add the child to the children of the parent
        parent_borrow.children.push(child.clone());
    }

    fn next_points(&self, contraption: &Contraption) -> Vec<PointWithDirection> {
        let space = match contraption.at(&self.at.point) {
            Some(space) => space,
            None => return Vec::new(),
        };
        let next_points = space.next_points(&self.at.point, &self.at.direction);
        // Trim off the points that are outside the contraption.
        let (width, height) = contraption.dimensions();
        let width = width as i32;
        let height = height as i32;
        next_points
            .into_iter()
            .filter(|point_with_direction| {
                point_with_direction.point.x < width
                    && point_with_direction.point.y < height
                    && point_with_direction.point.x >= 0
                    && point_with_direction.point.y >= 0
            })
            .collect::<Vec<_>>()
    }

    pub fn add_next_children(parent: &Rc<RefCell<Beam>>, contraption: &Contraption, exclude: &HashSet<PointWithDirection>) -> Vec<PointWithDirection> {
        let next_points = parent.borrow().next_points(contraption).into_iter().filter(|point_with_direction| !exclude.contains(point_with_direction)).collect::<Vec<_>>();
        next_points.iter().for_each(|point_with_direction| {
            let child = Self::new(point_with_direction.clone());
            Self::add_child(&parent, child.clone());
        });
        next_points
    }

    fn all_points(&self) -> HashSet<PointWithDirection> {
        let mut points = HashSet::new();
        points.insert(self.at.clone());
        for child in self.children.iter() {
            let child_borrow = child.borrow();
            let child_points = child_borrow.all_points();
            points.extend(child_points);
        }
        points
    }

    pub fn visualize(&self, contraption: &Contraption) -> String {
        let mut s = String::new();
        let points_with_directions: HashMap<Point, Direction> = self
            .all_points()
            .iter()
            .map(|point_with_direction| {
                (
                    point_with_direction.point.clone(),
                    point_with_direction.direction.clone(),
                )
            })
            .collect();
        let (width, height) = contraption.dimensions();
        for y in 0..height as i32 {
            for x in 0..width as i32 {
                let c = match points_with_directions.get(&Point { x, y }) {
                    Some(Direction::Up) => '^',
                    Some(Direction::Down) => 'v',
                    Some(Direction::Left) => '<',
                    Some(Direction::Right) => '>',
                    None => contraption.display_at(&Point { x, y }),
                };
                s.push(c);
            }
            s.push('\n');
        }
        s
    }

    // Helper method to find all leaf nodes
    fn leaf_nodes(node: &Rc<RefCell<Beam>>, leaves: &mut Vec<Rc<RefCell<Beam>>>) {
        let node_borrow = node.borrow();
        if node_borrow.children.is_empty() {
            leaves.push(node.clone());
        } else {
            for child in node_borrow.children.iter() {
                Self::leaf_nodes(child, leaves);
            }
        }
    }
}

pub struct BeamState {
    root: Rc<RefCell<Beam>>,
    contraption: Contraption,
    seen: HashSet<PointWithDirection>,
}

impl BeamState {
    pub fn new(contraption: Contraption, at: PointWithDirection) -> Self {
        let root = Beam::new(at);
        let seen = HashSet::new();
        Self { root, contraption, seen }
    }

    #[allow(dead_code)]
    pub fn visualize(&self) -> String {
        self.root.borrow().visualize(&self.contraption)
    }

    // Method to add children to all leaf nodes
    // Returns true if any children were added
    pub fn step(&mut self) -> bool {
        let mut leaves = Vec::new();
        Beam::leaf_nodes(&self.root, &mut leaves);

        let mut found_children = false;
        for leaf in leaves {
            let new_points = Beam::add_next_children(&leaf, &self.contraption, &self.seen);
            if !new_points.is_empty() {
                found_children = true;
            }
            self.seen.extend(new_points);
        }
        found_children
    }

    pub fn energized_count(&self) -> usize {
        self.root
            .borrow()
            .all_points()
            .iter()
            .map(|point_with_direction| point_with_direction.point.clone())
            .collect::<HashSet<_>>()
            .len()
    }
}
