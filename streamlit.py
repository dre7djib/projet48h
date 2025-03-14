import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string

#pip3 install streamlit
#pip3 install pandas
#pip3 install plotly
#pip3 install openpyxl 
#pip install wordcloud 

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

mots_a_exclure = {
    "à", "de", "pour","fois","quoi","encore","leur","trop", "https", "la", "le", "les", "je", "sur", "ne", "ce", "pas", "et", "vous", "en", "faire", "fait",
    "dans", "moi", "c'est", "plus", "sans", "un", "des", "au", "par", "c est", "t", "c  est", "co", "est", "alors", "que",
    "il", "nous", "ça", "n", "mon", "même", "suis", "ou", "m", "d", "ma", "mes", "êtes", "qu", "ils", "son", "vos", "du",
    "j'ai", "va", "ont", "car", "là", "nje", "l", "se", "n'est", "donc", "ni", "mais", "voir", "nvous", "une", "avez",
    "n'ai", "cette", "y", "dites", "plusieurs", "cher", "bonjour", "aucune", "aucun", "toute", "tout", "très", "tu",
    "peux", "entre", "sont", "j ai", "avoir", "quand", "c", "cela", "notre", "elle", "peut", "sous", "aux", "chez",
    "votre", "part", "avec", "j  ai", "d'un", "tous", "tout", "toutes", "sa", "bon", "vais", "merde", "depuis",
    "dernière", "avant", "soit", "mère", "parle", "non", "qu' il", "quel", "juste", "dit", "moins", "nj'ai", "j", "ai",
    "après", "qu'il", "où", "voulez", "comme", "engie", "engiepart", "engieconso", "engiepartsav", "engiepartfr",
    "engiegroup", "qui", "jour", "mois", "jamais", "rien", "été", "normal", "faut", "jours", "dire", "semaine", "deux",
    "si", "?", "!", "2", "3", ",", "@engiepartfr", "@engiegroup", "@engiepartsav", "c'est", "cest", "d", "l", "c'est", ":", "."
}

def nettoyer_texte(texte):
    texte = str(texte).lower()
    texte = re.sub(r"http\S+", "", texte)
    texte = re.sub(r"@\w+", "", texte)
    texte = re.sub(r"[’‘']", " ", texte)
    texte = texte.translate(str.maketrans("", "", string.punctuation))
    mots = texte.split()
    mots_filtres = [mot for mot in mots if mot not in mots_a_exclure and len(mot) > 1]
    return " ".join(mots_filtres)

def nuage_mots(df) : 
    df["clean_text"] = df["full_text"].apply(nettoyer_texte)

    st.write('## Nuage de mots des tweets')

    texte_global = " ".join(df["clean_text"])

    if st.button("Générer le nuage de mots"):
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(texte_global)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)


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
    MyChart("Nuage de mots", ["Nuage de point", "Mots"], nuage_mots),
    MyChart("Map Lieu", ["Map", "Lieu"], map_lieu)
]

with st.sidebar:
    all_tags = sorted(set(tag for chart in charts for tag in chart.tags))
    selected_tags = st.multiselect("Filtrer par tags :", options=all_tags)

for chart in charts:
    if not selected_tags or any(tag in chart.tags for tag in selected_tags):
        fig = chart.chart_function(df)
