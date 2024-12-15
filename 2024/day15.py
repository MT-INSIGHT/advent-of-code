def parse_input(filename: str) -> tuple[list[list[str]], str]:
    """
    Parse the input
    """
    with open(filename, 'r') as file:
        data = file.read()
        grid_lines, movements = data.split('\n\n')
        grid_lines = grid_lines.split('\n')
        grid = []
        for line in grid_lines:
            grid.append(list(line))

        movement_str = ''.join(movement_line.strip() for movement_line in movements)

    return grid, movement_str


def find_robot_starting_position(grid: list[list[str]]) -> tuple[int, int]:
    """
    Find the starting position of the robot
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '@':
                return row, col


def move_robot(grid: list[list[str]],
               position: tuple[int, int], movement: str) -> tuple[list[list[str]], tuple[int, int]]:
    """
    Move the robot according to the provided movement
    """
    movement_adders = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    row, col = position
    movement_row, movement_col = movement_adders[movement]

    open_row, open_col = row + movement_row, col + movement_col
    open_space_found = False
    # Find open space
    while grid[open_row][open_col] != '#':
        if grid[open_row][open_col] == '.':
            open_space_found = True
            break
        elif grid[open_row][open_col] == 'O':
            open_row, open_col = open_row + movement_row, open_col + movement_col

    # Shift robot and boxes
    next_row, next_col = position
    if open_space_found:
        next_row, next_col = row + movement_row, col + movement_col
        grid[row][col] = '.'  # Leave open space post-movement
        move_to_row, move_to_col = open_row, open_col
        move_from_row, move_from_col = open_row, open_col
        while (move_from_row, move_from_col) != (row, col):
            move_from_row, move_from_col = move_from_row - movement_row, move_from_col - movement_col
            grid[move_to_row][move_to_col] = grid[move_from_row][move_from_col]
            move_to_row, move_to_col = move_from_row, move_from_col

    return grid, (next_row, next_col)


def part1(grid: list[list[str]], movements: str) -> int:
    """
    Sum box GPS coordinates in the final state
    """
    # Find final state
    position = find_robot_starting_position(grid=grid)
    for movement in movements:
        grid, position = move_robot(grid=grid, position=position, movement=movement)

    # Sum box GPS coordinates
    coordinate_sum = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'O':
                coordinate_sum += (row * 100 + col)

    return coordinate_sum


def scale_grid(grid: list[list[str]]) -> list[list[str]]:
    """
    Create new warehouse map
    """
    new_grid = []
    for row in grid:
        old_row = ''.join(row)
        new_row = (old_row
                   .replace('#', '##')
                   .replace('O', '[]')
                   .replace('.', '..')
                   .replace('@', '@.'))
        new_grid.append(list(new_row))

    return new_grid


def move_robot_scaled(grid: list[list[str]],
                      position: tuple[int, int], movement: str) -> tuple[list[list[str]], tuple[int, int]]:
    """
    Move the robot according to the provided movement in the scaled grid
    """
    movement_adders = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    row, col = position
    movement_row, movement_col = movement_adders[movement]

    open_space_found = False
    to_search = [(row + movement_row, col + movement_col)]
    to_move = [(row, col)]
    # Find open space
    while grid[open_row][open_col] != '#':
        next_row, next_col = to_search.pop(0)
        if grid[open_row][open_col] == '.':
            open_space_found = True
            break
        elif grid[open_row][open_col] == '[':
            open_row, open_col = open_row + movement_row, open_col + movement_col

    # Shift robot and boxes
    next_row, next_col = position
    if open_space_found:
        next_row, next_col = row + movement_row, col + movement_col
        grid[row][col] = '.'  # Leave open space post-movement
        move_to_row, move_to_col = open_row, open_col
        move_from_row, move_from_col = open_row, open_col
        while (move_from_row, move_from_col) != (row, col):
            move_from_row, move_from_col = move_from_row - movement_row, move_from_col - movement_col
            grid[move_to_row][move_to_col] = grid[move_from_row][move_from_col]
            move_to_row, move_to_col = move_from_row, move_from_col

    return grid, (next_row, next_col)


def part2(grid: list[list[str]], movements: str) -> int:
    """
    Sum box GPS coordinates in the final state
    """
    # Find final state
    position = find_robot_starting_position(grid=grid)
    for movement in movements:
        grid, position = move_robot(grid=grid, position=position, movement=movement)

    # Sum box GPS coordinates
    coordinate_sum = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '[':
                coordinate_sum += (row * 100 + col)

    return coordinate_sum


if __name__ == '__main__':
    grid, movements = parse_input('data/day15.txt')
    new_grid = scale_grid(grid=grid)

    part1 = part1(grid=grid, movements=movements)
    print(f'part 1: {part1}')

    # part2 = part2(grid=new_grid, movements=movements)
    # print(f'part 2: {part2}')