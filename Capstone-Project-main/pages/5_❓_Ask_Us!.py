import streamlit as st
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import smtplib


# Connect to SQLite database
conn = sqlite3.connect('your_database_name.db')
c = conn.cursor()

# Functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT, title TEXT, question TEXT, qdate DATE)')

def add_data(author, title, question, qdate):
    c.execute('INSERT INTO blogtable(author, title, question, qdate) VALUES (?,?,?,?)', (author, title, question, qdate))
    conn.commit()

def view_all_questions():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def send_email(name, question_title, question, qdate):
    sender_email = "aithlets@gmail.com"  # Update with your Gmail email address
    receiver_email = "aithlets@gmail.com"

    subject = f"New Question from {name}"
    body = f"Name: {name}\nQuestion Title: {question_title}\nQuestion: {question}\nDate: {qdate}"

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Log in using an App Password
    app_password = 'hjbt ihzt tflw xdrr'  # Replace with the App Password you generated
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.ehlo()

        # Log in using App Password
        server.login(sender_email, app_password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

# Streamlit UI
create_table()

st.subheader("Do you have any questions? Feel free to ask us!")
st.markdown("")
st.markdown("Fill in the form below!")
st.markdown("")

# Asking the user to insert his name
name = st.text_input("Name:", max_chars=40)
# Title of the request
question_title = st.text_input("State your question briefly (Title of your Request)", max_chars=100)
# Corpus of the question
question = st.text_area("Insert your question explained here")
# Entering date
qdate = st.date_input("Enter the current date:")

if st.button("Add"):
    with conn:
        add_data(name, question_title, question, qdate)
        send_email(name, question_title, question, qdate)
        st.write(f"Question: {question_title} Saved and sent to your company email.")

# Close the connection when done
conn.close()

######## Setting a new style for the page ########
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
                        