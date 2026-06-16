import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

st.set_page_config(page_title="Bütçe & Gelir Analizi", page_icon="💰", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">💰 Bütçe & Gelir Analizi</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# FİLM ARAMA
# ---------------------------------------------------------------
arama = st.text_input("", placeholder="Film adı ile filtrele...", label_visibility="collapsed", key="butce_arama")

secili_film = None
if arama.strip():
    eslesme = df[df['movie_title'].str.contains(arama, case=False, na=False)].sort_values('imdb_score', ascending=False)
    if eslesme.empty:
        st.warning("Film bulunamadı.")
    else:
        secim = st.selectbox("Sonuçlar:", eslesme['movie_title'].tolist(), key="butce_secim")
        secili_film = eslesme[eslesme['movie_title'] == secim].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Film", secili_film['movie_title'])
        c2.metric("Bütçe", f"${secili_film['budget']:,.0f}" if secili_film['budget'] == secili_film['budget'] else "—")
        c3.metric("Gişe", f"${secili_film['gross']:,.0f}" if secili_film['gross'] == secili_film['gross'] else "—")
        c4.metric("Kâr", f"${secili_film['profit']:,.0f}" if secili_film['profit'] == secili_film['profit'] else "—")

st.write("Filmlerin bütçesi ile gişe geliri arasındaki ilişki ve en kârlı filmler.")

# ---------------------------------------------------------------
# YIL ARALIĞI
# ---------------------------------------------------------------
min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
year_range = st.slider("Yıl Aralığı", min_year, max_year, (1990, max_year), key="butce_yil")
filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

# ---------------------------------------------------------------
# SCATTER — Bütçe vs Gişe
# ---------------------------------------------------------------
fig = px.scatter(
    filtered, x='budget', y='gross',
    hover_name='movie_title',
    color='main_genre',
    title="Bütçe vs Gişe Geliri",
    log_x=True, log_y=True,
    labels={'budget': 'Bütçe ($)', 'gross': 'Gişe Geliri ($)', 'main_genre': 'Tür'},
    opacity=0.5,
)

if secili_film is not None and secili_film['budget'] == secili_film['budget']:
    fig.add_trace(go.Scatter(
        x=[secili_film['budget']],
        y=[secili_film['gross']],
        mode='markers+text',
        marker=dict(color='#f97316', size=18, symbol='star', line=dict(color='white', width=1)),
        text=[f"  {secili_film['movie_title'][:20]}"],
        textposition='middle right',
        textfont=dict(color='#f97316', size=13),
        name=secili_film['movie_title'],
        showlegend=False,
    ))

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# EN KÂRLI FİLMLER
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🏆 En Kârlı 10 Film</p>', unsafe_allow_html=True)
top_profit = filtered.sort_values('profit', ascending=False).head(10)[
    ['movie_title', 'title_year', 'budget', 'gross', 'profit']
].copy()
top_profit.columns = ['Film', 'Yıl', 'Bütçe ($)', 'Gişe Geliri ($)', 'Kâr ($)']
st.dataframe(top_profit, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Bütçe ile gişe geliri arasında pozitif bir ilişki gözlemlenmektedir,
            ancak yüksek bütçeli birçok film beklenen geliri sağlayamamıştır.
            En kârlı filmler genellikle Aksiyon/Macera/Fantezi türlerinde yoğunlaşmaktadır.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
