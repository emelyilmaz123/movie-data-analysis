import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Yönetmen & Oyuncu Analizi", page_icon="🎬", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">🎬 Yönetmen & Oyuncu Analizi</p>', unsafe_allow_html=True)
st.write("En yüksek ortalama IMDB skoruna sahip yönetmen ve oyuncular.")

min_films = st.slider("Minimum film sayısı", 2, 20, 5)

# Yönetmen analizi
director_counts = df['director_name'].value_counts()
frequent_directors = director_counts[director_counts >= min_films].index
director_avg = (
    df[df['director_name'].isin(frequent_directors)]
    .groupby('director_name')['imdb_score']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
director_avg.columns = ['Yönetmen', 'Ortalama IMDB Skoru']

# Oyuncu analizi (actor_1_name)
actor_counts = df['actor_1_name'].value_counts()
frequent_actors = actor_counts[actor_counts >= min_films].index
actor_avg = (
    df[df['actor_1_name'].isin(frequent_actors)]
    .groupby('actor_1_name')['imdb_score']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
actor_avg.columns = ['Oyuncu', 'Ortalama IMDB Skoru']

col1, col2 = st.columns(2)

fig1 = px.bar(
    director_avg.sort_values('Ortalama IMDB Skoru'),
    x='Ortalama IMDB Skoru', y='Yönetmen', orientation='h',
    title=f"En Yüksek Ortalama Skora Sahip Yönetmenler (en az {min_films} film)",
    color_discrete_sequence=['#0f766e'],
)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    actor_avg.sort_values('Ortalama IMDB Skoru'),
    x='Ortalama IMDB Skoru', y='Oyuncu', orientation='h',
    title=f"En Yüksek Ortalama Skora Sahip Oyuncular (en az {min_films} film)",
    color_discrete_sequence=['#14b8a6'],
)
col2.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Christopher Nolan, Quentin Tarantino ve James Cameron gibi yönetmenler
            en az 5 film çekmiş yönetmenler arasında en yüksek ortalama IMDB
            skoruna sahiptir. Minimum film sayısı eşiği düşürüldüğünde listeye
            daha az tanınan ama yüksek puanlı yönetmenler de girebilmektedir.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
