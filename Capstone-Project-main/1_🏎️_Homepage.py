import streamlit as st
from streamlit_option_menu import option_menu 
import json
import hashlib

teams = ['Mercedes', 'Red Bull',
         'McLaren', 'Aston Martin',
         'AlphaTauri', 'Haas F1 Team',
         'Alpine F1 team', 'Williams',
         'Ferrari', 'Alfa Romeo']

drivers = ['Daniel Ricciardo', 'Lando Norris',
           'Lewis Hamilton', 'George Russell',
           'Alexander Albon', 'Carlos Sainz',
           'Charles Leclerc', 'Esteban Ocon',
           'Fernando Alonso', 'Lance Stroll',
           'Valtteri Bottas', 'Guanyu Zhou',
           'Sergio Pérez', 'Max Verstappen',
           'Nico Hülkenberg', 'Pierre Gasly',
           'Yuki Tsunoda', 'Nicholas Latifi',
           'Kevin Magnussen']

nations = ['United States', 'Afghanistan', 'Albania',
           'Algeria', 'American Samoa', 'Andorra',
           'Angola', 'Anguilla', 'Antarctica',
           'Antigua And Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Australia', 'Austria',
           'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
           'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia And Herzegowina',
           'Botswana', 'Bouvet Island', 'Brazil', 'Brunei Darussalam',
           'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon',
           'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Rep', 
           'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos Islands',
           'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica',
           'Cote D`ivoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
           'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
           'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea',
           'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)',
           'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana',
           'French Polynesia', 'French S. Territories', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland',
           'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-bissau',
           'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland',
           'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
           'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 
           'Korea (North)', 'Korea (South)', 'Kuwait', 'Kyrgyzstan', 'Laos',
           'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein',
           'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 
           'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands',
           'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco',
           'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
           'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua',
           'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea',
           'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal',
           'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 
           'Rwanda', 'Saint Kitts And Nevis', 'Saint Lucia', 'St Vincent/Grenadines',
           'Samoa', 'San Marino', 'Sao Tome', 'Saudi Arabia', 'Senegal', 'Seychelles',
           'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands',
           'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'St. Helena', 'St.Pierre',
           'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic',
           'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tokelau',
           'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City State', 'Venezuela', 
           'Viet Nam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 
           'Western Sahara', 'Yemen', 'Yugoslavia', 'Zaire', 'Zambia', 'Zimbabwe']



######## Setting a new style for the page ########
st.set_page_config(
    layout='wide',
    page_title='AiTHLETES F1 Hub | Homepage',
    page_icon="🏎️",
    initial_sidebar_state='collapsed',
    #menu_items = {'item': 'link'} could be interesting to explore (top right corner)
)


######## Setting a new style for the page ########
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h2 style='font-weight: bold;'>Welcome to the AiTHLETES Formula One Hub!</h2>", unsafe_allow_html=True)


# Load users if file exists, else create an empty dictionary
try:
    with open('users.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False

def register(username, password):
    if username in users:
        return False
    else:
        users[username] = password
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True

def display_home_page():
       
    # Add your news content here
    st.title("Latest News!")
    st.subheader("Verstappen's winning streak keeps on going as he wins in Spa!")
    st.image("https://www.autoracing1.com/wp-content/uploads/2023/f1/spa/podium2.jpg", width=1150)
    
    st.subheader("It's a disappointing drive from Daniel Ricciardo as he finishes below his teammate for the first time of the year!")
    st.image("https://i.guim.co.uk/img/media/d7be378ebe1048d91fee6e3dc2b53432a1c6acd2/0_0_5413_3248/master/5413.jpg?width=465&dpr=1&s=none", width=1150)

def display_registration_page():

    menu = ["Login", "SignUp"]
    choice = st.radio("", menu)

    if choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')
                
        if st.button("Login"):
            if authenticate(username, password):
                st.success("Logged In as {}".format(username))
            else:
                st.warning("Incorrect Username/Password")
    elif choice == "SignUp":
        
        st.subheader("Create New Account")
        
        new_user = st.text_input("Enter username")
        new_password = st.text_input("Enter a password", type='password')
        
        name = st.text_input("Insert your first name")
        surname = st.text_input("Insert your last name")
        
        birthday = st.date_input("Select your birthday", min_value=None, max_value=None, key=None, help="")
              
        

        nationality = st.selectbox("Select your nationality", nations)
        
        fav_team = st.selectbox("Select your favorite constructor's team:", teams)
        fav_driver = st.selectbox("Select your favorite driver:", drivers)

        if st.button("SignUp"):
            if register(new_user, new_password):
                st.success("You have successfully created an account")
                st.info("Go to Login Menu to login")
            else:
                st.warning("Username already exists")






def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return True
    else:
        return False

def register(username, password, name, surname, birthday, nationality, fav_team, fav_driver ):
    if username in users:
        return False
    else:
        users[username] = {"password": password, 
                           "name": name,
                           "surname": surname,
                           "password": password,
                           "birthday": birthday,
                           "nationality": nationality,
                           "fav_team": fav_team,
                           "fav_driver": fav_driver}
        
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return True




import datetime
import os
import base64

def display_profile_settings(username):
    st.subheader("Profile Settings for {}".format(username))
    user_data = users.get(username, {})

    
    if st.button("Change Password"):
        # Fetch user data
        current_password = st.text_input("Current Password", type='password')
        new_password = st.text_input("New Password", type='password')
        confirm_new_password = st.text_input("Confirm New Password", type='password')

        if st.button("Update Password"):
            if authenticate(username, current_password):
                if new_password == confirm_new_password:
                # Update the hashed password in your user data
                    users[username]["password"] = new_password
                    with open('users.json', 'w') as f:
                        json.dump(users, f)
                    st.success("Password updated successfully!")
                else:
                    st.warning("New Passwords do not match.")
            else:
                st.warning("Incorrect Current Password")
                
    
    user_image_path = user_data.get("profile_image", "")

    if st.button('Upload your profile picture'):
        
        uploaded_image = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"])
    
        st.markdown('Insert your profile picture below:')
        if st.button("Change Profile Image"):       
            if uploaded_image is not None:
            # Save the uploaded image locally
                uploads_folder = "uploads"
                os.makedirs(uploads_folder, exist_ok=True)
                user_image_path = os.path.join(uploads_folder, f"{username}_profile_image.png")
                uploaded_image.save(user_image_path)
                st.success("Profile Image uploaded successfully!")
            
        if os.path.exists(user_image_path):
            with open(user_image_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                st.image(f"data:image/png;base64,{img_base64}", caption="Profile Image", use_column_width=True)
            
        



    if st.button('Add cellphone number'):
    # Display user email
        user_number = user_data.get("number", "")
        new_number = st.text_input("Number", value=user_number)
        if st.button("Add number"):
            users[username]["number"] = new_number
            with open('users.json', 'w') as f:
                json.dump(users, f)
            st.success("Email added successfully!")

    # You can add more profile settings here based on your requirements


def main():
    menu_options = ["Home", "Registration", 'Settings']
    selected_option = option_menu("Select Menu", menu_options, orientation="horizontal")

  

    if selected_option == "Home":
            display_home_page()
    elif selected_option == 'Settings':
            display_profile_settings(username='F1 Fan')
    elif selected_option == "Registration":
            display_registration_page()



                
                
                


if __name__ == "__main__":
    main()








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
                        