import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data
from lang import t

st.set_page_config(page_title="Popülerlik & Sosyal Medya", page_icon="📈", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'tr'

col_lang = st.columns([8, 1])[1]
with col_lang:
    if st.session_state['lang'] == 'tr':
        if st.button("🇬🇧 English", key="lang_pop"):
            st.session_state['lang'] = 'en'
            st.rerun()
    else:
        if st.button("🇹🇷 Türkçe", key="lang_pop"):
            st.session_state['lang'] = 'tr'
            st.rerun()

df = load_data()

st.markdown(f'<p class="section-title">{t("pop_title")}</p>', unsafe_allow_html=True)

arama = st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed", key="pop_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning(t('no_film_found'))
    else:
        secim = st.selectbox(t('results_label'), eslesme['movie_title'].tolist(), key="pop_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric(t('film'), secili_film['movie_title'])
        c2.metric(t('pop_votes'), f"{int(secili_film['num_voted_users']):,}" if secili_film['num_voted_users'] == secili_film['num_voted_users'] else "—")
        c3.metric(t('pop_fb'), f"{int(secili_film['movie_facebook_likes']):,}" if secili_film['movie_facebook_likes'] == secili_film['movie_facebook_likes'] else "—")

st.write(t('pop_desc'))

col1, col2 = st.columns(2)

fig1 = px.scatter(df, x='num_voted_users', y='imdb_score', hover_name='movie_title',
                  title=t('pop_chart1'), log_x=True, color_discrete_sequence=['#0f766e'],
                  labels={'num_voted_users': t('pop_votes'), 'imdb_score': t('imdb')}, opacity=0.5)
if secili_film is not None and secili_film['num_voted_users'] == secili_film['num_voted_users']:
    fig1.add_trace(go.Scatter(x=[secili_film['num_voted_users']], y=[secili_film['imdb_score']],
                              mode='markers+text', marker=dict(color='#f97316', size=16, symbol='star'),
                              text=[f"  {secili_film['movie_title'][:15]}"],
                              textposition='middle right', textfont=dict(color='#f97316', size=12), showlegend=False))
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(df, x='movie_facebook_likes', y='gross', hover_name='movie_title',
                  title=t('pop_chart2'), log_x=True, log_y=True, color_discrete_sequence=['#14b8a6'],
                  labels={'movie_facebook_likes': t('pop_fb'), 'gross': f"{t('gross')} ($)"}, opacity=0.5)
if secili_film is not None and secili_film['movie_facebook_likes'] == secili_film['movie_facebook_likes']:
    fig2.add_trace(go.Scatter(x=[secili_film['movie_facebook_likes']], y=[secili_film['gross']],
                              mode='markers+text', marker=dict(color='#f97316', size=16, symbol='star'),
                              text=[f"  {secili_film['movie_title'][:15]}"],
                              textposition='middle right', textfont=dict(color='#f97316', size=12), showlegend=False))
col2.plotly_chart(fig2, use_container_width=True)

corr_votes_score = df['num_voted_users'].corr(df['imdb_score'])
corr_fb_gross = df['movie_facebook_likes'].corr(df['gross'])
col1.caption(f"Korelasyon ({t('pop_votes')} - {t('imdb')}): **{corr_votes_score:.2f}**")
col2.caption(f"Korelasyon ({t('pop_fb')} - {t('gross')}): **{corr_fb_gross:.2f}**")

st.markdown(f'<p class="section-title">{t("pop_top_voted")}</p>', unsafe_allow_html=True)
top_voted = df.sort_values('num_voted_users', ascending=False).head(10)[
    ['movie_title', 'title_year', 'num_voted_users', 'num_critic_for_reviews', 'imdb_score']]
top_voted.columns = t('pop_cols')
st.dataframe(top_voted, use_container_width=True, hide_index=True)

st.markdown(f'<p class="section-title">{t("pop_country")}</p>', unsafe_allow_html=True)
country_counts = df['country'].value_counts().head(10)
top_countries = country_counts.index
col3, col4 = st.columns(2)
cc_df = country_counts.reset_index()
cc_df.columns = ['Ülke', 'n']
fig3 = px.bar(cc_df, x='n', y='Ülke', orientation='h', color_discrete_sequence=['#0f766e'],
              title=t('pop_country'))
col3.plotly_chart(fig3, use_container_width=True)
country_avg = (df[df['country'].isin(top_countries)].groupby('country')['imdb_score']
               .mean().sort_values(ascending=False).reset_index())
country_avg.columns = ['Ülke', t('imdb')]
fig4 = px.bar(country_avg, x='Ülke', y=t('imdb'), color_discrete_sequence=['#14b8a6'])
col4.plotly_chart(fig4, use_container_width=True)

st.markdown(f'<p class="section-title">{t("pop_rating")}</p>', unsafe_allow_html=True)
rating_df = df.dropna(subset=['content_rating'])
rating_counts = rating_df['content_rating'].value_counts()
common_ratings = rating_counts[rating_counts >= 20].index
col5, col6 = st.columns(2)
fig5 = px.bar(rating_counts.head(8).reset_index(), x='content_rating', y='count',
              color_discrete_sequence=['#0f766e'],
              labels={'content_rating': t('pop_rating'), 'count': 'n'})
col5.plotly_chart(fig5, use_container_width=True)
rating_avg = (rating_df[rating_df['content_rating'].isin(common_ratings)]
              .groupby('content_rating')['imdb_score'].mean().sort_values(ascending=False).reset_index())
rating_avg.columns = [t('pop_rating'), t('imdb')]
fig6 = px.bar(rating_avg, x=t('pop_rating'), y=t('imdb'), color_discrete_sequence=['#14b8a6'])
col6.plotly_chart(fig6, use_container_width=True)
