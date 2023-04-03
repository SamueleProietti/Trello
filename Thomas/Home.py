import streamlit as st
from functions import autenticazione
from PIL import Image


st.set_page_config(page_title="Thomas", page_icon="🤖", layout="wide")

if autenticazione():
  st.title("Benvenuto in Thomas")

  image = Image.open('logo_thomas.png')

  st.image(image)


