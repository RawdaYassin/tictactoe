import sys
import pygame
import util 

# Initialize Pygame
pygame.init()


def main():
    """Main game loop."""
    util.draw_lines()
    util.draw_buttons()

    player = 1
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                row = mouse_y // util.SQUARE_SIZE
                col = mouse_x // util.SQUARE_SIZE

                if util.available_square(row, col):
                    util.mark_square(row, col, player)
                    if util.check_win(player):
                        game_over = True
                    player = 3 - player  # Switch player

                    if not game_over:
                        if util.USED_ALGORITHM == "minimax":
                            if util.best_move():
                                if util.check_win(2):
                                    game_over = True
                                player = 3 - player
                        elif util.USED_ALGORITHM == "minimax_alpha_beta":
                            if util.best_move_with_alpha_beta():
                                if util.check_win(2):
                                    game_over = True
                                player = 3 - player
                        elif util.USED_ALGORITHM == "minimax_heuristic_basic":
                            if util.best_move_heuristic_basic():
                                if util.check_win(2):
                                    game_over = True
                                player = 3 - player
                        elif util.USED_ALGORITHM == "minimax_heuristic_advanced":
                            if util.best_move_heuristic_advanced():
                                if util.check_win(2):
                                    game_over = True
                                player = 3 - player

                    if not game_over and util.is_board_full():
                        game_over = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                util.restart_game()
                game_over = False
                player = 1

        if not game_over:
            util.draw_figures()
        else:
            if util.check_win(1):
                util.draw_figures(util.GREEN)
                util.draw_lines(util.GREEN)
            elif util.check_win(2):
                util.draw_figures(util.RED)
                util.draw_lines(util.RED)
            else:
                util.draw_figures(util.GREY)
                util.draw_lines(util.GREY)

        pygame.display.update()


if __name__ == "__main__":
    main()
