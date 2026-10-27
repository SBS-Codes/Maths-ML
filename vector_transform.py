import matplotlib.pyplot as plt
import numpy as np

# Set up figure and side-by-side subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 1. Define initial basis vectors and a target vector
# v = [2, 1]
i_hat = np.array([1.0, 0.0])
j_hat = np.array([0.0, 1.0])
v = np.array([2.0, 1.0])

# 2. Define transformation matrix A
A = np.array([[1.5, 0.5], [-0.5, 1.2]])

# 3. Compute transformed landing spots
i_trans = A @ i_hat
j_trans = A @ j_hat
v_trans = A @ v

# --- Plot 1: Original Space ---
ax1.set_title("Original Space (Standard Basis)", fontsize=13, fontweight="bold")

# Draw background coordinate grid
for x in np.linspace(-1, 4, 11):
    ax1.axvline(x, color="#E0E0E0", linestyle="--", linewidth=0.8)
for y in np.linspace(-2, 3, 11):
    ax1.axhline(y, color="#E0E0E0", linestyle="--", linewidth=0.8)

ax1.axhline(0, color="black", linewidth=1.2)
ax1.axvline(0, color="black", linewidth=1.2)

# Plot vectors
ax1.quiver(0, 0, i_hat[0], i_hat[1], angles="xy", scale_units="xy", scale=1, color="#D95F02", label="i-hat = [1, 0]")
ax1.quiver(0, 0, j_hat[0], j_hat[1], angles="xy", scale_units="xy", scale=1, color="#7570B3", label="j-hat = [0, 1]")
ax1.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1, color="#1B9E77", label="v = 2(i-hat) + 1(j-hat) = [2, 1]")
ax1.set_xlim(-1, 4)
ax1.set_ylim(-2, 3)
ax1.set_aspect("equal")
ax1.legend(loc="upper left", frameon=True)

# --- Plot 2: Transformed Space ---
ax2.set_title("Transformed Space (Matrix A)", fontsize=13, fontweight="bold")

# Draw transformed coordinate grid lines
for x in np.linspace(-1, 4, 11):
    start, end = A @ np.array([x, -2]), A @ np.array([x, 3])
    ax2.plot([start[0], end[0]], [start[1], end[1]], color="#E0E0E0", linestyle="--", linewidth=0.8)
for y in np.linspace(-2, 3, 11):
    start, end = A @ np.array([-1, y]), A @ np.array([4, y])
    ax2.plot([start[0], end[0]], [start[1], end[1]], color="#E0E0E0", linestyle="--", linewidth=0.8)

ax2.axhline(0, color="black", linewidth=1.2)
ax2.axvline(0, color="black", linewidth=1.2)

# Plot transformed vectors
ax2.quiver(0, 0, i_trans[0], i_trans[1], angles="xy", scale_units="xy", scale=1, color="#D95F02", label="Landing Spot i-hat': [1.5, -0.5]")
ax2.quiver(0, 0, j_trans[0], j_trans[1], angles="xy", scale_units="xy", scale=1, color="#7570B3", label="Landing Spot j-hat': [0.5, 1.2]")
ax2.quiver(0, 0, v_trans[0], v_trans[1], angles="xy", scale_units="xy", scale=1, color="#1B9E77", label="Transformed v' = A v = [3.5, 0.2]")
ax2.set_xlim(-1, 4)
ax2.set_ylim(-2, 3)
ax2.set_aspect("equal")
ax2.legend(loc="upper left", frameon=True)

plt.tight_layout()
plt.show()
