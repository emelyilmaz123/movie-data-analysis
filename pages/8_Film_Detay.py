import streamlit as st
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="Film Detay", page_icon="🎞️", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

st.markdown('<p class="section-title">🎞️ Film Detay</p>', unsafe_allow_html=True)
st.write("Film adını yaz, listeden seç — tüm verileri ve analizini gör.")

# ---------------------------------------------------------------
# ARAMA
# ---------------------------------------------------------------
query = st.text_input("", placeholder="Film adı yaz...", label_visibility="collapsed")

if not query.strip():
    st.info("Aramak istediğin filmin adını yaz.")
    st.stop()

matches = df[df['movie_title'].str.contains(query, case=False, na=False)].sort_values('imdb_score', ascending=False)

if matches.empty:
    st.warning("Film bulunamadı. Farklı bir isim dene.")
    st.stop()

secenekler = matches['movie_title'].tolist()
secim = st.selectbox("Sonuçlar:", secenekler)

film = matches[matches['movie_title'] == secim].iloc[0]

st.markdown("---")

# ---------------------------------------------------------------
# BAŞLIK
# ---------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero" style="padding: 2rem; text-align:left;">
        <div class="hero-logo" style="font-size:2rem;">🎬 {film['movie_title']}</div>
        <p class="hero-sub" style="text-align:left; margin-top:0.3rem;">
            {int(film['title_year'])} &nbsp;·&nbsp; {film['main_genre']} &nbsp;·&nbsp;
            {int(film['duration']) if film['duration'] == film['duration'] else '?'} dk &nbsp;·&nbsp;
            {film['content_rating'] if film['content_rating'] == film['content_rating'] else 'Belirtilmemiş'} &nbsp;·&nbsp;
            {film['language'] if film['language'] == film['language'] else ''} &nbsp;·&nbsp;
            {film['country'] if film['country'] == film['country'] else ''}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# SKORLAR & POPÜLERLİK
# ---------------------------------------------------------------
st.markdown('<p class="section-title">⭐ Skorlar & Popülerlik</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("IMDB Skoru", f"{film['imdb_score']:.1f} / 10")
c2.metric("Oy Sayısı", f"{int(film['num_voted_users']):,}" if film['num_voted_users'] == film['num_voted_users'] else "—")
c3.metric("Eleştiri Sayısı", f"{int(film['num_critic_for_reviews']):,}" if film['num_critic_for_reviews'] == film['num_critic_for_reviews'] else "—")
c4.metric("Kullanıcı Yorumu", f"{int(film['num_user_for_reviews']):,}" if film['num_user_for_reviews'] == film['num_user_for_reviews'] else "—")

# ---------------------------------------------------------------
# EKİP
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🎭 Ekip</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"**Yönetmen**\n\n{film['director_name'] if film['director_name'] == film['director_name'] else '—'}")
c2.markdown(f"**Başrol**\n\n{film['actor_1_name'] if film['actor_1_name'] == film['actor_1_name'] else '—'}")
c3.markdown(f"**2. Oyuncu**\n\n{film['actor_2_name'] if film['actor_2_name'] == film['actor_2_name'] else '—'}")
c4.markdown(f"**3. Oyuncu**\n\n{film['actor_3_name'] if film['actor_3_name'] == film['actor_3_name'] else '—'}")

# ---------------------------------------------------------------
# BÜTÇE & GİŞE
# ---------------------------------------------------------------
st.markdown('<p class="section-title">💰 Bütçe & Gişe</p>', unsafe_allow_html=True)

butce = film['budget']
gise = film['gross']
kar = film['profit']

c1, c2, c3 = st.columns(3)
c1.metric("Bütçe", f"${butce:,.0f}" if butce == butce else "—")
c2.metric("Gişe Geliri", f"${gise:,.0f}" if gise == gise else "—")

if kar == kar:
    delta_label = f"{'Kâr' if kar > 0 else 'Zarar'}: ${abs(kar):,.0f}"
    c3.metric("Kâr / Zarar", f"${kar:,.0f}", delta=delta_label)
else:
    c3.metric("Kâr / Zarar", "—")

# Bütçe vs Gişe bar grafiği
if butce == butce and gise == gise:
    import pandas as pd
    bar_df = pd.DataFrame({
        'Kategori': ['Bütçe', 'Gişe Geliri'],
        'Tutar ($)': [butce, gise],
        'Renk': ['#0f766e', '#14b8a6']
    })
    fig_bar = px.bar(
        bar_df, x='Kategori', y='Tutar ($)',
        color='Kategori',
        color_discrete_map={'Bütçe': '#0f766e', 'Gişe Geliri': '#14b8a6'},
        title="Bütçe & Gişe Karşılaştırması",
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------------
# SOSYAL MEDYA
# ---------------------------------------------------------------
st.markdown('<p class="section-title">📱 Sosyal Medya Beğenileri</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Film Sayfası", f"{int(film['movie_facebook_likes']):,}" if film['movie_facebook_likes'] == film['movie_facebook_likes'] else "—")
c2.metric(film['actor_1_name'] if film['actor_1_name'] == film['actor_1_name'] else "Başrol", f"{int(film['actor_1_facebook_likes']):,}" if film['actor_1_facebook_likes'] == film['actor_1_facebook_likes'] else "—")
c3.metric(film['actor_2_name'] if film['actor_2_name'] == film['actor_2_name'] else "2. Oyuncu", f"{int(film['actor_2_facebook_likes']):,}" if film['actor_2_facebook_likes'] == film['actor_2_facebook_likes'] else "—")
c4.metric(film['director_name'] if film['director_name'] == film['director_name'] else "Yönetmen", f"{int(film['director_facebook_likes']):,}" if film['director_facebook_likes'] == film['director_facebook_likes'] else "—")

st.markdown("---")

# ---------------------------------------------------------------
# YÖNETMENİN DİĞER FİLMLERİ
# ---------------------------------------------------------------
yonetmen = film['director_name']
if yonetmen == yonetmen:
    st.markdown(f'<p class="section-title">🎬 {yonetmen} Filmleri</p>', unsafe_allow_html=True)
    yonetmen_filmleri = df[
        (df['director_name'] == yonetmen) &
        (df['movie_title'] != film['movie_title'])
    ].sort_values('imdb_score', ascending=False)[['movie_title', 'title_year', 'main_genre', 'imdb_score']]

    if yonetmen_filmleri.empty:
        st.info("Veri setinde bu yönetmenin başka filmi bulunmuyor.")
    else:
        yonetmen_filmleri.columns = ['Film', 'Yıl', 'Tür', 'IMDB']
        yonetmen_filmleri['Yıl'] = yonetmen_filmleri['Yıl'].astype(int)

        fig_dir = px.bar(
            yonetmen_filmleri.sort_values('IMDB'),
            x='IMDB', y='Film', orientation='h',
            color='IMDB',
            color_continuous_scale='teal',
            title=f"{yonetmen} — IMDB Skorları",
            labels={'IMDB': 'IMDB Skoru'},
        )
        fig_dir.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_dir, use_container_width=True)

# ---------------------------------------------------------------
# BENZERİ FİLMLER
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🍿 Benzer Filmler</p>', unsafe_allow_html=True)
st.caption(f"Aynı tür · IMDB skoru {film['imdb_score']:.1f} ± 1.0")

benzer = df[
    (df['main_genre'] == film['main_genre']) &
    (df['movie_title'] != film['movie_title']) &
    (df['imdb_score'] >= film['imdb_score'] - 1.0) &
    (df['imdb_score'] <= film['imdb_score'] + 1.0)
].sort_values('imdb_score', ascending=False).head(6)

if benzer.empty:
    st.info("Benzer film bulunamadı.")
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(benzer.iterrows()):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="info-card">
                    <h4>{row['movie_title']}</h4>
                    <p>🎬 {row['director_name']}<br>
                    📅 {int(row['title_year'])} &nbsp;·&nbsp; ⭐ {row['imdb_score']:.1f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
