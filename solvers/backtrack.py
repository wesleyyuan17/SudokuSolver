from solvers.util import is_valid_move


def backtrack(board, candidates=None):
    """
    Solves given sudoku board by backtracking. The general steps are as follows

        1. Find an unfilled space
        2. Try lowest valid number between 1 and n
        3. Recursively call solve given the new placement (DFS)
            a. if all spaces filled then return True
            b. otherwise reset previously placed number and try next number
        4. If tried every number and space is still blank then board is not solvable
        5. If no empty spaces on baord then board is solved

    Args:
        board: np.ndarray, unsolved board to be solved
        candidates: list[list[list[int]]], possible values at each location on board
    """

    n = board.shape[0]
    for i in range(n):
        for j in range(n):
            if board[i, j] != 0:
                continue # already filled space

            if candidates is not None:
                try_nums = candidates[i][j]
            else:
                try_nums = range(1, n+1)
            
            for number in try_nums:
                if is_valid_move(board, number, i ,j):
                    board[i, j] = number
                    if backtrack(board, candidates):
                        return True
                    else:
                        board[i, j] = 0
            if board[i, j] == 0:
                return False
    return True