def transform(input: str) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split(","))) for line in input.splitlines()]


def part_1(input: list[tuple[int, int]]):
    return max(
        (abs(input[t1_idx][0] - input[t2_idx][0]) + 1)
        * (abs(input[t1_idx][1] - input[t2_idx][1]) + 1)
        for t1_idx in range(0, len(input) - 1)
        for t2_idx in range(t1_idx + 1, len(input))
    )


def part_2(input: list[tuple[int, int]]):
    compressed_i = {
        i: i_idx for i_idx, i in enumerate(sorted({coord[0] for coord in input}))
    }

    compressed_j = {
        j: j_idx for j_idx, j in enumerate(sorted({coord[1] for coord in input}))
    }

    CG_EXTERIOR = 0
    CG_INTERIOR = 1
    CG_PLACEHOLDER = 2
    compressed_grid = [
        [CG_PLACEHOLDER for _ in range(len(compressed_j))]
        for _ in range(len(compressed_i))
    ]

    # Draw boundary within compressed grid.
    for coord_idx, (coord_i, coord_j) in enumerate(input):
        coord_i_gz = compressed_i[coord_i]
        coord_j_gz = compressed_j[coord_j]
        compressed_grid[coord_i_gz][coord_j_gz] = CG_INTERIOR
        next_coord_i, next_coord_j = input[(coord_idx + 1) % len(input)]
        if next_coord_i == coord_i:
            next_coord_j_gz = compressed_j[next_coord_j]
            diff = next_coord_j_gz - coord_j_gz
            sign = -1 if diff < 0 else +1
            for d_j in range(1, abs(diff)):
                compressed_grid[coord_i_gz][coord_j_gz + (d_j * sign)] = CG_INTERIOR

        elif next_coord_j == coord_j:
            next_coord_i_gz = compressed_i[next_coord_i]
            diff = next_coord_i_gz - coord_i_gz
            sign = -1 if diff < 0 else +1
            for d_i in range(1, abs(diff)):
                compressed_grid[coord_i_gz + (d_i * sign)][coord_j_gz] = CG_INTERIOR

        else:
            raise ValueError()

    # Flood fill from outside edges.
    coordinate_frontier = set(
        [(i, 0) for i in range(len(compressed_i) - 1)]
        + [(i, len(compressed_j) - 1) for i in range(len(compressed_i) - 1)]
        + [(0, j) for j in range(len(compressed_j) - 1)]
        + [(len(compressed_i) - 1, j) for j in range(len(compressed_j) - 1)]
    )

    while coordinate_frontier:
        oc_i, oc_j = coordinate_frontier.pop()
        if compressed_grid[oc_i][oc_j] == CG_PLACEHOLDER:
            compressed_grid[oc_i][oc_j] = CG_EXTERIOR
            for off_i, off_j in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                neigh_i = oc_i + off_i
                if 0 > neigh_i or neigh_i >= len(compressed_i):
                    continue
                neigh_j = oc_j + off_j
                if 0 > neigh_j or neigh_j >= len(compressed_j):
                    continue
                if compressed_grid[neigh_i][neigh_j] == CG_PLACEHOLDER:
                    coordinate_frontier.add((neigh_i, neigh_j))

    ...

    rect_sizes_bboxes = sorted(
        [
            (
                (abs(input[t1_idx][0] - input[t2_idx][0]) + 1)
                * (abs(input[t1_idx][1] - input[t2_idx][1]) + 1),
                min(input[t1_idx][0], input[t2_idx][0]),
                max(input[t1_idx][0], input[t2_idx][0]),
                min(input[t1_idx][1], input[t2_idx][1]),
                max(input[t1_idx][1], input[t2_idx][1]),
            )
            for t1_idx in range(0, len(input) - 1)
            for t2_idx in range(t1_idx + 1, len(input))
        ],
        reverse=True,
    )

    def _contained_in_interior(min_i: int, max_i: int, min_j: int, max_j: int) -> bool:
        compressed_min_i = compressed_i[min_i]
        compressed_max_i = compressed_i[max_i]
        compressed_min_j = compressed_j[min_j]
        compressed_max_j = compressed_j[max_j]

        # Left:
        for i in range(compressed_min_i, compressed_max_i + 1):
            if compressed_grid[i][compressed_min_j] == CG_EXTERIOR:
                return False

        # Right:
        for i in range(compressed_min_i, compressed_max_i + 1):
            if compressed_grid[i][compressed_max_j] == CG_EXTERIOR:
                return False

        # Top:
        for j in range(compressed_min_j, compressed_max_j + 1):
            if compressed_grid[compressed_min_i][j] == CG_EXTERIOR:
                return False

        # Bottom:
        for j in range(compressed_min_j, compressed_max_j + 1):
            if compressed_grid[compressed_max_i][j] == CG_EXTERIOR:
                return False

        return True

    for size, min_i, max_i, min_j, max_j in rect_sizes_bboxes:
        if _contained_in_interior(min_i, max_i, min_j, max_j):
            return size

    raise ValueError()
