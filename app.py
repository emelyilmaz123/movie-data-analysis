import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(
    page_title="FilmRadar",
    page_icon="📡",
    layout="wide",
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

# ---------------------------------------------------------------
# HERO
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-logo">📡 FilmRadar</div>
        <p class="hero-sub">Tarif et. Biz bulalım.</p>
        <p class="hero-desc">
            Adını hatırlamıyor musun? Türünü, oyuncusunu, yönetmenini ya da aklındaki herhangi bir şeyi yaz.
            FilmRadar binlerce film arasından en iyi eşleşmeleri sana getirir.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# SEARCH — AKLIMDA Kİ FİLM
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🔍 Aklındaki filmi bul</p>', unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="Örn: Nolan   psikolojik gerilim   hapishane   uzay   Tom Hanks",
    label_visibility="collapsed",
)

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
        st.warning("Eşleşen film bulunamadı. Farklı kelimeler dene.")
    else:
        st.success(f"**{len(results)} film bulundu** — en iyi sonuçlar gösteriliyor")
        display = results[['movie_title', 'director_name', 'actor_1_name',
                            'genres', 'title_year', 'imdb_score']].head(20).copy()
        display.columns = ['Film Adı', 'Yönetmen', 'Başrol', 'Türler', 'Yıl', 'IMDB']
        display['Yıl'] = display['Yıl'].astype(int)
        display['IMDB'] = display['IMDB'].round(1)
        display = display.reset_index(drop=True)
        display.index += 1
        st.dataframe(display, use_container_width=True)

st.markdown("---")

# ---------------------------------------------------------------
# WHAT TO WATCH — TÜR SEÇİMİ
# ---------------------------------------------------------------
st.markdown('<p class="section-title">🎬 Ne izlemeliyim?</p>', unsafe_allow_html=True)
st.write("Türünü seç, yıl ve skor filtrele — sana en iyileri getirelim.")

col1, col2, col3 = st.columns(3)
genres = sorted(df['main_genre'].dropna().unique().tolist())
selected_genre = col1.selectbox("Tür", genres)
year_range = col2.slider("Yıl aralığı", int(df['title_year'].min()), int(df['title_year'].max()), (2000, int(df['title_year'].max())))
min_score = col3.slider("Minimum IMDB skoru", 1.0, 9.0, 6.5, step=0.1)

filtered = df[
    (df['main_genre'] == selected_genre) &
    (df['title_year'] >= year_range[0]) &
    (df['title_year'] <= year_range[1]) &
    (df['imdb_score'] >= min_score)
].sort_values('imdb_score', ascending=False).head(10)

if filtered.empty:
    st.warning("Bu kriterlere uyan film bulunamadı. Filtreleri genişletmeyi dene.")
else:
    for i, row in enumerate(filtered.itertuples(), 1):
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        c1.markdown(f"**{i}. {row.movie_title}**")
        c2.markdown(f"🎬 {row.director_name}")
        c3.markdown(f"📅 {int(row.title_year)}")
        c4.markdown(f"⭐ {row.imdb_score:.1f}")

st.markdown("---")

# ---------------------------------------------------------------
# STATS + ANALİZ SAYFALAR
# ---------------------------------------------------------------
st.markdown('<p class="section-title">📊 Veri Tabanı</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Film", f"{len(df):,}")
col2.metric("Ortalama IMDB", f"{df['imdb_score'].mean():.2f}")
col3.metric("Yönetmen Sayısı", f"{df['director_name'].nunique():,}")
col4.metric("Yıl Aralığı", f"{df['title_year'].min()} – {df['title_year'].max()}")

st.markdown('<p class="section-title">📈 Detaylı Analizler</p>', unsafe_allow_html=True)

pages = [
    ("pages/8_Film_Detay.py",                     "🎞️ Film Detay",             "Bir filmin tüm verilerini, ekibini ve benzer filmleri gör."),
    ("pages/1_Yil_Analizi.py",                    "📅 Yıl Trendleri",          "Yıllara göre film sayısı ve IMDB skor trendi."),
    ("pages/2_Tur_Analizi.py",                    "🎭 Tür Analizi",            "Tür dağılımı ve ortalama skorlar."),
    ("pages/3_Butce_Gelir_Analizi.py",            "💰 Bütçe & Gelir",          "Yüksek bütçe başarıyı garantiler mi?"),
    ("pages/4_Yonetmen_Oyuncu_Analizi.py",        "🎬 Yönetmen & Oyuncu",      "En tutarlı yönetmen ve oyuncular kimler?"),
    ("pages/5_Veri_Kesfi.py",                     "🔍 Veri Keşfi",             "Ham veriyi ara, filtrele, keşfet."),
    ("pages/6_Populerlik_Sosyal_Medya_Analizi.py","📈 Popülerlik & Sosyal",    "Oy sayısı, beğeniler, ülke ve içerik analizi."),
]

cols = st.columns(len(pages))
for col, (path, title, desc) in zip(cols, pages):
    with col:
        if st.button(f"{title}\n\n{desc}", key=path, use_container_width=True):
            st.switch_page(path)

st.markdown(
    '<p class="footer">FilmRadar · IMDB 5000 Movie Dataset · Geliştirici: Emel Yılmaz</p>',
    unsafe_allow_html=True,
)
