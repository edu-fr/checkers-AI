import pygame

from .AI import check_if_possible_moves
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        # Show how many kings there are on game
        # from main import font, WIN
        # if font is not None:
        #     text_surface = font.render("WK: " + str(self.board.white_kings) + " RK: " + str(self.board.red_kings), False, BLUE)
        #     WIN.blit(text_surface, (0, 0))
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        else:
            self.selected = None
            self.valid_moves = None

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.board.register_movement(self.selected, [self.selected.row, self.selected.col], [row, col], skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        if moves is None:
            return None
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_valid_moves(self):
        return self.valid_moves

    def get_selected(self):
        return self.selected

    def auto_move(self, movement):

        self.board.register_movement(movement.piece, [movement.piece.row, movement.piece.col],
                                     [movement.move[0], movement.move[1]], movement.skip)
        self.board.move(movement.piece, movement.move[0], movement.move[1])
        if movement.skip:
            self.board.remove(movement.skip)
        self.change_turn()


