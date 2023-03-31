import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
data = pd.read_csv('balanced_data.csv')

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    data['Review'], data['flair_labels'], random_state=42)

# Vectorize the text data
vect = CountVectorizer().fit(X_train)
X_train_vectorized = vect.transform(X_train)

# Train the logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using logistic regression
X_test_vectorized = vect.transform(X_test)
lr_predictions = lr_model.predict(X_test_vectorized)

# Write the logistic regression predictions to Column D of the test data
data.loc[X_test.index, 'Logistic Regression Predictions'] = lr_predictions

# Calculate and display the accuracy of the logistic regression model
lr_accuracy = accuracy_score(y_test, lr_predictions)
print(f'Logistic Regression Accuracy: {lr_accuracy:.2f}')

# Train the random forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using random forest
rf_predictions = rf_model.predict(X_test_vectorized)

# Write the random forest predictions to Column E of the test data
data.loc[X_test.index, 'Random Forest Predictions'] = rf_predictions

# Calculate and display the accuracy of the random forest model
rf_accuracy = accuracy_score(y_test, rf_predictions)
print(f'Random Forest Accuracy: {rf_accuracy:.2f}')

# Train the decision tree model
clf = DecisionTreeClassifier()
clf_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using decision tree
clf_predictions = clf_model.predict(X_test_vectorized)

# Write the decision tree predictions to Column F of the test data
data.loc[X_test.index, 'Decision Tree Predictions'] = clf_predictions

# Calculate and display the accuracy of the decision tree model
clf_accuracy = accuracy_score(y_test, clf_predictions)
print(f'Decision Tree Accuracy: {clf_accuracy:.2f}')

# Train the decision tree model
clf = DecisionTreeClassifier()
clf_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using multinomial naive bayes
mnb_predictions = mnb_model.predict(X_test_vectorized)

# Write the multinomial naive bayes predictions to Column G of the test data
data.loc[X_test.index, 'Multinomial Naive Bayes Predictions'] = mnb_predictions

# Calculate and display the accuracy of the multinomial naive bayes model
mnb_accuracy = accuracy_score(y_test, mnb_predictions)
print(f'Multinomial Naive Bayes Accuracy: {clf_accuracy:.2f}')
# Save the updated data to a new file
data.to_csv('balanced_data_with_predictions.csv', index=False)
