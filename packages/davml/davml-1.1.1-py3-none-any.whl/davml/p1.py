
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
dataset = pd.read_csv("salary_data.csv")
dataset.head()
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 1/3, random_state = 1)
model = LinearRegression()
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
plt.scatter(X_test,y_test, color = "red")
plt.plot(X_test,y_pred, color = "blue")
plt.title("salary vs experience")
plt.xlabel("Years of exp")
plt.ylabel("salary")
plt.show()
