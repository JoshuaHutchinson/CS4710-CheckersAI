# Rules and assumptions
# Backwards movement only allow for Kings ("WW", "BB")
# Must take opponent's piece if possible
# Multi jumps are allowed
# Lose when no pieces left or no moves left

import numpy as np

# TO DO:
# Integrate capturing, testing - Justin
# Implement heuristic and default move for getAction() - Joshua


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
        for r in range(len(self.board)):
            row = self.board[r]
            for col in range(len(row)):
                if row[col] == color or row[col] == 2 * color:
                    #print("at x ", row, "or r ", r," and y ", col, " we have ", color)
                    retList.append([r, col])
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
            self.currentTurn = "W"
        else:
            self.currentTurn = "B"

    def generateSuccessors(self, Actions, color):
        retList = []
        for action in Actions.getPossibleActions(self, color):
            thisGame = GameState()
            Actions.applyAction(thisGame, action)
            retList.append(thisGame)
        return retList

    def makeKings(self):
        if self.currentTurn == "W":
            for pieceLocation in self.getPiecesLocations("W"):
                if pieceLocation[0] == 7:
                    self.board[pieceLocation[0]][pieceLocation[1]] = "WW"
        else:
            for pieceLocation in self.getPiecesLocations("B"):
                if pieceLocation[0] == 0:
                    self.board[pieceLocation[0]][pieceLocation[1]] = "BB"

    def carryOutTurn(self, actions):
        action = AlphaBetaAgent.getAction()  # need to implement
        actions.applyAction(self, action)
        self.makeKings()
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
                swPoint = GameState.board[x - 1][y - 1]
                jumpPoint = GameState.board[x - 2][y - 2]           #these two get the contents- should be enemy and empty respectively
                if (swPoint != teamColor) and (jumpPoint == 0):
                    newPiece = [x-2,y-2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture SW")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture SW" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                sePoint = GameState.board[x - 1][y + 1]
                jumpPoint = GameState.board[x - 2][y + 2]
                if (sePoint != teamColor) and (jumpPoint == 0):
                    newPiece = [x-2,y+2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture SE")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture SE" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
        if (pieceColor != "W") and (x<boardMax-2):                   #black or king, can go North, increasing X.
            if (y>1):
                nwPoint = GameState.board[x + 1][y - 1]
                jumpPoint = GameState.board[x + 2][y - 2]
                if (nwPoint != teamColor) and (jumpPoint == 0):
                    newPiece = [x+2,y-2]
                    further = self.checkCapturing(self, GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    if further == []:
                        retList.append("Capture NW")                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append("Capture NW" + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                nePoint = GameState.board[x + 1][y + 1]
                jumpPoint = GameState.board[x + 2][y + 2]
                if (nePoint != teamColor) and (jumpPoint == 0):
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

        for piece in pieces: # piece = [row,col]
            #print(piece)
            #print(piece[0][0])
            #print(GameState.board[piece[0]][piece[1]])
            pieceColor = GameState.board[piece[0]][piece[1]]
            if pieceColor != "W":
                try:
                    #print("piece ", piece," going NW")
                    #print(piece[0] - 1, " , ", piece[1] - 1)
                    #print(GameState.board[piece[0] - 1][piece[1] - 1], "\n")
                    if GameState.board[piece[0] - 1][piece[1] - 1] == 0 and piece[0] > 0 and piece[1] > 0:
                        #print(piece, "can go NW")
                        retList.append([piece, "NW"])
                except:
                    pass
                try:
                    #print("piece ", piece," going NE")
                    #print(piece[0] - 1, " , ", piece[1] + 1)
                    #print(GameState.board[piece[0] - 1][piece[1] + 1], "\n")
                    if GameState.board[piece[0] - 1][piece[1] + 1] == 0 and piece[0] > 0 and piece[1] < 7:
                        #print(piece, "can go NE")
                        retList.append([piece, "NE"])
                except:
                    pass
            if pieceColor != "B":
                try:
                    #print("piece ", piece," going SW")
                    #print(piece[0] + 1, " , ", piece[1] - 1)
                    #print(GameState.board[piece[0] + 1][piece[1] - 1], "\n")
                    if GameState.board[piece[0] + 1][piece[1] - 1] == 0 and piece[0] < 7 and piece[1] > 0:
                        #print(piece, "can go SW")
                        retList.append([piece, "SW"])
                except:
                    pass
                try:
                    #print("piece ", piece," going SE")
                    #print(piece[0] + 1, " , ", piece[1] + 1)
                    #print(GameState.board[piece[0] + 1][piece[1] + 1], "\n")
                    if GameState.board[piece[0] + 1][piece[1] + 1] == 0 and piece[0] < 7 and piece[1] < 7:
                        #print(piece, "can go SE")
                        retList.append([piece, "SE"])
                except:
                    pass

        capturePossible = False
        for piece in pieces:  # piece = [row, col]
            #print(piece)
            pieceColor = pieceColor = GameState.board[piece[0]][piece[1]]
            capturingMoves = GameState.checkCapturing(GameState, piece, pieceColor)
            #capturingMoves = self.checkCapturing(GameState, piece, pieceColor)
            if len(capturingMoves) > 0:
                print("capture possible at ", piece)
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
            color = GameState.board[location[0]][location[1]]
            if direction == "NE":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] - 1][location[1] + 1] = color
            elif direction == "SE":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] + 1][location[1] + 1] = color
            elif direction == "SW":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] + 1][location[1] - 1] = color
            elif direction == "NW":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] - 1][location[1] - 1] = color

class AlphaBetaAgent:
    def evaluationFunction(self, GameState, color):
        return GameState.getPiecesCount(color)  # change to something more complicated

    def getAction(self, GameState, Actions, color):
        # need to figure out default move
        if color == "B":
            bestAction = [[5, 0], "NE"]
        else:
            bestAction = [[2, 7], "SW"]
        bestValue = float('-inf')
        a = bestValue
        b = -bestValue
        for action in Actions.getPossibleActions(GameState, color):
            newState = GameState()
            Actions.applyAction(newState, [action])
            curValue = self.prune(newState, 10, a, b, color, color, Actions)
            if curValue > bestValue:
                bestValue = curValue
                bestAction = action
            if bestValue > b:
                return bestValue
            a = max(a, curValue)
        return bestAction

    def prune(self, GameState, depth, a, b, color, maximizingColor, Actions):
        if depth == 0 or GameState.isGameOver():
            return self.evaluationFunction(gameState, color)
        potentialStates = GameState.generateSuccessors(Actions, color)
        if color == "W":
            color = "B"
        else:
            color = "W"
        depth -= 1
        if color == maximizingColor:
            v = float('-inf')
            for state in potentialStates:
                v = max(v, self.prune(state, depth, a, b, color, maximizingColor, Actions))
                if v > b:
                    return v
                a = max(a, v)
            return v
        else:
            v = float('inf')
            for state in potentialStates:
                v = min(v, self.prune(state, depth, a, b, color, maximizingColor, Actions))
                if v < a:
                    return v
                b = min(b, v)
            return v


def main():
    game = GameState()
    actions = Actions()

    print("Choose Agent 1- AI or PLAYER")
    agent1 = str(input()).upper()
    print("Choose Agent 2- AI or PLAYER")
    agent2 = str(input()).upper()

    #print(np.matrix(game.board))

    if agent1 == "PLAYER" and agent2 == "PLAYER":       #just for testing, real should implement playing
        while not game.isGameOver():
            print(np.matrix(game.board))
            a = actions.getPossibleActions(game, game.currentTurn)
            print("Input an integer 0 or greater among moves available for", game.currentTurn, " :")
            for move in range(len(a)):
                print(move, ": ", a[move])
            choice = int(input())
            actions.applyAction(game,[a[choice]])
            game.changeTurn()

    #while not game.isGameOver():
    #    game.carryOutTurn(actions)
    #    print(np.matrix(game.board))

    print("Game Over")


main()
