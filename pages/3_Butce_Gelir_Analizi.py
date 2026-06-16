import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data
from lang import t, render_lang_selector, render_footer

st.set_page_config(page_title="Bütçe & Gelir Analizi", page_icon="💰", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_lang_selector()

df = load_data()

st.markdown(f'<p class="section-title">{t("butce_title")}</p>', unsafe_allow_html=True)

arama = st.text_input("", placeholder=t('search_placeholder'), label_visibility="collapsed", key="butce_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning(t('no_film_found'))
    else:
        secim = st.selectbox(t('results_label'), eslesme['movie_title'].tolist(), key="butce_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(t('film'), secili_film['movie_title'])
        c2.metric(t('budget'), f"${secili_film['budget']:,.0f}" if secili_film['budget'] == secili_film['budget'] else "—")
        c3.metric(t('gross'), f"${secili_film['gross']:,.0f}" if secili_film['gross'] == secili_film['gross'] else "—")
        c4.metric(t('profit'), f"${secili_film['profit']:,.0f}" if secili_film['profit'] == secili_film['profit'] else "—")

st.write(t('butce_desc'))

min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
year_range = st.slider(t('yil_slider'), min_year, max_year, (1990, max_year), key="butce_yil")
filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

fig = px.scatter(filtered, x='budget', y='gross', hover_name='movie_title', color='main_genre',
                 title=t('butce_chart'), log_x=True, log_y=True, opacity=0.5,
                 labels={'budget': f"{t('budget')} ($)", 'gross': f"{t('gross')} ($)", 'main_genre': t('genre')})
if secili_film is not None and secili_film['budget'] == secili_film['budget']:
    fig.add_trace(go.Scatter(
        x=[secili_film['budget']], y=[secili_film['gross']],
        mode='markers+text',
        marker=dict(color='#f97316', size=18, symbol='star', line=dict(color='white', width=1)),
        text=[f"  {secili_film['movie_title'][:20]}"],
        textposition='middle right', textfont=dict(color='#f97316', size=13),
        showlegend=False,
    ))
st.plotly_chart(fig, use_container_width=True)

st.markdown(f'<p class="section-title">{t("butce_top")}</p>', unsafe_allow_html=True)
top_profit = filtered.sort_values('profit', ascending=False).head(10)[
    ['movie_title', 'title_year', 'budget', 'gross', 'profit']].copy()
top_profit.columns = [t('film'), t('year'), f"{t('budget')} ($)", f"{t('gross')} ($)", f"{t('profit')} ($)"]
st.dataframe(top_profit, use_container_width=True, hide_index=True)

st.markdown(f'<div class="info-card"><h4>{t("finding")}</h4><p>{t("butce_finding")}</p></div>', unsafe_allow_html=True)

render_footer(df)
