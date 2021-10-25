# Rules and assumptions
# Backwards movement only allow for Kings ("WW", "BB")
# Must take opponent's piece if possible
# Multi jumps are allowed
# Lose when no pieces left or no moves left

import numpy as np

# TO DO:
# Implement capturing - Justin
# Implement generateSuccessors()
# Implement driver code/print board - Joshua
# Implement human playability
# Implement agent and heuristic
# Implement king functionality

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
        for row in self.Board:
            for col in row:
                if row[col] == color:
                    retList.append([row, col])
        return retList

    def getPiecesCount(self, color):
        return len(self.getPiecesLocations(color))

    def isGameOver(self):
        if self.getPiecesCount("W") == 0 or self.getPiecesCount("B") == 0:
            return True
        return False

    def changeTurn(self):
        if self.currentTurn == "B":
            self.cuurentTurn = "W"
        else:
            self.currentTurn = "B"

    def generateSuccessors(self): # need to implement
        pass

    def carryOutTurn(self, actions):
        action = AlphaBetaAgent.getAction() # need to implement
        actions.applyAction(self, action)
        self.changeTurn()


class Actions:
    def getPossibleActions(self, GameState, color): # need to implement capturing
        retList = []
        pieces = GameState.getPiecesLocations(color)

        for piece in pieces: # piece = [row, col]
            pieceColor = GameState.Board[piece]
            if pieceColor != "B":
                try:
                    if GameState.Board[piece[0] - 1, piece[1] - 1] == 0:
                        retList.append([piece, "SW"])
                except:
                    pass
                try:
                    if GameState.Board[piece[0] - 1, piece[1] + 1] == 0:
                        retList.append([piece, "SE"])
                except:
                    pass
            if pieceColor != "W":
                try:
                    if GameState.Board[piece[0] + 1, piece[1] - 1] == 0:
                        retList.append([piece, "NW"])
                except:
                    pass
                try:
                    if GameState.Board[piece[0] + 1, piece[1] + 1] == 0:
                        retList.append([piece, "NE"])
                except:
                    pass

        return retList

    def applyAction(self, GameState, action): # action = [[row, col], "direction"], need to implement capturing
        direction = action[1]
        location = action[0]
        color = GameState.Board[location[0], location[1]]
        if direction == "NE":
            GameState.Board[location[0], location[1]] = 0
            GameState.Board[location[0] - 1, location[1] + 1] = color
        elif direction == "SE":
            GameState.Board[location[0], location[1]] = 0
            GameState.Board[location[0] + 1, location[1] + 1] = color
        elif direction == "SW":
            GameState.Board[location[0], location[1]] = 0
            GameState.Board[location[0] + 1, location[1] - 1] = color
        elif direction == "NW":
            GameState.Board[location[0], location[1]] = 0
            GameState.Board[location[0] - 1, location[1] - 1] = color

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

    print(np.Matrix(game.board))
    while not game.isGameOver():
        game.carryOutTurn(actions)
        print(np.Matrix(game.board))

    print("Game Over")