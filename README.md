# CZ4034
Course Project for CZ4034 - Information Retrieval 


## Branch related Info

This branch contains the codes as well as data and model files for the first try of classifaticion using RNN - Flair Labels. 
The accuracy on Test Set is 80.4%, however, this model is heavily overfitting on the positive labels due to the class imbalance in the crawled dataset.

Hence, the next step would be to solve this - a posisble appraoch would be to remove duplicates (ie samples with the same semantic meaning) by using Text Similarity Score. --> This can maybe be an innovation in itself as it is Domain Specific (ie: reviews specific to skincare)
