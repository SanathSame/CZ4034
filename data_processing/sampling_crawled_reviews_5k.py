# # Sampling Subset - Crawled Dataset (Beautiful Soup)
# 
# Involve just removing Null Values and choosing 5000 rows randomly.


from langdetect import detect
import pandas as pd
import re

dataset = pd.read_csv("/Users/sankeerthana/Documents/NTU/YEAR_4/SEM_2/CZ4034/IR-Sentiment-Analysis/IR-Sentiment-Analysis/skincare_dataset/clean_crawled_reviews_5k.csv")
#dataset = pd.read_csv('/Users/sankeerthana/Documents/NTU/YEAR_4/SEM_2/CZ4034/IR-Sentiment-Analysis/IR-Sentiment-Analysis/skincare_dataset/productReviews_soup.csv')
dataset.head()

dataset.shape #62460

print("Number of Null Values:")
print(f"Review Title: {dataset['Review_Title'].isna().sum()}")
print(f"Review : {dataset['Review'].isna().sum()}")


# The crawled dataset has 62460 rows and 5 columns out of which 5256 rows have null values.

#dataset.drop(['Product_Name', 'Reviewer', 'Product_ID'], axis=1, inplace=True)
dataset.dropna(inplace=True)


print("Number of Null Values:")
print(f"Review Title: {dataset['Review_Title'].isna().sum()}")
print(f"Review : {dataset['Review'].isna().sum()}")

non_eng = []
def detect_lang():
    for row in dataset.itertuples():
        try:
            lang = detect(row.Review)
            if lang != 'en':
                non_eng.append(row.Index)
                print(f"{row.Review} ====> {lang}")
                ans = input("Should this review be removed?")
                if ans == "y":
                    dataset.drop([row.Index], axis='index', inplace=True)
                    print("INFO: Review Removed!")
                else:
                    pass

            if row.Review == "N/A":
                dataset.drop([row.Index], axis='index', inplace=True)
                print("Removed N/A")
        except:
            dataset.drop([row.Index], axis='index', inplace=True) #index=753


print(len(dataset)) #56960

sampled_df = dataset.sample(n=5000)
sampled_df.to_csv('/Users/sankeerthana/Documents/NTU/YEAR_4/SEM_2/CZ4034/IR-Sentiment-Analysis/IR-Sentiment-Analysis/skincare_dataset/clean_crawled_reviews_5k.csv')

