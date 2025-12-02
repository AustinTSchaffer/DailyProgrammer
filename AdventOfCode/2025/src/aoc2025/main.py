def main():
    for i in range(1, 13):
        module_name = f"day_{i:02d}"

        try:
            module = __import__(module_name, fromlist='aoc2025')
        except Exception as e:
            if str(e).startswith('No module named'):
                continue
            raise

        print()
        print('AoC 2025 Day', i)
        actual_input = None
        sample_input = None

        try:
            actual_input = open(f'data/{module_name}.txt').read()
            sample_input = open(f'data/{module_name}.sample.txt').read()
        except Exception as e:
            print('\t'+str(e))

        try:
            if actual_input:
                actual_input = module.transform(actual_input)
            if sample_input:
                sample_input = module.transform(sample_input)
        except Exception as e:
            if "has no attribute 'transform'" not in str(e):
                raise

        if sample_input:
            print('\tPart 1 (sample):', module.part_1(sample_input))
        if actual_input:
            print('\tPart 1 (actual):', module.part_1(actual_input))
        if sample_input:
            print('\tPart 2 (sample):', module.part_2(sample_input))
        if actual_input:
            print('\tPart 2 (actual):', module.part_2(actual_input))

if __name__ == "__main__":
    main()
