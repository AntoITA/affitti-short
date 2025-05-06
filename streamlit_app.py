import pandas as pd
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Caricamento del dataset
@st.cache
def load_data():
    df = pd.read_csv('airbnb_seattle.csv')
    df = df[['id', 'name', 'description', 'price', 'picture_url']]
    df['description'] = df['description'].fillna('')
    return df

df = load_data()

# Funzione per ottenere le raccomandazioni
def get_recommendations(listing_id):
    idx = df[df['id'] == listing_id].index[0]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-6:-1][::-1]
    return df.iloc[similar_indices]

# Interfaccia utente
st.title('App di Raccomandazione Airbnb')
listing_id = st.number_input('Inserisci l\'ID dell\'annuncio:', min_value=1)
if listing_id:
    st.subheader('Annuncio Selezionato')
    selected_listing = df[df['id'] == listing_id].iloc[0]
    st.image(selected_listing['picture_url'])
    st.write(f"**Nome:** {selected_listing['name']}")
    st.write(f"**Prezzo:** {selected_listing['price']}")
    st.write(f"**Descrizione:** {selected_listing['description']}")

    st.subheader('Annunci Simili')
    recommendations = get_recommendations(listing_id)
    for _, row in recommendations.iterrows():
        st.image(row['picture_url'])
        st.write(f"**Nome:** {row['name']}")
        st.write(f"**Prezzo:** {row['price']}")
        st.write(f"**Descrizione:** {row['description']}")
