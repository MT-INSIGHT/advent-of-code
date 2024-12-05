import re
import math


def parse_input(filename: str) -> tuple[dict[str, list[str]], list[list[str]]]:
    """
    Parse the input into a rules tracker for following pages and the updates that are being made
    """
    following_pages = {}
    with open(filename, 'r') as file:
        rules, updates = file.read().split('\n\n')

        for rule in rules.split('\n'):
            current_page, following_page = rule.split('|')
            if current_page in following_pages:
                following_pages[current_page].append(following_page)
            else:
                following_pages[current_page] = [following_page]

        update_pages = [update.split(',') for update in updates.split('\n')]

    return following_pages, update_pages

def is_valid_page(following_page_tracker: dict[str, list[str]], current_page: str, page_update: list[str]) -> bool:
    """
    Determine if the provided page is ordered in a valid way in the given update
    """
    if current_page not in following_page_tracker:  # No rules
        return True

    else:
        following_pages = following_page_tracker[current_page]
        current_page_index = page_update.index(current_page)
        is_valid = all(page_update.index(following_page) > current_page_index
                       for following_page in following_pages if following_page in page_update)

        return is_valid

def part1(following_page_tracker: dict[str, list[str]], page_updates: list[list[str]]) -> int:
    """
    Sum middle page numbers of valid page update orderings
    """
    total_valid_middle_pages = 0
    for page_update in page_updates:
        valid_ordering = all(is_valid_page(following_page_tracker, page, page_update) for page in page_update)
        if valid_ordering:
            middle_index = math.floor(len(page_update) / 2)
            total_valid_middle_pages += int(page_update[middle_index])

    return total_valid_middle_pages

def correctly_order_update(following_page_tracker: dict[str, list[str]], page_update: list[str]) -> list[str]:
    """
    Correctly order an incorrectly ordered update
    """
    # Find the number of relevant pages expected to be following each page in the page_update
    following_page_counts = {}
    for page in page_update:
        relevant_following_pages = [following_page
                                    for following_page in following_page_tracker[page] if following_page in page_update]
        following_page_counts[page] = len(relevant_following_pages)

    # Sort descending by relevant page count as a page with more following pages must be earlier
    correct_order = [sorted_page_count[0] for sorted_page_count in
                     sorted(following_page_counts.items(), key=lambda page_count: page_count[1], reverse=True)]

    return correct_order

def part2(following_page_tracker: dict[str, list[str]], page_updates: list[list[str]]) -> int:
    """
    Sum middle page numbers of invalid page update orderings
    """
    total_invalid_middle_pages = 0
    for page_update in page_updates:
        valid_ordering = all(is_valid_page(following_page_tracker, page, page_update) for page in page_update)
        if not valid_ordering:
            correct_ordering = correctly_order_update(following_page_tracker, page_update)
            middle_index = math.floor(len(correct_ordering) / 2)
            total_invalid_middle_pages += int(correct_ordering[middle_index])

    return total_invalid_middle_pages

if __name__ == '__main__':
    following_page_tracker, page_updates = parse_input('data/day5.txt')
    print(following_page_tracker)

    part_1 = part1(following_page_tracker, page_updates)
    print(f'part 1: {part_1}')

    part_2 = part2(following_page_tracker, page_updates)
    print(f'part 2: {part_2}')
