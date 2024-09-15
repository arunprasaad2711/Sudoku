import tkinter as tk
from tkinter import font, ttk
import numpy as np
import time
from itertools import combinations, product
import sudoku_puzzles as sp
import copy
import sys
#import PySimpleGUI as sg

class Sudoku:

    def __init__(self, master, matrix, orderRow=3, orderCol=3, scale=40, inc=1,
                 max_iter=5, pencil=False, logics=True, gear05=True, 
                 diagonals=False, oddDiagonals=False, evenDiagonals=False, 
                 oddEvenDiagonals=False, evenOddDiagonals=False, windoku=False,
                 thermometer=False, nThermometerSets=0, thermometerSets=[],
                 antiknight=False, nonConsec=False, antiking=False, cr_status=False,
                 queen=False, queendigits=[9], oddKnightEvenQueen=False, evenKnightOddQueen=False,
                 magicSquare=False, nMagicsumSets=0, magicSum_sets=[], magicSumVal=15, evenCorner=True,
                 sandwich=False, row_sums=[], col_sums=[], royal=False, testing=False):

        # Sudoku Puzzle Variables
        self.orderRow = orderRow
        self.orderCol = orderCol
        self.rows = orderRow * orderCol
        self.cols = orderRow * orderCol
        # number of unique numbers
        self.nuns = orderRow * orderCol
        # max number of digits
        self.max_digits = len(str(self.nuns))

        # Special SUDOKU variables
        self.diagonals = diagonals
        self.oddDiagonals = oddDiagonals
        self.oddEvenDiagonals = oddEvenDiagonals
        self.evenDiagonals = evenDiagonals
        self.evenOddDiagonals = evenOddDiagonals
        self.windoku = windoku
        self.antiknight = antiknight
        self.nonConsec = nonConsec
        self.antiking = antiking
        self.queen = queen
        self.oddKNevenQN = oddKnightEvenQueen
        self.evenKNoddQN = evenKnightOddQueen
        self.royal = royal

        # magic sum sets
        self.magicSquare = magicSquare
        self.nMagicsumSets = nMagicsumSets
        self.magicSum_sets = magicSum_sets
        self.magicSumVal = magicSumVal
        self.evenCorner = evenCorner

        # Testing purposes
        self.testing = testing

        if self.magicSquare:
            if self.evenCorner:
                self.modCorner = 0
                self.modEdge = 1
            else:
                self.modCorner = 1
                self.modEdge = 0

        # thermometer sets
        self.thermometer = thermometer
        self.nThermometerSets = nThermometerSets
        self.Thermometer_IDs = thermometerSets

        # Sandwich sudoku sets
        self.sandwich = sandwich
        self.extremes = np.array((1, self.rows), dtype=np.int32)
        self.row_sums = row_sums + sum(self.extremes)
        self.col_sums = col_sums + sum(self.extremes)

        # Graphic variables
        self.scale = scale
        self.offset = scale * 0.5
        self.inc = inc
        self.linewidth_minor = inc
        self.linewidth_major = inc * 3
        self.HEIGHT = self.scale * self.nuns + self.inc
        self.WIDTH = self.scale * self.nuns + self.inc
        self.border = "-"*(self.nuns*(self.max_digits + 1) + 2*self.orderRow + 1)

        # Solver variables
        self.Grids = []
        self.Entries = []
        self.shadowGrids = []
        self.MAX_ITER = max_iter
        self.matrix = matrix.copy()
        self.Solution = np.zeros((self.rows, self.cols), dtype=np.int32)
        self.btMatrix = np.zeros((self.rows, self.cols), dtype=np.int32)
        self.priority_list = []
        self.zeros = 0
        self.global_choices = 0
        self.super_set = [i for i in range(1, self.nuns+1)]
        self.subgrid_IDS = [(sg_row, sg_col) for sg_row in range(0, self.orderCol)
                            for sg_col in range(0, self.orderRow)]
        self.logfilename = "sudoku_log.txt"
        self.pencil = pencil
        self.constraints = 3 * self.nuns
        self.magic_sum = sum(self.super_set)
        self.logics = logics
        self.gear05 = gear05
        self.cr_status = cr_status

        # Font Variables
        self.font = "Helvetica"
        self.numFontstyle = "normal"
        self.btnFontstyle = "normal"
        self.penFontstyle = "normal"
        self.numFontsize = int(scale * 0.5)
        self.btnFontsize = int(scale * 0.3)
        self.penFontsize = int(scale * 0.2)
        self.numFont = font.Font(
            family=self.font, size=self.numFontsize, weight=self.numFontstyle)
        self.btnFont = font.Font(
            family=self.font, size=self.btnFontsize, weight=self.btnFontstyle)
        self.penFont = font.Font(
            family=self.font, size=self.penFontsize, weight=self.penFontstyle)

        # sudoku colours
        self.colour_grids = "#ffffff"
        self.colour_major_border = "#000000"
        # self.colour_minor_border = "#326872"
        self.colour_minor_border = "#aaaaaa"
        # self.colour_minor_border = "#75bbfd"
        # self.colour_major = "#c70039"
        self.colour_major = "#000000"
        # self.colour_minor = "#642e8e"
        # self.colour_minor = "#0000ff"
        self.colour_minor = "#1d6ae5"
        self.colour_btn = "#33b5e5"
        self.colour_markup = "#c70039"
        self.colour_btns = ["#32527b", "#008080", "#888888"]

        # Initializer
        self.pack_grids(master)
        self.draw_lines()
        self.pack_buttons(master)
        self.draw_lines(offset=self.WIDTH)

        # Diagonal IDS
        if self.diagonals or self.oddDiagonals or self.evenDiagonals or self.oddEvenDiagonals or self.evenOddDiagonals:
            if (self.rows - 1) % 2 == 0:
                self.d1_ids = self.diagonalTLBR_ids((self.rows - 1) // 2, 
                                                    (self.rows - 1) // 2)
                self.d2_ids = self.diagonalTRBL_ids((self.rows - 1) // 2, 
                                                    (self.rows - 1) // 2)
            else:
                self.d1_ids = self.diagonalTLBR_ids((self.rows - 1) // 2, 
                                                    (self.rows - 1) // 2)
                self.d2_ids = self.diagonalTRBL_ids((self.rows - 1) // 2, 
                                                    (self.rows - 1) // 2 - 1)
        
        if self.royal:
            self.kings = []
            self.knights = [1, 3, 5, 7, 9]
            self.queens = [2, 4, 6, 8]

        # Setup IDS for windoku
        if self.windoku:

            self.w0_IDs = []
            self.w0_IDs.append(list(product([1, 2, 3], [1, 2, 3])))
            self.w0_IDs.append(list(product([1, 2, 3], [5, 6, 7])))
            self.w0_IDs.append(list(product([5, 6, 7], [1, 2, 3])))
            self.w0_IDs.append(list(product([5, 6, 7], [5, 6, 7])))
            self.w0_IDs.append(list(product([1, 2, 3], [0, 4, 8])))
            self.w0_IDs.append(list(product([5, 6, 7], [0, 4, 8])))
            self.w0_IDs.append(list(product([0, 4, 8], [1, 2, 3])))
            self.w0_IDs.append(list(product([0, 4, 8], [5, 6, 7])))
            self.w0_IDs.append(list(product([0, 4, 8], [0, 4, 8])))
        
        if self.queen:
            self.queens = queendigits

        if self.oddKNevenQN:
            self.knights = [i for i in self.super_set if i % 2 == 1]
            self.queens  = [i for i in self.super_set if i % 2 == 0]
        
        if self.evenKNoddQN:
            self.queens  = [i for i in self.super_set if i % 2 == 1]
            self.knights = [i for i in self.super_set if i % 2 == 0]

    def pack_grids(self, master):

        self.canvas = tk.Canvas(master, width=self.WIDTH,
                                height=self.HEIGHT, bg=self.colour_grids)
        self.canvas.grid(row=0, column=0)

        # self.entriesCanvas = tk.Canvas(master, width=self.WIDTH,
        #                         height=self.HEIGHT, bg=self.colour_grids)
        # self.entriesCanvas.grid(row=0, column=1)

        for i in range(0, self.rows):
            row_grids = []
            # row_entries = []
            for j in range(0, self.cols):
                grid = {}
                # entry = {}
                grid["choices"] = self.super_set.copy()
                grid["num_choices"] = len(grid["choices"])
                grid["label"] = self.canvas.create_text(self.inc + self.offset + j * self.scale,
                                                        self.inc + self.offset + i * self.scale,
                                                        text='',
                                                        fill=self.colour_major,
                                                        font=self.numFont)
                grid["I"] = i // self.orderRow
                grid["J"] = j // self.orderCol
                row_grids.append(grid)
                
                # entry["entry"] = tk.Entry(self.entriesCanvas)
                # entry["v"] = entry["entry"].get()

                # entry["entry"].place(x=j*self.scale + 5.0*self.inc, 
                #                     y=i*self.scale + 5.0*self.inc, 
                #                     width=2*self.offset - 5.0*self.inc, 
                #                     height=2*self.offset - 5.0*self.inc)
                # entry["entry"].config({"background": self.colour_grids})
                # row_entries.append(entry)

            self.Grids.append(row_grids)
            # self.Entries.append(row_entries)

    def draw_lines(self, offset=0):
        # Draw horizontal and vertical lines
        for i in range(0, self.rows + 1):

            colour01 = self.colour_major_border if i % self.orderRow == 0 else self.colour_minor_border
            colour02 = self.colour_major_border if i % self.orderCol == 0 else self.colour_minor_border
            linewidth01 = self.linewidth_major if i % self.orderRow == 0 else self.linewidth_minor
            linewidth02 = self.linewidth_major if i % self.orderCol == 0 else self.linewidth_minor

            x0 = self.inc
            y0 = self.scale * i + self.inc
            x1 = self.WIDTH
            y1 = self.scale * i + self.inc
            self.canvas.create_line(
                x0, y0, x1, y1, fill=colour01, width=linewidth01)
            # self.entriesCanvas.create_line(
            #     x0+offset, y0, x1+offset, y1, fill=colour01, width=linewidth01)

            x0 = self.scale * i + self.inc
            y0 = self.inc
            x1 = self.scale * i + self.inc
            y1 = self.HEIGHT
            self.canvas.create_line(
                x0, y0, x1, y1, fill=colour02, width=linewidth02)
            # self.entriesCanvas.create_line(
            #     x0+offset, y0, x1+offset, y1, fill=colour02, width=linewidth02)

    def pack_buttons(self, master):

        set_problem = tk.Button(master, text="Set", fg=self.colour_btns[0], bg=self.colour_grids,
                                font=self.btnFont, command=self.set_problem)
        set_problem.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        set_problem.grid(row=1, column=0, sticky=tk.W)

        solve = tk.Button(master, text="Solve", fg=self.colour_btns[1], bg=self.colour_grids,
                          font=self.btnFont, command=self.solve)
        solve.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        solve.grid(row=1, column=0, sticky=tk.N)

        reset = tk.Button(master, text="Reset", fg=self.colour_btns[2], bg=self.colour_grids,
                          font=self.btnFont, command=self.reset)
        reset.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        reset.grid(row=1, column=0, sticky=tk.E)

        print_status = tk.Button(master, text="Status", fg=self.colour_btns[0], bg=self.colour_grids,
                                 font=self.btnFont, command=self.print_sudoku_status)
        print_status.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        print_status.grid(row=2, column=0, sticky=tk.W)

        markup = tk.Button(master, text="Markup", fg=self.colour_btns[1], bg=self.colour_grids,
                           font=self.btnFont, command=self.toggle_markup)
        markup.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        markup.grid(row=2, column=0, sticky=tk.N)

        status_log = tk.Button(master, text="Log", fg=self.colour_btns[2], bg=self.colour_grids,
                               font=self.btnFont, command=self.log_sudoku_status)
        status_log.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        status_log.grid(row=2, column=0, sticky=tk.E)

        # npair = tk.Button(master, text="npairs", fg=self.colour_btns[1], bg=self.colour_grids,
        #                   font=self.btnFont, command=self.pair_finder_full)
        # npair.configure(
        #     width=10, activebackground=self.colour_btn, relief=tk.RAISED)
        # npair.grid(row=3, column=0, sticky=tk.N)

        # lp_solver = tk.Button(master, text="ILP Solve", fg=self.colour_btns[1], bg=self.colour_grids,
        #                    font=self.btnFont, command=self.lp_sudoku_solver)
        # lp_solver.configure(
        #     width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        # lp_solver.grid(row=3, column=0, sticky=tk.N)

        # bt_solver = tk.Button(master, text="BT Solve", fg=self.colour_btns[2], bg=self.colour_grids,
        #                    font=self.btnFont, command=self.bt_sudoku_solver)
        # bt_solver.configure(
        #     width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        # bt_solver.grid(row=3, column=0, sticky=tk.E)

        cr_solver = tk.Button(master, text="CRSolve", fg=self.colour_btns[0], bg=self.colour_grids,
                           font=self.btnFont, command=self.chain_reaction)
        cr_solver.configure(
            width=5, activebackground=self.colour_btn, relief=tk.RAISED)
        cr_solver.grid(row=3, column=0, sticky=tk.W)

        # blocker = tk.Button(master, text="Blocker", fg=self.colour_btns[2], bg=self.colour_grids,
        #                     font=self.btnFont, command=self.pair_finder_full)
        # blocker.configure(
        #     width=10, activebackground=self.colour_btn, relief=tk.RAISED)
        # blocker.grid(row=3, column=0, sticky=tk.E)

        # button1_window = canvas1.create_window(10, 10, anchor=NW, window=button1)

    def set_problem(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):

                if self.matrix[i, j] != 0:
                    self.canvas.itemconfigure(
                        self.Grids[i][j]["label"], text=self.matrix[i, j],
                        fill=self.colour_major, font=self.numFont)
                    self.Grids[i][j]["choices"] = []
                    self.Grids[i][j]["num_choices"] = 0
        
        if self.thermometer:
            for setnum in range(0, self.nThermometerSets):
                IDs = self.Thermometer_IDs[setnum]
                lenIDs = len(IDs)
                # print(IDs, lenIDs)
                for i in range(0, lenIDs):
                    x, y = IDs[i]
                    minVal = i + 1
                    maxVal = max(self.super_set) - lenIDs + i + 2
                    self.Grids[x][y]["choices"] = list(range(minVal, maxVal))
                    self.Grids[x][y]["num_choices"] = len(self.Grids[x][y]["choices"])
                    # print(self.Grids[x][y]["choices"])

        if self.magicSquare:
                
            for setnum in range(0, self.nMagicsumSets):
                IDs = self.magicSum_sets[setnum]
                # print(flat_IDs)
                x0, y0 = IDs[4]
                self.Grids[x0][y0]["choices"] = [5]
                self.Grids[x0][y0]["num_choices"] = 1

                for i in range(0, len(IDs)):
                    x, y = IDs[i]
                    if i % 2 == self.modCorner and i != 4 and self.matrix[x, y] == 0:
                        self.Grids[x][y]["choices"] = [entry for entry in self.super_set if entry % 2 == self.modCorner]
                        self.Grids[x][y]["num_choices"] = len(self.Grids[x][y]["choices"])
                    if i % 2 == self.modEdge and self.matrix[x, y] == 0:
                        self.Grids[x][y]["choices"] = [entry for entry in self.super_set if entry % 2 == self.modEdge]
                        self.Grids[x][y]["num_choices"] = len(self.Grids[x][y]["choices"])
                    # print(x, y, self.Grids[x][y]["choices"])
        
        if self.oddDiagonals:
            for entry in self.super_set:
                if entry % 2 == 0:
                    self.fastScanner_gen(self.d1_ids, entry, solve=False)
                    self.fastScanner_gen(self.d2_ids, entry, solve=False)
        
        if self.evenDiagonals:
            for entry in self.super_set:
                if entry % 2 == 1:
                    self.fastScanner_gen(self.d1_ids, entry, solve=False)
                    self.fastScanner_gen(self.d2_ids, entry, solve=False)
        
        if self.evenOddDiagonals:
            for entry in self.super_set:
                if entry % 2 == 1:
                    self.fastScanner_gen(self.d1_ids, entry, solve=False)
                if entry % 2 == 0:
                    self.fastScanner_gen(self.d2_ids, entry, solve=False)

        if self.oddEvenDiagonals:
            for entry in self.super_set:
                if entry % 2 == 0:
                    self.fastScanner_gen(self.d1_ids, entry, solve=False)
                if entry % 2 == 1:
                    self.fastScanner_gen(self.d2_ids, entry, solve=False)

        if self.testing:
            print("Testing!")
            self.Grids[6][6]["choices"].remove(2)
            # self.Grids[2][1]["choices"].remove(2)
            self.Grids[6][6]["num_choices"] = len(self.Grids[6][6]["choices"])
            # self.Grids[2][1]["num_choices"] = len(self.Grids[2][1]["choices"])

        self.Solution = self.matrix.copy()
        self.fastScanner_full(solve=False)
        self.count_zeros(self.Solution)

    def markup(self, i, j, choices):

        counter = 0
        pencil_mark = " "

        order = max(self.orderRow, self.orderCol)

        for entry in self.super_set:

            if counter > 0 and counter % order == 0:
                pencil_mark += "\n "

            if entry in choices:
                pencil_mark += f"{entry} "
            else:
                pencil_mark += "  "
            counter += 1

        self.canvas.itemconfigure(self.Grids[i][j]["label"], text=pencil_mark,
                                  fill=self.colour_markup, font=self.penFont)

    def reset(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.canvas.itemconfigure(
                    self.Grids[i][j]["label"], text="")
                self.Grids[i][j]["choices"] = self.super_set.copy()
                self.Grids[i][j]["num_choices"] = len(self.super_set)
        self.Solution = np.zeros((self.rows, self.cols), dtype=np.int32)
        self.btMatrix = np.zeros((self.rows, self.cols), dtype=np.int32)

    def grid_markup(self):

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.Solution[i, j] == 0:
                    self.markup(i, j, self.Grids[i][j]["choices"])

    def reset_markup(self):

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.Solution[i, j] == 0:
                    self.canvas.itemconfigure(self.Grids[i][j]["label"], text="",
                                              fill=self.colour_major, font=self.penFont)

    def toggle_markup(self):

        self.pencil = ~self.pencil
        if self.pencil:
            self.fastScanner_full(solve=False)
            self.grid_markup()
        else:
            self.reset_markup()

    def log_sudoku_status(self):

        fp = open(self.logfilename, "w")

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                grid = self.Grids[i][j]
                face_value = self.Solution[i, j]
                if face_value == "":
                    face_value = 0
                print(f"Grid {i+1, j+1}, Facevalue = {face_value}", file=fp)
                print(f"choices = {grid['choices']}, num_choices = {grid['num_choices']}", file=fp)
        print("The Sudoku at this stage is:", file=fp)
        self.print_sudoku(self.Solution, file=fp)
        fp.close()

    def print_sudoku_status(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                grid = self.Grids[i][j]
                face_value = self.Solution[i, j]
                if face_value == "":
                    face_value = 0
                print(f"Grid {i+1, j+1}, Facevalue = {face_value}")
                print(f"choices = {grid['choices']}, num_choices = {grid['num_choices']}")
        print("The Sudoku at this stage is:")
        self.print_sudoku(self.Solution)

    def count_zeros(self, Solution, forced_chain=False):
        zeros = 0
        choices = 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if Solution[i, j] == 0:
                    zeros += 1
                    choices += self.Grids[i][j]["num_choices"]
        self.zeros = zeros
        if forced_chain:
            return True if zeros == 0 else False
        else:
            self.global_choices = choices

    def update_cell(self, i, j, entry, forced_chain=False):

        # print(f"Updating Entry {entry} in grid {i, j}")
        # writing it into the sudoku
        if forced_chain:
            # print(f"Updating Entry {entry} in grid {i, j} in forced chain")
            self.btMatrix[i, j] = int(entry)
        else:
            self.Solution[i, j] = int(entry)
            self.zeros -= 1
            self.canvas.itemconfigure(self.Grids[i][j]["label"], text=entry, 
                fill=self.colour_minor, font=self.numFont)
        self.Grids[i][j]["choices"] = []
        self.Grids[i][j]["num_choices"] = 0
        # print(f"Calling SRC after filling entry {entry} in cell {i, j}")
        self.fastScanner_SRC(
            self.Grids[i][j]["I"], self.Grids[i][j]["J"], i, j, entry, forced_chain=forced_chain)

    def antiknight_IDs(self, i, j):

        IDS = []

        if i - 2 >= 0:
            if j - 1 >= 0:
                IDS.append((i - 2, j - 1))
            if j + 1 < self.cols:
                IDS.append((i - 2, j + 1))
        if i - 1 >= 0:
            if j - 2 >= 0:
                IDS.append((i - 1, j - 2))
            if j + 2 < self.cols:
                IDS.append((i - 1, j + 2))
        if i + 2 < self.rows:
            if j - 1 >= 0:
                IDS.append((i + 2, j - 1))
            if j + 1 < self.cols:
                IDS.append((i + 2, j + 1))
        if i + 1 < self.rows:
            if j - 2 >= 0:
                IDS.append((i + 1, j - 2))
            if j + 2 < self.cols:
                IDS.append((i + 1, j + 2))

        return IDS
    
    def nonConsec_IDs(self, i, j):

        IDS = []

        if i - 1 >= 0:
            IDS.append((i - 1, j))
        if i + 1 < self.rows:
            IDS.append((i + 1, j))
        if j - 1 >= 0:
            IDS.append((i, j - 1))
        if j + 1 < self.cols:
            IDS.append((i, j + 1))

        return IDS
    
    def antiking_IDs(self, i, j):

        IDS = []

        # Top Row
        if i - 1 >= 0:
            IDS.append((i - 1, j))
            if j - 1 >= 0:
                IDS.append((i - 1, j - 1))
            if j + 1 < self.cols:
                IDS.append((i - 1, j + 1))

        # Middle Row
        if j - 1 >= 0:
            IDS.append((i, j - 1))
        if j + 1 < self.cols:
            IDS.append((i, j + 1))
        
        # Bottom Row
        if i + 1 < self.rows:
            IDS.append((i + 1, j))
            if j - 1 >= 0:
                IDS.append((i + 1, j - 1))
            if j + 1 < self.cols:
                IDS.append((i + 1, j + 1))

        return IDS
    
    def diagonalTRBL_ids(self, i, j):

        IDS = []

        if i < self.rows and i >= 0 and j < self.cols and j >= 0:
            IDS.append((i, j))

        x, y = i, j
        
        while x - 1 >= 0 and y + 1 <= self.cols - 1:
            IDS.append((x - 1, y + 1))
            x -= 1
            y += 1
        
        x, y = i, j

        while x + 1 <= self.rows - 1 and y - 1 >=  0:
            IDS.append((x + 1, y - 1))
            x += 1
            y -= 1
        
        return IDS

    def diagonalTLBR_ids(self, i, j):

        IDS = []

        if i < self.rows and i >= 0 and j < self.cols and j >= 0:
            IDS.append((i, j))

        x, y = i, j
        
        while x - 1 >= 0 and y - 1 >= 0:
            IDS.append((x - 1, y - 1))
            x -= 1
            y -= 1
        
        x, y = i, j

        while x + 1 <= self.rows - 1 and y + 1 <=  self.cols - 1:
            IDS.append((x + 1, y + 1))
            x += 1
            y += 1
        
        return IDS

    def fastScanner_gen(self, IDs, entry, solve=True, forced_chain=False):

        # for row_id, col_id, in zip(row_ids, col_ids):
        for (row_id, col_id) in IDs:
                
            # print(f"Scanning cell {row_id, col_id} for {entry}")
            if self.Grids[row_id][col_id]["num_choices"] > 1:

                # print(f"Trying to remove {entry} in {self.Grids[row_id][col_id]['choices']} at Grid {row_id, col_id}")
                try:
                    self.Grids[row_id][col_id]["choices"].remove(entry)
                    self.Grids[row_id][col_id]["num_choices"] -= 1
                except ValueError:
                    pass
                # print(f"Removed {entry} in {self.Grids[row_id][col_id]['choices']} at Grid {row_id, col_id}")

                if solve and self.Grids[row_id][col_id]["num_choices"] == 1:
                    # print(f"Found a naked entry {self.Grids[row_id][col_id]['num_choices']} in cell {row_id, col_id}")
                    self.update_cell(
                        row_id, col_id, self.Grids[row_id][col_id]["choices"][0], forced_chain)

    def fastScanner_SRC(self, I, J, i, j, entry, solve=True, forced_chain=False):

        # Find IDS for row and column in subgrid
        # I = 0 range(0, 3); I = 1 range(3, 6)
        sg_row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
        sg_col_ids = range(J*self.orderCol, (J+1)*self.orderCol)
        IDs = list(product(sg_row_ids, sg_col_ids))
        # print(f"Scanning SG IDs for i, j, I, J = {i, j, I, J}")
        self.fastScanner_gen(IDs, entry, solve, forced_chain)

        # Common row IDS
        cr_row_ids = [i]
        cr_col_ids = range(0, self.cols)
        IDs = list(product(cr_row_ids, cr_col_ids))
        # print(f"Scanning ROW IDs for i, j, I, J = {i, j, I, J}")
        self.fastScanner_gen(IDs, entry, solve, forced_chain)

        # Common col IDS
        cc_row_ids = range(0, self.rows)
        cc_col_ids = [j]
        IDs = list(product(cc_row_ids, cc_col_ids))
        # print(f"Scanning COL IDs for i, j, I, J = {i, j, I, J}")
        self.fastScanner_gen(IDs, entry, solve, forced_chain)

        if self.antiknight:
            KIDS = self.antiknight_IDs(i, j)
            self.fastScanner_gen(KIDS, entry, solve, forced_chain)
        
        if self.antiking:
            KIDS = self.antiking_IDs(i, j)
            self.fastScanner_gen(KIDS, entry, solve, forced_chain)
        
        if self.nonConsec:
            KIDS = self.nonConsec_IDs(i, j)
            if entry + 1 <= self.rows:
                self.fastScanner_gen(KIDS, entry + 1, solve, forced_chain)
            if entry - 1 >  0:
                self.fastScanner_gen(KIDS, entry - 1, solve, forced_chain)
        
        if self.queen and entry in self.queens:
            d1_ids = self.diagonalTLBR_ids(i, j)
            d2_ids = self.diagonalTRBL_ids(i, j)
            self.fastScanner_gen(d1_ids, entry, solve, forced_chain)
            self.fastScanner_gen(d2_ids, entry, solve, forced_chain)
        
        if self.oddKNevenQN or self.evenKNoddQN:
            if entry in self.knights:
                KIDS = self.antiknight_IDs(i, j)
                self.fastScanner_gen(KIDS, entry, solve, forced_chain)
            
            if entry in self.queens:
                d1_ids = self.diagonalTLBR_ids(i, j)
                d2_ids = self.diagonalTRBL_ids(i, j)
                self.fastScanner_gen(d1_ids, entry, solve, forced_chain)
                self.fastScanner_gen(d2_ids, entry, solve, forced_chain)
        
        if self.royal:
            if entry in self.knights:
                KIDS = self.antiknight_IDs(i, j)
                self.fastScanner_gen(KIDS, entry, solve, forced_chain)
            
            if entry in self.queens:
                d1_ids = self.diagonalTLBR_ids(i, j)
                d2_ids = self.diagonalTRBL_ids(i, j)
                self.fastScanner_gen(d1_ids, entry, solve, forced_chain)
                self.fastScanner_gen(d2_ids, entry, solve, forced_chain)
            
            if entry in self.kings:
                KIDS = self.antiking_IDs(i, j)
                self.fastScanner_gen(KIDS, entry, solve, forced_chain)
        
    def fastScanner_full(self, solve=True, forced_chain=False):

        for i in range(0, self.rows):
            for j in range(0, self.cols):

                num_choices = self.Grids[i][j]["num_choices"]

                # removes all duplicate entries in row/column/subgrid
                if num_choices == 0:
                    # entry = int(self.canvas.itemcget(
                    #     self.Grids[i][j]["label"], "text"))
                    if forced_chain:
                        entry = self.btMatrix[i, j]
                    else:
                        entry = self.Solution[i, j]
                    
                    I = self.Grids[i][j]["I"]
                    J = self.Grids[i][j]["J"]
                    # print(f"Grid {i,j}, Facevalue = {entry}, choices = {self.Grids[i][j]['choices']}, num_choices = {num_choices}")
                    # print(f"Subgrid {I, J}")
                    self.fastScanner_SRC(I, J, i, j, entry, solve, forced_chain)
                
                if solve and num_choices == 1:
                    # print(f"Found a naked entry {self.Grids[i][j]['choices'][0]} in fast scanner.")
                    self.update_cell(i, j, self.Grids[i][j]["choices"][0], forced_chain)
        
        if self.windoku:
            for i in range(0, len(self.w0_IDs)):
                self.specialScanner(self.w0_IDs[i], solve, forced_chain)
        
        if self.diagonals:
            self.specialScanner(self.d1_ids, solve, forced_chain)
            self.specialScanner(self.d2_ids, solve, forced_chain)
        
        if self.magicSquare:
            for setnum in range(0, self.nMagicsumSets):

                IDs = self.magicSum_sets[setnum]

                rows = []
                rows.append([IDs[i] for i in (0, 1, 2)])
                rows.append([IDs[i] for i in (3, 4, 5)])
                rows.append([IDs[i] for i in (6, 7, 8)])
                rows.append([IDs[i] for i in (0, 3, 6)])
                rows.append([IDs[i] for i in (1, 4, 7)])
                rows.append([IDs[i] for i in (2, 5, 8)])
                rows.append([IDs[i] for i in (0, 4, 8)])
                rows.append([IDs[i] for i in (2, 4, 6)])
                # print(flat_ids)
                
                # Row/Col/Diagonal sum checker
                for row in rows:
                    # print(f"scanning through row = {row}")
                    self.magicSumSolver(row, solve, forced_chain)
                
                # removing filled entries in the magic square
                self.specialScanner(IDs, solve, forced_chain)
                
    def magicSumSolver(self, row, solve=True, forced_chain=False):     
        # print(f"scanning through col = {row}")
        rowSum = 0
        empty_entry_indices = []
        for x, y in row:
            # print(x, y)
            if forced_chain:
                entry = self.btMatrix[x, y]
            else:
                entry = self.Solution[x, y]
            if entry != 0:
                rowSum += entry
            else:
                empty_entry_indices.append((x, y))
            
        if len(empty_entry_indices) == 1 and solve:
            # print(f"Found a break in row/col/dia = {row} and empty cell = {empty_entry_indices}")
            newEntry = self.magicSumVal - rowSum
            i, j = empty_entry_indices[0]
            self.update_cell(i, j, newEntry, forced_chain)
        
        if len(empty_entry_indices) == 2 and solve:
            newSplit = self.magicSumVal - rowSum
            # print(f"Found a  2-empty cell break in row/col/dia = {row} and new split = {newSplit}")
            i1, j1 =  empty_entry_indices[0]
            i2, j2 =  empty_entry_indices[1]
            choices1 = self.Grids[i1][j1]["choices"]
            choices2 = self.Grids[i2][j2]["choices"]

            nChoices1 = set()
            nChoices2 = set()

            pairs = list(product(choices1, choices2))
            for a, b in pairs:
                if a + b == newSplit:
                    nChoices1.add(a)
                    nChoices2.add(b)
            
            self.Grids[i1][j1]["choices"] = sorted(nChoices1)
            self.Grids[i2][j2]["choices"] = sorted(nChoices2)
            self.Grids[i1][j1]["num_choices"] = len(nChoices1)
            self.Grids[i2][j2]["num_choices"] = len(nChoices2)
    
    def specialScanner(self, IDs, solve=True, forced_chain=False):

        for i, j in IDs:

            num_choices = self.Grids[i][j]["num_choices"]

            if solve and num_choices == 1:
                self.update_cell(i, j, self.Grids[i][j]["choices"][0], forced_chain)

            if num_choices == 0:
                if forced_chain:
                    entry = self.btMatrix[i, j]
                else:
                    entry = self.Solution[i, j]
                
                # print(f"Found an entry = {entry} for a special scan!")
                self.fastScanner_gen(IDs, entry, solve, forced_chain)

    def update_entries(self, row_ids, col_ids):
        # print(f"Row IDS = {row_ids} Col IDS = {col_ids}")
        IDs = list(product(row_ids, col_ids))
        entries = self.core(IDs)
        return entries

    def core(self, IDs):

        # Create an entry and an indices dictionary
        entries = {}
        for item in self.super_set:
            entries[item] = {}
            entries[item]["count"] = 0
            entries[item]["IDS"] = []

        for i, j in IDs:
            # face_value = self.canvas.itemcget(self.Grids[i][j]["label"], "text")
            # print(f"(i,j) = {i,j}")
            if self.Grids[i][j]["num_choices"] == 0:
                # print(f"Skipping grid {i+1, j+1} as it is filled with {face_value}")
                pass
            else:
                options = self.Grids[i][j]["choices"]
                # print(f"In grid {i+1, j+1} the choices are {options}")
                for option in options:
                    # print(f"In grid {i+1, j+1}, updating option {option} to options")
                    # print(f"Before updating option {option}, the entry value is {entries[option]}")
                    entries[option]["count"] += 1
                    entries[option]["IDS"].append((i, j))
                    # print(f" After updating option {option}, the entry value is {entries[option]}")

        return entries
    
    def update_entries_IDs(self, IDs):
        entries = self.core(IDs)
        return entries

    def specialDeepScanner(self, IDs, gear03=True, forced_chain=False):
        # print(f"Calling diagonal {IDs}")
        entries = self.update_entries_IDs(IDs)
        self.lone_solutions(entries, forced_chain)

        if gear03:
            entries = self.update_entries_IDs(IDs)
            self.npairs_IDs(entries, IDs, forced_chain)

    def deepScanner_gen(self, row_ids, col_ids, gear03=True, normal_block=True, retainer=False, forced_chain=False):

        entries = self.update_entries(row_ids, col_ids)
        # Uncomment this to get a clean and organised diagnostics
        # self.print_entry(entries)
        self.lone_solutions(entries, forced_chain)

        if gear03:
            # print("Activating subgrid n pairs!")
            entries = self.update_entries(row_ids, col_ids)
            self.npairs(entries, row_ids, col_ids, forced_chain)
            
            if normal_block:
                entries = self.update_entries(row_ids, col_ids)
                if retainer:
                    self.rc_retainers(entries, forced_chain)
                else:
                    self.rc_blockers(entries, forced_chain)
            
            # This one is problematic! needs some more testing!
            # if self.antiking or self.antiknight:
            #     entries = self.update_entries(row_ids, col_ids)
            #     if not retainer:
            #         self.KnightKingIntersections(entries, forced_chain)

    # def KnightKingIntersections(self, entries, forced_chain=False):

    #     for num in [2]:
    #         fields = []
    #         for option in self.super_set:
    #             # print(f"Scanning Subgrid {I+1, J+1} for entry {option}")
    #             if entries[option]["count"] == num:
    #                 parentIDs = entries[option]["IDS"]
    #                 print(f"option = {option} occuring {num} times in {parentIDs}")
                
    #                 for ID in parentIDs:
    #                     field = self.KnightKingSpans(ID)
    #                     fields.append(field)
                    
    #                 IDS = fields[0]
    #                 for i in range(num):
    #                     IDS = IDS.intersection(fields[i])
                    
    #                 IDS = sorted(IDS - set(parentIDs))
    #                 print(option, num, IDS)
    #                 self.fastScanner_gen(IDS, option, forced_chain=forced_chain)
    
    # def KnightKingSpans(self, MID):

    #     fieldIDs = []
    #     i, j = MID
    #     I = i // self.orderRow
    #     J = j // self.orderCol

    #     # Subgrid IDS
    #     sg_row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
    #     sg_col_ids = range(J*self.orderCol, (J+1)*self.orderCol)
    #     Sub_IDs = list(product(sg_row_ids, sg_col_ids))

    #     # Common row IDS
    #     cr_row_ids = [i]
    #     cr_col_ids = range(0, self.cols)
    #     IDs = list(product(cr_row_ids, cr_col_ids))
    #     for ID in IDs:
    #         fieldIDs.append(ID)

    #     # Common col IDS
    #     cc_row_ids = range(0, self.rows)
    #     cc_col_ids = [j]
    #     IDs = list(product(cc_row_ids, cc_col_ids))
    #     for ID in IDs:
    #         fieldIDs.append(ID)
        
    #     # if self.antiking:
    #     #     IDs = self.antiking_IDs(i, j)
    #     #     for ID in IDs:
    #     #         fieldIDs.append(ID)
        
    #     if self.antiknight:
    #         IDs = self.antiknight_IDs(i, j)
    #         for ID in IDs:
    #             fieldIDs.append(ID)
        
    #     return set(fieldIDs) - set(Sub_IDs)

    def chessPinch(self, row_ids, col_ids, gear03=True, forced_chain=False):

        if gear03:
            MIDs = list(product(row_ids, col_ids))

            # A simple collection of all possible entries to scan through
            super_set_nums = set(self.super_set)

            # scan through each row and column of row/col/subgrid
            # and pick out the already filled elements and remove them
            # from superset - to reduce potential combinations
            for row_id, col_id in MIDs:
                
                if forced_chain:
                    entry = self.btMatrix[row_id, col_id]
                else:
                    entry = self.Solution[row_id, col_id]
                
                # by default, add only unfilled IDS
                if entry != 0:
                    # remove non-zero entries from super set of numbers
                    super_set_nums.discard(entry)
            
            # create a dictionary of counters for each entry, with x and y positions
            entryCounter = {}
            for entry in super_set_nums:
                entryCounter[entry] = {}
                entryCounter[entry]["count"] = 0
                entryCounter[entry]["IDs"] = []
            
            for row_id, col_id in MIDs:
                if self.Grids[row_id][col_id]["num_choices"] > 1:
                    for val in self.Grids[row_id][col_id]["choices"]:
                        entryCounter[val]["count"] += 1
                        entryCounter[val]["IDs"].append([row_id, col_id])
            
            # Uncomment these lines for detailed log.
            # print("chess pincher counter dictionary for MIDs")
            # print(MIDs)
            # print(entryCounter)

            if self.antiknight:
                for valkey in entryCounter.keys():
                    if entryCounter[valkey]["count"] == 2:
                        # print("Antiknight pinch scan for value:", valkey, " with IDs:", entryCounter[valkey]["IDs"])
                        # case 0, 0, 0; 1, 0, 0; 0, 1, 0
                        # Collect all IDs.
                        IDs = []
                        if(tuple(entryCounter[valkey]["IDs"][0]) == MIDs[3] and tuple(entryCounter[valkey]["IDs"][1]) == MIDs[7]):
                            # print("Found an antiknight pinch for value ", valkey, " to remove in cell index:", MIDs[3][0], MIDs[3][1] - 1)
                            if(MIDs[3][1] == 3 or MIDs[3][1] == 6):
                                IDs.append([MIDs[3][0], MIDs[3][1] - 1])
                            if(MIDs[7][1] == 4 or MIDs[7][1] == 7):
                                IDs.append([MIDs[7][0], MIDs[7][1] - 3])

                            self.fastScanner_gen(IDs, valkey, solve=True, forced_chain=forced_chain)


    def deepScanner_full(self, gear03=True, forced_chain=False):

        for i in range(0, self.rows):

            cr_row_ids = [i]
            cr_col_ids = [crcol for crcol in range(0, self.cols)]
            self.deepScanner_gen(cr_row_ids, cr_col_ids, gear03, retainer=True,  forced_chain=forced_chain)

            cc_row_ids = [ccrow for ccrow in range(0, self.rows)]
            cc_col_ids = [i]
            self.deepScanner_gen(cc_row_ids, cc_col_ids, gear03, retainer=True,  forced_chain=forced_chain)

            I, J = self.subgrid_IDS[i]
            sg_row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
            sg_col_ids = range(J*self.orderCol, (J+1)*self.orderCol)
            self.deepScanner_gen(sg_row_ids, sg_col_ids, gear03, retainer=False, forced_chain=forced_chain)

            if self.antiknight:
                self.chessPinch(sg_row_ids, sg_col_ids, gear03, forced_chain=forced_chain)
        
        if self.windoku:
            for i in range(0, len(self.w0_IDs)):
                row_ids, col_ids = self.ID2RC_pairs(self.w0_IDs[i])
                self.deepScanner_gen(row_ids, col_ids, gear03, normal_block=False, forced_chain=forced_chain)
        
        if self.diagonals: # or self.oddDiagonals or self.evenDiagonals or self.oddEvenDiagonals or self.evenOddDiagonals:
            # print("Calling diagonals")
            self.specialDeepScanner(self.d1_ids, gear03, forced_chain=forced_chain)
            self.specialDeepScanner(self.d2_ids, gear03, forced_chain=forced_chain)
        
        if self.magicSquare:

            for setNum in range(0, self.nMagicsumSets):
                IDs = self.magicSum_sets[setNum]
                entries = self.update_entries_IDs(IDs)
                
                # if setNum == 0:
                for entry in self.super_set:
                    
                    # letting fastScanner_full() take care of the count == 1 case

                    if entries[entry]["count"] == 2:
                        # print(f"Entry = {entry} occured twice in {cIDs}")
                        cIDs = entries[entry]["IDS"]
                        pID = self.find_pinched_cell(IDs, cIDs, entry)

                        if len(pID) == 1:
                            x, y = pID[0]
                            choices = copy.deepcopy(self.Grids[x][y]["choices"])
                            newChoices = copy.deepcopy(self.Grids[x][y]["choices"])
                            newSplit = self.magicSumVal - entry
                            # print(f"Entry {entry} pinches cell {pID}, having choices = {choices} and split = {newSplit}")
                            for option in choices:
                                # print(entry, option, choices, newChoices)
                                if option >= newSplit:
                                    # print(f"Option = {option} is a violator in {x,y} for pinching entry {entry} with split = {newSplit}")
                                    newChoices.remove(option)
                            # print(f"Updated choices = {newChoices}")
                            self.Grids[x][y]["choices"] = copy.deepcopy(newChoices)
                            self.Grids[x][y]["num_choices"] = len(newChoices)
                            entries = self.update_entries_IDs(IDs)

    def find_pinched_cell(self, flat_IDs, cIDs, entry):

        index01 = flat_IDs.index(cIDs[0])
        index02 = flat_IDs.index(cIDs[1])

        ID = []

        if entry % 2 == 0:
            ID.append(flat_IDs[(index01 + index02)//2])
        else:
            if (index01, index02) == (1, 3):
                ID.append(flat_IDs[0])
            if (index01, index02) == (1, 5):
                ID.append(flat_IDs[2])
            if (index01, index02) == (3, 7):
                ID.append(flat_IDs[6])
            if (index01, index02) == (5, 7):
                ID.append(flat_IDs[8])

        # print(f"Entry = {entry}, pinch_cell = {ID}")

        return ID

    def ID2RC_pairs(self, IDs):

        row_ids = sorted(set([x for x, _ in IDs]))
        col_ids = sorted(set([y for _, y in IDs]))

        # print(row_ids, col_ids)
        
        return row_ids, col_ids

    def pair_finder_full(self):

        for i in range(0, self.rows):

            cr_row_ids = [i]
            cr_col_ids = [cr for cr in range(0, self.cols)]
            entries = self.update_entries(cr_row_ids, cr_col_ids)
            self.npairs(entries, cr_row_ids, cr_col_ids)

            cc_row_ids = [cc for cc in range(0, self.rows)]
            cc_col_ids = [i]
            entries = self.update_entries(cc_row_ids, cc_col_ids)
            self.npairs(entries, cc_row_ids, cc_col_ids)

            I, J = self.subgrid_IDS[i]
            sg_row_ids = [sg for sg in range(I*self.orderRow, (I+1)*self.orderRow)]
            sg_col_ids = [sg for sg in range(J*self.orderCol, (J+1)*self.orderCol)]
            entries = self.update_entries(sg_row_ids, sg_col_ids)
            self.npairs(entries, sg_row_ids, sg_col_ids)

    def lone_solutions(self, entries, forced_chain=False):
        for option in entries:
            # print(f"Scanning Subgrid {I+1, J+1} for entry {option}")
            if entries[option]["count"] == 1:
                i, j = entries[option]["IDS"][0]
                self.update_cell(i, j, option, forced_chain)
    
    def npairs_IDs(self, entries, MIDs, forced_chain=False):

        # A simple collection of all possible entries to scan through
        super_set_nums = set(self.super_set)

        # scan through each row and column of row/col/subgrid
        # and pick out the already filled elements and remove them
        # from superset - to reduce potential combinations
        for row_id, col_id in MIDs:
            
            if forced_chain:
                entry = self.btMatrix[row_id, col_id]
            else:
                entry = self.Solution[row_id, col_id]
            
            # by default, add only unfilled IDS
            if entry != 0:
                # remove non-zero entries from super set of numbers
                super_set_nums.discard(entry)
        
        # set the least order pair and the highest order pair to find
        nmin = 2
        nmax = len(super_set_nums)

        # start scanning for all possible n order hidden pairs
        for n in range(nmin, nmax+1):

            # collect numbers that are potential pair possibilities of order n
            collector = []

            # scan through only those entries in superset
            for item in super_set_nums:

                count = entries[item]["count"]
                # start counting entries
                if count >= nmin and count <= n:
                    collector.append(item)
        
            # check if number of entries are equal to or more than order
            if len(collector) >= n:

                # make all possible pair of combinations of order n
                pairs = list(combinations(collector, n))

                # scan through all combinations of n order pairs one at a time ...
                for pair in pairs:

                    # a collection of IDS
                    IDS = set()

                    for entry in pair:

                        # update all IDS to the potential hidden pair
                        IDS |= set(entries[entry]["IDS"])

                    # check for potential hidden pairs of order n:
                    if len(IDS) == n:
                        # print(f"Found a pair {combination} of order = {n} in IDS = {IDS}")
                        entries_toClean = super_set_nums - set(pair)

                        for entry in entries_toClean:
                            self.fastScanner_gen(IDS, entry, forced_chain=forced_chain)

    def npairs(self, entries, row_ids, col_ids, forced_chain=False):

        MIDs = list(product(row_ids, col_ids))

        # A simple collection of all possible entries to scan through
        super_set_nums = set(self.super_set)

        # scan through each row and column of row/col/subgrid
        # and pick out the already filled elements and remove them
        # from superset - to reduce potential combinations
        for row_id, col_id in MIDs:
            
            if forced_chain:
                entry = self.btMatrix[row_id, col_id]
            else:
                entry = self.Solution[row_id, col_id]
            
            # by default, add only unfilled IDS
            if entry != 0:
                # remove non-zero entries from super set of numbers
                super_set_nums.discard(entry)
        
        # set the least order pair and the highest order pair to find
        nmin = 2
        nmax = len(super_set_nums)

        # start scanning for all possible n order hidden pairs
        for n in range(nmin, nmax+1):

            # collect numbers that are potential pair possibilities of order n
            collector = []

            # scan through only those entries in superset
            for item in super_set_nums:

                count = entries[item]["count"]
                # start counting entries
                if count >= nmin and count <= n:
                    collector.append(item)
        
            # check if number of entries are equal to or more than order
            if len(collector) >= n:

                # make all possible pair of combinations of order n
                pairs = list(combinations(collector, n))

                # scan through all combinations of n order pairs one at a time ...
                for pair in pairs:

                    # a collection of IDS
                    IDS = set()

                    for entry in pair:

                        # update all IDS to the potential hidden pair
                        IDS |= set(entries[entry]["IDS"])

                    # check for potential hidden pairs of order n:
                    if len(IDS) == n:
                        # print(f"Found a pair {combination} of order = {n} in IDS = {IDS}")
                        entries_toClean = super_set_nums - set(pair)

                        for entry in entries_toClean:
                            self.fastScanner_gen(IDS, entry, forced_chain=forced_chain)
    
    def rc_blockers(self, entries, forced_chain=False):

        for entry in entries:
            IDs = entries[entry]["IDS"]
            # print(f"Scanning entry = {entry} and IDS = {IDs}")

            if entries[entry]["count"] > 1:
                common_row, common_col = self.check_common_row_col(IDs)
                # I, J = self.check_common_row_col_subID(IDs)
                common_sg, _, _ = self.check_common_subID(IDs)

                # if common_row_sgid and common_row:
                if common_sg and common_row:
                    # Row Blocker:
                    # print(f"entry = {entry} is a row blocker with IDs = {IDs}")
                    row_ids = [IDs[0][0]]
                    col_ids = list(set(range(0, self.cols)) - set([ID[1] for ID in IDs]))
                    BIDS = list(product(row_ids, col_ids))
                    # print(f"Entry = {entry} is a row blocker and to be cleared from IDs = {BIDS}")
                    self.fastScanner_gen(BIDS, entry, forced_chain=forced_chain)

                    if self.antiknight:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.oddKNevenQN or self.evenKNoddQN:
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.antiking:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.royal:

                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                        if entry in self.kings and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                # if common_col_sgid and common_col:
                if common_sg and common_col:
                    # if common_col:
                    # print(f"entry = {entry} is a col blocker with IDs = {IDs}")
                    row_ids = list(set(range(0, self.rows)) -
                                   set([ID[0] for ID in IDs]))
                    col_ids = [IDs[0][1]]
                    BIDS = list(product(row_ids, col_ids))
                    # print(f"Entry = {entry} is a col blocker and to be cleared from IDs = {BIDS}")
                    self.fastScanner_gen(BIDS, entry, forced_chain=forced_chain)

                    if self.antiknight:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiknight_deepscanIDS(IDs, colblock=True)
                            # print(f"For col blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.oddKNevenQN or self.evenKNoddQN:
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, colblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.antiking:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiking_deepscanIDS(IDs, colblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking col blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.royal:
                        
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                        if entry in self.kings and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
    
    def rc_retainers(self, entries, forced_chain=False):

        for entry in entries:
            IDs = entries[entry]["IDS"]
            # print(f"Scanning entry = {entry} and IDS = {IDs}")

            if entries[entry]["count"] > 1:
                common_row, common_col = self.check_common_row_col(IDs)
                # I, J = self.check_common_row_col_subID(IDs)
                common_sg, I, J = self.check_common_subID(IDs)

                # if common_row_sgid and common_row:
                if common_sg and common_row:
                    # Row Retainer:
                    # print(f"entry = {entry} is a row retainer with IDs = {IDs}")
                    row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
                    col_ids = range(J*self.orderCol, (J+1)*self.orderCol)
                    RIDS = list(set(product(row_ids, col_ids)) - set(IDs))
                    # print(f"Entry = {entry} is a row retainer and to be cleared from IDs = {BIDS}")
                    self.fastScanner_gen(RIDS, entry, forced_chain=forced_chain)

                    if self.antiknight:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.oddKNevenQN or self.evenKNoddQN:
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row retainer entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                    if self.antiking:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row retainer entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.royal:
                        
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                        if entry in self.kings and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                # if common_col_sgid and common_col:
                if common_sg and common_col:
                    # col retainer
                    # print(f"entry = {entry} is a col retainer with IDs = {IDs}")
                    row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
                    col_ids = range(J*self.orderCol, (J+1)*self.orderCol)
                    RIDS = list(set(product(row_ids, col_ids)) - set(IDs))
                    # print(f"Entry = {entry} is a col retainer and to be cleared from IDs = {BIDS}")
                    self.fastScanner_gen(RIDS, entry, forced_chain=forced_chain)

                    if self.antiknight:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiknight_deepscanIDS(IDs, colblock=True)
                            # print(f"For col retainer entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.oddKNevenQN or self.evenKNoddQN:
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, colblock=True)
                            # print(f"For row retainer entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.antiking:
                        if entries[entry]["count"] == 2 or entries[entry]["count"] == 3:
                            KIDs = self.antiking_deepscanIDS(IDs, colblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking col retainer entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)
                    
                    if self.royal:
                        
                        if entry in self.knights and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiknight_deepscanIDS(IDs, rowblock=True)
                            # print(f"For row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

                        if entry in self.kings and (entries[entry]["count"] == 2 or entries[entry]["count"] == 3):
                            KIDs = self.antiking_deepscanIDS(IDs, rowblock=True)
                            # if entries[entry]["count"] == 3:
                            #     print(f"For antiking row blocker entry = {entry}, in SG {common_row_sgid+1, common_col_sgid+1}, the KIDS = {KIDs}")
                            # if entries[entry]["count"] == 2:
                            self.fastScanner_gen(KIDs, entry, forced_chain=forced_chain)

    def antiknight_deepscanIDS(self, IDs, rowblock=False, colblock=False):

        numIDs = len(IDs)

        KIDS = []

        if numIDs == 2:
            rowID01, colID01 = IDs[0]
            rowID02, colID02 = IDs[1]

            if rowblock:
                # row blockers - two entries along the row adjacent to eachother
                if colID02 == colID01 + 1 or colID02 == colID01 - 1:
                    if rowID01 + 2 < self.rows:
                        KIDS.append((rowID01 + 2, colID01))
                        KIDS.append((rowID01 + 2, colID02))
                    if rowID01 - 2 >= 0:
                        KIDS.append((rowID01 - 2, colID01))
                        KIDS.append((rowID01 - 2, colID02))

                # row blockers - two entries along the row with a filled/empty cell between them
                if colID02 == colID01 + 2 or colID02 == colID01 - 2:
                    if rowID01 + 2 < self.rows:
                        KIDS.append((rowID01 + 2, (colID01 + colID02)//2))
                    if rowID01 - 2 >= 0:
                        KIDS.append((rowID01 - 2, (colID01 + colID02)//2))
                    if rowID01 + 1 < self.rows:
                        KIDS.append((rowID01 + 1, colID01))
                        KIDS.append((rowID01 + 1, colID02))
                    if rowID01 - 1 >= 0:
                        KIDS.append((rowID01 - 1, colID01))
                        KIDS.append((rowID01 - 1, colID02))

            if colblock:
                # col blockers - two entries along the column adjacent to eachother
                if rowID02 == rowID01 + 1 or rowID02 == rowID01 - 1:
                    if colID01 + 2 < self.cols:
                        KIDS.append((rowID01, colID01 + 2))
                        KIDS.append((rowID02, colID01 + 2))
                    if colID01 - 2 >= 0:
                        KIDS.append((rowID01, colID01 - 2))
                        KIDS.append((rowID02, colID01 - 2))

                # col blockers -two entries along the column with a filled/empty cell between them
                if rowID02 == rowID01 + 2 or rowID02 == rowID01 - 2:
                    if colID01 + 2 < self.cols:
                        KIDS.append(((rowID01 + rowID02)//2, colID01 + 2))
                    if colID01 - 2 >= 0:
                        KIDS.append(((rowID01 + rowID02)//2, colID01 - 2))
                    if colID01 + 1 < self.cols:
                        KIDS.append((rowID01, colID01 + 1))
                        KIDS.append((rowID02, colID01 + 1))
                    if colID01 - 1 >= 0:
                        KIDS.append((rowID01, colID01 - 1))
                        KIDS.append((rowID02, colID01 - 1))

        if numIDs == 3:
            rowID02, colID02 = IDs[1]

            if rowblock:
                # row blockers - 3 entires in a row
                if colID02 + 2 < self.rows:
                    KIDS.append((rowID02, colID02 + 2))
                if colID02 - 2 >= 0:
                    KIDS.append((rowID02, colID02 - 2))

            if colblock:
                # col blockers - 3 entries in a col
                if rowID02 + 2 < self.rows:
                    KIDS.append((rowID02 + 2, colID02))
                if rowID02 - 2 >= 0:
                    KIDS.append((rowID02 - 2, colID02))

        return KIDS
    
    def antiking_deepscanIDS(self, IDs, rowblock=False, colblock=False):

        numIDs = len(IDs)

        KIDS = []

        if numIDs == 2:
            rowID01, colID01 = IDs[0]
            rowID02, colID02 = IDs[1]

            if rowblock:
                # row blockers - entries in a row adjacent to eachother
                if colID02 == colID01 + 1 or colID02 == colID01 - 1:
                    if rowID01 + 1 < self.rows:
                        KIDS.append((rowID01 + 1, colID01))
                        KIDS.append((rowID01 + 1, colID02))
                    if rowID01 - 1 >= 0:
                        KIDS.append((rowID01 - 1, colID01))
                        KIDS.append((rowID01 - 1, colID02))

                # row blockers - entires in a row with a filled/empty cell between them
                if colID02 == colID01 + 2 or colID02 == colID01 - 2:
                    if rowID01 + 1 < self.rows:
                        KIDS.append((rowID01 + 1, (colID01 + colID02)//2))
                    if rowID01 - 1 >= 0:
                        KIDS.append((rowID01 - 1, (colID01 + colID02)//2))

            if colblock:
                # col blockers adjacent to eachother
                if rowID02 == rowID01 + 1 or rowID02 == rowID01 - 1:
                    if colID01 + 1 < self.cols:
                        KIDS.append((rowID01, colID01 + 1))
                        KIDS.append((rowID02, colID01 + 1))
                    if colID01 - 1 >= 0:
                        KIDS.append((rowID01, colID01 - 1))
                        KIDS.append((rowID02, colID01 - 1))

                # col blockers with a filled/empty cell between them
                if rowID02 == rowID01 + 2 or rowID02 == rowID01 - 2:
                    if colID01 + 1 < self.cols:
                        KIDS.append(((rowID01 + rowID02)//2, colID01 + 1))
                    if colID01 - 1 >= 0:
                        KIDS.append(((rowID01 + rowID02)//2, colID01 - 1))

        if numIDs == 3:
            rowID02, colID02 = IDs[1]

            if rowblock:
                # row blockers - 3 in a row
                if rowID02 + 1 < self.rows:
                    KIDS.append((rowID02 + 1, colID02))
                if rowID02 - 1 >= 0:
                    KIDS.append((rowID02 - 1, colID02))

            if colblock:
                # col blockers - 3 in a col
                if colID02 + 1 < self.rows:
                    KIDS.append((rowID02, colID02 + 1))
                if colID02 - 1 >= 0:
                    KIDS.append((rowID02, colID02 - 1))

        return KIDS

    def check_common_row_col(self, IDs):
        num_ids = len(IDs)
        count_rows = 0
        count_cols = 0
        common_row = False
        common_col = False
        first_row_id, first_col_id = IDs[0]

        for ID in IDs:
            i, j = ID
            if i == first_row_id:
                count_rows += 1
            if j == first_col_id:
                count_cols += 1

        if count_rows == num_ids:
            common_row = True
        if count_cols == num_ids:
            common_col = True

        return common_row, common_col

    def check_common_row_col_subID(self, IDs):
        num_ids = len(IDs)
        count_rows = 0
        count_cols = 0
        common_row_sg = False
        common_col_sg = False
        first_row_sgid, first_col_sgid = IDs[0]
        first_row_sgid, first_col_sgid = first_row_sgid // self.orderRow, first_col_sgid // self.orderCol

        for ID in IDs:
            i, j = ID
            i, j = i // self.orderRow, j // self.orderCol
            if i == first_row_sgid:
                count_rows += 1
            if j == first_col_sgid:
                count_cols += 1

        if count_rows == num_ids:
            common_row_sg = True
        if count_cols == num_ids:
            common_col_sg = True

        return common_row_sg, common_col_sg

    def check_common_subID(self, IDs):
        num_ids = len(IDs)
        count_entries = 0
        common_sg = False
        first_row_sgid, first_col_sgid = IDs[0]
        first_row_sgid, first_col_sgid = first_row_sgid // self.orderRow, first_col_sgid // self.orderCol

        for ID in IDs:
            i, j = ID
            i, j = i // self.orderRow, j // self.orderCol
            if i == first_row_sgid and j == first_col_sgid:
                count_entries += 1

        if count_entries == num_ids:
            common_sg = True

        return common_sg, first_row_sgid, first_col_sgid

    def print_entry(self, entries):
        for option in entries:
            print(
                f"Option = {option}, count = {entries[option]['count']}, IDs = {entries[option]['IDS']}")

    def complex_scanner(self):
        self.xwings()
        # self.swordfish()

    def xwings(self):

        xwing_counter = 2

        # row xwings - scan double entries along columns and eliminate entries along rows
        row01_col_ids = [col_id for col_id in range(0, self.cols)]
        row02_col_ids = [col_id for col_id in range(0, self.cols)]

        # col xwings - scan double entries along columns and eliminate entries along rows
        col01_row_ids = [row_id for row_id in range(0, self.rows)]
        col02_row_ids = [row_id for row_id in range(0, self.rows)]

        for i in range(0, self.cols-1):

            row01_row_ids = [i]
            row01_entries = self.update_entries(row01_row_ids, row01_col_ids)

            col01_col_ids = [i]
            col01_entries = self.update_entries(col01_row_ids, col01_col_ids)

            for j in range(i+1, self.cols):

                # print(f"Scanning row pair {i+1, j+1}")
                row02_row_ids = [j]
                row02_entries = self.update_entries(row02_row_ids, row02_col_ids)

                # print(f"Scanning col pair {i+1, j+1}")
                col02_col_ids = [j]
                col02_entries = self.update_entries(col02_row_ids, col02_col_ids)

                for entry in self.super_set:

                    # checks for row xwings
                    if row01_entries[entry]["count"] == xwing_counter and row02_entries[entry]["count"] == xwing_counter:
                        # print(f"Found a possible xwing/swordfish entry {entry} in rows {i+1, j+1}")
                        IDS_row01 = row01_entries[entry]["IDS"]
                        IDS_row02 = row02_entries[entry]["IDS"]
                        counter = 0
                        target_col_ids = []
                        for (ID1, ID2) in zip(IDS_row01, IDS_row02):
                            _, y1 = ID1
                            _, y2 = ID2
                            if y1 == y2:
                                counter += 1
                                target_col_ids.append(y1)

                        if counter == xwing_counter:
                            # print(f"Found a row xwing entry {entry} in rows {[i, j]} cols {target_col_ids}")
                            row_ids = list(
                                set([x for x in range(0, self.rows)]) - set([i, j]))
                            col_ids = target_col_ids
                            XIDS = list(product(row_ids, col_ids))
                            # print(f"To remove entry {entry} in (r,c) = {row_id, col_id}")
                            self.fastScanner_gen(XIDS, entry, solve=True)

                    # check for col xwings
                    if col01_entries[entry]["count"] == xwing_counter and col02_entries[entry]["count"] == xwing_counter:
                        # print(f"Found a possible xwing/swordfish entry {entry} in cols {i+1, j+1}")
                        IDS_col01 = col01_entries[entry]["IDS"]
                        IDS_col02 = col02_entries[entry]["IDS"]
                        counter = 0
                        target_row_ids = []
                        for (ID1, ID2) in zip(IDS_col01, IDS_col02):
                            x1, _ = ID1
                            x2, _ = ID2
                            if x1 == x2:
                                counter += 1
                                target_row_ids.append(x1)

                        if counter == xwing_counter:
                            # print(f"Found a col xwing entry {entry} in rows {target_row_ids} cols {[i, j]}")
                            row_ids = target_row_ids
                            col_ids = list(
                                set([y for y in range(0, self.cols)]) - set([i, j]))
                            XIDS = list(product(row_ids, col_ids))
                            # print(f"To remove entry {entry} in (r,c) = {row_id, col_id}")
                            self.fastScanner_gen(XIDS, entry, solve=True)

    def swordfish(self):

        # Row swordfishes - scan double/triple entries along columns and eliminate entries along rows
        row01_col_ids = [col_id for col_id in range(0, self.cols)]
        row02_col_ids = [col_id for col_id in range(0, self.cols)]
        row03_col_ids = [col_id for col_id in range(0, self.cols)]

        # column swordfishes - scan double/triple entries along columns and eliminate entries along rows
        col01_row_ids = [row_id for row_id in range(0, self.rows)]
        col02_row_ids = [row_id for row_id in range(0, self.rows)]
        col03_row_ids = [row_id for row_id in range(0, self.rows)]

        for i in range(0, self.cols-2):

            row01_row_ids = [i]
            row01_entries = self.update_entries(row01_row_ids, row01_col_ids)

            col01_col_ids = [i]
            col01_entries = self.update_entries(col01_row_ids, col01_col_ids)

            for j in range(i+1, self.cols-1):

                row02_row_ids = [j]
                row02_entries = self.update_entries(row02_row_ids, row02_col_ids)

                col02_col_ids = [j]
                col02_entries = self.update_entries(col02_row_ids, col02_col_ids)

                for k in range(j+1, self.cols):

                    row03_row_ids = [k]
                    row03_entries = self.update_entries(row03_row_ids, row03_col_ids)

                    col03_col_ids = [k]
                    col03_entries = self.update_entries(col03_row_ids, col03_col_ids)

                    for entry in self.super_set:

                        IDS_row01 = row01_entries[entry]["IDS"]
                        IDS_row02 = row02_entries[entry]["IDS"]
                        IDS_row03 = row03_entries[entry]["IDS"]
                        col_ids_row01 = set()
                        col_ids_row02 = set()
                        col_ids_row03 = set()
                        row_ids_row01 = set()
                        row_ids_row02 = set()
                        row_ids_row03 = set()

                        for (x1, y1) in IDS_row01:
                            row_ids_row01.add(x1)
                            col_ids_row01.add(y1)
                        
                        for (x1, y1) in IDS_row02:
                            row_ids_row02.add(x1)
                            col_ids_row02.add(y1)
                        
                        for (x1, y1) in IDS_row03:
                            row_ids_row03.add(x1)
                            col_ids_row03.add(y1)
                        
                        IDS_col01 = col01_entries[entry]["IDS"]
                        IDS_col02 = col02_entries[entry]["IDS"]
                        IDS_col03 = col03_entries[entry]["IDS"]
                        row_ids_col01 = set()
                        row_ids_col02 = set()
                        row_ids_col03 = set()
                        col_ids_col01 = set()
                        col_ids_col02 = set()
                        col_ids_col03 = set()

                        for (x1, y1) in IDS_col01:
                            row_ids_col01.add(x1)
                            col_ids_col01.add(y1)
                        
                        for (x1, y1) in IDS_col02:
                            row_ids_col02.add(x1)
                            col_ids_col02.add(y1)
                        
                        for (x1, y1) in IDS_col03:
                            row_ids_col03.add(x1)
                            col_ids_col03.add(y1)

                        # condition for a potential 2-2-2 row swordfish or a 2-2-3, 2-3-2, 2-3-3 row swordfishes
                        if row01_entries[entry]["count"] == 2:

                            # condition for a 2-2-2 row swordfish
                            if row02_entries[entry]["count"] == 2 and row03_entries[entry]["count"] == 2:

                                # condition for a perfect/dangling 2-2-2 row swordfish
                                if (len(col_ids_row01 & col_ids_row02) >= 1 and 
                                    len(col_ids_row02 & col_ids_row03) >= 1 and 
                                    len(col_ids_row01 & col_ids_row03) >= 1 and
                                    ( len(col_ids_row01 & col_ids_row02 & col_ids_row03) == 3 or
                                      len(col_ids_row01 & col_ids_row02 & col_ids_row03) == 0) ):
                                    
                                    # print(f"A perfect/dangling 2-2-2 swordfish with entry {entry} in rows {i,j,k}")
                                    row_ids = list(set([x for x in range(0, self.rows)]) - set([i, j, k]))
                                    col_ids = list(col_ids_row01 | col_ids_row02 | col_ids_row03)
                                    SIDS = list(product(row_ids, col_ids))
                                    # print(f"To remove entry {entry} in (r,c) = {row_id, col_id}")
                                    self.fastScanner_gen(SIDS, entry, solve=True)
                            
                            # condition for a 2-2-3 row swordfish
                            if row02_entries[entry]["count"] == 2 and row03_entries[entry]["count"] == 3:

                                # condition for a perfect/dangling 2-2-2 row swordfish
                                if (len(col_ids_row01 & col_ids_row02) >= 1 and 
                                    len(col_ids_row02 & col_ids_row03) >= 1 and 
                                    len(col_ids_row01 & col_ids_row03) >= 1 and
                                    ( len(col_ids_row01 & col_ids_row02 & col_ids_row03) == 3 or
                                      len(col_ids_row01 & col_ids_row02 & col_ids_row03) == 0) ):
                                    
                                    # print(f"A perfect/dangling 2-2-2 swordfish with entry {entry} in rows {i,j,k}")
                                    row_ids = list(set([x for x in range(0, self.rows)]) - set([i, j, k]))
                                    col_ids = list(col_ids_row01 | col_ids_row02 | col_ids_row03)
                                    SIDS = list(product(row_ids, col_ids))
                                    # print(f"To remove entry {entry} in (r,c) = {row_id, col_id}")
                                    self.fastScanner_gen(SIDS, entry, solve=True)

                        # condition for a potential 2-2-2 col swordfish or a 2-2-3, 2-3-2, 2-3-3 col swordfishs
                        if col01_entries[entry]["count"] == 2:

                            # condition for a potential 2-2-2 col swordfish
                            if col02_entries[entry]["count"] == 2 and col03_entries[entry]["count"] == 2:
                                
                                # condition for a perfect/dangling 2-2-2 col swordfish
                                if (len(row_ids_col01 & row_ids_col02) >= 1 and 
                                    len(row_ids_col02 & row_ids_col03) >= 1 and 
                                    len(row_ids_col01 & row_ids_col03) >= 1 and
                                    ( len(row_ids_col01 & row_ids_col02 & row_ids_col03) == 3 or
                                      len(row_ids_col01 & row_ids_col02 & row_ids_col03) == 0) ):

                                    # print(f"A perfect/dangling 2-2-2 swordfish with entry {entry} in cols {i,j,k}")
                                    row_ids = list(row_ids_col01 | row_ids_col02 | row_ids_col03)
                                    col_ids = list(set([y for y in range(0, self.cols)]) - set([i, j, k]))
                                    SIDS = list(product(row_ids, col_ids))
                                    # print(f"To remove entry {entry} in (r,c) = {row_id, col_id}")
                                    self.fastScanner_gen(SIDS, entry, solve=True)

    def priority_list_updater_strict(self):

        # giving a hard reset to the list
        self.priority_list = []

        # don't go more than 10 entries
        max_count = 10
        count = 0

        global_choices = []

        for (I, J) in self.subgrid_IDS:
            sg_row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
            sg_col_ids = range(J*self.orderCol, (J+1)*self.orderCol)

            num_choices = 0
            for r in sg_row_ids:
                for c in sg_col_ids:
                    num_choices += self.Grids[r][c]['num_choices']
            global_choices.append(num_choices)
        
        sortedIndices = np.argsort(global_choices)
        for priority_order in range(1, self.rows+1):
            for index in sortedIndices:
                I, J = self.subgrid_IDS[index]
                sg_row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
                sg_col_ids = range(J*self.orderCol, (J+1)*self.orderCol)

                for r in sg_row_ids:
                    for c in sg_col_ids:
                        if self.Grids[r][c]['num_choices'] == priority_order and count <= max_count:
                            self.priority_list.append([r, c])
                            count += 1
    
    def priority_list_updater(self):

        # giving a hard reset to the list
        self.priority_list = []

        # don't go more than 10 entries
        max_count = 10
        count = 0

        for priority_order in range(1, self.rows+1):
            for r in range(0, self.rows):
                for c in range(0, self.cols):
                    if self.Grids[r][c]['num_choices'] == priority_order and count <= max_count:
                        self.priority_list.append([r, c])
                        count += 1

    def chain_reaction(self):

        isSudokuValid = sudoku_valid = self.evaluate_solution(self.Solution, self.zeros)

        if isSudokuValid:

            # cleansweep single entry cells.
            print("Starting a preliminary clean-up!")
            self.fastScanner_full()
            self.deepScanner_full()

            # check if the sudoku is empty or filled
            self.count_zeros(self.Solution)

            if self.zeros == 0:
                sudoku_valid = self.evaluate_solution(self.Solution, self.zeros)
                if sudoku_valid:
                    print("Solved in elementary analysis!")
                    return True
                else:
                    print("Houston! Cannot solve a brozen puzzle!")
                    return False
            else:
                print("Preliminary cleanup didn't work!")

                # set forced chain parameters
                unSolved = True
                checkpointLevel = 0

                # Take a master backup if things go haywire
                # setup a backup 0 - if things go haywire
                self.shadowGrids = copy.deepcopy(self.Grids)

                # create a checkpoint 
                checkpointGrids = []
                checkpointGrids.append(copy.deepcopy(self.Grids))
                self.btMatrix = self.Solution.copy()
                checkpoint_matrix = []
                checkpoint_matrix.append(self.Solution.copy())

                # first update of the priority list
                self.priority_list_updater_strict()
                # self.priority_list_updater()

                # iterator variable - for diagnosis
                n = 0

                # Forced Chain Reaction Tracker
                fcr_tracker = {}

                # Pre-allocation of fcr tracker
                fcr_tracker[checkpointLevel] = {}
                fcr_tracker[checkpointLevel]["ID"] = []
                fcr_tracker[checkpointLevel]["Attempted Choices"] = []

                while unSolved:

                    # take the first element
                    x, y = self.priority_list[0]

                    # make a choices list by subtracting all the previously 
                    # attempted entries in the current level
                    choices = list( set(copy.deepcopy(self.Grids[x][y]["choices"])) - 
                                    set(fcr_tracker[checkpointLevel]["Attempted Choices"]) )
                    
                    print("Choices = ", choices, "Priority Cell = ", self.priority_list[0], "Checkpoint Level = ", checkpointLevel)
                    
                    # check if there are still valid choices
                    if len(choices) >= 1:
                        # so, there is atleast one valid entry to simulate chain reaction
                        # Sorting the entries
                        choices.sort()
                        # Picking the first entry
                        entry = choices[0]

                        # kicking an iteration up
                        n += 1

                    else:

                        if checkpointLevel > 0:
                            # no choice is valid at this level! - Violation occured at a higher level
                            # print(f"All entries violated for this level {checkpointLevel}! Deleting Backup!")

                            # clearning the checkpoint in the tracker!
                            fcr_tracker[checkpointLevel]['ID'] = []
                            fcr_tracker[checkpointLevel]["Attempted Choices"] = []

                            # clearning the backup at this checkpoint level
                            _ = checkpointGrids.pop()
                            _ = checkpoint_matrix.pop()

                            # reducing checkpoint by one unit
                            checkpointLevel -= 1

                            # Rolling back to the previous checkpoint
                            self.Grids = copy.deepcopy(checkpointGrids[checkpointLevel])
                            self.btMatrix = checkpoint_matrix[checkpointLevel].copy()

                            # update priority list
                            self.priority_list_updater_strict()
                            # self.priority_list_updater()

                            # kicking an iteration
                            n += 1

                            # skip the current loop
                            continue
                        else:
                            print('Houston, we have a situation! The sudoku is invalid!')
                            return False

                    # storing the tracked ID and attempted choice
                    fcr_tracker[checkpointLevel]['ID'].append([x,y])
                    fcr_tracker[checkpointLevel]['Attempted Choices'].append(entry)
                    # print(f"Target Cell = {x,y} choice = {entry} valid choices = {choices}")

                    # trigger a chain reaction
                    # print(f"Plugging {entry} into cell {x, y}")
                    self.update_cell(x, y, entry, forced_chain=True)
                    # cleansweep single entry cells.
                    self.fastScanner_full(forced_chain=True)
                    self.deepScanner_full(forced_chain=True)

                    if self.cr_status:
                        print(f"Unfilled Entries = {self.zeros} Iteration = {n}")

                    # check if the sudoku is empty or filled
                    isSudokuFull = self.count_zeros(self.btMatrix, forced_chain=True)

                    # Check for the validity of the solution - it can be valid or corrupted.
                    sudoku_valid = self.evaluate_solution(self.btMatrix, self.zeros)

                    # If the sudoku is filled - meaning chain reaction completed the sudoku
                    if sudoku_valid:
                        
                        if isSudokuFull:
                            # this means the sudoku solution is valid
                            print(f"Sudoku Solved using Gear 5 in {n} iteration(s)!")
                            # self.print_sudoku(self.btMatrix)

                            ## Fill in the grid and update num_choices and choices
                            for i in range(0, self.rows):
                                for j in range(0, self.cols):
                                    if self.Solution[i, j] == 0:
                                        v = self.btMatrix[i, j]
                                        self.Solution[i, j] = v
                                        self.canvas.itemconfigure(self.Grids[i][j]["label"],
                                                                    text=v,
                                                                    fill=self.colour_minor,
                                                                    font=self.numFont)
                                        self.Grids[i][j]["choices"] = 0
                                        self.Grids[i][j]["num_choices"] = 0
                            
                            ## Destroy backups
                            checkpointGrids = []
                            checkpoint_matrix = []
                            self.shadowGrids = []

                            # destroy the iterative backtracing matrix
                            self.btMatrix = np.zeros((self.rows, self.cols), dtype=np.int32)

                            # print the fcr_tracker
                            # print(fcr_tracker)
                            
                            # activate the kill-switch
                            unSolved = False

                        else:

                            # print(f"A partial chain reaction is successful! Creating checkpoint = {checkpointLevel+1}")
                            # self.print_sudoku(self.btMatrix)
                            # Create a new checkpoint
                            checkpointLevel += 1

                            # Create a new checkpoint in the fcr tracker
                            fcr_tracker[checkpointLevel] = {}
                            fcr_tracker[checkpointLevel]["ID"] = []
                            fcr_tracker[checkpointLevel]["Attempted Choices"] = []

                            # save the current state in checkpoint
                            checkpointGrids.append(copy.deepcopy(self.Grids))
                            checkpoint_matrix.append(self.btMatrix.copy())

                            # update priority list
                            self.priority_list_updater_strict()
                            # self.priority_list_updater()
                    
                    else:

                        # the solution is invalid - rolling back to the previous checkpoint
                        # print(f"Violation while filling {entry} in cell {x, y} in checkpoint {checkpointLevel}")
                        # self.print_sudoku(self.btMatrix)

                        # Rolling back to the previous checkpoint
                        self.Grids = copy.deepcopy(checkpointGrids[checkpointLevel])
                        self.btMatrix = checkpoint_matrix[checkpointLevel].copy()
                        # print("Restored previous version of btMatrix!")
                        # self.print_sudoku(self.btMatrix)

                        # update priority list
                        self.priority_list_updater_strict()
                        # self.priority_list_updater()

                return True
        else:
            print("Houston! You gave an invalid sudoku!")
            return False
            
    def evaluate_solution(self, Solution, zeros):

        sudokuFull = True if zeros == 0 else False

        classicValid = True
        for I in range(0, self.rows):
            row = list(Solution[I, :])
            col = list(Solution[:, I])

            row_lst = list(filter(lambda a: a != 0, row))
            col_lst = list(filter(lambda a: a != 0, col))

            row_set = set(row_lst)
            col_set = set(col_lst)

            if len(row_lst) != len(row_set):
                # print(f"In FC partial counter violation! Counts = {counter}, Constraints = {self.constraints}")
                return False
            
            if len(col_lst) != len(col_set):
                # print(f"In FC partial counter violation! Counts = {counter}, Constraints = {self.constraints}")
                return False

        for I in range(0, self.orderCol):
            for J in range(0, self.orderRow):

                row_ids = range(I*self.orderRow, (I+1)*self.orderRow)
                col_ids = range(J*self.orderCol, (J+1)*self.orderCol)

                IDs = list(product(row_ids, col_ids))

                subgrid_lst = []

                for x, y in IDs:
                    subgrid_lst.append(Solution[x, y])
                
                subgrid_lst = list(filter(lambda a: a != 0, subgrid_lst))

                subgrid_set = set(subgrid_lst)

                if len(subgrid_lst) != len(subgrid_set):
                    # print(f"In FC partial counter violation! Counts = {counter}, Constraints = {self.constraints}")
                    return False

        # check for a valid classical solution
        # print(f"Counts = {counter}, Constraints = {self.constraints}")
        # classicValid = True if counter == self.constraints else False
        # print(f"classic clear {classicValid}")

        # print(f"In FC partial counter Counts = {counter}, Constraints = {self.constraints}")
        if self.antiknight:
            antiknightValid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry != 0:
                        KIDS = self.antiknight_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == Solution[r, c]:
                                return False
                                
            classicValid = classicValid and antiknightValid
            # print(f"antiknight clear {classicValid}")
        
        if self.nonConsec:
            nonConsecValid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry != 0:
                        KIDS = self.nonConsec_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == 1 and Solution[r, c] == entry + 1 :
                                # print(f"broke at entry = {entry}, i, j = {i,j}, r,c = {r,c}")
                                return False
                            if entry == self.rows and Solution[r, c] == entry - 1:
                                # print(f"broke at entry = {entry}, i, j = {i,j}, r,c = {r,c}")
                                return False
                            if entry > 1 and entry < self.rows:
                                if entry == Solution[r, c] + 1 or entry == Solution[r, c] - 1:
                                    # print(f"broke at entry = {entry}, i, j = {i,j}, r,c = {r,c}")
                                    return False
            classicValid = classicValid and nonConsecValid
            # print(f"nonconsec clear {classicValid} {nonConsecValid}")
        
        if self.windoku:

            windoku_Valid = True
            for i in range(0, len(self.w0_IDs)):

                subgrid_lst = []
                for x, y in self.w0_IDs[i]:
                    subgrid_lst.append(Solution[x, y])

                subgrid_lst = list(filter(lambda a: a != 0, subgrid_lst))
                subgrid_set = set(subgrid_lst)

                if len(subgrid_lst) != len(subgrid_set):
                    # print(f"In FC partial counter violation! Counts = {counter}, Constraints = {self.constraints}")
                    return False
            
            classicValid = classicValid and windoku_Valid
        
        if self.sandwich and sudokuFull:

            sandwichValid = True
            
            for i in range(0, self.rows):
                
                row = list(Solution[i, :])
                col = list(Solution[:, i])

                row_counter = 0
                col_counter = 0

                for entry in self.extremes:
                    if entry in row:
                        row_counter += 1
                    if entry in col:
                        col_counter += 1
                    
                if row_counter == 2:
                    I1 = row.index(self.extremes[0])
                    I2 = row.index(self.extremes[1])

                    start, end = (I1, I2) if I1 < I2 else (I2, I1)
                    sandwichRowSum = sum(row[start:end+1])

                    if sandwichRowSum != self.row_sums[i]:
                        # print(f"row = {i}", start, end, sandwichRowSum, row, self.row_sums[i])
                        return False
                
                if col_counter == 2:
                    J1 = col.index(self.extremes[0])
                    J2 = col.index(self.extremes[1])

                    start, end = (J1, J2) if J1 < J2 else (J2, J1)
                    sandwichColSum = sum(col[start:end+1])

                    if sandwichColSum != self.col_sums[i]:
                        # print(f"col = {i}", start, end, sandwichColSum, col, self.col_sums[i])
                        return False

            classicValid = classicValid and sandwichValid
        
        if self.thermometer:

            thermometerValid = True
            for i in range(0, self.nThermometerSets):
                IDs = self.Thermometer_IDs[i]

                thermometer_lst = []
                for x, y in IDs:
                    thermometer_lst.append(Solution[x, y])
                
                thermometer_lst = list(filter(lambda a: a != 0, thermometer_lst))
                sorted_thermometer_lst = copy.deepcopy(thermometer_lst)
                sorted_thermometer_lst.sort()

                if thermometer_lst == sorted_thermometer_lst:
                    therm_set = set(thermometer_lst)
                    if len(thermometer_lst) != len(therm_set):
                        return False
                else:
                    return False

            classicValid = classicValid and thermometerValid
        
        if self.royal:
            royalValid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry in self.kings:
                        KIDS = self.antiking_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == Solution[r, c]:
                                return False

                    if entry in self.knights:
                        KIDS = self.antiknight_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == Solution[r, c]:
                                # print(f"Issue with antiknight with entry={entry}!")
                                return False
                    
                    if entry in self.queens:
                        d1_ids = self.diagonalTLBR_ids(i, j)
                        for (r, c) in d1_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                # print(f"Issue with diagonalqn!")
                                return False
                        
                        d2_ids = self.diagonalTRBL_ids(i, j)
                        for (r, c) in d2_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                # print(f"Issue with antidiagonalqn!")
                                return False
            
            classicValid = classicValid and royalValid
            # print(f"oddKNevenQN clear {classicValid}")

        if self.oddKNevenQN or self.evenKNoddQN:
            KNQN_Valid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry in self.knights:
                        KIDS = self.antiknight_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == Solution[r, c]:
                                # print(f"Issue with antiknight with entry={entry}!")
                                return False
                    
                    if entry in self.queens:
                        d1_ids = self.diagonalTLBR_ids(i, j)
                        for (r, c) in d1_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                # print(f"Issue with diagonalqn!")
                                return False
                        
                        d2_ids = self.diagonalTRBL_ids(i, j)
                        for (r, c) in d2_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                # print(f"Issue with antidiagonalqn!")
                                return False
            
            classicValid = classicValid and KNQN_Valid
            # print(f"oddKNevenQN clear {classicValid}")

        if self.antiking:
            antikingValid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry != 0:
                        KIDS = self.antiking_IDs(i, j)
                        for (r, c) in KIDS:
                            if entry == Solution[r, c]:
                                return False
            classicValid = classicValid and antikingValid
            # print(f"antiking clear {classicValid}")
        
        if self.queen:
            queenValid = True
            for i in range(0, self.rows):
                for j in range(0, self.cols):

                    entry = Solution[i,j]

                    if entry in self.queens:
                        d1_ids = self.diagonalTLBR_ids(i, j)
                        for (r, c) in d1_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                return False
                        
                        d2_ids = self.diagonalTRBL_ids(i, j)
                        for (r, c) in d2_ids:
                            if entry == Solution[r, c] and i != r and j != c:
                                return False
            
            classicValid = classicValid and queenValid
            # print(f"queen clear {classicValid}")

        if self.diagonals:
            diagonalsValid = True
            for i, j in self.d1_ids:
                entry = Solution[i, j]
                if entry != 0:
                    for r, c in self.d1_ids:
                        if entry == Solution[r, c] and i != r and j != c:
                            return False
            
            for i, j in self.d2_ids:
                entry = Solution[i, j]
                if entry != 0:
                    for r, c in self.d2_ids:
                        if entry == Solution[r, c] and i != r and j != c:
                            return False
            
            classicValid = classicValid and diagonalsValid
            # print(f"diagonals clear {classicValid}")

        return classicValid
    
    def print_sudoku(self, matrix, file=sys.stdout):

        for i in range(0, self.rows):
            if i % self.orderRow == 0:
                print(self.border, file=file)
            line = "|"
            for j in range(0, self.cols):
                line += f" {matrix[i, j]:{self.max_digits}}"
                if (j + 1) % self.orderCol == 0:
                    line += " |"
            print(line, file=file)
            
        print(self.border, file=file)
    
    def logical_solver(self):

        iterator = 0
        diff = self.global_choices

        while diff > 0 and self.zeros > 0 and iterator < self.MAX_ITER:

            global_choices = self.global_choices

            # print("Activating Gear 1")
            self.fastScanner_full()
            self.count_zeros(self.Solution)
            print(f"After Gear 1, iteration {iterator+1}, unfilled entries = {self.zeros}, global choices = {self.global_choices}")

            if (self.zeros > 0):
                # print("Activating Gear 2")
                self.deepScanner_full(gear03=False)
                self.count_zeros(self.Solution)
                print(f"After Gear 2, iteration {iterator+1}, unfilled entries = {self.zeros}, global choices = {self.global_choices}")

            if (self.zeros > 0):
                # print("Activating Gear 3")
                self.deepScanner_full()
                self.count_zeros(self.Solution)
                print(f"After Gear 3, iteration {iterator+1}, unfilled entries = {self.zeros}, global choices = {self.global_choices}")

            if (self.zeros > 0):
                # print("Activating Gear 4")
                self.complex_scanner()
                self.count_zeros(self.Solution)
                print(f"After Gear 4, iteration {iterator+1}, unfilled entries = {self.zeros}, global choices = {self.global_choices}")
            
            diff = global_choices - self.global_choices
            iterator += 1
        
        # self.fastScanner_full(solve=False)
        # self.grid_markup()
        return iterator

    def solve(self):

        start = time.time()
        iterator = 0
        cr_solved = False

        print("Diagnosis on the Entered Sudoku!")
        isSudokuValid = self.evaluate_solution(self.matrix, self.zeros)

        if isSudokuValid:
            print("The sudoku seems valid!")
            print(f"Alright! Starting with {self.zeros} unfilled entries and {self.global_choices} global choices")

            if self.logics:
                # iterative logical solver
                print("Initiating the Logical Iterative Solver!")
                iterator = self.logical_solver()
            
            if self.zeros != 0 and self.gear05:
                # chain reaction solver
                print("Sudoku unsolved using logics! Switching to Chain Reaction Solver!")
                cr_solved = self.chain_reaction()
                validity = cr_solved
            else:
                print("Verifying the Solved Solution!")
                self.count_zeros(self.Solution)
                validity = self.evaluate_solution(self.Solution, self.zeros)
            
            valid = "valid" if validity else "invalid"
            correctly = "correctly" if validity else "incorrectly"
            full = "full" if self.zeros == 0 else "partial"

            print(f"The {full} sudoku solution is {valid}!")
            self.print_sudoku(self.Solution)

            end = time.time()

            status = "Completed" if self.zeros == 0 and isSudokuValid and validity else "Partially Solved"
            method = "logics and chain reaction" if cr_solved else "pure logics"
            only = "and chain reaction" if cr_solved else "alone"

            print(f"Sudoku {status} using {method}")
            print(f"It took {iterator} logical iteration(s) {only} to {correctly} solve the {full} puzzle.")
            print(f"Time taken is {end-start} seconds")

        else:
            print("Houston! Refusing to solve an invalid Sudoku!")


SudokuRoot = tk.Tk()

# my_sudoku = Sudoku(SudokuRoot, sp.problem3_patto_shye)

# root.tk.call('tk', 'scaling', 1.25)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_0numTherm, thermometer=True, nThermometerSets=11, thermometerSets=thermometerSets)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_aadTribute02,
#                     thermometer=True, nThermometerSets=1, thermometerSets=thermometerSets, antiknight=True,
#                     magicSquare=True, nMagicsumSets=1, magicSum_sets=magicSum_sets, magicSumVal=15)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_RiSaMiracle2,
#                     thermometer=True, nThermometerSets=6, thermometerSets=sp.thermometer_RiSa, antiknight=True)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_expert08)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_chess_oddKnightEvenQN, oddKnightEvenQueen=True)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_twinMSOddD, oddDiagonals=True,
#                    magicSquare=True, nMagicsumSets=2, magicSum_sets=sp.magicSum_special, magicSumVal=15)
# my_sudoku = Sudoku(SudokuRoot, sp.problem2x3_extreme02, orderCol=3, orderRow=2, gear05=False)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_chess_miracle01, gear05=False, antiking=True, nonConsec=True, antiknight=True)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_antiknightC1, antiknight=True)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_Sandwich01, sandwich=True, row_sums=sp.problem3_Sandwich01_rowsums, cr_status=True,
#                             orderRow=3, orderCol=3, col_sums=sp.problem3_Sandwich01_colsums, gear05=True)
# my_sudoku = Sudoku(SudokuRoot, sp.problem3_MySudoku02, diagonals=True, antiking=True, gear05=False)
my_sudoku = Sudoku(SudokuRoot, sp.problem3_4numbers01, max_iter=1, antiknight=True, diagonals=True, gear05=False,
                                magicSquare=True, nMagicsumSets=1, magicSum_sets=sp.magicSum_centre3X3, magicSumVal=15)
SudokuRoot.title("Sudoku")
SudokuRoot.mainloop()
