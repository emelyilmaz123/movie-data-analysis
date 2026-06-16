import streamlit as st
import plotly.express as px
from utils import load_data
from lang import t

st.set_page_config(page_title="Yıl Analizi", page_icon="📅", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'tr'

col_lang = st.columns([8, 1])[1]
with col_lang:
    if st.session_state['lang'] == 'tr':
        if st.button("🇬🇧 English", key="lang_yil"):
            st.session_state['lang'] = 'en'
            st.rerun()
    else:
        if st.button("🇹🇷 Türkçe", key="lang_yil"):
            st.session_state['lang'] = 'tr'
            st.rerun()

df = load_data()

st.markdown(f'<p class="section-title">{t("yil_title")}</p>', unsafe_allow_html=True)

arama = st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed", key="yil_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning(t('no_film_found'))
    else:
        secim = st.selectbox(t('results_label'), eslesme['movie_title'].tolist(), key="yil_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric(t('film'), secili_film['movie_title'])
        c2.metric(t('year'), int(secili_film['title_year']))
        c3.metric(t('imdb'), f"{secili_film['imdb_score']:.1f}")

st.write(t('yil_desc'))

min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
default_start = int(secili_film['title_year']) if secili_film is not None else 1990
year_range = st.slider(t('yil_slider'), min_year, max_year, (min(default_start, 1990), max_year))

filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

col1, col2 = st.columns(2)
col1.metric(t('yil_count'), f"{len(filtered):,}")
col2.metric(t('yil_avg'), f"{filtered['imdb_score'].mean():.2f}")

movie_counts = filtered.groupby('title_year').size().reset_index(name='n')
fig1 = px.bar(movie_counts, x='title_year', y='n', title=t('yil_chart1'), color_discrete_sequence=['#14b8a6'])
fig1.update_layout(xaxis_title=t('year'), yaxis_title='')
if secili_film is not None:
    film_yil = int(secili_film['title_year'])
    fig1.add_vline(x=film_yil, line_dash="dash", line_color="#f97316", line_width=2)
    fig1.add_annotation(x=film_yil, y=movie_counts['n'].max(),
                        text=f"◀ {secili_film['movie_title'][:20]}",
                        showarrow=False, font=dict(color="#f97316", size=12), xanchor="left")
st.plotly_chart(fig1, use_container_width=True)

yearly_avg = filtered.groupby('title_year')['imdb_score'].mean().reset_index()
fig2 = px.line(yearly_avg, x='title_year', y='imdb_score', title=t('yil_chart2'),
               markers=True, color_discrete_sequence=['#0f766e'])
fig2.update_layout(xaxis_title=t('year'), yaxis_title=t('imdb'))
if secili_film is not None:
    import plotly.graph_objects as go
    fig2.add_vline(x=film_yil, line_dash="dash", line_color="#f97316", line_width=2)
    fig2.add_trace(go.Scatter(x=[film_yil], y=[secili_film['imdb_score']],
                              mode='markers+text',
                              marker=dict(color='#f97316', size=14, symbol='star'),
                              text=[f"  {secili_film['movie_title'][:15]}"],
                              textposition='middle right', showlegend=False))
st.plotly_chart(fig2, use_container_width=True)

st.markdown(f'<div class="info-card"><h4>{t("finding")}</h4><p>{t("yil_finding")}</p></div>', unsafe_allow_html=True)
