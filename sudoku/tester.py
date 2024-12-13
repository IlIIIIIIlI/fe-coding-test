# sudoku/tester.py
import argparse
from typing import List, Dict, Any
import time
from .solver import SudokuSolver
from .generator import SudokuGenerator

class SudokuTester:
    """Test Sudoku solver performance."""
    
    # Difficulty mapping
    DIFFICULTY_LEVELS = {
        'easy': 0.3,
        'medium': 0.5,
        'hard': 0.7,
        'extreme': 0.9
    }
    
    def __init__(self, num_puzzles: int = 10, difficulty: str = 'medium'):
        """
        Initialize tester.
        
        Args:
            num_puzzles (int): Number of puzzles to test
            difficulty (str): Difficulty level
                            ('easy', 'medium', 'hard', 'extreme', 'inkala2006')
        """
        self.num_puzzles = num_puzzles
        self.difficulty = difficulty
        self.results: List[Dict[str, Any]] = []
        
    def run_tests(self) -> None:
        """Run the performance tests."""
        print(f"\nRunning Sudoku Solver Tests")
        print("-" * 50)
        
        def print_board(board):
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
            print()  # Extra line after board
            
        if self.difficulty == 'inkala2006':
            # Test specific Inkala puzzle
            puzzle = getattr(SudokuGenerator, 'INKALA_2006')
            print(f"Testing {self.difficulty.upper()} puzzle (World's most difficult Sudoku)")
            print("\nInitial board:")
            print_board(puzzle)
            puzzle_copy = [row[:] for row in puzzle]
            solver = SudokuSolver(puzzle_copy)
            solved = solver.solve()
            solve_time = solver.get_solve_time()
            
            self.results.append({
                'solved': solved,
                'time': solve_time,
                'puzzle_type': 'inkala2006'
            })
        else:
            # Test random puzzles
            difficulty_value = self.DIFFICULTY_LEVELS[self.difficulty]
            print(f"Testing {self.num_puzzles} puzzles with difficulty: {self.difficulty.upper()}")
            
            for i in range(self.num_puzzles):
                puzzle = SudokuGenerator.generate_puzzle(difficulty_value)
                solver = SudokuSolver(puzzle)
                
                solved = solver.solve()
                solve_time = solver.get_solve_time()
                
                self.results.append({
                    'solved': solved,
                    'time': solve_time,
                    'puzzle_type': 'random'
                })
                
                print(f"Progress: {i+1}/{self.num_puzzles}", end='\r')
            print()  # New line after progress
            
    def print_results(self) -> None:
        """Print detailed test results."""
        print("\nResults:")
        
        if self.difficulty == 'inkala2006':
            # For predefined puzzles
            result = self.results[0]
            print(f"Solved: {'Yes' if result['solved'] else 'No'}")
            print(f"Time taken: {result['time']*1000:.2f}ms")
        else:
            # For random puzzles
            solved_count = sum(1 for r in self.results if r['solved'])
            total_time = sum(r['time'] for r in self.results)
            success_rate = (solved_count / len(self.results)) * 100
            avg_time = total_time / len(self.results)
            
            # Calculate min and max times
            times = [r['time'] * 1000 for r in self.results]  # Convert to ms
            min_time = min(times)
            max_time = max(times)
            
            print(f"Solved: {solved_count}/{self.num_puzzles} ({success_rate:.1f}%)")
            print(f"Average time: {avg_time*1000:.2f}ms")
            print(f"Min time: {min_time:.2f}ms")
            print(f"Max time: {max_time:.2f}ms")

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Sudoku Solver Tester')
    parser.add_argument('-n', '--num_puzzles', type=int, default=10,
                      help='Number of puzzles to test')
    parser.add_argument('-d', '--difficulty', 
                      default='medium',
                      choices=['easy', 'medium', 'hard', 'extreme', 'inkala2006'],
                      help='Puzzle difficulty level')
    args = parser.parse_args()
    
    tester = SudokuTester(args.num_puzzles, args.difficulty)
    tester.run_tests()
    tester.print_results()

if __name__ == "__main__":
    main()