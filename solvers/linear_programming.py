import numpy as np
from pulp import *


def linear_programming(board):
    """
    https://github.com/coin-or/pulp/blob/master/examples/Sudoku1.py
    """
    n = board.shape[0]
    sqrt_n = int(np.sqrt(n))

    # all rows, columns and values a Sudoku take values from 1 to n
    vals = range(1, n+1)
    rows = cols = range(n)

    # boxes list is created with row/column index of each sqare in each box
    boxes = [
        [(sqrt_n * i + k, sqrt_n * j + l) for k in range(sqrt_n) for l in range(sqrt_n)]
        for i in range(sqrt_n)
        for j in range(sqrt_n)
    ]

    # the problem variable is created to contain the problem data
    prob = LpProblem('SudokuProblem')

    # the decision variables are created
    choices = LpVariable.dict('Choice', (vals, rows, cols), cat='Binary')

    # we do not define an objective function since none is needed

    # a constraint ensuring only one value can be in each square is created
    for r in rows:
        for c in cols:
            prob += lpSum([choices[v][r][c] for v in vals]) == 1

    # row/column/box constraints are added for each value
    for v in vals:
        for r in rows:
            prob += lpSum([choices[v][r][c] for c in cols]) == 1

        for c in cols:
            prob += lpSum([choices[v][r][c] for r in rows]) == 1

        for b in boxes:
            prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1

    # the starting numbers are entered as constraints
    for i in range(n):
        for j in range(n):
            if board[i, j] != 0:
                prob += choices[board[i, j]][i][j] == 1

    # the problem data is written to an .lp file
    prob.writeLP('Sudoku.lp')

    # problem is solved using PuLP's choiec of solver
    prob.solve()

    # write solution to board
    for i in range(n):
        for j in range(n):
            for num in range(1, n+1):
                if value(choices[num][i][j]) == 1:
                    board[i, j] = n

    return LpStatus[prob.status]