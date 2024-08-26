import util
import numpy as np

def minimax_heuristic_basic(board, player):
    """Evaluate the board state for Player 2 by calculating potential winning possibilities for each move."""
    score = 0
    opponent = 1 
    player = 2

    # Evaluate all rows, columns, and diagonals
    for i in range(util.BOARD_ROWS):
        row = board[i]
        col = [board[j][i] for j in range(util.BOARD_COLUMNS)]
        score += evaluate_line(row, player, opponent)
        score += evaluate_line(col, player, opponent)

    diag1 = [board[i][i] for i in range(util.BOARD_ROWS)]
    diag2 = [board[i][util.BOARD_COLUMNS - 1 - i] for i in range(util.BOARD_ROWS)]
    score += evaluate_line(diag1, player, opponent)
    score += evaluate_line(diag2, player, opponent)

    return score

def evaluate_line(line, player, opponent):
    """Evaluate a line for potential winning possibilities for Player 2 and blocking the opponent."""
    score = 0

    if np.sum(line == player) == 3:
        score += 100  
    elif np.sum(line == player) == 2 and np.sum(line == 0) == 1:
        score += 10  

    if np.sum(line == opponent) == 3:
        score -= 100  
    elif np.sum(line == opponent) == 2 and np.sum(line == 0) == 1:
        score -= 10  

    return score

