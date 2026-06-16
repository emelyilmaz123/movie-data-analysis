import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Tür Analizi", page_icon="🎭", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">🎭 Tür Analizi</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# FİLM ARAMA
# ---------------------------------------------------------------
arama = st.text_input("", placeholder="Film adı ile filtrele...", label_visibility="collapsed", key="tur_arama")

secili_film = None
vurgulu_tur = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning("Film bulunamadı.")
    else:
        secim = st.selectbox("Sonuçlar:", eslesme['movie_title'].tolist(), key="tur_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        vurgulu_tur = secili_film['main_genre']
        c1, c2, c3 = st.columns(3)
        c1.metric("Film", secili_film['movie_title'])
        c2.metric("Tür", vurgulu_tur)
        c3.metric("IMDB", f"{secili_film['imdb_score']:.1f}")

st.write("Film türlerinin dağılımı ve türlere göre ortalama IMDB skoru.")

# ---------------------------------------------------------------
# TÜR SEÇİMİ
# ---------------------------------------------------------------
genre_counts = df['main_genre'].value_counts()
all_genres = genre_counts.index.tolist()

default_genres = [vurgulu_tur] if vurgulu_tur else genre_counts.head(8).index.tolist()
selected_genres = st.multiselect("Türleri seçin", options=all_genres, default=default_genres)

filtered = df[df['main_genre'].isin(selected_genres)]

# ---------------------------------------------------------------
# GRAFİKLER
# ---------------------------------------------------------------
counts = filtered['main_genre'].value_counts().reset_index()
counts.columns = ['Tür', 'Film Sayısı']
counts['Renk'] = counts['Tür'].apply(lambda x: '#f97316' if x == vurgulu_tur else '#14b8a6')

fig1 = px.bar(
    counts.sort_values('Film Sayısı', ascending=True),
    x='Film Sayısı', y='Tür', orientation='h',
    title="Seçilen Türlere Göre Film Sayısı",
    color='Renk',
    color_discrete_map='identity',
)
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

genre_avg = filtered.groupby('main_genre')['imdb_score'].mean().sort_values(ascending=False).reset_index()
genre_avg.columns = ['Tür', 'Ortalama IMDB Skoru']
genre_avg['Renk'] = genre_avg['Tür'].apply(lambda x: '#f97316' if x == vurgulu_tur else '#0f766e')

fig2 = px.bar(
    genre_avg, x='Tür', y='Ortalama IMDB Skoru',
    title="Türlere Göre Ortalama IMDB Skoru",
    color='Renk',
    color_discrete_map='identity',
)
fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Biyografi, Suç ve Dram türleri ortalamada en yüksek IMDB skorlarına
            sahiptir. Korku ve Komedi gibi yüksek hacimli türler ise ortalama
            skor bakımından daha düşük seviyelerde kalmaktadır.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
