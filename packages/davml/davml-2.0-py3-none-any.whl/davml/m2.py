import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("salary.csv")

X = data.iloc[:, 0]
y = data.iloc[:, 1]

# Manual calculation of linear regression coefficients
n = len(data)
sum_x = sum(X)
sum_y = sum(y)
sum_xy = sum(X * y)
sum_x_squared = sum(X ** 2)

a = (sum_y * sum_x_squared - sum_x * sum_xy) / (n * sum_x_squared - sum_x ** 2)
b = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)

# Predicting salary for a new value (e.g., years of experience = 1.7)
x_test = np.array([1.7, 2.5, 6.5, 1, 2.2])
y_pred = a + b * x_test

# Plotting
plt.scatter(X, y, color="orange", label="Original data")
plt.plot(X, a + b * X, color="blue", label="Linear regression line")
plt.scatter(x_test, y_pred, color="red", label="Predictions")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.title(" Linear Regression")
plt.legend()
plt.show()


## dataset 

,YearsExperience,Salary
0,1.2,39344
1,1.4,46206
2,1.6,37732
3,2.1,43526
4,2.3,39892
5,3,56643
6,3.1,60151
7,3.3,54446
8,3.3,64446
9,3.8,57190
10,4,63219
11,4.1,55795
12,4.1,56958
13,4.2,57082
14,4.6,61112
15,5,67939
16,5.2,66030
17,5.4,83089
18,6,81364
19,6.1,93941
20,6.9,91739
21,7.2,98274
22,8,101303
23,8.3,113813
24,8.8,109432
25,9.1,105583
26,9.6,116970
27,9.7,112636
28,10.4,122392
29,10.6,121873
