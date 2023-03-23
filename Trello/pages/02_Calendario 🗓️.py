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




if check_password():
    # Crea un dataframe per memorizzare gli eventi del calendario
    #df = pd.DataFrame(columns=['data', 'evento'])
    if not firebase_admin._apps:
        cred = credentials.Certificate('firestore-key.json')
        firebase_admin.initialize_app(cred)
        # Crea un elenco di mesi e anni
    mesi = [calendar.month_name[i] for i in range(1, 13)]
    anni = [anno for anno in range(date.today().year, date.today().year + 10)]

    # Crea la pagina Streamlit
    st.set_page_config(page_title="Calendario Aziendale", page_icon="🗓️", layout="wide")
    st.title("Calendario Aziendale")

    # Crea i selettori per il mese e l'anno
    col1, col2 = st.columns(2)
    with col1:
        mese = st.selectbox("Seleziona il mese", mesi)
    with col2:
        anno = st.selectbox("Seleziona l'anno", anni)

    # Ottieni il numero del mese selezionato
    numero_mese = list(calendar.month_name).index(mese)

    # Crea il calendario per il mese e l'anno selezionati
    calendario = calendar.monthcalendar(anno, numero_mese)

    # Crea una tabella con il calendario
    colonne = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
    tabella_calendario = pd.DataFrame(calendario, columns=colonne)
    tabella_calendario.replace(0, "", inplace=True)
    st.table(tabella_calendario)

    # Crea un campo di input per gli eventi
    data_ev = st.date_input("Aggiungi la data", datetime.date(2023, 3, 20))
    evento = st.text_input("Aggiungi un evento")
    descrizione = st.text_input("Aggiungi una descrizione")
    
    db = firestore.client()

    # Crea un pulsante per salvare l'evento nel dataframe
    if st.button("Aggiungi evento"):
        if evento == '':
            st.warning('⚠️ Inserisci un nome valido')
        else:
            
            db.collection(u"eventi").document(evento).set({   
                            'descrizione': str(descrizione),
                            'data': str(data_ev),
                            })
            st.success("Evento aggiunto")
        
    # --- Modalità di lettura di una specifica raccolta all'interno del database
    doc_ref = db.collection("eventi")
    # --- Modalità di lettura dei documenti all'interno della raccolta
    docs = doc_ref.stream()

    # --- Costruzione di una tabella dei dati del database
    people = []
    for doc in docs:
    #st.write(doc)
        people_dict = {'evento': doc.id, 'descrizione': doc.to_dict()['descrizione'], 'data': doc.to_dict()['data']}
        people.append(people_dict)

    if people!=[]:
        data = pd.DataFrame(people)
        gd = GridOptionsBuilder.from_dataframe(data)
        gd.configure_selection(selection_mode='multiple', use_checkbox=True)
        gd.configure_grid_options(enableCellTextSelection=True)
        gd.configure_grid_options(ensureDomOrder=True)
        gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

        gridOptions = gd.build()

        table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)

        selected = table['selected_rows']
    
        if st.button('Elimina eventi selezionati'):
            for dict in selected:
                db.collection('eventi').document(dict['evento']).delete()

                st.success('Eliminazione effettuata')
                time.sleep(1)
                st.experimental_rerun()

    else:
        st.warning('Nessun evento registrato')
        
    

