import os

CURRENT_DIR, _ = os.path.split(__file__)
DATA_FLIE = os.path.join(CURRENT_DIR, 'data.txt')


def data_file_iter(data_file):
    with open(data_file, 'r') as data:
        for box_id in data:
            box_id = box_id.strip()
            if (box_id):
                yield box_id

def part1():
    num_ids_with_duplicated_letter = 0
    num_ids_with_triplicated_letter = 0

    for box_id in data_file_iter(DATA_FLIE):

        box_id_histogram = {}
        for letter in box_id:
            box_id_histogram.setdefault(letter, 0)
            box_id_histogram[letter] += 1
        
        distinct_letter_occurances = {
            occurance
            for letter, occurance in
            box_id_histogram.items()
        }

        if 2 in distinct_letter_occurances:
            num_ids_with_duplicated_letter += 1
        if 3 in distinct_letter_occurances:
            num_ids_with_triplicated_letter += 1

    checksum = (
        num_ids_with_duplicated_letter * 
        num_ids_with_triplicated_letter
    )

    print('Checksum:', checksum)
    return checksum

def calculate_diff(str1, str2):
    """
    Returns a list of the indexes where the 2 strings differ.
    """
    return [
        i for i, letter_tuple in enumerate(zip(str1, str2))
        if letter_tuple[0] != letter_tuple[1]
    ]

def part2():
    all_box_ids = [line for line in data_file_iter(DATA_FLIE)]
    for i in range(len(all_box_ids) - 1):
        for j in range(i + 1, len(all_box_ids)):
            bid1 = all_box_ids[i]
            bid2 = all_box_ids[j]
            diff = calculate_diff(bid1, bid2)
            if len(diff) == 1:
                print('These box IDs differ by 1 character:', (bid1, bid2))
                stripped = bid1[0:diff[0]] + bid1[diff[0]+1:]
                print('Box ID without that character:', stripped)
                return stripped

if __name__ == '__main__':
    part1()
    part2()
