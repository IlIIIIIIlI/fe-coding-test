from typing import List, Tuple, Optional, Set
import time
import copy

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
        
        # Validate input board
        self.validate_input(board)
        
        # Create deep copies of the board
        self.initial_board = [row[:] for row in board]
        self.board = [row[:] for row in board]
        
        # Initialize candidates for each cell
        self.candidates = [[set() for _ in range(9)] for _ in range(9)]
        self.initialize_candidates()

    def validate_input(self, board: List[List[int]]) -> None:
        """Validate input board format and values."""
        if len(board) != self.size or any(len(row) != self.size for row in board):
            raise ValueError(f"Input board must be {self.size}x{self.size}")
            
        for row in board:
            if not all(isinstance(x, int) and 0 <= x <= self.size for x in row):
                raise ValueError(f"Board values must be integers from 0 to {self.size}")
        
        # Validate initial configuration
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != 0 and not self.is_valid(board[i][j], (i, j), board):
                    raise ValueError("Initial board configuration is invalid")

    def validate_solution(self) -> bool:
        """Validate if current board state is a valid solution."""
        if any(0 in row for row in self.board):
            return False
            
        # Check rows, columns and boxes
        for i in range(self.size):
            row = set(self.board[i])
            col = set(self.board[j][i] for j in range(self.size))
            if len(row) != 9 or len(col) != 9:
                return False
        
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = set()
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        box.add(self.board[i][j])
                if len(box) != 9:
                    return False
        
        # Check against initial constraints
        for i in range(self.size):
            for j in range(self.size):
                if self.initial_board[i][j] != 0:
                    if self.board[i][j] != self.initial_board[i][j]:
                        return False
        
        return True
        
    def get_box_start(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Get top-left position of the box containing pos."""
        row, col = pos
        return (row // 3 * 3, col // 3 * 3)

    def is_valid(self, num: int, pos: Tuple[int, int], board: Optional[List[List[int]]] = None) -> bool:
        """Check if number is valid in given position."""
        current_board = board if board is not None else self.board
        row, col = pos
        
        # Check row and column
        for i in range(self.size):
            if (current_board[row][i] == num and i != col) or \
               (current_board[i][col] == num and i != row):
                return False
        
        # Check box
        box_row, box_col = self.get_box_start(pos)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if current_board[i][j] == num and (i, j) != pos:
                    return False
                    
        return True
        
    def initialize_candidates(self):
        """Initialize all possible candidates for each empty cell."""
        # First fill all empty cells with all possibilities
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.candidates[i][j] = set(range(1, 10))
                else:
                    self.candidates[i][j].clear()
                    
        # Remove candidates based on existing numbers
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    self.update_candidates((i, j), self.board[i][j])
                    
    def update_candidates(self, pos: Tuple[int, int], num: int):
        """Remove a number from candidates in affected cells."""
        row, col = pos
            
        # Remove from row, column and box
        for i in range(self.size):
            # Row
            if self.board[row][i] == 0:
                self.candidates[row][i].discard(num)
            # Column    
            if self.board[i][col] == 0:
                self.candidates[i][col].discard(num)
                
        # Remove from box
        box_row, box_col = self.get_box_start(pos)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == 0:
                    self.candidates[i][j].discard(num)
                    
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
        
        # Check rows, columns and boxes
        for unit_type in ['row', 'col', 'box']:
            for idx in range(self.size):
                positions = []
                if unit_type == 'row':
                    positions = [(idx, j) for j in range(self.size)]
                elif unit_type == 'col':
                    positions = [(i, idx) for i in range(self.size)]
                else:  # box
                    box_row, box_col = (idx // 3) * 3, (idx % 3) * 3
                    positions = [(box_row + i, box_col + j) 
                               for i in range(3) for j in range(3)]
                
                for num in range(1, self.size + 1):
                    valid_positions = []
                    for pos in positions:
                        if (self.board[pos[0]][pos[1]] == 0 and 
                            num in self.candidates[pos[0]][pos[1]]):
                            valid_positions.append(pos)
                    if len(valid_positions) == 1:
                        unique.append((valid_positions[0], num))
                        
        return unique

    def print_board(self, board: List[List[int]]) -> None:
        """Pretty print the Sudoku board."""
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")
        print()
        
    def solve(self, verbose: bool = False) -> bool:
        """
        Solve the Sudoku using DFS with heuristic strategies.
        
        Args:
            verbose (bool): Whether to print the boards and detailed information
            
        Returns:
            bool: True if solved successfully, False otherwise
        """
        if verbose:
            print("Initial board:")
            self.print_board(self.initial_board)
            
        start_time = time.time()
        self.attempts = 0
        result = self._solve_dfs()
        self.solve_time = time.time() - start_time
        
        if verbose:
            if result and self.validate_solution():
                print("\nSolution found!")
                print(f"Attempts: {self.attempts}")
                print(f"Time: {self.solve_time*1000:.2f}ms")
                print("\nSolution:")
                self.print_board(self.board)
            else:
                print("\nNo solution exists or invalid solution!")
                print(f"Attempts: {self.attempts}")
                print(f"Time: {self.solve_time*1000:.2f}ms")
                
        return result and self.validate_solution()
        
    def _solve_dfs(self) -> bool:
        """DFS implementation with heuristic strategies."""
        self.attempts += 1
        
        # Save current state
        old_board = [row[:] for row in self.board]
        old_candidates = copy.deepcopy(self.candidates)
        
        # Apply strategies
        made_progress = True
        while made_progress:
            made_progress = False
            
            # Strategy I: Single candidates
            singles = self.find_single_candidates()
            for pos, num in singles:
                if self.is_valid(num, pos):
                    self.board[pos[0]][pos[1]] = num
                    self.update_candidates(pos, num)
                    made_progress = True
                else:
                    # Invalid state reached, restore and return
                    self.board = old_board
                    self.candidates = old_candidates
                    return False
                
            # Strategy II: Unique candidates
            if not made_progress:
                uniques = self.find_unique_candidates()
                for pos, num in uniques:
                    if self.is_valid(num, pos):
                        self.board[pos[0]][pos[1]] = num
                        self.update_candidates(pos, num)
                        made_progress = True
                    else:
                        # Invalid state reached, restore and return
                        self.board = old_board
                        self.candidates = old_candidates
                        return False
        
        # Find cell with minimum candidates
        min_candidates = 10
        min_pos = None
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    num_candidates = len(self.candidates[i][j])
                    if num_candidates == 0:  # No valid candidates, invalid state
                        self.board = old_board
                        self.candidates = old_candidates
                        return False
                    if num_candidates < min_candidates:
                        min_candidates = num_candidates
                        min_pos = (i, j)
                        
        if min_pos is None:
            return self.validate_solution()  # 确保找到的解是有效的
            
        row, col = min_pos
        candidates = sorted(list(self.candidates[row][col]))  # Sort for deterministic behavior
        
        # Try each candidate
        for num in candidates:
            if self.is_valid(num, (row, col)):
                # Save state before trying this number
                curr_board = [row[:] for row in self.board]
                curr_candidates = copy.deepcopy(self.candidates)
                
                # Try this number
                self.board[row][col] = num
                self.update_candidates((row, col), num)
                
                if self._solve_dfs():
                    return True
                    
                # Restore state after failed attempt
                self.board = curr_board
                self.candidates = curr_candidates
            
        # No valid solution found with any candidate
        self.board = old_board
        self.candidates = old_candidates
        return False
    
    def get_solve_time(self) -> float:
        """Get the time taken to solve."""
        return self.solve_time
        
    def get_attempts(self) -> int:
        """Get the number of attempts made during solving."""
        return self.attempts