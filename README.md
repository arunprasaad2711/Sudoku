# Sudoku
My very own sudoku solver based on human solving strategies and algorithms. While usual sudoku solvers use some form of backtracking, I wanted to make a solver that efficiently solves sudoku using as many human-solving methods as possible.
The coding base is python, and uses simple numpy and vanilla python for the vast majority of the code. The UI is made using Tkinter.

Right now, the code supports classic sudoku, diagonal sudoku, magic square sudoku, chess sudoku variants, windoku, and scalable nxn classic sudoku variants.
Thermos sudoku and sandwich sudoku features are inbuilt, but may not be solveable due to the need for more rigorous logical implementations.

A chain-reaction solver (a sophisticated backtracking solver) is written for a guaranteed solution for solving certain sudokus with advanced logics that are not implemented into the code.
