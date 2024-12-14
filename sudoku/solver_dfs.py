# sudoku/solver.py
from typing import List, Tuple, Optional
import time

class SudokuSolver:
    """
    DFS-based Sudoku solver implementation.
    
    Time Complexity: O(9^(n*n)) worst case, where n is board size
    
    Space Complexity: O(n*n) for the recursion stack
    """
    
    def __init__(self, board: List[List[int]]):
        """
        Initialize solver with a board.
        
        Args:
            board: 9x9 matrix with values 0-9 (0 for empty cells)
        Raises:
            ValueError: If board dimensions or values are invalid
        """
        # Initialize class attributes first
        self.size = 9
        self.box_size = 3
        self.solve_time = None
        self.attempts = 0
        
        # Validate input after attributes are initialized
        self.validate_input(board)
        self.board = board
        
    def validate_input(self, board: List[List[int]]) -> None:
        """Validate input board format and values."""
        # Check dimensions
        if len(board) != self.size or any(len(row) != self.size for row in board):
            raise ValueError(f"Input board must be {self.size}x{self.size}")
            
        # Check values
        for row in board:
            if not all(isinstance(x, int) and 0 <= x <= self.size for x in row):
                raise ValueError(f"Board values must be integers from 0 to {self.size}")
                
        # Optionally check if initial board is valid
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != 0:
                    temp = board[i][j]
                    board[i][j] = 0
                    if not self.is_valid(temp, (i, j), board):  # Pass board as parameter
                        board[i][j] = temp
                        raise ValueError("Initial board configuration is invalid")
                    board[i][j] = temp

    def is_valid(self, num: int, pos: Tuple[int, int], board: Optional[List[List[int]]] = None) -> bool:
        """
        Check if number is valid in given position.
        
        Args:
            num: Number to check
            pos: Position tuple (row, col)
            board: Optional board to check against (uses self.board if None)
        """
        current_board = board if board is not None else self.board
        row, col = pos
        
        # Check row
        for x in range(self.size):
            if current_board[row][x] == num and col != x:
                return False
            
        # Check column
        for x in range(self.size):
            if current_board[x][col] == num and row != x:
                return False
            
        # Check box
        box_x = (row // self.box_size) * self.box_size
        box_y = (col // self.box_size) * self.box_size
        
        for i in range(box_x, box_x + self.box_size):
            for j in range(box_y, box_y + self.box_size):
                if current_board[i][j] == num and (i,j) != (row,col):
                    return False
                
        return True
        
    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Find an empty cell in the board."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve(self) -> bool:
        """
        Solve the Sudoku using DFS.
        
        Returns:
            bool: True if solved successfully, False otherwise
        """
        start_time = time.time()
        self.attempts = 0  # Reset attempt counter
        result = self._solve_dfs()
        self.solve_time = time.time() - start_time
        return result
        
    def _solve_dfs(self) -> bool:
        """DFS implementation for solving Sudoku."""
        self.attempts += 1  # Increment attempt counter
        
        empty = self.find_empty()
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
    
    def get_solve_time(self) -> float:
        """Get the time taken to solve."""
        return self.solve_time
        
    def get_attempts(self) -> int:
        """Get the number of attempts made during solving."""
        return self.attempts