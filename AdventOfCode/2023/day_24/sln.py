import re
import dataclasses
import timeit
import numpy as np
import itertools
import z3

@dataclasses.dataclass
class PV_Vector_3D:
    p: tuple[int, int, int]
    v: tuple[int, int, int]


@dataclasses.dataclass
class Input:
    pv_vectors: list[PV_Vector_3D]
    search_space: tuple[int, int]

def parse_input(filename: str, search_space: tuple[int, int]) -> Input:
    with open(filename, 'r') as f:
        pv_vectors = []

        for line in f:
            ps, vs = line.split('@')
            ps = ps.split(',')
            vs = vs.split(',')
            pv_vectors.append(PV_Vector_3D(
                p=tuple(map(int, map(str.strip, ps))),
                v=tuple(map(int, map(str.strip, vs))),
            ))

        return Input(
            pv_vectors=pv_vectors,
            search_space=search_space,
        )

def part_1(input: Input):
    p1_ans = 0
    for a_idx in range(len(input.pv_vectors)):
        a = input.pv_vectors[a_idx]
        for b_idx in range(a_idx + 1, len(input.pv_vectors)):
            b = input.pv_vectors[b_idx]

            ans = [b.p[0] - a.p[0], b.p[1] - a.p[1]]
            eqs = [
                (a.v[0], -b.v[0]),
                (a.v[1], -b.v[1]),
            ]

            cv, _, _, _ = np.linalg.lstsq(eqs, ans, rcond=None)
            if cv[0] < 0 or cv[1] < 0:
                continue

            result_x = (cv[0] * a.v[0]) + a.p[0]
            result_y = (cv[0] * a.v[1]) + a.p[1]
            if input.search_space[0] <= result_x <= input.search_space[1] and input.search_space[0] <= result_y <= input.search_space[1]:
                p1_ans += 1

    return p1_ans

def part_2(input: Input):
    s = z3.Solver()

    x, y, z, vx, vy, vz = z3.Ints("x y z vx vy vz")

    for i, pv_vec in enumerate(input.pv_vectors, start=1):
        t = z3.Int(f't_{i}')
        s.add(t > 0)
        s.add(x + (t * vx) - (t * pv_vec.v[0]) == pv_vec.p[0])
        s.add(y + (t * vy) - (t * pv_vec.v[1]) == pv_vec.p[1])
        s.add(z + (t * vz) - (t * pv_vec.v[2]) == pv_vec.p[2])

    assert s.check() == z3.sat
    model = s.model()
    return model.eval(x + y + z)

if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt', (7, 27))
    input = parse_input('input.txt', (200_000_000_000_000, 400_000_000_000_000))

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals=timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals=timeit_globals
    )

    timeit_globals['input'] = sample_input
    time = part_1_timer.timeit(1)
    print('Part 1 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = sample_input
    time = part_2_timer.timeit(1)
    print('Part 2 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
