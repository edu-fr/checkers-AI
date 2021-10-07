import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.red_history = []
        self.white_history = []

    def set_board(self, board, red_left, red_kings, white_left, white_kings):
        self.board = board
        self.red_left = red_left
        self.white_left = white_left
        self.red_kings = red_kings
        self.white_kings = white_kings

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if not piece.king:
            if piece.color == WHITE and row == ROWS - 1:
                piece.make_king()
                self.white_kings += 1
            elif piece.color == RED and row == 0:
                piece.make_king()
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                    if piece.king:
                        self.red_kings -= 1
                else:
                    self.white_left -= 1
                    if piece.king:
                        self.white_kings -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def moves_repeated_with_king(self, color):
        counter = 0
        if color == RED:
            i = len(self.red_history) - 1
            if i < 2:
                return 0
            while i > 1:
                if self.red_history[i][3] and self.red_history[i] == self.red_history[i - 2]:
                    counter += 1
                    i -= 1
                else:
                    return counter

                if counter > 19:
                    return counter
            return counter
        else:
            i = len(self.white_history) - 1
            if i < 2:
                return 0
            while i > 1:
                if self.white_history[i][3] and self.white_history[i] == self.white_history[i - 2]:
                    counter += 1
                    i -= 1
                else:
                    return counter

                if counter > 19:
                    return counter
            return counter

    def register_movement(self, piece, origin, destination, skips):
        if piece.color == RED:
            self.red_history.append([origin, destination, skips, piece.king])
        else:
            self.white_history.append([origin, destination, skips, piece.king])

    def check_draw(self):
        return True if self.moves_repeated_with_king(WHITE) >= 20 or self.moves_repeated_with_king(RED) >= 20 else False

    def get_board(self):
        return self.board

    def get_red_left(self):
        return self.red_left

    def get_white_left(self):
        return self.white_left

    def get_red_king_left(self):
        return self.red_kings

    def get_white_king_left(self):
        return self.white_kings

    def print_history(self):
        print("RED HISTORY: ")
        print(self.red_history)
        print("WHITE HISTORY: ")
        print(self.white_history)
