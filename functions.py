# functions

def printMetrics(a, ticker, printM = True):
  lenA = len(a) - 1

  try:
    summary = yf.Ticker(ticker).info['longBusinessSummary']
  except:
    summary = np.nan()
    print(f'No Summary for {ticker}')


  nowDate = a.iloc[-1]['Date'].strftime("%Y-%m-%d")
  firstDate = a.iloc[0]['Date'].strftime("%Y-%m-%d")
 
  firstClose = round(a['Adj Close'][0],2) 
  lastClose = round(a['Adj Close'][lenA],2)

  ymin = round(min(a['Adj Close']),2)
  ymax = round(max(a['Adj Close']),2)

  openP = a.iloc[0]['Adj Close']
  currP = a.iloc[-1]['Adj Close']
  changeD = currP - openP
  changeP = (currP/openP) * 100

  if (changeD > 0):
    uod = 'UP'
  else:
    uod = 'DOWN'
  
  metrics = {
      'ticker': ticker,
      'Summary': summary,
      'nowDate': nowDate,
      'firstDate': firstDate,
      'firstClose': firstClose,
      'lastClose': lastClose,
      'ymin': ymin,
      'ymax': ymax,
      'openP': openP,
      'currP': currP,
      'changeD': changeD,
      'changeP': changeP
  }

  if(printM):
    print(f'{ticker}')
    print(f'{firstDate: <5} \t {nowDate: ^5} \t ${changeD: ^5,.2f} \t {uod: >5}')
    print(f'$ {firstClose: <5,.2f} \t $ {lastClose: ^5,.2f} \t {changeP: >5,.2f}%')
    print(50 * '-') 
    print(f'{"Low": <10}{"High": >10}')
    print(f'{ymin: <10}{ymax: >10}')
    print(50 * '-')
    print()
    try:
      pprint.pprint(summary, width=120)
    except:
      pass

  return metrics

def printPctChange(ticker):
  """
  Input: ticker
  Output: Percent change of symbol
  : 1 Month
  : 3 Months
  : 6 Month
  : 1 Year
  : 3 Year
  """
  v = yf.download(ticker)
  output.clear()

  v0 = float(v[-1:]['Adj Close'])
  v1 = float(v[-30:-29]['Adj Close'])
  v3 = float(v[-90:-89]['Adj Close'])
  v6 = float(v[-180:-179]['Adj Close'])
  v12 = float(v[-360:-359]['Adj Close'])
  v36 = float(v[-1080:-1079]['Adj Close'])

  print('Percent Change')
  print()
  print(f'1 Month: {round(v0/v1,2)}')
  print(f'3 Month: {round(v0/v3,2)}')
  print(f'6 Month: {round(v0/v6,2)}')
  print('-' * 15)
  print(f'1 Year: {round(v0/v12,2)}')
  print(f'3 Year: {round(v0/v36,2)}')


def plotTickerSolo(ticker, w = 18, h = 5, printM = True):
  """
  Input single ticker symbol
  : printM = True (Default)
  :
  : - First traded price
  : - Current traded price
  : - Highest Price
  : - Lowest Price
  : - Business summary
  :
  : Plots Adj Close (blue) vs Volume (red)
  : 
  : 
  """
  a = yf.download(ticker, start=startDate, end=endDate).reset_index(drop=False)
  
  # print metrics? Default is true
  if(printM):
    metrics = printMetrics(a, ticker)
 
  fig, ax1 = plt.subplots(figsize=(w,h))
  ax2 = ax1.twinx()
 
  sns.lineplot(data=a, x='Date', y='Adj Close', color = 'red', ax = ax1, linewidth = 3);
  sns.lineplot(data=a, x='Date', y='Volume', color = 'blue', ax = ax2, alpha = 0.5, linewidth = 0.5);


def plotTickers(tickerList, h = 18, w = 5, metric = 1):
  """
  Input list of tickers to compare.
  : Metric options: High, Low, Close, Adj Close, Volume
  : Adj Close
  """
  listNA = []

  metricDict = {
      1: 'Adj Close',
      2: 'Pct Change',
      3: 'Pct Change2'
  }
  m = metricDict[metric]

  plt.subplots(figsize=(h,w))

  for i in range(len(tickerList)):
    ticker = tickerList[i]
    try:
      df1 = yf.download(ticker)[startDate:endDate].reset_index()
      df1['Pct Change'] = df1['Adj Close'] / df1['Adj Close'][0]
      df1['Pct Change2'] = df1['Adj Close'].pct_change()
      x = (max(df1['Date'])) + datedelta.datedelta(days=0)        # used in graphing
      y = df1[m][-1:]
      plt.annotate(s = ticker, xy = (x,y), fontsize=14)
      if (m == 2):
        plt.hlines(y = 1, xmin = df1['Date'][0], xmax = x, colors='grey', linestyles='dashed')
      
      sns.lineplot(data=df1, x='Date', y=m)
    except:
      listNA.append(ticker)
 
    output.clear()
  
  print(listNA, "is not defined")

def plotETF(ticker, h = 18, w = 5, base = False):
  """
  : Input single ETF ticker
  : Gets all holdings inside ET
  :
  : Top Graph       Plots Adj Close
  : Bottom Graph    Plots Pct Change
  :
  : if base = True, includes baseline ticker VTI
  """
  t = Ticker(ticker)

  listA = []

  try:
    holding = t.fund_holding_info[ticker]['holdings']
    for i in range(len(holding)):
      listA.append(holding[i]['symbol'])
  except:
    pass

  if(base):
    listA.append('VTI')

  plotTickers(listA, h, w, metric = 1)
  plotTickers(listA, h, w, metric = 2)
  
  plt.show();

def getETFHoldings(sSymbol):
  """
  Input: Symbol as a string.
  Output: Top 10 holdings, names, percentages held
  
  Example: >>>getETFHoldings('VOO')
  """
  dfH = pd.DataFrame()
  nameL = []
  percentL = []
  symbolL = []

  lenT = len(Ticker(sSymbol).fund_holding_info[sSymbol]['holdings'])

  for i in range(lenT):
    nameL.append(Ticker(sSymbol).fund_holding_info[sSymbol]['holdings'][i]['holdingName'])
    percentL.append(round(Ticker(sSymbol).fund_holding_info[sSymbol]['holdings'][i]['holdingPercent'],3)*100)
    symbolL.append(Ticker(sSymbol).fund_holding_info[sSymbol]['holdings'][i]['symbol'])

  data = {
      'name':nameL,
      'percent':percentL,
      'symbol':symbolL
      }

  dfH = pd.DataFrame(data = data)
  expRatio = round(Ticker(sSymbol).all_modules[sSymbol]['fundProfile']['feesExpensesInvestment']['annualReportExpenseRatio'] * 100,2)
  hold = Ticker(sSymbol).fund_holding_info[sSymbol]['equityHoldings']
  weight = Ticker(sSymbol).fund_holding_info[sSymbol]['sectorWeightings']

  print(f'Expense Ratio: {expRatio}')
  print()
  print(f'Holdings inside {sSymbol}')
  print()
  display(dfH.sort_values(by='percent', ascending=False).T)
  print(100 * '-')
  print('Holding Info')
  print(hold)
  print(100 * '-')
  print('Weight Info')
  print(weight)


def plotIntraday(tick, interval = '2m', h = 18, w = 6):
  """
  Accepts single ticker symbol
  Plots close vs volume
    
  Only functional while trading is in session
  """
  t = str(datetime.date.today())
  tom = str(datetime.date.today() + datetime.timedelta(days = 1))
  ticker = tick.upper()
  iD = yf.download(ticker, start = t, end = tom, interval = interval).reset_index()

  output.clear()

  fig, ax1 = plt.subplots(figsize=(h,w))
  ax2 = ax1.twinx()
  ax1.spines['right'].set_visible(False)
  ax2.spines['right'].set_visible(False)
  ax2.get_yaxis().set_visible(False)

  ac = iD.iloc[-1]['Adj Close']
  vol = iD.iloc[-2]['Volume']
  d = str(iD.iloc[0]['Datetime'])[:10]

  minP = iD['Adj Close'].min()
  maxP = iD['Adj Close'].max()
  variance = round(maxP - minP,2)

  openP = iD.iloc[0]['Adj Close']
  currP = iD.iloc[-1]['Adj Close']
  changeD = currP - openP
  changeP = 100 * (currP - openP)/openP

  if (changeD > 0):
    uod = 'UP'
  else:
    uod = 'DOWN'

  print(f'{ticker} \t\t {d}')
  print(f'{interval} intervals')
  print(30 * '-')
  print(f'Open: \t\t ${openP:.2f}')
  print(f'Current Price: \t ${ac:.2f}')
  print(f'Volume: \t {vol:,.0f}')
  print(30 * '-')
  print(f'High \t\t ${maxP:,.2f}')
  print(f'Low \t\t ${minP:,.2f}')
  print(f'Variance \t ${variance}')
  print(30 * '-')
  print(f'{uod} \t\t ${changeD:,.2f}')
  print(f'\t\t {changeP:,.2f}%')

  ax1.hlines(y = openP, xmin = iD.iloc[0]['Datetime'], xmax = iD.iloc[-1]['Datetime'], linestyles = 'dashed', alpha = 0.5)
  ax1.hlines(y = maxP, xmin = iD.iloc[0]['Datetime'], xmax = iD.iloc[-1]['Datetime'], linestyles = 'dashed', alpha = 0.5)

  ax1.text(x = iD.iloc[-1]['Datetime'], y = maxP, s = f'  H{maxP:.2f}', fontsize = 12)
  ax1.text(x = iD.iloc[-1]['Datetime'], y = ac, s = f'  C{ac:.2f}', fontsize = 12)
  ax1.text(x = iD.iloc[-1]['Datetime'], y = openP, s = f'  O{openP:.2f}', fontsize = 12)
  ax1.text(x = iD.iloc[-1]['Datetime'], y = minP, s = f'  L{minP:.2f}', fontsize = 12)

  sns.lineplot(data = iD, x = 'Datetime', y = 'Adj Close', ax = ax1, color = 'red', linewidth = 1);
  sns.lineplot(data = iD, x = 'Datetime', y = iD['Adj Close'].rolling(10).mean(), ax = ax1, color = 'orange', linewidth = 5);
  #sns.lineplot(data = iD, x = 'Datetime', y = 'Volume', ax = ax2, color = 'blue');
  sns.scatterplot(data = iD, x = 'Datetime', y = 'Volume', ax = ax2, color = 'blue', alpha = 0.5);
  plt.show();

def plotIntraday2(tick, interval = '2m', h = 18, w = 6):
  """
  Accepts single ticker symbol
  Plots close vs volume
    
  Only functional while trading is in session
  """
  t = str(datetime.date.today())
  tom = str(datetime.date.today() + datetime.timedelta(days = 1))
  ticker = tick.upper()
  iD = yf.download(ticker, start = t, end = tom, interval = interval).reset_index()

  # output.clear()

  # # fig, ax1 = plt.subplots(figsize=(h,w))
  # # ax2 = ax1.twinx()
  # # ax1.spines['right'].set_visible(False)
  # # ax2.spines['right'].set_visible(False)
  # # ax2.get_yaxis().set_visible(False)

  # ac = iD.iloc[-1]['Adj Close']
  # vol = iD.iloc[-2]['Volume']
  # d = str(iD.iloc[0]['Datetime'])[:10]

  # minP = iD['Adj Close'].min()
  # maxP = iD['Adj Close'].max()
  # variance = round(maxP - minP,2)

  # openP = iD.iloc[0]['Adj Close']
  # currP = iD.iloc[-1]['Adj Close']
  # changeD = currP - openP
  # changeP = 100 * (currP - openP)/openP

  # if (changeD > 0):
  #   uod = 'UP'
  # else:
  #   uod = 'DOWN'

  # print(f'{ticker} \t\t {d}')
  # print(f'{interval} intervals')
  # print(30 * '-')
  # print(f'Open: \t\t ${openP:.2f}')
  # print(f'Current Price: \t ${ac:.2f}')
  # print(f'Volume: \t {vol:,.0f}')
  # print(30 * '-')
  # print(f'High \t\t ${maxP:,.2f}')
  # print(f'Low \t\t ${minP:,.2f}')
  # print(f'Variance \t ${variance}')
  # print(30 * '-')
  # print(f'{uod} \t\t ${changeD:,.2f}')
  # print(f'\t\t {changeP:,.2f}%')

  # # ax1.hlines(y = minP, xmin = iD.iloc[0]['Datetime'], xmax = iD.iloc[-1]['Datetime'], linestyles = 'dashed', alpha = 0.5)
  # # ax1.hlines(y = maxP, xmin = iD.iloc[0]['Datetime'], xmax = iD.iloc[-1]['Datetime'], linestyles = 'dashed', alpha = 0.5)

  # # ax1.text(x = iD.iloc[-1]['Datetime'], y = maxP, s = f'  H{maxP:.2f}', fontsize = 12)
  # # ax1.text(x = iD.iloc[-1]['Datetime'], y = ac, s = f'  C{ac:.2f}', fontsize = 12)
  # # ax1.text(x = iD.iloc[-1]['Datetime'], y = openP, s = f'  O{openP:.2f}', fontsize = 12)
  # # ax1.text(x = iD.iloc[-1]['Datetime'], y = minP, s = f'  L{minP:.2f}', fontsize = 12)

  #px.lineplot(data = iD, x = 'Datetime', y = 'Volume', ax = ax2, color = 'blue');
  px.line(iD, 'Datetime', 'Adj Close')
  # plt.show();