from copy import deepcopy
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
        print("morre")
        return None


def get_available_pieces(board, color):
    available_pieces = []
    for row in range(ROWS):
        for col in range(COLS):
            current_piece = board.get_piece(row, col)
            if current_piece == 0 or current_piece.get_color() != color:
                continue
            available_pieces.append(current_piece)
    print("Peças disponiveis: " + str(len(available_pieces)))
    return available_pieces


def simulate_move(board, move, piece, skip):
    new_board = deepcopy(board)
    new_board.move(piece, move[0], move[1])
    if skip:
        new_board.remove(skip)
    return new_board


def minimax(board, depth, color):
    if depth == 0 or board.winner() is not None:
        value = board.get_white_left() - board.get_red_left()
        return value, None

    best_move = None

    best_value = float('-inf') if color == WHITE else float('inf')
    available_pieces = get_available_pieces(board, color)
    for piece in available_pieces:
        available_moves = board.get_valid_moves(piece)
        if available_moves is not None:
            for move, skip in available_moves.items():
                simulated_board = simulate_move(board, move, piece, skip)
                value, current_move = minimax(simulated_board, depth - 1, WHITE if (color == RED) else RED)
                best_value = max(value, best_value) if color == WHITE else min(value, best_value)
                if value == best_value:
                    best_move = Movement(move, piece, skip)
        else:
            return 0, None
    print("Cheguei! Best value: " + str(best_value) + " Best move: (" +
          str(best_move.move[0]) + ", " + str(best_move.move[1]) + ")")
    return best_value, best_move
