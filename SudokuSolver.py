"""
written in Python 3

Find all the solutions of a given board.

Algorithm: backtracking (dfs) in an optimal order
1. Keep track of candidates of each cell.
2. Find the cell with fewest candidates. Fill the cell with one of the candidates. Update the candidates of other cells.
3. Repeat step 2 until solved. Or if the board is not solvable anymore (there's any cell that is empty but has no candidates), undo step 2 and try the next candidate.
"""

from copy import deepcopy


class SudokuSolver:
    col_size = 9  # len(self.board)
    row_size = 9  # len(self.board[0])
    block_col_size = 3
    block_row_size = 3
    digits = '123456789'
    empty_symbol = ' '

    # def solve_board(self, board: List[List[str]]) -> None:
    def solve_board(self, board):
        self.init_board(board)
        self.solve()
        return self.solutions

    def init_board(self, board):
        self.board = deepcopy(board)

        # list all empty cells. a `cell` is a tuple `(row_index, col_index)`
        self.empty_cells = set([(ri, ci) for ri in range(self.row_size) for ci in range(self.col_size) if self.board[ri][ci] == self.empty_symbol])

        # find candidates of each cell
        self.candidates = [[set(self.digits) for ci in range(self.col_size)] for ri in range(self.row_size)]
        for ri in range(self.row_size):
            for ci in range(self.col_size):
                digit = self.board[ri][ci]
                if digit != self.empty_symbol:
                    self.candidates[ri][ci] = set()
                    self.update_candidates((ri, ci), digit)

        self.solutions = []

    def solve(self):
        # if there are no empty cells, it's solved
        if not self.empty_cells:
            self.solutions.append(deepcopy(self.board))
            return

        # get the cell with fewest candidates
        cell = min(self.empty_cells, key=lambda cell: len(self.candidates[cell[0]][cell[1]]))

        # try filling the cell with one of the candidates, and solve recursively
        ri, ci = cell
        for digit in list(self.candidates[ri][ci]):
            candidate_updated_cells = self.fill_cell(cell, digit)
            solved = self.solve()
            self.unfill_cell(cell, digit, candidate_updated_cells)

    def fill_cell(self, cell, digit):
        # fill the cell with the digit
        ri, ci = cell
        self.board[ri][ci] = digit

        # remove the cell from empty_cells
        self.empty_cells.remove(cell)

        # update the candidates of other cells
        # keep a list of updated cells. will be used when unfilling cells
        candidate_updated_cells = self.update_candidates(cell, digit)

        return candidate_updated_cells

    def unfill_cell(self, cell, digit, candidate_updated_cells):
        # unfill cell
        ri, ci = cell
        self.board[ri][ci] = self.empty_symbol

        # add the cell back to empty_cells
        self.empty_cells.add(cell)

        # add back candidates of other cells
        for ri, ci in candidate_updated_cells:
            self.candidates[ri][ci].add(digit)

    def update_candidates(self, filled_cell, digit):
        candidate_updated_cells = []
        for ri, ci in self.related_cells(filled_cell):
            if (self.board[ri][ci] == self.empty_symbol) and (digit in self.candidates[ri][ci]):
                self.candidates[ri][ci].remove(digit)
                candidate_updated_cells.append((ri, ci))
        return candidate_updated_cells

    def related_cells(self, cell):
        return list(set(self.cells_in_same_row(cell) + self.cells_in_same_col(cell) + self.cells_in_same_block(cell)))

    def cells_in_same_row(self, cell):
        return [(cell[0], ci) for ci in range(self.col_size)]

    def cells_in_same_col(self, cell):
        return [(ri, cell[1]) for ri in range(self.row_size)]

    def cells_in_same_block(self, cell):
        block_first_cell_ri = (cell[0] // self.block_row_size) * self.block_row_size
        block_first_cell_ci = (cell[1] // self.block_col_size) * self.block_col_size
        return [
            (block_first_cell_ri + in_block_ri, block_first_cell_ci + in_block_ci)
            for in_block_ri in range(self.block_row_size)
            for in_block_ci in range(self.block_col_size)
        ]

    def print_solutions(self, boards):
        for board in boards:
            self.print_board(board)

    def print_board(self, board):
        border = '+' + '+'.join(['-'.join('-' * self.block_col_size)] * (self.row_size // self.block_col_size)) + '+'
        inside_border = '+' + '+'.join([' '.join(' ' * self.block_col_size)] * (self.row_size // self.block_col_size)) + '+'

        print(border)
        for ri in range(self.row_size):
            if ri % self.block_row_size == 0 and ri != 0:
                print(border)
            row = board[ri]
            row_str = '|'
            for block_col_idx in range(self.row_size // self.block_row_size):
                start_ci = block_col_idx * self.block_col_size
                end_ci = start_ci + self.block_col_size
                row_str += ' '.join(row[start_ci:end_ci]) + '|'
            print(row_str)
        print(border)


if __name__ == '__main__':
    import time

    board_0 = [
        ['8','2',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ','3','6',' ',' ',' ',' ',' '],
        [' ','7',' ',' ','9',' ','2',' ',' '],
        [' ','5',' ',' ',' ','7',' ',' ',' '],
        [' ',' ',' ',' ','4','5','7',' ',' '],
        [' ',' ',' ','1',' ',' ',' ','3',' '],
        [' ',' ','1',' ',' ',' ',' ','6','8'],
        [' ',' ','8','5',' ',' ',' ','1',' '],
        [' ','9',' ',' ',' ',' ','4',' ',' ']
    ]
    # [hardest sudoku](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html)
    board_1 = [
        ['8',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ','3','6',' ',' ',' ',' ',' '],
        [' ','7',' ',' ','9',' ','2',' ',' '],
        [' ','5',' ',' ',' ','7',' ',' ',' '],
        [' ',' ',' ',' ','4','5','7',' ',' '],
        [' ',' ',' ','1',' ',' ',' ','3',' '],
        [' ',' ','1',' ',' ',' ',' ','6','8'],
        [' ',' ','8','5',' ',' ',' ','1',' '],
        [' ','9',' ',' ',' ',' ','4',' ',' ']
    ]
    board_2 = [
        [' ','8',' ',' ',' ','9','7','4','3'],
        [' ','5',' ',' ',' ','8',' ','1',' '],
        [' ','1',' ',' ',' ',' ',' ',' ',' '],
        ['8',' ',' ','2',' ','5',' ',' ',' '],
        [' ',' ',' ','8',' ','4',' ',' ',' '],
        [' ',' ',' ','3',' ',' ',' ',' ','6'],
        [' ',' ',' ',' ',' ',' ',' ','7',' '],
        [' ','3',' ','5',' ',' ',' ','8',' '],
        ['9','7','2','4',' ',' ',' ','5',' '],
    ]
    solver = SudokuSolver()

    def solve_and_print(board):
        start_time = time.time()
        solutions = solver.solve_board(board)
        elapsed_time = time.time() - start_time

        print('board to solve:')
        solver.print_board(board)
        print('{} solution found in {} seconds.'.format(len(solutions), elapsed_time))
        solver.print_solutions(solutions)
        print()

    solve_and_print(board_0)
    solve_and_print(board_1)
    solve_and_print(board_2)
