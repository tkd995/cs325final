import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
import torch
'''
ARIMA: Auto Regression, Moving Average, and Differencing for stationarity[I]
'''

data_path = "./berkshire_hathaway_data.csv"

data = pd.read_csv(data_path, index_col='Date', parse_dates=True).dropna()#default for drop na is nan rows

for key in data.columns:#loop for adding AMAs to training set, different windows for testing
	if key == "Date": continue#skip non-statistical data

	data["ama10-"+key] = data[key].rolling(window=10).mean()
	data["ama100-"+key] = data[key].rolling(window=100).mean()
	data["ama365-"+key] = data[key].rolling(window=365).mean()

#first difference, source: https://people.duke.edu/~rnau/411diff.htm
data.diff(axis=0, periods=2)

xtrain, xtest, ytrain, ytest = train_test_split(data[:-1], data["Open"][1:], test_size=.2)#idk what we are thinking of using as the expected result so I just picked this as a place holder

#load/define a model here
#test for evaluation
#output results