import time
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


def find_obstacles_and_starting_position(grid: list[list[str]]) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    """
    Find the coordinates of all obstacles in the grid and the starting position of the guard
    """
    obstacles = []
    starting_position = None
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '#':
                obstacles.append((row, col))
            elif grid[row][col] == '^':
                starting_position = (row, col)

    return obstacles, starting_position


def find_next_obstacle(current_row: int, current_col: int, current_direction: str,
                       obstacles: [list[tuple[int, int]]]) -> tuple[int, int]:
    """
    Find the next obstacle in the current direction
    """
    next_obstacle = None
    for obstacle_row, obstacle_col in obstacles:
        if current_direction in ['N', 'S'] and obstacle_col == current_col:
            if current_direction == 'N' and obstacle_row < current_row:
                if next_obstacle is None:
                    next_obstacle = (obstacle_row, obstacle_col)
                else:  # Closest obstacle in column
                    next_obstacle = max(next_obstacle[0], obstacle_row), obstacle_col
            elif current_direction == 'S' and obstacle_row > current_row:
                if next_obstacle is None:
                    next_obstacle = (obstacle_row, obstacle_col)
                else:  # Closest obstacle in column
                    next_obstacle = min(next_obstacle[0], obstacle_row), obstacle_col
        elif current_direction in ['E', 'W'] and obstacle_row == current_row:
            if current_direction == 'E' and obstacle_col > current_col:
                if next_obstacle is None:
                    next_obstacle = (obstacle_row, obstacle_col)
                else:  # Closest obstacle in row
                    next_obstacle = obstacle_row, min(next_obstacle[1], obstacle_col)
            elif current_direction == 'W' and obstacle_col < current_col:
                if next_obstacle is None:
                    next_obstacle = (obstacle_row, obstacle_col)
                else:  # Closest obstacle in row
                    next_obstacle = obstacle_row, max(next_obstacle[1], obstacle_col)

    return next_obstacle


def find_next_position(next_obstacle_row: int, next_obstacle_col: int, current_direction: str) -> tuple[int, int]:
    """
    Find the position after moving up to the next obstacle
    """
    if current_direction == 'N':
        return next_obstacle_row + 1, next_obstacle_col
    elif current_direction == 'S':
        return next_obstacle_row - 1, next_obstacle_col
    elif current_direction == 'E':
        return next_obstacle_row, next_obstacle_col - 1
    elif current_direction == 'W':
        return next_obstacle_row, next_obstacle_col + 1


def find_positions_visited(current_row: int, current_col: int,
                           next_obstacle_row: int, next_obstacle_col: int,
                           current_direction: str) -> set[tuple[int, int, str]]:
    """
    Find positions visited between current and next position
    """
    if current_direction == 'N':
        return {(row, current_col, current_direction) for row in range(current_row - 1, next_obstacle_row, -1)}
    elif current_direction == 'S':
        return {(row, current_col, current_direction) for row in range(current_row + 1, next_obstacle_row)}
    elif current_direction == 'E':
        return {(current_row, col, current_direction) for col in range(current_col + 1, next_obstacle_col)}
    elif current_direction == 'W':
        return {(current_row, col, current_direction) for col in range(current_col - 1, next_obstacle_col, -1)}


def find_position_after_exit(grid: list[list[str]],
                             current_row: int, current_col: int, current_direction: str) -> tuple[int, int]:
    """
    Find position after exiting the grid
    """
    if current_direction == 'N':
        return -1, current_col
    elif current_direction == 'S':
        return len(grid), current_col
    elif current_direction == 'E':
        return current_row, len(grid[0])
    elif current_direction == 'W':
        return current_row, -1


def find_path(grid: list[list[str]], obstacles: list[tuple[int, int]],
              starting_position: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
    """
    Find positions visited in the predicted path
    Return None when a loop is found
    """
    next_directions = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
    current_row, current_col = starting_position
    current_direction = 'N'
    exited = False
    unique_positions_visited = {(current_row, current_col, current_direction)}

    while not exited:
        next_obstacle = find_next_obstacle(current_row, current_col, current_direction, obstacles)

        if next_obstacle is None:  # Escaped
            after_exit_row, after_exit_col = find_position_after_exit(grid, current_row, current_col, current_direction)
            next_obstacle_row, next_obstacle_col = after_exit_row, after_exit_col
            exited = True
        else:
            next_obstacle_row, next_obstacle_col = next_obstacle

        positions_visited = find_positions_visited(current_row, current_col,
                                                   next_obstacle_row, next_obstacle_col,
                                                   current_direction)
        if unique_positions_visited.intersection(positions_visited):
            return None
        else:
            unique_positions_visited = unique_positions_visited.union(positions_visited)

            current_row, current_col = find_next_position(next_obstacle_row, next_obstacle_col, current_direction)
            current_direction = next_directions[current_direction]

    unique_places_visited = {(row, col) for (row, col, direction) in unique_positions_visited}

    return unique_places_visited

def part2(grid: list[list[int]], obstacles: list[tuple[int, int]],
          starting_position: tuple[int, int], predicted_path: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Count positions where placing an obstacle causes a loop
    """
    loop_possibilities = 0
    for position in predicted_path:
        if position != starting_position:
            if find_path(grid, obstacles + [position], starting_position) is None:
                loop_possibilities += 1

    return loop_possibilities

if __name__ == '__main__':
    grid = parse_grid('data/day6.txt')
    obstacles, starting_position = find_obstacles_and_starting_position(grid)

    predicted_path = find_path(grid, obstacles, starting_position)
    print(f'part 1: {len(predicted_path)}')

    print(f"\nStart time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
    part2 = part2(grid, obstacles, starting_position, predicted_path)
    print(f'part 2: {part2}')
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")


