import pandas
import numpy as np

years = ['2014', '2015', '2016', '2017', '2018']
df = pandas.DataFrame(columns=['ticker', 'Year', 'Revenue', 'Revenue Growth', 'Cost of Revenue', 'Gross Profit', 'SG&A Expense', 'Operating Expenses', 'Operating Income', 'Interest Expense'])
for year in years:
    df_tmp = pandas.read_csv('data/financial_data/{}_Financial_Data.csv'.format(year), usecols=['Unnamed: 0', 'Revenue', 'Revenue Growth', 'Cost of Revenue', 'Gross Profit', 'SG&A Expense', 'Operating Expenses', 'Operating Income', 'Interest Expense'])
    df_tmp = df_tmp.rename(columns={"Unnamed: 0": "ticker"})
    df_tmp['Year'] = year
    print(df_tmp)
    df = pandas.concat([df,df_tmp])
    
df.to_csv('data/financial_data_processed/All_Financial_Data.csv', index=False)