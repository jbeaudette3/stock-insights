# download tickers, place into separate files for scraping

dfAll = pd.read_csv('http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt', sep='|')

# filter out just the stocks
dfStocks = dfAll[(dfAll['ETF'] == 'N') & (dfAll['Nasdaq Traded'] == 'Y')]

# arbitrary number of chunks
chunks = 20

x = dfStocks['Symbol'].to_list()
l = np.array_split(numpy.array(x), chunks)

for i in range(len(l)):
  pd.DataFrame(l[i]).to_csv('/data/tickers' + str(i) + '.csv', index=False)