class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        # check rows
        for row in board:
            charSet = set()
            for char in row:
                if char != '.':
                    if char in charSet:
                        return False
                    charSet.add(char)

        # check cols
        for colIdx in xrange(9):
            charSet = set()
            for rowIdx in xrange(9):
                char = board[rowIdx][colIdx]
                if char != '.':
                    if char in charSet:
                        return False
                    charSet.add(char)

        # check blocks
        for blockRowIdx in [0,3,6]:
            for blockColIdx in [0,3,6]:
                charSet = set()
                for inBlockRowIdx in xrange(3):
                    for inBlockColIdx in xrange(3):
                        char = board[blockRowIdx+inBlockRowIdx][blockColIdx+inBlockColIdx]
                        if char != '.':
                            if char in charSet:
                                return False
                            charSet.add(char)

        return True
