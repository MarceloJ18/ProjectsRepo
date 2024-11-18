import pandas as pd
import numpy as np 
from pathlib import Path
from warnings import simplefilter
simplefilter("ignore")  # ignore warnings to clean up output cells

import matplotlib.pyplot as plt


# DATA #


results = pd.read_csv('data/results.csv', index_col = 'resultId')
drivers = pd.read_csv('data/drivers.csv', index_col = 'driverId')
circuits = pd.read_csv('data/circuits.csv', index_col = 'circuitId')
races = pd.read_csv('data/races.csv', index_col = 'raceId')

drivers.info()
circuits.info()
results.info()

results.head()
circuits.head()
drivers.head()

results.raceId.value_counts()

results[results.raceId == 800].T

drivers.loc[509]

# trying to forecast the future year ending results for HAMILTON

hami_results = results[results['driverId'] == 1].loc[:,['raceId','position', 'points', 'rank']]
hami_results  

hami_results.replace('\\N', np.nan, inplace=True)
np.where(hami_results.isna())[0]
hami_results = hami_results.dropna()


from sklearn.linear_model import LinearRegression


########## Simple Predictions ###########
'''# predicting position
# Training data
X = hami_results.loc[:, ['raceId']]  # features
y = hami_results.loc[:, 'position']  # target

# Train the model
model = LinearRegression()
model.fit(X, y)

# Store the fitted values as a time series with the same time index as
# the training data
y_pred = pd.Series(model.predict(X), index=X.index)


ax = y_pred.plot()
ax.set_title('Hamiltons finishing positions through his races')'''

'''# predicting points
# Training data
X = hami_results.loc[:, ['raceId']]  # features
y = hami_results.loc[:, 'points']  # target

# Train the model
model = LinearRegression()
model.fit(X, y)

# Store the fitted values as a time series with the same time index as
# the training data
y_pred = pd.Series(model.predict(X), index=X.index)


ax = y_pred.plot()
ax.set_title('Hamiltons points through his races')'''


######### Lag Variables #########
hami_results['Lag_1'] = hami_results['points'].shift(1)


X = hami_results.loc[:, ['Lag_1']]
X.dropna(inplace=True)  # drop missing values in the feature set
y = hami_results.loc[:, 'points']  # create the target
y, X = y.align(X, join='inner')  # drop corresponding values in target

model = LinearRegression()
model.fit(X, y)

y_pred = pd.Series(model.predict(X), index=X.index)

fig, ax = plt.subplots()
ax.plot(X['Lag_1'], y, '.', color='0.25')
ax.plot(X['Lag_1'], y_pred)
ax.set_aspect('equal')
ax.set_ylabel('points')
ax.set_xlabel('Lag_1')
ax.set_title('Lag Plot of points scored by Hamilton')

ax = y_pred.plot()