import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, MINIMAX
from checkers.game import Game
from checkers.AI import AI_playing, check_if_possible_moves

# from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 40)

depth_1 = 1
depth_2 = 4

red_cpu = True
white_cpu = True


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    winner = None

    while run:
        clock.tick(FPS)

        if game.board.check_draw():
            print("Empate!")
            run = False
            continue

        if game.turn == WHITE:
            if not check_if_possible_moves(game.board, WHITE):
                winner = RED
            else:
                if white_cpu:
                    value, movement = AI_playing(game.board, depth_1, WHITE, MINIMAX)
                    if movement is not None and movement.piece is not None \
                            and movement.move[0] is not None and movement.move[1] is not None:  # double checking
                        game.auto_move(movement)

        if game.turn == RED:
            if not check_if_possible_moves(game.board, RED):
                winner = WHITE
            else:
                if red_cpu:
                    value, movement = AI_playing(game.board, depth_2, RED, MINIMAX)
                    if movement is not None and movement.piece is not None \
                            and movement.move[0] is not None and movement.move[1] is not None:
                        game.auto_move(movement)

        if game.winner() is not None:  # standard win
            print("Red venceu por capturar todas as peças!" if game.winner() == (
            255, 0, 0) else "White venceu por capturar todas as peças!")
            run = False
        elif winner is not None:  # win by drowning
            print("Red venceu por afogar White!" if winner == (255, 0, 0) else "White venceu por afogar Red!")
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if (not red_cpu and game.turn == RED) or (not white_cpu and game.turn == WHITE):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()
        # You can use `render` and then blit the text surface ...

    pygame.quit()


main()
