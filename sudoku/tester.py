import argparse
import json
import os
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime
from .solver import SudokuSolver
from .generator import SudokuGenerator

class SudokuTester:
    """Test Sudoku solver performance and save results."""

    # Difficulty mapping with corresponding max cells to remove
    DIFFICULTY_LEVELS = {
        'easy': 0.3,    # Remove ~19 numbers, keep 62
        'medium': 0.5,  # Remove ~32 numbers, keep 49
        'hard': 0.7,    # Remove ~45 numbers, keep 36
        'extreme': 0.9  # Remove ~58 numbers, keep 23
    }

    def __init__(self, num_puzzles: int = 10, difficulty: str = 'medium', save_dir: str = None):
        """
        Initialize tester.
        
        Args:
            num_puzzles (int): Number of puzzles to test
            difficulty (str): Difficulty level ('easy', 'medium', 'hard', 'extreme')
            save_dir (str): Directory to save generated puzzles, relative to sudoku package
        """
        self.num_puzzles = num_puzzles
        self.difficulty = difficulty
        
        # Set default save directory within sudoku package
        if save_dir is None:
            import os.path
            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.save_dir = os.path.join(package_dir, 'sudoku', 'puzzles')
        else:
            self.save_dir = save_dir
            
        self.results: List[Dict[str, Any]] = []
        self.stats: Dict[str, float] = {}
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)

    def save_puzzles(self) -> None:
        """Save generated puzzles and solutions to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.save_dir}/sudoku_{self.difficulty}_{timestamp}.json"
        
        save_data = {
            "metadata": {
                "difficulty": self.difficulty,
                "number_of_puzzles": self.num_puzzles,
                "generated_at": timestamp,
                "stats": self.stats
            },
            "puzzles": [{
                "id": i + 1,
                "puzzle": result["puzzle"],
                "solution": result["solution"],
                "solve_time_ms": result["time"] * 1000,
                "solve_attempts": result["attempts"]
            } for i, result in enumerate(self.results)]
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
            
        print(f"\nPuzzles saved to: {filename}")

    def run_tests(self) -> None:
        """Run the performance tests."""
        print(f"\nRunning Sudoku Solver Tests")
        print("-" * 50)
        
        if self.difficulty in ['inkala2006', 'inkala2010']:
            # Test specific Inkala puzzle
            if self.difficulty == 'inkala2006':
                puzzle = SudokuGenerator.INKALA_2006
                print(f"Testing Inkala 2006 puzzle (World's most difficult Sudoku)")
            else:
                puzzle = SudokuGenerator.INKALA_2010
                print(f"Testing Inkala 2010 puzzle (AI Escargot)")
                
            puzzle_copy = [row[:] for row in puzzle]
            solver = SudokuSolver(puzzle_copy)
            solved = solver.solve(verbose=True)
            
            self.results.append({
                'puzzle': puzzle,
                'solution': solver.board if solved else None,
                'solved': solved,
                'time': solver.get_solve_time(),
                'attempts': solver.get_attempts()
            })
            
        else:
            # Test random puzzles
            difficulty_value = self.DIFFICULTY_LEVELS[self.difficulty]
            print(f"Testing {self.num_puzzles} puzzles with difficulty: {self.difficulty.upper()}")
            
            total_time = 0
            total_attempts = 0
            solved_count = 0
            min_time = float('inf')
            max_time = 0
            
            for i in range(self.num_puzzles):
                puzzle, solution = SudokuGenerator.generate_puzzle(difficulty_value)
                puzzle_copy = [row[:] for row in puzzle]
                solver = SudokuSolver(puzzle_copy)
                solved = solver.solve(verbose=False)
                solve_time = solver.get_solve_time()
                attempts = solver.get_attempts()
                
                total_time += solve_time
                total_attempts += attempts
                if solved:
                    solved_count += 1
                min_time = min(min_time, solve_time)
                max_time = max(max_time, solve_time)
                
                print(f"Progress: {i+1}/{self.num_puzzles}", end='\r')
                
                self.results.append({
                    'puzzle': puzzle,
                    'solution': solution,
                    'solved': solved,
                    'time': solve_time,
                    'attempts': attempts
                })
                
            print()  # New line after progress
            
            # Store statistics
            self.stats = {
                'total_time': total_time,
                'avg_time': total_time / self.num_puzzles,
                'min_time': min_time,
                'max_time': max_time,
                'total_attempts': total_attempts,
                'avg_attempts': total_attempts / self.num_puzzles,
                'solved_count': solved_count,
                'success_rate': (solved_count / self.num_puzzles) * 100
            }

    def print_results(self) -> None:
        """Print test results."""
        if not self.results:
            print("\nNo results available!")
            return
            
        print("-" * 50)
        
        if self.difficulty in ['inkala2006', 'inkala2010']:
            # Single puzzle results
            result = self.results[0]
            print(f"Status: {'Solved' if result['solved'] else 'Failed to solve'}")
            print(f"Time: {result['time']*1000:.2f}ms")
            print(f"Attempts: {result['attempts']}")
        else:
            # Multiple puzzle statistics
            print(f"Solved: {self.stats['solved_count']}/{self.num_puzzles} "
                  f"({self.stats['success_rate']:.1f}%)")
            print(f"Average time: {self.stats['avg_time']*1000:.2f}ms")
            print(f"Min time: {self.stats['min_time']*1000:.2f}ms")
            print(f"Max time: {self.stats['max_time']*1000:.2f}ms")
            print(f"Average attempts: {self.stats['avg_attempts']:.1f}")

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description='Sudoku Solver Tester')
    parser.add_argument('-n', '--num_puzzles', type=int, default=10,
                      help='Number of puzzles to test')
    parser.add_argument('-d', '--difficulty',
                      default='medium',
                      choices=['easy', 'medium', 'hard', 'extreme',
                              'inkala2006', 'inkala2010'],
                      help='Puzzle difficulty level')
    parser.add_argument('-s', '--save_dir', default=None,
                      help='Directory to save generated puzzles (default: sudoku/puzzles)')
    
    args = parser.parse_args()
    
    tester = SudokuTester(args.num_puzzles, args.difficulty, args.save_dir)
    tester.run_tests()
    tester.print_results()
    tester.save_puzzles()

if __name__ == "__main__":
    main()