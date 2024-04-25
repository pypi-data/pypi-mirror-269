import numpy as np
import matplotlib.pyplot as plt
n = int(input("Enter the number of values (n): "))

X1_values = input("Enter X1 values separated by commas: ").split(',')
X1 = np.array([float(x.strip()) for x in X1_values])

X2_values = input("Enter X2 values separated by commas: ").split(',')
X2 = np.array([float(x.strip()) for x in X2_values])

Y_values = input("Enter Y values separated by commas: ").split(',')
Y = np.array([float(y.strip()) for y in Y_values])
print("X1:", X1)
print("X2:", X2)
print("Y:", Y)
b0, b1, b2 = 0, 0, 0
s = float(input("Enter threshold between 0 to 1: "))
p = []
pc = []
for i in range(n):
    P = 1 / (1 + np.exp(-(b0 + b1 * X1[i] + b2 * X2[i] + b2 * X2[i])))
    b0 = b0 + 0.01 * (Y[i] - P) * P * (1 - P) * 1
    b1 = b1 + 0.01 * (Y[i] - P) * P * (1 - P) * X1[i]
    b2 = b2 + 0.01 * (Y[i] - P) * P * (1 - P) * X2[i]
print(f"Calculated coefficients:  b0 = {b0}, b1 = {b1}, b2 = {b2}")
print("X1\tX2\tActual Class\tP\tPc")
print("X1\tX2\tActual class\tPediction p\tPredictiion class pc")
for i in range(n):
    P = 1 / (1 + np.exp(-(b0 + b1 * X1[i] + b2 * X2[i] + b2 * X2[i])))
    pc.append(1 if P > s else 0) # threshold wala loop
    print(f"{X1[i]}\t{X2[i]}\t{Y[i]}\t\t{P}\t\t{pc[i]}")
