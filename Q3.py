import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import linprog

# ----------------------------
# Step 1: Define the LP problem
# ----------------------------

# Maximize Z = 12x1 + 15x2 + 14x3 ⇒ minimize -Z
c = [-12, -15, -14]  # Coefficients for x1 (A), x2 (B), x3 (C)

# Constraints (Ax ≤ b form)
A = [
    [1, 1, 1],            # x1 + x2 + x3 ≤ 100 (Total amount)
    [0, -1, 2],           # -x2 + 2x3 ≤ 0   (Ash ≤ 3%)
    [-0.01, 0.01, 0]      # -0.01x1 + 0.01x2 ≤ 0 (Phosphorous ≤ 0.03%)
]
b = [100, 0, 0]

# Bounds: xi ≥ 0
x_bounds = [(0, None), (0, None), (0, None)]

# ----------------------------
# Step 2: Solve using linprog
# ----------------------------
res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

if res.success:
    print("✅ Optimal Solution Found:")
    for i in range(3):
        print(f"x{i+1} (Coal {chr(65+i)}): {res.x[i]:.2f} tons")
    print(f"Maximum Profit: {-res.fun:.2f} BDT")
else:
    print("❌ No feasible solution found.")

# ----------------------------
# Step 3: Visualization (3D Plot)
# ----------------------------

# Create grid for x1 and x2
x_vals = np.linspace(0, 100, 100)
y_vals = np.linspace(0, 100, 100)
X1, X2 = np.meshgrid(x_vals, y_vals)
Z = np.empty_like(X1)

# Compute feasible x3 and profit Z at each (x1, x2)
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        x1 = X1[i, j]
        x2 = X2[i, j]

        # Apply constraints to solve for feasible x3
        x3_min_ash = x2 / 2           # From ash constraint: x3 ≥ x2 / 2
        x3_max_total = 100 - x1 - x2  # From total: x3 ≤ 100 - x1 - x2

        # Phosphorous constraint: x2 ≤ x1
        if x2 > x1 or x3_min_ash > x3_max_total or x3_min_ash < 0:
            Z[i, j] = np.nan
        else:
            x3 = x3_min_ash  # Use minimum feasible x3 (for max profit)
            Z[i, j] = 12*x1 + 15*x2 + 14*x3  # Compute profit

# Plot the 3D surface
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='k', alpha=0.75)
ax.set_xlabel('Coal A (x1)')
ax.set_ylabel('Coal B (x2)')
ax.set_zlabel('Profit (Z)')
ax.set_title('Feasible Region and Profit Surface')

# Plot optimal point
if res.success:
    x1_opt, x2_opt, x3_opt = res.x
    z_opt = 12*x1_opt + 15*x2_opt + 14*x3_opt
    ax.scatter(x1_opt, x2_opt, z_opt, color='red', s=80, label='Optimal Solution')
    ax.legend()

plt.tight_layout()
plt.show()
