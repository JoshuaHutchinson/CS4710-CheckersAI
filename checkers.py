# Rules and assumptions
# Backwards movement only allow for Kings ("WW", "BB")
# Must take opponent's piece if possible
# Multi jumps are allowed
# Lose when no pieces left or no moves left

import numpy as np
import random
import copy


# TO DO:
# Integrate capturing, testing - Justin
# Implement heuristic and default move for getAction() - Joshua


class GameState:
    def __init__(self):
        self.currentTurn = "B"
        
        '''
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, "W", 0, "W", 0, 0, 0],
                 [0, 0, 0, "BB", 0, 0, 0, 0],
                 [0, 0, "W", 0, "W", 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, "W", 0, "W", 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]

        '''
        self.board = [[0, "W", 0, "W", 0, "W", 0, "W"],
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
                    retList.append([r, col])
        return retList

    def getPiecesCount(self, color):
        return len(self.getPiecesLocations(color))

    def getKingsCount(self, color):
        ret = 0
        for r in range(len(self.board)):
            row = self.board[r]
            for col in range(len(row)):
                if row[col] == 2 * color:
                    ret += 1
        return ret

    def getPieceColor(self, location):  # should not call on empty space
        return self.board[location[0]][location[1]][0]

    def isGameOver(self, actionsObject):  # add in stale mate checking
        if self.getPiecesCount("W") == 0 or self.getPiecesCount("B") == 0 or len(actionsObject.getPossibleActions(self, self.currentTurn)) == 0 :#or len(actionsObject.getPossibleActions(self, "B")) == 0:
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
            thisGame = copy.deepcopy(self)
            # weird multicapture getaround?
            try:
                single = [possible[action]]
                actionsObject.applyAction(thisGame, single)
            except:
                multicapture = possible[action]
                actionsObject.applyAction(thisGame, multicapture)
            # print("generating successor ", multicapture)
            # Actions.applyAction(thisGame, [possible[action]])
            retList.append(thisGame)
        return retList

    def carryOutTurn(self, actionsObject):
        action = AlphaBetaAgent.getAction()  # need to implement
        actionsObject.applyAction(self, action)
        self.changeTurn()

    def checkCapturing(self, gameObject, pieceLocation, pieceColor):
        # pieceColor = GameState.board[piece]         #can be W, B, WW, BB
        teamColor = pieceColor[0]  # corrects for kingness
        boardMax = len(gameObject.board)  # make sure not to index at this row / column.
        further = []
        # y+2 < boardMax, as a capture moves you 2 spaces
        # y-1 > 0 for the same reason
        x = pieceLocation[0]
        y = pieceLocation[1]
        retList = []
        if (pieceColor != "W") and (x > 1):  # white or king, can go South, decreasing X. Can jump to row 0.
            if (y > 1):
                swPoint = gameObject.board[x - 1][y - 1]
                jumpPoint = gameObject.board[x - 2][
                    y - 2]  # these two get the contents- should be enemy and empty respectively
                if (swPoint != teamColor and swPoint != 2 * teamColor and swPoint != 0) and (jumpPoint == 0):
                    newPiece = [x - 2, y - 2]
                    #print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                    #    newPiece) + " direction: NW")
                    # gameObject.board[x - 1][y - 1] = 0

                    hypothetical = copy.deepcopy(gameObject)
                    hypothetical.board[x][y] = 0
                    hypothetical.board[x - 1][y - 1] = 0
                    hypothetical.board[x - 2][y - 2] = pieceColor

                    further = self.checkCapturing(hypothetical, newPiece,
                                                  pieceColor)  # recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture NW"]]
                    if further == []:
                        if retList == []:
                            retList.append(move)  # simple 1 capture
                    else:
                        for capture in further:
                            retList.append(
                                move + capture)  # multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y < boardMax - 2):
                sePoint = gameObject.board[x - 1][y + 1]
                jumpPoint = gameObject.board[x - 2][y + 2]
                if (sePoint != teamColor and sePoint != 2 * teamColor and sePoint != 0) and (jumpPoint == 0):
                    newPiece = [x - 2, y + 2]
                    #print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                    #    newPiece) + " direction: NE")
                    # gameObject.board[x - 1][y + 1] = 0

                    hypothetical = copy.deepcopy(gameObject)
                    hypothetical.board[x][y] = 0
                    hypothetical.board[x - 1][y + 1] = 0
                    hypothetical.board[x - 2][y + 2] = pieceColor

                    further = self.checkCapturing(hypothetical, newPiece,
                                                  pieceColor)  # recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture NE"]]
                    if further == []:
                        retList.append(move)  # simple 1 capture
                    else:
                        for capture in further:
                            retList.append(
                                move + capture)  # multiple capture options NE, SE, NW, SW. Add those to simple capture.
        if (pieceColor != "B") and (x < boardMax - 2):  # black or king, can go North, increasing X.
            if (y > 1):
                nwPoint = gameObject.board[x + 1][y - 1]
                jumpPoint = gameObject.board[x + 2][y - 2]
                if (nwPoint != teamColor and nwPoint != 2 * teamColor and nwPoint != 0) and (
                        jumpPoint == 0):  # and nwPoint != 2*teamColor
                    newPiece = [x + 2, y - 2]
                    #print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                    #    newPiece) + " direction: SW")
                    # gameObject.board[x + 1][y - 1] = 0

                    hypothetical = copy.deepcopy(gameObject)
                    hypothetical.board[x][y] = 0
                    hypothetical.board[x + 1][y - 1] = 0
                    hypothetical.board[x + 2][y - 2] = pieceColor

                    further = self.checkCapturing(hypothetical, newPiece,
                                                  pieceColor)  # recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture SW"]]
                    if further == []:
                        retList.append(move)  # simple 1 capture
                    else:
                        for capture in further:
                            retList.append(
                                move + capture)  # multiple capture options NE, SE, NW, SW. Add those to simple capture.
            if (y < boardMax - 2):
                nePoint = gameObject.board[x + 1][y + 1]
                jumpPoint = gameObject.board[x + 2][y + 2]
                if (nePoint != teamColor and nePoint != 2 * teamColor and nePoint != 0) and (jumpPoint == 0):
                    newPiece = [x + 2, y + 2]
                    #print("Piece location: " + str(pieceLocation) + " new piece location: " + str(
                    #    newPiece) + " direction: SE")
                    # gameObject.board[x + 1][y + 1] = 0

                    hypothetical = copy.deepcopy(gameObject)
                    hypothetical.board[x][y] = 0
                    hypothetical.board[x + 1][y + 1] = 0
                    hypothetical.board[x + 2][y + 2] = pieceColor

                    further = self.checkCapturing(hypothetical, newPiece,
                                                  pieceColor)  # recursively makes a list of all possible jumps from that position
                    move = [[pieceLocation, "Capture SE"]]
                    if further == []:
                        retList.append(move)  # simple 1 capture
                    else:
                        for capture in further:
                            retList.append(
                                move + capture)  # multiple capture options NE, SE, NW, SW. Add those to simple capture.
        return retList
        # This gives up to 4 options, each of which may be only the start of a chain
        # should be able to see the entire jump chain, using recursion


class Actions:
    def getPossibleActions(self, gameObject, color):  # need to implement capturing
        retList = []
        pieces = gameObject.getPiecesLocations(color)

        for piece in pieces:  # piece = [row,col]
            pieceColor = gameObject.board[piece[0]][piece[1]]
            if pieceColor != "W":
                try:
                    if gameObject.board[piece[0] - 1][piece[1] - 1] == 0 and piece[0] > 0 and piece[1] > 0:
                        retList.append([[piece, "NW"]])
                except:
                    pass
                try:
                    if gameObject.board[piece[0] - 1][piece[1] + 1] == 0 and piece[0] > 0 and piece[1] < 7:
                        retList.append([[piece, "NE"]])
                except:
                    pass
            if pieceColor != "B":
                try:
                    if gameObject.board[piece[0] + 1][piece[1] - 1] == 0 and piece[0] < 7 and piece[1] > 0:
                        retList.append([[piece, "SW"]])
                except:
                    pass
                try:
                    if gameObject.board[piece[0] + 1][piece[1] + 1] == 0 and piece[0] < 7 and piece[1] < 7:
                        retList.append([[piece, "SE"]])
                except:
                    pass

        capturePossible = False
        for piece in pieces:  # piece = [row, col]
            pieceColor = gameObject.board[piece[0]][piece[1]]
            capturingMoves = gameObject.checkCapturing(gameObject, piece, pieceColor)
            if len(capturingMoves) > 0:
                if not capturePossible:
                    retList = capturingMoves
                if capturePossible:
                    retList.append(capturingMoves)
                capturePossible = True
        return retList

    def applyAction(self, gameObject, actions):  # action = [[row, col], "direction"], need to implement capturing
        if gameObject.isGameOver(self):
            return
        #print("full actions is", actions)
        actions = actions[0]
        for action in actions:
            direction = action[1]
            location = action[0]
            #print("Number of pieces left: Black: " + str(gameObject.getPiecesCount("B")) + " White: " + str(
            #    gameObject.getPiecesCount("W")))
            #print("Current action: " + str(action))
            #print("Current board", print(np.matrix(gameObject.board)))
            color = gameObject.board[location[0]][location[1]]
            if direction == "NE":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] - 1][location[1] + 1] = color
            elif direction == "SE":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] + 1][location[1] + 1] = color
            elif direction == "SW":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] + 1][location[1] - 1] = color
            elif direction == "NW":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] - 1][location[1] - 1] = color
            elif direction == "Capture NE":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] - 1][location[1] + 1] = 0
                gameObject.board[location[0] - 2][location[1] + 2] = color
            elif direction == "Capture SE":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] + 1][location[1] + 1] = 0
                gameObject.board[location[0] + 2][location[1] + 2] = color
            elif direction == "Capture SW":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] + 1][location[1] - 1] = 0
                gameObject.board[location[0] + 2][location[1] - 2] = color
            elif direction == "Capture NW":
                gameObject.board[location[0]][location[1]] = 0
                gameObject.board[location[0] - 1][location[1] - 1] = 0
                gameObject.board[location[0] - 2][location[1] - 2] = color
        self.promoting(gameObject, color)
        #print(np.matrix(gameObject.board))

    def promoting(self, gameObject, color):
        boardMax = len(gameObject.board)
        pieces = gameObject.getPiecesLocations(color)
        if color == "W":
            for piece in pieces:
                if piece[0] == boardMax - 1:
                    gameObject.board[piece[0]][piece[1]] = "WW"
        if color == "B":
            for piece in pieces:
                if piece[0] == 0:
                    gameObject.board[piece[0]][piece[1]] = "BB"


class AlphaBetaAgent:
    def evaluationFunction(self, gameObject, color):
        selfCount = gameObject.getPiecesCount(color)  # Count number of pieces agent has
        numKings = gameObject.getKingsCount(color)  # Count number of kings agent has

        # Switch color
        if color == "B":
            color = "W"
        else:
            color = "B"
        enemyCount = -1 * gameObject.getPiecesCount(color)  # Count number of piece opponent has
        numEnemyKings = -1 * gameObject.getKingsCount(color)  # Count number of kings opponent has

        return 1 * selfCount + 3 * enemyCount + 1 * numKings + 2 * numEnemyKings
        #Could change to something more complicated. Incorporate kings, potential kings, potential captures even?

    def getAction(self, gameObject, actionsObject, color):
        # need to figure out default move
        if color == "B":
            bestAction = [[5, 0], "NE"]  # default action should just be first item in actionsObject.
        else:
            bestAction = [[2, 7], "SW"]
        bestValue = float('-inf')
        a = bestValue
        b = -bestValue
        possible = actionsObject.getPossibleActions(gameObject, color)
        for choice in range(len(possible)):
            newState = GameState()
            # print("attempting to apply action", possible[choice])
            # actionsObject.applyAction(newState, [possible[choice]])## should call with actions as [a[choice]], where a is possible actions, b is index.

            try:
                actionsObject.applyAction(newState, [possible[choice]])
            except:
                actionsObject.applyAction(newState, possible[choice])

            curValue = self.prune(newState, 4, a, b, color, color, actionsObject)
            if curValue > bestValue:
                bestValue = curValue
                bestAction = possible[choice]
                # print("bestAction = ", possible[choice])
            if bestValue > b:
                return bestValue
            a = max(a, curValue)
        return bestAction

    def prune(self, gameObject, depth, a, b, color, maximizingColor, actionsObject):
        if depth == 0 or gameObject.isGameOver(actionsObject):
            return self.evaluationFunction(gameObject, color)
        potentialStates = gameObject.generateSuccessors(actionsObject, color)
        if color == "W":
            color = "B"
        else:
            color = "W"
        depth -= 1
        if color == maximizingColor:
            v = float('-inf')
            for state in potentialStates:
                v = max(v, self.prune(state, depth, a, b, color, maximizingColor, actionsObject))
                if v > b:
                    return v
                a = max(a, v)
            return v
        else:
            v = float('inf')
            for state in potentialStates:
                v = min(v, self.prune(state, depth, a, b, color, maximizingColor, actionsObject))
                if v < a:
                    return v
                b = min(b, v)
            return v

class ExpectiMaxAgent:
    def evaluationFunction(self, gameObject, color):
        selfCount = gameObject.getPiecesCount(color)  # Count number of pieces agent has
        numKings = gameObject.getKingsCount(color)  # Count number of kings agent has

        # Switch color
        if color == "B":
            color = "W"
        else:
            color = "B"
        enemyCount = -1 * gameObject.getPiecesCount(color)  # Count number of piece opponent has
        numEnemyKings = -1 * gameObject.getKingsCount(color)  # Count number of kings opponent has

        return 1 * selfCount + 3 * enemyCount + 1 * numKings + 2 * numEnemyKings
        #Could change to something more complicated. Incorporate kings, potential kings, potential captures even?

    def getAction(self, gameObject, actionsObject, color):
        # need to figure out default move
        if color == "B":
            bestAction = [[5, 0], "NE"]  # default action should just be first item in actionsObject.
        else:
            bestAction = [[2, 7], "SW"]
        bestValue = float('-inf')
        a = bestValue
        b = -bestValue
        possible = actionsObject.getPossibleActions(gameObject, color)
        for choice in range(len(possible)):
            newState = GameState()
            # print("attempting to apply action", possible[choice])
            # actionsObject.applyAction(newState, [possible[choice]])## should call with actions as [a[choice]], where a is possible actions, b is index.
            try:
                actionsObject.applyAction(newState, [possible[choice]])
            except:
                actionsObject.applyAction(newState, possible[choice])
            curValue = self.prune(newState, 4, a, b, color, color, actionsObject)
            if curValue > bestValue:
                bestValue = curValue
                bestAction = possible[choice]
                # print("bestAction = ", possible[choice])
            if bestValue > b:
                return bestValue
            a = max(a, curValue)
        return bestAction

    def prune(self, gameObject, depth, a, b, color, maximizingColor, actionsObject):
        if depth == 0 or gameObject.isGameOver(actionsObject):
            return self.evaluationFunction(gameObject, color)
        potentialStates = gameObject.generateSuccessors(actionsObject, color)
        if color == "W":
            color = "B"
        else:
            color = "W"
        depth -= 1
        if color == maximizingColor:
            v = float('-inf')
            for state in potentialStates:
                v = max(v, self.prune(state, depth, a, b, color, maximizingColor, actionsObject))
                if v > b:
                    return v
                a = max(a, v)
            return v
        else:
            vTotal = 0
            for state in potentialStates:
                vTotal += self.prune(state, depth, a, b, color, maximizingColor, actionsObject)
            v = vTotal/len(potentialStates)
            return v

class RandomAgent:
    def getAction(self, gameObject, actionsObject, color):
        possible = actionsObject.getPossibleActions(gameObject, color)
        r = random.randint(0, len(possible) - 1)
        return r


def main():
    game = GameState()
    actions = Actions()

    print("Pick Black Agent- PLAYER (P), RANDOM (R), MINIMAX(M), or EXPECTIMAX(E)")
    agent1 = str(input()).upper()
    print("Pick White Agent- PLAYER (P), RANDOM (R), MINIMAX(M), oe EXPECTIMAX(E)")
    agent2 = str(input()).upper()

    # game.board = game.capturingBoard
    # game.board = game.board

    agents = {"B": agent1, "W": agent2}
    #turnsTaken = 0
    while not game.isGameOver(actions):
        #turnsTaken += 1
        print(np.matrix(game.board))
        a = actions.getPossibleActions(game, game.currentTurn)
        if len(a) == 0:
            print(game.currentTurn, "has no moves. Game Over.")
            if game.currentTurn=="B":
                print("White Wins")
            if game.currentTurn=="W":
                print("Black Wins")
            return
        if agents[game.currentTurn] == "PLAYER" or agents[game.currentTurn] == "P" or agents[game.currentTurn] == "1":
            print("Input an integer 0 or greater among moves available for", game.currentTurn, " :")
            for move in range(len(a)):
                print(move, ": ", a[move])
            choice = int(input())
            try:
                actions.applyAction(game, [a[choice]])
            except:
                actions.applyAction(game, a[choice])
        if agents[game.currentTurn] == "AI" or agents[game.currentTurn] == "A" or agents[
            game.currentTurn] == "MINIMAX" or agents[game.currentTurn] == "M" or agents[game.currentTurn] == "2":
            ai = AlphaBetaAgent()
            choice = ai.getAction(game, actions, game.currentTurn)
            try:
                actions.applyAction(game, [choice])
            except:
                actions.applyAction(game, choice)
        if agents[game.currentTurn] == "R" or agents[game.currentTurn] == "RANDOM" or agents[game.currentTurn] == "3":
            ai = RandomAgent()
            choice = int(ai.getAction(game, actions, game.currentTurn))
            try:
                actions.applyAction(game, [a[choice]])
            except:
                actions.applyAction(game, a[choice])
        if agents[game.currentTurn] == "E" or agents[game.currentTurn] == "EXPECTIMAX" or agents[game.currentTurn] == "4":
            ai = ExpectiMaxAgent()
            choice = ai.getAction(game, actions, game.currentTurn)
            try:
                actions.applyAction(game, [choice])
            except:
                actions.applyAction(game, choice)
        game.changeTurn()
        #print(turnsTaken)
    print(np.matrix(game.board))
    print("Game Over")
    if game.currentTurn=="B":
        print(game.getPiecesCount("B"), "Black pieces left. White Wins")
    if game.currentTurn=="W":
        print(game.getPiecesCount("W"), "White pieces left. Black Wins")


main()
