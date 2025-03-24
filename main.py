import pandas as pd
import matplotlib.pyplot as plt


data_path = "./berkshire_hathaway_data.csv"

# Load data into a dataframe.
data = pd.read_csv(data_path)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)


## -- Visalize Raw Data -- ##

# # Plot
# plt.figure(figsize=(16, 10))

# # Plot Adj Close, Open, High, Low
# plt.subplot(2, 1, 1)
# plt.plot(data.index, data["Adj Close"], label="Adj Close", linewidth=1.2)
# plt.plot(data.index, data["Open"], label="Open", linestyle='--')
# plt.plot(data.index, data["High"], label="High", linestyle='--')
# plt.plot(data.index, data["Low"], label="Low", linestyle='--')
# plt.title("Original Price Data: Adj Close, Open, High, Low")
# plt.legend()
# plt.grid(True)

# # Plot Volume
# plt.subplot(2, 1, 2)
# plt.plot(data.index, data["Volume"], label="Volume", color='purple', alpha=0.6)
# plt.title("Trading Volume Over Time")
# plt.legend()
# plt.grid(True)

# plt.tight_layout()
# plt.show()


## -- Clean data -- ## 
clean_data = data.copy()

clean_data = clean_data.drop(columns=['Open', 'High', 'Low']) # Remove volitility and noise

# Clean meaningful features ##

clean_data['Daily Return'] = clean_data['Adj Close'].pct_change() # Day-to-Day porice change as %
clean_data['SMA_10'] = clean_data['Adj Close'].rolling(10).mean() # A simple moving average for 10 days (short term)
clean_data['SMA_50'] = clean_data['Adj Close'].rolling(50).mean() # A simple moving average for 50 days (long term)
clean_data['Volatility_10'] = clean_data['Daily Return'].rolling(10).std() # A way to measure risk by showing how the daily returns shift (short term)

# Target Column: Future Price (5-day lookahead)
clean_data['Future_Price'] = clean_data['Adj Close'].shift(-5)

clean_data.dropna(inplace=True) # Drop any incomplete rows



## -- Visualize Baseline Data -- ##

plt.figure(figsize=(16, 10))

# Adj Close with SMA
plt.subplot(2, 1, 1)
plt.plot(clean_data.index, clean_data["Adj Close"], label="Adj Close", linewidth=1.2)
plt.plot(clean_data.index, clean_data["SMA_10"], label="SMA 10", linestyle='--')
plt.plot(clean_data.index, clean_data["SMA_50"], label="SMA 50", linestyle='--')
plt.title("Adjusted Close Price with Moving Averages")
plt.legend()
plt.grid(True)

# Daily return and volatility
plt.subplot(2, 1, 2)
plt.plot(clean_data.index, clean_data["Daily Return"], label="Daily Return", alpha=0.6)
plt.plot(clean_data.index, clean_data["Volatility_10"], label="10-Day Volatility", color='orange')
plt.title("Daily Return and Volatility")
plt.legend()
plt.grid(True)

plt.show()


