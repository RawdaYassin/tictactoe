import sys
import pygame
import numpy
import minimax
import minimax_heuristic_basic
import minimax_alpha_beta
import test
import minimax_heuristic_advanced

pygame.init()

# Colors
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportions & Sizes
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BLACK)
board = numpy.zeros((BOARD_ROWS , BOARD_COLUMNS))


def draw_lines(color =WHITE):
    for i in range(1 , BOARD_ROWS):
        pygame.draw.line(screen, color, (0 , SQUARE_SIZE * i), (WIDTH , SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i , 0), (SQUARE_SIZE * i , HEIGHT), LINE_WIDTH)
        

def draw_figures(color = WHITE):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 1:
                pygame.draw.circle(screen, color, (int(column * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][column] == 2:
                pygame.draw.line(screen, color, (column * SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + SQUARE_SIZE // 4 ), (column * SQUARE_SIZE + 3*SQUARE_SIZE // 4 , row * SQUARE_SIZE + 3*SQUARE_SIZE // 4 ), CROSS_WIDTH)
                pygame.draw.line(screen, color, (column * SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + 3*SQUARE_SIZE // 4 ), (column * SQUARE_SIZE + 3*SQUARE_SIZE // 4 , row * SQUARE_SIZE + SQUARE_SIZE // 4 ), CROSS_WIDTH)


def mark_square(row, column, player):
    board[row][column] = player   


def available_square(row, column):
    return board[row][column] == 0


def is_board_full(check_board = board):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if check_board[row][column] == 0:
                return False
    return True

def check_win(player, check_board = board):

    for column in range(BOARD_COLUMNS):
        if check_board[0][column] == player and check_board[1][column] == player and check_board[2][column] == player:
            return True
    
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def restart_game():
    board = numpy.zeros((BOARD_ROWS , BOARD_COLUMNS))

def best_move(algorithm):
    """Determine the best move using a basic heuristic."""
    best_score = float('-inf')
    move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                if algorithm == "minimax":
                    score = minimax.minimax(board, 0, False)     
                elif algorithm == "minimax_alpha_beta":
                    score = minimax_alpha_beta.minimax_alpha_beta(board, 0, False,  float('-inf'),  float('inf'))     
                elif algorithm == "minimax_heuristic_basic":
                    score = test.heuristic_function_1(board, row, col)           
                elif algorithm == "minimax_heuristic_advanced":
                    score = test.heuristic_function_2(board, row, col)      
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False



def main(algorithm):
    draw_lines()
    player = 1
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                row = mouseY // SQUARE_SIZE
                column = mouseX // SQUARE_SIZE
                
                if available_square(row, column):
                    mark_square(row, column, player)
                    if check_win(player):
                        game_over = True
                    player = player % 2 + 1
                    if not game_over:
                        if best_move(algorithm):
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1
                            
                    if not game_over:
                        if is_board_full():
                            game_over = True
                            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.k_r:
                    restart_game()
                    game_over = False
                    player = 1
        
        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GREY)
                draw_lines(GREY)
            
        pygame.display.update()
        
