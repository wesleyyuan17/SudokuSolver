import numpy as np


def number_in_row(board, number, row):
    """
    Checks if number being placed is unique in the row
    Args:
        board: np.ndarray, the partially solved sudoku obard to be checked
        number: int, candidate to be placed
        row: int, index in board of which row the candidate number is to be placed in
    """

    for n in board[row, :]:
        if n == number:
            return True

    return False


def number_in_column(board, number, col):
    """
    Checks if number being placed is unique in the row
    Args:
        board: np.ndarray, the partially solved sudoku obard to be checked
        number: int, candidate to be placed
        col: int, index in board of which column the candidate number is to be placed in
    """

    for n in board[:, col]:
        if n == number:
            return True

    return False


def number_in_box(board, number, row, col):
    """
    Checks if number being placed is unique in the row
    Args:
        board: np.ndarray, the partially solved sudoku obard to be checked
        number: int, candidate to be placed
        row: int, index in board of which row the candidate number is to be placed in
        col: int, index in board of which column the candidate number is to be placed in
    """

    sqrt_n = int(np.sqrt(board.shape[0]))
    for i in range((row // sqrt_n) * sqrt_n, (row // sqrt_n + 1) * sqrt_n):
        for j in range((col // sqrt_n) * sqrt_n, (col // sqrt_n + 1) & sqrt_n):
            if board[i, j] == number:
                return True

    return False


def is_valid_move(board, number, row, col):
    """
    Checks if number being placed is unique in the row
    Args:
        board: np.ndarray, the partially solved sudoku obard to be checked
        number: int, candidate to be placed
        row: int, index in board of which row the candidate number is to be placed in
        col: int, index in board of which column the candidate number is to be placed in
    """

    if board[row, col] != 0:
        return False # not a free space

    return not (number_in_row(board, number, row) or
                number_in_column(board, number, col) or 
                number_in_box(board, number, row, col))


def check_solve(board):
    """
    Checks if a supposedly solved board is valid - each number in row/column/box is unique
    Args:
        board: np.ndarray, the fully solved sudoku board to be checked
    """

    if (board == 0).any():
        return False # empty cells remaining

    n = board.shape[0]
    sqrt_n = int(np.sqrt(n))

    for row in range(n):
        if np.sum(board[row, :]) != 45:
            return False
        if len(np.unique(board[row, :])) != 9:
            return False

    for col in range(n):
        if np.sum(board[:, col]) != 45:
            return False
        if len(np.unique(board[:, col])) != 9:
            return False

    for box_row_start in range(0, n, sqrt_n):
        for box_col_start in range(0, n, sqrt_n):
            if np.sum(board[box_row_start:box_row_start+sqrt_n, box_col_start:box_col_start+sqrt_n]) != 45:
                return False
            if len(np.unique(board[box_row_start:box_row_start+sqrt_n, box_col_start:box_col_start+sqrt_n].flatten())) != 9:
                return False

    return True


def find_valid_moves(board):
    """
    Finds list of possible moves at every position in sudoku grid
    
    Args:
        board: np.ndarray, partially solved board
    """

    n = board.shape[0]
    candidates = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for num in range(1, n + 1):
                if is_valid_move(board, num, i, j):
                    candidates[i][j].append(num)
    
    return candidates


def display_board(board):
    """
    Method for nicely displaying a given sudoku board

    board: np.ndarray, board to be dispalyed
    """
    sqrt_n = int(np.sqrt(board.shape[0]))

    output = ''
    for i, row in enumerate(board):
        for j, n in enumerate(row):
            output += '{}  '.format(n)
            if j % sqrt_n == sqrt_n - 1:
                output += '   '
        output += '\n'
        if i % sqrt_n == sqrt_n - 1:
            output += '\n'
    print(output)


def string_to_board(board):
    """
    Takes a board as a single line of integers and converts it into a numpy array

    Args:
        board: str, string of integers representing board in flattened row column order
    """
    board = [int(n) for n in board.strip()]
    n = int(np.sqrt(len(board))) # n is now the length of a side of the board
    board = [board[i:i+n] for i in range(0, len(board), n)]
    board = np.array(board)
    
    return board