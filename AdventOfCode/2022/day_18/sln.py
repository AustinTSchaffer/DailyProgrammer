sample_input: list[tuple[int, int, int]] = [
    tuple(map(int, line.strip().split(",")))
    for line in open("sample_input.txt", "r").readlines()
]

input: list[tuple[int, int, int]] = [
    tuple(map(int, line.strip().split(",")))
    for line in open("input.txt", "r").readlines()
]

def visualize_droplet(input: list[tuple[int, int, int]], path_and_prefix="./layers/layer_"):
    min_x = min(c[0] for c in input)
    min_y = min(c[1] for c in input)
    min_z = min(c[2] for c in input)

    max_x = max(c[0] for c in input)
    max_y = max(c[1] for c in input)
    max_z = max(c[2] for c in input)

    output = [
        [[" " for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
        for _ in range(min_z, max_z + 1)
    ]

    for cube in input:
        output[cube[2] - min_z][cube[1] - min_y][cube[0] - min_x] = "#"

    for i, layer in enumerate(output):
        with open(f"{path_and_prefix}{i}.txt", "w") as f:
            for row in layer:
                for val in row:
                    f.write(val)
                f.write("\n")

def generate_faces(voxel: tuple[int, int, int]):
    x, y, z = voxel
    fbl, fbr, ftl, ftr, bbl, bbr, btl, btr = (
        (x, y, z),
        (x + 1, y, z),
        (x, y + 1, z),
        (x + 1, y + 1, z),
        (x, y, z + 1),
        (x + 1, y, z + 1),
        (x, y + 1, z + 1),
        (x + 1, y + 1, z + 1),
    )

    # Front
    yield (fbl, ftl, ftr, fbr)

    # Back
    yield (bbl, btl, btr, bbr)

    # Bottom
    yield (fbl, bbl, bbr, fbr)

    # Top
    yield (ftl, btl, btr, ftr)

    # Left
    yield (fbl, ftl, btl, bbl)

    # Right
    yield (fbr, ftr, btr, bbr)


def generate_voxel_neighbors(voxel: tuple[int, int, int]):    
    yield (voxel[0]+1, voxel[1], voxel[2])
    yield (voxel[0]-1, voxel[1], voxel[2])
    yield (voxel[0], voxel[1]+1, voxel[2])
    yield (voxel[0], voxel[1]-1, voxel[2])
    yield (voxel[0], voxel[1], voxel[2]+1)
    yield (voxel[0], voxel[1], voxel[2]-1)


def part_1(input: list[tuple[int, int, int]]):
    unobscured_faces = set()
    obscured_faces = set()
    for voxel in input:
        for face in generate_faces(voxel):
            if face in obscured_faces:
                ...
            elif face in unobscured_faces:
                unobscured_faces.remove(face)
                obscured_faces.add(face)
            else:
                unobscured_faces.add(face)

    return unobscured_faces


def part_2(input: list[tuple[int, int, int]]):
    unobscured_faces = part_1(input)

    input_as_set = set(input)

    min_x = min(c[0] for c in input)
    min_y = min(c[1] for c in input)
    min_z = min(c[2] for c in input)

    max_x = max(c[0] for c in input)
    max_y = max(c[1] for c in input)
    max_z = max(c[2] for c in input)

    faces_touched_by_flooding = set()

    # TODO: Change this to a BFS instead of whatever this is.
    #       On my specific input, this iterates 5 times.

    something_new_touched_by_flood = True
    flood = {(min_x-1, min_y-1, min_z-1)}
    while something_new_touched_by_flood:
        something_new_touched_by_flood = False
        for x in range(min_x-1, max_x+2):
            for y in range(min_y-1, max_y+2):
                for z in range(min_z-1, max_z+2):
                    new_flood_voxel = (x, y, z)
                    if new_flood_voxel in input_as_set:
                        continue
                    if any(True for neighbor in generate_voxel_neighbors(new_flood_voxel) if neighbor in flood):
                        flood.add(new_flood_voxel)
                        for face in generate_faces(new_flood_voxel):
                            if face in unobscured_faces and face not in faces_touched_by_flooding:
                                something_new_touched_by_flood = True
                                faces_touched_by_flooding.add(face)

    return faces_touched_by_flooding

print("Part 1 (sample):", len(part_1(input)))
print("Part 2 (sample):", len(part_2(input)))
