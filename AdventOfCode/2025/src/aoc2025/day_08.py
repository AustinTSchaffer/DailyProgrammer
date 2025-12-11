def transform(input: str) -> list[tuple[int, int, int]]:
    return [tuple(map(int, line.split(","))) for line in input.splitlines() if line]


def dist(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return sum((v_b - v_a) ** 2 for v_a, v_b in zip(a, b)) ** 0.5


def part_1(input: list[tuple[int, int, int]]):
    n_connections = 10 if len(input) == 20 else 1000

    circuits = {
        jbox: [jbox]
        for jbox in input
    }

    distances = sorted([
        (dist(input[jbox1_idx], input[jbox2_idx]), input[jbox1_idx], input[jbox2_idx])
        for jbox1_idx in range(len(input) - 1)
        for jbox2_idx in range(jbox1_idx+1, len(input))
    ])

    connections = []
    while len(connections) < n_connections:
        distance, jbox1, jbox2 = distances.pop(0)
        connections.append((jbox1, jbox2))
        if jbox1 not in circuits[jbox2]:
            for jbox1_circuit_jbox in circuits[jbox1]:
                circuits[jbox1_circuit_jbox] = circuits[jbox2]
                circuits[jbox2].append(jbox1_circuit_jbox)

    circuit_lens = sorted({
        id(circuit): len(circuit)
        for circuit in circuits.values()
    }.values(), reverse=True)[:3]

    prod = 1
    for circuit_len in circuit_lens:
        prod *= circuit_len
    return prod


def part_2(input: list[tuple[int, int, int]]):
    circuits = {
        jbox: [jbox]
        for jbox in input
    }

    distances = sorted([
        (dist(input[jbox1_idx], input[jbox2_idx]), input[jbox1_idx], input[jbox2_idx])
        for jbox1_idx in range(len(input) - 1)
        for jbox2_idx in range(jbox1_idx+1, len(input))
    ])

    connections = []
    while True:
        distance, jbox1, jbox2 = distances.pop(0)
        connections.append((jbox1, jbox2))
        if jbox1 not in circuits[jbox2]:
            for jbox1_circuit_jbox in circuits[jbox1]:
                circuits[jbox1_circuit_jbox] = circuits[jbox2]
                circuits[jbox2].append(jbox1_circuit_jbox)
            if len(circuits[jbox2]) == len(input):
                break

    return connections[-1][0][0] * connections[-1][1][0]
