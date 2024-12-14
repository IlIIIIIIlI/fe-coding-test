```{bash}
# Testing
python -m sudoku.tester -n 10 -d easy
python -m sudoku.tester -n 10 -d medium
python -m sudoku.tester -n 10 -d hard
python -m sudoku.tester -n 10 -d extreme

# Test extreme difficulty
python -m sudoku.tester -d inkala2006
python -m sudoku.tester -d inkala2010
```

![alt text](image.png)

| Difficulty Level | Coefficient | Calculation | Numbers Removed | Numbers Given | Description                                |
| ---------------- | ----------- | ----------- | --------------- | ------------- | ------------------------------------------ |
| Easy             | 0.3         | 0.3 \* 64   | 19              | 62            | Easiest level to solve                     |
| Medium           | 0.5         | 0.5 \* 64   | 32              | 49            | Moderate difficulty                        |
| Hard             | 0.7         | 0.7 \* 64   | 45              | 36            | Challenging level                          |
| Extreme          | 0.9         | 0.9 \* 64   | 58              | 23            | Close to minimum clues(17), most difficult |

Note: The calculation is based on max_to_remove = 64 (81 total cells - 17 minimum clues required for a unique solution)

![alt text](image-1.png)
