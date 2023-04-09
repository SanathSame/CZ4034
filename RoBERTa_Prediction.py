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
import time

# Load data
data = pd.read_csv('testRoBERTa.csv')

reviews, targets = data['Review'], data['flair_labels']

# Load the pre-trained RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
# Load the fine-tuned RoBERTa model
roberta_model = TFRobertaForSequenceClassification.from_pretrained(
    'RoBERTa_model')

# Tokenize the training and test data
# train_encodings = tokenizer(X_train.tolist(), truncation=True, padding=True)
test_encodings = tokenizer(reviews.tolist(), truncation=True, padding=True)

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    targets
))
start = time.time()
# Use the loaded model for prediction
roberta_predictions = roberta_model.predict(
    test_dataset.batch(16)).logits.argmax(axis=-1)
end = time.time()
# Write the RoBERTa predictions to Column I of the test data
data.loc[reviews.index, 'RoBERTa'] = roberta_predictions

# Calculate and display the accuracy of the RoBERTa model
roberta_accuracy = accuracy_score(targets, roberta_predictions)
print(f'RoBERTa Accuracy: {roberta_accuracy:.2f}')

# Display the classification report for the RoBERTa model
print('RoBERTa Classification Report:')
print(classification_report(targets, roberta_predictions))

# Save the updated data to a new file
data.to_csv('RoBERTa.csv', index=False)
total_minutes = (end - start)/60
total_hours = total_minutes/60
if (total_hours < 1):
    print("Time taken: " + str(total_minutes) + " minutes")
else:
    print("Time taken: " + str(total_hours) + " hours")
