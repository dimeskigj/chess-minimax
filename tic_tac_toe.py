class TicTacToe:
    def __init__(self, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moves = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1),
                      6: (1, 2), 7: (2, 0), 8: (2, 1), 9: (2, 2)}
        self.encode = {1: "o", -1: "x", 0: " "}

    def print(self):
        for i in range(3):
            print("[%s] [%s] [%s]" % (str(i * 3 + 1) if self.board[i][0] == 0 else self.encode[self.board[i][0]],
                                      str(i * 3 + 2) if self.board[i][1] == 0 else self.encode[self.board[i][1]],
                                      str(i * 3 + 3) if self.board[i][2] == 0 else self.encode[self.board[i][2]]))

    def reset(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def move(self, move, character):
        self.board[self.moves[move][0]][self.moves[move][1]] = character

    def undo(self, move):
        self.board[self.moves[move][0]][self.moves[move][1]] = 0

    def valid_move(self, move):
        return self.board[self.moves[move][0]][self.moves[move][1]] == 0

    def no_moves(self):
        return sum([row.count(0) for row in self.board]) == 0

    def check(self):
        for row in self.board:
            if sum(row) == -3:
                return -1
            elif sum(row) == 3:
                return 1
        for i in range(3):
            if sum((self.board[0][i], self.board[1][i], self.board[2][i])) == -3:
                return -1
            if sum((self.board[0][i], self.board[1][i], self.board[2][i])) == 3:
                return 1
        if sum((self.board[0][0], self.board[1][1], self.board[2][2])) == -3 or sum(
                (self.board[0][2], self.board[1][1], self.board[2][0])) == -3:
            return -1
        if sum((self.board[0][0], self.board[1][1], self.board[2][2])) == 3 or sum(
                (self.board[0][2], self.board[1][1], self.board[2][0])) == 3:
            return 1
        return 0


if __name__ == '__main__':
    game = TicTacToe([[1, 1, 1], [1, 1, 1], [1, 1, 0]])
    print(game.no_moves())
