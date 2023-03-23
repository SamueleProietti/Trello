import streamlit as st
import time
import pandas as pd
import calendar
from datetime import date
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
from functions import check_password
import pyrebase

if not firebase_admin._apps:
    cred = credentials.Certificate('firestore-key.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title="Trello 2.0", page_icon="🤖", layout="wide")
st.title("Welcome to Trello 2.0")
  #firbase key
firebaseConfig = {
  'apiKey': "AIzaSyDPvww8RG0oRSdq3_3Ytp2b2aYOSqVuQxA",
  'authDomain': "prova-1091e.firebaseapp.com",
  'databaseURL': "https://prova-1091e-default-rtdb.europe-west1.firebasedatabase.app", 
  'projectId': "prova-1091e",
  'storageBucket': "prova-1091e.appspot.com",
  'messagingSenderId': "996283803718",
  'appId': "1:996283803718:web:2cf52008aea3fb0fa80247",
  'measurementId': "G-CC19K9JRN2"
}


###################################################################################################################
# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# Authentication
choice = st.radio('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.text_input('Please enter your email address')
password = st.text_input('Please enter your password',type = 'password')

# App 

# Sign up Block
if choice == 'Sign up':
    handle = st.text_input(
        'Please input your app handle name', value='Default')
    submit = st.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created suceesfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + handle)
        st.info('Login via login drop down selection')

# Login Block
if choice == 'Login':
    login = st.button('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email,password)
###################################################################################################################
