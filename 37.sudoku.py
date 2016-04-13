from copy import deepcopy

class Solution(object):
    def charToInt(self, char):
        if char == '.':
            return 0
        else:
            return int(char)

    def initSolvingUtils(self):
        board = self.originalBoard

        rowLen = self.rowLen
        colLen = self.colLen
        contUnsol = self.cellContentUnsolved
        contMin = self.cellContentMin
        contMax = self.cellContentMax

        self.unsolvedCellCoords = []
        self.possCellSols = [ [ range(contMin, contMax+1) for w in xrange(rowLen) ] for h in xrange(colLen) ]
        # [ [ [1~9], ..9.. ], ..9.. ]

        for rowIdx in xrange(len(board)):
            for colIdx in xrange(len(board[rowIdx])):
                if board[rowIdx][colIdx] == contUnsol:
                    self.unsolvedCellCoords.append( (rowIdx,colIdx) )
                else:
                    self.updatePossCellSols(self.possCellSols, (rowIdx, colIdx), board[rowIdx][colIdx])

    def updatePossCellSols(self, possCellSols, ansCoord, ansValue):
        if len(ansCoord) != 2:
            return
        ansRowCoord, ansColCoord = ansCoord
        # update row
        for colIdx in xrange(len(possCellSols[ansRowCoord])):
            if ansValue in possCellSols[ansRowCoord][colIdx]:
                possCellSols[ansRowCoord][colIdx].remove(ansValue)

        # update col
        for rowIdx in xrange(len(possCellSols)):
            if ansValue in possCellSols[rowIdx][ansColCoord]:
                possCellSols[rowIdx][ansColCoord].remove(ansValue)

        # update block
        blockRowIdx = ansRowCoord / self.blockRowLen
        blockColIdx = ansColCoord / self.blockColLen
        for inBlockRowIdx in xrange(self.blockRowLen):
            for inBlockColIdx in xrange(self.blockColLen):
                rowIdx = blockRowIdx * self.blockRowLen + inBlockRowIdx
                colIdx = blockColIdx * self.blockColLen + inBlockColIdx
                if ansValue in possCellSols[rowIdx][colIdx]:
                    possCellSols[rowIdx][colIdx].remove(ansValue)

        # update the cell
        possCellSols[ansRowCoord][ansColCoord] = [ansValue]

    def sortUnsolvedCellCoords(self, unsolvedCellCoords, possCellSols):
        # cells having less possible solutions will be in the front
        unsolvedCellCoords.sort(key=lambda coord: len(possCellSols[coord[0]][coord[1]]))

    def solveAnyCell(self, solvingBoard, unsolvedCellCoords, possCellSols):
        if len(unsolvedCellCoords) == 0:
            return "boardSolved"

        for i in xrange(len(unsolvedCellCoords)):
            rowCoord, colCoord = unsolvedCellCoords[i]
            possCellSolsCount = len(possCellSols[rowCoord][colCoord])
            if possCellSolsCount == 0:
                return "someCellNoPossibleSol"
            elif possCellSolsCount == 1:
                ans = possCellSols[rowCoord][colCoord][0]
                self.updatePossCellSols(possCellSols, (rowCoord, colCoord), ans)
                solvingBoard[rowCoord][colCoord] = ans
                unsolvedCellCoords.pop(i)
                return "cellSolved"

        return "needGuess"

    def guessAndSolveRecursively(self, solvingBoard, unsolvedCellCoords, possCellSols):
        self.sortUnsolvedCellCoords(unsolvedCellCoords, possCellSols)

        rowCoord, colCoord = unsolvedCellCoords[0]
        for possCellSol in possCellSols[rowCoord][colCoord]:
            tempSolvingBoard = deepcopy(solvingBoard)
            tempUnsolvedCellCoords = deepcopy(unsolvedCellCoords)
            tempPossCellSols = deepcopy(possCellSols)

            guessAns = possCellSol

            tempSolvingBoard[rowCoord][colCoord] = guessAns
            tempUnsolvedCellCoords.pop(0)
            self.updatePossCellSols(tempPossCellSols, (rowCoord, colCoord), guessAns)

            while True:
                result = self.solveAnyCell(tempSolvingBoard, tempUnsolvedCellCoords, tempPossCellSols)
                if result == "cellSolved":
                    continue
                elif result == "boardSolved":
                    # guessResult = "correctGuess"
                    self.solvingBoard = tempSolvingBoard
                    self.unsolvedCellCoords = tempUnsolvedCellCoords
                    self.possCellSols = tempPossCellSols
                    return "boardSolved"
                elif result == "someCellNoPossibleSol":
                    # guessResult = "wrongGuess"
                    break # try the next possible cell solution
                elif result == "needGuess":
                    guessResult = self.guessAndSolveRecursively(tempSolvingBoard, tempUnsolvedCellCoords, tempPossCellSols)
                    if guessResult == "boardSolved":
                        return "boardSolved"
                    elif guessResult == "boardNotSolvable":
                        # previous guess is wrong
                        break # try the next possible cell solution

        # come here if can't reach "boardSolved"
        return "boardNotSolvable"

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        # change strBoard to intBoard
        self.originalBoard = [[self.charToInt(char) for char in row] for row in board]
        self.solvingBoard = [[self.charToInt(char) for char in row] for row in board]

        self.colLen = len(board)
        self.rowLen = len(board[0])
        self.blockColLen = 3
        self.blockRowLen = 3

        self.cellContentUnsolved = 0
        self.cellContentMin = 1
        self.cellContentMax = 9

        self.initSolvingUtils()
        self.sortUnsolvedCellCoords(self.unsolvedCellCoords, self.possCellSols)

        while True:
            result = self.solveAnyCell(self.solvingBoard, self.unsolvedCellCoords, self.possCellSols)
            if result == "cellSolved":
                continue
            elif result == "boardSolved":
                break
            elif result == "needGuess":
                self.sortUnsolvedCellCoords(self.unsolvedCellCoords, self.possCellSols)
                guessResult = self.guessAndSolveRecursively(self.solvingBoard, self.unsolvedCellCoords, self.possCellSols)
                break

        for i in xrange(len(board)):
            board[i] = ''.join(str(i) for i in self.solvingBoard[i])
