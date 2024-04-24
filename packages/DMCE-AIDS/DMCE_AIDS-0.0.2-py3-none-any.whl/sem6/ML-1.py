import numpy as np
import pandas as pd
import tensorflow as tf
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.datasets import mnist # Dataset
mnist = tf.keras.datasets.mnist
(train_images, train_labels),(test_images, test_labels) = mnist.load_data()
# Display dataset properties
print("Train images shape:", train_images.shape)
print("Train labels shape:", train_labels.shape)
print("Test images shape:", test_images.shape)
print("Test labels shape:", test_labels.shape)
num_classes = len(np.unique(train_labels))
print("Number of different labels in the dataset:", num_classes)
#Output 1
# Normalize the pixel values to be between 0 and 1
train_images = train_images / 255.0
test_images = test_images / 255.0
# Define the neural network model
def tfmodel():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='sigmoid')
    ])
    return model

model = tfmodel()
# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# Train the model on the training data
hist = model.fit(train_images, train_labels, epochs=5, validation_split=0.2)
#Output 2
# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(test_images, test_labels)
print(f'Test-accuracy: {test_accuracy}')
#Output 3
# Make predictions on the test data
predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)
print(predicted_labels)
#Output 4

#if any URL error occurs then 
# requests.packages.urllib3.disable_warnings()
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     # Legacy Python that doesn't verify HTTPS certificates by default
#     pass
# else:
#     # Handle target environment that doesn't support HTTPS verification
#     ssl._create_default_https_context = _create_unverified_https_context