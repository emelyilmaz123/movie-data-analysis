import streamlit as st
import plotly.express as px
from utils import load_data
from lang import t, render_lang_selector, render_footer

st.set_page_config(page_title="Tür Analizi", page_icon="🎭", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_lang_selector()

df = load_data()

st.markdown(f'<p class="section-title">{t("tur_title")}</p>', unsafe_allow_html=True)

arama = st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed", key="tur_arama")

secili_film = None
vurgulu_tur = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning(t('no_film_found'))
    else:
        secim = st.selectbox(t('results_label'), eslesme['movie_title'].tolist(), key="tur_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        vurgulu_tur = secili_film['main_genre']
        c1, c2, c3 = st.columns(3)
        c1.metric(t('film'), secili_film['movie_title'])
        c2.metric(t('genre'), vurgulu_tur)
        c3.metric(t('imdb'), f"{secili_film['imdb_score']:.1f}")

st.write(t('tur_desc'))

genre_counts = df['main_genre'].value_counts()
all_genres = genre_counts.index.tolist()
default_genres = [vurgulu_tur] if vurgulu_tur else genre_counts.head(8).index.tolist()
selected_genres = st.multiselect(t('tur_select'), options=all_genres, default=default_genres)

filtered = df[df['main_genre'].isin(selected_genres)]

counts = filtered['main_genre'].value_counts().reset_index()
counts.columns = [t('genre'), 'n']
counts['Renk'] = counts[t('genre')].apply(lambda x: '#f97316' if x == vurgulu_tur else '#14b8a6')
fig1 = px.bar(counts.sort_values('n', ascending=True), x='n', y=t('genre'), orientation='h',
              title=t('tur_chart1'), color='Renk', color_discrete_map='identity')
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

genre_avg = filtered.groupby('main_genre')['imdb_score'].mean().sort_values(ascending=False).reset_index()
genre_avg.columns = [t('genre'), t('imdb')]
genre_avg['Renk'] = genre_avg[t('genre')].apply(lambda x: '#f97316' if x == vurgulu_tur else '#0f766e')
fig2 = px.bar(genre_avg, x=t('genre'), y=t('imdb'), title=t('tur_chart2'),
              color='Renk', color_discrete_map='identity')
fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(f'<div class="info-card"><h4>{t("finding")}</h4><p>{t("tur_finding")}</p></div>', unsafe_allow_html=True)

render_footer(df)
