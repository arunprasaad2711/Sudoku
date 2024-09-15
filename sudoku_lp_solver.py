import numpy as np
import pulp as lp
import sudoku_puzzles as sp
import time as time

def lp_sudoku_solver(matrix, orderRow=3, orderCol=3, antiknight=False):

	Solution = matrix.copy()
	orderRow = orderRow
	orderCol = orderCol

	# number of row/col/subgrids
	nrcs = orderRow * orderCol

	subgrid_IDS = [(sg_row, sg_col) for sg_row in range(0, orderCol)
                            for sg_col in range(0, orderRow)]
	vals = rows = cols = [i for i in range(1, nrcs+1)]

	# find all the subgrid IDS
	subgrid_rcIDS = [[(x, y) for x in range(I*orderRow + 1, (I+1)*orderRow + 1)
							 for y in range(J*orderCol + 1, (J+1)*orderCol + 1)] 
							 for (I, J) in subgrid_IDS]

	# The prob variable is created to contain the problem data
	prob = lp.LpProblem("Sudoku Problem")

	# The decision variables are created
	choices = lp.LpVariable.dicts("Choice", (vals, rows, cols), cat='Binary')

	# A constraint ensuring that only one value can be in each square is created
	for r in rows:
		for c in cols:
			var_list = [choices[v][r][c] for v in vals]
			# print(var_list)
			prob += lp.lpSum(var_list) == 1

	# A constraint ensuring that each row, col, subgrid can have only one value
	for v in vals:

		for r in rows:
			var_list = [choices[v][r][c] for c in cols]
			prob += lp.lpSum(var_list) == 1

		for c in cols:
			var_list = [choices[v][r][c] for r in rows]
			prob += lp.lpSum(var_list) == 1

		for ID in subgrid_rcIDS:
			var_list = [choices[v][r][c] for (r, c) in ID]
			prob += lp.lpSum(var_list) == 1
	
	# adding the initial problem!
	for r in rows:
		for c in cols:
			v = matrix[r-1, c-1]
			if v != 0:
				prob += choices[v][r][c] == 1

	# The problem data is written to an .lp file
	prob.writeLP("Sudoku.lp")

	# The problem is solved using PuLP's choice of Solver
	prob.solve()

	# The status of the solution is printed to the screen
	solved = True if lp.LpStatus[prob.status] == "Optimal" else False

	if solved:
		print("The sudoku is solved successfully")
		valid = True
	else:
		print("Something went wrong")
		valid = False
	for r in rows:
		for c in cols:
			for v in vals:
				if lp.value(choices[v][r][c]) == 1 and Solution[r-1, c-1] == 0:
					Solution[r-1, c-1] = v
	
	return valid, Solution

problem  = sp.problem3_patto_shye
start = time.time()
valid, solution = lp_sudoku_solver(problem, orderRow=3, orderCol=3)
end = time.time()

status = "completely" if valid else "partially"

print("The initial Sudoku")
print(problem)
print(f"The Final Sudoku {status} solved in {end - start} seconds")
print(solution)
