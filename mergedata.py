# merge into single file

dfTmp = pd.DataFrame()
df2 = pd.DataFrame()

for i in range(chunks):
  dfTmp = pd.read_csv('/data/stock data/tickers' + str(i) + '.csv')
  df2 = df2.append(dfTmp, ignore_index = True)

# 2021.05.10 - it appends to existing data - i need to overwrtite with new, get rid of old
# 2021.06.10 - i don't remember why i left the above comment, but imma leave it in, in case i remember - sorry, yo

# https://stackoverflow.com/questions/33469677/saving-a-file-or-overwriting-it-if-it-exists
# with open('calendar.txt', 'w') as cal: # file would be created if not exists
#     try:
#         cal.write(yourdata)
#     except:
#         return False
# return True

df2 = df2[df2['name'].notna()]
df2 = df2.reset_index(drop = True)

conditions = [
      (df2['marketCap'] > 200_000_000_000),
      (df2['marketCap'] >= 10_000_000_000) & (df2['marketCap'] < 2_000_00_000_000),
      (df2['marketCap'] >= 2_000_000_000) & (df2['marketCap'] < 100_00_000_000),
      (df2['marketCap'] >= 300_000_000) & (df2['marketCap'] < 200_000_000_000),
      (df2['marketCap'] >= 50_000_000) & (df2['marketCap'] < 300_000_000),
      (df2['marketCap'] < 50_000_000)
]
values = ['Mega', 'Large', 'Mid', 'Small', 'Micro', 'Nano']
df2['marketCapLabel'] = np.select(conditions, values)

# move columns around
columnTmp = df2['marketCapLabel']
df2.drop(labels = ['marketCapLabel'], axis = 1, inplace = True)
_ = df2.columns.get_loc('marketCap') + 1
df2.insert(_, 'marketCapLabel', columnTmp)

conditions = [
      (df2['fullTimeEmployees'] > 1_000_000),
      (df2['fullTimeEmployees'] >= 500_000) & (df2['fullTimeEmployees'] < 1_000_000),
      (df2['fullTimeEmployees'] >= 100_000) & (df2['fullTimeEmployees'] < 500_000),
      (df2['fullTimeEmployees'] >= 50_000) & (df2['fullTimeEmployees'] < 100_000),
      (df2['fullTimeEmployees'] >= 10_000) & (df2['fullTimeEmployees'] < 50_000),
      (df2['fullTimeEmployees'] >= 5_000) & (df2['fullTimeEmployees'] < 10_000),
      (df2['fullTimeEmployees'] >= 1_000) & (df2['fullTimeEmployees'] < 5_000),
      (df2['fullTimeEmployees'] >= 500) & (df2['fullTimeEmployees'] < 1_000),
      (df2['fullTimeEmployees'] >= 100) & (df2['fullTimeEmployees'] < 500),
      (df2['fullTimeEmployees'] >= 50) & (df2['fullTimeEmployees'] < 100),
      (df2['fullTimeEmployees'] < 50)
]
values = ['1M+', '500k+', '100k+', '50k+', '10k+', '5k+', '1k+', '500+', '100+', '50+', '1+']
df2['employeeLabel'] = np.select(conditions, values)

# move columns around
columnTmp = df2['employeeLabel']
df2.drop(labels = ['employeeLabel'], axis = 1, inplace = True)
_ = df2.columns.get_loc('fullTimeEmployees') + 1
df2.insert(_, 'employeeLabel', columnTmp)

df2.to_csv('/data/mergedData.csv', index = False)