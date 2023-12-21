from sln import *
import collections

input = parse_input('input.txt')

def repr(mid, mod: BCastMod | ConjMod | FFMod):
    return (
        mid if isinstance(mod, BCastMod) else
        f'%{mid}' if isinstance(mod, FFMod) else
        f'&{mid}' if isinstance(mod, ConjMod) else
        mid
    )

with open('graph.txt', 'w') as f:
    for mid, mod in input.modules.items():
        for dst_mid in mod.out:
            dst_mod = input.modules.get(dst_mid)
            f.write(f'{repr(mid, mod)} {repr(dst_mid, dst_mod)}\n')
