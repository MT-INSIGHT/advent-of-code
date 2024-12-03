import re
import math


def parse_memory(filename: str) -> list[list[int]]:
    """
    Parse the corrupted file for instructions
    """
    memory = []
    with open(filename, 'r') as file:
        for line in file:
            memory += re.findall('mul\([0-9]+\,[0-9]+\)|do\(\)|don\'t\(\)', line)

    return memory

def execute_mul_instructions(instructions: list[str]) -> int:
    """
    Sum the results of obeying only the mul instructions
    """
    result = 0
    for instruction in instructions:
        if 'mul' in instruction:
            result += math.prod([int(i) for i in re.findall('\d+', instruction)])

    return result

def execute_all_instructions(instructions: list[str]) -> int:
    """
    Sum the results of obeying all instructions
    """
    result = 0
    mul_enabled = True
    for instruction in instructions:
        if 'don\'t' in instruction:
            mul_enabled = False
        elif 'do' in instruction:
            mul_enabled = True
        elif mul_enabled:
            result += math.prod([int(i) for i in re.findall('\d+', instruction)])

    return result


if __name__ == '__main__':
    all_instructions = parse_memory('data/day3.txt')

    part_1 = execute_mul_instructions(all_instructions)
    print(f'part 1: {part_1}')

    part_2 = execute_all_instructions(all_instructions)
    print(f'part 2: {part_2}')

