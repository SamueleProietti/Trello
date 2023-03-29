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
import email_validator
import pyrebase

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == 'jesap':
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def autenticazione():
    if not firebase_admin._apps:
        cred = credentials.Certificate('firestore-key.json')
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    def validazione_email(email):
        try:
            email_validator.validate_email(email)
            return True
        except email_validator.EmailNotValidError:
            return False
        
    

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

    # Firebase Authentication
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()


    # Authentication
    choice = st.radio('login/Signup', ['Login', 'Sign up'])

    # Obtain User Input for email and password
    email = st.text_input('Perfavore inserisci il tuo indirizzo email', key="email")
    password = st.text_input('Perfavore inserisci la password',type = 'password', key="password")


    # App 

    # Sign up Block
    if choice == 'Sign up':
        handle = st.text_input('Per favore inserisci il tuo nome', value='Default')
        submit = st.button('Crea il mio account')

        if submit:
            if not validazione_email(email): 
                st.warning('⚠️ Formato email non valido')
            if email == '':
                st.warning('⚠️ Inserisci una email valida')
            if password == '':
                st.warning('⚠️ Inserisci una password valida')
            else:
                user = auth.create_user_with_email_and_password(email, password)
                db.collection(u'lista_mail').document(email).set({
                                'password': str(password),
                                'handle': str(handle),
                                })
            
                # Sign in
                user = auth.sign_in_with_email_and_password(email, password)
                #db.child(user['localId']).child("Handle").set(handle)
                #db.child(user['localId']).child("ID").set(user['localId']
                return True
    # Login Block
    if choice == 'Login':
        login = st.button('Login')
        if login:
            user = auth.sign_in_with_email_and_password(email,password)
            return True
