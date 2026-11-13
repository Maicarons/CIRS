import tomllib, pathlib, json
d = pathlib.Path('src/docs')
ref = tomllib.loads(d.joinpath('extra_strings.toml').read_text(encoding='utf-8'))
def leaves(o, p=''):
    out = {}
    for k,v in o.items():
        key = p + '.' + k if p else k
        if isinstance(v, dict): out.update(leaves(v, key))
        else: out[key] = v
    return out
R = leaves(ref)
files = sorted(d.glob('extra_strings_*.toml'))
res = []
for f in files:
    L = leaves(tomllib.loads(f.read_text(encoding='utf-8')))
    same = sum(1 for k,v in R.items() if L.get(k) == v)
    missing = [k for k in R if k not in L]
    res.append((f.name, len(L), same, len(missing)))
for n,total,same,miss in res: print(f'{n:44s} keys={total:4d} english={same:4d} missing={miss}')
print('TOTAL FILES', len(res))