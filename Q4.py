import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Big-M method setup
M = 1e6  # A very large number to penalize artificial variables

# Objective function:
# Minimize Z = 4x1 + 3x2 + M*a1 + M*a2 + M*a3
# Variables: [x1, x2, a1, a2, a3]
c = [4, 3, M, M, M]

# Constraints converted to equality form:
# 1) 200x1 + 100x2 >= 4000 → -200x1 -100x2 + a1 = -4000
# 2) x1 + 2x2 >= 50       → -x1 -2x2 + a2 = -50
# 3) 40x1 + 40x2 >= 1400  → -40x1 -40x2 + a3 = -1400

A_eq = [
    [-200, -100, 1, 0, 0],
    [-1, -2, 0, 1, 0],
    [-40, -40, 0, 0, 1]
]
b_eq = [-4000, -50, -1400]

# Variable bounds (all ≥ 0)
bounds = [(0, None)] * 5  # x1, x2, a1, a2, a3

# Solve the linear program using scipy's linprog
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Extract decision variables
x1, x2 = res.x[0], res.x[1]
actual_cost = 4 * x1 + 3 * x2

# Display results
if res.success:
    print("✅ Optimal Solution Found:")
    print(f"Food A (x₁) = {round(x1, 2)} units")
    print(f"Food B (x₂) = {round(x2, 2)} units")
    print(f"Minimum Cost = {round(actual_cost, 2)} BDT")
else:
    print("❌ No feasible solution found.")

# ----------- Visualization of Constraints -----------

x = np.linspace(0, 100, 500)

# Lines from original constraints (before conversion)
y1 = (4000 - 200 * x) / 100   # 200x1 + 100x2 ≥ 4000
y2 = (50 - x) / 2             # x1 + 2x2 ≥ 50
y3 = (1400 - 40 * x) / 40     # 40x1 + 40x2 ≥ 1400

plt.figure(figsize=(8, 6))
plt.plot(x, y1, label='Vitamins: 200x₁ + 100x₂ ≥ 4000', color='red')
plt.plot(x, y2, label='Minerals: x₁ + 2x₂ ≥ 50', color='green')
plt.plot(x, y3, label='Calories: 40x₁ + 40x₂ ≥ 1400', color='blue')

# Shade the feasible region
y1_feasible = np.maximum(y1, 0)
y2_feasible = np.maximum(y2, 0)
y3_feasible = np.maximum(y3, 0)
y_feasible = np.maximum.reduce([y1_feasible, y2_feasible, y3_feasible])
plt.fill_between(x, y_feasible, 100, where=(y_feasible <= 100), color='grey', alpha=0.3)

# Mark the optimal point
plt.plot(x1, x2, 'ko', label=f'Optimal Point ({round(x1, 1)}, {round(x2, 1)})')

plt.xlim((0, 50))
plt.ylim((0, 50))
plt.xlabel('Food A units (x₁)')
plt.ylabel('Food B units (x₂)')
plt.title('Feasible Region for Diet Problem (Big-M Method)')
plt.legend()
plt.grid(True)
plt.show()
