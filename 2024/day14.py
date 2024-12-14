import math
import re
from tqdm import tqdm

def parse_input(filename: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Parse the input
    """
    robot_positions = []
    robot_velocities = []
    with open(filename, 'r') as file:
        for robot in file:
            [(px, py), (vx, vy)] = re.findall(r'(-?\d+),(-?\d+)', robot)
            robot_positions.append((int(px), int(py)))
            robot_velocities.append((int(vx), int(vy)))

    return robot_positions, robot_velocities


def move_robot(position: tuple[int, int], velocity: tuple[int, int], width: int, height: int) -> tuple[int, int]:
    """
    Move the robot according to its velocity, teleporting when it reaches a border
    """
    px, py = position
    vx, vy = velocity

    new_px = (px + vx) % width
    new_py = (py + vy) % height

    return new_px, new_py


def simulate_robot_movements(robot_positions: list[tuple[int, int]], robot_velocities: list[tuple[int, int]],
                             width: int, height: int, seconds: int) -> list[tuple[int, int]]:
    """
    Simulate the movement of the robots for the provided amount of time
    """
    for seconds_elapsed in range(seconds):
        for index, (position, velocity) in enumerate(zip(robot_positions, robot_velocities)):
            robot_positions[index] = move_robot(position=position, velocity=velocity, width=width, height=height)

    return robot_positions


def count_robots_per_quadrant(robot_positions: list[tuple[int, int]], width: int, height: int) -> list[int]:
    """
    Count the number of robots in each quadrant
    """
    max_x = width - 1
    max_y = height - 1

    mid_x = max_x / 2
    mid_y = max_y / 2

    quadrant_counts = [0, 0, 0, 0]
    for (px, py) in robot_positions:
        if mid_x < px <= max_x and 0 <= py < mid_y:  # Quad 1
            quadrant_counts[0] += 1
        elif 0 <= px < mid_x and 0 <= py < mid_y:  # Quad 2
            quadrant_counts[1] += 1
        elif 0 <= px < mid_x and mid_y < py <= max_y:  # Quad 3
            quadrant_counts[2] += 1
        elif mid_x < px <= max_x and mid_y < py <= max_y: # Quad 4
            quadrant_counts[3] += 1

    return quadrant_counts


def part1(robot_positions: list[tuple[int, int]], robot_velocities: list[tuple[int, int]],
          width: int, height: int, seconds: int) -> int:
    """
    Calculate safety factor of the robots
    """
    final_positions = simulate_robot_movements(robot_positions=robot_positions, robot_velocities=robot_velocities,
                                               width=width, height=height, seconds=seconds)
    quadrant_counts = count_robots_per_quadrant(robot_positions=final_positions, width=width, height=height)
    safety_factor = math.prod(quadrant_counts)

    return safety_factor


def christmas_tree_found(robot_positions: list[tuple[int, int]], width: int, height: int, seconds_elapsed: int) -> bool:
    """
    Find the seconds elapsed at the point that the Christmas tree is created
    """
    is_christmas_tree = False

    # Populate grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for y, x in robot_positions:
        grid[x][y] = '*'

    # Identify Christmas tree iteration
    for row in grid:
        if '*********' in ''.join(row):  # Should include a bunch of asterisks in a row
            is_christmas_tree = True

    # Print seconds elapsed and the image
    if is_christmas_tree:
        print(seconds_elapsed)
        for row in grid:
            print(''.join(row))

    return is_christmas_tree


def part2(robot_positions: list[tuple[int, int]], robot_velocities: list[tuple[int, int]],
          width: int, height: int, seconds: int) -> None:
    """
    Simulate the movement of the robots and print potential Christmas trees
    """
    for seconds_elapsed in range(1, seconds):
        for index, (position, velocity) in enumerate(zip(robot_positions, robot_velocities)):
            robot_positions[index] = move_robot(position=position, velocity=velocity, width=width, height=height)

        if christmas_tree_found(robot_positions=robot_positions, width=width, height=height,
                                seconds_elapsed=seconds_elapsed):
            break

    return


if __name__ == '__main__':
    positions, velocities = parse_input('data/day14.txt')

    part1 = part1(robot_positions=positions.copy(), robot_velocities=velocities, width=101, height=103, seconds=100)
    print(f'part 1: {part1}')

    part2(robot_positions=positions.copy(), robot_velocities=velocities, width=101, height=103, seconds=10403)