import streamlit as st
import plotly.express as px
from utils import load_data
from lang import t, render_lang_selector

st.set_page_config(page_title="Yönetmen & Oyuncu Analizi", page_icon="🎬", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_lang_selector()

df = load_data()

st.markdown(f'<p class="section-title">{t("yon_title")}</p>', unsafe_allow_html=True)

arama = st.text_input("", placeholder=t('yon_placeholder'), label_visibility="collapsed", key="yon_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning(t('no_film_found'))
    else:
        secim = st.selectbox(t('results_label'), eslesme['movie_title'].tolist(), key="yon_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]

if secili_film is not None:
    yonetmen = secili_film['director_name']
    oyuncu = secili_film['actor_1_name']
    st.markdown("---")

    if yonetmen == yonetmen:
        st.markdown(f'<p class="section-title">🎬 {t("director")}: {yonetmen}</p>', unsafe_allow_html=True)
        yf = df[df['director_name'] == yonetmen].sort_values('imdb_score', ascending=False)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(t('yon_total'), len(yf))
        c2.metric(t('yon_avg'), f"{yf['imdb_score'].mean():.2f}")
        c3.metric(t('yon_best'), f"{yf['imdb_score'].max():.1f}")
        c4.metric(t('yon_avg_gross'), f"${yf['gross'].mean():,.0f}" if yf['gross'].notna().any() else "—")
        fig_dir = px.bar(yf.sort_values('imdb_score'), x='imdb_score', y='movie_title', orientation='h',
                         color='imdb_score', color_continuous_scale='teal',
                         title=f"{yonetmen} — {t('imdb')}",
                         labels={'imdb_score': t('imdb'), 'movie_title': t('film')})
        fig_dir.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_dir, use_container_width=True)
        tablo = yf[['movie_title', 'title_year', 'main_genre', 'imdb_score', 'gross', 'profit']].copy()
        tablo.columns = [t('film'), t('year'), t('genre'), t('imdb'), f"{t('gross')} ($)", f"{t('profit')} ($)"]
        tablo[t('year')] = tablo[t('year')].astype(int)
        st.dataframe(tablo, use_container_width=True, hide_index=True)

    st.markdown("---")

    if oyuncu == oyuncu:
        st.markdown(f'<p class="section-title">🎭 {t("actor")}: {oyuncu}</p>', unsafe_allow_html=True)
        af = df[(df['actor_1_name'] == oyuncu) | (df['actor_2_name'] == oyuncu) | (df['actor_3_name'] == oyuncu)].sort_values('imdb_score', ascending=False)
        c1, c2, c3 = st.columns(3)
        c1.metric(t('yon_total'), len(af))
        c2.metric(t('yon_avg'), f"{af['imdb_score'].mean():.2f}")
        c3.metric(t('yon_best'), f"{af['imdb_score'].max():.1f}")
        fig_act = px.bar(af.head(15).sort_values('imdb_score'), x='imdb_score', y='movie_title', orientation='h',
                         color='imdb_score', color_continuous_scale='teal',
                         title=f"{oyuncu} — {t('imdb')}",
                         labels={'imdb_score': t('imdb'), 'movie_title': t('film')})
        fig_act.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_act, use_container_width=True)

    st.markdown("---")

st.write(t('yon_desc'))
min_films = st.slider(t('yon_min_films'), 2, 20, 5)

director_counts = df['director_name'].value_counts()
frequent_directors = director_counts[director_counts >= min_films].index
director_avg = (df[df['director_name'].isin(frequent_directors)]
                .groupby('director_name')['imdb_score'].mean()
                .sort_values(ascending=False).head(10).reset_index())
director_avg.columns = [t('director'), t('imdb')]
vurgulu_yonetmen = secili_film['director_name'] if secili_film is not None else None
director_avg['Renk'] = director_avg[t('director')].apply(lambda x: '#f97316' if x == vurgulu_yonetmen else '#0f766e')

actor_counts = df['actor_1_name'].value_counts()
frequent_actors = actor_counts[actor_counts >= min_films].index
actor_avg = (df[df['actor_1_name'].isin(frequent_actors)]
             .groupby('actor_1_name')['imdb_score'].mean()
             .sort_values(ascending=False).head(10).reset_index())
actor_avg.columns = [t('actor'), t('imdb')]
vurgulu_oyuncu = secili_film['actor_1_name'] if secili_film is not None else None
actor_avg['Renk'] = actor_avg[t('actor')].apply(lambda x: '#f97316' if x == vurgulu_oyuncu else '#14b8a6')

col1, col2 = st.columns(2)
fig1 = px.bar(director_avg.sort_values(t('imdb')), x=t('imdb'), y=t('director'), orientation='h',
              title=f"{t('yon_dir_chart')} (min. {min_films})", color='Renk', color_discrete_map='identity')
fig1.update_layout(showlegend=False)
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(actor_avg.sort_values(t('imdb')), x=t('imdb'), y=t('actor'), orientation='h',
              title=f"{t('yon_act_chart')} (min. {min_films})", color='Renk', color_discrete_map='identity')
fig2.update_layout(showlegend=False)
col2.plotly_chart(fig2, use_container_width=True)

st.markdown(f'<div class="info-card"><h4>{t("finding")}</h4><p>{t("yon_finding")}</p></div>', unsafe_allow_html=True)
