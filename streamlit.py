import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import requests

#pip3 install streamlit
#pip3 install pandas
#pip3 install plotly
#pip3 install openpyxl  

geolocator = Nominatim(user_agent="myGeocoder")

class MyChart:
    def __init__(self, title, tags, chart_function):
        self.title = title
        self.tags = tags 
        self.chart_function = chart_function 

uploaded_file = "filtered_tweets_engie_cleaned.csv"
df = pd.read_csv('filtered_tweets_engie_cleaned.csv', sep=';')

def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()
    
    if data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return latitude, longitude
    else:
        return None, None


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

def histogramme_sentiment(df):
    df_count = df.groupby("Sentiment").size().reset_index(name='count')
    st.write('## Histogramme des Sentiments')
    st.bar_chart(df_count.set_index('Sentiment'))

def camembert_problématique(df):
    df_count = df['Problematique'].value_counts().reset_index()
    df_count.columns = ['Problematique', 'count']
    st.write('## Répartition des Problematique')
    fig = px.pie(df_count, names='Problematique', values='count', title='Répartition des Problematiques')
    st.plotly_chart(fig)

def histogramme_problematique(df):
    df_count = df.groupby("Problematique").size().reset_index(name='count')
    st.write('## Histogramme des Problematiques')
    st.bar_chart(df_count.set_index('Problematique'))

def histogramme_score(df):
    df_count = df.groupby("Score").size().reset_index(name='count')
    st.write('## Distribution des Scores')
    st.bar_chart(df_count.set_index('Score'))

def tableau_plaintes(df):
    df_complaints = df[df['Type'].str.contains('Plainte', na=False)]
    st.write('## Tableau des plaintes')
    st.dataframe(df_complaints)

def tableau_questions(df):
    df_questions = df[df['Type'].str.contains('Question', na=False)]
    st.write('## Tableau des questions')
    st.dataframe(df_questions)

def tableau_positifs(df):
    df_positifs = df[df['Sentiment'].str.contains('Positif', na=False)]
    st.write('## Tableau des tweets positifs')
    st.dataframe(df_positifs)

def histogramme_type(df):
    df_count = df.groupby("Type").size().reset_index(name='count')
    st.write('## Histogramme des Types')
    st.bar_chart(df_count.set_index('Type'))

def camembert_type(df):
    df_count = df['Type'].value_counts().reset_index()
    df_count.columns = ['Type', 'count']
    st.write('## Répartition des Types')
    fig = px.pie(df_count, names='Type', values='count', title='Répartition des Types')
    st.plotly_chart(fig)

def map_lieu(df):
    st.write('## Carte des lieux')
    locations_with_value = df['Lieu'].dropna().unique().tolist()
    coordinates = []
    for location in locations_with_value:
        lat, lon = get_coordinates(location)
        if lat is not None and lon is not None:
            coordinates.append({'Lieu': location, 'latitude': lat, 'longitude': lon})

    coordinates_df = pd.DataFrame(coordinates)
    coordinates_df['latitude'] = coordinates_df['latitude'].astype(float)
    coordinates_df['longitude'] = coordinates_df['longitude'].astype(float)
    st.map(coordinates_df)




st.title('Dashboard Projet 48h')
charts = [
    MyChart("Nombre de tweet par heure", ["Temps", "Heure","Histogramme"], nb_tweets_par_heure),
    MyChart("Nombre de tweet par heure", ["Temps","Mois","Histogramme"], nb_tweets_par_mois),
    MyChart("Camembert Sentiment", ["Camembert", "Sentiment"], camembert_sentiment),
    MyChart("Histogramme Sentiment", ["Histogramme", "Sentiment"], histogramme_sentiment),
    MyChart("Camembert Problématique", ["Camembert", "Problematique"], camembert_problématique),
    MyChart("Histogramme Problématique", ["Histogramme", "Problematique"], histogramme_problematique),
    MyChart("Histogramme Score", ["Score", "Histogramme"], histogramme_score),
    MyChart("Tableau Plaintes", ["Tableau", "Plainte"], tableau_plaintes),
    MyChart("Tableau Questions", ["Tableau", "Question"], tableau_questions),
    MyChart("Tableau Positifs", ["Tableau", "Positif"], tableau_positifs),
    MyChart("Histogramme Type", ["Histogramme", "Type"], histogramme_type),
    MyChart("Camembert Type", ["Camembert", "Type"], camembert_type),
    MyChart("Map Lieu", ["Map", "Lieu"], map_lieu)
]

with st.sidebar:
    all_tags = sorted(set(tag for chart in charts for tag in chart.tags))
    selected_tags = st.multiselect("Filtrer par tags :", options=all_tags)

for chart in charts:
    if not selected_tags or any(tag in chart.tags for tag in selected_tags):
        fig = chart.chart_function(df)
