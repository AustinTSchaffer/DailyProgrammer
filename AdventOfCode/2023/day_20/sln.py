import re
import dataclasses
import timeit
import copy
import collections
from typing import Iterable
import math

@dataclasses.dataclass
class Pulse:
    val: bool
    src: str
    dst: str

@dataclasses.dataclass
class BCastMod:
    mid: str
    out: tuple[str, ...]

    def recv(self, pulse: Pulse) -> Iterable[Pulse]:
        """
        When a broadcast modules receives a pulse, it sends the same
        pulse to all of its destination modules.
        """
        yield from (
            Pulse(val=pulse.val, src=self.mid, dst=mid)
            for mid in self.out
        )

@dataclasses.dataclass
class FFMod:
    mid: str
    val: bool
    out: tuple[str, ...]

    def recv(self, pulse: Pulse) -> Iterable[Pulse]:
        """
        If a flip-flop module receives a high pulse, it is ignored and nothing
        happens.

        If a flip-flop module receives a low pulse, it flips between on and off.
        If it was off, it turns on and sends a high pulse. If it was on, it turns
        off and sends a low pulse.
        """
        if not pulse.val:
            self.val = not self.val
            yield from (
                Pulse(val=self.val, src=self.mid, dst=mid)
                for mid in self.out
            )

@dataclasses.dataclass
class ConjMod:
    mid: str
    inp: dict[str, bool]
    out: tuple[str, ...]

    def recv(self, pulse: Pulse) -> Iterable[Pulse]:
        """
        When a pulse is received, the conjunction module first updates its
        memory for that input. Then, if it remembers high pulses for all
        inputs, it sends a low pulse; otherwise, it sends a high pulse.
        """
        self.inp[pulse.src] = pulse.val
        val = not all(self.inp.values())
        yield from (
            Pulse(val=val, src=self.mid, dst=mid)
            for mid in self.out
        )

@dataclasses.dataclass
class Input:
    modules: dict[str, BCastMod | FFMod | ConjMod]

MODULE_RE = re.compile(r'(?P<m_type>[%&]?)(?P<m_id>\w+) -> (?P<out>.+)')

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        modules: dict[str, ConjMod | FFMod | BCastMod] = {}
        for line in f:
            if rem := MODULE_RE.match(line):
                kwargs = {
                    "mid": rem['m_id'],
                    "out": tuple(map(str.strip, rem['out'].split(',')))
                }

                modules[rem['m_id']] = (
                    ConjMod(inp={}, **kwargs) if rem['m_type'] == '&' else
                    FFMod(val=False, **kwargs) if rem['m_type'] == '%' else
                    BCastMod(**kwargs)
                )

        for mid, mod in modules.items():
            for dst_mid in mod.out:
                if (dst_mod := modules.get(dst_mid)) and isinstance(dst_mod, ConjMod):
                    dst_mod.inp[mid] = False

        return Input(modules)

def part_1(input: Input):
    input = copy.deepcopy(input)
    queue: collections.deque[Pulse] = collections.deque([])
    pulses_sent = [0, 0]

    for _ in range(1000):
        # There is a module with a single button on it called, aptly, the *button module*.
        # When you push the button, a single *low pulse* is sent directly to the
        # `broadcaster` module.
        queue.append(Pulse(val=False, src='button', dst='broadcaster'))

        while len(queue) > 0:
            pulse = queue.popleft()
            pulses_sent[pulse.val] += 1
            if dst_mod := input.modules.get(pulse.dst):
                queue.extend(dst_mod.recv(pulse))

    return pulses_sent[0] * pulses_sent[1]

def part_2(input: Input):
    input = copy.deepcopy(input)
    queue: collections.deque[Pulse] = collections.deque([])

    # Find the one ConjMod that outputs to `rx`.
    rx_upstream = next(
        mod
        for mod in input.modules.values()
        if 'rx' in mod.out and isinstance(mod, ConjMod)
    )

    # History of the first time that `rx_upstream` received a
    # "high" pulse from each of its inputs.
    rx_upstream_recv_high = {}

    button_presses = 0
    while True:
        # There is a module with a single button on it called, aptly, the *button module*.
        # When you push the button, a single *low pulse* is sent directly to the
        # `broadcaster` module.
        queue.append(Pulse(val=False, src='button', dst='broadcaster'))
        button_presses += 1

        while len(queue) > 0:
            pulse = queue.popleft()
            if pulse.dst == 'rx' and pulse.val == False:
                return button_presses
            if dst_mod := input.modules.get(pulse.dst):
                queue.extend(dst_mod.recv(pulse))
            if pulse.val and pulse.dst == rx_upstream.mid:
                if pulse.src not in rx_upstream_recv_high:
                    rx_upstream_recv_high[pulse.src] = button_presses

        if len(rx_upstream_recv_high) == len(rx_upstream.inp):
            # It feels wrong to once again ignore the potential
            # cases where cycles are offset, but I guess that's
            # part of the magic of AoC. Thanks Eric for all your
            # hard work. <3
            return math.lcm(*rx_upstream_recv_high.values())

if __name__ == '__main__':
    input = parse_input('input.txt')
    ben_input = parse_input('ben_input.txt')
    sample_input_1 = parse_input('sample_input_1.txt')
    sample_input_2 = parse_input('sample_input_2.txt')

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = timeit_globals
    )

    print('Part 1 (sample 1):', part_1(sample_input_1))
    print('Part 1 (sample 2):', part_1(sample_input_2))

    timeit_globals['input'] = ben_input
    time = part_1_timer.timeit(1)
    print('Part 1 (Ben L):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = ben_input
    time = part_2_timer.timeit(1)
    print('Part 2 (Ben L):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
