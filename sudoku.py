from copy import deepcopy

class Solution(object):
    def charToInt(self, char):
        if char == '.':
            return 0
        else:
            return int(char)

    def printIntBoard(self, intBoard):
        for row in intBoard:
            print ''.join(str(i) for i in row)

    def initSolvingUtils(self):
        board = self.originalBoard

        rowLen = self.rowLen
        colLen = self.colLen
        contUnsol = self.cellContentUnsolved
        contMin = self.cellContentMin
        contMax = self.cellContentMax

        self.unsolvedCellCoords = []
        self.possCellSols = [ [ [i for i in xrange(contMin, contMax+1) ] for w in xrange(rowLen) ] for h in xrange(colLen) ]
        # [ [ [1~9], ..9.. ], ..9.. ]

        for rowIdx in xrange(len(board)):
            for colIdx in xrange(len(board[rowIdx])):
                if board[rowIdx][colIdx] == contUnsol:
                    self.unsolvedCellCoords.append( (rowIdx,colIdx) )
                else:
                    self.updataPossCellSols(self.possCellSols, (rowIdx, colIdx), board[rowIdx][colIdx])

    def updataPossCellSols(self, possCellSols, ansCoord, ansValue):
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

    def sortUnsolvedCellCoords(self):
        # if a cell has less possible solutions, it will be in the front
        self.unsolvedCellCoords.sort(key=lambda coord: len(self.possCellSols[coord[0]][coord[1]]))

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
                self.updataPossCellSols(possCellSols, (rowCoord, colCoord), ans)
                solvingBoard[rowCoord][colCoord] = ans
                unsolvedCellCoords.pop(i)
                return "cellSolved"
            # else:
            #     continue

        return "needGuess"

    def guessAndSolve(self, solvingBoard, unsolvedCellCoords, possCellSols):
        # guessResult = "notSolved"
        for i in xrange(len(unsolvedCellCoords)):
            rowCoord, colCoord = unsolvedCellCoords[i]
            for possCellSol in possCellSols[rowCoord][colCoord]:
                tempSolvingBoard = deepcopy(solvingBoard)
                tempUnsolvedCellCoords = deepcopy(unsolvedCellCoords)
                tempPossCellSols = deepcopy(possCellSols)

                guessAns = possCellSol

                tempSolvingBoard[rowCoord][colCoord] = guessAns
                tempUnsolvedCellCoords.pop(i)
                self.updataPossCellSols(tempPossCellSols, (rowCoord, colCoord), guessAns)

                while True:
                    result = self.solveAnyCell(tempSolvingBoard, tempUnsolvedCellCoords, tempPossCellSols)
                    if result == "cellSolved":
                        continue
                    else:
                        break
                    # elif result == "boardSolved":
                    #     break
                    # elif result == "needGuess":
                    #     break
                    # else:
                    #     print "error: result not expected in guessAndSolve"
                    #     break

                if result == "boardSolved":
                    # guessResult = "correctGuess"
                    self.solvingBoard = tempSolvingBoard
                    self.unsolvedCellCoords = tempUnsolvedCellCoords
                    self.possCellSols = tempPossCellSols
                    return "boardSolved"
                # elif result == "someCellNoPossibleSol":
                #     guessResult = "wrongGuess"
                #     continue
                # elif result == "needGuess":
                #     guessResult = "stillNeedGuess"
                #     continue
                # else:
                #     print "error: result not expected in guessAndSolve"
                #     guessResult = "error"
                #     break

        return "needGuessInGuess"
        # TODO: guess in a guess

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
        self.sortUnsolvedCellCoords()

        print self.possCellSols
        print len(self.unsolvedCellCoords)

        while True:
            result = self.solveAnyCell(self.solvingBoard, self.unsolvedCellCoords, self.possCellSols)
            if result == "cellSolved":
                continue
            elif result == "boardSolved":
                break
            elif result == "needGuess":
                self.sortUnsolvedCellCoords()
                guessResult = self.guessAndSolve(self.solvingBoard, self.unsolvedCellCoords, self.possCellSols)
                print guessResult
                break
            else:
                print "error: result not expected"
                break

        print len(self.unsolvedCellCoords)
        self.printIntBoard(self.solvingBoard)

        return [''.join(str(i) for i in row) for row in self.solvingBoard]
#
# sol = Solution()
# sol.solveSudoku(["..9748...","7........",".2.1.9...","..7...24.",".64.1.59.",".98...3..","...8.3.2.","........6","...2759.."])
