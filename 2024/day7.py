import re
import math
from itertools import product


def parse_input(filename: str) -> list[tuple[int, list[int]]]:
    """
    Parse the input into a rules tracker for following pages and the updates that are being made
    """
    value_equations = []
    with open(filename, 'r') as file:
        for line in file:
            value, equation_factors = line.split(': ')
            factors = [int(factor) for factor in equation_factors.split(' ')]
            value_equations.append((int(value), factors))

    return value_equations

def apply_operator(value: int, factor: int, operator: str) -> int:
    """
    Apply the operator to the value and the factor
    """
    if operator == '+':
        return value + factor
    elif operator == '*':
        return value * factor
    elif operator == '||':
        return int(f'{value}{factor}')

def is_valid(factors: list[int], operator_combinations: list[str], expected_value: int) -> bool:
    """
    Determine if there is a possible combination of factors that yield the expected value
    """
    for operator_combination in operator_combinations:
        total = factors[0]
        for factor, operator in zip(factors[1:], operator_combination):
            total = apply_operator(value=total, factor=factor, operator=operator)
        if total == expected_value:
            return True

    return False


def calculate_calibration_result(value_equations: list[tuple[int, list[int]]], allowed_operators: list[str]) -> int:
    """
    Sum values of correct equations
    """
    total_calibration_result = 0
    for value, equation_factors in value_equations:
        operator_combos = list(product(allowed_operators, repeat=len(equation_factors) - 1))
        if is_valid(factors=equation_factors, operator_combinations=operator_combos, expected_value=value):
            total_calibration_result += value

    return total_calibration_result

if __name__ == '__main__':
    value_equations = parse_input('data/day7.txt')

    part_1 = calculate_calibration_result(value_equations=value_equations, allowed_operators=['*', '+'])
    print(f'part 1: {part_1}')

    part_2 = calculate_calibration_result(value_equations=value_equations, allowed_operators=['*', '+', '||'])
    print(f'part 1: {part_2}')