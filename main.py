import sys
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, MINIMAX, RAND
from checkers.game import Game
from checkers.AI import ai_playing, check_if_possible_moves

# from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 40)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    red_cpu = True
    white_cpu = True

    # 1: depth1 , 2: depth2, 3: CPU1_alg, 4: CPU2+_alg    
    args = sys.argv[1:]
    args[0] = int(args[0])
    args[1] = int(args[1])
    
    if(len(args) >= 3):
        if args[2] is not None:
            args[2] = MINIMAX if args[2] == "MINIMAX" else RAND
        if(len(args) >= 4):
            if args[2] is not None and args[3] is not None:
                args[3] = MINIMAX if args[3] == "MINIMAX" else RAND
        else:
            red_cpu = False
    else:
        white_cpu = False
        red_cpu = False

    start = time.time()
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

        if game.turn == RED:
            if not check_if_possible_moves(game.board, RED):
                winner = WHITE
            else:
                if red_cpu:
                    value, movement = ai_playing(game.board, args[1], RED, args[3])
                    if movement is not None and movement.piece is not None \
                            and movement.move[0] is not None and movement.move[1] is not None:
                        game.auto_move(movement)


        if game.turn == WHITE:
            if not check_if_possible_moves(game.board, WHITE):
                winner = RED
            else:
                if white_cpu:
                    value, movement = ai_playing(game.board, args[0], WHITE, args[2])

                    if movement is not None and movement.piece is not None \
                            and movement.move[0] is not None and movement.move[1] is not None:  # double checking
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
    pygame.quit()
    end = time.time()

main()
