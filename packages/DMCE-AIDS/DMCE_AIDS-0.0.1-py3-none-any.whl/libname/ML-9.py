from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# Load the iris dataset
iris = load_iris()
X = iris.data
y = iris.target  # Target variable


feature1 = 0
feature2 = 1
plt.scatter(X[:, feature1], X[:, feature2], c=y)  # Color points by target class

# Add labels and title
plt.xlabel(iris.feature_names[feature1])
plt.ylabel(iris.feature_names[feature2])
plt.title("Iris Sepal Length vs. Sepal Width")

# Show the plot
plt.show()

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)  # Assuming we want 2 principal components
X_pca = pca.fit_transform(X_scaled)

# Print the transformed data
print(X_pca)


plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y)  # Color points by target class

# Add labels and title
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Iris Data After PCA")

# Show the plot
plt.show()