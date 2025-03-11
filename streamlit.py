import streamlit as st
import pandas as pd

#pip3 install openpyxl  

class MyChart:
    def __init__(self, title, tags, chart_function):
        self.title = title
        self.tags = tags 
        self.chart_function = chart_function 

uploaded_file = "filtered_tweets_engie_cleaned.xlsx"
df = pd.read_excel(uploaded_file)

def nb_tweets_par_heure(df):
    df_count = df.groupby("heure").size().reset_index(name='count')
    st.write('## Nombre de tweets par heure')
    st.bar_chart(df_count.set_index('heure'))
 
def nb_tweets_par_mois(df):
    df_count = df.groupby("mois").size().reset_index(name='count')
    st.write('## Nombre de tweets par mois')
    st.bar_chart(df_count.set_index('mois'))

def camembert_sentiment(df):
    df_count = df.groupby("Sentiment").size().reset_index(name='count')
    st.write('## Répartition des Sentiments')
    st.pie_chart(df_count.set_index('Sentiment'))

st.title('Dashboard Projet 48h')
charts = [
    MyChart("Graphique 1", ["Temps", "Heure","Historigramme"], nb_tweets_par_heure),
    MyChart("Graphique 1", ["Temps","Mois","Historigramme"], nb_tweets_par_mois),
    MyChart("Graphique 3", ["Camembert", "Sentiment"], camembert_sentiment),
]

with st.sidebar:
    all_tags = sorted(set(tag for chart in charts for tag in chart.tags))
    selected_tags = st.multiselect("Filtrer par tags :", options=all_tags)

for chart in charts:
    if not selected_tags or any(tag in chart.tags for tag in selected_tags):
        fig = chart.chart_function(df)



