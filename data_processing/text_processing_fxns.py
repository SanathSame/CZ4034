#DATA PROCESSING FOR THE CRAWLED DATA

#Imports
from nltk.corpus import stopwords
from cleantext import clean
import string
import re

#Processing Fxn 1 - Processes minute stuff
def processing(data):
    #remove new line characters
    data = re.sub('\s+', ' ', data)

    #remove emojis
    data = clean(data, no_emoji=True, no_punct=True, no_currency_symbols=True)

    #remove distracting single quotes
    data = str(re.sub("\'", "", data))

    #converting the text to lowercase
    data = data.lower()
    
    return data

#Processing Fxn 2 - Removes Punctuations
def remove_punctuation(data):
    ans = []
    for word in data.split():
        x = word.strip(string.punctuation)
        ans.append(x)

    #returns a list
    return ans

#Processing Fxn 3 - Removes stopwords
def remove_stopwords(data):
    #as the input is already a list
    review = data
    filtered_words = []

    for word in review:
        if word not in stopwords.words('english'):
            filtered_words.append(word)

    return filtered_words



