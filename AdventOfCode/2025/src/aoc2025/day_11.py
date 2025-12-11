Graph = dict[str, list[str]]

def transform(input: str) -> Graph:
    graph = Graph()
    for line in input.splitlines():
        src, dests = line.split(':')
        dests = dests.strip().split(' ')
        graph[src] = list(dests)
    return graph

def part_1(input: Graph):
    start = 'you'
    end = 'out'

    _pto_cache: dict[str, int] = {}
    def _paths_to_out(start: str) -> int:
        if start in _pto_cache:
            return _pto_cache[start]
        _pto = 0
        for neighbor in input[start]:
            if neighbor == end:
                _pto += 1
            else:
                _pto += _paths_to_out(neighbor)
        _pto_cache[start] = _pto
        return _pto

    return _paths_to_out(start)

def part_2(input: Graph):
    start = 'svr'
    end = 'out'

    _pto_cache: dict[tuple[str, bool, bool], int] = {}
    def _paths_to_out(start: str, seen_fft: bool, seen_dac: bool) -> int:
        if start == 'out':
            return 0
        if (start, seen_fft, seen_dac) in _pto_cache:
            return _pto_cache[(start, seen_fft, seen_dac)]
        _pto = 0
        for neighbor in input[start]:
            if neighbor == end and seen_fft and seen_dac:
                _pto += 1
            else:
                _pto += _paths_to_out(neighbor, seen_fft or start == 'fft', seen_dac or start == 'dac')
        _pto_cache[(start, seen_fft, seen_dac)] = _pto
        return _pto

    return _paths_to_out(start, False, False)
