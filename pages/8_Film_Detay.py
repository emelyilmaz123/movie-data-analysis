import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data
from lang import t

st.set_page_config(page_title="Film Detay", page_icon="🎞️", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'tr'

col_lang = st.columns([8, 1])[1]
with col_lang:
    if st.session_state['lang'] == 'tr':
        if st.button("🇬🇧 English", key="lang_detay"):
            st.session_state['lang'] = 'en'
            st.rerun()
    else:
        if st.button("🇹🇷 Türkçe", key="lang_detay"):
            st.session_state['lang'] = 'tr'
            st.rerun()

df = load_data()

st.markdown(f'<p class="section-title">{t("detay_title")}</p>', unsafe_allow_html=True)
st.write(t('detay_desc'))

query = st.text_input("", placeholder=t('detay_placeholder'), label_visibility="collapsed")

if not query.strip():
    st.info(t('detay_no_film'))
    st.stop()

matches = df[df['movie_title'].str.contains(query, case=False, na=False)].sort_values('imdb_score', ascending=False)

if matches.empty:
    st.warning(t('no_film_found'))
    st.stop()

secim = st.selectbox(t('results_label'), matches['movie_title'].tolist())
film = matches[matches['movie_title'] == secim].iloc[0]

st.markdown("---")

st.markdown(
    f"""
    <div class="hero" style="padding: 2rem; text-align:left;">
        <div class="hero-logo" style="font-size:2rem;">🎬 {film['movie_title']}</div>
        <p class="hero-sub" style="text-align:left; margin-top:0.3rem;">
            {int(film['title_year'])} &nbsp;·&nbsp; {film['main_genre']} &nbsp;·&nbsp;
            {int(film['duration']) if film['duration'] == film['duration'] else '?'} {'dk' if st.session_state.get('lang','tr') == 'tr' else 'min'} &nbsp;·&nbsp;
            {film['content_rating'] if film['content_rating'] == film['content_rating'] else t('detay_unrated')}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<p class="section-title">{t("detay_scores")}</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric(t('imdb'), f"{film['imdb_score']:.1f} / 10")
c2.metric(t('detay_votes'), f"{int(film['num_voted_users']):,}" if film['num_voted_users'] == film['num_voted_users'] else "—")
c3.metric(t('detay_critics'), f"{int(film['num_critic_for_reviews']):,}" if film['num_critic_for_reviews'] == film['num_critic_for_reviews'] else "—")
c4.metric(t('detay_users'), f"{int(film['num_user_for_reviews']):,}" if film['num_user_for_reviews'] == film['num_user_for_reviews'] else "—")

st.markdown(f'<p class="section-title">{t("detay_crew")}</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"**{t('director')}**\n\n{film['director_name'] if film['director_name'] == film['director_name'] else '—'}")
c2.markdown(f"**{t('actor')}**\n\n{film['actor_1_name'] if film['actor_1_name'] == film['actor_1_name'] else '—'}")
c3.markdown(f"**{t('detay_2nd')}**\n\n{film['actor_2_name'] if film['actor_2_name'] == film['actor_2_name'] else '—'}")
c4.markdown(f"**{t('detay_3rd')}**\n\n{film['actor_3_name'] if film['actor_3_name'] == film['actor_3_name'] else '—'}")

st.markdown(f'<p class="section-title">{t("detay_budget")}</p>', unsafe_allow_html=True)
butce = film['budget']
gise = film['gross']
kar = film['profit']
c1, c2, c3 = st.columns(3)
c1.metric(t('budget'), f"${butce:,.0f}" if butce == butce else "—")
c2.metric(t('gross'), f"${gise:,.0f}" if gise == gise else "—")
if kar == kar:
    c3.metric(t('detay_profit'), f"${kar:,.0f}", delta=f"${abs(kar):,.0f}")
else:
    c3.metric(t('detay_profit'), "—")

if butce == butce and gise == gise:
    bar_df = pd.DataFrame({t('budget'): [t('budget'), t('gross')], '$': [butce, gise]})
    fig_bar = px.bar(bar_df, x=t('budget'), y='$', color=t('budget'),
                     color_discrete_map={t('budget'): '#0f766e', t('gross'): '#14b8a6'},
                     title=t('detay_bar_title'))
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown(f'<p class="section-title">{t("detay_social")}</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric(t('detay_film_page'), f"{int(film['movie_facebook_likes']):,}" if film['movie_facebook_likes'] == film['movie_facebook_likes'] else "—")
c2.metric(film['actor_1_name'] if film['actor_1_name'] == film['actor_1_name'] else t('actor'), f"{int(film['actor_1_facebook_likes']):,}" if film['actor_1_facebook_likes'] == film['actor_1_facebook_likes'] else "—")
c3.metric(film['actor_2_name'] if film['actor_2_name'] == film['actor_2_name'] else t('detay_2nd'), f"{int(film['actor_2_facebook_likes']):,}" if film['actor_2_facebook_likes'] == film['actor_2_facebook_likes'] else "—")
c4.metric(film['director_name'] if film['director_name'] == film['director_name'] else t('director'), f"{int(film['director_facebook_likes']):,}" if film['director_facebook_likes'] == film['director_facebook_likes'] else "—")

st.markdown("---")

yonetmen = film['director_name']
if yonetmen == yonetmen:
    st.markdown(f'<p class="section-title">🎬 {yonetmen}</p>', unsafe_allow_html=True)
    yf = df[(df['director_name'] == yonetmen) & (df['movie_title'] != film['movie_title'])].sort_values('imdb_score', ascending=False)
    if yf.empty:
        st.info(t('detay_no_director'))
    else:
        fig_dir = px.bar(yf.sort_values('imdb_score'), x='imdb_score', y='movie_title', orientation='h',
                         color='imdb_score', color_continuous_scale='teal',
                         labels={'imdb_score': t('imdb'), 'movie_title': t('film')})
        fig_dir.update_layout(coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig_dir, use_container_width=True)

st.markdown(f'<p class="section-title">{t("detay_similar")}</p>', unsafe_allow_html=True)
st.caption(f"{t('detay_similar_caption')} {film['imdb_score']:.1f} ± 1.0")
benzer = df[(df['main_genre'] == film['main_genre']) & (df['movie_title'] != film['movie_title']) &
            (df['imdb_score'] >= film['imdb_score'] - 1.0) & (df['imdb_score'] <= film['imdb_score'] + 1.0)].sort_values('imdb_score', ascending=False).head(6)
if benzer.empty:
    st.info(t('detay_no_similar'))
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(benzer.iterrows()):
        with cols[i % 3]:
            st.markdown(f'<div class="info-card"><h4>{row["movie_title"]}</h4><p>🎬 {row["director_name"]}<br>📅 {int(row["title_year"])} &nbsp;·&nbsp; ⭐ {row["imdb_score"]:.1f}</p></div>', unsafe_allow_html=True)
