import numpy as np
import util


"""
def minimax_without_reduction(board, depth, is_maximizing):
    ""Minimax algorithm without symmetry reduction.""
    # Check terminal states
    if util.check_win(2):
        return float('inf')
    if util.check_win(1):
        return float('-inf')
    if util.is_board_full():
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    
    # Iterate over all possible moves
    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2 if is_maximizing else 1
                score = minimax_without_reduction(board, depth + 1, not is_maximizing)
                board[row][col] = 0
                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)

    return best_score
"""


# Memoization dictionary
memo = {}

def minimax(board, depth, is_maximizing):
    """Minimax algorithm with symmetry reduction."""
    # Get the canonical form of the board
    canonical_board = util.canonical_form(board).tobytes()  # Convert to bytes for hashing

    # Check if this board state has been evaluated before
    if canonical_board in memo:
        return memo[canonical_board]

    # Check terminal states
    if util.check_win(2):
        return float('inf')
    if util.check_win(1):
        return float('-inf')
    if util.is_board_full():
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    
    # Iterate over all possible moves
    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if board[row][col] == 0:
                board[row][col] = 2 if is_maximizing else 1
                score = minimax(board, depth + 1, not is_maximizing)
                board[row][col] = 0
                if is_maximizing:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
    
    # Memoize the result for the canonical form
    memo[canonical_board] = best_score
    return best_score
