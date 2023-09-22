import streamlit as st
import pandas as pd
from PIL import Image  # Import the Image module for working with images
import os
import requests
import datetime
import pytz
import sqlite3

# Load the logo image
logo_image = Image.open('unimelb_logo.JPG')

# Display the logo image in the top-left corner
st.image(logo_image, use_column_width=False, width=100)

# Load the CSV with software list
software_df = pd.read_csv('software_list.csv', encoding='ISO-8859-1')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .big-font {
                font-size:20px !important;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

DATABASE_NAME = "submissions.db"

def save_submission(username, subject_code, software_list):
    # Connect to the SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY,
        user_email TEXT NOT NULL,
        subject_code TEXT NOT NULL,
        software_list TEXT NOT NULL,
        DateTime TEXT NOT NULL
    )
    ''')

    # Get current datetime in Melbourne timezone
    melbourne_tz = pytz.timezone('Australia/Melbourne')
    current_datetime = datetime.datetime.now(melbourne_tz).strftime('%Y-%m-%d %H:%M:%S')

    # Insert the new submission
    cursor.execute('''
    INSERT INTO submissions (user_email, subject_code, software_list, DateTime)
    VALUES (?, ?, ?, ?)
    ''', (username, subject_code, ', '.join(software_list), current_datetime))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Check if the form was previously submitted
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    st.title("Thank You!")
    st.write("Thank you for your submission. The Software Licensing Team is reviewing the request and will get back to you shortly.")
else:
    st.write(
        "<h2 style='text-align: left; font-weight: bold;'>Lab Software Request Semester 1, 2024</h2>",
        unsafe_allow_html=True)

    st.write("""
It is important that we, as a University, submit our teaching software requirements in a timely manner. There are a number of reasons for this, including but not limited to, Cybersecurity checks, licensing requirements, and to package and deploy the software.

All of these take time, so by having your requests in with us by 30 November 2023 for Semester 1 2024, together we can ensure our students have a great learning experience.
""")

    # Message for submitting a form for each subject code
    st.markdown("""
    <div style="color: #f63366; background-color: #f0f2f6; padding: 10px; border-radius: 5px;">
        <b>Note:</b><br>
        1. If you manage multiple courses, submit a separate form for each subject's software request.<br>
        2. You can request up to 5 software per form.<br>
        3. The latest licensed version of the software will be installed.
    </div>
""", unsafe_allow_html=True)

    # User input with custom style
    st.markdown('<div class="big-font">Enter your email address: <i style="color:red;">*</i></div>', unsafe_allow_html=True)
    username = st.text_input("", key="email_input")

    st.markdown('<div class="big-font">Enter the course code: <i style="color:red;">*</i></div>', unsafe_allow_html=True)
    subject_code = st.text_input("", key="subject_code_input").upper()  # Convert subject code to uppercase

    st.markdown('<div class="big-font">How many specialist software do you require for the course this semester?</div>', unsafe_allow_html=True)
    num_software = st.number_input("", min_value=1, max_value=10, value=1, key="num_software_input")

    italic_select = '𝑆𝑒𝑙𝑒𝑐𝑡 𝑓𝑟𝑜𝑚 𝑑𝑟𝑜𝑝𝑑𝑜𝑤𝑛'
    software_options = [italic_select] + software_df['application-name'].tolist() + ['Other']
    software_selections = []

    for i in range(num_software):
        st.markdown(f'<div class="big-font">Select software {i+1}:</div>', unsafe_allow_html=True)
        software_choice = st.selectbox("", software_options, index=0, key=f"software_select_{i}")
        if software_choice == 'Other':
            st.markdown(f'<div class="big-font">Enter the name of software {i+1}:</div>', unsafe_allow_html=True)
            software_choice = st.text_input("", key=f"software_text_{i}")
        software_selections.append(software_choice)

    # Message for selecting 'Other' if software is not found
    st.markdown("""
    <div style="color: #f63366; background-color: #f0f2f6; padding: 10px; border-radius: 5px;">
        <b>Note:</b><br>If you are unable to find the software, please select 'Other' and enter the name of the software.</div>""", unsafe_allow_html=True)

    st.write("")
    if st.button("Submit"):
        if not username or not subject_code:
            st.warning("Please fill out the required fields!")
        elif '𝑆𝑒𝑙𝑒𝑐𝑡 𝑓𝑟𝑜𝑚 𝑑𝑟𝑜𝑝𝑑𝑜𝑤𝑛' in software_selections:
            st.warning("Please select a valid software!")
        else:
            save_submission(username, subject_code, software_selections)
            st.session_state.form_submitted = True
            st.experimental_rerun()
