# 2021.07.26 - does the actual scraping
# 2021.07.27 - modified try/except block per Reddit comments
# Does the actual scraping

import datetime, datedelta
import yfinance as yf
import pandas as pd
import numpy as np

pd.set_option("display.max_rows", None)

v = input()
pathIn = '/data/stock list/tickers' + str(v) + '.csv'
pathOut = '/data/stock data/tickers' + str(v) + '.csv'

print(f'v: {v}')
print(f'File Path In: {pathIn}')
print(f'File Path Out: {pathOut}')

dfC = pd.read_csv(pathIn)

nameL = []
tickerL = []
betaL = []
enterpriseToEbitdaL = []
fullTimeEmployeesL = []
industryL = []
marketCapL = []
sectorL = []
volumeL = []
previousCloseL = []
bookValueL = []
priceToBookL = []
forwardPEL = []
pegRatioL = []
trailingPEL = []
summaryL = []

print(50 * '-')
print(f'{v}: Download starting...')

for i in range(len(dfC)):  
  print(f'{i} out of {len(dfC)} \t {i/len(dfC) * 100:.2f}%')
  #print(i, '\t', (round(i/len(dfC)*100,2)))

  ticker = dfC['0'][i]
  tickerL.append(ticker)

  try: fo = yf.Ticker(ticker).info
  except: fo = np.nan

  nameL.append(fo.get('longName', np.nan))
  betaL.append(fo.get('beta', np.nan))
  enterpriseToEbitdaL.append(fo.get('enterpriseToEbitda', np.nan))
  fullTimeEmployeesL.append(fo.get('fullTimeEmployees', np.nan))
  industryL.append(fo.get('industry', np.nan))
  marketCapL.append(fo.get('marketCap', np.nan))
  sectorL.append(fo.get('sector', np.nan))
  volumeL.append(fo.get('volume', np.nan))
  previousCloseL.append(fo.get('previousClose', np.nan))
  bookValueL.append(fo.get('bookValue', np.nan))
  priceToBookL.append(fo.get('priceToBook', np.nan))
  forwardPEL.append(fo.get('forwardPE', np.nan))
  pegRatioL.append(fo.get('pegRatio', np.nan))
  trailingPEL.append(fo.get('trailingPE', np.nan))
  summaryL.append(fo.get('summary', np.nan))


data = {
    'name': nameL,
    'ticker': tickerL,
    'beta': betaL,
    'enterpriseToEbitda': enterpriseToEbitdaL,
    'fullTimeEmployees': fullTimeEmployeesL,
    'industry': industryL,
    'marketCap': marketCapL,
    'sector': sectorL,
    'volume': volumeL,
    'previousClose': previousCloseL,
    'bookValue': bookValueL,
    'priceToBook': priceToBookL,
    'forwardPE': forwardPEL,
    'pegRatio': pegRatioL,
    'trailingPE': trailingPEL,
    'summary': summaryL
}

# DEBUGGING
# for key, values in data.items():
#     print(f'{len(values)} \t {key}')

dfA = pd.DataFrame()
dfA = pd.DataFrame(data)

dfA.to_csv(pathOut, index = False)

print(20 * '- ')
print(f'{v} - Done')
print(20 * '- ')