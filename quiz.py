#!/usr/bin/env python3
import sys
from typing import List
from sudoku.solver import SudokuSolver

def solve_sudoku(matrix: List[List[int]]) -> bool:
    """
    Solve a 9x9 Sudoku board.
    
    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.

    Args:
        matrix (List[List[int]]): A 9x9 matrix representing the Sudoku board, 
                                where 0 represents empty cells.
    Returns:
        bool: True if solved successfully, False otherwise.
              The input matrix is modified in place with the solution.
    """
    solver = SudokuSolver(matrix)
    return solver.solve()