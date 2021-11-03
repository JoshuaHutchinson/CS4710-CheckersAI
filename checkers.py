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

    capturingBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, "W", 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, "W", 0, "W", 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, "W", 0, "W", 0, 0, 0],
                    [0, 0, 0, "B", 0, 0, 0, 0]]

    def getPiecesLocations(self, color):
        retList = []
        for r in range(len(self.board)):
            row = self.board[r]
            for col in range(len(row)):
                if row[col] == color or row[col] == 2 * color:
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
        if (pieceColor != "W") and (x>1):                   #white or king, can go South, decreasing X. Can jump to row 0.
            if (y>1):
                swPoint = GameState.board[x - 1][y - 1]
                jumpPoint = GameState.board[x - 2][y - 2]           #these two get the contents- should be enemy and empty respectively
                if (swPoint != teamColor and swPoint != 2*teamColor and swPoint != 0) and (jumpPoint == 0):
                    newPiece = [x-2,y-2]
                    further = self.checkCapturing(GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture NW"]]
                    if further == []:
                        if retList == []:
                            retList.append(move)                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append(move + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                sePoint = GameState.board[x - 1][y + 1]
                jumpPoint = GameState.board[x - 2][y + 2]
                if (sePoint != teamColor and sePoint != 2*teamColor and sePoint != 0) and (jumpPoint == 0):
                    newPiece = [x-2,y+2]
                    further = self.checkCapturing(GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture NE"]]
                    if further == []:
                        retList.append(move)                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append(move + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
        if (pieceColor != "B") and (x<boardMax-2):                   #black or king, can go North, increasing X.
            if (y>1):
                nwPoint = GameState.board[x + 1][y - 1]
                jumpPoint = GameState.board[x + 2][y - 2]
                if (nwPoint != teamColor and nwPoint != 2*teamColor and nwPoint != 0) and (jumpPoint == 0):    # and nwPoint != 2*teamColor
                    newPiece = [x+2,y-2]
                    further = self.checkCapturing(GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture SW"]]
                    if further == []:
                        retList.append(move)                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append(move + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                nePoint = GameState.board[x + 1][y + 1]
                jumpPoint = GameState.board[x + 2][y + 2]
                if (nePoint != teamColor and nePoint != 2*teamColor and nePoint != 0) and (jumpPoint == 0):
                    newPiece = [x+2,y+2]
                    further = self.checkCapturing(GameState, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture SE"]]
                    if further == []:
                        retList.append(move)                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append(move + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
        return retList
        #This gives up to 4 options, each of which may be only the start of a chain
        #should be able to see the entire jump chain, using recursion
        #could just have applyAction run check after landing a capture, but that gives little ability to evaluate between different captures.


class Actions:
    def getPossibleActions(self, GameState, color):  # need to implement capturing
        retList = []
        pieces = GameState.getPiecesLocations(color)

        for piece in pieces: # piece = [row,col]
            pieceColor = GameState.board[piece[0]][piece[1]]
            if pieceColor != "W":
                try:
                    if GameState.board[piece[0] - 1][piece[1] - 1] == 0 and piece[0] > 0 and piece[1] > 0:
                        retList.append([[piece, "NW"]])
                except:
                    pass
                try:
                    if GameState.board[piece[0] - 1][piece[1] + 1] == 0 and piece[0] > 0 and piece[1] < 7:
                        retList.append([[piece, "NE"]])
                except:
                    pass
            if pieceColor != "B":
                try:
                    if GameState.board[piece[0] + 1][piece[1] - 1] == 0 and piece[0] < 7 and piece[1] > 0:
                        retList.append([[piece, "SW"]])
                except:
                    pass
                try:
                    if GameState.board[piece[0] + 1][piece[1] + 1] == 0 and piece[0] < 7 and piece[1] < 7:
                        retList.append([[piece, "SE"]])
                except:
                    pass

        capturePossible = False
        for piece in pieces:  # piece = [row, col]
            pieceColor = pieceColor = GameState.board[piece[0]][piece[1]]
            capturingMoves = GameState.checkCapturing(GameState, piece, pieceColor)
            if len(capturingMoves) > 0:
                if not capturePossible:
                    retList = capturingMoves
                if capturePossible:
                    retList.append(capturingMoves)
                capturePossible = True
        return retList

    def applyAction(self, GameState, actions):  # action = [[row, col], "direction"], need to implement capturing
        actions = actions[0]
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
            elif direction == "Capture NE":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] - 1][location[1] + 1] = 0
                GameState.board[location[0] - 2][location[1] + 2] = color
            elif direction == "Capture SE":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] + 1][location[1] + 1] = 0
                GameState.board[location[0] + 2][location[1] + 2] = color
            elif direction == "Capture SW":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] + 1][location[1] - 1] = 0
                GameState.board[location[0] + 2][location[1] - 2] = color
            elif direction == "Capture NW":
                GameState.board[location[0]][location[1]] = 0
                GameState.board[location[0] - 1][location[1] - 1] = 0
                GameState.board[location[0] - 2][location[1] - 2] = color

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
            return self.evaluationFunction(GameState, color)
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

    game.board = game.capturingBoard

    if (agent1 == "PLAYER" or agent1=="P") and (agent2 == "PLAYER" or agent2=="P"):       #just for testing, real should implement playing
        while not game.isGameOver():
            print(np.matrix(game.board))
            a = actions.getPossibleActions(game, game.currentTurn)
            print("Input an integer 0 or greater among moves available for", game.currentTurn, " :")
            for move in range(len(a)):
                print(move, ": ", a[move])
            choice = int(input())
            actions.applyAction(game,[a[choice]])
            game.changeTurn()

    print("Game Over")


main()
