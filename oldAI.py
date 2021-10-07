import math
from copy import deepcopy
import pygame
from checkers.board import Board
from checkers.constants import ROWS, COLS, RED, WHITE
from checkers.piece import Piece


class Movement:
    def __init__(self, move, piece, skip):
        self.move = move
        self.piece = piece
        self.skip = skip


def minimax(board, depth, maximizing, color, no_move_available):
    if depth == 0 or board.winner() is not None:
        value = board.get_white_left() - board.get_red_left()
        return value, None

    movement = Movement(None, None, None)

    if maximizing:  # CPU
        max_value = - math.inf
        for row in range(ROWS):
            for col in range(COLS):
                current_piece = board.get_piece(row, col)
                if current_piece == 0 or current_piece.get_color() != color:
                    continue
                valid_moves = board.get_valid_moves(current_piece)
                if valid_moves is not None:
                    no_move_available = False
                    for valid_move, skip in valid_moves.items():
                        new_board = deepcopy(board)
                        new_Board = Board()

                        new_Board.board = new_board
                        new_Board.red_kings = board.red_kings
                        new_Board.red_left = board.red_left
                        new_Board.white_kings = board.white_kings
                        new_Board.white_left = board.white_left
                        new_Board.board.move(new_Board.board.get_piece(row, col),
                                             valid_move[0], valid_move[1])
                        if skip:
                            new_Board.board.remove(skip)
                        current_value = minimax(new_Board.board, depth - 1, False, WHITE if (color == RED) else RED,
                                                no_move_available)
                        max_value = max(max_value, current_value[0])
                        if max_value == current_value[0]:
                            movement.move = valid_move
                            movement.piece = board.get_piece(row, col)
                            movement.skip = skip
        if no_move_available:
            print("DRAW")
        return max_value, movement

    else:  # CPU 2
        min_value = math.inf
        min_move = None
        min_piece = None
        for row in range(ROWS):
            for col in range(COLS):
                current_piece = board.get_piece(row, col)
                if current_piece == 0 or current_piece.get_color() != color:
                    continue
                valid_moves = board.get_valid_moves(current_piece)
                if valid_moves is not None:
                    no_move_available = False
                    for valid_move, skip in valid_moves.items():
                        new_board = deepcopy(board)
                        new_Board = Board()

                        new_Board.board = new_board
                        new_Board.red_kings = board.red_kings
                        new_Board.red_left = board.red_left
                        new_Board.white_kings = board.white_kings
                        new_Board.white_left = board.white_left
                        new_Board.board.move(new_Board.board.get_piece(row, col),
                                             valid_move[0], valid_move[1])
                        if skip:
                            new_Board.board.remove(skip)
                        current_value = minimax(new_Board.board, depth - 1, True, WHITE if (color == RED) else RED,
                                                no_move_available)
                        min_value = min(min_value, current_value[0])
                        if min_value == current_value[0]:
                            movement.move = valid_move
                            movement.piece = board.get_piece(row, col)
                            movement.skip = skip
        if no_move_available:
            print("DRAW")
        return min_value, movement
