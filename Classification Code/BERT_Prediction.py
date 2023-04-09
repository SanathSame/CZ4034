import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report
import tensorflow as tf
import time

# Load data
data = pd.read_csv('balanced_data.csv')

reviews, targets = data['Review'], data['flair_labels']

# Load the pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertForSequenceClassification.from_pretrained('BERT_model_0.83')

# Tokenize the test data
test_encodings = tokenizer(reviews.tolist(), truncation=True, padding=True)

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    targets
))

start = time.time()
# Use the loaded model for prediction
bert_predictions = bert_model.predict(
    test_dataset.batch(16)).logits.argmax(axis=-1)
end = time.time()

# Write the BERT predictions to Column I of the test data
data.loc[reviews.index, 'BERT'] = bert_predictions

# Calculate and display the accuracy of the BERT model
bert_accuracy = accuracy_score(targets, bert_predictions)
print(f'BERT Accuracy: {bert_accuracy:.2f}')

# Display the classification report for the BERT model
print('BERT Classification Report:')
print(classification_report(targets, bert_predictions))

# Save the updated data to a new file
data.to_csv('BERT.csv', index=False)
total_minutes = (end - start)/60
total_hours = total_minutes/60
if (total_hours < 1):
    print("Time taken: " + str(total_minutes) + " minutes")
else:
    print("Time taken: " + str(total_hours) + " hours")
