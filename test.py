from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
yf.pdr_override()

# Add stock names in the list to fetch data
tickers = ['^NSEI', 'RELIANCE.NS', 'PNB.NS', 'HINDPETRO.NS', 'BHARTIARTL.NS']

# date format = yyyy-mm-dd
start_date = "2017-01-01"
end_date = "2020-12-21"

files = []


def getData(ticker):
    print(ticker)
    data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
    files.append(ticker)
    SaveData(data, ticker)


def SaveData(df, filename):
    df.to_csv(
        '<YOUR PATH>/stock-data-yfinance-master/data/' + filename + '.csv')


for t in tickers:
    getData(t)

for i in range(0, 5): # Modify the range according to the number of stocks in the list
    df1 = pd.read_csv(
        '<YOUR PATH>/stock-data-yfinance-master/data/' + str(files[i]) + '.csv')
    # print(df1.head())
