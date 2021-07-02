import math

from tic_tac_toe import TicTacToe

positions = {(0, 0): 1, (0, 1): 2, (0, 2): 3,
             (1, 0): 4, (1, 1): 5, (1, 2): 6,
             (2, 0): 7, (2, 1): 8, (2, 2): 9}

MIN_MINIMUM, MAX_MAXIMUM = -1, 1


def next_move(state):
    mini, move = math.inf, 0
    board = state.board
    for position in positions.keys():
        if state.board[position[0]][position[1]] == 0:
            board[position[0]][position[1]] = -1
            result = minimax(state, 1)
            if result < mini:
                mini = result
                move = positions[position]
            board[position[0]][position[1]] = 0
            if mini == MIN_MINIMUM: return move
    return move


def minimax(state, player):
    if state.no_moves() or state.check() != 0:
        return state.check()
    board = state.board
    res = math.inf * -player

    for position in positions.keys():
        if state.board[position[0]][position[1]] == 0:
            board[position[0]][position[1]] = player
            res = max(minimax(state, -player), res) if player == 1 else min(minimax(state, -player), res)
            board[position[0]][position[1]] = 0
        if res == MAX_MAXIMUM and player == 1: return res
        if res == MIN_MINIMUM and player == -1: return res

    return res


if __name__ == '__main__':
    game = TicTacToe()

    player_next = False
    while not game.no_moves() and game.check() == 0:
        if player_next:
            __move = int(input())
            while not game.valid_move(__move):
                print("Invalid move, please enter another one")
                __move = int(input())
            game.move(__move, 1)
        else:
            game.move(next_move(game), -1)
        if not player_next: game.print()
        player_next = not player_next

    if not player_next: game.print()
    print("{} won!".format("O" if game.check() == 1 else "X") if game.check() != 0 else "Tie!")
