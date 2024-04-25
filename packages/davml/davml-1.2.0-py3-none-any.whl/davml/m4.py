from sklearn import datasets
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load breast cancer dataset
data = datasets.load_breast_cancer()
X = data.data
y = data.target

# Print dataset information
print("Number of classes:", len(set(y)))
print("Number of samples per class:")
print(pd.Series(y).value_counts())
print("Total number of samples:", len(y))
print("Dimensionality:", X.shape[1])
print("Features:", data.feature_names)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=60)

# Initialize and train SVM classifier
object_SVM = SVC(kernel='linear')
object_SVM.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = object_SVM.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Print evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)