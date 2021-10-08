import copy
import math
from copy import deepcopy
from random import randrange
from checkers import game
from checkers.constants import ROWS, COLS, RED, WHITE, RAND, MINIMAX


class Movement:
    def __init__(self, move, piece, skip):
        self.move = move
        self.piece = piece
        self.skip = skip


def ai_playing(board, depth, color, AI_type):
    beta = math.inf
    alpha = - math.inf
    if AI_type == MINIMAX:
        value, move = minimax(board, depth, color,alpha,beta)
        return value, move
    else:
        value, move = random_ia(board, color, depth)
        return value, move

def check_if_possible_moves(board, color):
    available_pieces = get_available_pieces(board, color)
    for piece in available_pieces:
        if len(board.get_valid_moves(piece)) > 0:
            return True
    return False


def get_available_pieces(board, color):
    available_pieces = []
    for row in range(ROWS):
        for col in range(COLS):
            current_piece = board.get_piece(row, col)
            if current_piece == 0 or current_piece.get_color() != color:
                continue
            available_pieces.append(current_piece)
    return available_pieces


def simulate_move(board, move, piece, skip):
    new_board = deepcopy(board)
    piece_copy = deepcopy(piece)
    new_board.move(piece_copy, move[0], move[1])
    if skip:
        new_board.remove(skip)
    return new_board


def minimax(board, depth, color,alpha,beta):
    aux_break = False
    if depth == 0 or board.winner() is not None:
        value = ((board.get_white_left() * 1) + (2 * board.white_kings)) \
                - ((board.get_red_left() * 1) + (2 * board.red_kings))
        return value, None
    best_move = None
    best_value = float('-inf') if color == WHITE else float('inf')

    available_pieces = get_available_pieces(board, color)
    for piece in available_pieces:
        available_moves = board.get_valid_moves(piece)

        if aux_break:
            break
        if available_moves is not None:
            for move, skip in available_moves.items():
                simulated_board = simulate_move(board, move, piece, skip)
                next_color = WHITE if (color == RED) else RED
                value, current_move = minimax(simulated_board, depth - 1, next_color,alpha,beta)
                best_value = max(value, best_value) if color == WHITE else min(value, best_value)

                if value == best_value:
                    best_move = Movement(move, piece, skip)

                if color == WHITE:
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        aux_break = True
                        break
                else:
                    beta = min(beta, value)
                    if beta <= alpha:
                        aux_break = True
                        break

    return best_value, best_move


def rate_movement(movement, board):

    simulated_board = simulate_move(board, movement.move, movement.piece, movement.skip)
    value = ((board.get_white_left() * 1) + (2 * board.white_kings)) \
            - ((board.get_red_left() * 1) + (2 * board.red_kings))

    value2 = ((simulated_board.get_white_left() * 1) + (2 * simulated_board.white_kings)) \
            - ((simulated_board.get_red_left() * 1) + (2 * simulated_board.red_kings))

    return value2 - value if movement.piece.color == RED else -1 * (value2 - value)


def random_ia(board, color, list_size):

    list_moves = []
    best_moves = []

    available_pieces = get_available_pieces(board, color)
    for piece in available_pieces:
        available_moves = board.get_valid_moves(piece)

        if available_moves is not None:
            for move, skip in available_moves.items():
                movement = Movement(move, piece, skip)
                list_moves.append([rate_movement(movement, board), movement])

    if len(list_moves) < list_size:
        list_size = len(list_moves)
    if len(list_moves) == 0:
        return None, None
    else:
        sorted(list_moves, key=lambda tup: tup[0])
        for i in range(0, list_size):
            best_moves.append(list_moves[i])
        if list_size == 1:
            index_random = 0
        else:
            index_random = randrange(list_size - 1)

    return best_moves[index_random][0], best_moves[index_random][1]
