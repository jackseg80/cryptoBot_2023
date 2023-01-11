import sys
sys.path.append('../..')
import matplotlib.pyplot as plt
import pandas as pd

# Open file in read mode
with open("balance_history.txt", "r") as f:
    data = f.read()

# Split data into lines
lines = data.split("\n")

# Split each line into time and balance
records = [line.split(";") for line in lines]

# Filter records that have the correct number of columns
records = [record for record in records if len(record) == 2]

# Create dataframe from filtered records
df = pd.DataFrame(records, columns=["time", "balance"])

# Convert "time" column to datetime and "balance" column to float
df["time"] = pd.to_datetime(df["time"])
df["balance"] = df["balance"].astype(float)

# Calculate final balance and difference with 5000
final_balance = df["balance"].iloc[-1]
difference = final_balance - 5021

# Calculate percentage difference
percentage_difference = (difference / 5021) * 100

# Filter data from specified start time
start_time = pd.to_datetime("14/12/2022 12:00")
df_filtered = df[df["time"] >= start_time]

# Plot graph
plt.plot(df_filtered["time"], df_filtered["balance"], '-', label='Balance')
plt.plot([df_filtered["time"].min(), df_filtered["time"].max()], [5021, 5021], '--', color='gray', label='Solde départ')

# Add text to graph
if percentage_difference >= 0:
    color = "green"
else:
    color = "red"
plt.text(df_filtered["time"].max(), final_balance, f"{final_balance:.2f} ({percentage_difference:.2f}%)", ha='right', va='center', color=color)

# Add legend and title
plt.legend()
plt.title("Balance history")

# Show graph
plt.show()
