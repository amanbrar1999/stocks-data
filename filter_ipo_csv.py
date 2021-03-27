import pandas

df = pandas.read_csv('data/IPODataFull.csv', usecols=['Symbol', 'Year', 'Month', 'Day', 'highDay0', 'openDay0', 'lowDay0', 'volumeDay0'])

df.to_csv('data/IPODataProcessed.csv', index=False)