import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Objective function (we negate for maximization)
c = [-2, -1]  # Maximize Z = 2x1 + x2 → Minimize -Z

# Constraints: A_ub * x <= b_ub
A = [
    [1, 2],     # x1 + 2x2 <= 10
    [1, 1],     # x1 + x2 <= 6
    [1, -1],    # x1 - x2 <= 2
    [1, -2]     # x1 - 2x2 <= 1
]
b = [10, 6, 2, 1]

# Bounds for x1 and x2
x_bounds = (0, None)
y_bounds = (0, None)

# Solve using linprog
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

# Print optimal values
print("Optimal Solution:")
print(f"x1 = {round(res.x[0], 2)}")
print(f"x2 = {round(res.x[1], 2)}")
print(f"Maximum Z = {round(-res.fun, 2)}")  # Reverse sign to get max value

# ----------------------------
# Plotting the feasible region
# ----------------------------
x = np.linspace(0, 10, 400)
plt.figure(figsize=(10, 8))

# Constraint lines
plt.plot(x, (10 - x)/2, label=r'$x_1 + 2x_2 \leq 10$')
plt.plot(x, 6 - x, label=r'$x_1 + x_2 \leq 6$')
plt.plot(x, x - 2, label=r'$x_1 - x_2 \leq 2$')
plt.plot(x, (x - 1)/2, label=r'$x_1 - 2x_2 \leq 1$')

# Shading feasible region
y1 = (10 - x)/2
y2 = 6 - x
y3 = x - 2
y4 = (x - 1)/2

# Combine all upper bounds and clip below x-axis
y = np.minimum.reduce([y1, y2, y3, y4])
y = np.maximum(y, 0)

plt.fill_between(x, 0, y, where=(y >= 0), color='lightblue', alpha=0.5, label='Feasible Region')

# Plot optimal point
if res.success:
    plt.plot(res.x[0], res.x[1], 'ro', label='Optimal Point')

# Labels and Legend
plt.xlim(0, 8)
plt.ylim(0, 8)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')
plt.title('Graphical Solution to Linear Programming Problem')
plt.legend()
plt.grid(True)
plt.show()
