import pandas as pd
import streamlit as st

TUR_CEVIRISI = {
    'Action':      'Aksiyon',
    'Adventure':   'Macera',
    'Animation':   'Animasyon',
    'Biography':   'Biyografi',
    'Comedy':      'Komedi',
    'Crime':       'Suç',
    'Documentary': 'Belgesel',
    'Drama':       'Dram',
    'Family':      'Aile',
    'Fantasy':     'Fantezi',
    'Film-Noir':   'Film-Noir',
    'Game-Show':   'Oyun Şovu',
    'History':     'Tarih',
    'Horror':      'Korku',
    'Music':       'Müzik',
    'Musical':     'Müzikal',
    'Mystery':     'Gizem',
    'Romance':     'Romantik',
    'Sci-Fi':      'Bilim Kurgu',
    'Thriller':    'Gerilim',
    'Western':     'Western',
}


@st.cache_data
def load_data():
    df = pd.read_csv('movie_metadata.csv')

    df = df.drop_duplicates()
    df['movie_title'] = df['movie_title'].str.strip()
    df = df.dropna(subset=['title_year', 'imdb_score', 'budget', 'gross'])

    df['title_year'] = df['title_year'].astype(int)
    df['main_genre'] = df['genres'].str.split('|').str[0].map(TUR_CEVIRISI).fillna(df['genres'].str.split('|').str[0])
    df['profit'] = df['gross'] - df['budget']

    return df
