#%%

from sln import *

sample_input = parse_input('sample_input.txt')
input = parse_input('input.txt')

#%%

test_number = 1

# %%

def calc_and_write(input_name: str, steps_taken: int):
    _input = (
        input if input_name == 'input' else
        sample_input if input_name == 'sample' else
        None
    )

    if not input:
        raise ValueError(input_name)

    nnv, explored = num_visitable_bfs(_input, steps_taken)

    min_i = min(n[0] for n in explored)
    max_i = max(n[0] for n in explored)
    min_j = min(n[1] for n in explored)
    max_j = max(n[1] for n in explored)

    with open(f'explored/{input_name}/steps_{steps_taken}.txt', 'w') as f:
        f.write(f'Input name: {input_name}\n')
        f.write(f'Steps taken: {steps_taken}\n')
        f.write(f'Num nodes visited: {nnv}\n\n')

        for i in range(min_i - 1, max_i + 2):
            if i % _input.height == 0:
                f.write('\n')
            for j in range(min_j - 1, max_j + 2):
                if j % _input.width == 0:
                    f.write(' ')
                node = (i, j)
                if node == _input.start:
                    f.write('S')
                elif node in explored and explored[node] % 2 == 0:
                    f.write('O')
                elif (i % _input.height, j % _input.width) in _input.rocks:
                    f.write('#')
                else:
                    f.write('.')
            f.write('\n')

# %%

calc_and_write('input', 100)
calc_and_write('input', 200)
calc_and_write('input', 300)
calc_and_write('input', 400)
calc_and_write('input', 500)

# %%

calc_and_write('sample', 100)
calc_and_write('sample', 200)
calc_and_write('sample', 300)
calc_and_write('sample', 400)
calc_and_write('sample', 500)

# %%
