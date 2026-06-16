import streamlit as st
import pandas as pd
from utils import load_data
from lang import t, STRINGS, render_lang_selector

st.set_page_config(page_title="FilmRadar", page_icon="📡", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_lang_selector()

df = load_data()

# ---------------------------------------------------------------
# HERO
# ---------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-logo">📡 FilmRadar</div>
        <p class="hero-sub">{t('hero_sub')}</p>
        <p class="hero-desc">{t('hero_desc')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# ARAMA
# ---------------------------------------------------------------
st.markdown(f'<p class="section-title">{t("search_title")}</p>', unsafe_allow_html=True)

query = st.text_input("", placeholder=t('search_main_placeholder'), label_visibility="collapsed")

TR_TO_EN = {
    "aksiyon": "action", "korku": "horror", "komedi": "comedy",
    "dram": "drama", "gerilim": "thriller", "macera": "adventure",
    "bilim": "science", "kurgu": "fiction", "animasyon": "animation",
    "romantik": "romance", "aşk": "love", "savaş": "war",
    "polisiye": "crime", "suç": "crime", "gizem": "mystery",
    "psikolojik": "psychological", "psikoloji": "psychological",
    "hapishane": "prison", "dedektif": "detective", "uzay": "space",
    "robot": "robot", "zombi": "zombie", "vampir": "vampire",
    "tarih": "history", "biyografi": "biography", "müzik": "music",
    "spor": "sport", "kahraman": "hero", "karanlık": "dark",
    "distopya": "dystopia", "hayatta kalma": "survival",
}

def search_films(df, query):
    if not query.strip():
        return pd.DataFrame()
    translated = query.lower()
    for tr, en in TR_TO_EN.items():
        translated = translated.replace(tr, en)
    keywords = translated.split()
    search_cols = ['movie_title', 'director_name', 'actor_1_name',
                   'actor_2_name', 'actor_3_name', 'genres', 'plot_keywords']
    def match_score(row):
        combined = " ".join(str(row[c]).lower() for c in search_cols if pd.notna(row[c]))
        return sum(1 for kw in keywords if kw in combined)
    df = df.copy()
    df['_score'] = df.apply(match_score, axis=1)
    results = df[df['_score'] > 0].sort_values(['_score', 'imdb_score'], ascending=[False, False])
    return results.drop(columns=['_score'])

if query:
    results = search_films(df, query)
    if results.empty:
        st.warning(t('no_match'))
    else:
        st.success(f"**{len(results)} {t('found')}** — {t('showing_top')}")
        display = results[['movie_title', 'director_name', 'actor_1_name',
                            'genres', 'title_year', 'imdb_score']].head(20).copy()
        display.columns = [t('film'), t('director'), t('lead_actor'), t('genres'), t('year'), t('imdb')]
        display[t('year')] = display[t('year')].astype(int)
        display[t('imdb')] = display[t('imdb')].round(1)
        display = display.reset_index(drop=True)
        display.index += 1
        st.dataframe(display, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------
# NE İZLEMELİYİM
# ---------------------------------------------------------------
st.markdown(f'<p class="section-title">{t("watch_title")}</p>', unsafe_allow_html=True)
st.write(t('watch_desc'))

col1, col2, col3 = st.columns(3)
genres = sorted(df['main_genre'].dropna().unique().tolist())
selected_genre = col1.selectbox(t('genre_select'), genres)
year_range = col2.slider(t('year_range'), int(df['title_year'].min()), int(df['title_year'].max()), (2000, int(df['title_year'].max())))
min_score = col3.slider(t('min_score'), 1.0, 9.0, 6.5, step=0.1)

filtered = df[
    (df['main_genre'] == selected_genre) &
    (df['title_year'] >= year_range[0]) &
    (df['title_year'] <= year_range[1]) &
    (df['imdb_score'] >= min_score)
].sort_values('imdb_score', ascending=False).head(10)

if filtered.empty:
    st.warning(t('no_match_filter'))
else:
    for i, row in enumerate(filtered.itertuples(), 1):
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        c1.markdown(f"**{i}. {row.movie_title}**")
        c2.markdown(f"🎬 {row.director_name}")
        c3.markdown(f"📅 {int(row.title_year)}")
        c4.markdown(f"⭐ {row.imdb_score:.1f}")

st.markdown("---")

# ---------------------------------------------------------------
# İSTATİSTİKLER
# ---------------------------------------------------------------
st.markdown(f'<p class="section-title">{t("db_title")}</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total_films'), f"{len(df):,}")
col2.metric(t('avg_imdb'), f"{df['imdb_score'].mean():.2f}")
col3.metric(t('directors'), f"{df['director_name'].nunique():,}")
col4.metric(t('year_range_label'), f"{df['title_year'].min()} – {df['title_year'].max()}")

st.markdown(f'<p class="section-title">{t("analysis_title")}</p>', unsafe_allow_html=True)

pages = t('pages')
cols = st.columns(len(pages))
for col, (path, title, desc) in zip(cols, pages):
    with col:
        if st.button(f"{title}\n\n{desc}", key=path, use_container_width=True):
            st.switch_page(path)

st.markdown(
    f"""
    <div class="footer-rich">
        <div class="footer-logo">📡 FilmRadar</div>
        <p class="footer-desc">{t('footer_desc')}</p>

        <div class="footer-stats">
            <div class="footer-stat">
                <div class="footer-stat-value">{len(df):,}</div>
                <div class="footer-stat-label">{t('footer_stat_films')}</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">{df['director_name'].nunique():,}</div>
                <div class="footer-stat-label">{t('footer_stat_directors')}</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">{df['main_genre'].nunique()}</div>
                <div class="footer-stat-label">{t('footer_stat_genres')}</div>
            </div>
            <div class="footer-stat">
                <div class="footer-stat-value">{int(df['title_year'].min())}–{int(df['title_year'].max())}</div>
                <div class="footer-stat-label">{t('footer_stat_years')}</div>
            </div>
        </div>

        <div class="footer-links">
            <span>👩‍💻 {t('footer_dev')}: Emel Yılmaz</span>
            <a href="https://github.com/emelyilmaz123/movie-data-analysis" target="_blank">⭐ GitHub</a>
            <a href="https://streamlit.io" target="_blank">🚀 Streamlit</a>
            <span>📊 IMDB 5000 Dataset</span>
        </div>

        <div class="footer-copy">{t('footer_copy')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
