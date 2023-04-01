pip install transformers datasets

from transformers import pipeline
from tqdm.notebook import tqdm
import pandas as pd

rw = pd.read_csv('balanced_review.csv')
classifier = pipeline("zero-shot-classification", device=0)#GPU

# Put reviews in a list
sequences = rw['Review'].to_list()

# Define the candidate labels 
candidate_labels = ["positive", "negative"]

# Set the hyppothesis template
hypothesis_template = "The sentiment of this review is {}."

# Prediction results
hf_prediction = classifier(sequences, candidate_labels, hypothesis_template=hypothesis_template)

# Save the output as a dataframe
hf_prediction = pd.DataFrame(hf_prediction)

# Take a look at the data
hf_prediction.head()

# The column for the predicted topic
hf_prediction['hf_prediction'] = hf_prediction['labels'].apply(lambda x: x[0])

# Map sentiment values
hf_prediction['hf_prediction'] = hf_prediction['hf_prediction'].map({'positive': 1, 'negative': 0})

# The column for the score of predicted topic
hf_prediction['hf_predicted_score'] = hf_prediction['scores'].apply(lambda x: x[0])

# The actual labels
hf_prediction['true_label'] = rw['flair_labels']

# Drop the columns that we do not need
hf_prediction = hf_prediction.drop(['labels', 'scores'], axis=1)

# Take a look at the data
hf_prediction.head()

# Compare Actual and Predicted
# Import accuracy_score to check performance
from sklearn.metrics import accuracy_score
accuracy_score(hf_prediction['hf_prediction'], hf_prediction['true_label'])
