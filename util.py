
import numpy
import pygame

pygame.init()

WHITE = (255, 255, 255)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Constants
WIDTH = 300
HEIGHT = 400  # Increased height to accommodate buttons
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = WIDTH // BOARD_COLUMNS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
BUTTON_HEIGHT = 50

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BLACK)

# Initialize the game board
board = numpy.zeros((BOARD_ROWS, BOARD_COLUMNS))
USED_ALGORITHM = "minimax"  # Default algorithm



# Define button areas
button_areas = {
    "minimax": (0, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT),
    "alpha_beta": (WIDTH // 2, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT),
    "heuristic_basic": (0, HEIGHT - 2 * BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT),
    "heuristic_advanced": (WIDTH // 2, HEIGHT - 2 * BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT),
}


def draw_buttons():
    """Draw the algorithm selection buttons."""
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))  # Minimax
    pygame.draw.rect(screen, ORANGE, (WIDTH // 2, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))  # Alpha-Beta
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 2 * BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))  # Heuristic Basic
    pygame.draw.rect(screen, ORANGE, (WIDTH // 2, HEIGHT - 2 * BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))  # Heuristic Advanced
    font = pygame.font.Font(None, 36)
    minimax_text = font.render('Minimax', True, WHITE)
    alpha_beta_text = font.render('Alpha-Beta', True, WHITE)
    heuristic_basic_text = font.render('Heuristic Basic', True, WHITE)
    heuristic_advanced_text = font.render('Heuristic Advanced', True, WHITE)
    screen.blit(minimax_text, (WIDTH // 4 - minimax_text.get_width() // 2, HEIGHT - BUTTON_HEIGHT + 10))
    screen.blit(alpha_beta_text, (WIDTH * 3 // 4 - alpha_beta_text.get_width() // 2, HEIGHT - BUTTON_HEIGHT + 10))
    screen.blit(heuristic_basic_text, (WIDTH // 4 - heuristic_basic_text.get_width() // 2, HEIGHT - 2 * BUTTON_HEIGHT + 10))
    screen.blit(heuristic_advanced_text, (WIDTH * 3 // 4 - heuristic_advanced_text.get_width() // 2, HEIGHT - 2 * BUTTON_HEIGHT + 10))



def draw_lines(color=WHITE):
    """Draw the lines that form the game board."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_figures(color=WHITE):
    """Draw the Xs and Os on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)



def mark_square(row, col, player):
    """Mark a square with the player's number."""
    board[row][col] = player


def available_square(row, col):
    """Check if a square is available."""
    return board[row][col] == 0


def is_board_full():
    """Check if the board is full."""
    return not any(board[row][col] == 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLUMNS))


def check_win(player):
    """Check if the specified player has won."""
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLUMNS)):
            return True
    
    # Check columns
    for col in range(BOARD_COLUMNS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or \
       all(board[i][BOARD_COLUMNS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True

    return False


def canonical_board(board):
    """Convert the board to its canonical form considering symmetries."""
    rotations = [board]
    for _ in range(3):
        rotations.append(numpy.rot90(rotations[-1]))

    reflections = []
    for b in rotations:
        reflections.append(numpy.fliplr(b))
        reflections.append(numpy.flipud(b))

    canonical = min([tuple(map(tuple, b)) for b in rotations + reflections])
    return canonical


def minimax(board, depth, is_maximizing):
    """Minimax algorithm."""
    if check_win(2):
        return float('inf')
    if check_win(1):
        return float('-inf')
    if is_board_full():
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2 if is_maximizing else 1
                score = minimax(board, depth + 1, not is_maximizing)
                board[row][col] = 0
                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
    return best_score


def best_move():
    """Determine the best move using minimax."""
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    """Restart the game."""
    screen.fill(BLACK)
    draw_lines()
    board[:] = 0


def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """Minimax algorithm with alpha-beta pruning."""
    if check_win(2):
        return float('inf')
    if check_win(1):
        return float('-inf')
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score


def best_move_with_alpha_beta():
    """Determine the best move using minimax with alpha-beta pruning."""
    best_score = float('-inf')
    move = (-1, -1)
    alpha = float('-inf')
    beta = float('inf')
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_alpha_beta(board, 0, False, alpha, beta)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def minimax_heuristic_basic(board):
    """Evaluate the board state using a basic heuristic."""
    score = 0
    for i in range(BOARD_ROWS):
        row = board[i]
        col = [board[j][i] for j in range(BOARD_COLUMNS)]
        score += evaluate_line(row)
        score += evaluate_line(col)

    diag1 = [board[i][i] for i in range(BOARD_ROWS)]
    diag2 = [board[i][BOARD_COLUMNS - 1 - i] for i in range(BOARD_ROWS)]
    
    score += evaluate_line(diag1)
    score += evaluate_line(diag2)
    
    return score


def evaluate_line(line):
    """Evaluate a line for the heuristic."""
    if line.count(2) == 2 and line.count(0) == 1:
        return 10
    elif line.count(1) == 2 and line.count(0) == 1:
        return -10
    return 0


def best_move_heuristic_basic():
    """Determine the best move using a basic heuristic."""
    best_score = float('-inf')
    move = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_heuristic_basic(board)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def minimax_heuristic_advanced(board):
    """Evaluate the board state using an advanced heuristic."""
    score = 0
    for i in range(BOARD_ROWS):
        row = board[i]
        col = [board[j][i] for j in range(BOARD_COLUMNS)]
        score += evaluate_line_advanced(row, 2)
        score -= evaluate_line_advanced(row, 1)
        score += evaluate_line_advanced(col, 2)
        score -= evaluate_line_advanced(col, 1)

    diag1 = [board[i][i] for i in range(BOARD_ROWS)]
    diag2 = [board[i][BOARD_COLUMNS - 1 - i] for i in range(BOARD_ROWS)]
    
    score += evaluate_line_advanced(diag1, 2)
    score -= evaluate_line_advanced(diag1, 1)
    score += evaluate_line_advanced(diag2, 2)
    score -= evaluate_line_advanced(diag2, 1)
    
    return score


def evaluate_line_advanced(line, player):
    """Evaluate a line for the advanced heuristic."""
    if line.count(player) == 2 and line.count(0) == 1:
        return 20
    elif line.count(player) == 1 and line.count(0) == 2:
        return 5
    return 0


def best_move_heuristic_advanced():
    """Determine the best move using an advanced heuristic."""
    best_score = float('-inf')
    move = (-1, -1)
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_heuristic_advanced(board)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

