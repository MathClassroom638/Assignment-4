import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Coefficients of the objective function (costs per unit of food)
c = [45, 40, 85, 65]  # x1, x2, x3, x4

# Nutritional constraints (converted to ≤ by multiplying by -1)
A = [
    [-3, -4, -8, -6],  # Protein
    [-2, -2, -7, -5],  # Fat
    [-6, -4, -7, -4]   # Carbs
]
b = [-800, -200, -700]

# Bounds: each food amount ≥ 0
x_bounds = [(0, None)] * 4

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Show results and visualize
if res.success:
    x_vals = res.x
    cost = res.fun

    print("✅ Optimal Solution Found:")
    for i, x in enumerate(x_vals):
        print(f"x{i+1} (Food {i+1}): {x:.2f} units")
    print(f"Minimum Total Cost = {cost:.2f} BDT")

    # Visualization: Bar Chart
    labels = [f"Food {i+1}" for i in range(len(x_vals))]
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, x_vals, color=colors)
    plt.title(f"Optimal Food Mix (Cost: {cost:.2f} BDT)")
    plt.ylabel("Units of Food")

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f"{height:.2f}", ha='center')

    plt.tight_layout()
    plt.show()
else:
    print("❌ No feasible solution found.")
