import util
import numpy as np

def heuristic_function_2(board, row, col):
    player = 2
    board = util.canonical_form(board).copy()  # Apply symmetry reduction and work on a copy
    
    # Place the player's move
    board[row][col] = 1
    if util.is_winning_move(board, 1):
        return 1000  # Immediate win
    
    # Restore the board state for the player's move
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


