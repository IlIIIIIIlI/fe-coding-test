import random
import time
from typing import List, Tuple, Optional
from copy import deepcopy
from .solver import SudokuSolver

class SudokuGenerator:
    """Generate random Sudoku puzzles with varying difficulty."""
    
    # Arto Inkala's puzzles (kept as reference for difficulty benchmarking)
    INKALA_2006 = [
        [0, 0, 5, 3, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 7, 0, 0, 1, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 5, 3, 0, 0],
        [0, 1, 0, 0, 7, 0, 0, 0, 6],
        [0, 0, 3, 2, 0, 0, 0, 8, 0],
        [0, 6, 0, 5, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 9, 7, 0, 0]
    ]

    INKALA_2010 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ]

    @staticmethod
    def has_unique_solution(puzzle: List[List[int]], time_limit: float = 0.1) -> bool:
        """Check if puzzle has exactly one solution within time limit."""
        start_time = time.time()
        
        # First solution
        board_copy = [row[:] for row in puzzle]
        solver = SudokuSolver(board_copy)
        if not solver.solve():
            return False
            
        # Quick check for second solution
        board_copy = [row[:] for row in puzzle]
        solver = SudokuSolver(board_copy)
        
        def find_empty() -> Optional[Tuple[int, int]]:
            """Find an empty cell."""
            for i in range(9):
                for j in range(9):
                    if board_copy[i][j] == 0:
                        return (i, j)
            return None
        
        # Use stack instead of recursion
        stack = []
        empty = find_empty()
        if empty:
            row, col = empty
            for num in range(1, 10):
                if solver.is_valid(num, (row, col)):
                    stack.append((row, col, num, 1))  # 1 means first try
        
        while stack:
            if time.time() - start_time > time_limit:
                return False
                
            row, col, num, state = stack.pop()
            
            if state == 1:  # First try of this number
                board_copy[row][col] = num
                empty = find_empty()
                
                if not empty:  # Found second solution
                    return False
                    
                next_row, next_col = empty if empty else (-1, -1)
                # Push backtrack state
                stack.append((row, col, num, 2))  # 2 means need to backtrack
                
                # Push next empty cell possibilities
                if empty:
                    for next_num in range(1, 10):
                        if solver.is_valid(next_num, (next_row, next_col)):
                            stack.append((next_row, next_col, next_num, 1))
                            
            else:  # Backtrack
                board_copy[row][col] = 0
                
        return True

    @staticmethod
    def _generate_solved_board() -> Optional[List[List[int]]]:
        """Generate a completely solved Sudoku board."""
        def fill_diagonal_boxes():
            for i in range(0, 9, 3):
                nums = list(range(1, 10))
                random.shuffle(nums)
                for r in range(3):
                    for c in range(3):
                        board[i + r][i + c] = nums[r * 3 + c]

        board = [[0] * 9 for _ in range(9)]
        fill_diagonal_boxes()  # Fill diagonal 3x3 boxes (independent)
        
        solver = SudokuSolver(board)
        if solver.solve():
            return solver.board
        return None

    @staticmethod
    def generate_puzzle(difficulty: float = 0.5, timeout: float = 15.0) -> Tuple[List[List[int]], List[List[int]]]:
        """Generate a random solvable Sudoku puzzle."""
        start_time = time.time()
        
        # Generate initial solved board
        solution = SudokuGenerator._generate_solved_board()
        if not solution:
            return None, None
            
        # Define number of cells to remove based on difficulty
        holes = {
            0.3: 30,  # easy - remove 30 numbers
            0.5: 40,  # medium - remove 40 numbers
            0.7: 50,  # hard - remove 50 numbers
            0.9: 55   # extreme - remove 55 numbers
        }.get(difficulty, 40)
        
        # Create empty board
        puzzle = [row[:] for row in solution]
        
        # Get positions of cells we can try to remove
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        # Remove numbers until we reach our target or run out of cells
        removed = 0
        for i, j in cells:
            if removed >= holes:
                break
            
            # Remember current value
            temp = puzzle[i][j]
            puzzle[i][j] = 0
            
            # Check if puzzle is still valid with this number removed
            board_copy = [row[:] for row in puzzle]
            solver = SudokuSolver(board_copy)
            
            if solver.solve():
                # Verify this is still the only solution
                board_copy = [row[:] for row in puzzle]
                solver2 = SudokuSolver(board_copy)
                if solver2.solve():
                    removed += 1
                    continue
            
            # If we get here, removing this number created problems
            puzzle[i][j] = temp
            
        return puzzle, solution