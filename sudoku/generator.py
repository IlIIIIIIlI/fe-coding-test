# sudoku/generator.py
import random
from typing import List, Tuple
from .solver import SudokuSolver

class SudokuGenerator:
    """Generate random Sudoku puzzles with varying difficulty."""
    
    # Arto Inkala's 2006 puzzle, considered one of the hardest
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
    
    @staticmethod
    def generate_puzzle(difficulty: float = 0.5) -> List[List[int]]:
        """
        Generate a random solvable Sudoku puzzle.
        
        Args:
            difficulty (float): Value between 0.0 and 1.0
                              0.0 = Easiest (most filled)
                              1.0 = Hardest (least filled)
        """
        # Calculate number of cells to remove based on difficulty
        # Min clues = 17, Max empty = 81-17 = 64
        max_to_remove = 64
        cells_to_remove = int(difficulty * max_to_remove)
        
        # Start with a solved board
        board = SudokuGenerator._generate_solved_board()
        
        # Create a copy for removing numbers
        puzzle = [row[:] for row in board]
        
        # Get all cell positions
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        removed = 0
        for pos in positions:
            if removed >= cells_to_remove:
                break
                
            row, col = pos
            temp = puzzle[row][col]
            puzzle[row][col] = 0
            
            # Check if still has unique solution
            board_copy = [row[:] for row in puzzle]
            solver = SudokuSolver(board_copy)
            
            if solver.solve():
                removed += 1
            else:
                puzzle[row][col] = temp
                
        return puzzle
    
    @staticmethod
    def _generate_solved_board() -> List[List[int]]:
        """Generate a completely solved Sudoku board."""
        board = [[0] * 9 for _ in range(9)]
        solver = SudokuSolver(board)
        
        # Fill diagonal boxes first (they're independent)
        for i in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    board[i + r][i + c] = nums[r * 3 + c]
        
        # Solve the rest
        solver.solve()
        return board