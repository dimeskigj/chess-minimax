import math
import time as t

import chess

PIECE_VALUE = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 1000,
               "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -1000}
CENTRE = (18, 19, 20, 21, 25, 26, 27, 28, 34, 35, 36, 37, 42, 43, 44, 45)
BISHOP_SQUARES = (33, 25, 30, 38)
KNIGHT_SQUARES = (42, 45, 18, 21)
PAWN_SQUARES = (19, 20, 27, 28, 35, 36, 43, 44)
WHITE, BLACK = 1, -1
CHECK_VALUE = 0.5
CASTLE_VALUE = 1


def evaluate_position(board: chess.Board, player):
    if board.result() != "*":
        return math.inf if board.result() == "1-0" else -math.inf if board.result() == "0-1" else 0
    curr = WHITE if player == WHITE else BLACK
    piece_map = board.piece_map()
    res = 0
    for piece in piece_map.keys():
        res += PIECE_VALUE[piece_map[piece].symbol()]
        if piece_map[piece].symbol().lower() != "k" and piece_map[piece].symbol().lower() != "q" and piece in CENTRE:
            res += PIECE_VALUE[piece_map[piece].symbol()]
    for sqr in BISHOP_SQUARES:
        if sqr not in piece_map: continue
        res += PIECE_VALUE[piece_map[sqr].symbol()] / 2 if piece_map[sqr].symbol().lower() == "b" else 0
    for sqr in KNIGHT_SQUARES:
        if sqr not in piece_map: continue
        res += PIECE_VALUE[piece_map[sqr].symbol()] / 2 if piece_map[sqr].symbol().lower() == "n" else 0
    for sqr in PAWN_SQUARES:
        if sqr not in piece_map: continue
        res += PIECE_VALUE[piece_map[sqr].symbol()] / 2 if piece_map[sqr].symbol().lower() == "p" else 0
    if board.is_check(): res += -CHECK_VALUE if curr == WHITE else CHECK_VALUE
    if board.has_castling_rights(chess.WHITE): res += CASTLE_VALUE
    if board.has_castling_rights(chess.BLACK): res -= CASTLE_VALUE
    return res


def next_move(board: chess.Board, player: int, depth: int):
    """
    :param player: positive = white (max), negative = black (min)
    :param depth: the depth for the search
    :param board: current board
    :return: chess.Move / none
    """
    best_eval, best_depth, alpha, beta = math.inf * -player, 0, -math.inf, math.inf
    best_move = None
    for move in board.legal_moves:
        board.push_san(move.uci())
        n_best_eval, n_best_depth = minimax(board, -player, depth - 1, alpha=-math.inf, beta=math.inf)
        board.pop()
        if best_eval != n_best_eval or best_eval == math.inf * -player:
            if player == WHITE and best_eval <= n_best_eval:
                best_eval = n_best_eval
                best_move = move
            if player == BLACK and best_eval >= n_best_eval:
                best_eval = n_best_eval
                best_move = move
        else:  # if the evaluation is the same, choose the one with the shortest path
            if n_best_depth > best_depth:
                best_move = move
        best_depth = max(best_depth, n_best_depth)
        if player == WHITE: alpha = max(alpha, best_eval)
        if player == BLACK: beta = min(beta, best_eval)
        if alpha >= beta / 10: break

    return best_move


def minimax(board: chess.Board, player: int, depth: int, alpha, beta):
    """
    :param beta: lowest evaluation found in the path
    :param alpha: highest evaluation found in the path
    :param depth: how deep the search should go on
    :param board: current board in the tree
    :param player: positive = white (max), negative = black (min)
    :return: evaluation: int, depth: int
    """
    if depth == 0 or board.result() != "*":
        return evaluate_position(board, player), depth

    result, best_depth = math.inf * -player, 0
    for move in board.legal_moves:
        board.push_san(move.uci())
        n_result, n_best_depth = minimax(board, -player, depth - 1, alpha, beta)
        board.pop()
        result = max(result, n_result) if player == WHITE else min(result, n_result)
        best_depth = max(best_depth, n_best_depth)

        if player == WHITE: alpha = max(alpha, result)
        if player == BLACK: beta = min(beta, result)
        if alpha >= beta / 10: break

    return result, best_depth


def player_move(state):
    while True:
        try:
            state.push_san(input())
            return
        except ValueError:
            print("ValueError: please enter a legal move")


DEPTH, AI = 4, WHITE

if __name__ == '__main__':
    _board = chess.Board()

    if AI == BLACK:
        print(_board.unicode(empty_square="▭", invert_color=True) + "\n")
        player_move(_board)
    while True:
        # print(len(list(board.generate_legal_captures())))
        print(_board.unicode(empty_square="▭", invert_color=True) + "\n")

        if _board.result() != "*": break

        seconds = t.time()
        best = next_move(_board, AI, DEPTH)
        seconds = math.ceil(t.time() - seconds)
        _board.push_san(best.uci())

        print("{}>time: {}\n{}".format(best.uci(), seconds, _board.unicode(empty_square="▭", invert_color=True)))
        player_move(_board)

    # while True:
    #     if _board.result() != "*": break
    #     seconds = t.time()
    #     best = next_move(_board, AI, DEPTH)
    #     seconds = math.ceil(t.time() - seconds)
    #     _board.push_san(best.uci())
    #     print("{}>time: {}\n{}".format(best.uci(), seconds, _board.unicode(empty_square="▭", invert_color=True)))
    #     AI = -AI

    print(_board.result())
