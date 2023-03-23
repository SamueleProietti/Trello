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

st.set_page_config(page_title="Bacheche", page_icon="📋", layout="wide")
st.title("Le mie Bacheche")
  #firbase key
if check_password():
    docs = db.collection(u'lista_bacheche').stream()
    prodotti = ['']
    for doc in docs:
        prodotti.append(doc.id)
    st.header('Crea scheda')
    bacheca = st.selectbox('Seleziona la bacheca', prodotti)
        
        
    if bacheca !='':
        st.header(bacheca)
        
    col1, col2, col3 = st.columns(3)
 
    with col1:
        if bacheca != '':
            st.subheader("Da Fare")
            # --- Modalità di lettura di una specifica raccolta all'interno del database
            doc_ref = db.collection(bacheca + '-da_fare')
            # --- Modalità di lettura dei documenti all'interno della raccolta
            docs = doc_ref.stream()

            # --- Costruzione di una tabella dei dati del database
            fare = []
            for doc in docs:
                #st.write(doc)
                fare_dict = {'scheda': doc.id, 'descrizione': doc.to_dict()['descrizione']}
                fare.append(fare_dict)

            if fare!=[]:
                data = pd.DataFrame(fare)
                gd = GridOptionsBuilder.from_dataframe(data)
                gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                gd.configure_grid_options(enableCellTextSelection=True)
                gd.configure_grid_options(ensureDomOrder=True)
                gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

                gridOptions = gd.build()

                table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)

                selected = table['selected_rows']
                
                if st.button('Sposta scheda in Esecuzione'):
                    for dict in selected:
                          
                        db.collection(bacheca + '-in_esecuzione').document(dict['scheda']).set({ 
                            'descrizione': dict['descrizione'],
                            })
                        db.collection(bacheca + '-da_fare').document(dict['scheda']).delete()

                        st.success('Spostamento effettuato')
                        st.success('Eliminazione effettuata')
                        time.sleep(1)
                        st.experimental_rerun()

            else:
                st.warning('Nessuna scheda registrata')         
    with col2:
            
        if bacheca != '':
            st.subheader("In Esecuzione")
            # --- Modalità di lettura di una specifica raccolta all'interno del database
            doc_ref = db.collection(bacheca + '-in_esecuzione')
            # --- Modalità di lettura dei documenti all'interno della raccolta
            docs = doc_ref.stream()

            # --- Costruzione di una tabella dei dati del database
            esecuzione = []
            
            for doc in docs:
                #st.write(doc)
                esecuzione_dict = {'scheda': doc.id, 'descrizione': doc.to_dict()['descrizione']}
                esecuzione.append(esecuzione_dict)

            if esecuzione!=[]:
                data = pd.DataFrame(esecuzione)
                gd = GridOptionsBuilder.from_dataframe(data)
                gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                gd.configure_grid_options(enableCellTextSelection=True)
                gd.configure_grid_options(ensureDomOrder=True)
                gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

                gridOptions = gd.build()

                table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)

                selected = table['selected_rows']
                
                if st.button('Sposta scheda in Fatto'):
                    for dict in selected:
                          
                        db.collection(bacheca + '-fatto').document(dict['scheda']).set({ 
                            'descrizione': dict['descrizione'],
                            })
                        db.collection(bacheca + '-in_esecuzione').document(dict['scheda']).delete()

                        st.success('Spostamento effettuato')
                        st.success('Eliminazione effettuata')
                        time.sleep(1)
                        st.experimental_rerun()

            else:
                st.warning('Nessuna scheda registrata') 
    with col3:
            
        if bacheca != '':
            st.subheader("Fatto")
            # --- Modalità di lettura di una specifica raccolta all'interno del database
            doc_ref = db.collection(bacheca + '-fatto')
            # --- Modalità di lettura dei documenti all'interno della raccolta
            docs = doc_ref.stream()

            # --- Costruzione di una tabella dei dati del database
            fatto = []
            
            for doc in docs:
                #st.write(doc)
                fatto_dict = {'scheda': doc.id, 'descrizione': doc.to_dict()['descrizione']}
                fatto.append(fatto_dict)

            if fatto!=[]:
                data = pd.DataFrame(fatto)
                gd = GridOptionsBuilder.from_dataframe(data)
                gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                gd.configure_grid_options(enableCellTextSelection=True)
                gd.configure_grid_options(ensureDomOrder=True)
                gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

                gridOptions = gd.build()

                table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)

                selected = table['selected_rows']
                
                if st.button('Elimina Scheda'):
                    for dict in selected:
                          
                        db.collection(bacheca + '-fatto').document(dict['scheda']).delete()

                        st.success('Eliminazione effettuata')
                        time.sleep(1)
                        st.experimental_rerun()

            else:
                st.warning('Nessuna scheda registrata')