import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv('movie_metadata.csv')

    df = df.drop_duplicates()
    df['movie_title'] = df['movie_title'].str.strip()
    df = df.dropna(subset=['title_year', 'imdb_score', 'budget', 'gross'])

    df['title_year'] = df['title_year'].astype(int)
    df['main_genre'] = df['genres'].str.split('|').str[0]
    df['profit'] = df['gross'] - df['budget']

    return df
