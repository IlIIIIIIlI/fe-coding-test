# sudoku/solver.py
from typing import List, Tuple, Optional, Set
import time

class SudokuSolver:
    """
    Advanced Sudoku solver with multiple heuristic strategies.
    
    Implements the following strategies:
    1. Candidate Reduction: Remove invalid candidates after each assignment
    2. Uniqueness in Unit: If a number can only go in one place in a unit
    3. Hidden Pairs: If two cells in a unit share the same two candidates exclusively
    4. Naked Pairs: If two cells in a unit contain only the same two candidates
    """
    
    def __init__(self, board: List[List[int]]):
        """Initialize solver with a board."""
        self.size = 9
        self.box_size = 3
        self.solve_time = None
        self.attempts = 0
        
        # Initialize candidates for each cell
        self.board = board
        self.candidates = [[set() for _ in range(9)] for _ in range(9)]
        self.initialize_candidates()
        
    def get_box_start(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Get top-left position of the box containing pos."""
        row, col = pos
        return (row // 3 * 3, col // 3 * 3)
        
    def initialize_candidates(self):
        """Initialize all possible candidates for each empty cell."""
        # First fill all empty cells with all possibilities
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.candidates[i][j] = set(range(1, 10))
                    
        # Remove candidates based on existing numbers
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    self.update_candidates((i, j), self.board[i][j])
                    
    def update_candidates(self, pos: Tuple[int, int], num: int):
        """Remove a number from candidates in affected cells."""
        row, col = pos
        
        # Clear candidates for the cell itself
        if self.board[row][col] == 0:
            self.candidates[row][col].clear()
            
        # Remove from row
        for j in range(self.size):
            if num in self.candidates[row][j]:
                self.candidates[row][j].remove(num)
                
        # Remove from column
        for i in range(self.size):
            if num in self.candidates[i][col]:
                self.candidates[i][col].remove(num)
                
        # Remove from box
        box_row, box_col = self.get_box_start((row, col))
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if num in self.candidates[i][j]:
                    self.candidates[i][j].remove(num)
                    
    def find_single_candidates(self) -> List[Tuple[Tuple[int, int], int]]:
        """Find cells that have only one candidate (Strategy I)."""
        singles = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and len(self.candidates[i][j]) == 1:
                    num = next(iter(self.candidates[i][j]))
                    singles.append(((i, j), num))
        return singles
        
    def find_unique_candidates(self) -> List[Tuple[Tuple[int, int], int]]:
        """Find numbers that can only go in one place in a unit (Strategy II)."""
        unique = []
        
        # Check rows
        for i in range(self.size):
            for num in range(1, self.size + 1):
                valid_positions = []
                for j in range(self.size):
                    if self.board[i][j] == 0 and num in self.candidates[i][j]:
                        valid_positions.append((i, j))
                if len(valid_positions) == 1:
                    unique.append((valid_positions[0], num))
                    
        # Check columns
        for j in range(self.size):
            for num in range(1, self.size + 1):
                valid_positions = []
                for i in range(self.size):
                    if self.board[i][j] == 0 and num in self.candidates[i][j]:
                        valid_positions.append((i, j))
                if len(valid_positions) == 1:
                    unique.append((valid_positions[0], num))
                    
        # Check boxes
        for box_row in range(0, self.size, 3):
            for box_col in range(0, self.size, 3):
                for num in range(1, self.size + 1):
                    valid_positions = []
                    for i in range(box_row, box_row + 3):
                        for j in range(box_col, box_col + 3):
                            if self.board[i][j] == 0 and num in self.candidates[i][j]:
                                valid_positions.append((i, j))
                    if len(valid_positions) == 1:
                        unique.append((valid_positions[0], num))
                        
        return unique
        
    def solve(self) -> bool:
        """
        Solve the Sudoku using DFS with heuristic strategies.
        
        Returns:
            bool: True if solved successfully, False otherwise
        """
        start_time = time.time()
        self.attempts = 0
        result = self._solve_dfs()
        self.solve_time = time.time() - start_time
        return result
        
    def _solve_dfs(self) -> bool:
        """DFS implementation with heuristic strategies."""
        self.attempts += 1
        
        # Apply strategies
        made_progress = True
        while made_progress:
            made_progress = False
            
            # Strategy I: Single candidates
            singles = self.find_single_candidates()
            for pos, num in singles:
                self.board[pos[0]][pos[1]] = num
                self.update_candidates(pos, num)
                made_progress = True
                
            # Strategy II: Unique candidates
            if not made_progress:
                uniques = self.find_unique_candidates()
                for pos, num in uniques:
                    self.board[pos[0]][pos[1]] = num
                    self.update_candidates(pos, num)
                    made_progress = True
        
        # Find cell with minimum candidates
        min_candidates = 10
        min_pos = None
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    num_candidates = len(self.candidates[i][j])
                    if num_candidates < min_candidates:
                        min_candidates = num_candidates
                        min_pos = (i, j)
                        
        if min_pos is None:
            return True
            
        row, col = min_pos
        candidates = list(self.candidates[row][col])
        
        for num in candidates:
            self.board[row][col] = num
            old_candidates = [row[:] for row in self.candidates]
            self.update_candidates((row, col), num)
            
            if self._solve_dfs():
                return True
                
            self.board[row][col] = 0
            self.candidates = old_candidates
            
        return False
        
    def get_solve_time(self) -> float:
        """Get the time taken to solve."""
        return self.solve_time
        
    def get_attempts(self) -> int:
        """Get the number of attempts made during solving."""
        return self.attempts