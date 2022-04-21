import numpy as np

from solvers.util import find_valid_moves, is_valid_move
from solvers import backtrack


def candidate_checking(board, candidates):
    """
    Helper function for candidate_place_checking algorithm - does candidate checking

    Args:
        board: np.ndarray, unsolved board to be solved
        candidates: list[list[list[int]]], possible values at each location on board
    """

    n = board.shape[0]

    n_placed = 0
    for i in range(n):
        for j in range(n):
            if board[i, j] != 0:
                continue # already placed

            if len(candidates[i][j]) == 1:
                # singleton, straight assign
                board[i, j] = candidates[i][j][0]
                candidates[i][j] = [] # no need for candidates
                n_placed += 1
            else:
                # see if any candidates are stale and are no longer avlid
                still_valid_candidates = []
                for num in candidates[i][j]:
                    if is_valid_move(board, num, i, j):
                        still_valid_candidates.append(num)
                candidates[i][j] = still_valid_candidates

    return candidates, n_placed


def place_checking(board, candidates):
    """
    Helper function for candidate_place_checking algorithm - does candidate checking

    Args:
        board: np.ndarray, unsolved board to be solved
        candidates: list[list[list[int]]], possible values at each location on board
    """

    n = board.shape[0]
    sqrt_n = int(np.sqrt(n))
    n_placed = 0

    # check rows
    for i in range(n):
        missing = [num for num in range(1, n+1) if num not in board[i, :]]
        for num in missing:
            possible_idx = []
            for j in range(n):
                if num in candidates[i][j]:
                    possible_idx.append(j)
            if len(possible_idx) == 1:
                # singelton placement - directly assign
                board[i, possible_idx[0]] = num
                candidates[i][possible_idx[0]] = []
                n_placed += 1

    # check columns
    for j in range(n):
        missing = [num  for num in range(1, n+1) if num not in board[:, j]]
        for num in missing:
            possible_idx = []
            for i in range(n):
                if num in candidates[i][j]:
                    possible_idx.append(i)
            if len(possible_idx) == 1:
                # singleton placement - directly assign
                board[possible_idx[0], j] = num
                candidates[possible_idx[0]][j] = []
                n_placed += 1

    # check boxes
    for box_row_start in range(0, n, sqrt_n):
        for box_col_start in range(0, n, sqrt_n):
            missing = [num for num in range(1, n+1) if num not in board[box_row_start:box_row_start+sqrt_n, box_col_start:box_col_start+sqrt_n].flatten()]
            for num in missing:
                possible_idx = []
                for i in range(box_row_start, box_row_start + sqrt_n):
                    for j in range(box_col_start, box_col_start + sqrt_n):
                        if num in candidates[i][j]:
                            possible_idx.append((i, j))
                if len(possible_idx) == 1:
                    # singleton placement - directly assign
                    board[possible_idx[0][0], possible_idx[0][1]] = num
                    candidates[possible_idx[0][0]][possible_idx[0][1]] = []
                    n_placed += 1

    return candidates, n_placed


def candidate_place_checking(board):
    """
    Method for solving sudoku puzzle by alternatively checking if there are singleton candidates (only one possible place for a square)
    or singleton placement (only one possible place for a number in a row/column/box)

    Args:
        board: np.ndarray, unsolved board to be solved
    """
    candidates = find_valid_moves(board)
    check_candidate = True # toggled on/off to switch b/w candidate and place checking
    n_placed = 1 # initially set to start while-loop, then to check if porgress is made
    while n_placed > 0:
        if check_candidate:
            candidates, n_placed = candidate_checking(board, candidates)
        else:
            candidates, n_placed = place_checking(board, candidates)
        check_candidate = not check_candidate

    if (board == 0).any():
        # counldn't fully solve via above - finish with backtracking
        return backtrack(board, candidates)

    return True