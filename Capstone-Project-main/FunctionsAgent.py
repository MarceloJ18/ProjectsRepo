from ChatbotFunctions import *

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
    }
]
