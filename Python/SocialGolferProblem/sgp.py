NUM_GROUPS = 11
OBJ_PER_GROUP = 4

objects = {
    (original_group, group_object_number)
    for original_group in range(NUM_GROUPS)
    for group_object_number in range(OBJ_PER_GROUP)
}

objects_matched_with = {
    obj: set()
    for obj in objects
}

print(len(objects), "objects")
print(NUM_GROUPS, "groups")
print(OBJ_PER_GROUP, "objects per group")

total_grouping_rounds = 0
while True:
    grouping_round = {
        x: set() for x in range(NUM_GROUPS)
    }

    for obj in objects:
        grouping_round[(obj[0] + (obj[1] * total_grouping_rounds)) % NUM_GROUPS].add(obj)

    print("Round", total_grouping_rounds+1, ": ", grouping_round)

    for group_number, group in grouping_round.items():
        assert len(group) == OBJ_PER_GROUP
        for obj in group:
            for other_obj in group:
                if obj != other_obj:
                    if other_obj in objects_matched_with[obj]:
                        print(obj, "has already matched with", other_obj, "total grouping rounds:", total_grouping_rounds)
                        exit(0)
                    objects_matched_with[obj].add(other_obj)

    total_grouping_rounds += 1
