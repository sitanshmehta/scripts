from itertools import combinations

data = [
    ['milk', 'bread', 'eggs'],
    ['bread', 'diapers', 'beer', 'eggs'],
    ['milk', 'diapers', 'bread', 'cola'],
    ['bread', 'milk', 'diapers', 'beer'],
    ['milk', 'bread', 'diapers', 'cola'],
    ['bread', 'milk', 'eggs'],
    ['diapers', 'cola', 'bread'],
    ['milk', 'bread', 'diapers', 'eggs'],
    ['bedsheets', 'lamps', 'pillow'],
]

c = 0.99
support = 2
mp = {}
longest = 0
for array in data:
    if len(array) > longest:
        longest = len(array)
    for word in array:
        mp[word] = mp.get(word, 0) + 1 
        
keys = []
for key, val in mp.items():
    if val >= support:
        keys.append(key)



