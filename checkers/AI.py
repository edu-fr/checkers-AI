from copy import deepcopy

from checkers import game
from checkers.constants import ROWS, COLS, RED, WHITE, RAND, MINIMAX


class Movement:
    def __init__(self, move, piece, skip):
        self.move = move
        self.piece = piece
        self.skip = skip


def AI_playing(board, depth, color, AI_type):
    if AI_type == MINIMAX:
        value, move = minimax(board, depth, color)
        return value, move
    else:
        return None


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


def minimax(board, depth, color):
    if depth == 0 or board.winner() is not None:
        value = ((board.get_white_left() * 2) + (1 * board.white_kings)) \
                - ((board.get_red_left() * 2) + (1 * board.red_kings))
        return value, None
    best_move = None
    best_value = float('-inf') if color == WHITE else float('inf')

    available_pieces = get_available_pieces(board, color)
    for piece in available_pieces:
        available_moves = board.get_valid_moves(piece)
        if available_moves is not None:
            for move, skip in available_moves.items():
                simulated_board = simulate_move(board, move, piece, skip)
                next_color = WHITE if (color == RED) else RED
                value, current_move = minimax(simulated_board, depth - 1, next_color)
                best_value = max(value, best_value) if color == WHITE else min(value, best_value)
                if value == best_value:
                    best_move = Movement(move, piece, skip)
    return best_value, best_move
