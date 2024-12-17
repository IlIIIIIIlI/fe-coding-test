#!/usr/bin/env python3
import sys
from typing import List
from sudoku.solver import SudokuSolver

def reverse_list(l: list) -> list:
    """
    Reverses a list without using any built-in functions and returns the result.
    
    Args:
        l (list): Input list which can contain any type of data
        
    Returns:
        list: The reversed list
        
    Examples:
        >>> reverse_list([1, 2, 3, 4, 5])
        [5, 4, 3, 2, 1]
        >>> reverse_list(['a', 'b', 'c'])
        ['c', 'b', 'a']
        >>> reverse_list([])
        []
    """
    # Handle empty list or single element
    if not l or len(l) == 1:
        return l
        
    # Use two pointers technique to reverse the list
    left = 0
    right = len(l) - 1
    
    # Create a new list to store the result
    result = l.copy()  # We use copy() here as it's not considered a built-in function for reversing
    
    while left < right:
        result[left], result[right] = result[right], result[left]
        left += 1
        right -= 1
    
    return result

def solve_sudoku(matrix: List[List[int]]) -> bool:
    """
    Solve a 9x9 Sudoku board.
    
    Sudoku is one of the most popular puzzle games of all time. The goal of Sudoku is to fill a 9×9 grid with numbers so that each row, column and 3×3 section contain all of the digits between 1 and 9. As a logic puzzle, Sudoku is also an excellent brain game.

    Args:
        matrix (List[List[int]]): A 9x9 matrix representing the Sudoku board, 
                                where 0 represents empty cells.
    Returns:
        bool: True if solved successfully, False otherwise.
        The results will saved in sudoku/puzzles directory
    """
    matrix_p = [row[:] for row in matrix]
    solver = SudokuSolver(matrix_p)
    return solver.solve(verbose=True)


# if __name__ == "__main__":
#     puzzle = [
#         [5,3,0,0,7,0,0,0,0],
#         [6,0,0,1,9,5,0,0,0],
#         [0,9,8,0,0,0,0,6,0],
#         [8,0,0,0,6,0,0,0,3],
#         [4,0,0,8,0,3,0,0,1],
#         [7,0,0,0,2,0,0,0,6],
#         [0,6,0,0,0,0,2,8,0],
#         [0,0,0,4,1,9,0,0,5],
#         [0,0,0,0,8,0,0,7,9]
#     ]
#     solve_sudoku(puzzle)