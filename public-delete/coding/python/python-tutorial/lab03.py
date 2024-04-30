# Lists
programming_langs = ['c', 'python', 'golang', 'java', 'javascript', 'c++']
programming_langs.append('ruby')
programming_langs.sort()
print(programming_langs)
programming_langs.reverse()
print(programming_langs)
programming_langs.pop()
print(programming_langs)

# Stacks
# .pop() and .append () :)

# Queues
from collections import deque
q = deque(programming_langs)
q.append('typescript')
q.append('asm')
q.popleft()
print(q)

# List comprehensions
s0 = [x**2 for x in range(10)]
s1 = list(map(lambda x: x**2, range(10)))
print(s0)
print(s1)

# Tuples
t = 12, 34, 45, 'hello' # simple tuple
nt = t, (1, 2, 3, 4, 5) # nested tuple
print(t[3])
print(nt[1])

# Sets
programming_langs.append('golang')
programming_langs.append('c++')
print(set(programming_langs)) # Unique list of values

# Dictionaries
d = { 'bolivia': 100, 'chile': 200, 'argentina': 300, 'peru': 400 }
d['brazil'] = 500
print("Sorted dict: {}".format(sorted(d)))
print("Peru item from the dict: {}".format(d['peru']))
for k,v in d.items():
    print("country: {} is index {}".format(k, v))
print(d.keys())
