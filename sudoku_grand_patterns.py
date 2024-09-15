import numpy as np

'''
A = 1 B = 2 ,, I = 9
'''

pattern = np.array([['I', 'D', 'H', 'C', 'G', 'B', 'F', 'A', 'E'],
                    ['C', 'G', 'B', 'F', 'A', 'E', 'I', 'D', 'H'],
                    ['F', 'A', 'E', 'I', 'D', 'H', 'C', 'G', 'B'],
                    ['D', 'H', 'C', 'G', 'B', 'F', 'A', 'E', 'I'],
                    ['G', 'B', 'F', 'A', 'E', 'I', 'D', 'H', 'C'],
                    ['A', 'E', 'I', 'D', 'H', 'C', 'G', 'B', 'F'],
                    ['H', 'C', 'G', 'B', 'F', 'A', 'E', 'I', 'D'],
                    ['B', 'F', 'A', 'E', 'I', 'D', 'H', 'C', 'G'],
                    ['E', 'I', 'D', 'H', 'C', 'G', 'B', 'F', 'A']], dtype=np.str)

# print(pattern)

pattern1 = np.zeros((9, 9, 9), dtype=np.int32)

for i in range(9):
    maps = {}

    for j in range(i, i+9):
        maps[chr(65 + j - i)] = j%9 + 1 

    # print(maps)

    for k in range(9):
        for l in range(9):
            pattern1[i, k, l] = maps[pattern[k, l]]


print(pattern1[1, :, :])
    


