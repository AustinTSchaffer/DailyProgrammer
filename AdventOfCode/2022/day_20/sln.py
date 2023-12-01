import dataclasses

@dataclasses.dataclass
class Number:
    val: int
    position: int

def simulate(input: list[int], rounds=1) -> list[int]:
    numnums = len(input)

    number_processing_order = [
        Number(n, i)
        for i, n in enumerate(input)
    ]

    number_current_positions = [
        n for n in number_processing_order
    ]

    for _ in range(rounds):
        for num in number_processing_order:
            number_current_positions[num.position] = None
            new_position = (
                num.position + (num.val % (numnums - 1))
            )

            if num.val != 0:
                if (new_position <= 0):
                    new_position = (new_position - 1) % numnums
                elif (new_position >= (numnums - 1)):
                    new_position = (new_position + 1) % numnums

            if new_position == num.position:
                ...
            elif new_position > num.position:
                for idx in range(num.position+1, new_position+1):
                    shifted_num = number_current_positions[idx]
                    number_current_positions[idx] = None
                    shifted_num.position = (shifted_num.position - 1) % numnums
                    number_current_positions[shifted_num.position] = shifted_num
            else:
                for idx in range(num.position-1, new_position-1, -1):
                    shifted_num = number_current_positions[idx]
                    number_current_positions[idx] = None
                    shifted_num.position = (shifted_num.position + 1) % numnums
                    number_current_positions[shifted_num.position] = shifted_num

            number_current_positions[new_position] = num
            num.position = new_position

            for i,n in enumerate(number_current_positions):
                assert n is not None
                assert n.position == i

    return [n.val for n in number_current_positions]

def part1(input):
    result = simulate(input)
    zero_loc = result.index(0)
    print((
        result[(zero_loc + 1000) % len(result)],
        result[(zero_loc + 2000) % len(result)],
        result[(zero_loc + 3000) % len(result)],
    ))

    return (
        result[(zero_loc + 1000) % len(result)] +
        result[(zero_loc + 2000) % len(result)] +
        result[(zero_loc + 3000) % len(result)]
    )

def part2(input):
    input = [ n*811589153 for n in input ]
    result = simulate(input, rounds=10)
    zero_loc = result.index(0)
    print((
        result[(zero_loc + 1000) % len(result)],
        result[(zero_loc + 2000) % len(result)],
        result[(zero_loc + 3000) % len(result)],
    ))

    return (
        result[(zero_loc + 1000) % len(result)] +
        result[(zero_loc + 2000) % len(result)] +
        result[(zero_loc + 3000) % len(result)]
    )


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = [
            int(line.strip())
            for line in f.read().splitlines()
        ]
    
    with open("sample_input.txt", "r") as f:
        sample_input = [
            int(line.strip())
            for line in f.read().splitlines()
        ]

    print("Part 1 (sample):", part1(sample_input))
    print("Part 1 (9945):", part1(input))

    print("Part 2 (sample):", part2(sample_input))
    print("Part 2:", part2(input))
