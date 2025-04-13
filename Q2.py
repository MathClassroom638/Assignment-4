import numpy as np
from scipy.optimize import linprog

# Coefficients of the objective function (costs)
c = [45, 40, 85, 65]  # We want to minimize this

# Coefficients of the inequality constraints (Ax ≥ b → -Ax ≤ -b)
A = [
    [-3, -4, -8, -6],  # Proteins
    [-2, -2, -7, -5],  # Fat
    [-6, -4, -7, -4]   # Carbohydrates
]
b = [-800, -200, -700]

# Bounds for each variable (x1 to x4 ≥ 0)
x_bounds = [(0, None)] * 4

# Solve the problem
res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Display results
if res.success:
    print("Optimal Solution Found:")
    for i in range(4):
        print(f"x{i+1} = {round(res.x[i], 2)} units")
    print(f"Minimum Cost = {round(res.fun, 2)} BDT")
else:
    print("No feasible solution found.")
