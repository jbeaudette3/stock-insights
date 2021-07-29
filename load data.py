# load data from Drive to variable df
df = pd.DataFrame()

# load in merged file here
df = pd.read_csv('/data/mergedData.csv')

# create dataframes based on market cap size
dfMega = df[df['marketCapLabel'] == 'Mega']
dfLarge = df[df['marketCapLabel'] == 'Large']
dfMid = df[df['marketCapLabel'] == 'Mid']
dfSmall = df[df['marketCapLabel'] == 'Small']
dfMicro = df[df['marketCapLabel'] == 'Micro']
dfNano = df[df['marketCapLabel'] == 'Nano']
dfSP500 = df.sort_values(by='marketCap', ascending = False).head(500)

# load new ETFs, Stocks from Nasdaq
dfETF = pd.read_csv('data/etf data/dfETF2.csv')