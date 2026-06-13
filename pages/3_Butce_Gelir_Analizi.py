import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Bütçe & Gelir Analizi", page_icon="💰", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">💰 Bütçe & Gelir Analizi</p>', unsafe_allow_html=True)
st.write("Filmlerin bütçesi ile gişe geliri arasındaki ilişki ve en kârlı filmler.")

min_year, max_year = int(df['title_year'].min()), int(df['title_year'].max())
year_range = st.slider("Yıl Aralığı", min_year, max_year, (1990, max_year), key="butce_yil")

filtered = df[(df['title_year'] >= year_range[0]) & (df['title_year'] <= year_range[1])]

# Bütçe vs gişe geliri scatter
fig = px.scatter(
    filtered, x='budget', y='gross',
    hover_name='movie_title',
    color='main_genre',
    title="Bütçe vs Gişe Geliri",
    log_x=True, log_y=True,
    labels={'budget': 'Bütçe ($)', 'gross': 'Gişe Geliri ($)', 'main_genre': 'Tür'},
)
st.plotly_chart(fig, use_container_width=True)

# En kârlı filmler
st.markdown('<p class="section-title">🏆 En Kârlı 10 Film</p>', unsafe_allow_html=True)
top_profit = filtered.sort_values('profit', ascending=False).head(10)[
    ['movie_title', 'title_year', 'budget', 'gross', 'profit']
]
top_profit.columns = ['Film', 'Yıl', 'Bütçe ($)', 'Gişe Geliri ($)', 'Kâr ($)']
st.dataframe(top_profit, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div class="info-card">
        <h4>📌 Bulgu</h4>
        <p>
            Bütçe ile gişe geliri arasında pozitif bir ilişki gözlemlenmektedir,
            ancak bu ilişki doğrusal değildir — yüksek bütçeli birçok film
            beklenen geliri sağlayamamıştır. En kârlı filmler genellikle
            Action/Adventure/Fantasy türlerinde yoğunlaşmaktadır.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
