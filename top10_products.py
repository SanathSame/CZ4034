import pandas as pd

df = pd.read_csv('productReviews_soup.csv')


df['Product_ID'] = df['Product_ID'].astype(int)
top_10 = df.groupby(['Product_ID', 'Product_Name']
                    ).size().sort_values(ascending=False).head(10)
print(top_10)
