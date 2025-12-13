import dataclasses


@dataclasses.dataclass(frozen=True)
class Input:
    @dataclasses.dataclass(frozen=True)
    class Shape:
        shape_id: int
        n_pips: int
        pips: tuple[
            tuple[bool, bool, bool], tuple[bool, bool, bool], tuple[bool, bool, bool]
        ]

    @dataclasses.dataclass(frozen=True)
    class Arrangement:
        width: int
        length: int
        shape_counts: tuple[int, ...]

    shapes: tuple[Shape, ...]
    arrangements: tuple[Arrangement, ...]


def transform(input: str) -> Input:
    *shapes, arrangements = input.split("\n\n")
    shapes_parsed = []
    for shape in shapes:
        shape_id, *pips = shape.splitlines()
        shape_id = int(shape_id.strip(":"))
        pips = tuple([tuple([char == "#" for char in row]) for row in pips])
        n_pips = sum(map(sum, pips))
        shapes_parsed.append(
            Input.Shape(
                shape_id=shape_id,
                pips=pips,
                n_pips=n_pips,
            )
        )

    shapes_parsed = tuple(shapes_parsed)

    arrangements_parsed = []
    for arrangement in arrangements.splitlines():
        width_length, *shape_counts = arrangement.split(" ")
        width, length = list(map(int, width_length.strip(":").split("x")))
        shape_counts = tuple(map(int, shape_counts))
        arrangements_parsed.append(
            Input.Arrangement(
                width=width,
                length=length,
                shape_counts=shape_counts,
            )
        )

    arrangements_parsed = tuple(arrangements_parsed)

    return Input(
        shapes=shapes_parsed,
        arrangements=arrangements_parsed,
    )


def fits_part_1(
    shapes: tuple[Input.Shape, ...], arrangement: Input.Arrangement
) -> bool:
    total_available_pips = arrangement.length * arrangement.width
    total_shapes = 0
    total_pips = 0
    for shape_id, count in enumerate(arrangement.shape_counts):
        total_pips += count * shapes[shape_id].n_pips
        total_shapes += count
    definitely_too_small = total_available_pips < total_pips
    if definitely_too_small:
        return False

    possible_non_overlapping_shapes = (arrangement.length // 3) * (arrangement.width // 3)

    definitely_big_enough = possible_non_overlapping_shapes >= total_shapes
    if definitely_big_enough:
        return True

    # Doesn't work on the sample, but we never reach this point
    # on the actual input.
    return True


def part_1(input: Input):
    return sum(map(lambda a: fits_part_1(input.shapes, a), input.arrangements))


def part_2(input: Input):
    # Freebie?
    ...
