import sys
import pygame
import numpy as np
import minimax
import minimax_heuristic_basic
import minimax_alpha_beta
import tt
import home
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (240, 240, 240)
BUTTON_COLOR = (0, 123, 255)  # Blue color for buttons
BUTTON_HOVER_COLOR = (0, 102, 204)  # Darker blue for hover
STOP_COLOR = (220, 53, 69)  # Red color for Stop button
RESTART_COLOR = (40, 167, 69)  # Green color for Restart button
TEXT_COLOR = (255, 255, 255)

# Proportions & Sizes
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH , HEIGHT ))

#button_screen = pygame.display.set_mode((WIDTH ,  100))
pygame.display.set_caption("Tic Tac Toe AI")
#all_screen.fill(WHITE)
screen.fill(BLACK)
board = np.zeros((BOARD_ROWS , BOARD_COLUMNS))
font = pygame.font.SysFont('Arial', 24)
# Define button rectangles
stop_button_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT - 80, 100, 60)
restart_button_rect = pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT - 80, 100, 60)

def draw_button(color, text, rect):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


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
    global board  # Access the global board variable
    board = np.zeros((3, 3))  # Reset the board to a 3x3 array of zeros

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
                    score = minimax_heuristic_basic.heuristic_function_1(board, row, col)           
                elif algorithm == "minimax_heuristic_advanced":
                    score = minimax_heuristic_basic.heuristic_function_2(board, row, col)      
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def canonical_form(board):
    """Generate the canonical form of the board considering all symmetries."""
    transformations = [
        lambda b: b,  # Original
        lambda b: np.rot90(b),  # 90 degree rotation
        lambda b: np.rot90(b, 2),  # 180 degree rotation
        lambda b: np.rot90(b, 3),  # 270 degree rotation
        lambda b: np.fliplr(b),  # Horizontal flip
        lambda b: np.flipud(b),  # Vertical flip
        lambda b: np.fliplr(np.rot90(b)),  # Horizontal flip and 90 degree rotation
        lambda b: np.flipud(np.rot90(b)),  # Vertical flip and 90 degree rotation
    ]
    
    min_board = board
    for transform in transformations:
        transformed_board = transform(board)
        if np.lexsort(transformed_board.flatten()) < np.lexsort(min_board.flatten()):
            min_board = transformed_board
    return min_board

def is_winning_move(board, player):
    """Check if the given player has a winning move on the board."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def show_endgame_menu(screen):
    # Draw the endgame menu
    screen.fill(BACKGROUND_COLOR)
    #draw_lines()  # Redraw the board lines to ensure they appear correctly
    #draw_figures()  # Redraw the figures if necessary
    draw_button(STOP_COLOR, 'Stop', stop_button_rect)
    draw_button(RESTART_COLOR, 'Restart', restart_button_rect)
    
    pygame.display.update()
def main(algorithm):
    player = 1
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                if game_over:
                    if stop_button_rect.collidepoint(mouseX, mouseY):
                        pygame.quit()
                        sys.exit()
                    
                    if restart_button_rect.collidepoint(mouseX, mouseY):
                        restart_game()
                        #main(algorithm)
                        home.create_algorithm_selection_window()  # This will call main with the selected algorithm

                else:
                    row = mouseY // SQUARE_SIZE
                    column = mouseX // SQUARE_SIZE
                    
                    if available_square(row, column):
                        mark_square(row, column, player)
                        if check_win(player):
                            game_over = True
                        player = player % 2 + 1
                        if not game_over:
                            if tt.best_move(algorithm):  # Replace with actual algorithm call
                                if check_win(2):
                                    game_over = True
                                player = player % 2 + 1
                                
                        if not game_over:
                            if is_board_full():
                                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
        
        screen.fill(BLACK)
        if not game_over:
            draw_lines()
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines()
            elif check_win(2):
                draw_figures(RED)
                draw_lines()
            else:
                draw_figures(GREY)
                draw_lines()
            show_endgame_menu(screen)
            
        pygame.display.update()