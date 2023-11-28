#%%

input = [
    tuple(map(int, line.strip().split(',')))
    for line in
    open("input.txt", "r").readlines()
]

# %%

def generate_sides(droplet: tuple[int, int, int]):
    x, y, z = droplet
    fbl, fbr, ftl, ftr, bbl, bbr, btl, btr = (
        (x, y, z),
        (x+1, y, z),
        (x, y+1, z),
        (x+1, y+1, z),
        (x, y, z+1),
        (x+1, y, z+1),
        (x, y+1, z+1),
        (x+1, y+1, z+1),
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

unconnected_sides = set()
connected_sides = set()
for droplet in input:
    for side in generate_sides(droplet):
        if side in connected_sides:
            ...
        elif side in unconnected_sides:
            unconnected_sides.remove(side)
            connected_sides.add(side)
        else:
            unconnected_sides.add(side)

print("Part 1:", len(unconnected_sides))

# %%
