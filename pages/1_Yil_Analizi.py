import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

st.set_page_config(page_title="Yıl Analizi", page_icon="📅", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">📅 Yıl Analizi</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# FİLM ARAMA
# ---------------------------------------------------------------
arama = st.text_input("", placeholder="Film adı ile filtrele...", label_visibility="collapsed", key="yil_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning("Film bulunamadı.")
    else:
        secim = st.selectbox("Sonuçlar:", eslesme['movie_title'].tolist(), key="yil_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Film", secili_film['movie_title'])
        c2.metric("Yıl", int(secili_film['title_year']))
        c3.metric("IMDB", f"{secili_film['imdb_score']:.1f}")

st.write("Filmlerin yıllara göre dağılımı ve ortalama IMDB skoru trendi.")

# ---------------------------------------------------------------
# YIL ARALIĞI
# ---------------------------------------------------------------
min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
default_start = int(secili_film['title_year']) if secili_film is not None else 1990
year_range = st.slider("Yıl Aralığı", min_year, max_year, (min(default_start, 1990), max_year))

filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

col1, col2 = st.columns(2)
col1.metric("Seçilen Aralıktaki Film Sayısı", f"{len(filtered):,}")
col2.metric("Seçilen Aralıkta Ortalama Skor", f"{filtered['imdb_score'].mean():.2f}")

# ---------------------------------------------------------------
# GRAFİK 1 — Yıllara Göre Film Sayısı
# ---------------------------------------------------------------
movie_counts = filtered.groupby('title_year').size().reset_index(name='Film Sayısı')
fig1 = px.bar(
    movie_counts, x='title_year', y='Film Sayısı',
    title="Yıllara Göre Film Sayısı",
    color_discrete_sequence=['#14b8a6'],
)
fig1.update_layout(xaxis_title="Yıl", yaxis_title="Film Sayısı")

if secili_film is not None:
    film_yil = int(secili_film['title_year'])
    fig1.add_vline(x=film_yil, line_dash="dash", line_color="#f97316", line_width=2)
    fig1.add_annotation(x=film_yil, y=movie_counts['Film Sayısı'].max(),
                        text=f"◀ {secili_film['movie_title'][:20]}",
                        showarrow=False, font=dict(color="#f97316", size=12), xanchor="left")

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------------
# GRAFİK 2 — Yıllara Göre Ortalama IMDB Skoru
# ---------------------------------------------------------------
yearly_avg = filtered.groupby('title_year')['imdb_score'].mean().reset_index()
fig2 = px.line(
    yearly_avg, x='title_year', y='imdb_score',
    title="Yıllara Göre Ortalama IMDB Skoru",
    markers=True,
    color_discrete_sequence=['#0f766e'],
)
fig2.update_layout(xaxis_title="Yıl", yaxis_title="Ortalama IMDB Skoru")

if secili_film is not None:
    fig2.add_vline(x=film_yil, line_dash="dash", line_color="#f97316", line_width=2)
    fig2.add_scatter(x=[film_yil], y=[secili_film['imdb_score']],
                     mode='markers+text',
                     marker=dict(color='#f97316', size=14, symbol='star'),
                     text=[f"  {secili_film['movie_title'][:15]}"],
                     textposition='middle right',
                     name=secili_film['movie_title'],
                     showlegend=False)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            2000'li yıllardan sonra üretilen film sayısı önemli ölçüde artmıştır,
            ancak ortalama IMDB skorlarında zamana göre belirgin bir düşüş eğilimi
            görülmektedir.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
