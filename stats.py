import streamlit as st
import pandas as pd
from PIL import Image  # Import the Image module for working with images
import os
import requests
import datetime
import pytz
import base64  # Add this import statement


# Load the logo image
logo_image = Image.open('unimelb_logo.JPG')

# Display the logo image in the top-left corner
st.image(logo_image, use_column_width=False, width=100)

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

# Check if the submissions CSV exists
if os.path.exists('submissions.csv'):
    submissions_df = pd.read_csv('submissions.csv')
    #submissions_df['submission-date'] = pd.to_datetime(submissions_df['DateTime'])  # Convert to datetime
    submissions_df['submission-date'] = pd.to_datetime(submissions_df['DateTime'], format='%Y-%m-%d %H:%M:%S')

else:
    st.write("No submissions found!")
    st.stop()

# Title
st.write("<h2 style='text-align: left; font-weight: bold;'>Lab Software Request Semester 1, 2024 Visualizations</h2>", unsafe_allow_html=True)

# Create columns for the three numbers with borders
col1, col2, col3 = st.columns(3)

# Display the three numbers in very big, bold, italics with borders
tile_style = """
    border: 2px solid #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
"""

with col1:
    st.markdown('<div style="{}"><span style="font-size:20px; font-weight:bold;">Total Number of Responses</span><br><span style="font-size:40px; font-weight:bold; font-style:italic;">{}</span></div>'.format(tile_style, len(submissions_df)), unsafe_allow_html=True)

with col2:
    unique_apps_count = len(submissions_df['software-list'].str.split(', ').explode().unique())
    st.markdown('<div style="{}"><span style="font-size:20px; font-weight:bold;">Count of Unique Apps Requested</span><br><span style="font-size:40px; font-weight:bold; font-style:italic;">{}</span></div>'.format(tile_style, unique_apps_count), unsafe_allow_html=True)

with col3:
    unique_subject_codes = submissions_df['subject-code'].nunique()
    st.markdown('<div style="{}"><span style="font-size:20px; font-weight:bold;">Unique Subject Codes Submitted</span><br><span style="font-size:40px; font-weight:bold; font-style:italic;">{}</span></div>'.format(tile_style, unique_subject_codes), unsafe_allow_html=True)

# Display the table for apps vs count
st.subheader("Software vs Count")
software_counts = submissions_df['software-list'].str.split(', ').explode().value_counts().reset_index()
software_counts.columns = ['Software', 'Count']
st.write(software_counts)


# Display the table for all responses
st.subheader("All Responses")
st.write(submissions_df)

# Add a download button for the CSV file
st.subheader("Download all submissions")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"submissions-{current_datetime}.csv"

# Add a download button for the CSV file with the dynamic filename
if st.download_button("Download CSV", submissions_df.to_csv(index=False), key="download-csv", mime='text/csv', file_name=filename):
    pass  # Placeholder, no action needed here
