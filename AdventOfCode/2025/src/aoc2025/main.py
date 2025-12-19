import os
import time

LATEST = os.getenv("LATEST", "0").strip() == "1"
DAY = os.getenv("DAY", None)


def main():
    total_computation_runtime_ms = 0

    range_ = (
        [int(DAY)]
        if DAY
        else range(12, 0, -1)
        if LATEST
        else range(1, 13)
    )

    for i in range_:
        module_name = f"day_{i:02d}"
        daily_computation_runtime_ms = 0

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
        
        daily_computation_runtime_ms += time.monotonic() - start

        if sample_input:
            before = time.monotonic()
            result = module.part_1(sample_input)
            runtime_ms = (time.monotonic() - before) * 1000
            daily_computation_runtime_ms += runtime_ms
            print(f"\tPart 1 (sample) ({runtime_ms:.06f} ms): {result}")

        if actual_input:
            before = time.monotonic()
            result = module.part_1(actual_input)
            runtime_ms = (time.monotonic() - before) * 1000
            daily_computation_runtime_ms += runtime_ms
            print(f"\tPart 1 (actual) ({runtime_ms:.06f} ms): {result}")

        if sample_input_p2 or sample_input:
            before = time.monotonic()
            result = module.part_2(sample_input_p2 or sample_input)
            runtime_ms = (time.monotonic() - before) * 1000
            daily_computation_runtime_ms += runtime_ms
            print(f"\tPart 2 (sample) ({runtime_ms:.06f} ms): {result}")

        if actual_input:
            before = time.monotonic()
            result = module.part_2(actual_input)
            runtime_ms = (time.monotonic() - before) * 1000
            daily_computation_runtime_ms += runtime_ms
            print(f"\tPart 2 (actual) ({runtime_ms:.06f} ms): {result}")
        
        total_computation_runtime_ms += daily_computation_runtime_ms
        print(f"\tRuntime (computation): {daily_computation_runtime_ms:.06f} ms")

        if LATEST:
            break
    
    print()
    print(f"Total Runtime (computation): {total_computation_runtime_ms:.06f} ms")


if __name__ == "__main__":
    main()
