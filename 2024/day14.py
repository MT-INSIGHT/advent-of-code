import math
import re
from tqdm import tqdm

def parse_input(filename: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Parse the input
    """
    a_buttons = []
    b_buttons = []
    prizes = []
    with open(filename, 'r') as file:
        data = file.read()
        for machine in data.split('\n\n'):
            button_a, button_b, prize = machine.split('\n')
            a_x, a_y = [int(val) for val in re.findall('\d+', button_a)]
            a_buttons.append((a_x, a_y))
            b_x, b_y = [int(val) for val in re.findall('\d+', button_b)]
            b_buttons.append((b_x, b_y))
            prize_x, prize_y = [int(val) for val in re.findall('\d+', prize)]
            prizes.append((prize_x, prize_y))


    return a_buttons, b_buttons, prizes


def solve_system(a_button: tuple[int, int], b_button: tuple[int, int], prize: tuple[int, int]) -> tuple[float, float]:
    """
    Solve the system of equations for the intersection point
    """
    lcm_a = math.lcm(a_button[0], a_button[1])
    x_mult = lcm_a / a_button[0]
    y_mult = lcm_a / a_button[1]
    b = (prize[0] * x_mult - prize[1] * y_mult) / (b_button[0] * x_mult - b_button[1] * y_mult)
    a = (prize[1] - b_button[1] * b) / a_button[1]

    return (a, b)


def calculate_tokens(a_buttons: list[tuple[int, int]],
                     b_buttons: list[tuple[int, int]],
                     prizes: list[tuple[int, int]],
                     prize_position_adder: int) -> int:
    """
    Calculate the fewest tokens needed to win all possible prizes
    """
    required_tokens = 0
    for (a_button, b_button, prize) in zip(a_buttons, b_buttons, prizes):
        adjusted_prize = (prize[0] + prize_position_adder, prize[1] + prize_position_adder)
        a, b = solve_system(a_button=a_button, b_button=b_button, prize=adjusted_prize)
        if int(a) == a and int(b) == b:  # Valid if solution has an integer number of button pushes
            required_tokens += (3 * a + b)

    return required_tokens


if __name__ == '__main__':
    a_buttons, b_buttons, prizes = parse_input('data/day13.txt')

    part_1 = calculate_tokens(a_buttons=a_buttons, b_buttons=b_buttons, prizes=prizes,
                              prize_position_adder=0)
    print(f'part 1: {part_1}')

    part_2 = calculate_tokens(a_buttons=a_buttons, b_buttons=b_buttons, prizes=prizes,
                              prize_position_adder=10000000000000)
    print(f'part 2: {part_2}')