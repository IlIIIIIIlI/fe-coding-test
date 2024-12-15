from solver import DFSSolver

solver = DFSSolver()
matrix = [
    [7, 8, 3, 4, 9, 6, 2, 1, 5],
    [6, 9, 2, 1, 5, 3, 4, 8, 7],
    [4, 1, 5, 8, 2, 7, 3, 9, 6],
    [3, 6, 0, 5, 0, 9, 0, 4, 0],
    [9, 2, 4, 6, 7, 1, 5, 3, 8],
    [5, 7, 1, 3, 4, 8, 6, 2, 9],
    [8, 3, 9, 7, 6, 5, 1, 0, 4],
    [1, 5, 7, 2, 3, 4, 8, 6, 0],
    [2, 4, 6, 9, 1, 0, 7, 5, 3]
]

solved = solver.solve(matrix)
if solved:
    print("Solution found!")
    stats = solver.get_stats()
    print(f"Attempts: {stats['attempts']}")
    print(f"Time: {stats['time']:.2f}s")
else:
    print("No solution exists")

# RWKV求解器
from solver import RWKVSolver 

solver = RWKVSolver()
solved = solver.solve(matrix)