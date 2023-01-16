import sys
sys.path.append('../../..')
import ccxt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines
#matplotlib.use("Agg")
import pandas as pd

def get_historical_from_db(exchange, symbol, timeframe, path="database/"):
    symbol = symbol.replace('/','-')
    df = pd.read_csv(filepath_or_buffer=path+str(exchange.name)+"/"+timeframe+"/"+symbol+".csv")
    df = df.set_index(df['date'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['date']
    return df

# Choix de la paire à trader et de la plage de temps des bougies
pair = "ETH/USDT"
tf = "1h"

# Chargement des données dans un dataframe depuis la base de donnée /database
# mise à jour à faire avec "node download_data.js"
df_ETH = get_historical_from_db(
    ccxt.binance(), 
    pair,
    tf,
    path="database/"
)

# read log file as a single string
with open("cronlog.log", "r") as f:
    log = f.read()

# split log into separate lines
lines = log.split("\n")

# create a DataFrame from the lines
df_bitget = pd.DataFrame({"line": lines})

# filter DataFrame to only include lines that contain the desired information
df_bitget = df_bitget[df_bitget["line"].str.contains("--- Start Time :") | df_bitget["line"].str.contains("USD balance :") | 
        df_bitget["line"].str.contains("Place Open Short" ) | df_bitget["line"].str.contains("Place Open Long") |
        df_bitget["line"].str.contains("Place Close Long") | df_bitget["line"].str.contains("Place Close Short")]

# Extract the desired information using string manipulation and regular expressions
df_bitget['time'] = df_bitget['line'].str.extract(r"--- Start Time : (.*?) ---")
df_bitget['balance'] = df_bitget['line'].str.extract(r"USD balance : (.*?) \$")
df_bitget['balance'] = df_bitget['balance'].shift(-1)
df_bitget[['position', 'direction', 'size', 'price']] = df_bitget['line'].str.extract(r"Place (.*?) (.*?) Market Order: (.*?) ETH/USDT at the price of (.*?)\$")
df_bitget[['position', 'direction', 'size', 'price']] = df_bitget[['position', 'direction', 'size', 'price']].shift(-2)

# drop the original line column
df_bitget.drop(columns=['line'], inplace=True)
df_bitget.dropna(how='all', inplace=True)

#df_bitget = df_bitget.append({'time': "12/01/2023 03:00:02", 'balance': 6400, 'position': "Open", 'direction': "Short", 'size': 5, 'price': 1400}, ignore_index=True)

df_bitget["time"] = pd.to_datetime(df_bitget["time"], format="%d/%m/%Y %H:%M:%S")
df_bitget["balance"] = df_bitget["balance"].astype(float)
df_bitget["size"] = df_bitget["size"].astype(float)
df_bitget["price"] = df_bitget["price"].astype(float)

start_balance = 5021
final_balance = df_bitget["balance"].iloc[-1]
difference = final_balance - start_balance
percentage_difference = (difference / start_balance) * 100

# Commencer le graphique depuis cette date
start_time = pd.to_datetime("12/15/2022")
df_filtered = df_bitget[df_bitget["time"] >= start_time]
df_ETH = df_ETH[df_ETH.index >= start_time]

# Plot graph
fig, ax_left = plt.subplots(figsize=(15, 20), nrows=2, ncols=1)

ax_left[0].title.set_text("Balance history")
ax_left[0].plot(df_filtered["time"], df_filtered["balance"], '-', label='Balance')
ax_left[0].plot([df_filtered["time"].min(), df_filtered["time"].max()], [start_balance, start_balance], '--', color='gray', linewidth=2, label='Solde de départ')
ax_left[0].fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] < start_balance), color='red', alpha=0.2)
ax_left[0].fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] >= start_balance), color='green', alpha=0.2)
ax_left[0].set_xlim(pd.Timestamp(start_time), df_filtered['time'].max())
ax_left[0].legend()

# Gain ou pertes affiché en haut à droite
if percentage_difference >= 0:
    color = "green"
    sign = '+'
else:
    color = "red"
    sign = '-'
ax_left[0].annotate(f"{final_balance:.2f}$\n({sign}{percentage_difference:.2f}%)",
             xy=(df_filtered["time"].max(), final_balance), xytext=(35, 35),
             textcoords='offset points', ha='center', va='bottom', color=color,
             bbox=dict(boxstyle='round,pad=0.4', fc='yellow', alpha=1),
             arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=-0.1'))

ax_left[1].title.set_text("Ethereum")
ax_left[1].plot(df_ETH["close"], '-', label='ETH')
ax_left[1].set_xlim(pd.Timestamp(start_time), df_filtered['time'].max())

# Open Long
df_filtered = df_bitget.query("position == 'Open' and direction == 'Long'")

for index,row in df_filtered.iterrows():
    annotation1 = ax_left[1].annotate(f"{row['size']}\n{row['price']}", xytext=(row['time'], row['price']-70),
                xy=(row['time'], row['price']),
                arrowprops=dict(color='green', arrowstyle='->', linewidth=2, shrinkA=5, shrinkB=5), fontsize = 8, color='green')

# Open Short
df_filtered = df_bitget.query("position == 'Open' and direction == 'Short'")

for index,row in df_filtered.iterrows():
    annotation2 = ax_left[1].annotate(f"{row['size']}\n{row['price']}", xytext=(row['time'], row['price']+50),
                xy=(row['time'], row['price']),
                arrowprops=dict(color='red', arrowstyle='->', linewidth=2, shrinkA=5, shrinkB=5), fontsize = 8, color='red')

# Close Position
df_filtered = df_bitget.query("position == 'Close'")

for index,row in df_filtered.iterrows():
    annotation3 = ax_left[1].annotate(f"{row['size']}\n{row['price']}", xytext=(row['time'], row['price']+50),
                xy=(row['time'], row['price']),
                arrowprops=dict(color='blue', arrowstyle='->', linewidth=2, shrinkA=5, shrinkB=5), fontsize = 8, color='blue')
    
#create proxy artist
proxy1 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='green', marker = 'o')
proxy2 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='red', marker = 'o')
proxy3 = matplotlib.lines.Line2D([0],[0], linestyle="none", c='blue', marker = 'o')

#create legend
ax_left[1].legend([proxy1, proxy2, proxy3], ['Open Long', 'Open Short', 'Close Position'])

plt.savefig("balance.png", dpi = 300)
plt.show()


