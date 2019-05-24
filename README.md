# sudoku-solver

A fast sudoku solver for [LeetCode 37. Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) written in Python 3.

## Result on LeetCode

* Runtime: 40 ms, faster than 99.51% of Python3 online submissions for Sudoku Solver.
* Memory Usage: 13.1 MB, less than 65.46% of Python3 online submissions for Sudoku Solver.

![result](https://i.imgur.com/2xkpY4J.png)

![graph](https://i.imgur.com/IXUYbQY.png)

(submitted on 2019/05/24)

## Algorithm

backtracking (dfs) in an optimal order

1. Keep track of candidates of each cell.
2. Find the cell with fewest candidates. Fill the cell with one of the candidates. Update the candidates of other cells.
3. Repeat step 2 until solved. Or if the board is not solvable anymore (there's any cell that is empty but has no candidates), undo step 2 and try the next candidate.

## Discuss on LeetCode

https://leetcode.com/problems/sudoku-solver/discuss/298365/Fast-Python-3-Solution-with-Comments-(40ms-faster-than-99.51)
