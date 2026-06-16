import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

st.set_page_config(page_title="Popülerlik & Sosyal Medya Analizi", page_icon="📈", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">📈 Popülerlik & Sosyal Medya Analizi</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# FİLM ARAMA
# ---------------------------------------------------------------
arama = st.text_input("", placeholder="Film adı ile filtrele...", label_visibility="collapsed", key="pop_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning("Film bulunamadı.")
    else:
        secim = st.selectbox("Sonuçlar:", eslesme['movie_title'].tolist(), key="pop_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Film", secili_film['movie_title'])
        c2.metric("Oy Sayısı", f"{int(secili_film['num_voted_users']):,}" if secili_film['num_voted_users'] == secili_film['num_voted_users'] else "—")
        c3.metric("Facebook Beğenisi", f"{int(secili_film['movie_facebook_likes']):,}" if secili_film['movie_facebook_likes'] == secili_film['movie_facebook_likes'] else "—")

st.write("Oy sayısı, eleştiri sayısı, Facebook beğenileri, ülke ve içerik derecesi bazlı analizler.")

# ---------------------------------------------------------------
# OY SAYISI vs IMDB SKORU
# ---------------------------------------------------------------
col1, col2 = st.columns(2)

fig1 = px.scatter(
    df, x='num_voted_users', y='imdb_score',
    hover_name='movie_title',
    title="Oy Sayısı vs IMDB Skoru",
    log_x=True,
    color_discrete_sequence=['#0f766e'],
    labels={'num_voted_users': 'Oy Sayısı', 'imdb_score': 'IMDB Skoru'},
    opacity=0.5,
)
if secili_film is not None and secili_film['num_voted_users'] == secili_film['num_voted_users']:
    fig1.add_trace(go.Scatter(
        x=[secili_film['num_voted_users']], y=[secili_film['imdb_score']],
        mode='markers+text',
        marker=dict(color='#f97316', size=16, symbol='star'),
        text=[f"  {secili_film['movie_title'][:15]}"],
        textposition='middle right',
        textfont=dict(color='#f97316', size=12),
        showlegend=False,
    ))
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(
    df, x='movie_facebook_likes', y='gross',
    hover_name='movie_title',
    title="Facebook Beğenisi vs Gişe Geliri",
    log_x=True, log_y=True,
    color_discrete_sequence=['#14b8a6'],
    labels={'movie_facebook_likes': 'Facebook Beğenisi', 'gross': 'Gişe Geliri ($)'},
    opacity=0.5,
)
if secili_film is not None and secili_film['movie_facebook_likes'] == secili_film['movie_facebook_likes']:
    fig2.add_trace(go.Scatter(
        x=[secili_film['movie_facebook_likes']], y=[secili_film['gross']],
        mode='markers+text',
        marker=dict(color='#f97316', size=16, symbol='star'),
        text=[f"  {secili_film['movie_title'][:15]}"],
        textposition='middle right',
        textfont=dict(color='#f97316', size=12),
        showlegend=False,
    ))
col2.plotly_chart(fig2, use_container_width=True)

corr_votes_score = df['num_voted_users'].corr(df['imdb_score'])
corr_fb_gross = df['movie_facebook_likes'].corr(df['gross'])
col1.caption(f"Korelasyon (oy sayısı - IMDB skoru): **{corr_votes_score:.2f}**")
col2.caption(f"Korelasyon (Facebook beğenisi - gişe geliri): **{corr_fb_gross:.2f}**")

# ---------------------------------------------------------------
# EN ÇOK OY ALAN FİLMLER
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🗳️ En Çok Oy Alan 10 Film</p>', unsafe_allow_html=True)
top_voted = df.sort_values('num_voted_users', ascending=False).head(10)[
    ['movie_title', 'title_year', 'num_voted_users', 'num_critic_for_reviews', 'imdb_score']
]
top_voted.columns = ['Film', 'Yıl', 'Oy Sayısı', 'Eleştiri Sayısı', 'IMDB Skoru']
st.dataframe(top_voted, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------
# ÜLKE ANALİZİ
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🌍 Ülke Analizi</p>', unsafe_allow_html=True)

country_counts = df['country'].value_counts().head(10)
top_countries = country_counts.index

col3, col4 = st.columns(2)

country_counts_df = country_counts.reset_index()
country_counts_df.columns = ['Ülke', 'Film Sayısı']

fig3 = px.bar(
    country_counts_df, x='Film Sayısı', y='Ülke', orientation='h',
    title="En Çok Film Üreten 10 Ülke",
    color_discrete_sequence=['#0f766e'],
)
col3.plotly_chart(fig3, use_container_width=True)

country_avg = (
    df[df['country'].isin(top_countries)]
    .groupby('country')['imdb_score']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
country_avg.columns = ['Ülke', 'Ortalama IMDB Skoru']
fig4 = px.bar(
    country_avg, x='Ülke', y='Ortalama IMDB Skoru',
    title="En Çok Film Üreten Ülkelerde Ortalama IMDB Skoru",
    color_discrete_sequence=['#14b8a6'],
)
col4.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------------
# İÇERİK DERECESİ ANALİZİ
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🎟️ İçerik Derecesi Analizi</p>', unsafe_allow_html=True)

rating_df = df.dropna(subset=['content_rating'])
rating_counts = rating_df['content_rating'].value_counts()
common_ratings = rating_counts[rating_counts >= 20].index

col5, col6 = st.columns(2)

fig5 = px.bar(
    rating_counts.head(8).reset_index(),
    x='content_rating', y='count',
    title="İçerik Derecesine Göre Film Sayısı",
    color_discrete_sequence=['#0f766e'],
    labels={'content_rating': 'İçerik Derecesi', 'count': 'Film Sayısı'},
)
col5.plotly_chart(fig5, use_container_width=True)

rating_avg = (
    rating_df[rating_df['content_rating'].isin(common_ratings)]
    .groupby('content_rating')['imdb_score']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
rating_avg.columns = ['İçerik Derecesi', 'Ortalama IMDB Skoru']
fig6 = px.bar(
    rating_avg, x='İçerik Derecesi', y='Ortalama IMDB Skoru',
    title="İçerik Derecesine Göre Ortalama IMDB Skoru",
    color_discrete_sequence=['#14b8a6'],
)
col6.plotly_chart(fig6, use_container_width=True)

top_country = country_counts.index[0]
top_country_share = country_counts.iloc[0] / len(df) * 100
best_avg_country = country_avg.iloc[0]['Ülke']
best_avg_country_score = country_avg.iloc[0]['Ortalama IMDB Skoru']
top_rating = rating_counts.index[0]

st.markdown(
    f"""
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Oy sayısı ile IMDB skoru arasındaki korelasyon <b>{corr_votes_score:.2f}</b>,
            Facebook beğenisi ile gişe geliri arasındaki korelasyon ise
            <b>{corr_fb_gross:.2f}</b> olarak hesaplanmıştır.
            Veri setindeki filmlerin <b>%{top_country_share:.1f}</b>'i <b>{top_country}</b>
            yapımıdır. En çok film üreten 10 ülke arasında en yüksek ortalama IMDB
            skoruna sahip ülke <b>{best_avg_country}</b> (ortalama {best_avg_country_score:.2f}).
            En yaygın içerik derecesi <b>{top_rating}</b>'dir.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
