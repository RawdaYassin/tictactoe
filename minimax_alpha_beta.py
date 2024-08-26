import util

def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """Minimax algorithm with alpha-beta pruning."""
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
        return best_score

"""
def best_move_with_alpha_beta():
   Determine the best move using minimax with alpha-beta pruning.
    best_score = float('-inf')
    move = (-1, -1)
    alpha = float('-inf')
    beta = float('inf')
    
    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if util.board[row][col] == 0:
                util.board[row][col] = 2
                score = minimax_alpha_beta(util.board, 0, False, alpha, beta)
                util.board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        util.mark_square(move[0], move[1], 2)
        return True
    return False
 """
