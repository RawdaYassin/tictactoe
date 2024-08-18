import util
import numpy

def minimax_heuristic_basic(board):
    """Evaluate the board state using a basic heuristic."""
    score = 0
    for i in range(util.BOARD_ROWS):
        row = board[i]
        col = [board[j][i] for j in range(util.BOARD_COLUMNS)]
        score += evaluate_line(row)
        score += evaluate_line(col)

    diag1 = [board[i][i] for i in range(util.BOARD_ROWS)]
    diag2 = [board[i][util.BOARD_COLUMNS - 1 - i] for i in range(util.BOARD_ROWS)]
    score += evaluate_line(diag1)
    score += evaluate_line(diag2)

    return score


def evaluate_line(line):
    """Evaluate a line for the heuristic."""
    if numpy.sum(line == 2) == 3:
        return 10
    elif numpy.sum(line == 1) == 3:
        return -10
    elif numpy.sum(line == 2) == 2 and numpy.sum(line == 0) == 1:
        return 5
    elif numpy.sum(line == 1) == 2 and numpy.sum(line == 0) == 1:
        return -5
    return 0


def best_move_heuristic_basic():
    """Determine the best move using a basic heuristic."""
    best_score = float('-inf')
    move = (-1, -1)

    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if util.board[row][col] == 0:
                util.board[row][col] = 2
                score = minimax_heuristic_basic(util.board)
                util.board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        util.mark_square(move[0], move[1], 2)
        return True
    return False


