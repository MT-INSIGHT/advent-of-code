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
    return [report[i] - report[i - 1] for i in range(1, len(report))]


def is_safe_report(report: list[int]) -> bool:
    """
    Determine if the set of deviations is valid - must not deviate from {1, 2, 3} or {-1, -2, -3}
    """
    deviations = calculate_deviations(report)
    return len(set(deviations) - {1, 2, 3}) == 0 or len(set(deviations) - {-1, -2, -3}) == 0


def count_safe_reports(reports_list: list[list[int]]) -> int:
    """
    Find the number of safe reports
    """
    total_safe_reports = 0
    for report in reports_list:
        if is_safe_report(report):
            total_safe_reports += 1

    return total_safe_reports


def count_safe_reports_tolerant(reports_list: list[list[int]]) -> int:
    """
    Find the number of safe reports, tolerant of one bad level
    """
    total_safe_reports = 0
    for report in reports_list:
        if any([is_safe_report(report[:level_index] + report[level_index + 1:]) for level_index in range(len(report))]):
            total_safe_reports += 1

    return total_safe_reports


if __name__ == '__main__':
    reports = parse_reports('data/day2.txt')

    safe_reports = count_safe_reports(reports)
    print(f'part 1: {safe_reports}')

    tolerant_safe_reports = count_safe_reports_tolerant(reports)
    print(f'part 2: {tolerant_safe_reports}')

