import util
import numpy

def minimax_heuristic_advanced(board):
    """Evaluate the board state using an advanced heuristic."""
    score = 0
    for i in range(util.BOARD_ROWS):
        row = board[i]
        col = [board[j][i] for j in range(util.BOARD_COLUMNS)]
        score += evaluate_line_advanced(row, 2)
        score -= evaluate_line_advanced(row, 1)
        score += evaluate_line_advanced(col, 2)
        score -= evaluate_line_advanced(col, 1)

    diag1 = [board[i][i] for i in range(util.BOARD_ROWS)]
    diag2 = [board[i][util.BOARD_COLUMNS - 1 - i] for i in range(util.BOARD_ROWS)]
    
    score += evaluate_line_advanced(diag1, 2)
    score -= evaluate_line_advanced(diag1, 1)
    score += evaluate_line_advanced(diag2, 2)
    score -= evaluate_line_advanced(diag2, 1)
    
    return score

def evaluate_line_advanced(line, player):
    """Evaluate a line for the advanced heuristic."""
    opponent = 2 if player == 1 else 1
    
    # Convert line to a numpy array if it's not already
    line = numpy.array(line)
    
    player_count = numpy.sum(line == player)
    opponent_count = numpy.sum(line == opponent)
    empty_count = numpy.sum(line == 0)
    score = 0
    
    if player_count == 2 and empty_count == 1:
        score += 20
    elif player_count == 1 and empty_count == 2:
        score += 5
        
    if opponent_count == 2 and empty_count == 1:
        score -= 20
    elif opponent_count == 1 and empty_count == 2:
        score -= 5

    return score


"""
def best_move_heuristic_advanced():
    Determine the best move using an advanced heuristic.
    best_score = float('-inf')
    move = (-1, -1)
    
    for row in range(util.BOARD_ROWS):
        for col in range(util.BOARD_COLUMNS):
            if util.board[row][col] == 0:
                util.board[row][col] = 2
                score = minimax_heuristic_advanced(util.board)
                util.board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        util.mark_square(move[0], move[1], 2)
        return True
    return False

"""



















