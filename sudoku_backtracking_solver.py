import numpy as np
import sudoku_puzzles as sp
import time

def safe_entry(matrix, r, c, entry, orderRow=3, orderCol=3, rows=9, cols=9):

    I, J = r // orderRow, c // orderCol
    sg_row_ids = range(I*orderRow, (I+1)*orderRow)
    sg_col_ids = range(J*orderCol, (J+1)*orderCol)

    cr_row_ids = [r]
    cr_col_ids = range(0, cols)

    cc_row_ids = range(0, rows)
    cc_col_ids = [c]

    for i in sg_row_ids:
        for j in sg_col_ids:
            if matrix[i,j] == entry:
                return False
    
    for i in cr_row_ids:
        for j in cr_col_ids:
            if matrix[i,j] == entry:
                return False
    
    for i in cc_row_ids:
        for j in cc_col_ids:
            if matrix[i,j] == entry:
                return False
    
    return True
    
def empty_location(matrix, rows=9, cols=9): 

    for i in range(0, rows): 
        for j in range(0, cols):
            if matrix[i, j] == 0: 
                return [i, j, True]

    return [-1, -1, False]

def bt_sudoku_solver(matrix, orderRow=3, orderCol=3, rows=9, cols=9):
    
    # If there is no unassigned location, we are done
    ID = empty_location(matrix, rows, cols)
    if not ID[2]:
        return True
      
    # Assigning list values to row and col that we got from the above Function  
    r , c, _ = ID
      
    # consider digits 1 to 9 
    for entry in range(1, rows + 1):
          
        # if looks promising
        if safe_entry(matrix, r, c, entry, orderRow, orderCol, rows, cols): 
              
            # make tentative assignment 
            matrix[r, c] = entry 
  
            # return, if success, ya! 
            if bt_sudoku_solver(matrix, orderRow, orderCol, rows, cols):
                return True
  
            # failure, unmake & try again 
            matrix[r, c] = 0
              
    # this triggers backtracking         
    return False 

orderRow = 2
orderCol = 3
rows = orderRow * orderCol
cols = orderRow * orderCol

problem = sp.problem2x3_extreme01
solution = problem.copy()

start = time.time()
valid = bt_sudoku_solver(solution, orderRow, orderCol, rows, cols)
end = time.time()

status = "completely" if valid else "partially"

print("The initial Sudoku")
print(problem)
print(f"The Final Sudoku {status} solved in {end - start} seconds")
print(solution)



