import numpy as np
from sklearn.decomposition import PCA as SklearnPCA


class PCAFromScratch:
    def __init__(self, n_components):
        if not isinstance(n_components, int) or isinstance(n_components, bool):
            raise TypeError("n_components must be an integer.")
        if n_components < 1:
            raise ValueError("n_components must be at least 1.")

        self.n_components = n_components
        self.mean = None
        self.components = None
        self.eigenvalues = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X must be a 2D array.")
        if X.shape[0] < 2 or X.shape[1] < 1:
            raise ValueError("X must contain at least two samples and one feature.")
        if not np.all(np.isfinite(X)):
            raise ValueError("X must contain only finite values.")
        if self.n_components > min(X.shape):
            raise ValueError(
                "n_components cannot exceed the number of samples or features."
            )

        # Step 1: Mean subtraction
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # Step 2: Covariance matrix (sample covariance with N-1)
        cov_matrix = np.atleast_2d(np.cov(X_centered, rowvar=False))

        # Step 3: Eigendecomposition of symmetric matrix
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Step 4: Sort in descending order
        sort_idx = np.argsort(eigenvalues)[::-1]
        self.eigenvalues = eigenvalues[sort_idx]
        self.components = eigenvectors[:, sort_idx]

        # Calculate ratio of total variance captured
        total_variance = np.sum(self.eigenvalues)
        if total_variance <= 0:
            raise ValueError("PCA requires data with non-zero total variance.")
        self.explained_variance_ratio_ = (
            self.eigenvalues[: self.n_components] / total_variance
        )

        # Select top n_components
        self.components = self.components[:, : self.n_components]
        return self

    def transform(self, X):
        if self.mean is None or self.components is None:
            raise RuntimeError("Call fit before transform.")
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.mean.shape[0]:
            raise ValueError("X must be 2D and have the same features as the fit data.")
        if not np.all(np.isfinite(X)):
            raise ValueError("X must contain only finite values.")

        # Center data using fitted mean and project onto eigenvectors
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X_projected):
        if self.mean is None or self.components is None:
            raise RuntimeError("Call fit before inverse_transform.")
        X_projected = np.asarray(X_projected, dtype=float)
        if X_projected.ndim != 2 or X_projected.shape[1] != self.n_components:
            raise ValueError(
                "X_projected must be 2D with n_components columns."
            )
        if not np.all(np.isfinite(X_projected)):
            raise ValueError("X_projected must contain only finite values.")

        # Reconstruct high-dimensional points from projected codes
        return np.dot(X_projected, self.components.T) + self.mean


# Generate reproducible correlated data with three features.
np.random.seed(42)
mean = [2.0, 3.0, 1.0]
cov_true = [
    [3.0, 2.2, 0.6],
    [2.2, 2.0, 0.5],
    [0.6, 0.5, 1.0],
]
X = np.random.multivariate_normal(mean, cov_true, 300)

# Create custom PCA vs. sklearn PCA comparison
pca_custom = PCAFromScratch(n_components=2)
X_projected_custom = pca_custom.fit_transform(X)

pca_sklearn = SklearnPCA(n_components=2)
X_projected_sklearn = pca_sklearn.fit_transform(X)

# Check parity
print("Custom Ratio:", pca_custom.explained_variance_ratio_)
print("Sklearn Ratio:", pca_sklearn.explained_variance_ratio_)

# Eigenvectors may point in opposite directions, so align signs before comparing.
signs = np.sign(
    np.sum(pca_custom.components * pca_sklearn.components_.T, axis=0)
)
X_projected_sklearn *= signs
max_diff = np.max(np.abs(X_projected_custom - X_projected_sklearn))
print(f"Max Difference: {max_diff:.2e}")
