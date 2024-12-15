from time import sleep

from .robot import RobotGrid


def b(input: str) -> str:
    grid = RobotGrid.from_str(input, 101, 103)  # For real input
    steps = 1
    grid.iterate_n_seconds(steps)
    while True:
        steps += 1
        grid.iterate_n_seconds(1)
        if grid.is_symmetric():
            print(grid)
            sleep(0.5)
            print(steps)
    return ''