# Rules and assumptions
# Backwards movement only allow for Kings ("WW", "BB")
# Must take opponent's piece if possible
# Multi jumps are allowed
# Lose when no pieces left or no moves left

# TO DO:
# Implement capturing
# Implement generateSuccessors()
# Implement driver code/print board
# Implement human playability
# Implement agent and heuristic

class GameState:
    currentTurn = "B"

    board = [[0, "W", 0, "W", 0, "W", 0, "W"],
             ["W", 0, "W", 0, "W", 0, "W", 0],
             [0, "W", 0, "W", 0, "W", 0, "W"],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             ["B", 0, "B", 0, "B", 0, "B", 0],
             [0, "B", 0, "B", 0, "B", 0, "B"],
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
