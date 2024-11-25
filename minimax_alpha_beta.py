import numpy as np
import util


"""
def minimax_alpha_beta_without_reduction(board, depth, is_maximizing, alpha, beta):
    "Minimax algorithm with alpha-beta pruning without symmetry reduction."
    # Check terminal states
    if util.check_win(2):
        return float('inf')
    if util.check_win(1):
        return float('-inf')
    if util.is_board_full():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(util.BOARD_ROWS):
            for col in range(util.BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax_alpha_beta_without_reduction(board, depth + 1, False, alpha, beta)
                    board[row][col] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for row in range(util.BOARD_ROWS):
            for col in range(util.BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax_alpha_beta_without_reduction(board, depth + 1, True, alpha, beta)
                    board[row][col] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score


    """
    
# Memoization dictionary
memo = {}

def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """Minimax algorithm with alpha-beta pruning and symmetry reduction."""
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

    if is_maximizing:
        best_score = float('-inf')
        for row in range(util.BOARD_ROWS):
            for col in range(util.BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        # Memoize the result for the canonical form
        memo[canonical_board] = best_score
        return best_score
    else:
        best_score = float('inf')
        for row in range(util.BOARD_ROWS):
            for col in range(util.BOARD_COLUMNS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        # Memoize the result for the canonical form
        memo[canonical_board] = best_score
        return best_score
