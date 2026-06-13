import streamlit as st
from utils import load_data

st.set_page_config(
    page_title="Film Veri Analizi",
    page_icon="🎬",
    layout="wide",
)

# Özel stil dosyasını yükle
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎬 Film Veri Analizi</h1>
        <p>
            IMDB 5000 Movie Dataset üzerinde Python (pandas, plotly) ile yapılan
            keşifçi veri analizi (EDA) ve interaktif görselleştirmeler.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# GENEL METRİKLER
# ------------------------------------------------------------
st.markdown('<p class="section-title">📊 Genel Bakış</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Film Sayısı", f"{len(df):,}")
col2.metric("Ortalama IMDB Skoru", f"{df['imdb_score'].mean():.2f}")
col3.metric("Ortalama Bütçe", f"${df['budget'].mean():,.0f}")
col4.metric("Ortalama Gişe Geliri", f"${df['gross'].mean():,.0f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Veri Aralığı (Yıl)", f"{df['title_year'].min()} - {df['title_year'].max()}")
col6.metric("Farklı Yönetmen Sayısı", f"{df['director_name'].nunique():,}")
col7.metric("Farklı Tür Sayısı", f"{df['main_genre'].nunique()}")
col8.metric("En Yüksek IMDB Skoru", f"{df['imdb_score'].max():.1f}")

# ------------------------------------------------------------
# SAYFA REHBERİ
# ------------------------------------------------------------
st.markdown('<p class="section-title">🧭 Sayfalar</p>', unsafe_allow_html=True)

pages = [
    ("pages/1_Yil_Analizi.py", "📅 Yıl Analizi", "Yıllara göre film sayısı ve ortalama IMDB skoru trendi.", True),
    ("pages/2_Tur_Analizi.py", "🎭 Tür Analizi", "Tür dağılımı ve türlere göre ortalama skor karşılaştırması.", True),
    ("pages/3_Butce_Gelir_Analizi.py", "💰 Bütçe & Gelir Analizi", "Bütçe / gişe geliri ilişkisi ve en kârlı filmler.", True),
    ("pages/4_Yonetmen_Oyuncu_Analizi.py", "🎬 Yönetmen & Oyuncu Analizi", "En yüksek ortalama skora sahip yönetmen ve oyuncular.", True),
    ("pages/5_Veri_Kesfi.py", "🔍 Veri Keşfi", "Filtrelenebilir, aranabilir ham veri tablosu.", True),
]

cols = st.columns(len(pages))
for col, (path, title, desc, ready) in zip(cols, pages):
    with col:
        if ready:
            if st.button(
                f"{title}\n\n{desc}",
                key=path,
                use_container_width=True,
                help="Sayfaya gitmek için tıklayın",
            ):
                st.switch_page(path)
        else:
            st.markdown(
                f"""
                <div class="info-card">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                    <p>🚧 Yakında</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    '<p class="footer">Veri seti: IMDB 5000 Movie Dataset &middot; Geliştirici: Emel Yılmaz</p>',
    unsafe_allow_html=True,
)
