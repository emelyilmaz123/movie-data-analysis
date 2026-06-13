import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Yıl Analizi", page_icon="📅", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">📅 Yıl Analizi</p>', unsafe_allow_html=True)
st.write("Filmlerin yıllara göre dağılımı ve ortalama IMDB skoru trendi.")

min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
year_range = st.slider("Yıl Aralığı", min_year, max_year, (1990, max_year))

filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

col1, col2 = st.columns(2)
col1.metric("Seçilen Aralıktaki Film Sayısı", f"{len(filtered):,}")
col2.metric("Seçilen Aralıkta Ortalama Skor", f"{filtered['imdb_score'].mean():.2f}")

# Yıllara göre film sayısı
movie_counts = filtered.groupby('title_year').size().reset_index(name='Film Sayısı')
fig1 = px.bar(
    movie_counts, x='title_year', y='Film Sayısı',
    title="Yıllara Göre Film Sayısı",
    color_discrete_sequence=['#14b8a6'],
)
fig1.update_layout(xaxis_title="Yıl", yaxis_title="Film Sayısı")
st.plotly_chart(fig1, use_container_width=True)

# Yıllara göre ortalama IMDB skoru
yearly_avg = filtered.groupby('title_year')['imdb_score'].mean().reset_index()
fig2 = px.line(
    yearly_avg, x='title_year', y='imdb_score',
    title="Yıllara Göre Ortalama IMDB Skoru",
    markers=True,
    color_discrete_sequence=['#0f766e'],
)
fig2.update_layout(xaxis_title="Yıl", yaxis_title="Ortalama IMDB Skoru")
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            2000'li yıllardan sonra üretilen film sayısı önemli ölçüde artmıştır,
            ancak ortalama IMDB skorlarında zamana göre belirgin bir düşüş eğilimi
            görülmektedir — bu durum film sayısındaki artışın kalite ortalamasını
            biraz aşağı çekmiş olabileceğine işaret etmektedir.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
