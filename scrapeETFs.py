# -*- coding: utf-8 -*-

# scrape etf info
# takes ~ 30 minutes

from yahooquery import Ticker
import pandas as pd
import numpy as np


dfTest = pd.read_csv('http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt', sep='|')
dfETF = dfTest[dfTest['ETF'] == 'Y']

namesL = dfETF['Security Name'].to_list()
etfSymbolL = dfETF['Symbol'].to_list()

categoryL = []
expRatioL = []
summaryL = []
assetsL = []
prevCloseL = []
twoHDAvgL = []
betaL = []
ytdReturnL = []

l = int(len(etfSymbolL))

for i in range(l):
  e = etfSymbolL[i]
  et = Ticker(e).all_modules[e]

  if(i%10 == 0):
    print(f'{i} out of {l}')
    print(f'{round(i/l,2)}')
    
  categoryL.append(et.get('defaultKeyStatistics', np.nan).get('category', np.nan))
  expRatioL.append(round(et.get('fundProfile', np.nan).get('feesExpensesInvestment', np.nan).get('annualReportExpenseRatio', np.nan) * 100, 3))
  summaryL.append(et.get('assetProfile', np.nan).get('longBusinessSummary', np.nan))
  assetsL.append(et.get('summaryDetail', np.nan).get('totalAssets', np.nan))
  prevCloseL.append(et.get('summaryDetail', np.nan).get('previousClose', np.nan))
  twoHDAvgL.append(et.get('summaryDetail', np.nan).get('twoHundredDayAverage', np.nan))
  betaL.append(et.get('defaultKeyStatistics', np.nan).get('beta3Year', np.nan))
  ytdReturnL.append(et.get('defaultKeyStatistics', np.nan).get('ytdReturn', np.nan))
  
  
namesL = namesL[:l]
etfSymbolL = etfSymbolL[:l]
expRatioL = expRatioL[:l]
categoryL = categoryL[:l]
summaryL = summaryL[:l]
assetsL = assetsL[:l]
prevCloseL = prevCloseL[:l]
twoHDAvgL = twoHDAvgL[:l]
betaL = betaL[:l]
ytdReturnL = ytdReturnL[:l]

# DEBUGGING
# print(f'{len(namesL)} \t namesL')
# print(f'{len(etfSymbolL)} \t etfSymbol')
# print(f'{len(expRatioL)} \t expRatioL')
# print(f'{len(categoryL)} \t categoryL')
# print(f'{len(summaryL)} \t summaryL')
# print(f'{len(assetsL)} \t assetsL')
# print(f'{len(prevCloseL)} \t prevCloseL')
# print(f'{len(twoHDAvgL)} \t twoHDAvgL')
# print(f'{len(betaL)} \t betaL')
# print(f'{len(ytdReturnL)} \t ytdReturnL')

data = {
    'Names': namesL,
    'Symbol': etfSymbolL,
    'Category': categoryL,
    'Expense Ratio': expRatioL,
    'Beta3Year': betaL,
    'Assets': assetsL,
    'Previous Close': prevCloseL,
    'YtdReturn': ytdReturnL,
    '200 Day Avg': twoHDAvgL,
    'Summary': summaryL
}

dfETF2 = pd.DataFrame()
dfETF2 = pd.DataFrame(data)

dfETF2.to_csv('/data/etf data/dfETF2.csv', index=False)

print(25 * '-')
print('Done')
print(25 * '-')