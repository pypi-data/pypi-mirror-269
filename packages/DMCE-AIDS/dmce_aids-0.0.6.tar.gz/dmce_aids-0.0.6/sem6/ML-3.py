import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
X1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
X2 = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
Y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])  # Sample binary classification labels
n = len(X1)
# Initializing parameters
b0 = 0
b1 = 0
b2 = 0
# Learning rate and number of iterations
learning_rate = 0.01
num_iterations = 1000
# Gradient descent
for _ in range(num_iterations):
    # Calculate predictions
    predictions = 1 / (1 + np.exp(-(b0 + b1 * X1 + b2 * X2)))
    # Update parameters
    b0 -= learning_rate * np.sum(predictions - Y)
    b1 -= learning_rate * np.sum((predictions - Y) * X1)
    b2 -= learning_rate * np.sum((predictions - Y) * X2)
# Threshold for classification
s = 0.5
# Predictions
predicted_class = np.where(predictions >= s, 1, 0)
print("X1\tX2\tActual Class\tPrediction\tPredicted Class\tŷ")
for i in range(n):
    y_hat = b0 + b1 * X1[i] + b2 * X2[i]
    print(f"{X1[i]}\t{X2[i]}\t{Y[i]}\t\t{predictions[i]:.4f}\t\t{predicted_class[i]}\t\t{y_hat:.2f}")
#Output 1

conf_matrix = confusion_matrix(Y, predicted_class)
sns.set(font_scale =1.5)
fig,ax = plt.subplots(figsize =(10,6))
ax = sns.heatmap(conf_matrix,annot=True,fmt='d',cbar=False)
plt.xlabel("True label")
plt.ylabel("Predicteed label")
plt.show()
