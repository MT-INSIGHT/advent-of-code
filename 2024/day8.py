import itertools


def parse_grid(filename: str) -> list[list[str]]:
    """
    Parse the input into 2d grid
    """
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid


def find_antennas(grid: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    """
    Store the coordinates of all antennas by their frequency
    """
    frequency_antennas = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            frequency = grid[row][col]
            if frequency != '.':
                if frequency in frequency_antennas:
                    frequency_antennas[frequency].append((row, col))
                else:
                    frequency_antennas[frequency] = [(row, col)]

    return frequency_antennas


def find_in_bound_anti_nodes(start_row: int, start_col: int, row_diff: int, col_diff: int,
                             max_row: int, max_col: int) -> list[tuple[int, int]]:
    """
    Find all anti-nodes in the grid in line with the provided starting antenna using the given differences
    """
    in_bound_anti_nodes = []
    in_bound = True
    row, col = start_row, start_col

    while in_bound:
        row += row_diff
        col += col_diff
        if row < 0 or row > max_row or col < 0 or col > max_col:
            in_bound = False
        else:
            in_bound_anti_nodes.append((row, col))

    return in_bound_anti_nodes


def find_anti_nodes(antenna_1: tuple[int, int], antenna_2: tuple[int, int],
                    max_row: int, max_col: int, part1: bool) -> list[tuple[int, int]]:
    """
    Find the anti-nodes for the provided two antennas
    """
    antenna_1_row, antenna_1_col = antenna_1
    antenna_2_row, antenna_2_col = antenna_2

    row_diff = antenna_2_row - antenna_1_row
    col_diff = antenna_2_col - antenna_1_col

    if part1:
        anti_node_backward = antenna_1_row - row_diff, antenna_1_col - col_diff
        anti_node_forward = antenna_2_row + row_diff, antenna_2_col + col_diff
        in_bound_anti_nodes = [(row, col) for (row, col) in [anti_node_backward, anti_node_forward]
                              if 0 <= row <= max_row and 0 <= col <= max_col]
    else:
        in_bound_anti_nodes_backward = find_in_bound_anti_nodes(start_row=antenna_1_row, start_col=antenna_1_col,
                                                                row_diff=-row_diff, col_diff=-col_diff,
                                                                max_row=max_row, max_col=max_col)
        in_bound_anti_nodes_forward = find_in_bound_anti_nodes(start_row=antenna_2_row, start_col=antenna_2_col,
                                                               row_diff=row_diff, col_diff=col_diff,
                                                               max_row=max_row, max_col=max_col)
        in_bound_anti_nodes = in_bound_anti_nodes_backward + in_bound_anti_nodes_forward

    return in_bound_anti_nodes

def count_anti_nodes(grid: list[list[str]], part1: bool) -> int:
    """
    Count unique anti-nodes
    """
    max_row, max_col = len(grid) - 1, len(grid[0]) - 1
    frequency_antennas = find_antennas(grid)
    antenna_locations = set()
    anti_nodes = set()

    for frequency, antennas in frequency_antennas.items():
        antenna_locations = antenna_locations.union(antennas)
        antenna_combos = itertools.combinations(antennas, 2)
        for antenna_1, antenna_2 in antenna_combos:
            anti_nodes = anti_nodes.union(set(find_anti_nodes(antenna_1=antenna_1, antenna_2=antenna_2,
                                                              max_row=max_row, max_col=max_col, part1=part1)))

    if not part1:  # Antennas are also counted as anti-nodes
        anti_nodes = anti_nodes.union(antenna_locations - anti_nodes)  # Add unique anti-nodes among antennas

    return len(anti_nodes)


if __name__ == '__main__':
    grid = parse_grid('data/day8.txt')

    part_1 = count_anti_nodes(grid=grid, part1=True)
    print(f'part 1: {part_1}')

    part_2 = count_anti_nodes(grid=grid, part1=False)
    print(f'part 2: {part_2}')