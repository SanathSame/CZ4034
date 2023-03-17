# RNN Try 1 - Flair Labels

### General Info

This branch contains the codes as well as data and model files for the first try of classifaticion using RNN - Flair Labels. 
The accuracy on Test Set is 80.4%, however, this model is heavily overfitting on the positive labels due to the class imbalance in the crawled dataset.

Hence, the next step would be to solve this - a posisble appraoch would be to remove duplicates (ie samples with the same semantic meaning) by using Text Similarity Score. --> This can maybe be an innovation in itself as it is Domain Specific (ie: reviews specific to skincare)

### Processing

The code in the data_processing folder contains the codes for data processing of the crawled reviews (beautiful soup):

1. sampling_crawled_reviews_5k.py - contains the code to remove non english samples and samples with emoji and samples 5000 rows randomly
2. text_processing_fxns.py - contains the helper functions to clean the text
3. data_processing.py - actual cleaning of the 5k samples (df) takes place 
4. Generate_Flair_Labels.ipynb - code to generate flair labels -> NOTE: This was run on google colab due to Flair installation on local machine

### Training

Contains the following files:

1. Training_RNN.ipynb - contains codes to convert (text -> numpy.array -> tokenization -> sequences -> padded_sequences) as well as the RNN model building, training and evaluation
2. RNN_Try1.h5 - saved model
3. Loss and Accuracy Curves of the first try
4. cleaned_processed_flair_labels.csv - the dataset to be loaded and trained on
5. RNN_try1_history.txt - contains the history dictionary of the RNN Try 1 training in training_RNN.ipynb saved as a text file
