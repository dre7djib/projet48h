import streamlit as st
import pandas as pd
import plotly.express as px

#pip3 install streamlit
#pip3 install pandas
#pip3 install plotly
#pip3 install openpyxl  

class MyChart:
    def __init__(self, title, tags, chart_function):
        self.title = title
        self.tags = tags 
        self.chart_function = chart_function 

uploaded_file = "filtered_tweets_engie_cleaned.csv"
df = pd.read_csv('filtered_tweets_engie_cleaned.csv', sep=';')

def nb_tweets_par_heure(df):
    df_count = df.groupby("heure").size().reset_index(name='count')
    st.write('## Nombre de tweets par heure')
    st.bar_chart(df_count.set_index('heure'))
 
def nb_tweets_par_mois(df):
    df_count = df.groupby("mois").size().reset_index(name='count')
    st.write('## Nombre de tweets par mois')
    st.bar_chart(df_count.set_index('mois'))

def camembert_sentiment(df):
    df_count = df['Sentiment'].value_counts().reset_index()
    df_count.columns = ['Sentiment', 'count']
    st.write('## Répartition des Sentiments')
    fig = px.pie(df_count, names='Sentiment', values='count', title='Répartition des Sentiments')
    st.plotly_chart(fig)

def camembert_problématique(df):
    df_count = df['Problematique'].value_counts().reset_index()
    df_count.columns = ['Problematique', 'count']
    st.write('## Répartition des Problematique')
    fig = px.pie(df_count, names='Problematique', values='count', title='Répartition des Problematiques')
    st.plotly_chart(fig)

st.title('Dashboard Projet 48h')
charts = [
    MyChart("Graphique 1", ["Temps", "Heure","Historigramme"], nb_tweets_par_heure),
    MyChart("Graphique 2", ["Temps","Mois","Historigramme"], nb_tweets_par_mois),
    MyChart("Graphique 3", ["Camembert", "Sentiment"], camembert_sentiment),
    MyChart("Graphique 4", ["Camembert", "Problematique"], camembert_problématique)
]

with st.sidebar:
    all_tags = sorted(set(tag for chart in charts for tag in chart.tags))
    selected_tags = st.multiselect("Filtrer par tags :", options=all_tags)

for chart in charts:
    if not selected_tags or any(tag in chart.tags for tag in selected_tags):
        fig = chart.chart_function(df)



