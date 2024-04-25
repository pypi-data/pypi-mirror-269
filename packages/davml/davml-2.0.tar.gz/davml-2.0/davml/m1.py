import os
import numpy as np
import tensorflow as tf
from keras.utils import to_categorical

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize the input data
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# One-hot encode the labels
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Define the neural network model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))  # Convolutional layer with 32 filters, kernel size (3,3), ReLU activation, and input shape (28,28,1)
model.add(tf.keras.layers.MaxPooling2D((2, 2)))  # Max pooling layer with pool size (2,2)
model.add(tf.keras.layers.Flatten())  # Flatten layer to convert 2D output to 1D
model.add(tf.keras.layers.Dense(128, activation='relu'))  # Dense (fully connected) layer with 128 neurons and ReLU activation
model.add(tf.keras.layers.Dense(10, activation='softmax'))  # Output layer with 10 neurons (one for each class) and softmax activation

# Display the model summary
model.summary()

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=2)

# Evaluate the model on the test data
loss, accuracy = model.evaluate(x_test, y_test)

# Print the loss and accuracy
print("The model has a loss of: ", loss)
print("The model has an accuracy of about: ", accuracy*100, "%")
