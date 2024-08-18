import util

def minimax(board, depth, is_maximizing):
    """Minimax algorithm."""
    if util.check_win(2):
        return float('inf')
    if util.check_win(1):
        return float('-inf')
    if util.is_board_full():
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
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
    return best_score


def best_move():
    """Determine the best move using minimax."""
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if util.board[row][col] == 0:
                util.board[row][col] = 2
                score = minimax(util.board, 0, False)
                util.board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        util.mark_square(move[0], move[1], 2)
        return True
    return False

