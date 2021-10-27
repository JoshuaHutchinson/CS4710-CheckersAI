# Rules and assumptions
# Backwards movement only allow for Kings ("WW", "BB")
# Must take opponent's piece if possible
# Multi jumps are allowed
# Lose when no pieces left or no moves left

import numpy as np

# TO DO:
# Integrate capturing, testing, displaying board - Justin
# Implement generateSuccessors() - Joshua
# Implement human playability
# Implement agent and heuristic - Joshua


class GameState:
    currentTurn = "B"

    board = [[0, "W", 0, "W", 0, "W", 0, "W"],
                ["W", 0, "W", 0, "W", 0, "W", 0],
                [ 0, "W", 0, "W", 0, "W", 0, "W"],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                ["B", 0, "B", 0, "B", 0, "B", 0],
                [ 0, "B", 0, "B", 0, "B", 0, "B"],
                ["B", 0, "B", 0, "B", 0, "B", 0]]

    def getPiecesLocations(self, color):
        retList = []
        for row in self.board:
            for col in range(len(row)):
                if row[col] == color or row[col] == 2 * color:
                    retList.append([row, col])
        return retList

    def getPiecesCount(self, color):
        return len(self.getPiecesLocations(color))

    def getPieceColor(self, location):  # should not call on empty space
        return self.board[location[0]][location[1]][0]

    def isGameOver(self):  # add in stale mate checking
        if self.getPiecesCount("W") == 0 or self.getPiecesCount("B") == 0:
            return True
        return False

    def changeTurn(self):
        if self.currentTurn == "B":
            self.cuurentTurn = "W"
        else:
            self.currentTurn = "B"

    def generateSuccessors(self):  # need to implement
        pass

    def carryOutTurn(self, actions):
        action = AlphaBetaAgent.getAction()  # need to implement
        actions.applyAction(self, action)
        self.changeTurn()

    def checkCapturing(self, GameState, pieceLocation, pieceColor):     
        #pieceColor = GameState.board[piece]         #can be W, B, WW, BB
        teamColor = pieceColor[0]                   #corrects for kingness
        boardMax = len(GameState.board)             #make sure not to index at this row / column. 
        # y+2 < boardMax, as a capture moves you 2 spaces
        # y-1 > 0 for the same reason
        x = pieceLocation[0]
        y = pieceLocation[1]
        retList = []
        if (pieceColor != "B") and (x>1):                   #white or king, can go South, decreasing X. Can jump to row 0.
            if (y>1):
                swPoint = GameState.board[x - 1, y - 1]
                jumpPoint = GameState.board[x - 2, y - 2]           #these two get the contents- should be enemy and empty respectively
                if (swPoint[0] != teamColor) and (jumpPoint == 0):
                    newPiece = [x-2,y-2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture SW")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture SW" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                sePoint = GameState.board[x - 1, y + 1]
                jumpPoint = GameState.board[x - 2, y + 2]
                if (sePoint[0] != teamColor) and (jumpPoint == 0):
                    newPiece = [x-2,y+2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture SE")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture SE" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
        if (pieceColor != "W") and (x<boardMax-2):                   #black or king, can go North, increasing X.
            if (y>1):
                nwPoint = GameState.board[x + 1, y - 1]
                jumpPoint = GameState.board[x + 2, y - 2]
                if (nwPoint[0] != teamColor) and (jumpPoint == 0):
                    newPiece = [x+2,y-2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture NW")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture NW" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                nePoint = GameState.board[x + 1, y + 1]
                jumpPoint = GameState.board[x + 2, y + 2]
                if (nePoint[0] != teamColor) and (jumpPoint == 0):
                    newPiece = [x+2,y+2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture NE")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture NE" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
        return retList
        #This gives up to 4 options, each of which may be only the start of a chain
        #should be able to see the entire jump chain, using recursion
        #could just have applyAction run check after landing a capture, but that gives little ability to evaluate between different captures.


class Actions:
    def getPossibleActions(self, GameState, color):  # need to implement capturing
        retList = []
        pieces = GameState.getPiecesLocations(color)

        for piece in pieces: # piece = [row, col]
            pieceColor = GameState.board[piece]
            if pieceColor != "B":
                try:
                    if GameState.board[piece[0] - 1, piece[1] - 1] == 0:
                        retList.append([piece, "SW"])
                except:
                    pass
                try:
                    if GameState.board[piece[0] - 1, piece[1] + 1] == 0:
                        retList.append([piece, "SE"])
                except:
                    pass
            if pieceColor != "W":
                try:
                    if GameState.board[piece[0] + 1, piece[1] - 1] == 0:
                        retList.append([piece, "NW"])
                except:
                    pass
                try:
                    if GameState.board[piece[0] + 1, piece[1] + 1] == 0:
                        retList.append([piece, "NE"])
                except:
                    pass

        capturePossible = False
        for piece in pieces:  # piece = [row, col]
            pieceColor = GameState.board[piece]
            capturingMoves = self.checkCapturing(GameState, piece, pieceColor)
            if len(capturingMoves) > 0:
                if not capturePossible:
                    retList = capturingMoves
                if capturePossible:
                    retList.append(capturingMoves)
                capturePossible = True

        return retList

    def applyAction(self, GameState, actions):  # action = [[row, col], "direction"], need to implement capturing
        for action in actions:
            direction = action[1]
            location = action[0]
            color = GameState.board[location[0], location[1]]
            if direction == "NE":
                GameState.board[location[0], location[1]] = 0
                GameState.board[location[0] - 1, location[1] + 1] = color
            elif direction == "SE":
                GameState.board[location[0], location[1]] = 0
                GameState.board[location[0] + 1, location[1] + 1] = color
            elif direction == "SW":
                GameState.board[location[0], location[1]] = 0
                GameState.board[location[0] + 1, location[1] - 1] = color
            elif direction == "NW":
                GameState.board[location[0], location[1]] = 0
                GameState.board[location[0] - 1, location[1] - 1] = color

class AlphaBetaAgent:
    # need to adapt to checkers game
    """
    def getAction(self, GameState):
        bestAction = Directions.NORTH
        bestValue = float('-inf')
        a = bestValue
        b = -bestValue
        for action in gameState.getLegalActions(0):
            curValue = self.prune(1, 0, gameState.generateSuccessor(0, action), a, b)
            if curValue > bestValue:
                bestValue = curValue
                bestAction = action
            if bestValue > b:
                return bestValue
            a = max(a, curValue)
        return bestAction

    def prune(self, agentIndex, depth, gameState, a, b):
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        potentialActions = gameState.getLegalActions(agentIndex)
        if agentIndex == 0:
            v = float('-inf')
            for action in potentialActions:
                v = max(v, self.prune(agentIndex + 1, depth, gameState.generateSuccessor(agentIndex, action), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v
        else:
            v = float('inf')
            for action in potentialActions:
                v = min(v, self.prune(agentIndex + 1, depth, gameState.generateSuccessor(agentIndex, action), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v
    """


def main():
    game = GameState()
    actions = Actions()

    print(np.matrix(game.board))
    while not game.isGameOver():
        game.carryOutTurn(actions)
        print(np.matrix(game.board))

    print("Game Over")


main()
