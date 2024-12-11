import re
from tqdm import tqdm


def parse_input(filename: str) -> list[str]:
    """
    Parse the input
    """
    with open(filename, 'r') as file:
        data = file.read()
        stones = re.findall('\d+', data)

    return stones

def evolve_stone(stone: str) -> list[str]:
    """
    Evolve stone
    """
    if stone == '0':
        return ['1']

    elif len(stone) % 2 == 0:
        midpoint = len(stone) // 2
        return [str(int(stone[:midpoint])), str(int(stone[midpoint:]))]

    else:
        return [str(int(stone) * 2024)]

def count_stones(stones: list[str], num_blinks: int) -> int:
    """
    Count stones created from evolution more efficiently
    """
    stones = [(stone, 1) for stone in stones]
    for i in tqdm(range(num_blinks)):
        next_stones = {}
        while stones:
            stone, stone_count = stones.pop(0)
            for next_stone in evolve_stone(stone=stone):
                next_stones[next_stone] = next_stones.get(next_stone, 0) + stone_count
        stones = list(next_stones.items())

    return sum([stone_count for stone, stone_count in stones])


if __name__ == '__main__':
    stones = parse_input('data/day11.txt')

    part_1 = count_stones(stones=stones, num_blinks=25)
    print(f'part 1: {part_1}')

    part_2 = count_stones(stones=stones, num_blinks=75)
    print(f'part 2: {part_2}')