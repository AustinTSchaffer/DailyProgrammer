import os
import time

LATEST_ONLY = os.getenv("LATEST_ONLY", "0").strip() == "1"
SPECIFIC_DAY = os.getenv("SPECIFIC_DAY", None)


def main():
    range_ = (
        [int(SPECIFIC_DAY)]
        if SPECIFIC_DAY
        else range(12, 0, -1)
        if LATEST_ONLY
        else range(1, 13)
    )

    for i in range_:
        module_name = f"day_{i:02d}"

        try:
            module = __import__(module_name, fromlist="aoc2025")
        except Exception as e:
            if str(e).startswith("No module named"):
                continue
            raise

        print()
        print("AoC 2025 Day", i)
        actual_input = None
        sample_input = None
        sample_input_p2 = None

        try:
            actual_input = open(f"data/{module_name}.txt").read()
            sample_input = open(f"data/{module_name}.sample.txt").read()
            sample_input_p2 = open(f"data/{module_name}.sample_p2.txt").read()
        except Exception as e:
            ...

        start = time.monotonic()

        try:
            if actual_input:
                actual_input = module.transform(actual_input)
            if sample_input:
                sample_input = module.transform(sample_input)
            if sample_input_p2:
                sample_input_p2 = module.transform(sample_input_p2)
        except Exception as e:
            if "has no attribute 'transform'" not in str(e):
                raise

        if sample_input:
            before = time.monotonic()
            print(
                "\tPart 1 (sample):",
                module.part_1(sample_input),
                "(%.05fs)" % (time.monotonic() - before),
            )

        if actual_input:
            before = time.monotonic()
            print(
                "\tPart 1 (actual):",
                module.part_1(actual_input),
                "(%.05fs)" % (time.monotonic() - before),
            )

        if sample_input_p2 or sample_input:
            before = time.monotonic()
            print(
                "\tPart 2 (sample):",
                module.part_2(sample_input_p2 or sample_input),
                "(%.05fs)" % (time.monotonic() - before),
            )

        if actual_input:
            before = time.monotonic()
            print(
                "\tPart 2 (actual):",
                module.part_2(actual_input),
                "(%.05fs)" % (time.monotonic() - before),
            )

        runtime_s = time.monotonic() - start
        print(f"\tRuntime (computation): {runtime_s:.05f}s")

        if LATEST_ONLY:
            break


if __name__ == "__main__":
    main()
