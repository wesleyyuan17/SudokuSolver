import string
import numpy as np
import argparse

from solvers import *
from solvers.util import display_board, find_valid_moves, string_to_board, check_solve


SOLVE_METHODS_IMPLEMENTED = ['backtrack', 'backtrack_with_markup', 'candidate_place_checking', 'linear_programming']


def solve(method, board):
    """
    Wrapper for handling the solving for a given board - calls an implementation of solve given method

    Args:
        method: str, name of implmeented method of solving
        board: np.ndarray, the unsolved board to be solved
    """

    assert method in SOLVE_METHODS_IMPLEMENTED, 'Unknown solve method: {}. Must be in {}'.format(method, SOLVE_METHODS_IMPLEMENTED)

    if method == 'backtrack':
        return backtrack(board)
    elif method == 'backtrack_with_markup':
        candidates = find_valid_moves(board)
        return backtrack(board, candidates)
    elif method == 'candidate_place_checking':
        return candidate_place_checking(board)
    elif method == 'linear_programming':
        return linear_programming(board)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--boards', dest='boards', requred=True,
                        help='Name of file containing Sudoku board(s) to be solved, must be in one-line string format')
    parser.add_argument('--method', dest='method', required=False, default='backtrack',
                        help='Method to use to solve Sudoku board')
    parser.add_argument('--display', dest='display', required=False, default=False,
                        help='Whether program should display the solved boards or not')
    args = parser.parse_args()

    boards = []
    with open(args.boards, 'r') as f:
        for line in f:
            boards.append(string_to_board(line))

    for board in boards:
        assert solve(board), 'Board is unsolvable'
        assert check_solve(board), 'Invalid solve for board'

        if args.display:
            display_board(board)