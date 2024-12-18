# Solve sudoku quiz

## Core Strategy: Depth-First Search with Backtracking - solver_naiveDFS.py

We solve Sudoku using a method called Depth-First Search (DFS). Think of it as exploring a path as deeply as possible, and if we reach a dead end, we back up and try a different way.

### Main Algorithm Steps:

- Finding Empty Spaces
  We scan the grid from left to right, top to bottom, looking for empty cells (marked as 0). When we find an empty cell, we stop and try to fill it.
- Validation Process
  Before placing any number, we check three key rules:

  - Row Rule: The number must be unique in its row
  - Column Rule: The number must be unique in its column
  - Box Rule: The number must be unique in its 3×3 box

The Solving Process - it is recursive, but to show how progress is implemented, i write this process.

```python
if (found an empty cell):
    for each number from 1 to 9:
        if (number is valid in this cell):
            # place the number
            # try to solve the rest of the puzzle
            if (solution found):
                we're done!
            else:
                # undo this number and try next one
```

Backtracking Mechanism
If we reach a point where no numbers work, we go back to our last decision and try a different number. This is like an eraser - we can undo our work and try again.

Time Analysis:

Best Case: When we make correct choices immediately
Worst Case: When we need to try many combinations (9^81 possibilities)
Average Case: Much faster than worst case for typical puzzles

## Advanced Sudoku Solving Strategy - solver.py

> referred to docs/sudoku2.pdf

Core Components:

### Candidate Management System

Instead of simply trying numbers 1-9, this solver maintains a list of possible candidates for each empty cell. Imagine having a small notepad in each empty cell listing all possible numbers that could go there.

### Basic Strategy: Candidate Reduction

After placing a number, remove it as a candidate from:
All cells in the same row
All cells in the same column
All cells in the same 3x3 box

### Advanced Strategy I: Single Candidates

Find cells that have only one possible candidate
Example: If a cell can only be 7, then it must be 7

### Advanced Strategy II: Unique Candidates

Find numbers that can only go in one place within a unit
Example: If 4 can only go in one cell of a row, that cell must be 4

### Smart Backtracking

When the advanced strategies can't help anymore:

Choose the cell with the fewest candidates (minimizes branching)
Try each candidate in that cell
If it doesn't work, backtrack and try the next candidate

The Solving Process:

1. Initialize candidates for all empty cells
2. While we can make progress:

   - Apply Strategy I (Single Candidates)
   - If no progress, apply Strategy II (Unique Candidates)

3. If stuck:
   - Find cell with minimum candidates
   - Try each candidate recursively
   - Backtrack if needed
4. Validate final solution

**Improvements Over Basic Solver**:

More efficient: Uses smart candidate selection
Fewer attempts: Advanced strategies reduce guessing
Better handling of hard puzzles: Multiple strategies
Maintains puzzle state: Keeps track of all possibilities

## RWKV Sudoku Solver

A novel approach to solving Sudoku puzzles using RWKV language model reasoning capabilities combined with traditional techniques. This project demonstrates how large language models can be used for logical reasoning tasks with explainable steps.

### Multiple solving approaches:

- RWKV language model solver with step-by-step reasoning
- Real-time solving process explanation
- Puzzle generation with varying difficulties
- Performance benchmarking against known difficult puzzles

```
<input>
0 0 8 1 6 7 0 2 0
5 0 0 2 3 0 0 0 0
...
</input>

<reasoning>
[Analyzing board state]
=> Cell (0,0) has possibilities: 3,4,9
=> Row 1 constrains: 1,2,6,7,8
=> Column 1 restricts...

> Fill cell (0,0) 3
[Explanation of why this choice makes sense]
...
</reasoning>

<output>
3 4 8 1 6 7 5 2 9
...
</output>
```

![alt text](image-1.png)

it is so slow to solve a sudoku, but it can solve it. take an example of inkala2006, it spends 215k tokens to solve it.

> refer to:
> https://github.com/Jellyfish042/Sudoku-RWKV.git > https://huggingface.co/blog/zh/rwkv

# Self-Tester

I also write a tester myself to test the solver with different difficulty levels and test cases.

```{bash}
# Testing
python -m sudoku.tester -n 10 -d easy
python -m sudoku.tester -n 10 -d medium
python -m sudoku.tester -n 10 -d hard
python -m sudoku.tester -n 10 -d extreme

# Test super difficulty
python -m sudoku.tester -d inkala2006
python -m sudoku.tester -d inkala2010
```

| Difficulty Level | Coefficient | Numbers Removed | Description                                |
| ---------------- | ----------- | --------------- | ------------------------------------------ |
| Easy             | 0.3         | 30              | Easiest level to solve                     |
| Medium           | 0.5         | 40              | Moderate difficulty                        |
| Hard             | 0.7         | 50              | Challenging level                          |
| Extreme          | 0.9         | 55              | Close to minimum clues(17), most difficult |

There are more methods to solve a sudoku, referred to docs/sudoku1.pdf.
