import re
import math


def parse_grid(filename: str) -> list[list[int]]:
    """
    Parse the input into 2d grid
    """
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid

def find_letter_coords(grid: list[list[str]], letter: str) -> list[tuple[int, int]]:
    """
    Find the coordinates of all X values
    """
    coords = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == letter:
                coords.append((row, col))

    return coords

def find_next_coords(row: int, col: int, direction: str) -> tuple[int, int]:
    """
    Identify the coordinates after moving in the provided direction
    """
    if direction == 'N':
        return row - 1, col
    if direction == 'S':
        return row + 1, col
    if direction == 'E':
        return row, col + 1
    if direction == 'W':
        return row, col - 1
    if direction == 'NE':
        return row - 1, col + 1
    if direction == 'SE':
        return row + 1, col + 1
    if direction == 'SW':
        return row + 1, col - 1
    if direction == 'NW':
        return row - 1, col - 1

def in_bounds(row: int, col: int, max_row: int, max_col: int) -> bool:
    return 0 <= row <= max_row and 0 <= col <= max_col

def xmas_found(grid: list[list[str]], max_row: int, max_col: int,
               prior_letter: str, search_row: int, search_col: int, direction: str) -> bool:
    """
    Recursively iterate on the grid and identify if XMAS has been found
    """
    if not in_bounds(search_row, search_col, max_row, max_col):  # Out of bounds
        return False

    allowed_letter_pairs = [('X', 'M'), ('M', 'A'), ('A', 'S')]
    current_letter = grid[search_row][search_col]
    if (prior_letter, current_letter) in allowed_letter_pairs:
        if current_letter == 'S':  # XMAS found
            return True
        else:  # Keep searching
            next_row, next_col = find_next_coords(search_row, search_col, direction)
            return xmas_found(grid, max_row, max_col, current_letter, next_row, next_col, direction)
    else:  # XMAS not possible
        return False

def count_xmas(grid: list[list[str]]) -> int:
    """
    Count XMAS in the grid
    """
    xmas_count = 0
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    x_coords = find_letter_coords(grid, 'X')

    for row, col in x_coords:
        for direction in ['N', 'S', 'E', 'W', 'NE', 'SE', 'SW', 'NW']:
            next_row, next_col = find_next_coords(row, col, direction)
            xmas_count += xmas_found(grid, max_row, max_col, 'X', next_row, next_col, direction)

    return xmas_count

def count_x_mas(grid: list[list[str]]) -> int:
    """
    Count X-MAS in the grid
    """
    x_mas_count = 0
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    a_coords = find_letter_coords(grid, 'A')

    diagonal_directions = {'NE', 'SE', 'SW', 'NW'}
    for row, col in a_coords:
        diagonal_vals = {}
        for direction in diagonal_directions:
            diagonal_row, diagonal_col = find_next_coords(row, col, direction)
            if not in_bounds(diagonal_row, diagonal_col, max_row, max_col):
                break
            else:
                diagonal_vals[direction] = grid[diagonal_row][diagonal_col]

        if (diagonal_vals.keys() == diagonal_directions
                and {diagonal_vals['NE'], diagonal_vals['SW']} == {'M', 'S'}
                and {diagonal_vals['NW'], diagonal_vals['SE']} == {'M', 'S'}):
            x_mas_count += 1

    return x_mas_count

if __name__ == '__main__':
    grid = parse_grid('data/day4.txt')

    part_1 = count_xmas(grid)
    print(f'part 1: {part_1}')

    part_2 = count_x_mas(grid)
    print(f'part 2: {part_2}')

