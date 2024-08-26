import numpy as np
import util

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

def heuristic_function_1(board, row, col):
    """
    Blocking Heuristic:
    Assigns a score to the move at (row, col) based on how well it blocks the opponent from winning.
    """
    # Define the symbols for player and opponent
    opponent = 1
    player = 2
    
    # Apply symmetry reduction
    board = util.canonical_form(board)
    
    # Initialize the score
    score = 0

    # Check if the move blocks a winning opportunity for the opponent
    board[row][col] = opponent
    if is_winning_move(board, opponent):
        score += 100  # Assign a high score for blocking a winning move
    
    # Check if the move results in a win for the player
    board[row][col] = player
    if is_winning_move(board, player):
        score += 200  # Higher score for a winning move
    
    return score


def heuristic_function_2(board, row, col):
    player = 2
    board = util.canonical_form(board)
    
    # Place the player's move
    board[row][col] = 1
    if is_winning_move(board, 1):
        return 1000  # Immediate win
    
    board[row][col] = 2
    def line_weight(line, player):
        """Assign weight based on the number of player marks in the line."""
        player_count = np.sum(line == player)
        empty_count = np.sum(line == 0)
        opponent = 1 if player == 2 else 2
        opponent_count = np.sum(line == opponent)

        if opponent_count > 0:
            return 0
        
        if player_count == 2 and empty_count == 1:
            return 100
        elif player_count == 1 and empty_count == 2:
            return 10
        elif player_count == 0 and empty_count == 3:
            return 1
        else:
            return 0
    
    def get_main_diagonal(board, start_row, start_col):
        """Get the main diagonal (top-left to bottom-right)."""
        diag = []
        r, c = start_row, start_col
        while r < 3 and c < 3:
            diag.append(board[r, c])
            r += 1
            c += 1
        return np.array(diag)
    
    def get_anti_diagonal(board, start_row, start_col):
        """Get the anti-diagonal (top-right to bottom-left)."""
        diag = []
        r, c = start_row, start_col
        while r < 3 and c >= 0:
            diag.append(board[r, c])
            r += 1
            c -= 1
        return np.array(diag)

    def count_winning_lines_for_player(board, player, row, col):
        """Count and weight how many winning lines are possible for the given player."""
        winning_lines = 0

        # Check row
        row_line = board[row, :]
        winning_lines += line_weight(row_line, player)
        
        # Check column
        col_line = board[:, col]
        winning_lines += line_weight(col_line, player)
        
        # Check main diagonal (top-left to bottom-right)
        diag_main = get_main_diagonal(board, row, col)
        winning_lines += line_weight(diag_main, player)
        
        # Check anti-diagonal (top-right to bottom-left)
        diag_anti = get_anti_diagonal(board, row, col)
        winning_lines += line_weight(diag_anti, player)
        
        return winning_lines
    
    return count_winning_lines_for_player(board, player, row, col)
