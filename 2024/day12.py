import itertools
import re
from tqdm import tqdm


def parse_grid(filename: str) -> list[list[str]]:
    """
    Parse the input into 2d grid
    """
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid


def find_ungrouped_matching_neighbors(grid: list[list[str]], grouped_tracker: dict[tuple[int, int], bool],
                                      curr_row: int, curr_col: int, curr_val: str
                                      ) -> tuple[list[tuple[int, int]], list[tuple[int, int]], int]:
    """
    Find in-bound neighbors that match the current value
    """
    direction_adders = {'N': (-1, 0), 'S': (1, 0), 'E': (0, -1), 'W': (0, 1)}
    num_matching_neighbors = 0
    ungrouped_matching_neighbors, grouped_matching_neighbors = [], []

    for (row_adder, col_adder) in direction_adders.values():
        neighbor_row, neighbor_col = curr_row + row_adder, curr_col + col_adder
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # In bounds
            neighbor_value = grid[neighbor_row][neighbor_col]
            if neighbor_value == curr_val:
                num_matching_neighbors += 1
                if not grouped_tracker[(neighbor_row, neighbor_col)]:
                    ungrouped_matching_neighbors.append((neighbor_row, neighbor_col))
                else:
                    grouped_matching_neighbors.append((neighbor_row, neighbor_col))

    plot_perimeter = 4 - num_matching_neighbors

    return ungrouped_matching_neighbors, grouped_matching_neighbors, plot_perimeter


def find_regions(grid:list[list[str]]) -> tuple[dict[str, list[list[tuple[int, int]]]], dict[tuple[int, int], int]]:
    """
    Find all regions in the grid
    """
    grouped_tracker = {(row, col): False for row in range(len(grid)) for col in range(len(grid[0]))}
    plot_perimeters = {}
    region_tracker = {}
    ungrouped_coords = list(grouped_tracker.keys())

    while ungrouped_coords:
        curr_row, curr_col = ungrouped_coords.pop(0)
        curr_val = grid[curr_row][curr_col]
        if not grouped_tracker[curr_row, curr_col]:  # Only try to group coords that haven't already been grouped
            grouped_tracker[(curr_row, curr_col)] = True
            ungrouped_matching_neighbors, grouped_matching_neighbors, plot_perimeter = \
                find_ungrouped_matching_neighbors(
                    grid=grid, grouped_tracker=grouped_tracker,
                    curr_row=curr_row, curr_col=curr_col, curr_val=curr_val)
            plot_perimeters[(curr_row, curr_col)] = plot_perimeter

            # Update current region
            if curr_val in region_tracker:
                in_existing_region = False
                for index, region in enumerate(region_tracker[curr_val]):
                    if len(set(region).intersection(grouped_matching_neighbors)) > 0:  # Neighbors are in prior region
                        region_tracker[curr_val][index].append((curr_row, curr_col))  # Add to existing region
                        in_existing_region = True
                if not in_existing_region:
                    region_tracker[curr_val].append([(curr_row, curr_col)])
            else:
                region_tracker[curr_val] = [[(curr_row, curr_col)]]

            if ungrouped_matching_neighbors:   # Put ungrouped neighbors on top to search next
                ungrouped_coords = ungrouped_matching_neighbors + ungrouped_coords

    return region_tracker, plot_perimeters


def part1(region_tracker: dict[str, list[list[tuple[int, int]]]], plot_perimeters: dict[tuple[int, int], int]) -> int:
    """
    Sum the price of fencing all regions
    """
    total_price = 0
    for type, regions in region_tracker.items():
        for region in regions:
            area = len(region)
            perimeter = sum([plot_perimeters[(row, col)] for (row, col) in region])
            total_price += (perimeter * area)

    return total_price


def find_perimeter_plots(region: list[tuple[int, int]],
                         plot_perimeters: dict[tuple[int, int], int]) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Find the points on the perimeter
    """
    perimeter_plots, perimeter_plot_perimeters = [], []
    for plot in region:
        if plot_perimeters[plot] != 0:
            perimeter_plots.append(plot)
            perimeter_plot_perimeters.append(plot_perimeters[plot])

    return perimeter_plots, perimeter_plot_perimeters

def find_mismatched_neighbor_directions(grid: list[list[str]], curr_row: int, curr_col: int, curr_val: str) -> set[str]:
    """
    Find the directions that mismatched neighbors are in
    """
    directions = set()
    direction_adders = {'N': (-1, 0), 'S': (1, 0), 'E': (0, -1), 'W': (0, 1)}

    for direction, (row_adder, col_adder) in direction_adders.items():
        neighbor_row, neighbor_col = curr_row + row_adder, curr_col + col_adder
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # In bounds
            neighbor_value = grid[neighbor_row][neighbor_col]
            if neighbor_value != curr_val:
                directions.add(direction)
        else:  # Out of bounds also is a mismatch
            directions.add(direction)

    return directions


def count_interior_corners(plot1: tuple[int, int], plot2: tuple[int, int],
                           grid: list[list[str]], region: list[tuple[int, int]], ) -> int:
    """
    Count interior corners for plots that are diagonal to each other and have shared external neighbors
    """
    (row1, col1) = plot1
    (row2, col2) = plot2

    diagonal_differences = {(-1, -1): 'NE', (-1, 1): 'NW', (1, -1): 'SE', (1, 1): 'SW'}
    cardinal_direction_adjustments = {'N': (-1, 0), 'S': (1, 0), 'E': (0, -1), 'W': (0, 1)}

    diagonal_direction = diagonal_differences.get((row2 - row1, col2 - col1))
    if diagonal_direction:  # Plots are diagonal

        # Identify shared neighbors that are in bounds
        shared_neighbors = []
        for cardinal_direction in diagonal_direction:
            diff_row, diff_col = cardinal_direction_adjustments[cardinal_direction]
            neighbor_row, neighbor_col = (row1 + diff_row, col1 + diff_col)
            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):  # In bounds
                shared_neighbors.append((row1 + diff_row, col1 + diff_col))

        if len([neighbor for neighbor in shared_neighbors if neighbor not in region]) == 1:
            return 1

    return 0


def count_corners(grid: list[list[str]], region: list[tuple[int, int]], plot_perimeters: dict[tuple[int, int], int]) -> int:
    """
    Count the number of corners in the perimeter of the region - equivalent to the number of sides
    """
    # Identify perimeter plots from the region
    perimeter_plots, perimeter_plot_perimeters = find_perimeter_plots(region=region, plot_perimeters=plot_perimeters)

    num_corners = 0
    # Count corners facing out at plots outside the region
    two_sided_corner_required_mismatched_neighbor_directions = [{'N', 'E'}, {'S', 'E'}, {'N', 'W'}, {'S', 'W'}]
    cardinal_direction_adjustments = {'N': (-1, 0), 'S': (1, 0), 'E': (0, -1), 'W': (0, 1)}
    for index, perimeter in enumerate(perimeter_plot_perimeters):
        if perimeter == 4:
            num_corners += 4
        elif perimeter == 3:
            num_corners += 2
        elif perimeter == 2:
            plot_row, plot_col = perimeter_plots[index]
            plot_value = grid[plot_row][plot_col]
            mismatched_neighbor_directions = find_mismatched_neighbor_directions(grid=grid,
                                                                                 curr_row=plot_row, curr_col=plot_col,
                                                                                 curr_val=plot_value)
            if mismatched_neighbor_directions in two_sided_corner_required_mismatched_neighbor_directions:
                num_corners += 1

    # Count corners facing internal to the region
    if len(perimeter_plots) > 1:
        plot_pairs = itertools.combinations(perimeter_plots, 2)
        for (plot1, plot2) in plot_pairs:
            num_corners += count_interior_corners(plot1=plot1, plot2=plot2, grid=grid, region=region)

    return num_corners


def part2(grid: list[list[str]], region_tracker: dict[str, list[list[tuple[int, int]]]], plot_perimeters: dict[tuple[int, int], int]) -> int:
    """
    Sum the price of fencing all regions with the bulk discount
    """
    total_price = 0
    for type, regions in region_tracker.items():
        for region in regions:
            area = len(region)
            num_sides = count_corners(grid=grid, region=region, plot_perimeters=plot_perimeters)
            total_price += (num_sides * area)

    return total_price



if __name__ == '__main__':
    grid = parse_grid('data/day12.txt')
    region_tracker, plot_perimeters = find_regions(grid=grid)

    part_1 = part1(region_tracker=region_tracker, plot_perimeters=plot_perimeters)
    print(f'part 1: {part_1}')

    part_2 = part2(grid=grid, region_tracker=region_tracker, plot_perimeters=plot_perimeters)
    print(f'part 2: {part_2}')