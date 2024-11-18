#Importing the required packages
import streamlit as st
import pandas as pd
import re

#Used to create some of the plots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots

#Some useful created functions
# Custom function to convert numeric position to ordinal position
def ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f"{int(number)}{suffix}"

# Function to map values (to fix the status)
def categorize_status(value):
    if value == 'Finished':
        return 'Finished'
    elif  re.match(r'\+\d+ Laps?', value):
        return 'Lapped'
    elif value in ['Accident', 'Collision', 'Collision damage']:
        return 'Accident'
    else:
        return 'Mechanical'

#Useful Dictionaries
driver_nations = {'American' : '🇺🇸', 'British': '🇬🇧', 'Thai': '🇹🇭',
                  'Australian': '🇦🇺', 'Japanese': '🇯🇵', 'Canadian': '🇨🇦',
                  'Spanish': '🇪🇸', 'Dutch': '🇳🇱', 'German': '🇩🇪',
                  'Monegasque': '🇲🇨', 'French': '🇫🇷' , 'Finnish': '🇫🇮',
                  'Chinese': '🇨🇳', 'Mexican': '🇲🇽', 'Danish': '🇩🇰'}

driver_photos_2022 = {
    'Daniel Ricciardo': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/ricciardo.jpg.img.',
    'Lando Norris': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/norris.jpg.img.',
    'Lewis Hamilton': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/hamilton.jpg.img.',
    'George Russell': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/russell.jpg.img.',
    'Alexander Albon': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/albon.jpg.img.',
    'Carlos Sainz': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/sainz.jpg.img.',
    'Charles Leclerc': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/leclerc.jpg.img.',
    'Esteban Ocon': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/ocon.jpg.img.',
    'Fernando Alonso': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/alonso.jpg.img.',
    'Lance Stroll': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/stroll.jpg.img.',
    'Valtteri Bottas': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/bottas.jpg.img.',
    'Guanyu Zhou': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/zhou.jpg.img.',
    'Sergio Pérez': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/perez.jpg.img.',
    'Max Verstappen': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/verstappen.jpg.img.',
    'Nico Hülkenberg': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/hulkenberg.jpg.img.1920.medium.jpg/1676983071882.jpg',
    'Pierre Gasly': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/gasly.jpg.img.',
    'Yuki Tsunoda': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/tsunoda.jpg.img.',
    'Nicholas Latifi': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/latifi.jpg.img.',
    'Kevin Magnussen': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/magnussen.jpg.img.',
    'Mick Schumacher': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/schumacher.jpg.img.',
    'Nyck de Vries': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/devries.jpg.img.',
    'Sebastian Vettel': 'https://media.formula1.com/content/dam/fom-website/drivers/2022Drivers/vettel.jpg.img.'
}

driver_photos_2023 = {
    'Daniel Ricciardo': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/ricciardo.jpg.img.1920.medium.jpg/1689928543988.jpg',
    'Lando Norris': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/norris.jpg.img.1920.medium.jpg/1677069505471.jpg',
    'Oscar Piastri': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/piastri.jpg.img.1920.medium.jpg/1676983075734.jpg',
    'Lewis Hamilton': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/hamilton.jpg.img.1920.medium.jpg/1677069594164.jpg',
    'George Russell': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/russell.jpg.img.1920.medium.jpg/1677069334466.jpg',
    'Alexander Albon': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/albon.jpg.img.1920.medium.jpg/1689253984120.jpg',
    'Carlos Sainz': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/sainz.jpg.img.1920.medium.jpg/1677069189406.jpg',
    'Charles Leclerc': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/leclerc.jpg.img.1920.medium.jpg/1677069223130.jpg',
    'Esteban Ocon': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/ocon.jpg.img.1920.medium.jpg/1677069269007.jpg',
    'Fernando Alonso': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/alonso.jpg.img.1920.medium.jpg/1701269362697.jpg',
    'Lance Stroll': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/stroll.jpg.img.1920.medium.jpg/1677069453013.jpg',
    'Valtteri Bottas': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/bottas.jpg.img.1920.medium.jpg/1677069810695.jpg',
    'Guanyu Zhou': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/zhou.jpg.img.1920.medium.jpg/1701089369046.jpg',
    'Sergio Pérez': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/perez.jpg.img.1920.medium.jpg/1677069773437.jpg',
    'Max Verstappen': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/verstappen.jpg.img.1920.medium.jpg/1701270073824.jpg',
    'Nico Hülkenberg': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/hulkenberg.jpg.img.1920.medium.jpg/1676983071882.jpg',
    'Pierre Gasly': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/gasly.jpg.img.1920.medium.jpg/1701087615229.jpg',
    'Yuki Tsunoda': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/tsunoda.jpg.img.1920.medium.jpg/1701268830375.jpg',
    'Kevin Magnussen': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/magnussen.jpg.img.1920.medium.jpg/1677069387823.jpg',
    'Logan Sargeant': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/sargeant.jpg.img.1920.medium.jpg/1701272060171.jpg',
    'Nyck de Vries': 'https://media.formula1.com/content/dam/fom-website/drivers/2023Drivers/devries.jpg.img.',
}


driver_colors_2022 = { 'Daniel Ricciardo': '#FF8700',
    'Lando Norris': '#FF8700',
    'Lewis Hamilton': '#00D2BE',
    'George Russell': '#00D2BE',
    'Alexander Albon': '#005AFF',
    'Carlos Sainz': '#DC0000',
    'Charles Leclerc': '#DC0000',
    'Esteban Ocon': '#0090FF',
    'Fernando Alonso': '#0090FF',
    'Lance Stroll': '#006F62',
    'Valtteri Bottas': '#900000',
    'Guanyu Zhou': '#900000',
    'Sergio Pérez': '#0600EF',
    'Max Verstappen': '#0600EF',
    'Nico Hülkenberg': '#006F62',
    'Pierre Gasly': '#2B4562',
    'Yuki Tsunoda': '#2B4562',
    'Nicholas Latifi': '#005AFF',
    'Kevin Magnussen': '#FFFFFF',
    'Mick Schumacher': '#FFFFFF',
    'Nyck de Vries': '#005AFF',
    'Sebastian Vettel': '#006F62'
}

driver_colors_2023 = {
    'Daniel Ricciardo': '#2B4562',
    'Lando Norris': '#FF8700',
    'Oscar Piastri': '#FF8700',
    'Lewis Hamilton': '#00D2BE',
    'George Russell': '#00D2BE',
    'Alexander Albon': '#005AFF',
    'Carlos Sainz': '#DC0000',
    'Charles Leclerc': '#DC0000',
    'Esteban Ocon': '#0090FF',
    'Fernando Alonso': '#006F62',
    'Lance Stroll': '#006F62',
    'Valtteri Bottas': '#900000',
    'Valtteri Bottas': '#900000',
    'Sergio Pérez': '#0600EF',
    'Max Verstappen': '#0600EF',
    'Nico Hülkenberg': '#FFFFFF',
    'Pierre Gasly': '#0090FF',
    'Yuki Tsunoda': '#2B4562',
    'Kevin Magnussen': '#FFFFFF',
    'Logan Sargeant': '#005AFF',
    'Nyck de Vries': '#2B4562',
}


driver_helmets_2022 = {
    'Daniel Ricciardo': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/ricciardo.png',
    'Lando Norris': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/norris.png',
    'Lewis Hamilton': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/hamilton.png',
    'George Russell': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/russell.png',
    'Alexander Albon': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/albon.png',
    'Carlos Sainz': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/sainz.png',
    'Charles Leclerc': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/leclerc.png',
    'Esteban Ocon': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/ocon.png',
    'Fernando Alonso': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/alonso.png',
    'Lance Stroll': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/stroll.png',
    'Valtteri Bottas': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/bottas.png',
    'Guanyu Zhou': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/zhou.png',
    'Sergio Pérez': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/perez.png',
    'Max Verstappen': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/verstappen.png',
    'Nico Hülkenberg': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/hulkenberg.png',
    'Pierre Gasly': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/gasly.png',
    'Yuki Tsunoda': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/tsunoda.png',
    'Logan Sargeant': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/sargeant.png',
    'Kevin Magnussen': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/magnussen.png',
    'Nicholas Latifi': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/latifi.png',
    'Nyck de Vries': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/devries.png',
    'Sebastian Vettel': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/vettel.png',
    'Mick Schumacher': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/schumacher.png',

}

driver_helmets_2023 = {
    'Daniel Ricciardo': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2022/ricciardo.png',
    'Lando Norris': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/norris.png',
    'Lewis Hamilton': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/hamilton.png',
    'George Russell': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/russell.png',
    'Alexander Albon': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/albon.png',
    'Carlos Sainz': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/sainz.png',
    'Charles Leclerc': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/leclerc.png',
    'Esteban Ocon': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/ocon.png',
    'Fernando Alonso': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/alonso.png',
    'Lance Stroll': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/stroll.png',
    'Valtteri Bottas': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/bottas.png',
    'Guanyu Zhou': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/zhou.png',
    'Sergio Pérez': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/perez.png',
    'Max Verstappen': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/verstappen.png',
    'Nico Hülkenberg': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/hulkenberg.png',
    'Pierre Gasly': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/gasly.png',
    'Yuki Tsunoda': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/tsunoda.png',
    'Logan Sargeant': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/sargeant.png',
    'Kevin Magnussen': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/magnussen.png',
    'Oscar Piastri': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/piastri.png',
    'Nyck de Vries': 'https://media.formula1.com/content/dam/fom-website/manual/Helmets2023/devries.png',
}


constructor_logos = {
    'Mercedes': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/mercedes.png',
    'Red Bull': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/red%20bull.png',
    'McLaren': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/mclaren.png',
    'Aston Martin': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/aston%20martin.png',
    'AlphaTauri': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/alphatauri.png',
    'Haas F1 Team': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/haas.png',
    'Alpine F1 Team': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/alpine.png',
    'Williams': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/williams%20blue.png',
    'Ferrari': 'https://media.formula1.com/content/dam/fom-website/teams/Ferrari/logo-ferrari-18%20.png',
    'Alfa Romeo': 'https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/team%20logos/alfa%20romeo.png'
}

team_colors = {
    'Mercedes': '#00D2BE',
    'Red Bull': '#0600EF',
    'McLaren': '#FF8700',
    'Aston Martin': '#006F62',
    'AlphaTauri': '#2B4562',
    'Haas F1 Team': '#FFFFFF',
    'Alpine F1 Team': '#0090FF',
    'Williams': '#005AFF',
    'Ferrari': '#DC0000',
    'Alfa Romeo': '#900000'
}

constructor_liveries = {
    'Mercedes': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/mercedes.png.transform/6col/image.png',
    'Red Bull': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/red-bull-racing.png.transform/6col/image.png',
    'McLaren': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/mclaren.png.transform/6col/image.png',
    'Aston Martin': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/aston-martin.png.transform/6col/image.png',
    'AlphaTauri': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/alphatauri.png.transform/6col/image.png',
    'Haas F1 Team': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/haas-f1-team.png.transform/6col/image.png',
    'Alpine F1 Team': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/alpine.png.transform/6col/image.png',
    'Williams': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/williams.png.transform/6col/image.png',
    'Ferrari': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/ferrari.png.transform/6col/image.png',
    'Alfa Romeo': 'https://media.formula1.com/d_team_car_fallback_image.png/content/dam/fom-website/teams/2023/alfa-romeo.png.transform/6col/image.png'
}

track_maps = {
    "Albert Park Grand Prix Circuit": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.jpg',
    "Bahrain International Circuit": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Bahrain_Circuit.png.transform/9col/image.jpg',
    "Jeddah Corniche Circuit": 'https://media.formula1.com/image/upload/f_auto/q_auto/v1677244985/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit.png.transform/9col/image.jpg',
    "Red Bull Ring": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit.jpg',
    "Baku City Circuit": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.jpg',
    "Circuit de Barcelona-Catalunya": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Spain_Circuit.jpg',
    "Circuit Gilles Villeneuve": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit.png.transform/9col/image.jpg',
    "Miami International Autodrome": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png.transform/9col/image.jpg',
    "Circuit de Spa-Francorchamps": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.jpg',
    "Hungaroring ": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit.jpg',
    "Silverstone Circuit ": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit.jpg',
    "Circuit de Monaco": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monoco_Circuit.png.transform/9col/image.jpg',
    "Autódromo José Carlos Pace": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit.png.transform/9col/image.jpg',
    "Marina Bay Street Circuit ": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.png.transform/9col/image.jpg',
    "Autodromo Nazionale di Monza ": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Italy_Circuit.jpg',
    "Yas Marina Circuit": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit.jpg',
    "Circuit of the Americas": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.jpg',
    "Autodromo Enzo e Dino Ferrari": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.jpg',
    "Autódromo Hermanos Rodríguez": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.jpg',
    "Circuit Paul Ricard": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/France_Circuit.jpg',
    "Circuit Park Zandvoort": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Netherlands_Circuit.jpg',
    "Suzuka Circuit": 'https://media.formula1.com/image/upload/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Japan_Circuit.png.transform/9col/image.jpg',
    }

######## Setting the overall page configuration ########
st.set_page_config(
    layout='wide',
    page_title='AiTHLETES F1 Hub | Data Hub',
    page_icon="📊",
    initial_sidebar_state='collapsed'
)

######## Setting a new style for the page ########
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#### Importing the datasets from our github repo that will be used to create the visualizations ###
n2k = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/daniel.everything/n2k_data.csv")
#Data that was used for the modelling
new_era = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/main/data/data2022_2023.csv") #for general use

#Data for drivers info tab
drivers_data = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/main/data/drivers.csv")
constructors_data = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/main/data/constructors.csv")


#Data of Circuits
circuits_data = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/main/data/circuits.csv")
#altering a specific circuits_data column to avoid confusion
circuits_data.rename(columns = {'name': 'track_name'}, inplace=True)


#Data of Races
race_data = pd.read_csv("https://raw.githubusercontent.com/ARCadete21/Capstone-Project/main/data/races.csv")
#altering a specific race_data column to avoid confusion
race_data.rename(columns = {'name': 'gp_name'}, inplace=True)
# Convert the 'date' column in race_data to datetime format
race_data['date'] = pd.to_datetime(race_data['date'])
# Filter races that occurred in or after 2022
filtered_race_data = race_data[race_data['date'].dt.year >= 2022]



# Merge datasets based on 'driverRef'

#Adding driver's personal info
merged_drivers = pd.merge(new_era, drivers_data[['driverRef', 'forename', 'surname', 'dob', 'number', 'code']], on='driverRef', how='left')
#Adding constructors info
merged_drivers = pd.merge(merged_drivers, constructors_data[['constructorRef', 'name']], on='constructorRef', how='left')
#Adding track info & races info
merged_drivers = pd.merge(merged_drivers, circuits_data[['circuitRef', 'track_name', 'location', 'country', 'circuitId']], on='circuitRef', how='left') #possible to add lat, lng, alt
#Adding every gp information
merged_drivers = pd.merge(merged_drivers, filtered_race_data[['circuitId', 'year', 'gp_name', 'date', 'time']], on=['circuitId', 'year'], how='inner')


#######################

#Renaming the imported date column to gp_date, to know what it regards
merged_drivers.rename(columns = {'date': 'gp_date'}, inplace=True)

###### Additional data transformation #########

# Create a new column 'driver_name' by concatenating 'Forename' and 'Surname'
merged_drivers['driver_name'] = merged_drivers['forename'] + ' ' + merged_drivers['surname']
merged_drivers.rename(columns= {'name': 'team_name'}, inplace=True)


#Formatting time variables
# Reformat the 'dob' column to dd-mm-yyyy
merged_drivers['dob'] = pd.to_datetime(merged_drivers['dob'])
merged_drivers['dob'] = merged_drivers['dob'].dt.strftime('%d-%m-%Y')

# #Converting gp_date from object to datetime datatype
merged_drivers['gp_date'] = pd.to_datetime(merged_drivers['gp_date'])
# merged_drivers['gp_date'] = merged_drivers['gp_date'].dt.strftime('%d-%m-%Y')


# Convert the 'year' column to the appropriate data type (e.g., int)
merged_drivers['year'] = merged_drivers['year'].astype(int)




# Apply mapping function to 'status' column
merged_drivers['status'] = merged_drivers['status'].apply(categorize_status)


#Main Sidebar selectbox
st.sidebar.subheader("What are you looking for?")

select_opts = ['Driver Information', 
               'Constructor Statistics', 
               'Grand Prix Information']

# Driver statistics, Constructor Statistics, Grand Prix information, etc.
option_chosen = st.sidebar.selectbox('Select your option', [None] + select_opts)

main_menu_indication = st.subheader("")

if option_chosen == 'Driver Information':
    # Sidebar specifics
    selected_year = st.sidebar.selectbox('Select Year', merged_drivers['year'].unique())

    # Filter drivers based on the selected year
    drivers_for_selected_year = merged_drivers[merged_drivers['year'] == selected_year]['driver_name'].sort_values().unique()

    # Add a None option at the beginning of the list
    drivers_list = [None] + drivers_for_selected_year.tolist()

    # Select a driver
    selected_driver = st.selectbox("Select a driver:", drivers_list, index=0, key="driver_selectbox")
    

    # Add your driver statistics content here
    if selected_driver is None:
        # Driver Standings (using overall dataset to then use for specific cases)
        driver_standings = merged_drivers.groupby(['driver_name', 'team_name', 'year'])['points'].sum().reset_index()
        driver_standings = driver_standings.rename(columns={'points': 'Total Points'})
        driver_standings_sorted = driver_standings.sort_values(by='Total Points', ascending=False)

        selected_year_data = driver_standings_sorted[driver_standings_sorted['year'] == selected_year]

        # Dropping the index column, resetting the index starting from 1, and removing the 'year' column
        selected_year_data_reset_index = selected_year_data.drop(columns=['year']).reset_index(drop=True)
        selected_year_data_reset_index.index += 1  # Set the index to start from 1

        # Renaming the first two columns
        selected_year_data_reset_index = selected_year_data_reset_index.rename(columns={'driver_name': 'Driver Name', 'team_name': 'Team Name'})

        # Display the table and stretching across the page
        st.markdown("Current Driver Championship Standings")
        st.dataframe(selected_year_data_reset_index, width=1500, height=815)


        ###### Row A of data displaying #######
        # Initializing columns to display data
        col1, col2, col3 = st.columns(3)

        # Add a new column 'positions_gained' representing positions gained per race
        merged_drivers['positions_gained'] = merged_drivers['grid'] - merged_drivers['positionOrder']

        # Filter data for the selected year
        selected_year_data = merged_drivers[merged_drivers['year'] == selected_year]

        # Display the top 5 gainers in the selected year using st.metric
        top_gainers = selected_year_data.groupby('driver_name')['positions_gained'].mean().nlargest(5).round(1)
        col1.write(f"Top 5 Position Gainers in {selected_year}:")
        for driver, positions_gained in top_gainers.items():
            col1.metric(label=driver, value=positions_gained)

        # Display top 5 losers using st.metric
        top_losers = selected_year_data.groupby('driver_name')['positions_gained'].mean().nsmallest(5).round(1)
        col2.write(f"Top 5 Position Losers in {selected_year}:")
        for driver, positions_lost in top_losers.items():
            col2.metric(label=driver, value=positions_lost)


        # Filter the DataFrame to include only rows with specific statuses
        selected_year_data_dnf = selected_year_data[selected_year_data['status'].isin(['Mechanical', 'Accident'])]

        # Drivers with the highest sum of DNFs
        total_dnfs = selected_year_data_dnf.groupby('driver_name')['status'].count().nlargest(5)
        col3.write(f"Top 5 Drivers with the most DNFs (Mechanical + Accident) in {selected_year}:")

        for driver, count in total_dnfs.items():
            # Get the counts for 'Car issue' and 'Accident' separately
            car_issue_count = selected_year_data_dnf[(selected_year_data_dnf['driver_name'] == driver) & (selected_year_data_dnf['status'] == 'Mechanical')].shape[0]
            accident_count = selected_year_data_dnf[(selected_year_data_dnf['driver_name'] == driver) & (selected_year_data_dnf['status'] == 'Accident')].shape[0]

            # Display the driver with the total number of DNFs and counts for 'Car issue' and 'Accident'
            col3.metric(label=f"{driver} ({car_issue_count} Mechanical Issues + {accident_count} Accident)", value=count)


        ###### Row B ######
        #Drivers with most wins
        winner_counts = selected_year_data[selected_year_data['positionOrder'] == 1].groupby('driver_name').size()

        gp_winners = winner_counts.nlargest(5)

        # Create a horizontal bar chart using plotly express
        fig = px.bar(gp_winners, x=gp_winners.values, 
                     y=gp_winners.index, 
                     orientation='h', 
                     title=f"Top 5 Drivers with more Wins in {selected_year}")

        # Display the chart using st.plotly_chart
        col1.plotly_chart(fig)


        # Drivers with most top 3
        # Count the occurrences of each driver in the top 3 positions
        top3_counts = selected_year_data[selected_year_data['positionOrder'] <= 3].groupby('driver_name').size()

        top3_drivers = top3_counts.nlargest(5)

        # Create a horizontal bar chart using plotly express
        fig = px.bar(top3_drivers, x=top3_drivers.values, 
                     y=top3_drivers.index, 
                     orientation='h', 
                     title=f"Top 5 Drivers with more Podiums in {selected_year}")

        # Display the chart using st.plotly_chart
        col2.plotly_chart(fig)



        ###### Row C #######
        # Choose the appropriate driver color dictionary based on the selected year
        if selected_year == 2022:
            driver_colors = driver_colors_2022
        elif selected_year == 2023:
            driver_colors = driver_colors_2023

        # Convert gp_date to datetime
        selected_year_data['gp_date'] = pd.to_datetime(selected_year_data['gp_date'])

        # Sort the DataFrame by gp_date
        selected_year_data.sort_values(by='gp_date', inplace=True)

        # Create a new column for driver color
        selected_year_data['driver_color'] = selected_year_data['driver_name'].map(driver_colors)

        # Plotting using Plotly Express
        fig = px.line(selected_year_data, x='round', y='positionOrder', color='driver_name',
                    markers=True, line_shape='linear', labels={'positionOrder': 'Finishing Position'},
                    color_discrete_map=driver_colors)


        # Stretch the plot to take the length of the whole main page
        fig.update_layout(width=1400)

        # Customize layout
        fig.update_layout(title='Finishing Positions of Drivers in Each Race',
                        xaxis_title='Race Date',
                        yaxis_title='Finishing Position',
                        legend_title='Driver Code')

        # Invert the y-axis order
        fig.update_yaxes(autorange="reversed")

        # Display the plot in Streamlit
        st.plotly_chart(fig)



    else:
        #Row A
        #Initializing the columns
        col1, col2, col3 = st.columns(3)

        # Filter data for the selected year
        selected_year_data = merged_drivers[merged_drivers['year'] == selected_year]

        # Select the appropriate driver_photos dictionary based on the selected year
        driver_photos_dict = driver_photos_2022 if selected_year == 2022 else driver_photos_2023

        # Column 1
        driver_pic = driver_photos_dict.get(selected_driver)
        col1.image(driver_pic, use_column_width=True)

        
        # Column 2
        #Personal Information
        #Driver's Nationality
        selected_driver_nationality = selected_year_data.loc[selected_year_data['driver_name'] == selected_driver, 'nationality_x'].iloc[0]
        selected_driver_emoji = driver_nations.get(selected_driver_nationality, '')
        col2.metric("Driver Nationality", f"{selected_driver_nationality} \n {selected_driver_emoji}")

        #Driver's Age
        selected_driver_age = selected_year_data.loc[(selected_year_data['driver_name'] == selected_driver) & (selected_year_data['year'] == selected_year), 'age'].iloc[0]
        col2.metric(f"{selected_driver}'s Age", selected_driver_age)
        #DOB 
        date_birth = selected_year_data.loc[selected_year_data['driver_name'] == selected_driver, 'dob'].iloc[0]
        col2.metric(f"{selected_driver}'s Date of Birth", date_birth)

        # Professional Info :)
        # Driver's Team
        selected_driver_team = selected_year_data.loc[(selected_year_data['driver_name'] == selected_driver) & (selected_year_data['year'] == selected_year), 'team_name'].iloc[0]
        col2.metric(f"{selected_driver} drives for", selected_driver_team)
        
        #Driver's No and Ref
        selected_driver_no = selected_year_data.loc[(selected_year_data['driver_name'] == selected_driver) & (selected_year_data['year'] == selected_year), 'number'].iloc[0]
        selected_driver_ref = selected_year_data.loc[selected_year_data['driver_name'] == selected_driver, 'code'].iloc[0]
        # Convert the tuple to a string
        driver_references = f"{selected_driver_ref}   | {selected_driver_no}"

        # Display the metric
        col2.metric(label="Driver references on the track", value=driver_references)


        # Column 3
        # Select the appropriate driver_helmets dictionary based on the selected year
        driver_helmets_dict = driver_helmets_2022 if selected_year == 2022 else driver_helmets_2023

        # Column 1
        driver_helmet = driver_helmets_dict.get(selected_driver)
        col3.markdown(f"{selected_driver}'s Helmet Livery")
        col3.image(driver_helmet, use_column_width=True)


        #Displaying data of selected driver vs teammate
        ######## Stage 1 - Qualifying Position Comparison ########
        # Choose the appropriate driver color dictionary based on the selected year
        if selected_year == 2022:
            driver_colors = driver_colors_2022
        elif selected_year == 2023:
            driver_colors = driver_colors_2023

        # Convert gp_date to datetime
        selected_year_data['gp_date'] = pd.to_datetime(selected_year_data['gp_date'])

        # Sort the DataFrame by gp_date
        selected_year_data.sort_values(by='gp_date', inplace=True)

        # Filter data for the selected driver and his teammate
        team_name_selected_driver = selected_year_data.loc[
            selected_year_data['driver_name'] == selected_driver, 'team_name'].iloc[0]

        selected_driver_data = selected_year_data[selected_year_data['driver_name'] == selected_driver]
        teammate_data = selected_year_data[(selected_year_data['team_name'] == team_name_selected_driver) & 
                                            (selected_year_data['driver_name'] != selected_driver)]

        # Concatenate data for selected driver and teammate
        filtered_data = pd.concat([selected_driver_data, teammate_data])

        # Create a new column for driver color
        filtered_data['driver_color'] = filtered_data['driver_name'].map(driver_colors)

        # Swap colors between selected driver and teammate
        color_map = {selected_driver: driver_colors[teammate_data['driver_name'].iloc[0]],
                    teammate_data['driver_name'].iloc[0]: driver_colors[selected_driver]}

        # Plotting using Plotly Express
        fig = px.line(filtered_data, x='round', y='grid', color='driver_name',
                    markers=True, line_shape='linear', labels={'grid': 'Qualifying Position'},
                    color_discrete_map=color_map)

        # Manually set line dash for the selected driver and teammate
        fig.update_traces(selector=dict(name=selected_driver), line=dict(dash='solid'))
        fig.update_traces(selector=dict(name=teammate_data['driver_name'].iloc[0]), line=dict(dash='dot'))

        # Stretch the plot to take the length of the whole main page
        fig.update_layout(width=1400)

        # Customize layout
        fig.update_layout(title=f'Comparison of {selected_driver} and Teammate Qualifying Positions',
                        xaxis_title='Race Week',
                        yaxis_title='Qualifying Position',
                        legend_title='Drivers')

        # Invert the y-axis order
        fig.update_yaxes(autorange="reversed")

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        #Note for the user
        st.markdown(f"*Note: The Dashed Line represents {selected_driver}'s teammate - {teammate_data['driver_name'].iloc[0]}")

        ######## Stage 2 - Race Position Comparison ###########
        # Plotting using Plotly Express
        fig = px.line(filtered_data, x='round', y='positionOrder', color='driver_name',
                    markers=True, line_shape='linear', labels={'positionOrder': 'Finishing Position'},
                    color_discrete_map=driver_colors)

        # Swap colors between selected driver and teammate
        color_map = {selected_driver: driver_colors[teammate_data['driver_name'].iloc[0]],
                    teammate_data['driver_name'].iloc[0]: driver_colors[selected_driver]}

        # Manually set line dash for the selected driver and teammate
        fig.update_traces(selector=dict(name=selected_driver), line=dict(dash='solid'))
        fig.update_traces(selector=dict(name=teammate_data['driver_name'].iloc[0]), line=dict(dash='dot'))

        # Stretch the plot to take the length of the whole main page
        fig.update_layout(width=1400)

        # Customize layout
        fig.update_layout(title=f'Comparison of {selected_driver} and Teammate Finishing Positions',
                        xaxis_title='Race Date',
                        yaxis_title='Finishing Position',
                        legend_title='Driver Code')

        # Invert the y-axis order
        fig.update_yaxes(autorange="reversed")

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        #Note for the user
        st.markdown(f"*Note: The Dashed Line represents {selected_driver}'s teammate - {teammate_data['driver_name'].iloc[0]}")


        col4, col5 = st.columns(2)

        #Break lines
        st.markdown("")
        st.markdown("")

        # Find the highest finish for the selected driver
        highest_finish = selected_driver_data["positionOrder"].min()
        ordinal_hf = ordinal(highest_finish)
        race_with_highest_finish = selected_driver_data[selected_driver_data["positionOrder"] == highest_finish].iloc[0]

        # Display the highest finish, gp_date, and gp_name using .metric method
        col4.metric(f"{selected_driver}'s Highest Finish This Season", ordinal_hf)
        col4.metric(f"Date:", race_with_highest_finish['gp_date'].strftime('%d-%m-%Y'))
        col4.metric(f"Race:", race_with_highest_finish['gp_name'])

        #Displaying the total points achieved
        col5.metric(f"{selected_driver}'s Total Points This Season", selected_driver_data["points"].sum())
        col5.metric("", "")
        col5.metric(f"{selected_driver}'s Average Finishing Position This Season", ordinal(selected_driver_data["positionOrder"].mean()))



elif option_chosen == 'Constructor Statistics':

    selected_constructor = st.selectbox("Select your Constructor:", [None] + merged_drivers['team_name'].sort_values().unique().tolist(), 
                                   index=0, key="constructor_selectbox")
    # Sidebar specifics
    selected_year = st.sidebar.selectbox('Select Year', merged_drivers['year'].unique())

    # Filter drivers based on the selected year
    drivers_for_selected_year = merged_drivers[merged_drivers['year'] == selected_year]['driver_name'].sort_values().unique()

    # Add a None option at the beginning of the list
    drivers_list = [None] + drivers_for_selected_year.tolist()


    # Add your driver statistics content here
    if selected_constructor is None:
        # Driver Standings (using overall dataset to then use for specific cases)
        constructor_standings_totals = merged_drivers.groupby(['team_name', 'year', 'nationality_y'])['points'].sum().reset_index()
        constructor_standings_totals = constructor_standings_totals.rename(columns={'points': 'Total Points', 'nationality_y': "Constructor's Origin Country"})
        constructor_standings_sorted = constructor_standings_totals.sort_values(by='Total Points', ascending=False)

        selected_year_data = constructor_standings_sorted[constructor_standings_sorted['year'] == selected_year]

        # Dropping the index column, resetting the index starting from 1, and removing the 'year' column
        selected_year_data_reset_index = selected_year_data.drop(columns=['year']).reset_index(drop=True)
        selected_year_data_reset_index.index += 1  # Set the index to start from 1

        # Renaming the first two columns
        selected_year_data_reset_index = selected_year_data_reset_index.rename(columns={'team_name': 'Team Name'})

        # Display the table and stretching across the page
        st.markdown("Current Driver Championship Standings")
        st.dataframe(selected_year_data_reset_index, width=1500, height=400)


        ###### Row A of data displaying #######
        # Initializing columns to display data
        col1, col2, = st.columns(2)

        # Filter data for the selected year
        merged_drivers_selected_year = merged_drivers[merged_drivers['year'] == selected_year]

        # Filter for race wins (positionOrder == 1)
        race_wins = merged_drivers_selected_year[merged_drivers_selected_year['positionOrder'] == 1]

        # Group by 'team_name' and 'driver_name' and count the number of race wins
        team_driver_wins = race_wins.groupby(['team_name', 'driver_name']).size().reset_index(name='race_wins')

        # Group by 'team_name' and sum the race wins for each team
        team_wins = team_driver_wins.groupby('team_name')['race_wins'].sum().reset_index()

        # Sort teams based on total wins in descending order
        team_wins_sorted = team_wins.sort_values(by='race_wins', ascending=False)

        # Create a bar chart using Plotly Express
        fig = px.bar(team_wins_sorted, x='team_name', y='race_wins', color='team_name',
                    title=f'Total Wins per Team in {selected_year}',
                    labels={'race_wins': 'Total Wins', 'team_name': 'Team Name'},
                    color_discrete_map={team: team_colors[team] for team in team_wins_sorted['team_name']})

        # Display the chart in the Streamlit app
        col1.plotly_chart(fig)


        #Second Plot

        # Filter for podium finishes (positionOrder <= 3)
        podium_finishes = merged_drivers_selected_year[merged_drivers_selected_year['positionOrder'] <= 3]

        # Group by 'team_name' and 'driver_name' and count the number of podium finishes
        team_driver_podiums = podium_finishes.groupby(['team_name', 'driver_name']).size().reset_index(name='podiums')

        # Group by 'team_name' and sum the podium finishes for each team
        team_podiums = team_driver_podiums.groupby('team_name')['podiums'].sum().reset_index()

        # Sort teams based on total podiums in descending order
        team_podiums_sorted = team_podiums.sort_values(by='podiums', ascending=False)

        # Merge with the original team_driver_podiums DataFrame to get the correct driver names
        team_podiums_sorted = pd.merge(team_podiums_sorted, team_driver_podiums, on='team_name', how='left')

        # Create a new column combining driver names and podium counts
        team_podiums_sorted['driver_podium_info'] = team_podiums_sorted.apply(lambda row: f"{row['driver_name']} - {row['podiums_y']} podiums", axis=1)

        # Create a bar chart using Plotly Express
        fig = px.bar(team_podiums_sorted, x='team_name', y='podiums_y', color='team_name',
                    title=f'Total Podiums per Team in {selected_year}',
                    labels={'podiums_y': 'Total Podiums', 'team_name': 'Team Name'},
                    color_discrete_map={team: team_colors[team] for team in team_podiums_sorted['team_name']},
                    hover_data={'driver_podium_info': True})

        # Display the chart in the Streamlit app
        col2.plotly_chart(fig)


        ###### Row B ######

        col3, col4 = st.columns(2)
        #Distribution of dnfs by accident

        # Filter for DNFS by Accident
        dnfs_accident = merged_drivers_selected_year[merged_drivers_selected_year['status'] == 'Accident']

        # Group by 'team_name' and count the number of DNFS by Accident for each team
        team_dnfs_accident = dnfs_accident.groupby('team_name').size().reset_index(name='total_dnfs_accident')

        # Create a pie chart using Plotly Express
        fig = px.pie(team_dnfs_accident, names='team_name', values='total_dnfs_accident',
                    title=f'Distribution of Total DNFS by Accident Among Teams in {selected_year}',
                    color='team_name',
                    color_discrete_map={team: team_colors[team] for team in team_dnfs_accident['team_name']})

        # Display the chart in the Streamlit app
        col3.plotly_chart(fig)


        #Distribution of dnfs by mechanical fault

        # Filter for DNFS by Mechanical Fault
        dnfs_mechanical = merged_drivers_selected_year[merged_drivers_selected_year['status'] == 'Mechanical']

        # Group by 'team_name' and count the number of DNFS by Mechanical Fault for each team
        team_dnfs_mechanical = dnfs_mechanical.groupby('team_name').size().reset_index(name='total_dnfs_mechanical')

        # Create a pie chart using Plotly Express
        fig = px.pie(team_dnfs_mechanical, names='team_name', values='total_dnfs_mechanical',
                    title=f'Distribution of Total DNFS by Mechanical Fault Among Teams in {selected_year}',
                    color='team_name',
                    color_discrete_map={team: team_colors[team] for team in team_dnfs_mechanical['team_name']})

        # Display the chart in the Streamlit app
        col4.plotly_chart(fig)

        #Point variation per team per week

        # Group by 'team_name' and 'round' and sum the points for each team in each round
        team_points_per_round = merged_drivers_selected_year.groupby(['team_name', 'round'])['points'].sum().reset_index()

        # Create a line chart using Plotly Express
        fig = px.line(team_points_per_round, x='round', y='points', color='team_name',
                    title=f'Total Points Variation per Team per Round',
                    labels={'points': 'Total Points', 'round': 'Round', 'team_name': 'Team Name'},
                    color_discrete_map=team_colors) 
        
        fig.update_layout(width=1400)
        # Display the chart in the Streamlit app
        st.plotly_chart(fig)

        

    else:
        #Row A
        #Initializing the columns
        col1, col2, col3 = st.columns(3)

        # Filter data for the selected year
        selected_year_data = merged_drivers[merged_drivers['year'] == selected_year]

        # Column 1
        constructor_pic = constructor_logos.get(selected_constructor)
        col1.image(constructor_pic, use_column_width=True)

        
        # Column 2
        # #Constructor Information
        #Constructor's Origin Country
        selected_const_nationality = selected_year_data.loc[selected_year_data['team_name'] == selected_constructor, 'nationality_y'].iloc[0]
        selected_const_emoji = driver_nations.get(selected_const_nationality, '')
        col2.metric("Driver Nationality", f"{selected_const_nationality} \n {selected_const_emoji}")

        # Column 3
        liveries = constructor_liveries.get(selected_constructor)
        col3.markdown(f"{selected_constructor}'s Car Livery")
        col3.markdown("")
        col3.markdown("")
        col3.markdown("")
        col3.image(liveries, use_column_width=True)

        


        #Displaying in the constructors tab
        
        #Row B
        st.subheader(f"{selected_constructor}'s Driver Lineup:")
        driver_photos_dict = driver_photos_2022 if selected_year == 2022 else driver_photos_2023

        # Filter drivers based on selected constructor
        selected_team_data = selected_year_data[selected_year_data['team_name'] == selected_constructor]

        # Display driver photos and information in three columns
        col5, col6, col7 = st.columns(3)

        driver1 = None
        driver2 = None

        # Loop through the selected_team_data to assign drivers to variables
        for index, row in selected_team_data.iterrows():
            driver_name = row['driver_name']
            if driver_name in driver_photos_dict:
                if driver1 is None:
                    driver1 = (driver_name, driver_photos_dict[driver_name], row['number'])
                else:
                    driver2 = (driver_name, driver_photos_dict[driver_name], row['number'])
                    break  # Exit the loop after finding two drivers

        # Display drivers in specific columns
        if driver1:
            col5.image(driver1[1], caption=driver1[0], use_column_width=True)

        if driver2:
            col7.image(driver2[1], caption=driver2[0], use_column_width=True)

        # Display driver information using st.metric in the middle column
        if driver1:
            col6.metric("Left Driver's Name", value=f"⬅️{driver1[0]}")
            col6.metric(label=driver1[0], value=f"Driver Number: {driver1[2]}")

        col6.markdown("")

        if driver2:
            col6.metric("Right Driver's Name", value=f"{driver2[0]}➡️")
            col6.metric(label=driver1[0], value=f"Driver Number: {driver2[2]}")



        ######## Stage 1 - Points throughout the Championship Rounds ########

        #Point variation per team per week
        # Filter data for the selected team
        selected_team_data = selected_year_data[selected_year_data['team_name'] == selected_constructor]

        # Get the color for the selected team from the team_colors dictionary
        selected_team_color = team_colors.get(selected_constructor, 'default_color')

        # Group by 'round' and sum the points for the selected team in each round
        team_total_points_per_round = selected_team_data.groupby('round')['points'].sum().reset_index()

        # Create a line chart using Plotly Express
        fig = px.line(team_total_points_per_round, x='round', y='points',
                    title=f'Total Points Variation for {selected_constructor} per Round',
                    labels={'points': 'Total Points', 'round': 'Round'},
                    line_shape="linear", line_dash_sequence=['solid'], color_discrete_sequence=[selected_team_color])

        fig.update_layout(width=1400)

        # Display the chart in the Streamlit app
        st.plotly_chart(fig)



        ######## Stage 2 - Average Quali Position per Round
        
        # Get the color for the selected team from the team_colors dictionary
        selected_team_color = team_colors.get(selected_constructor, 'default_color')

        # Group by 'round' and sum the points for the selected team in each round
        team_total_points_per_round = selected_team_data.groupby('round')['grid'].mean().reset_index()

        # Create a line chart using Plotly Express
        fig = px.line(team_total_points_per_round, x='round', y='grid',
                    title=f'Average Qualifying Position Variation for {selected_constructor} per Round',
                    labels={'grid': 'Grid Position', 'round': 'Round'},
                    line_shape="linear", line_dash_sequence=['solid'], color_discrete_sequence=[selected_team_color])

        fig.update_layout(width=1400)

        # Invert the y-axis order
        fig.update_yaxes(autorange="reversed")
        # Display the chart in the Streamlit app
        st.plotly_chart(fig)


        


elif option_chosen == 'Grand Prix Information':
    selected_gp = st.selectbox("Select the Grand Prix you want to view:", merged_drivers['gp_name'].sort_values().unique().tolist(), 
                                   index=0, key="gp_selectbox")
    
    # Use loc to select columns related to the selected Grand Prix
    selected_gp_info = merged_drivers.loc[merged_drivers['gp_name'] == selected_gp,
                                        ['gp_name', 'gp_date', 'track_name', 'location_y', 'country_y', 'time']]
   
    selected_gp_info = pd.merge(selected_gp_info, n2k[['gp_name', 
                                                       'traction', 
                                                       'track_evolution',
                                                       'braking',
                                                       'asphalt_grip',
                                                       'lateral',
                                                       'asphalt_abrasion',
                                                       'tyre_stress',
                                                       'downforce',
                                                       'c1_compound',
                                                       'c2_compound',
                                                       'c3_compound',
                                                       'c4_compound',
                                                       'c5_compound',
                                                       'laps',
                                                       'race_dist',
                                                       'circuit_length',
                                                       'turns',
                                                       'elevation_change',
                                                       'top_speed']], on='gp_name', how='left')
    
    selected_gp_info = selected_gp_info.groupby(['gp_name', 'gp_date']).agg({
        'track_name': 'first',
        'location_y': 'first',
        'country_y': 'first',
        'time': 'first',
        'traction': 'first', 
        'track_evolution':'first',
        'braking':'first',
        'asphalt_grip':'first',
        'lateral':'first',
        'asphalt_abrasion':'first',
        'tyre_stress':'first',
        'downforce':'first',
        'c1_compound':'first',
        'c2_compound':'first',
        'c3_compound':'first',
        'c4_compound':'first',
        'c5_compound':'first',
        'laps':'first',
        'race_dist':'first',
        'circuit_length':'first',
        'turns':'first',
        'elevation_change':'first',
        'top_speed':'first'}).reset_index()


    #initializing columns
    col1, col2 = st.columns(2)

    #Track Information
    track_name_metric = selected_gp_info['track_name'].iloc[0]
    # Display the track name using metric
    col1.metric("Venue Name:", track_name_metric)

    #Location Information
    track_cnt_metric = selected_gp_info['country_y'].iloc[0]
    # Display the track name using metric
    col1.metric("Country", track_cnt_metric)
    #Track Information
    track_loc_metric = selected_gp_info['location_y'].iloc[0]
    # Display the track name using metric
    col1.metric("City", track_loc_metric)



    #Gp date
    gp_date = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'gp_date'].iloc[0]

    gp_date_str = gp_date.strftime('%d-%m-%Y')  # Convert Timestamp to string

    # Display the date using metric
    col2.metric(f"{selected_gp}'s Date", gp_date_str)

    #Gp Time
    gp_hours = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'time'].iloc[0]

    # Display the date using metric
    col2.metric(f"{selected_gp}'s Start Time (GMT)", gp_hours)

    #Displaying track length
    gp_length = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'circuit_length'].iloc[0]
    col2.metric(f"{track_name_metric}'s Track Length", value=f"{gp_length} km")

    #Laps
    gp_laps = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'laps'].iloc[0]

    # Display the date using metric
    col2.metric(f"{selected_gp}'s Total laps", value=f"{gp_laps}")

    # Display selected Grand Prix information
    if not selected_gp_info.empty:

        # Display track map image if available
        selected_track = selected_gp_info['track_name'].iloc[0]
        track_map_path = track_maps.get(selected_track)

        if track_map_path:
            st.subheader(f"{selected_gp}")
            st.markdown(f"{selected_track}'s track map")
            st.image(track_map_path, use_column_width=True)
        else:
            st.warning(f"No track map available for {selected_track}")
    else:
        st.warning("Please select a Grand Prix from the dropdown.")

    #Creating more columns
    col3, col4, col5 = st.columns(3)

    # Define the compound columns
    compound_columns = ['c1_compound', 'c2_compound', 'c3_compound', 'c4_compound', 'c5_compound']

    # Initialize variables to store softest, medium, and hardest compounds
    soft_compound = None
    medium_compound = None
    hard_compound = None

    # Iterate through the compound columns to find the first occurrence of each type
    for compound_column in compound_columns:
        if selected_gp_info[compound_column].iloc[0] == 1:
            if soft_compound is None:
                soft_compound = compound_column
            elif medium_compound is None:
                medium_compound = compound_column
            elif hard_compound is None:
                hard_compound = compound_column
            else:
                break  # Exit the loop after finding soft, medium, and hard compounds

    # Display the tyre information with capitalized names
    col3.metric("Soft Tyre", soft_compound.replace('_compound', ' Compound').capitalize() if soft_compound else "")
    col3.metric("Medium Tyre", medium_compound.replace('_compound', ' Compound').capitalize() if medium_compound else "")
    col3.metric("Hard Tyre", hard_compound.replace('_compound', ' Compound').capitalize() if hard_compound else "")
    
    #Characteristics of the circuit
    #Laps
    gp_ts = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'top_speed'].iloc[0]

    # Display the date using metric
    col4.metric("Top Speed", value=f"{gp_ts} km/h")

    #Turns
    gp_turns = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'turns'].iloc[0]

    # Display the date using metric
    col4.metric("Turns", value=f"{gp_turns}")



    ##########
    #race Dist
    gp_dist = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'race_dist'].iloc[0]

    # Display the date using metric
    col5.metric(f"{selected_gp}'s Total Length", value=f"{gp_dist} km")

    #Elevation Change
    gp_elev = selected_gp_info.loc[selected_gp_info['gp_name'] == selected_gp, 'elevation_change'].iloc[0]

    # Display the date using metric
    col5.metric(f"{track_name_metric}'s elevation change ", value=f"{gp_elev} m")



elif option_chosen is None:
    st.sidebar.write("Select an option to display relevant content")
    st.header("Data Hub")
    st.subheader("Use the sidebar selectbox to your left to select what data you want to see!")
    st.markdown("")
    st.markdown("")
    st.markdown("")

    st.image("https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2022/07/01142406/Lewis-Hamilton-pointing-finger-at-crowd-planetF1.jpg")


####To Finish Off the Sidebar with Trademark
st.sidebar.markdown('''
---
Website developed for the \n Capstone Project Course
                
                    © AiTHLETES  
''')


st.sidebar.markdown("Social Media Links")


st.sidebar.markdown('<a href="https://twitter.com/AiTHLETS" target="_blank"><img src="https://img.freepik.com/vetores-gratis/novo-design-de-icone-x-do-logotipo-do-twitter-em-2023_1017-45418.jpg?size=338&ext=jpg&ga=GA1.1.1412446893.1704585600&semt=ais" height="30" width="30" style="border-radius: 50%;"></a >'
                    '&nbsp;&nbsp;&nbsp;'
                        '<a href="https://www.instagram.com/f1_aithletes/" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" height="30" width="30" style="border-radius: 50%;"></a>', unsafe_allow_html=True)
                        