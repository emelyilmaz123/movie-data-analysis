# 📡 FilmRadar — Film Keşif ve Analiz Platformu

FilmRadar, IMDB 5000 Movie Dataset üzerinde geliştirilmiş interaktif bir film keşif ve veri analizi platformudur. Bir filmi tarif ederek arayabilir, türe göre öneri alabilir ve detaylı analizlere ulaşabilirsin.

🌐 **Canlı Site:** https://movie-data-analysis-6jfxfzmalaig8m5wxpyjui.streamlit.app

---

## Özellikler

- 🔍 **Aklındaki Filmi Bul** — Yönetmen, oyuncu, tür, konu veya anahtar kelime ile arama. Türkçe kelime desteği mevcut.
- 🎬 **Ne İzlemeliyim?** — Tür, yıl aralığı ve IMDB skoruna göre filtre uygula, en iyi filmleri listele.
- 🎞️ **Film Detay** — Seçilen filmin tüm verileri: ekip, bütçe/gişe, sosyal medya beğenileri, yönetmen filmleri ve benzer film önerileri.
- 📅 **Yıl Trendleri** — Yıllara göre film sayısı ve ortalama IMDB skoru trendi.
- 🎭 **Tür Analizi** — Tür dağılımı ve türlere göre ortalama skorlar.
- 💰 **Bütçe & Gelir** — Bütçe / gişe geliri ilişkisi ve en kârlı filmler.
- 🎬 **Yönetmen & Oyuncu** — En yüksek ortalama skora sahip yönetmen ve oyuncular.
- 🔎 **Veri Keşfi** — Filtrelenebilir, indirilebilir ham veri tablosu.
- 📈 **Popülerlik & Sosyal** — Oy sayısı, Facebook beğenileri, ülke ve içerik derecesi analizleri.

---

## Kullanılan Teknolojiler

- **Python**
- **Streamlit** — Web arayüzü
- **Pandas** — Veri işleme
- **Plotly** — İnteraktif grafikler

---

## Veri Seti

`movie_metadata.csv` — 28 sütun, ~5000 film (IMDB 5000 Movie Dataset)

Temel sütunlar: `movie_title`, `director_name`, `genres`, `title_year`, `budget`, `gross`, `imdb_score`, `plot_keywords`, `num_voted_users`, `movie_facebook_likes`

---

## Kurulum & Çalıştırma

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

---

## Geliştirici

**Emel Yılmaz**
