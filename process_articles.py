import pandas
import os

df = pandas.read_csv('data/articles/raw_analyst_ratings.csv')
df_2 = pandas.read_csv('data/articles/raw_partner_headlines.csv')

df = df.rename(columns={"Unnamed: 0": "index"})
df_2 = df_2.rename(columns={"Unnamed: 0": "index"})

if not os.path.exists('data/articles_processed'):
    os.makedirs('data/articles_processed')

df.to_csv('data/articles_processed/raw_analyst_ratings.csv', index=False)
df_2.to_csv('data/articles_processed/raw_partner_headlines.csv', index=False)