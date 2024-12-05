def a(input: str) -> str:
    grid = [[c for c in line.strip()] for line in input.split()]
    found = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'X':
                found += find_horizontal(grid, x, y)
                found += find_vertical(grid, x, y)
                found += find_diagonal(grid, x, y)
    return str(found)

def find_horizontal(grid: list[list[str]], x: int, y: int) -> int:
    # Only check to the left if there's enough room.
    count = 0
    if x - 3 >= 0:
        if grid[y][x-1] == 'M' and grid[y][x-2] == 'A' and grid[y][x-3]== 'S':
            count += 1
    # Only check to the right if there's enough room.
    if x + 3 < len(grid):
        if grid[y][x+1] == 'M' and grid[y][x+2] == 'A' and grid[y][x+3] == 'S':
            count += 1
    return count

def find_vertical(grid: list[list[str]], x: int, y: int) -> int:
    # Only check above if there's enough room.
    count = 0
    if y - 3 >= 0:
        if grid[y-1][x] == 'M' and grid[y-2][x] == 'A' and grid[y-3][x] == 'S':
            count += 1
    # Only check below if there's enough room.
    if y + 3 < len(grid):
        if grid[y+1][x] == 'M' and grid[y+2][x] == 'A' and grid[y+3][x] == 'S':
            count += 1
    return count

def find_diagonal(grid: list[list[str]], x: int, y: int) -> int:
    # Only check up-left if there's enough room.
    count = 0
    if x - 3 >= 0 and y - 3 >= 0:
        if grid[y-1][x-1] == 'M' and grid[y-2][x-2] == 'A' and grid[y-3][x-3] == 'S':
            count += 1
    # Only check up-right if there's enough room.
    if x + 3 < len(grid) and y - 3 >= 0:
        if grid[y-1][x+1] == 'M' and grid[y-2][x+2] == 'A' and grid[y-3][x+3] == 'S':
            count += 1
    # Only check down-left if there's enough room.
    if x - 3 >= 0 and y + 3 < len(grid):
        if grid[y+1][x-1] == 'M' and grid[y+2][x-2] == 'A' and grid[y+3][x-3] == 'S':
            count += 1
    # Only check down-right if there's enough room.
    if x + 3 < len(grid) and y + 3 < len(grid):
        if grid[y+1][x+1] == 'M' and grid[y+2][x+2] == 'A' and grid[y+3][x+3] == 'S':
            count += 1
    return count