import numpy as np

# Input array and desired output
input_array = np.array([1, 1, 0, 1])
desired_output = 1

# Define parameters
hidden_input_weights = np.array([[0.3, 0.1], [-0.2, 0.4], [0.2, -0.3], [0.1, 0.4]])
hidden_bias_input = np.array([0.2, 0.1])
output_input_weights = np.array([-0.3, 0.2])
bias_output = -0.3
learning_rate = 0.8

# Initialize iteration counter
iteration = 0
max_iterations = int(input("Enter the maximum number of iterations for the algorithm: "))

while iteration < max_iterations:
    # Forward pass
    hidden_netinput = np.dot(input_array, hidden_input_weights) + hidden_bias_input
    hidden_netoutput = 1 / (1 + np.exp(-hidden_netinput))
    net_input_output = np.dot(hidden_netoutput, output_input_weights) + bias_output
    hidden_out = 1 / (1 + np.exp(-net_input_output))

    # Error calculation
    error = desired_output - hidden_out

    # Backpropagation
    error_output_layer = hidden_out * (1 - hidden_out) * error
    error_hidden_layer = hidden_netoutput * (1 - hidden_netoutput) * np.dot(error_output_layer, output_input_weights)

    # Update weights and biases
    hidden_input_weights += learning_rate * np.outer(input_array, error_hidden_layer)
    hidden_bias_input += learning_rate * error_hidden_layer
    output_input_weights += learning_rate * error_output_layer * hidden_netoutput
    bias_output += learning_rate * error_output_layer

    # Increment iteration counter
    iteration += 1

print("Weights for Hidden Layer:")
print(hidden_input_weights)
print("Bias for Hidden Layer:", hidden_bias_input)
print("Weights for Output Layer:", output_input_weights)
print("Bias for Output Layer:", bias_output)
print("Number of iterations executed:", iteration)
print("Final Error:", error)
