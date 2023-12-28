use std::cell::RefCell;
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

    pub fn add_next_children(parent: &Rc<RefCell<Beam>>, contraption: &Contraption) {
        let next_points = parent.borrow().next_points(contraption);
        let children = next_points
            .iter()
            .map(|point_with_direction| {
                let child = Self::new(point_with_direction.clone());
                Self::add_child(&parent, child.clone());
                child
            })
            .collect::<Vec<_>>();
    }
}
