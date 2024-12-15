from .robot import RobotGrid


def a(input: str) -> str:
    # grid = RobotGrid.from_str(input, 11, 7) # For test input
    grid = RobotGrid.from_str(input, 101, 103) # For real input
    grid.iterate_n_seconds(100)
    return str(grid.safety_factor())