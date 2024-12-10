import itertools
from typing import Optional


def parse_grid(filename: str) -> list[list[str]]:
    """
    Parse the input into 2d grid
    """
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid


def find_trail_heads(grid: list[list[str]]) -> list[tuple[int, int]]:
    """
    Find the coordinates of all obstacles in the grid and the starting position of the guard
    """
    trail_heads = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '0':
                trail_heads.append((row, col))

    return trail_heads


def find_valid_neighbors(grid: list[list[str]], curr_row: int, curr_col: int, curr_val: int) -> list[tuple[int, int]]:
    """
    Find neighboring one step up elevation points
    """
    direction_adders = {'N': (1, 0), 'S': (-1, 0), 'E': (0, -1), 'W': (0, 1)}
    valid_neighbors = []
    for direction, (row_adder, col_adder) in direction_adders.items():
        neighbor_row, neighbor_col = curr_row + row_adder, curr_col + col_adder
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # In bounds
            neighbor_value = grid[neighbor_row][neighbor_col]
            if neighbor_value.isdigit() and int(neighbor_value) == curr_val + 1:  # Next elevation point
                valid_neighbors.append((neighbor_row, neighbor_col))

    return valid_neighbors


def find_unique_trail_ends(grid: list[list[str]], curr_row: int, curr_col: int) -> Optional[set[tuple[int, int]]]:
    """
    Identify whether we can travel through to the end of a hiking trail, one height step at a time
    """
    curr_val = int(grid[curr_row][curr_col])
    valid_neighbors = find_valid_neighbors(grid=grid, curr_row=curr_row, curr_col=curr_col, curr_val=curr_val)

    if curr_val == 9:  # End of path
        return {(curr_row, curr_col)}

    if len(valid_neighbors) == 0:  # No path found
        return None

    all_trail_ends = set()
    for neighbor_row, neighbor_col in valid_neighbors:
        trail_ends = find_unique_trail_ends(grid=grid, curr_row=neighbor_row, curr_col=neighbor_col)
        if trail_ends:
            trail_ends = [coord for coord in trail_ends if coord is not None]
            all_trail_ends = all_trail_ends.union(trail_ends)

    return all_trail_ends


def part1(grid: list[list[str]]) -> int:
    """
    Sum up the scores of all trailheads
    """
    trail_heads = find_trail_heads(grid=grid)

    total_score = 0
    for start_row, start_col in trail_heads:
        score = len(find_unique_trail_ends(grid=grid, curr_row=start_row, curr_col=start_col))
        total_score += score

    return total_score


def find_ratings(grid: list[list[str]], curr_row: int, curr_col: int) -> int:
    """
    Identify how many distinct hiking trail ends we can reach
    """
    curr_val = int(grid[curr_row][curr_col])

    if curr_val == 9:  # End of path
        return 1

    valid_neighbors = find_valid_neighbors(grid=grid, curr_row=curr_row, curr_col=curr_col, curr_val=curr_val)
    if len(valid_neighbors) == 0:  # No path found
        return 0

    total_rating = 0
    for neighbor_row, neighbor_col in valid_neighbors:
        total_rating += find_ratings(grid=grid, curr_row=neighbor_row, curr_col=neighbor_col)

    return total_rating


def part2(grid: list[list[str]]) -> int:
    """
    Sum up the scores of all trailheads
    """
    trail_heads = find_trail_heads(grid=grid)

    total_rating = 0
    for start_row, start_col in trail_heads:
        total_rating += find_ratings(grid=grid, curr_row=start_row, curr_col=start_col)

    return total_rating


if __name__ == '__main__':
    grid = parse_grid('data/day10.txt')

    part_1 = part1(grid=grid)
    print(f'part 1: {part_1}')

    part_2 = part2(grid=grid)
    print(f'part 2: {part_2}')