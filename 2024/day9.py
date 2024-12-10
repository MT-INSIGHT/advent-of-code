def parse_input(filename: str) -> tuple[str, str]:
    """
    Parse the input
    """
    with open(filename, 'r') as file:
        data = file.read()

    files = ''.join([char for index, char in enumerate(data) if index % 2 == 0])
    free_spaces = ''.join([char for index, char in enumerate(data) if index % 2 != 0])

    return files, free_spaces

def calculate_checksum_move_blocks(files: str, free_spaces: str) -> int:
    """
    Calculate the checksum, moving file blocks from the back as free spaces allowed
    """
    index = 0
    checksum = 0
    file_front_index = 0
    file_back_index = len(files) - 1
    end_state = ''.join(['0'] * len(files))

    while files != end_state: # Continue until all zeroed out
        # Update checksum for files from front
        num_file_blocks = int(files[file_front_index])
        while num_file_blocks:
            checksum += (index * file_front_index)
            index += 1
            num_file_blocks -= 1
        files = files[:file_front_index] + '0' + files[file_front_index + 1:]  # Update block count
        file_front_index += 1

        # Update checksum for moved blocks from end
        num_free_blocks = int(free_spaces[0])
        free_spaces = free_spaces[1:]  # Pop value from list

        num_blocks_to_move = int(files[file_back_index])
        while num_free_blocks:
            if num_blocks_to_move == 0:  # Already moved all file blocks for this file
                files = files[:file_back_index] + '0' + files[file_back_index + 1:]
                if files == end_state:
                    break
                else:
                    num_blocks_to_move = int(files[file_back_index - 1])
                    file_back_index -= 1
            checksum += (index * file_back_index)
            num_blocks_to_move -= 1
            index += 1
            num_free_blocks -= 1
        files = files[:file_back_index] + str(num_blocks_to_move) + files[file_back_index + 1:]  # Update block count

    return checksum


def calculate_checksum_move_files(files: str, free_spaces: str) -> int:
    """
    Calculate the checksum, moving files from the back to the front as free spaces allowed
    """
    file_chunks = [(file_id, int(size)) for file_id, size in enumerate(files)]
    free_chunks = {file_id_before: [(0, int(size))] for file_id_before, size in enumerate(free_spaces)}

    # Move files into leftmost open spots
    for file_chunk_index in range(len(file_chunks) - 1, 0, -1):  # Search from back to front
        file_id, num_file_blocks = file_chunks[file_chunk_index]
        for file_id_before in range(file_id):  # Only search through free spaces to the left
            num_free_blocks = (free_chunks[file_id_before][-1][1]
                               if file_id_before in free_chunks and free_chunks[file_id_before][-1][0] == 0
                               else 0)
            if num_file_blocks <= num_free_blocks:  # Move file
                # Update current free chunk
                num_free_blocks -= num_file_blocks
                free_chunks[file_id_before] = free_chunks[file_id_before][:-1] + [(file_id, num_file_blocks)]
                if num_free_blocks > 0:
                    free_chunks[file_id_before] += [(0, num_free_blocks)]

                # Merge chunks after moving file
                for preceding_file_id in range(file_id - 1, -1, -1):
                    if free_chunks.get(preceding_file_id) is not None:
                        preceding_free_chunk = free_chunks[preceding_file_id]
                        following_free_chunk = free_chunks[file_id] if file_id in free_chunks else []
                        preceding_ends_in_free_blocks = preceding_free_chunk[-1][0] == 0
                        only_free_blocks_in_following = following_free_chunk and following_free_chunk[0][0] == 0
                        preceding_free_blocks = preceding_free_chunk[-1][1] if preceding_ends_in_free_blocks else 0
                        following_free_blocks = following_free_chunk[0][1] if only_free_blocks_in_following else 0

                        if preceding_ends_in_free_blocks and only_free_blocks_in_following:  # Tracking free blocks
                            merged_chunks = (preceding_free_chunk[:-1]
                                             + [(0, preceding_free_blocks + num_file_blocks + following_free_blocks)]
                                             + following_free_chunk[1:])
                        elif preceding_ends_in_free_blocks > 0:
                            merged_chunks = (preceding_free_chunk[:-1]
                                             + [(0, preceding_free_blocks + num_file_blocks)]
                                             + following_free_chunk)
                        elif only_free_blocks_in_following > 0:
                            merged_chunks = (preceding_free_chunk
                                             + [(0, num_file_blocks + following_free_blocks)]
                                             + following_free_chunk[1:])
                        else:
                            merged_chunks = preceding_free_chunk + [(0, num_file_blocks)] + following_free_chunk
                        free_chunks[preceding_file_id] = merged_chunks
                        break

                if file_id in free_chunks:  # Delete because file has moved
                    del free_chunks[file_id]

                file_chunks.pop(file_chunk_index)  # Remove moved files from file chunks
                break

    # Calculate checksum
    checksum = 0
    index = 0
    for (file_id, num_blocks) in file_chunks:  # Unmoved files
        # Iterate through current file
        while num_blocks:
            checksum += (index * file_id)
            index += 1
            num_blocks -= 1

        # Iterate through following files
        for (following_file_id, num_following_blocks) in free_chunks[file_id]:
            while num_following_blocks:
                checksum += (index * following_file_id)
                index += 1
                num_following_blocks -= 1

    return checksum

if __name__ == '__main__':
    files, free_spaces = parse_input('data/day9.txt')
    calculate_checksum_move_files(files=files, free_spaces=free_spaces)

    part_1 = calculate_checksum_move_blocks(files=files, free_spaces=free_spaces)
    print(f'part 1: {part_1}')

    part_2 = calculate_checksum_move_files(files=files, free_spaces=free_spaces)
    print(f'part 2: {part_2}')