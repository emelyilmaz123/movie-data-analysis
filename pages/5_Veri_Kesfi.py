import streamlit as st
from utils import load_data
from lang import t, render_lang_selector, render_footer

st.set_page_config(page_title="Veri Keşfi", page_icon="🔍", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_lang_selector()

df = load_data()

st.markdown(f'<p class="section-title">{t("veri_title")}</p>', unsafe_allow_html=True)
st.write(t('veri_desc'))

col1, col2, col3 = st.columns(3)
with col1:
    genres = sorted(df['main_genre'].dropna().unique())
    selected_genres = st.multiselect(t('veri_genre'), genres, default=[])
with col2:
    min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
    year_range = st.slider(t('veri_year'), min_year, max_year, (min_year, max_year))
with col3:
    min_score, max_score = float(df['imdb_score'].min()), float(df['imdb_score'].max())
    score_range = st.slider(t('veri_score'), min_score, max_score, (min_score, max_score))

search = st.text_input(t('veri_search'), placeholder="...")

filtered = df[
    (df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1]) &
    (df['imdb_score'] >= score_range[0]) & (df['imdb_score'] <= score_range[1])
]
if selected_genres:
    filtered = filtered[filtered['main_genre'].isin(selected_genres)]
if search:
    filtered = filtered[filtered['movie_title'].str.contains(search, case=False, na=False)]

st.write(f"**{len(filtered):,}** {t('veri_found')}")

display_cols = ['movie_title', 'title_year', 'main_genre', 'director_name', 'imdb_score', 'budget', 'gross', 'profit', 'duration']
result = filtered[display_cols].sort_values('imdb_score', ascending=False)
result.columns = t('veri_cols')
st.dataframe(result, use_container_width=True, hide_index=True)

csv = result.to_csv(index=False).encode('utf-8')
st.download_button(t('veri_download'), data=csv, file_name="films.csv", mime="text/csv")

render_footer(df)
