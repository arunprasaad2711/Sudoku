import numpy as np
import itertools

def window_gen(orderRow=3, orderCol=3):

	BaseList = []
	AllList = []

	for i in range(orderRow):
		for j in range(orderCol):
			BaseList.append((i*orderRow, j*orderCol))
	
	print(BaseList)

	for x in range(orderRow):
		for y in range(orderCol):
			list1 = []
			for ID in BaseList:
				i, j = ID
				list1.append((i + x, j + y))
			AllList.append(list1)
	
	for i in range(len(AllList)):
		print(AllList[i])

window_gen(3, 3)

'''
# Personal creation - windoku, superWindoku, antiking, diagonal, centre magic square
-------------------------
| 6 1 4 | 7 9 3 | 8 5 2 |
| 8 7 5 | 6 4 2 | 1 9 3 |
| 2 9 3 | 8 1 5 | 7 4 6 |
-------------------------
| 5 4 1 | 2 7 6 | 3 8 9 |
| 3 8 6 | 9 5 1 | 4 2 7 |
| 9 2 7 | 4 3 8 | 5 6 1 |
-------------------------
| 4 6 8 | 1 2 7 | 9 3 5 |
| 7 3 9 | 5 6 4 | 2 1 8 |
| 1 5 2 | 3 8 9 | 6 7 4 |
-------------------------
'''