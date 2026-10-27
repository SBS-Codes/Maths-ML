import matplotlib.pyplot as plt
import numpy as np

# 1. Generate a correlated 2D dataset (300 data points)
np.random.seed(42)
mean = [2.0, 3.0]
cov_true = [[3.0, 2.2], [2.2, 2.0]]
X = np.random.multivariate_normal(mean, cov_true, 300)

# 2. Compute dataset mean and center the data
X_mean = np.mean(X, axis=0)
X_centered = X - X_mean

# 3. Calculate covariance matrix and eigendecomposition
cov_matrix = np.cov(X_centered, rowvar=False)
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

# Sort eigenvalues and eigenvectors in descending order
sort_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sort_indices]
eigenvectors = eigenvectors[:, sort_indices]

# 4. Plot the data points and principal axes
fig, ax = plt.subplots(figsize=(9, 7))
ax.scatter(
    X[:, 0],
    X[:, 1],
    alpha=0.55,
    color="#2B5C8F",
    s=35,
    label="Data Points",
)
ax.scatter(
    X_mean[0],
    X_mean[1],
    color="#D9381E",
    s=80,
    zorder=5,
    label="Dataset Mean (x̄)",
)

# Draw eigenvectors scaled by standard deviation (sqrt of eigenvalue)
colors = ["#D9381E", "#2E7D32"]
for i in range(2):
    # Scale vector length by 2 standard deviations for visual clarity
    v = eigenvectors[:, i] * np.sqrt(eigenvalues[i]) * 2
    ax.annotate(
        "",
        xy=(X_mean[0] + v[0], X_mean[1] + v[1]),
        xytext=(X_mean[0], X_mean[1]),
        arrowprops=dict(
            facecolor=colors[i],
            edgecolor=colors[i],
            width=2.5,
            headwidth=10,
            shrink=0,
        ),
    )
    ax.plot(
        [],
        [],
        color=colors[i],
        linewidth=2.5,
        label=f"Eigenvector {i + 1} (λ_{i + 1} = {eigenvalues[i]:.2f})",
    )

ax.set_title(
    "Eigenvectors of Data Covariance Matrix (Principal Axes)",
    fontsize=14,
    fontweight="bold",
)
ax.set_xlabel("Feature 1 ($x_1$)")
ax.set_ylabel("Feature 2 ($x_2$)")
ax.grid(True, linestyle="--", alpha=0.5)
ax.set_aspect("equal")
ax.legend(loc="upper left", frameon=True)

plt.tight_layout()
plt.show()
