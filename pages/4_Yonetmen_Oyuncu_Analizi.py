import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Yönetmen & Oyuncu Analizi", page_icon="🎬", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">🎬 Yönetmen & Oyuncu Analizi</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# FİLM ARAMA
# ---------------------------------------------------------------
arama = st.text_input("", placeholder="Film adı yaz, yönetmen ve oyuncu analizini gör...", label_visibility="collapsed", key="yon_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning("Film bulunamadı.")
    else:
        secim = st.selectbox("Sonuçlar:", eslesme['movie_title'].tolist(), key="yon_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]

# ---------------------------------------------------------------
# FİLM SEÇİLDİYSE — YÖNETMEN & OYUNCU ODAKLI ANALİZ
# ---------------------------------------------------------------
if secili_film is not None:
    yonetmen = secili_film['director_name']
    oyuncu = secili_film['actor_1_name']

    st.markdown("---")

    # YÖNETMEN BÖLÜMÜ
    if yonetmen == yonetmen:
        st.markdown(f'<p class="section-title">🎬 Yönetmen: {yonetmen}</p>', unsafe_allow_html=True)

        yonetmen_filmleri = df[df['director_name'] == yonetmen].sort_values('imdb_score', ascending=False)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Toplam Film", len(yonetmen_filmleri))
        c2.metric("Ort. IMDB Skoru", f"{yonetmen_filmleri['imdb_score'].mean():.2f}")
        c3.metric("En Yüksek Skor", f"{yonetmen_filmleri['imdb_score'].max():.1f}")
        c4.metric("Ort. Gişe Geliri", f"${yonetmen_filmleri['gross'].mean():,.0f}" if yonetmen_filmleri['gross'].notna().any() else "—")

        fig_dir = px.bar(
            yonetmen_filmleri.sort_values('imdb_score'),
            x='imdb_score', y='movie_title', orientation='h',
            color='imdb_score',
            color_continuous_scale='teal',
            title=f"{yonetmen} — Tüm Filmler (IMDB Skoru)",
            labels={'imdb_score': 'IMDB Skoru', 'movie_title': 'Film'},
        )
        fig_dir.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_dir, use_container_width=True)

        tablo = yonetmen_filmleri[['movie_title', 'title_year', 'main_genre', 'imdb_score', 'gross', 'profit']].copy()
        tablo.columns = ['Film', 'Yıl', 'Tür', 'IMDB', 'Gişe ($)', 'Kâr ($)']
        tablo['Yıl'] = tablo['Yıl'].astype(int)
        st.dataframe(tablo, use_container_width=True, hide_index=True)

    st.markdown("---")

    # OYUNCU BÖLÜMÜ
    if oyuncu == oyuncu:
        st.markdown(f'<p class="section-title">🎭 Başrol Oyuncu: {oyuncu}</p>', unsafe_allow_html=True)

        oyuncu_filmleri = df[
            (df['actor_1_name'] == oyuncu) |
            (df['actor_2_name'] == oyuncu) |
            (df['actor_3_name'] == oyuncu)
        ].sort_values('imdb_score', ascending=False)

        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Film", len(oyuncu_filmleri))
        c2.metric("Ort. IMDB Skoru", f"{oyuncu_filmleri['imdb_score'].mean():.2f}")
        c3.metric("En Yüksek Skor", f"{oyuncu_filmleri['imdb_score'].max():.1f}")

        fig_act = px.bar(
            oyuncu_filmleri.head(15).sort_values('imdb_score'),
            x='imdb_score', y='movie_title', orientation='h',
            color='imdb_score',
            color_continuous_scale='teal',
            title=f"{oyuncu} — Filmler (IMDB Skoru)",
            labels={'imdb_score': 'IMDB Skoru', 'movie_title': 'Film'},
        )
        fig_act.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_act, use_container_width=True)

    st.markdown("---")

# ---------------------------------------------------------------
# GENEL ANALİZ — HER ZAMAN GÖSTER
# ---------------------------------------------------------------
st.write("En yüksek ortalama IMDB skoruna sahip yönetmen ve oyuncular.")
min_films = st.slider("Minimum film sayısı", 2, 20, 5)

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
vurgulu_yonetmen = secili_film['director_name'] if secili_film is not None else None
director_avg['Renk'] = director_avg['Yönetmen'].apply(
    lambda x: '#f97316' if x == vurgulu_yonetmen else '#0f766e'
)

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
vurgulu_oyuncu = secili_film['actor_1_name'] if secili_film is not None else None
actor_avg['Renk'] = actor_avg['Oyuncu'].apply(
    lambda x: '#f97316' if x == vurgulu_oyuncu else '#14b8a6'
)

col1, col2 = st.columns(2)

fig1 = px.bar(
    director_avg.sort_values('Ortalama IMDB Skoru'),
    x='Ortalama IMDB Skoru', y='Yönetmen', orientation='h',
    title=f"En Yüksek Ortalama Skora Sahip Yönetmenler (en az {min_films} film)",
    color='Renk', color_discrete_map='identity',
)
fig1.update_layout(showlegend=False)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    actor_avg.sort_values('Ortalama IMDB Skoru'),
    x='Ortalama IMDB Skoru', y='Oyuncu', orientation='h',
    title=f"En Yüksek Ortalama Skora Sahip Oyuncular (en az {min_films} film)",
    color='Renk', color_discrete_map='identity',
)
fig2.update_layout(showlegend=False)
col2.plotly_chart(fig2, use_container_width=True)
