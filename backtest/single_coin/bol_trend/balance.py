import sys
sys.path.append('../..')
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use("Agg")
import pandas as pd

with open("balance_history.txt", "r") as f:
    data = f.read()

lines = data.split("\n")
records = [line.split(";") for line in lines]
records = [record for record in records if len(record) == 2]

df = pd.DataFrame(records, columns=["time", "balance"])
df["time"] = pd.to_datetime(df["time"], format="%d/%m/%Y %H:%M:%S")
df["balance"] = df["balance"].astype(float)

start_balance = 5021
final_balance = df["balance"].iloc[-1]
difference = final_balance - start_balance
percentage_difference = (difference / start_balance) * 100

# Commencer le graphique depuis cette date
start_time = pd.to_datetime("15/12/2022")
df_filtered = df[df["time"] >= start_time]

# Plot graph
plt.figure(figsize=(12, 8))
plt.plot(df_filtered["time"], df_filtered["balance"], '-', label='Balance')
plt.plot([df_filtered["time"].min(), df_filtered["time"].max()], [start_balance, start_balance], '--', color='gray', linewidth=2, label='Solde de départ')
plt.fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] < start_balance), color='red', alpha=0.2)
plt.fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] >= start_balance), color='green', alpha=0.2)

# Gain ou pertes affiché en haut à droite
if percentage_difference >= 0:
    color = "green"
    sign = '+'
else:
    color = "red"
    sign = '-'
plt.annotate(f"{final_balance:.2f}$\n({sign}{percentage_difference:.2f}%)",
             xy=(df_filtered["time"].max(), final_balance), xytext=(35, 35),
             textcoords='offset points', ha='center', va='bottom', color=color,
             bbox=dict(boxstyle='round,pad=0.4', fc='yellow', alpha=1),
             arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=-0.1'))

plt.legend()
plt.title("Balance history")

plt.savefig("balance.png", dpi = 300)
plt.show()