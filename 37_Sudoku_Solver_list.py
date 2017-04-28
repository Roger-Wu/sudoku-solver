"""
LeetCode Problem 37.Sudoku Solver
https://leetcode.com/problems/sudoku-solver/#/description
written in python 2

This is a duplicate of SudokuSolver.py.
"""

class Solution(object):
    def solveSudoku(self, board):
        self.init_params()
        self.read_board(board)
        self.init_solving_utils()

        self.fill_with_givens()
        self.is_solved = self.solve_by_dfs()

        for i in xrange(len(board)):
            board[i] = ''.join(str(i) for i in self.board[i])

    def init_params(self):
        self.col_size = 9  # len(self.board)
        self.row_size = 9  # len(self.board[0])
        self.block_col_size = 3
        self.block_row_size = 3

        self.digit_unfilled = 0
        self.digit_min = 1
        self.digit_max = 9

    def read_board(self, charBoard):
        self.initial_board = [[self.char_to_int(char) for char in row] for row in charBoard]
        self.board = [[self.digit_unfilled for char in row] for row in charBoard]

    def char_to_int(self, char):
        if char == '.':
            return 0
        else:
            return int(char)

    def print_board(self):
        for row in self.board:
            print(row)

    def init_solving_utils(self):
        self.psbl_digits = [[range(self.digit_min, self.digit_max + 1) for ci in xrange(self.col_size)] for ri in xrange(self.row_size)]
        self.unfilled_cells = []
        # In order to unfill cells
        self.each_step_updated_cells = []

    def fill_cell(self, cell, digit, is_solving):
        cell_row, cell_col = cell
        updated_cells = []

        self.board[cell_row][cell_col] = digit

        # update possible digits by row
        row = cell_row
        for col in xrange(self.col_size):
            if digit in self.psbl_digits[row][col]:
                self.psbl_digits[row][col].remove(digit)
                updated_cells.append((row, col))

        # update possible digits by col
        col = cell_col
        for row in xrange(self.row_size):
            if digit in self.psbl_digits[row][col]:
                self.psbl_digits[row][col].remove(digit)
                updated_cells.append((row, col))

        # update possible digits by block
        block_row_idx = cell_row / self.block_row_size
        block_col_idx = cell_col / self.block_col_size
        for in_block_row_idx in xrange(self.block_row_size):
            for in_block_col_idx in xrange(self.block_col_size):
                row = block_row_idx * self.block_row_size + in_block_row_idx
                col = block_col_idx * self.block_col_size + in_block_col_idx
                if digit in self.psbl_digits[row][col]:
                    self.psbl_digits[row][col].remove(digit)
                    updated_cells.append((row, col))

        if is_solving:
            self.each_step_updated_cells.append(updated_cells)

    def unfill_cell(self, cell, digit):
        row, col = cell
        self.board[row][col] = self.digit_unfilled

        updated_cells = self.each_step_updated_cells.pop()
        for row, col in updated_cells:
            self.psbl_digits[row][col].append(digit)

    def fill_with_givens(self):
        for row in xrange(self.row_size):
            for col in xrange(self.col_size):
                digit = self.initial_board[row][col]
                if digit != self.digit_unfilled:
                    self.fill_cell((row, col), digit, False)
                else:
                    self.unfilled_cells.append((row, col))

    def solve_by_dfs(self):
        # if unfilled_cells is empty, it's solved
        if not self.unfilled_cells:
            return True

        # get the cell with fewest possible answers
        self.unfilled_cells.sort(reverse=True, key=lambda cell: len(self.psbl_digits[cell[0]][cell[1]]))
        cell = self.unfilled_cells.pop()
        row, col = cell

        # try filling the cell with possible digits, and solve recursively
        psbl_digits = list(self.psbl_digits[row][col])  # copy
        for digit in psbl_digits:
            self.fill_cell(cell, digit, True)
            result = self.solve_by_dfs()
            if result:
                return True
            else:
                self.unfill_cell(cell, digit)

        # if not solved in previous section, add this cell back to unfilled_cells and go up
        self.unfilled_cells.append(cell)
        return False

    def print_result(self):
        if self.is_solved:
            print('Solved')
            self.print_board()
        else:
            print('Not Solvable')
