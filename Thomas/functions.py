import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import email_validator
import re

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
        st.error("Password Errata!!!")
        return False
    else:
        # Password correct.
        return True


def autenticazione():
    
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
    if not firebase_admin._apps:
        cred = credentials.Certificate('firestore-key.json')
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    def auth_entered():
        """Checks whether a password entered by the user is correct."""
        #if st.session_state["password"] == 'jesap':
        st.session_state["auth_correct"] = True
            #del st.session_state["password"]  # don't store password
        #else:
            #st.session_state["password_correct"] = False
            
    if "auth_correct" not in st.session_state:        
        
        def validazione_email(email):
            try:
                email_validator.validate_email(email)
                return True
            except email_validator.EmailNotValidError:
                return False
        # Authentication
        choice = st.radio('login/Signup', ['Login', 'Sign up'])
        
        # Obtain User Input for email and password
        email = st.text_input('Perfavore inserisci il tuo indirizzo email', key="email")
        password = st.text_input('Perfavore inserisci la password',type = 'password', key="password")
        # App 
        # Sign up Block
        if choice == 'Sign up':
            password_ripetuta = st.text_input('Perfavore ripeti la password',type = 'password', key="password2")
            submit = st.button('Crea il mio account')

            if submit:
                docs = db.collection(u'lista_mail').stream()
                mail = ['']
                mail_esistente = False
                for doc in docs:
                    mail.append(doc.id)
                for i in mail:
                    if i == email and email != '':
                        mail_esistente=True

                # Dividi l'indirizzo email sulla base dell'@ e del punto
                parts = email.split('@')[0].split('.')

                # Estrai il nome e il cognome dalla lista 'parts'
                nome = parts[0]
                cognome = parts[1]

                match = re.match(r"[^@]+@([^@]+\.[^@]+)", email)
                if password != password_ripetuta:
                    st.warning("⚠️ Errore nella creazione della password, non corrispondono le due password. Ricontrolla i campi!")
                elif match and match.group(1) != "jesap.it":
                    st.warning("⚠️ Email non autorizzata all'accesso, utilizza la mail jesap")
                elif mail_esistente:
                    st.warning('⚠️ Email già in uso')
                elif email == '':
                    st.warning('⚠️ Inserisci una email valida')
                elif not validazione_email(email): 
                    st.warning('⚠️ Formato email non valido')
                elif password == '':
                    st.warning('⚠️ Inserisci una password valida')
                else:
                    db.collection(u'lista_mail').document(email).set({
                                    'password': str(password),
                                    'nome': str(nome),
                                    'cognome': str(cognome)
                                    })
                    auth_entered()
                    st.experimental_rerun()
        # Login Block
        if choice == 'Login':
            
            col1, col2 = st.columns(2)
            with col1:
                login = st.button('Login')            
            with col2:
                st.write('Hai dimenticato la password?')
                reset = st.checkbox('Reset Password')
            if reset:
                email_reset = st.text_input('Perfavore inserisci il tuo indirizzo email', key="email_reset")
                password_reset = st.text_input('Perfavore inserisci la password',type = 'password', key="password_reset")
                password_ripetuta_reset = st.text_input('Perfavore ripeti la password',type = 'password', key="password2_reset")
                cambio_pass = st.button('Cambia Password')
                if cambio_pass:
                    docs = db.collection(u'lista_mail').stream()
                    mail = ['']
                    mail_esistente = False
                    for doc in docs:
                        mail.append(doc.id)
                    for i in mail:
                        if i == email_reset and email_reset != '':
                            mail_esistente=True

                    # Dividi l'indirizzo email sulla base dell'@ e del punto
                    parts = email_reset.split('@')[0].split('.')

                    # Estrai il nome e il cognome dalla lista 'parts'
                    nome = parts[0]
                    cognome = parts[1]

                    match = re.match(r"[^@]+@([^@]+\.[^@]+)", email_reset)
                    if password_reset != password_ripetuta_reset:
                        st.warning("⚠️ Errore nella creazione della password, non corrispondono le due password. Ricontrolla i campi!")
                    elif match and match.group(1) != "jesap.it":
                        st.warning("⚠️ Email non autorizzata all'accesso, utilizza la mail jesap")
                    elif not mail_esistente:
                        st.warning('⚠️ Email non presente nel sistema')
                    elif email_reset == '':
                        st.warning('⚠️ Inserisci una email valida')
                    elif not validazione_email(email_reset): 
                        st.warning('⚠️ Formato email non valido')
                    elif password_reset == '':
                        st.warning('⚠️ Inserisci una password valida')
                    else:
                        db.collection(u'lista_mail').document(email_reset).update({
                                        'password': str(password_reset),
                                        })
                        st.success('Cambio Password avvenuto con successo')
                #st.experimental_rerun()
                        
            if login:
                
                doc_ref = db.collection(u"lista_mail")
                docs = doc_ref.stream()
                credenziali = []
                for doc in docs:
                #st.write(doc)
                    credenziali_dict = {'mail': doc.id, 'password': doc.to_dict()['password']}
                    credenziali.append(credenziali_dict)
                    
                match_mail = False
                match_password = False
                for i in credenziali:
                    if i['mail'] == email:
                        match_mail = True
                        if i['password'] == password:
                            match_password = True
                            
                match = re.match(r"[^@]+@([^@]+\.[^@]+)", email)
                
                if match and match.group(1) != "jesap.it":
                    st.warning("⚠️ Email non autorizzata all'accesso, utilizza la mail jesap")            
                elif email == '':
                    st.warning('⚠️ Inserisci una email valida')
                elif password == '':
                    st.warning('⚠️ Inserisci una password valida')
                elif not validazione_email(email): 
                    st.warning('⚠️ Formato email non valido')
                elif match_mail == False:
                    st.error('⚠️ mail non valida, non presente nel sistema. Effettua prima il Sign Up')
                elif match_password == False:
                    st.error('⚠️ Password Errata!!!')
                elif match_mail==True and match_password==True:
                    auth_entered()
                    st.experimental_rerun()
                    
        return False
    else:
        # Password correct.
        return True
        
