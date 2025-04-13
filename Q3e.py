import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Objective function (maximize profit)
c = [-12, -15, -14]  # Coefficients for x1 (A), x2 (B), x3 (C)

# Constraints (Ax ≤ b)
A = [
    [1, 1, 1],            # x1 + x2 + x3 ≤ 100 (Total amount)
    [0, -1, 2],           # -x2 + 2x3 ≤ 0   (Ash ≤ 3%)
    [-0.01, 0.01, 0]      # -0.01x1 + 0.01x2 ≤ 0 (Phosphorous ≤ 0.03%)
]
b = [100, 0, 0]
x_bounds = [(0, None), (0, None), (0, None)]

# Solve the LP problem
res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Print results
if res.success:
    x1, x2, x3 = res.x
    total_profit = -res.fun
    print(f"Coal A (x1): {x1:.2f} tons")
    print(f"Coal B (x2): {x2:.2f} tons")
    print(f"Coal C (x3): {x3:.2f} tons")
    print(f"Total Profit: {total_profit:.2f} BDT")

    # Bar Chart Visualization
    labels = ['Coal A', 'Coal B', 'Coal C']
    values = [x1, x2, x3]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, color=['#1f77b4', '#2ca02c', '#ff7f0e'])
    plt.title(f"Optimal Coal Mix (Total Profit: {total_profit:.2f} BDT)")
    plt.ylabel("Tons Used")
    plt.ylim(0, max(values)*1.2)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.2f}', ha='center')

    plt.tight_layout()
    plt.show()
else:
    print("❌ No feasible solution found.")
