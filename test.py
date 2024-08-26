import numpy as np


def is_winning_move(board, player):
        # Check rows, columns, and diagonals
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
    # Initialize the score
    score = 0

    # Define the symbols for player and opponent
    
    opponent = 1

    # Function to check if the given player can win with the current board state


    # Check if the move blocks a winning opportunity for the opponent
    # Temporarily place the opponent's move in the current cell to see if it would result in a win
    board[row][col] = opponent
    if is_winning_move(board, opponent):
        score += 100  # Assign a high score for blocking a winning move
    board[row][col] = 2
    if is_winning_move(board, 2):
        score += 200
    return score


def heuristic_function_2(board, row, col):
    player = 2
    board[row][col] = 1
    if is_winning_move(board, 1):
        return 1000
    board[row][col] = 2
    def line_weight(line, player):
        """Assign weight based on the number of player marks in the line."""
        line = line.flatten() if isinstance(line, np.ndarray) else line
        player_count = np.sum(line == player)
        empty_count = np.sum(line == 0)
        opponent = 1 if player == 2 else 2
        opponent_count = np.sum(line == opponent)

        if opponent_count > 0:
            # If the line is blocked by the opponent, it doesn't count
            return 0
        
        if player_count == 2 and empty_count == 1:
            # 2 in a line and 1 empty: high weight
            return 100
        elif player_count == 1 and empty_count == 2:
            # 1 in a line and 2 empty: medium weight
            return 10
        elif player_count == 0 and empty_count == 3:
            # No player marks and 3 empty: low weight
            return 1
        else:
            # Not a winning line or blocked by opponent
            return 0
    
    def get_main_diagonal(board, start_row, start_col):
        """Get the main diagonal (top-left to bottom-right)."""
        rows, cols = board.shape
        diag = []
        r, c = start_row, start_col
        while r < rows and c < cols:
            diag.append(board[r, c])
            r += 1
            c += 1
        return np.array(diag)
    
    def get_anti_diagonal(board, start_row, start_col):
        """Get the anti-diagonal (top-right to bottom-left)."""
        rows, cols = board.shape
        diag = []
        r, c = start_row, start_col
        while r < rows and c >= 0:
            diag.append(board[r, c])
            r += 1
            c -= 1
        return np.array(diag)

    def count_winning_lines_for_player(board, player, row, col):
        """Count and weight how many winning lines are possible for the given player."""
        winning_lines = 0
        rows, cols = board.shape

        # Check row
        row_line = board[row, :]
        winning_lines += line_weight(row_line, player)
        
        # Check column
        col_line = board[:, col]
        winning_lines += line_weight(col_line, player)
        
        # Check main diagonal (top-left to bottom-right)
        start_row, start_col = row, col
        diag_main = get_main_diagonal(board, start_row, start_col)
        winning_lines += line_weight(diag_main, player)
        
        # Check anti-diagonal (top-right to bottom-left)
        start_row, start_col = row, col
        diag_anti = get_anti_diagonal(board, start_row, start_col)
        winning_lines += line_weight(diag_anti, player)
        
        return winning_lines
    
    return count_winning_lines_for_player(board, player, row, col)