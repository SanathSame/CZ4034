import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from joblib import dump
from transformers import BertTokenizer, TFBertForSequenceClassification, RobertaTokenizer, TFRobertaForSequenceClassification
import tensorflow as tf

# Load data
data = pd.read_csv('final_dataset.csv')

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    data['Review'], data['flair_labels'], random_state=42)


# Load the pre-trained RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
# Load the fine-tuned RoBERTa model
roberta_model = TFRobertaForSequenceClassification.from_pretrained(
    'RoBERTa_model')

# Tokenize the training and test data
train_encodings = tokenizer(X_train.tolist(), truncation=True, padding=True)
test_encodings = tokenizer(X_test.tolist(), truncation=True, padding=True)

# Convert the tokenized data into a TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),
    y_train
))
test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    y_test
))

# Use the loaded model for prediction
roberta_predictions = roberta_model.predict(
    test_dataset.batch(16)).logits.argmax(axis=-1)

# Write the RoBERTa predictions to Column I of the test data
data.loc[X_test.index, 'RoBERTa'] = roberta_predictions

# Calculate and display the accuracy of the RoBERTa model
roberta_accuracy = accuracy_score(y_test, roberta_predictions)
print(f'RoBERTa Accuracy: {roberta_accuracy:.2f}')

# Display the classification report for the RoBERTa model
print('RoBERTa Classification Report:')
print(classification_report(y_test, roberta_predictions))

# Save the updated data to a new file
data.to_csv('final_dataset_with_predictions.csv', index=False)
