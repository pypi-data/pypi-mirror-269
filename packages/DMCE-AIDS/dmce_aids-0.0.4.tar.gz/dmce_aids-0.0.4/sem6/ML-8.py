import numpy as np

class SingleLayerPerceptron:
    def __init__(self, learning_rate=0.01, epochs=100):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def activation_function(self, x):
        return np.where(x >= 0, 1, -1)

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)

        for _ in range(self.epochs):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_predicted = self.activation_function(linear_output)
                update = self.learning_rate * (y[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return self.activation_function(linear_output)


# Instantiate the perceptron with a higher number of epochs to ensure learning
slp = SingleLayerPerceptron(learning_rate=0.1, epochs=50)

# Training data for AND gate
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([-1, -1, -1, 1])  # Outputs for AND gate: false (-1), false (-1), false (-1), true (1)

# Training the perceptron
slp.fit(X_train, y_train)

# Predicting with the trained perceptron to test if it has learned the AND logic
predictions = slp.predict(X_train)

# Correcting the access to internal variables
weights = slp.weights
bias = slp.bias

# Display the weights, bias, and predictions
print(weights, bias, predictions)
