import streamlit as st
import pandas as pd

#pip3 install openpyxl  

uploaded_file = "filtered_tweets_engie_cleaned.xlsx"
df = pd.read_excel(uploaded_file)

with st.sidebar:
    options = ["Problèmes de facturation", "Pannes et urgences", "Service client injoignable", "Problèmes avec l’application", "Délai d’intervention"]
    selection = st.pills("Catégories", options, selection_mode="multi")

if "Problèmes de facturation" in selection or selection == []:
    st.title('Dashboard Projet 48h')
    st.write('## Données')
    st.dataframe(df.head())  

    df_count = df.groupby("heure").size().reset_index(name='count')

    st.write('## Nombre de tweets par heure')
    st.bar_chart(df_count.set_index('heure'))
