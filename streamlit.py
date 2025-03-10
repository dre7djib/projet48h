import streamlit as st
import pandas as pd


uploaded_file = "filtered_tweets_engie_cleaned.xlsx"
df = pd.read_excel(uploaded_file)

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.title('Dashboard Projet 48h')

st.write('## Données')
st.dataframe(df.head())  

df_count = df.groupby("heure").size().reset_index(name='count')

st.write('## Nombre de tweets par heure')
st.bar_chart(df_count.set_index('heure'))
