survey_results = [
    line.strip()
    for line in
    open("survey_results.txt").readlines()
]

total_count = 0
current_group = set()
for line in survey_results:
    if len(line.strip()) == 0:
        total_count += len(current_group)
        current_group = set()
    else:
        current_group = current_group.union(line)

total_count += len(current_group)
print("Part 1:", total_count)

total_count = 0
current_group = set()
first_person_in_group = True
for line in survey_results:
    if len(line.strip()) == 0:
        total_count += len(current_group)
        first_person_in_group = True
    elif first_person_in_group:
        current_group = set(line)
        first_person_in_group = False
    else:
        current_group = current_group.intersection(line)

total_count += len(current_group)
print("Part 2:", total_count)
