import fastf1.legacy
import fastf1 as ff1
import fastf1.legacy
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

colormap = mpl.cm.plasma


def draw_f1_circuit(circuit, year=2023):
    session = fastf1.get_session(year, circuit, 'R')
    session.load()
    circuit_info = session.get_circuit_info()
    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()
    fig, ax = plt.subplots(figsize=(10, 5))

    track = pos.loc[:, ('X', 'Y')].to_numpy()

    track_angle = circuit_info.rotation / 180 * np.pi

    offset_vector = [500, 0]

    def rotate(xy, *, angle):
        rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                            [-np.sin(angle), np.cos(angle)]])
        return np.matmul(xy, rot_mat)

    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1], color='tab:orange')

    # Iterate over all corners.
    for _, corner in circuit_info.corners.iterrows():
        # Create a string from corner number and letter
        txt = f"{corner['Number']}{corner['Letter']}"

        # Convert the angle from degrees to radian.
        offset_angle = corner['Angle'] / 180 * np.pi

        # Rotate the offset vector so that it points sideways from the track.
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        # Add the offset to the position of the corner
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        # Rotate the text position equivalently to the rest of the track map
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        # Rotate the center of the corner equivalently to the rest of the track map
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        # Draw a circle next to the track.
        plt.scatter(text_x, text_y, color='yellow', s=140)

        # Draw a line from the track to this circle.
        plt.plot([track_x, text_x], [track_y, text_y], color='yellow')

        # Finally, print the corner number inside the circle.
        plt.text(text_x, text_y, txt,
                 va='center_baseline', ha='center', size='small', color='black')

        # Add title with session name
        plt.title(session.event['EventName'])

        # hide axis
        ax.axis('off')


def compare_track_dominance(race_name, driver_surname1, driver_surname2, year=2023, session='Q'):
    session_event = ff1.get_session(year, race_name, session)
    session_event.load()

    driver01 = session_event.results[session_event.results['LastName'] == driver_surname1]['Abbreviation'].values[0]
    driver02 = session_event.results[session_event.results['LastName'] == driver_surname2]['Abbreviation'].values[0]

    drivers = [driver01, driver02]
    compare_drivers = session_event.laps[session_event.laps['Driver'].isin(drivers)]

    fastest_lap_driver01 = session_event.laps.pick_driver(driver01).pick_fastest()
    fastest_lap_driver02 = session_event.laps.pick_driver(driver02).pick_fastest()

    telemetry_driver01 = fastest_lap_driver01.get_telemetry().add_distance()
    telemetry_driver02 = fastest_lap_driver02.get_telemetry().add_distance()

    telemetry_driver01['Driver'] = driver01
    telemetry_driver02['Driver'] = driver02
    # telemetry_drivers = pd.DataFrame(telemetry_driver01).append(pd.DataFrame(telemetry_driver02))
    telemetry_drivers = pd.concat([telemetry_driver01, telemetry_driver02])

    # We want 25 mini-sectors (this can be adjusted up and down)
    num_minisectors = 7 * 3

    # Grab the maximum value of distance that is known in the telemetry
    total_distance = total_distance = max(telemetry_drivers['Distance'])

    # Generate equally sized mini-sectors
    minisector_length = total_distance / num_minisectors

    # Initiate minisector variable, with 0 (meters) as a starting point.
    minisectors = [0]

    # Add multiples of minisector_length to the minisectors
    for i in range(0, (num_minisectors - 1)):
        minisectors.append(minisector_length * (i + 1))

    telemetry_drivers['Minisector'] = telemetry_drivers['Distance'].apply(
        lambda dist: (
            int((dist // minisector_length) + 1)
        )
    )

    average_speed = telemetry_drivers.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

    # Select the driver with the highest average speed
    fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]

    # Get rid of the speed column and rename the driver column
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

    # Join the fastest driver per minisector with the full telemetry
    telemetry_drivers = telemetry_drivers.merge(fastest_driver, on=['Minisector'])

    # Order the data by distance to make matploblib does not get confused
    telemetry_drivers = telemetry_drivers.sort_values(by=['Distance'])

    # Convert driver name to integer
    telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == driver01, 'Fastest_driver_int'] = 1
    telemetry_drivers.loc[telemetry_drivers['Fastest_driver'] == driver02, 'Fastest_driver_int'] = 2

    x = np.array(telemetry_drivers['X'].values)
    y = np.array(telemetry_drivers['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fastest_driver_array = telemetry_drivers['Fastest_driver_int'].to_numpy().astype(float)

    cmap = plt.get_cmap('spring', 2)
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    plt.rcParams['figure.figsize'] = [12, 6]

    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    cbar = plt.colorbar(mappable=lc_comp, label='Driver', boundaries=np.arange(1, 4))
    cbar.set_ticks(np.arange(1.5, 3.5))
    cbar.set_ticklabels([driver01, driver02])
    # Store the fastest lap time of each driver. Use only minutes and seconds.

    title_color = 'silver'  # '#6441a5'
    plt.title(
        f"{year} {race_name} | {session} {driver_surname1} ({fastest_lap_driver01['LapTime']}) vs {driver_surname2} ({fastest_lap_driver02['LapTime']})",
        color=title_color, fontsize=16)

    plt.show()


# Gather data from FastF1
def get_from_fastf1(year, gp, session):
    # To get any data, you need to specify a session. This can be done by using the get_session method.
    # Session can be one of 'FP1', 'FP2', 'FP3', 'Q', 'R'.
    # GP can be the name of the GP, e.g. 'Monaco' or 'Monza', or the name of the circuit, e.g. 'Baku City Circuit'.
    # It can also be the name of the country, e.g. 'Italy' or 'Azerbaijan', but some countries have multiple GPs.
    session = ff1.get_session(year, gp, session)
    session.load()


import plotly.express as px
from plotly.io import show

from fastf1.ergast import Ergast
def plot_driver_standings_by_year(year):
    """
    Plot the driver standings of a given year. The data is obtained from Ergast. Be careful of the Ergast API limit.

    Parameters
    ----------
    year : int
        The year of the season.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        A figure object.
    """

    ergast = Ergast()
    races = ergast.get_race_schedule(year)  # Races in year 2022
    results = []

    # For each race in the season
    for rnd, race in races['raceName'].items():

        # Get results. Note that we use the round no. + 1, because the round no.
        # starts from one (1) instead of zero (0)
        temp = ergast.get_race_results(season=year, round=rnd + 1)
        temp = temp.content[0]

        # If there is a sprint, get the results as well
        sprint = ergast.get_sprint_results(season=year, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
            # Add sprint points and race points to get the total
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        # Add round no. and grand prix name
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
        results.append(temp)

    # Append all races into a single dataframe
    results = pd.concat(results)
    races = results['race'].drop_duplicates()

    results = results.pivot(index='driverCode', columns='round', values='points')
    # Here we have a 22-by-22 matrix (22 races and 22 drivers, incl. DEV and HUL)

    # Rank the drivers by their total points
    results['total_points'] = results.sum(axis=1)
    results = results.sort_values(by='total_points', ascending=False)
    results.drop(columns='total_points', inplace=True)

    # Use race name, instead of round no., as column names
    results.columns = races

    fig = px.imshow(
        results,
        text_auto=True,
        aspect='auto',  # Automatically adjust the aspect ratio
        color_continuous_scale=[[0,    'rgb(198, 219, 239)'],  # Blue scale
                                [0.25, 'rgb(107, 174, 214)'],
                                [0.5,  'rgb(33,  113, 181)'],
                                [0.75, 'rgb(8,   81,  156)'],
                                [1,    'rgb(8,   48,  107)']],
        labels={'x': 'Race',
                'y': 'Driver',
                'color': 'Points'}       # Change hover texts
    )
    fig.update_xaxes(title_text='')      # Remove axis titles
    fig.update_yaxes(title_text='')
    fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                     showline=False,
                     tickson='boundaries')              # Show horizontal grid only
    fig.update_xaxes(showgrid=False, showline=False)    # And remove vertical grid
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')     # White background
    fig.update_layout(coloraxis_showscale=False)        # Remove legend
    fig.update_layout(xaxis=dict(side='top'))           # x-axis on top
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
    show(fig)


from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Might use load_tools instead
def access_wikipedia_api(subject):
    """
    Access the Wikipedia API to get a summary of a given subject given by the user in their query.

    Parameters
    ----------
    subject : str
        The subject of the query.

    Returns
    -------
    summary : str
        The summary of the subject.
    """
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    summary = wikipedia.run(subject)
    return summary


import pandas as pd
from itertools import combinations


def create_combinations(data, i, defined_keys=None):
    available_keys = data[-1].keys()
    remaining_keys = available_keys - (defined_keys or set())
    defined_keys_list = list(defined_keys) if defined_keys else []

    data_combinations = combinations(remaining_keys, i - len(defined_keys_list))
    data_combinations = [defined_keys_list + list(data_combination) for data_combination in data_combinations]

    return data_combinations


def optimize_team(current_round, num_previous_race=1, max_capacity=100, drivers_defined=None, constructors_defined=None):
    """
    Gives the best possible combination of drivers and constructors.

    Parameters
    ----------
    current_round : int
        The current round of the season.

    num_previous_race : int, optional
        How many races to consider (at least 1). The default is 1. If 0 will give error.

    max_capacity : int, optional
        The maximum capacity (budget) of the team. The default is 100.

    drivers_defined : list, optional
        A list of drivers to be included in the team. The default is None.

    constructors_defined : list, optional
        A list of constructors to be included in the team. The default is None.
    """
    # Import data from pickle files
    drivers_dict = pd.read_pickle('drivers_dict.pkl')
    constructors_dict = pd.read_pickle('constructors_dict.pkl')
    # Initialize variables
    best_value = 0
    best_team = None

    # Collect data from previous races
    drivers_data = [drivers_dict[i] for i in range(current_round - num_previous_race + 1, current_round + 1)]
    constructors_data = [constructors_dict[i] for i in range(current_round - num_previous_race + 1, current_round + 1)]

    # Generate combinations of 5 drivers
    driver_combinations = create_combinations(drivers_data, 5, drivers_defined)

    # Iterate through all combinations
    for drivers_combo in driver_combinations:
        # Generate combinations of 2 constructors for each driver combination iteration
        constructor_combinations = create_combinations(constructors_data, 2, constructors_defined)

        for constructors_combo in constructor_combinations:
            # Calculate total weight for the combination
            total_weight = sum(drivers_data[-1][driver][0] for driver in drivers_combo) + sum(constructors_data[-1][constructor][0] for constructor in constructors_combo)

            # Check if within capacity limit
            if total_weight > max_capacity:
                continue

            # Initialize total value
            total_value = 0

            for i in range(num_previous_race):
                # Calculate mean value for each driver and constructor
                driver_value_mean = sum(drivers_data[i][driver][1] for driver in drivers_combo) / num_previous_race
                constructor_value_mean = sum(constructors_data[i][constructor][1] for constructor in constructors_combo) / num_previous_race

                # Calculate total value for the combination
                total_value += driver_value_mean + constructor_value_mean

            # Update best team
            if total_value > best_value:
                best_value = total_value
                best_team = (list(drivers_combo), list(constructors_combo))

    return best_value, best_team

### Prediction model all functions
# DATA TYPES
def datatype_distinction(data):
    '''
    Distinguishes between the numerical and categorical columns in a DataFrame.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame.

    Returns:
    --------
    numerical : pandas.DataFrame
        DataFrame containing only numerical columns.

    categorical : pandas.DataFrame
        DataFrame containing only categorical columns.
    '''
    # Select numerical columns using select_dtypes with np.number
    numerical = data.select_dtypes(include=np.number).copy()

    # Select categorical columns by excluding numerical types
    categorical = data.select_dtypes(exclude=np.number).copy()

    return numerical, categorical


# DATA TRANSFORMATION
def transformation(technique, data, column_transformer=False):
    '''
    Applies the specified transformation technique to the DataFrame.

    Parameters:
    -----------
    technique : object
        The transformation technique (e.g., from Scikit-learn) to be applied.

    data : pandas.DataFrame
        The input DataFrame to be transformed.

    column_transformer : bool, optional (default=False)
        Flag to indicate if a column transformer is used for custom column names.

    Returns:
    --------
    data_transformed : pandas.DataFrame
        Transformed DataFrame.

    Notes:
    ------
    - If column_transformer is False, the columns in the transformed DataFrame
      will retain the original column names.
    - If column_transformer is True, the method assumes that technique has a
      get_feature_names_out() method and uses it to get feature names for the
      transformed data, otherwise retains the original column names.
    '''
    # Apply the specified transformation technique to the data
    data_transformed = technique.transform(data)

    # Create a DataFrame from the transformed data
    data_transformed = pd.DataFrame(
        data_transformed,
        index=data.index,
        columns=technique.get_feature_names_out() if column_transformer else data.columns
    )

    return data_transformed


def data_transform(technique, X_train, X_val=None, column_transformer=False):
    '''
    Fits a data transformation technique on the training data and applies the transformation
    to both the training and validation data.

    Parameters:
    -----------
    technique : object
        The data transformation technique (e.g., from Scikit-learn) to be applied.

    X_train : pandas.DataFrame or array-like
        The training data to fit the transformation technique and transform.

    X_val : pandas.DataFrame or array-like, optional (default=None)
        The validation data to be transformed.

    column_transformer : bool, optional (default=False)
        Flag to indicate if a column transformer is used for custom column names.

    Returns:
    --------
    X_train_transformed : pandas.DataFrame
        Transformed training data.

    X_val_transformed : pandas.DataFrame or None
        Transformed validation data. None if X_val is None.

    Notes:
    ------
    - Fits the transformation technique on the training data (X_train).
    - Applies the fitted transformation to X_train and optionally to X_val if provided.
    '''
    # Fit the transformation technique on the training data
    technique.fit(X_train)

    # Apply transformation to the training data
    X_train_transformed = transformation(technique, X_train, column_transformer)

    # Apply transformation to the validation data if provided
    X_val_transformed = None
    if X_val is not None:
        X_val_transformed = transformation(technique, X_val, column_transformer)

    return X_train_transformed, X_val_transformed

# Because this is panel data so I will split each country_Region's data
def train_test_split(data):
    # size = int(len(data)*0.8)
    # for train data will be collected from each country's data which index is from 0-size (80%)
    x_train = data.drop(columns=['positionOrder']).iloc[0:-1]
    # for test data will be collected from each country's  data which index is from size to the end (20%)
    x_test = data.drop(columns=['positionOrder']).iloc[-1:]
    y_train = data['positionOrder'].iloc[0:-1]
    y_test = data['positionOrder'].iloc[-1:]
    return x_train, x_test, y_train, y_test


# Code Source: https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in-1, -1, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    # for i in range(0, n_out):
    #     cols.append(df.shift(-i))
    #     if i == 0:
    #         names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
    #     else:
    #         names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# create the reshape function
def reshape_data(train,test):
    #Frame as supervised learning and drop all time t columns except
    reframed_train = series_to_supervised(train, 1, 1)
    reframed_test = series_to_supervised(test, 1, 1)
    # split into train and test sets
    train= reframed_train.values
    test=reframed_test.values
    # split into input and outputs
    train_X, y_train = train[:, :-1], train[:, -1]
    test_X, y_test = test[:, :-1], test[:, -1]
    # reshape input to be 3D [samples, timesteps, features]
    x_train = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    x_test = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    return x_train,x_test,y_train,y_test


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
import re

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error, r2_score, classification_report

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

import warnings
warnings.filterwarnings('ignore')

def predictive_model(round_to_predict):
    # filter data
    train = pd.read_pickle('data_to_model.pkl')

    train_filtered = train[((train['round'] <= round_to_predict) & (train['year'] == 2023)) | (train['year'] == 2022)]

    # normalized the data
    train_scaled = data_transform(MinMaxScaler(), train_filtered.drop(columns=['positionOrder', 'constructorRef', 'firstDriver', 'year', 'round']))[0]

    # impute missing values
    imputer = KNNImputer(n_neighbors=5)
    train_scaled = data_transform(imputer, train_scaled)[0]

    # create label column
    train_copy = train_filtered.copy()
    train_copy[train_scaled.columns] = np.array(train_scaled)
    train_copy['driver'] = list(zip(train_copy.constructorRef, train_copy.firstDriver))

    # set index
    train_copy = train_copy.set_index(['constructorRef', 'firstDriver', 'year', 'round'])

    # get list of driver
    driver = list(set(train_copy.driver))

    # loop each country_Region and split the data into train and test data
    X_train = []
    X_test = []
    Y_train = []
    Y_test = []
    for i in range(0,len(driver)):
        data = train_copy[train_copy['driver'] == driver[i]]
        # applied the function I created above
        x_train, x_test, y_train, y_test = train_test_split(data)
        X_train.append(x_train)
        X_test.append(x_test)
        Y_train.append(y_train)
        Y_test.append(y_test)


    # concatenate each train dataset in X_train list and Y_train list respectively
    X_train = pd.concat(X_train)
    Y_train = pd.DataFrame(pd.concat(Y_train))

    # concatenate each test dataset in X_test list and Y_test list respectively
    X_test = pd.concat(X_test)
    Y_test = pd.DataFrame(pd.concat(Y_test))

    # encode the driver column
    encoder = LabelEncoder()

    #combine X train and Y train as train data
    train_data = pd.DataFrame()
    train_data[X_train.columns] = X_train
    train_data[Y_train.columns] = Y_train
    train_data['driver'] = encoder.fit_transform(train_data['driver'].astype(str)).astype(float)

    #combine X test and Y test as test data
    test_data = pd.DataFrame()
    test_data[X_test.columns] = X_test
    test_data[Y_test.columns] = Y_test
    test_data['driver'] = encoder.fit_transform(test_data['driver'].astype(str)).astype(float)

    # using the function to obtian reshaped x_train,x_test,y_train,y_test
    x_train, x_test, y_train, y_test = reshape_data(train_data, test_data)

    # correct the data type
    x_train = np.asarray(x_train).astype(np.float32)
    y_train = np.asarray(y_train).astype(np.float32)
    x_test = np.asarray(x_test).astype(np.float32)
    y_test = np.asarray(y_test).astype(np.float32)

    # design network for confirmed cases data
    model = None
    model = Sequential()
    model.add(LSTM(40, activation='relu', input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(30, activation='relu'))

    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    # fit network
    history = model.fit(x_train, y_train, epochs=100, batch_size=50, verbose=0, shuffle=False)

    # make a prediction
    y_test_pred = model.predict(x_test)

    # create evaluation dataframe
    evaluation = pd.DataFrame()
    evaluation[['constructorRef', 'firstDriver', 'year', 'round']] = X_test.reset_index()[
        ['constructorRef', 'firstDriver', 'year', 'round']]
    evaluation['prediction'] = [i[0] for i in y_test_pred]
    # evaluation['position'] = y_test

    # rank the 'prediction' values within each 'round'
    evaluation['positionPrediction'] = evaluation.groupby('round')['prediction'].rank(ascending=False)

    # transform ranks to positions (20 to 1)
    evaluation['positionPrediction'] = 20 - evaluation['positionPrediction'] + 1

    drivers_evaluation_map = {
        'Max Verstappen': ['red_bull', 1],
        'Sergio Perez': ['red_bull', 0],
        'Lewis Hamilton': ['mercedes', 1],
        'George Russell': ['mercedes', 0],
        'Charles Leclerc': ['ferrari', 1],
        'Carlos Sainz': ['ferrari', 0],
        'Lando Norris': ['mclaren', 1],
        'Oscar Piastri': ['mclaren', 0],
        'Esteban Ocon': ['alpine', 1],
        'Pierre Gasly': ['alpine', 0],
        'Lance Stroll': ['aston_martin', 1],
        'Fernando Alonso': ['aston_martin', 0],
        'Valterri Bottas': ['alfa', 1],
        'Guanyu Zhou': ['alfa', 0],
        'Yuki Tsunoda': ['alphatauri', 1],
        'Nyck De Vries': ['alphatauri', 0],
        'Kevin Magnussen': ['haas', 1],
        'Nico Hulkenberg': ['haas', 0],
        'Alexander Albon': ['williams', 1],
        'Logan Sargeant': ['williams', 0]
    }

    def map_drivers(row):
        constructor = row['constructorRef']
        first_driver = row['firstDriver']
        for driver, values in drivers_evaluation_map.items():
            if values[0] == constructor and values[1] == first_driver:
                return driver
        return 'Unknown'  # If no match is found

    # Applying the function to create the 'driver' column
    evaluation['driver'] = evaluation.apply(map_drivers, axis=1)

    # Drop unnecessary columns
    evaluation.drop(columns=['constructorRef', 'firstDriver', 'prediction', 'year', 'round'], inplace=True)

    # Sort by positionPrediction
    evaluation.sort_values(by='positionPrediction', inplace=True)
    return evaluation

#####

#######################################################################################################################
tools_custom = [
    {
        'name': 'draw_f1_circuit',
        'description': 'Draws an F1 circuit map with corner information. Returns a graph.',
        'function': draw_f1_circuit,
        'parameters': ['circuit', 'year'],
        'dependencies': ['fastf1', 'matplotlib', 'numpy']
    },
    {
        'name': 'compare_track_dominance',
        'description': 'Compares the track dominance between two F1 drivers. Returns a graph.',
        'function': compare_track_dominance,
        'parameters': ['race_name', 'driver_surname1', 'driver_surname2', 'year', 'session'],
        'dependencies': ['fastf1', 'matplotlib', 'numpy', 'pandas']
    },
    {
        'name': 'get_from_fastf1',
        'description': 'Gathers data from FastF1 for a specific F1 session.',
        'function': get_from_fastf1,
        'parameters': ['year', 'gp', 'session'],
        'dependencies': ['fastf1']
    },
    {
        'name': 'plot_driver_standings_by_year',
        'description': 'Plots the driver standings for a given F1 season using Ergast data. Caution with requests per '
                       'hour. Returns a heatmap.',
        'function': plot_driver_standings_by_year,
        'parameters': ['year'],
        'dependencies': ['plotly.express', 'plotly.io', 'fastf1.ergast']
    },
    {
        'name': 'access_wikipedia_api',
        'description': 'Accesses the Wikipedia API to get a summary of a given subject. Returns a JSON',
        'function': access_wikipedia_api,
        'parameters': ['subject'],
        'dependencies': ['langchain.tools.WikipediaQueryRun', 'langchain_community.utilities.WikipediaAPIWrapper']
    },
    {
        'name': 'create_combinations',
        'description': 'Creates combinations of data based on specified keys.',
        'function': create_combinations,
        'parameters': ['data', 'i', 'defined_keys'],
        'dependencies': ['pandas', 'itertools']
    },
    {
        'name': 'optimize_team',
        'description': "Optimizes a team's combination of drivers and constructors. Returns best driver combination "
                       "and best constructor combination separately.",
        'function': optimize_team,
        'parameters': ['current_round', 'num_previous_race', 'max_capacity', 'drivers_defined', 'constructors_defined'],
        'dependencies': ['pandas']
    },
    {
        'name': 'predictive_model',
        'description': 'Builds and evaluates a predictive model for F1 race positions. Returns a DataFrame.',
        'function': predictive_model,
        'parameters': ['round_to_predict'],
        'dependencies': ['pandas', 'numpy', 'scikit-learn', 'tensorflow']
    }
]
