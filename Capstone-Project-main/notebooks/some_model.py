import pandas as pd
import numpy as np 
from pathlib import Path
from warnings import simplefilter
simplefilter("ignore")  # ignore warnings to clean up output cells
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense

#################### DATA ############################

data = pd.read_csv('data/data2022_2023.csv')
results = pd.read_csv('data/results.csv', index_col = 'resultId')
drivers = pd.read_csv('data/drivers.csv', index_col = 'driverId')
circuits = pd.read_csv('data/circuits.csv', index_col = 'circuitId')
races = pd.read_csv('data/races.csv', index_col = 'raceId')
stand = pd.read_csv('data/driver_standings.csv', index_col= 'driverStandingsId')

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
############################################################################################
########## Simple Predictions ###########
# predicting position
# Training data

'''X = hami_results.loc[:, ['raceId']]  # features
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

'''hami_results['Lag_1'] = hami_results['points'].shift(1)
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
ax = y_pred.plot()'''



###################################### CNN ##############################################

hami_results = hami_results.astype('float16')

selected_X_data = hami_results.iloc[:, [0, 2, 3]].values
selected_y_data = (hami_results.position).values.reshape(296, 1)

X_train = selected_X_data.reshape(-1, 3, 2)  
y_train = selected_y_data.reshape(-1, 2, 1)  


print(X_train.shape)
print(y_train.shape)

#model simple
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(3, 2)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mae')


model.fit(X_train, y_train, epochs=50)


data_input = data[['positionOrder', 'points', 'rank']]
yhat = model.predict(data_input, verbose=2)


########################################################################################

