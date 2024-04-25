import numpy as np
import matplotlib.pyplot as plt

# Define dataset
x = np.array([4, 8, 13, 7])
y = np.array([11, 4, 5, 14])
dataset = np.array([x, y])
print("Define Dataset")
print(dataset)
print()

# Finding mean
xMean = np.mean(x)
yMean = np.mean(y)

# Adjusting the mean obtained
MeanAdjusted = np.array([x - xMean, y - yMean])
print("Mean adjusted:")
print(MeanAdjusted)
print("\n")

# Finding the Covariance
covariance_matrix = np.cov(dataset)
print("Covariance Matrix")
print(covariance_matrix)
print("\n")

# Compute the Eigen Values and Eigen Vectors
eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)
print("Eigen Values")
print(eigen_values)
print()

# Sort result in descending order
sorted_indices = np.argsort(eigen_values)[::-1]
sorted_eigen_values = eigen_values[sorted_indices]
sorted_eigen_vectors = eigen_vectors[:, sorted_indices]
print("Sorted Eigen Values")
print(sorted_eigen_values)
print()
print("Sorted Eigen Vectors")
print(sorted_eigen_vectors)
print()

# Perform PCA
PCA = np.dot(sorted_eigen_vectors.T, MeanAdjusted)
print("Principal Component Analysis:")
print(PCA)

# Scatter plot after PCA
plt.subplot(1, 2, 2)
plt.scatter(PCA[0], PCA[1], color='red')
plt.title('After PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

plt.tight_layout()
plt.show()