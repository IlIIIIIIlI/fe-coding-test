import torch
import torch.nn as nn
import os
import time
from pathlib import Path

current_path = Path(__file__).parent

class RWKVSolver:
    """Sudoku solver using RWKV model."""
    
    def __init__(self):
        """Initialize the RWKV model for solving Sudoku."""
        # Set environment variables
        os.environ["RWKV_JIT_ON"] = "1"
        os.environ["RWKV_CUDA_ON"] = "0"
        
        # Import RWKV after setting env vars
        from rwkv_model import RWKV
        from rwkv.utils import PIPELINE, PIPELINE_ARGS
        from rwkv.rwkv_tokenizer import TRIE_TOKENIZER
        
        # Initialize model
        model_path = current_path / "sudoku_rwkv_20241120.pth"
        self.model = RWKV(model=str(model_path), strategy="cuda fp16", verbose=False)
        self.pipeline = PIPELINE(self.model, "rwkv_vocab_v20230424")
        self.pipeline.tokenizer = TRIE_TOKENIZER(str(current_path / "sudoku_vocab.txt"))
        self.gen_args = PIPELINE_ARGS(top_k=1, alpha_frequency=0, alpha_presence=0, token_stop=[105])
        
        # Warm up model
        self.model.forward([0, 1], None)
        self.model.forward([0], None)
        
    def _format_board(self, board):
        """Format board into string representation."""
        return '\n'.join(' '.join(str(num) for num in row) + ' ' for row in board)
        
    def solve(self, matrix):
        """
        Solve a Sudoku puzzle using RWKV model.
        
        Args:
            matrix (List[List[int]]): A 9x9 matrix with 0s for empty cells
            
        Returns:
            bool: True if solved successfully, False otherwise
            matrix is modified in place with solution
        """
        # Format input
        input_str = f"<input>\n{self._format_board(matrix)}\n</input>\n\n"
        
        # Track moves and solution
        moves = []
        solved_matrix = [row[:] for row in matrix]
        
        def process_output(text):
            """Process model output text to extract moves."""
            if text.startswith("> Fill cell"):
                try:
                    # Parse move: "> Fill cell (row, col) num"
                    text = text.strip()
                    row = int(text[13])
                    col = int(text[16])
                    num = int(text[-1])
                    moves.append((row, col, num))
                    solved_matrix[row][col] = num
                except:
                    pass
        
        # Generate solution
        self.pipeline.generate(
            input_str, 
            token_count=10000000,
            args=self.gen_args,
            callback=process_output
        )
        
        # Check if solution is valid
        for row, col, num in moves:
            matrix[row][col] = num
            
        # Verify solution
        result = self._verify_solution(matrix)
        return result
    
    def _verify_solution(self, matrix):
        """Verify if solution is valid."""
        # Check all cells are filled
        if any(0 in row for row in matrix):
            return False
            
        # Check rows
        for row in matrix:
            if len(set(row)) != 9:
                return False
                
        # Check columns 
        for col in range(9):
            if len(set(matrix[row][col] for row in range(9))) != 9:
                return False
                
        # Check boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(matrix[box_row + i][box_col + j])
                if len(set(box)) != 9:
                    return False
                    
        return True

class BaseSolver:
    """Base class for Sudoku solvers."""
    
    def __init__(self):
        """Initialize solver."""
        self.size = 9
        self.box_size = 3
        
    def find_empty(self, matrix):
        """Find empty cell with minimum possibilities."""
        min_possibilities = 10
        min_pos = None
        
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i][j] == 0:
                    valid_moves = 0
                    # Count valid moves for this position
                    for num in range(1, 10):
                        if self.is_valid(matrix, num, (i, j)):
                            valid_moves += 1
                            if valid_moves >= min_possibilities:
                                break
                    if 0 < valid_moves < min_possibilities:
                        min_possibilities = valid_moves
                        min_pos = (i, j)
                        if min_possibilities == 1:  # Can't get better than 1
                            return min_pos
        return min_pos
    
    def is_valid(self, matrix, num, pos):
        """Check if number is valid in position."""
        row, col = pos
        
        # Check row
        for j in range(self.size):
            if matrix[row][j] == num and col != j:
                return False
                
        # Check column    
        for i in range(self.size):
            if matrix[i][col] == num and row != i:
                return False
                
        # Check box
        box_x = (row // self.box_size) * self.box_size
        box_y = (col // self.box_size) * self.box_size
        
        for i in range(box_x, box_x + self.box_size):
            for j in range(box_y, box_y + self.box_size):
                if matrix[i][j] == num and (i,j) != (row,col):
                    return False
                    
        return True

class DFSSolver(BaseSolver):
    """DFS-based Sudoku solver with MRV heuristic."""
    
    def __init__(self):
        """Initialize DFS solver."""
        super().__init__()
        self.attempts = 0
        self.solve_time = 0
        
    def solve(self, matrix):
        """
        Solve Sudoku using DFS with MRV heuristic.
        
        Args:
            matrix (List[List[int]]): 9x9 Sudoku board
            
        Returns: 
            bool: True if solved, False otherwise
            Matrix is modified in place
        """
        start_time = time.time()
        self.attempts = 0
        result = self._solve_dfs(matrix)
        self.solve_time = time.time() - start_time
        return result
    
    def _solve_dfs(self, matrix):
        """DFS implementation with MRV heuristic."""
        self.attempts += 1
        
        # Find empty cell with minimum remaining values
        pos = self.find_empty(matrix)
        if not pos:
            return True
            
        row, col = pos
        for num in range(1, self.size + 1):
            if self.is_valid(matrix, num, (row, col)):
                matrix[row][col] = num
                
                if self._solve_dfs(matrix):
                    return True
                    
                matrix[row][col] = 0
                
        return False
        
    def get_stats(self):
        """Get solving statistics."""
        return {
            'attempts': self.attempts,
            'time': self.solve_time
        }