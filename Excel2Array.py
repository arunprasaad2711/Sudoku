import numpy as np
import pandas as pd

fname = "Sudoku64x64.xlsx"
order = 64

df = pd.read_excel(fname, header=None)
df = df.replace(np.nan, " ")
array = df.to_numpy(dtype=str)
print(df)

unique = list(dict.fromkeys(array.flatten()))
print(unique)

sudoku = np.zeros((order, order), dtype=np.int32)

for i in range(order):
	for j in range(order):
		sudoku[i, j] = unique.index(array[i, j])
sudoku[sudoku == 1] = -1
sudoku[sudoku == 0] = 1
sudoku[sudoku == -1] = 0

np.save("64x64_sudoku.npy", sudoku)