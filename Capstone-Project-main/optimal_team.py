import pandas as pd
import numpy as np
import ast

# attempt to get the cost and points from the fantasy
dr_data = pd.read_csv('data/F1_23_drivers_basic.csv').drop(columns=['color', 'constructor'])
ct_data = pd.read_csv('data/F1_23_constructors_basic.csv').drop(columns=['color', 'constructor'])

def extract_values(string):
    # Convert the string representation of the list of dictionaries to an actual list
    lst = ast.literal_eval(string)

    # Extracting the required values
    weekend_points = lst[0]['results_per_race_list']
    price_at_lock = lst[1]['results_per_race_list']

    return weekend_points, price_at_lock


# Function to extract the values from the nested lists and create new columns
def extract_columns(row, column):
    return pd.Series(row[column])


################### GETTING DRIVERS COST AND POINTS WEEKLY #####################

# Apply the extract_values function to 'race_results' column to get two separate columns
dr_data[['weekend_points', 'price_at_lock']] = pd.DataFrame(dr_data['race_results'].apply(extract_values).tolist())

# Create new columns for each value within 'weekend_points' and 'price_at_lock'
weekend_points_df = pd.DataFrame(dr_data['weekend_points'].tolist(), columns=[f'weekend_point_{i}' for i in range(1, 23)])
price_at_lock_df = pd.DataFrame(dr_data['price_at_lock'].tolist(), columns=[f'price_at_lock_{i}' for i in range(1, 23)])

# Concatenate the new columns with the existing DataFrame
data = pd.concat([dr_data, weekend_points_df, price_at_lock_df], axis=1)

# Drop the original 'weekend_points' and 'price_at_lock' columns
data.drop(columns=['race_results', 'weekend_points', 'price_at_lock'], inplace=True)


race_dict = {}
for col in range(1, 23):
    race_data = {}
    for idx, row in data.iterrows():
        driver = row['abbreviation']
        weekend_points = row[f'weekend_point_{col}']
        price_at_lock = row[f'price_at_lock_{col}']
        race_data[driver] = [price_at_lock, weekend_points]
    race_dict[col] = race_data


race_dict[2]['OCO']

########################### CONSTRUCTORS COST AND WEEKLY POINTS ################

# Apply the extract_values function to 'race_results' column to get two separate columns
ct_data[['weekend_points', 'price_at_lock']] = pd.DataFrame(ct_data['race_results'].apply(extract_values).tolist())

# Create new columns for each value within 'weekend_points' and 'price_at_lock'
weekend_points_df = pd.DataFrame(ct_data['weekend_points'].tolist(), columns=[f'weekend_point_{i}' for i in range(1, 23)])
price_at_lock_df = pd.DataFrame(ct_data['price_at_lock'].tolist(), columns=[f'price_at_lock_{i}' for i in range(1, 23)])

# Concatenate the new columns with the existing DataFrame
data = pd.concat([ct_data, weekend_points_df, price_at_lock_df], axis=1)

# Drop the original 'weekend_points' and 'price_at_lock' columns
data.drop(columns=['race_results', 'weekend_points', 'price_at_lock'], inplace=True)


race_dict = {}
for col in range(1, 23):
    race_data = {}
    for idx, row in data.iterrows():
        constructor = row['abbreviation']
        weekend_points = row[f'weekend_point_{col}']
        price_at_lock = row[f'price_at_lock_{col}']
        race_data[constructor] = [price_at_lock, weekend_points]
    race_dict[col] = race_data
##########################################################################################




# first value is the cost to select in the fantasy
# and its followed by the avg points made during the season
drivers = {'verstappen': [30, 20],
           'perez': [20, 18],
           
           'hamilton': [25, 16],
           'russell': [20, 17],
           
           'leclerc': [25, 19],
           'sainz': [20, 15],
           
           'alonso': [12, 12],
           'stroll': [8, 8],
           
           'norris': [15, 14],
           'piastri': [8, 2],
           
           'ocon': [9, 13],
           'gasly': [8, 9],
           
           'de_vries': [5, 4],
           'tsunoda': [5, 7],
           
           'bottas': [8, 11],
           'zhou': [6, 6],
           
           'albon': [5, 5],
           'sargeant': [4, 1],
           
           'magnussen': [6, 10],
           'hulkenberg': [5, 3],
           }

# first value is the cost to select in the fantasy
# and its followed by the avg points made during the season
constructors = {'red_bull': [30, 10],
                'mercedes': [25, 8],
                'ferrari': [25, 9],
                'aston_martin': [8, 4],
                'mclaren': [12, 6],
                'alpine': [10, 7],
                'alpha_tauri': [5, 2],
                'williams': [4, 1],
                'alfa_romeo': [6, 5],
                'haas': [6, 3],
                }


from itertools import combinations

def optimize_team(drivers, constructors, max_capacity):
    best_value = 0
    best_team = None

    # Generate combinations of 5 drivers
    driver_combinations = combinations(drivers.keys(), 5)

    # Iterate through all combinations
    for drivers_combo in driver_combinations:
        # Generate combinations of 2 constructors for each driver combination iteration
        constructor_combinations = combinations(constructors.keys(), 2)

        for constructors_combo in constructor_combinations:
            # Calculate total weight and value for the combination
            total_weight = sum(drivers[driver][0] for driver in drivers_combo) + sum(constructors[constructor][0] for constructor in constructors_combo)
            total_value = sum(drivers[driver][1] for driver in drivers_combo) + sum(constructors[constructor][1] for constructor in constructors_combo)
            
            # Check if within weight limit and update best team
            if total_weight <= max_capacity and total_value > best_value:
                best_value = total_value
                best_team = (list(drivers_combo), list(constructors_combo))
    
    return best_value, best_team


# Usage
best_value, best_team = optimize_team(drivers, constructors, 100)
print("Best value:", best_value)
print("Best team (drivers, constructors):", best_team)
