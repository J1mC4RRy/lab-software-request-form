import streamlit as st
import pandas as pd
from PIL import Image  # Import the Image module for working with images
import os
import requests
import datetime
import pytz

pwd = os.getcwd

# Load the logo image
# logo_image = Image.open(pwd+ '\\unimelb_logo.jpg')
#logo_path = os.path.join(os.getcwd(), 'unimelb_logo.jpg')
#logo_image = Image.open(logo_path)

#path = os.path.dirname(__file__)
logo_image = pwd +'/unimelb_logo.jpg'


# Display the logo image in the top-left corner
st.image(logo_image, use_column_width=False, width=100)


# # Constants for Azure AD authentication
# CLIENT_ID = 'api://6c608245-0a3e-4c09-b9ca-a56a80a234f1'
# REDIRECT_URI = 'https://lab-software-request-form.streamlit.app/'
# AUTH_URL = 'https://login.microsoftonline.com/c99775de-bb20-4d91-ba77-dff350f59dd4/oauth2/v2.0/authorize'
# TOKEN_URL = 'https://login.microsoftonline.com/c99775de-bb20-4d91-ba77-dff350f59dd4/oauth2/v2.0/token'

# def get_login_url():
#     params = {
#         'client_id': CLIENT_ID,
#         'response_type': 'code',
#         'redirect_uri': REDIRECT_URI,
#         'scope': 'User.Read',
#         'response_mode': 'query'
#     }
#     return AUTH_URL + '?' + '&'.join(f'{k}={v}' for k, v in params.items())

# def get_token_from_code(code):
#     data = {
#         'client_id': CLIENT_ID,
#         'code': code,
#         'redirect_uri': REDIRECT_URI,
#         'grant_type': 'authorization_code'
#     }
#     response = requests.post(TOKEN_URL, data=data)
#     return response.json().get('access_token')

# # Check if user is authenticated
# if 'access_token' not in st.session_state:
#     # If code is in the URL params, user is returning from authentication
#     code = st.experimental_get_query_params().get('code')
#     if code:
#         st.session_state.access_token = get_token_from_code(code[0])
#     else:
#         st.write("Please login to continue.")
#         st.write(f"[Login with Microsoft]({get_login_url()})")
#         st.stop()
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

def save_submission(username, subject_code, software_list):
    # Check if the submissions CSV exists
    if os.path.exists('submissions.csv'):
        submissions_df = pd.read_csv('submissions.csv')
    else:
        submissions_df = pd.DataFrame(columns=['user-email', 'subject-code', 'software-list', 'DateTime'])  # Add 'DateTime' column
    
    # Get current datetime in Melbourne timezone
    melbourne_tz = pytz.timezone('Australia/Melbourne')
    current_datetime = datetime.datetime.now(melbourne_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # Append the new submission
    submissions_df = submissions_df.append({
        'user-email': username, 
        'subject-code': subject_code, 
        'software-list': ', '.join(software_list),
        'DateTime': current_datetime  # Add this line
    }, ignore_index=True)
    submissions_df.to_csv('submissions.csv', index=False)

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

#st.markdown('<a href="pages/privacy_policy.html" target="_blank">Privacy Policy</a>', unsafe_allow_html=True)


