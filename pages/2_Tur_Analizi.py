import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Tür Analizi", page_icon="🎭", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">🎭 Tür Analizi</p>', unsafe_allow_html=True)
st.write("Film türlerinin dağılımı ve türlere göre ortalama IMDB skoru.")

genre_counts = df['main_genre'].value_counts()
all_genres = genre_counts.index.tolist()

selected_genres = st.multiselect(
    "Türleri seçin",
    options=all_genres,
    default=genre_counts.head(8).index.tolist(),
)

filtered = df[df['main_genre'].isin(selected_genres)]

col1, col2 = st.columns(2)

# Tür dağılımı
counts = filtered['main_genre'].value_counts().reset_index()
counts.columns = ['Tür', 'Film Sayısı']
fig1 = px.bar(
    counts.sort_values('Film Sayısı', ascending=True),
    x='Film Sayısı', y='Tür', orientation='h',
    title="Seçilen Türlere Göre Film Sayısı",
    color_discrete_sequence=['#14b8a6'],
)
col1.plotly_chart(fig1, use_container_width=True)

# Tür bazlı ortalama skor
genre_avg = filtered.groupby('main_genre')['imdb_score'].mean().sort_values(ascending=False).reset_index()
genre_avg.columns = ['Tür', 'Ortalama IMDB Skoru']
fig2 = px.bar(
    genre_avg, x='Tür', y='Ortalama IMDB Skoru',
    title="Türlere Göre Ortalama IMDB Skoru",
    color_discrete_sequence=['#0f766e'],
)
col2.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Biography, Crime ve Drama türleri ortalamada en yüksek IMDB skorlarına
            sahiptir. Horror ve Comedy gibi yüksek hacimli türler ise ortalama
            skor bakımından daha düşük seviyelerde kalmaktadır.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
