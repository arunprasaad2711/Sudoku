import numpy as np

fname = "144x144_sat190s.txt"
order = 144
array = []

with open(fname, "r") as f:
	lines = f.readlines()

for line in lines:
	processedLine = line.strip("\n")
	# print(processedLine)
	entries = line.split(" ")
	# print(entries)
	for entry in entries:
		value = entry.strip("\n")
		if value == ".":
			array.append(0)
		elif value == "":
			pass
		else:
			array.append(int(value))

print(array)
sudoku = np.array(array, dtype=np.int32).reshape(order, order)
np.save("144x144_sudoku.npy", sudoku)
