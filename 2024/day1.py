def parse_lists(filename: str) -> tuple[list[float], list[float]]:
    """
    Parse the provided file into two lists of ints
    """
    left_values, right_values = [], []
    with open(filename, 'r') as file:
        for line in file:
            left_value, right_value = line.split('   ')
            left_values.append(float(left_value.strip()))
            right_values.append(float(right_value.strip()))

    return left_values, right_values


def find_total_distance(left_values: list[float], right_values: list[float]) -> float:
    """
    Find the sum of the absolute distance between the values in the sorted lists
    """
    left_sorted = sorted(left_values)
    right_sorted = sorted(right_values)

    distances = [abs(right_sorted[i] - left_sorted[i]) for i in range(len(left_sorted))]

    return sum(distances)


def find_counts(value_list: list[float]) -> dict[float, int]:
    """
    Find the counts of each value in the list
    """
    counter = {}
    for value in value_list:
        if value not in counter:
            counter[value] = 1
        else:
            counter[value] += 1

    return counter


def calculate_similarity_score(left_values: list[float], right_values: list[float]) -> float:
    """
    Find the sum of the product of each value in the left list with its number of occurrences in the two lists
    """
    left_counts = find_counts(left_values)
    right_counts = find_counts(right_values)

    total_similarity_score = 0
    for left_value, left_count in left_counts.items():
        similarity_score = left_value * left_count * right_counts.get(left_value, 0)  # Default to 0 for missing values
        total_similarity_score += similarity_score

    return total_similarity_score


if __name__ == '__main__':
    left_list, right_list = parse_lists('day1.txt')

    total_distance = find_total_distance(left_list, right_list)
    print(f'part 1: {total_distance}')

    total_similarity = calculate_similarity_score(left_values=left_list, right_values=right_list)
    print(f'part 2: {total_similarity}')
