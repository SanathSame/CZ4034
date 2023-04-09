import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from joblib import load
import time

# Load data
data = pd.read_csv('balanced_data.csv')

reviews, targets = data['Review'], data['flair_labels']

# Load the CountVectorizer object used for training
vect = load('vectorizer.joblib')

# Load the logistic regression model
lr_model = load('rf_model.joblib')

# Predict the sentiment for the test data using logistic regression
X_test_vectorized = vect.transform(reviews)
start = time.time()
lr_predictions = lr_model.predict(X_test_vectorized)
end = time.time()

# Write the logistic regression predictions to Column D of the test data
data.loc[reviews.index, 'Logistic Regression Predictions'] = lr_predictions

# Calculate and display the accuracy of the logistic regression model
lr_accuracy = accuracy_score(targets, lr_predictions)
print(f'Logistic Regression Accuracy: {lr_accuracy:.2f}')

# Display the classification report for the Logistic Regression model
print('Logistic Regression Classification Report:')
print(classification_report(targets, lr_predictions))

total_minutes = (end - start)/60
total_hours = total_minutes/60
if (total_hours < 1):
    print("Time taken: " + str(total_minutes) + " minutes")
else:
    print("Time taken: " + str(total_hours) + " hours")
