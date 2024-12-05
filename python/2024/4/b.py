def b(input: str) -> str:
    grid = [[c for c in line.strip()] for line in input.split()]
    found = 0
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[0])-1):
            if grid[y][x] == 'A':
                has_pos_slope_mas = False
                has_neg_slope_mas = False
                if grid[y-1][x-1] == 'M' and grid[y+1][x+1] == 'S':
                    has_pos_slope_mas = True
                if grid[y-1][x-1] == 'S' and grid[y+1][x+1] == 'M':
                    has_pos_slope_mas = True
                if grid[y-1][x+1] == 'M' and grid[y+1][x-1] == 'S':
                    has_neg_slope_mas = True
                if grid[y-1][x+1] == 'S' and grid[y+1][x-1] == 'M':
                    has_neg_slope_mas = True
                if has_pos_slope_mas and has_neg_slope_mas:
                    found += 1
    return str(found)
