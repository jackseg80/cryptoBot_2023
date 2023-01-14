import sys
sys.path.append('../..')
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use("Agg")
import pandas as pd

# Open file in read mode
with open("balance_history.txt", "r") as f:
    data = f.read()

# Split data into lines
lines = data.split("\n")
records = [line.split(";") for line in lines]

# Filter records that have the correct number of columns
records = [record for record in records if len(record) == 2]

df = pd.DataFrame(records, columns=["time", "balance"])

# Convert "time" column to datetime and "balance" column to float
df["time"] = pd.to_datetime(df["time"], format="%d/%m/%Y %H:%M:%S")
df["balance"] = df["balance"].astype(float)

# Calculate final balance and difference with 5021
start_balance = 5021
final_balance = df["balance"].iloc[-1]
difference = final_balance - start_balance
percentage_difference = (difference / start_balance) * 100

# Filter data from specified start time
start_time = pd.to_datetime("15/12/2022")
df_filtered = df[df["time"] >= start_time]

# Plot graph
plt.figure(figsize=(12, 8))
plt.plot(df_filtered["time"], df_filtered["balance"], '-', label='Balance')
plt.plot([df_filtered["time"].min(), df_filtered["time"].max()], [start_balance, start_balance], '--', color='gray', linewidth=2, label='Solde de départ')
plt.fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] < start_balance), color='red', alpha=0.2)
plt.fill_between(df_filtered["time"], df_filtered["balance"], start_balance, where=(df_filtered["balance"] >= start_balance), color='green', alpha=0.2)


# Add text to graph
if percentage_difference >= 0:
    color = "green"
else:
    color = "red"
plt.text(df_filtered["time"].max(), final_balance, f"{final_balance:.2f}\n ({percentage_difference:.2f}%)", ha='right', va='center', color=color)

# Add legend and title
plt.legend()
plt.title("Balance history")

# Show graph
plt.savefig("balance.png", dpi = 300)

plt.show()