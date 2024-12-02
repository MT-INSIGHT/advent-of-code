def parse_reports(filename: str) -> list[list[int]]:
    """
    Parse the provided file into a list of lists
    """
    reports_list = []
    with open(filename, 'r') as file:
        for line in file:
            report = [int(val) for val in line.split(' ')]
            reports_list.append(report)

    return reports_list


def calculate_deviations(report: list[int]) -> list[int]:
    """
    Find the deviations between levels in the report
    """
    deviations = []
    for i in range(1, len(report)):
        deviations.append(report[i] - report[i - 1])

    return deviations


def is_changing_in_one_direction(deviations: list[int]) -> bool:
    """
    Determine if the report levels are all increasing or all decreasing
    """
    is_one_direction = False
    if deviations[0] > 0:
        is_one_direction = all([deviation > 0 for deviation in deviations])
    else:
        is_one_direction = all([deviation < 0 for deviation in deviations])

    return is_one_direction


def all_valid_deviations(deviations: list[int]) -> bool:
    """
    Determine if the report levels differ by at least one and at most three
    """
    return all([1 <= abs(deviation) <= 3 for deviation in deviations])


def count_safe_reports(reports_list: list[list[int]]) -> int:
    """
    Find the number of safe reports
    """
    total_safe_reports = 0
    for report in reports_list:
        deviations = calculate_deviations(report)
        if is_changing_in_one_direction(deviations):
            if all_valid_deviations(deviations):
                total_safe_reports += 1

    return total_safe_reports


def is_changing_in_one_direction_tolerant(report: list[int], deviations: list[int]) -> tuple[bool, bool, list[int]]:
    """
    Determine if the report levels are all increasing or all decreasing
        - Allows for the removal of one bad level from the report and recalculates deviations
    """
    num_negative_deviations, num_positive_deviations = 0, 0
    last_negative_deviation_index, last_positive_deviation_index = 0, 0
    for index, deviation in enumerate(deviations):
        if deviation < 0:
            num_negative_deviations += 1
            last_negative_deviation_index = index
        else:
            num_positive_deviations += 1
            last_positive_deviation_index = index
        if num_negative_deviations > 1 and num_positive_deviations > 1:  # Totally unsafe
            return False, False, deviations

    if num_negative_deviations == 1:  # Potentially safe if level is removed
        report.pop(last_negative_deviation_index)
        adjusted_deviations = calculate_deviations(report)
        return True, True, adjusted_deviations
    elif num_positive_deviations == 1:  # Potentially safe if level is removed
        report.pop(last_positive_deviation_index)
        adjusted_deviations = calculate_deviations(report)
        return True, True, adjusted_deviations
    else:  # Safe
        return True, False, deviations


def all_valid_deviations_tolerant(removed_level: bool, report: list[int], deviations: list[int]) -> bool:
    """
    Determine if the report levels differ by at least one and at most three
        - Tolerates at most one bad level if a level has not already been removed
    """
    if removed_level:
        return all_valid_deviations(deviations)
    else:
        for index, deviation in enumerate(deviations):
            if abs(deviation) < 1 or abs(deviation) > 3:
                report.pop(index)
                adjusted_deviations = calculate_deviations(report)

                return all_valid_deviations(adjusted_deviations)

        return True


def count_safe_reports_tolerant(reports_list: list[list[int]]) -> int:
    """
    Find the number of safe reports
        - Tolerates at most one bad level in each report
    """
    total_safe_reports = 0
    for report in reports_list:
        deviations = calculate_deviations(report)
        is_direction_safe, removed_level, adjusted_deviations = is_changing_in_one_direction_tolerant(report, deviations)
        if is_direction_safe:
            if all_valid_deviations_tolerant(removed_level, report, adjusted_deviations):
                total_safe_reports += 1

    return total_safe_reports


if __name__ == '__main__':
    reports = parse_reports('data/day2.txt')

    safe_reports = count_safe_reports(reports)
    print(f'part 1: {safe_reports}')

    tolerant_safe_reports = count_safe_reports_tolerant(reports)
    print(f'part 2: {tolerant_safe_reports}')
