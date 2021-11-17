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
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, "W", 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, "W", 0, "W", 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, "W", 0, 0, 0, 0, 0],
             [0, 0, 0, "B", 0, 0, 0, 0]]

    '''
    board = [[0, "W", 0, "W", 0, "W", 0, "W"],
                ["W", 0, "W", 0, "W", 0, "W", 0],
                [ 0, "W", 0, "W", 0, "W", 0, "W"],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 0,  0,  0,  0,  0,  0,  0,  0],
                ["B", 0, "B", 0, "B", 0, "B", 0],
                [ 0, "B", 0, "B", 0, "B", 0, "B"],
                ["B", 0, "B", 0, "B", 0, "B", 0]]
    '''

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

    def generateSuccessors(self, actionsObject, color):
        retList = []
        possible = actionsObject.getPossibleActions(self, color)
        for action in range(len(possible)):
            thisGame = GameState()
            #weird multicapture getaround?
            try:
                single = [possible[action]]
                Actions.applyAction(thisGame, single)
            except:
                multicapture = possible[action]
                Actions.applyAction(thisGame, multicapture)
            #print("generating successor ", multicapture)
            #Actions.applyAction(thisGame, [possible[action]])
            retList.append(thisGame)
        return retList

    def carryOutTurn(self, actionsObject):
        action = AlphaBetaAgent.getAction()  # need to implement
        actionsObject.applyAction(self, action)
        self.changeTurn()

    def checkCapturing(self, gameObject, pieceLocation, pieceColor):
        #pieceColor = GameState.board[piece]         #can be W, B, WW, BB
        teamColor = pieceColor[0]                   #corrects for kingness
        boardMax = len(gameObject.board)             #make sure not to index at this row / column.
        # y+2 < boardMax, as a capture moves you 2 spaces
        # y-1 > 0 for the same reason
        x = pieceLocation[0]
        y = pieceLocation[1]
        retList = []
        if (pieceColor != "W") and (x>1):                   #white or king, can go South, decreasing X. Can jump to row 0.
            if (y>1):
                swPoint = gameObject.board[x - 1][y - 1]
                jumpPoint = gameObject.board[x - 2][y - 2]           #these two get the contents- should be enemy and empty respectively
                if (swPoint != teamColor and swPoint != 2*teamColor and swPoint != 0) and (jumpPoint == 0):
                    newPiece = [x-2,y-2]
                    print("Piece location: " + str(pieceLocation) + " new piece location: " + str(newPiece) + " direction: NW")
                    further = self.checkCapturing(gameObject, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture NW"]]
                    if further == []:
                        if retList == []:
                            retList.append(move)                            #simple 1 capture
                    else:
                        for capture in further:
                            retList.append(move + capture)                 #multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y<boardMax-2):
                sePoint = gameObject.board[x - 1][y + 1]
                jumpPoint = gameObject.board[x - 2][y + 2]
                if (sePoint != teamColor and sePoint != 2*teamColor and sePoint != 0) and (jumpPoint == 0):
                    newPiece = [x-2,y+2]
                    print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                        newPiece) + " direction: NE")
                    further = self.checkCapturing(gameObject, newPiece, pieceColor)    #recursively makes a list of all possible jumps from that position
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
                    print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                        newPiece) + " direction: SW")
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
                    print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                        newPiece) + " direction: SE")
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
            pieceColor = GameState.board[piece[0]][piece[1]]
            capturingMoves = GameState.checkCapturing(GameState, piece, pieceColor)
            if len(capturingMoves) > 0:
                if not capturePossible:
                    retList = capturingMoves
                if capturePossible:
                    retList.append(capturingMoves)
                capturePossible = True
        return retList

    def applyAction(self, game, actions):  # action = [[row, col], "direction"], need to implement capturing
        if game.isGameOver():
            return
        actions = actions[0]
        for action in actions:
            direction = action[1]
            location = action[0]
            print("Number of pieces left: Black: " + str(game.getPiecesCount("B")) + " White: " + str(game.getPiecesCount("W")))
            print("Current action: " + str(action))
            color = game.board[location[0]][location[1]]
            if direction == "NE":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] - 1][location[1] + 1] = color
            elif direction == "SE":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] + 1][location[1] + 1] = color
            elif direction == "SW":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] + 1][location[1] - 1] = color
            elif direction == "NW":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] - 1][location[1] - 1] = color
            elif direction == "Capture NE":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] - 1][location[1] + 1] = 0
                game.board[location[0] - 2][location[1] + 2] = color
            elif direction == "Capture SE":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] + 1][location[1] + 1] = 0
                game.board[location[0] + 2][location[1] + 2] = color
            elif direction == "Capture SW":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] + 1][location[1] - 1] = 0
                game.board[location[0] + 2][location[1] - 2] = color
            elif direction == "Capture NW":
                game.board[location[0]][location[1]] = 0
                game.board[location[0] - 1][location[1] - 1] = 0
                game.board[location[0] - 2][location[1] - 2] = color
        self.promoting(game, color)
        print(np.matrix(game.board))
    
    def promoting(self, GameState, color):
        boardMax = len(GameState.board)
        pieces = GameState.getPiecesLocations(color)
        if color=="W":
            for piece in pieces:
                if piece[0] == boardMax-1:
                    GameState.board[piece[0]][piece[1]] = "WW"
        if color=="B":
            for piece in pieces:
                if piece[0] == 0:
                    GameState.board[piece[0]][piece[1]] = "BB"

class AlphaBetaAgent:
    def evaluationFunction(self, game, color):
        return game.getPiecesCount(color)  # change to something more complicated. Incorporate kings, potential kings, potential captures even?

    def getAction(self, game, Actions, color):
        # need to figure out default move
        if color == "B":
            bestAction = [[5, 0], "NE"]
        else:
            bestAction = [[2, 7], "SW"]
        bestValue = float('-inf')
        a = bestValue
        b = -bestValue
        possible = Actions.getPossibleActions(game, color)
        for choice in range(len(possible)):
            newState = GameState()
            #print("attempting to apply action", possible[choice])
            Actions.applyAction(newState, [possible[choice]])## should call with actions as [a[choice]], where a is possible actions, b is index.
            curValue = self.prune(newState, 10, a, b, color, color, Actions)
            if curValue > bestValue:
                bestValue = curValue
                bestAction = possible[choice]
                #print("bestAction = ", possible[choice])
            if bestValue > b:
                return bestValue
            a = max(a, curValue)
        return bestAction

    def prune(self, game, depth, a, b, color, maximizingColor, Actions):
        if depth == 0 or game.isGameOver():
            return self.evaluationFunction(game, color)
        potentialStates = game.generateSuccessors(Actions, color)
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

    #game.board = game.capturingBoard
    #game.board = game.board

    agents = [agent1,agent2]

    if agents.count("PLAYER")==2 or agents.count("P")==2 or agents.count("1")==2:
        print("2 player")
        while not game.isGameOver():
            print(np.matrix(game.board))
            a = actions.getPossibleActions(game, game.currentTurn)
            if len(a)==0:
                print("Game Over")
                return
            print("Input an integer 0 or greater among moves available for", game.currentTurn, " :")
            for move in range(len(a)):
                print(move, ": ", a[move])
            choice = int(input())
            actions.applyAction(game,[a[choice]])
            game.changeTurn()
    if agents.count("AI")==2 or agents.count("A")==2 or agents.count("2")==2:
        print("2 AI")
        ai = AlphaBetaAgent()
        while not game.isGameOver():
            print(np.matrix(game.board))
            a = actions.getPossibleActions(game, game.currentTurn)
            if len(a)==0:
                print("Game Over")
                return
            choice = ai.getAction(game, actions, game.currentTurn)
            print("Choice: " + str(choice))
            actions.applyAction(game,choice)
            game.changeTurn()
    #implement PvE

    print("Game Over")


main()
