import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

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

# Train the random forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using random forest
rf_predictions = rf_model.predict(X_test_vectorized)

# Write the random forest predictions to Column E of the test data
data.loc[X_test.index, 'Random Forest Predictions'] = rf_predictions

# Save the updated data to a new file
data.to_csv('balanced_data_with_predictions.csv', index=False)
