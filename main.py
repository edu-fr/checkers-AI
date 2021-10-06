import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, MINIMAX
from checkers.game import Game
from checkers.AI import minimax, AI_playing

# from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

depth_1 = 2
depth_2 = 2

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

        if game.turn == WHITE:
            value, movement = AI_playing(game.board, depth_1, WHITE, MINIMAX)
            if movement.piece is None or movement.move[0] is None or movement.move[1] is None:
                winner = RED
            else:
                game.auto_move(movement)
                print("Branco jogou")

        # if game.turn == RED:
        #     value, movement = AI_playing(game.board, RED, MINIMAX, depth_2)
        #     print("Vermelho jogou")
        #     if movement is None or movement.piece is None or movement.move[0] is None or movement.move[1] is None:
        #         winner = WHITE
        #     else:
        #         game.auto_move(movement)

        if winner is not None:              # win by drowning
            print("Red" if winner == (255, 0, 0) else "White" + " venceu por afogamento!")
            run = False
        elif game.winner() is not None:     # standard win
            print("Red" if game.winner() == (255, 0, 0) else "White" + "venceu normal!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()
