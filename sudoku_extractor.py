import numpy as np
import pandas as pd

# use this for a proper text file with spacing
# rows = 64
# cols = 64
# fname = "64x64_sudoku.txt"
# npy_fname = "64x64_sudoku.npy"
# sudoku = np.zeros((rows, cols), dtype=np.int32)

# f = open(fname, "r")

# with open(fname, "r") as f:
#     i = 0
#     for line in f.readlines():
#         newline = line.strip('\n')
#         # print(newline)
#         j = 0
#         for entry in newline.split(' '):
#             # print(entry)
#             if entry == '.':
#                 sudoku[i, j] = 0
#             elif entry == '0':
#                 sudoku[i, j] = 100
#             elif entry == ' ':
#                 sudoku[i, j] = -1                
#             else:
#                 sudoku[i, j] = int(entry)
#             j += 1
#         i += 1

# np.save(npy_fname, sudoku)
# print(np.shape(sudoku))

# use this to read data from a spreadsheet

# fname = "36x36-giant-sudoku.xlsx"
# npy_fname = "36x36_sudoku.npy"

# fname = "huge-25x25-sudoku-puzzle.xlsx"
# npy_fname = "25x25_sudoku.npy"

fname = "Sudoku_49x49.xlsx"
npy_fname = "49x49_sudoku.npy"

df = pd.read_excel(fname, header=None)

letters1 = ['k', 'i', 'e', 'h', 'j', 'f', 'c', 'b', 'a', 'g', 'd', 
           "#", "$", "+",
           "1", "2", "3", "4", "5", "6", "7", "8", "9"]

letters2 = [chr(c) for c in range(65, 91)]
# print(letters2)
letters = letters1 + letters2
print(letters)

for col in df.columns:
    df[col] = df[col].fillna(0)

# for col in df.columns:
for entry in letters:
    index1 = letters.index(entry)+1
    df = df.replace(entry, index1)

# print(df)
sudoku = np.array(df, dtype=np.int32)
print(sudoku)
print(np.shape(sudoku))
np.save(npy_fname, sudoku)

