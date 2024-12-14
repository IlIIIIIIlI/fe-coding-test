# sudoku/solver.py
from typing import List, Tuple, Optional, Set
import time

class SudokuSolver:
    """
    Enhanced Sudoku solver combining DFS with optional heuristic strategies.
    Falls back to pure DFS if heuristics fail.
    """
    
    def __init__(self, board: List[List[int]]):
        self.size = 9
        self.box_size = 3
        self.solve_time = None
        self.attempts = 0
        self.board = [row[:] for row in board]  # Create a copy to preserve original
        self.candidates = None
        
    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """Check if number is valid in given position."""
        row, col = pos
        
        # Check row
        for x in range(self.size):
            if self.board[row][x] == num and col != x:
                return False
            
        # Check column
        for x in range(self.size):
            if self.board[x][col] == num and row != x:
                return False
            
        # Check box
        box_x = (row // self.box_size) * self.box_size
        box_y = (col // self.box_size) * self.box_size
        
        for i in range(box_x, box_x + self.box_size):
            for j in range(box_y, box_y + self.box_size):
                if self.board[i][j] == num and (i,j) != (row,col):
                    return False
                
        return True
    
    def initialize_candidates(self) -> bool:
        """Initialize candidate lists for all empty cells."""
        self.candidates = [[set() for _ in range(9)] for _ in range(9)]
        
        # Fill initial candidates
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    candidates = set()
                    for num in range(1, 10):
                        if self.is_valid(num, (i, j)):
                            candidates.add(num)
                    if not candidates:  # If no valid candidates, puzzle is unsolvable
                        return False
                    self.candidates[i][j] = candidates
        return True
    
    def find_best_empty(self) -> Optional[Tuple[int, int]]:
        """Find empty cell with fewest candidates."""
        min_candidates = 10
        best_pos = None
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    valid_moves = 0
                    # Count valid moves for this position
                    for num in range(1, 10):
                        if self.is_valid(num, (i, j)):
                            valid_moves += 1
                            if valid_moves >= min_candidates:
                                break
                    if 0 < valid_moves < min_candidates:
                        min_candidates = valid_moves
                        best_pos = (i, j)
                        if min_candidates == 1:  # Can't get better than 1
                            return best_pos
        return best_pos
    
    def _solve_heuristic(self) -> bool:
        """Try to solve using heuristic strategies."""
        if not self.initialize_candidates():
            return False
            
        try:
            while True:
                progress = False
                
                # Look for cells with single candidate
                for i in range(self.size):
                    for j in range(self.size):
                        if self.board[i][j] == 0 and len(self.candidates[i][j]) == 1:
                            num = next(iter(self.candidates[i][j]))
                            if self.is_valid(num, (i, j)):
                                self.board[i][j] = num
                                progress = True
                                
                if not progress:
                    # Look for unique candidates in units
                    for unit_type in ['row', 'col', 'box']:
                        for unit_idx in range(self.size):
                            # Get positions in this unit
                            if unit_type == 'row':
                                positions = [(unit_idx, j) for j in range(self.size)]
                            elif unit_type == 'col':
                                positions = [(i, unit_idx) for i in range(self.size)]
                            else:  # box
                                box_row, box_col = (unit_idx // 3) * 3, (unit_idx % 3) * 3
                                positions = [(box_row + i, box_col + j) 
                                           for i in range(3) for j in range(3)]
                                           
                            # Check each number
                            for num in range(1, 10):
                                valid_pos = []
                                for pos in positions:
                                    if (self.board[pos[0]][pos[1]] == 0 and 
                                        num in self.candidates[pos[0]][pos[1]]):
                                        valid_pos.append(pos)
                                if len(valid_pos) == 1:
                                    i, j = valid_pos[0]
                                    if self.is_valid(num, (i, j)):
                                        self.board[i][j] = num
                                        progress = True
                
                if not progress:
                    break
                    
            return self._solve_dfs()  # Continue with DFS if no more progress
            
        except Exception:
            return False  # If any error occurs, fall back to pure DFS
    
    def _solve_dfs(self) -> bool:
        """Pure DFS implementation."""
        self.attempts += 1
        
        empty = self.find_best_empty()
        if not empty:
            return True
            
        row, col = empty
        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                
                if self._solve_dfs():
                    return True
                    
                self.board[row][col] = 0
                
        return False
    
    def solve(self) -> bool:
        """
        Solve the Sudoku using hybrid approach.
        First tries heuristic approach, falls back to pure DFS if needed.
        """
        start_time = time.time()
        self.attempts = 0
        
        # Try heuristic first
        board_copy = [row[:] for row in self.board]
        if self._solve_heuristic():
            self.solve_time = time.time() - start_time
            return True
            
        # If heuristic fails, restore board and try pure DFS
        self.board = board_copy
        self.candidates = None
        result = self._solve_dfs()
        
        self.solve_time = time.time() - start_time
        return result
    
    def get_solve_time(self) -> float:
        """Get the time taken to solve."""
        return self.solve_time
        
    def get_attempts(self) -> int:
        """Get the number of attempts made during solving."""
        return self.attempts