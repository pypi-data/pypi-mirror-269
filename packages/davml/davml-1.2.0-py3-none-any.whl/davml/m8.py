import numpy as np

# Input array and desired output
input_array = np.array([1, 1, 0, 1])
desired_output = 1

# Define parameters
input_weights = np.array([0.3, -0.2, 0.2, 0.1])
bias = 0.2
learning_rate = 0.8

# Initialize iteration counter
iteration = 0
max_iterations = int(input("Enter the maximum number of iterations for the algorithm: "))

while iteration < max_iterations:
    # Forward pass
    net_input = np.dot(input_array, input_weights) + bias
    output = 1 / (1 + np.exp(-net_input))

    # Error calculation
    error = desired_output - output

    # Update weights and bias
    input_weights += learning_rate * error * input_array
    bias += learning_rate * error

    # Increment iteration counter
    iteration += 1

print("Weights:", input_weights)
print("Bias:", bias)
print("Number of iterations executed:", iteration)
print("Final Error:", error)

def perceptron_learning(samples):
    print(f'{"Input":^8}{"Target":^16}{"Weight changes":^15}{"Weights":^28}')
    w1, w2, b = 0, 0, 0
    print(' ' * 48, f'({w1:2}, {w2:2}, {b:2})')
    for x1, x2, y in samples:
        # Calculate the predicted output
        output = 1 if w1 * x1 + w2 * x2 + b >= 0 else 0

        # Update weights and bias using perceptron learning rule
        w1_change = x1 * (y - output)
        w2_change = x2 * (y - output)
        b_change = y - output

        w1 += w1_change
        w2 += w2_change
        b += b_change

        print(f'({x1:2}, {x2:2})\t {y:2}\t ({w1_change:2}, {w2_change:2}, {b_change:2})\t\t ({w1:2}, {w2:2}, {b:2})')

AND_samples = {
    'binary_input_binary_output': [
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
}

print('-' * 20, 'Perceptron Learning', '-' * 20)
print('AND with binary input and binary output')
perceptron_learning(AND_samples['binary_input_binary_output'])