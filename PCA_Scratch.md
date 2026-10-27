# Principal Component Analysis from Scratch

This guide explains [`PCA_Scratch.py`](./PCA_Scratch.py). The script implements a basic PCA transformer with NumPy, generates a reproducible dataset, and compares its results with scikit-learn's PCA implementation.

## What the script does

The script generates 300 observations with three features, then:

1. Centers the data by subtracting each feature's mean.
2. Computes the sample covariance matrix.
3. Finds the covariance matrix's eigenvalues and eigenvectors.
4. Sorts the eigenvectors by decreasing eigenvalue and keeps the requested number of components.
5. Projects the data onto those components.
6. Compares its explained-variance ratios and projected data with scikit-learn's results.

The example requests two components, reducing each three-feature observation to two values.

## Mathematical ideas

### 1. Centering the data

Let $X$ be a data matrix with $n$ observations (rows) and $d$ features (columns). The mean of each feature is

$$
\mu_j = \frac{1}{n}\sum_{i=1}^{n} x_{ij}.
$$

The script subtracts the feature means from every observation:

$$
X_c = X - \mu.
$$

Centering places the data around zero. PCA uses the variation around the mean to find its principal directions.

### 2. Covariance matrix

The sample covariance matrix is

$$
C = \frac{1}{n-1} X_c^\mathsf{T} X_c.
$$

It is a $d \times d$ matrix. Its diagonal entries are the feature variances, and its off-diagonal entries describe how pairs of features vary together. NumPy's `np.cov(X_centered, rowvar=False)` computes this matrix; `rowvar=False` means rows are observations and columns are features.

### 3. Eigenvectors and principal components

The script solves the eigenvector equation for the covariance matrix:

$$
C u_i = \lambda_i u_i.
$$

Each eigenvector $u_i$ is a direction in feature space, and its eigenvalue $\lambda_i$ is the variance along that direction. Eigenvectors are sorted from the largest eigenvalue to the smallest:

- The first principal component points along the direction of greatest data variance.
- The second points along the next greatest direction, perpendicular to the first.
- Keeping only the top $k$ directions reduces the number of dimensions while retaining as much variance as possible among all $k$-dimensional linear projections.

The code uses `np.linalg.eigh`, which is designed for symmetric matrices such as covariance matrices.

### 4. Explained variance

The explained-variance ratio for component $i$ is

$$
r_i = \frac{\lambda_i}{\sum_{j=1}^{d} \lambda_j}.
$$

It tells what fraction of the total variance is captured by that component. The ratios for the selected components need not add up to 1; the remaining variance belongs to the components that were dropped.

### 5. Projection and reconstruction

If $U_k$ contains the selected eigenvectors as columns, transforming the centered observations is

$$
Z = X_c U_k.
$$

Each row of $Z$ is the lower-dimensional representation of one observation. The script's `transform` method uses the mean and components learned in `fit`.

The approximate reconstruction back in the original feature space is

$$
\widehat{X} = Z U_k^\mathsf{T} + \mu.
$$

Because discarded components are not retained, this reconstruction generally loses some information. The `inverse_transform` method performs this calculation.

## Implementation overview

- `PCAFromScratch(n_components)` creates a PCA transformer and checks that the requested component count is a positive integer.
- `fit(X)` validates the data, learns the mean, covariance, eigenvalues, eigenvectors, and explained-variance ratios.
- `transform(X)` centers new data using the fitted mean and projects it onto the learned components.
- `fit_transform(X)` learns the PCA model and transforms the data in one call.
- `inverse_transform(X_projected)` maps projected data back to an approximate representation in the original feature space.

The implementation requires at least two observations, finite numeric values, and a nonzero total variance. Transforming or reconstructing data before fitting raises an error.

## How to run

Install the dependencies:

```bash
python3 -m pip install numpy scikit-learn
```

Run the comparison from the folder containing the script:

```bash
python3 PCA_Scratch.py
```

The random seed is set to `42`, making the generated example reproducible for a given NumPy environment.

## Output

Running the script produced:

```text
Custom Ratio: [0.77997336 0.16852251]
Sklearn Ratio: [0.77997336 0.16852251]
Max Difference: 5.22e-15
```

The two retained components explain about $77.997336\%$ and $16.852251\%$ of the total variance, respectively, or approximately $94.849587\%$ together. The small maximum difference (about $5.22 \times 10^{-15}$) is near floating-point precision and shows that the custom projection agrees closely with scikit-learn in this run.

Eigenvectors can have either sign and still represent the same principal direction. The script aligns component signs before comparing projected values so that this arbitrary sign choice does not make equivalent results appear different.

## Files

- [`PCA_Scratch.py`](./PCA_Scratch.py) — PCA implementation and comparison example.
- [`PCA_Scratch.md`](./PCA_Scratch.md) — this explanation.
