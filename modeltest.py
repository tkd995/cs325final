import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
import sklearn

import torch
'''
ARIMA: Auto Regression, Moving Average, and Differencing for stationarity[I]
'''
def create_lagged_features(data, lags):
    lagged_data = []
    for i in range(lags, len(data)):
        lagged_data.append(data[i-lags:i].values)
    return np.array(lagged_data)

data_path = "./berkshire_hathaway_data.csv"
d = pd.read_csv(data_path, header  = 0, index_col = 0, parse_dates=True)#.dropna()#default for drop na is nan rows
d.index = pd.DatetimeIndex(d.index).to_period('M')
parameter = 100

for key in d.columns:#loop for adding AMAs to training set, different windows for testing
	if key == "Date": continue#skip non-statistical data

	d["ama10-"+key] = d[key].rolling(window=10).mean()
	d["ama100-"+key] = d[key].rolling(window=100).mean()
	d["ama365-"+key] = d[key].rolling(window=365).mean()


#first differencing, can go further, source: https://people.duke.edu/~rnau/411diff.htm
d.diff(axis=0, periods=2)

print(d.shape)
d.to_csv("./mod.csv")

xtrain, xtest, ytrain, ytest = train_test_split(d[:-1], d["Open"][1:], test_size=.2)#idk what we are thinking of using as the expected result so I just picked this as a place holder

xtrain = create_lagged_features(xtrain, parameter)
ytrain = ytrain[parameter:]

xtest = create_lagged_features(xtest, parameter)
ytest = ytest[parameter:]


scaler = sklearn.preprocessing.MinMaxScaler()
scaled_ytrain = scaler.fit_transform(pd.DataFrame(ytrain))
scaled_ytest = scaler.fit_transform(pd.DataFrame(ytest))

xtraintensor = torch.tensor(xtrain, dtype=torch.float32)
ytraintensor = torch.tensor(scaled_ytrain, dtype=torch.float32)

xtesttensor = torch.tensor(xtest, dtype=torch.float32)
ytesttensor = torch.tensor(scaled_ytest, dtype=torch.float32)

lstm = torch.nn.LSTM(xtraintensor.shape[2], 64, 1)
output = torch.nn.Linear(64, 1)

#hyperparams
epochs = 100
#batchSize = 1
learningRate = .001

loss = torch.nn.MSELoss()
optimizer = torch.optim.Adam(lstm.parameters(), lr=learningRate)

for e in range(epochs):
	lstm.train()
	optimizer.zero_grad()

	lo, _ = lstm(xtraintensor)

	o = output(lo[:, -1, :])#might need to be 2
	l = loss(o.squeeze(), ytraintensor)

	optimizer.zero_grad()
	l.backward()
	optimizer.step()

lstm.eval()
with torch.no_grad():
	op, _ = lstm(xtesttensor)
	pred = output(po[:,-1,:]).squeeze().numpy()
	actual = ytesttensor.numpy()

	#generate results

#output results
