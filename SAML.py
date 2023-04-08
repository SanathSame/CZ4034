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

# Display the classification report for the Logistic Regression model
print('Logistic Regression Classification Report:')
print(classification_report(y_test, lr_predictions))

# Train the random forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using random forest
X_test_vectorized = vect.transform(X_test)
rf_predictions = rf_model.predict(X_test_vectorized)

# Write the random forest predictions to Column E of the test data
data.loc[X_test.index, 'Random Forest Predictions'] = rf_predictions

# Calculate and display the accuracy of the random forest model
rf_accuracy = accuracy_score(y_test, rf_predictions)
print(f'Random Forest Accuracy: {rf_accuracy:.2f}')

# Display the classification report for the Random Forest model
print('Random Forest Classification Report:')
print(classification_report(y_test, rf_predictions))


# Train the Multinomial Naive Bayes model
mnb = MultinomialNB()
mnb.fit(X_train_vectorized, y_train)

# Predict the sentiment for the test data using Multinomial Naive Bayes
mnb_predictions = mnb.predict(X_test_vectorized)

# Write the Multinomial Naive Bayes predictions to Column G of the test data
data.loc[X_test.index, 'Multinomial Naive Bayes Predictions'] = mnb_predictions

# Calculate and display the accuracy of the Multinomial Naive Bayes model
mnb_accuracy = accuracy_score(y_test, mnb_predictions)
print(f'Multinomial Naive Bayes Accuracy: {mnb_accuracy:.2f}')

# Display the classification report for the MNB model
print('MNB Classification Report:')
print(classification_report(y_test, mnb_predictions))

# Load the pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertForSequenceClassification.from_pretrained(
    'bert-base-uncased')

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

# Fine-tune the BERT model on the training data
bert_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
                   loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = bert_model.fit(train_dataset.shuffle(1000).batch(16),
                         validation_data=test_dataset.batch(16),
                         epochs=3,
                         batch_size=16)

# Predict the sentiment for the test data using BERT
bert_predictions = bert_model.predict(
    test_dataset.batch(16)).logits.argmax(axis=-1)

# Write the BERT predictions to Column H of the test data
data.loc[X_test.index, 'BERT Predictions'] = bert_predictions

# Calculate and display the accuracy of the BERT model
bert_accuracy = accuracy_score(y_test, bert_predictions)
print(f'BERT Accuracy: {bert_accuracy:.2f}')

# Plotting loss and accuracy curves for training and test accuracy
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Loss/Accuracy curve for BERT')
plt.ylabel('Loss/Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training Loss', 'Test Loss', 'Training Accuracy',
           'Test Accuracy'], loc='upper right')
plt.savefig('bert_loss_accuracy_curve.png')

# Display the classification report for the BERT model
print('BERT Classification Report:')
print(classification_report(y_test, bert_predictions))

# #Save the fine-tuned BERT model
# bert_model.save_pretrained('BERT_model')

# Load the pre-trained RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
roberta_model = TFRobertaForSequenceClassification.from_pretrained(
    'roberta-base')

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

# Fine-tune the RoBERTa model on the training data
roberta_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

history = roberta_model.fit(train_dataset.shuffle(1000).batch(16),
                            validation_data=test_dataset.batch(16),
                            epochs=3,
                            batch_size=16)

# Predict the sentiment for the test data using RoBERTa
roberta_predictions = roberta_model.predict(
    test_dataset.batch(16)).logits.argmax(axis=-1)

# Write the RoBERTa predictions to Column I of the test data
data.loc[X_test.index, 'RoBERTa Predictions'] = roberta_predictions

# Calculate and display the accuracy of the RoBERTa model
roberta_accuracy = accuracy_score(y_test, roberta_predictions)
print(f'RoBERTa Accuracy: {roberta_accuracy:.2f}')

# Display the classification report for the RoBERTa model
print('RoBERTa Classification Report:')
print(classification_report(y_test, roberta_predictions))

# Plotting loss and accuracy curves for training and test accuracy
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Loss/Accuracy curve for RoBERTa')
plt.ylabel('Loss/Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training Loss', 'Test Loss', 'Training Accuracy',
           'Test Accuracy'], loc='upper right')
plt.savefig('roberta_loss_accuracy_curve.png')

# Save the fine-tuned RoBERTa model
roberta_model.save_pretrained('RoBERTa_model')

# Save the updated data to a new file
data.to_csv('final_dataset_with_predictions.csv', index=False)
