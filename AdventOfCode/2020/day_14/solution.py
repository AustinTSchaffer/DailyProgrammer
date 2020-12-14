import re

original_program = open("data.txt").read()
program = re.sub(r"mask = ([X01]{36})", r'mem.mask = "\1"', original_program)

class MemoryPart1:
    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}
    
    def apply_mask(self, value: int) -> int:
        # bitwise-or with value
        ones_mask = int(self.mask.replace("X", "0"), 2)
        # bitwise-and with value
        zeros_mask = int(self.mask.replace("X", "1"), 2)
        return (value | ones_mask) & zeros_mask

    def __setitem__(self, address, value):
        self.memory[address] = self.apply_mask(value)

mem = MemoryPart1()
exec(program)

print("Part 1:", sum(mem.memory.values()))

class MemoryPart2:
    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}

    def apply_mask(self, address: int):
        binary_address_str = [
            (
                addr_bit if mask_bit == "0" else
                "1" if mask_bit == "1" else
                "X"
            )
            for (addr_bit, mask_bit) in
            zip("{0:036b}".format(address), self.mask)
        ]

        def generate_floating_addresses(index, binary_address):
            if index >= len(binary_address):
                yield ""

            elif binary_address[index] != "X":
                yield from (
                    binary_address[index] + remainder
                    for remainder in
                    generate_floating_addresses(index + 1, binary_address)
                )

            else:
                yield from (
                    "1" + remainder for remainder in
                    generate_floating_addresses(index + 1, binary_address)
                )

                yield from (
                    "0" + remainder for remainder in
                    generate_floating_addresses(index + 1, binary_address)
                )

        yield from (
            int(address, 2)
            for address in
            generate_floating_addresses(0, binary_address_str)
        )

    def __setitem__(self, address, value):
        for masked_address in self.apply_mask(address):
            self.memory[masked_address] = value

mem = MemoryPart2()
exec(program)

print("Part 2:", sum(mem.memory.values()))
