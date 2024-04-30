def sep(): print('------------------')

# Formatting output, number formats
sep()
a=1_000
b=1_000_000
s=f'{a:-10d} is {a/b:2.2%}'
print(s)
print('12'.zfill(10))

# Debugging with print
sep()
place='world'
plant='tree'
person='John'
print(f'{place=} {plant=} {person=}')

# hello
sep()
import math
print(f'The value of pi is approximately {math.pi:.3f}.')

# Files
sep()
with open('test.txt', 'w') as f:
    #print('Hello, world!', file=f)
    f.write('Hello, world!')
with open('test.txt', 'r') as f:
    print(f"From file: {f.read()}")

# JSON Files
import json
o = {'a': 1, 'b': 2, 'c': 3}
with open('test.json', 'w') as f:
    json.dump(o, f)
with open('test.json', 'r') as f:
    o = json.load(f)
print(f"From JSON: {o}")
