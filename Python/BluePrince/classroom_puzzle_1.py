"""
Uses a producers-consumers model to generate permutations of colors across the 12
objects and check those permutations against the scores received by the 3 available
student attempts. We infer that the wagon and hydrant are red based on a 4th given
student attempt.
"""

import itertools
import multiprocessing
import multiprocessing.synchronize
import pprint
import time

COLORS = [
    BLUE := "blue",
    GREEN := "green",
    YELLOW := "yellow",
    ORANGE := "orange",
    RED := "red",
    PURPLE := "purple",
]

OBJECT_NAMES = [
    "flag_mtn",
    "pumpkin",
    "wagon",
    "pond",
    "flag_hourglass",
    "banana",
    "hydrant",
    "lizard",
    "flag_heart",
    "broccoli",
    "blueprint",
    "grapes",
]

KNOWN_COLOR_POSITIONS = list(sorted([
    (OBJECT_NAMES.index("wagon"), RED),
    (OBJECT_NAMES.index("hydrant"), RED),
]))

# There are 2 copies of each color in the final result. We
# are pretty sure of the positioning of some.
AVAILABLE_COLORS = [
    color
    for color in COLORS
    for _ in range(2)
]

for _, color in KNOWN_COLOR_POSITIONS:
    AVAILABLE_COLORS.remove(color)

STUDENT_ATTEMPTS = [
    {
        "correct": 10,
        "config": [
            YELLOW,
            ORANGE,
            RED,
            BLUE,
            ORANGE,
            YELLOW,
            RED,
            GREEN,
            PURPLE,
            GREEN,
            BLUE,
            PURPLE,
        ],
    },
    {
        "correct": 9,
        "config": [
            YELLOW,
            ORANGE,
            RED,
            BLUE,
            GREEN,
            YELLOW,
            RED,
            PURPLE,
            ORANGE,
            GREEN,
            YELLOW,
            PURPLE,
        ],
    },
    {
        "correct": 10,
        "config": [
            BLUE,
            ORANGE,
            RED,
            BLUE,
            PURPLE,
            YELLOW,
            RED,
            RED,
            ORANGE,
            GREEN,
            BLUE,
            PURPLE,
        ],
    },
]


def generate_permutations(
    permutation_queue: multiprocessing.Queue, perm_prefix: str | list[str]
):
    _available_colors = list.copy(AVAILABLE_COLORS)
    if isinstance(perm_prefix, str):
        _available_colors.remove(perm_prefix)
    else:
        for color in perm_prefix:
            _available_colors.remove(color)

    for permutation_tuple in itertools.permutations(_available_colors):
        permutation = (
            [perm_prefix, *permutation_tuple]
            if isinstance(perm_prefix, str)
            else [*perm_prefix, *permutation_tuple]
        )

        for known_position, color in KNOWN_COLOR_POSITIONS:
            permutation.insert(known_position, color)

        permutation_queue.put(permutation)


def check_valid_permutation(
    permutation_queue: multiprocessing.Queue,
    results_queue: multiprocessing.Queue,
    iolock: multiprocessing.synchronize.Lock,
):
    while True:
        _is_valid_permutation = True

        permutation = permutation_queue.get()
        if permutation is None:
            permutation_queue.put(None)
            break

        for attempt in STUDENT_ATTEMPTS:
            num_matching = 0
            for c_1, c_2 in zip(permutation, attempt["config"]):
                if c_1 == c_2:
                    num_matching += 1
            if num_matching != attempt["correct"]:
                _is_valid_permutation = False
                break

        if _is_valid_permutation:
            results_queue.put(permutation)


def main():
    n_consumer_procs = 16
    permutation_prefix_length = 2
    iolock = multiprocessing.Lock()
    permutation_queue = multiprocessing.Queue()
    results_queue = multiprocessing.Queue()

    procs: list[multiprocessing.Process] = []
    permutation_prefixes = {
        perm_prefix
        for prefix_comb in itertools.combinations(AVAILABLE_COLORS, permutation_prefix_length)
        for perm_prefix in itertools.permutations(prefix_comb)
    }

    for perm_prefix in permutation_prefixes:
        procs.append(
            multiprocessing.Process(
                target=generate_permutations, args=(permutation_queue, perm_prefix)
            )
        )

    for proc in procs:
        proc.start()

    with multiprocessing.Pool(
        processes=n_consumer_procs,
        initializer=check_valid_permutation,
        initargs=(permutation_queue, results_queue, iolock),
    ):
        still_generating = True
        while still_generating:
            procs_still_running = [proc for proc in procs if proc.is_alive()]

            if not procs_still_running:
                still_generating = False
                break

            with iolock:
                print(f"{len(procs_still_running)} producers still running")
                latest_item = permutation_queue.get()
                permutation_queue.put(latest_item)
                print(f"Last queue item: {latest_item}")

            time.sleep(5)

        with iolock:
            print("Production complete. Sending shutdown signal to queue.")

        permutation_queue.put(None)

    distinct_results = set()
    while not results_queue.empty():
        distinct_results.add(tuple(results_queue.get()))

    print("Results")
    for result in distinct_results:
        pprint.pprint(dict(zip(OBJECT_NAMES, result)))


if __name__ == "__main__":
    main()
