STRINGS = {
    'tr': {
        # Genel
        'search_placeholder': 'Film adı ile filtrele...',
        'no_film_found': 'Film bulunamadı.',
        'results_label': 'Sonuçlar:',
        'film': 'Film',
        'director': 'Yönetmen',
        'actor': 'Başrol',
        'genre': 'Tür',
        'year': 'Yıl',
        'imdb': 'IMDB',
        'budget': 'Bütçe',
        'gross': 'Gişe Geliri',
        'profit': 'Kâr',
        'finding': '📌 Bulgu',

        # Ana sayfa
        'hero_sub': 'Tarif et. Biz bulalım.',
        'hero_desc': 'Adını hatırlamıyor musun? Türünü, oyuncusunu, yönetmenini ya da aklındaki herhangi bir şeyi yaz. FilmRadar binlerce film arasından en iyi eşleşmeleri sana getirir.',
        'search_title': '🔍 Aklındaki filmi bul',
        'search_main_placeholder': 'Örn: Nolan   psikolojik gerilim   hapishane   uzay   Tom Hanks',
        'no_match': 'Eşleşen film bulunamadı. Farklı kelimeler dene.',
        'found': 'film bulundu',
        'showing_top': 'en iyi sonuçlar gösteriliyor',
        'lead_actor': 'Başrol',
        'genres': 'Türler',
        'watch_title': '🎬 Ne izlemeliyim?',
        'watch_desc': 'Türünü seç, yıl ve skor filtrele — sana en iyileri getirelim.',
        'genre_select': 'Tür',
        'year_range': 'Yıl aralığı',
        'min_score': 'Minimum IMDB skoru',
        'no_match_filter': 'Bu kriterlere uyan film bulunamadı. Filtreleri genişletmeyi dene.',
        'db_title': '📊 Veri Tabanı',
        'total_films': 'Toplam Film',
        'avg_imdb': 'Ortalama IMDB',
        'directors': 'Yönetmen Sayısı',
        'year_range_label': 'Yıl Aralığı',
        'analysis_title': '📈 Detaylı Analizler',
        'footer': 'FilmRadar · IMDB 5000 Movie Dataset · Geliştirici: Emel Yılmaz',
        'footer_desc': 'FilmRadar, IMDB 5000 veri seti üzerine kurulu interaktif bir film keşif ve analiz platformudur. Aklındaki filmi tarif et, türüne göre öneri al, detaylı analizlere ulaş.',
        'footer_dev': 'Geliştirici',
        'footer_source': 'Kaynak Kod',
        'footer_platform': 'Platform',
        'footer_copy': '© 2024 FilmRadar · Emel Yılmaz tarafından geliştirildi.',
        'footer_stat_films': 'Film',
        'footer_stat_directors': 'Yönetmen',
        'footer_stat_genres': 'Tür',
        'footer_stat_years': 'Yıl',
        'pages': [
            ("pages/8_Film_Detay.py", "🎞️ Film Detay", "Bir filmin tüm verilerini, ekibini ve benzer filmleri gör."),
            ("pages/1_Yil_Analizi.py", "📅 Yıl Trendleri", "Yıllara göre film sayısı ve IMDB skor trendi."),
            ("pages/2_Tur_Analizi.py", "🎭 Tür Analizi", "Tür dağılımı ve ortalama skorlar."),
            ("pages/3_Butce_Gelir_Analizi.py", "💰 Bütçe & Gelir", "Yüksek bütçe başarıyı garantiler mi?"),
            ("pages/4_Yonetmen_Oyuncu_Analizi.py", "🎬 Yönetmen & Oyuncu", "En tutarlı yönetmen ve oyuncular kimler?"),
            ("pages/5_Veri_Kesfi.py", "🔍 Veri Keşfi", "Ham veriyi ara, filtrele, keşfet."),
            ("pages/6_Populerlik_Sosyal_Medya_Analizi.py", "📈 Popülerlik & Sosyal", "Oy sayısı, beğeniler, ülke ve içerik analizi."),
        ],

        # Yıl Analizi
        'yil_title': '📅 Yıl Analizi',
        'yil_desc': 'Filmlerin yıllara göre dağılımı ve ortalama IMDB skoru trendi.',
        'yil_slider': 'Yıl Aralığı',
        'yil_count': 'Seçilen Aralıktaki Film Sayısı',
        'yil_avg': 'Seçilen Aralıkta Ortalama Skor',
        'yil_chart1': 'Yıllara Göre Film Sayısı',
        'yil_chart2': 'Yıllara Göre Ortalama IMDB Skoru',
        'yil_finding': '2000\'li yıllardan sonra üretilen film sayısı önemli ölçüde artmıştır, ancak ortalama IMDB skorlarında zamana göre belirgin bir düşüş eğilimi görülmektedir.',

        # Tür Analizi
        'tur_title': '🎭 Tür Analizi',
        'tur_desc': 'Film türlerinin dağılımı ve türlere göre ortalama IMDB skoru.',
        'tur_select': 'Türleri seçin',
        'tur_chart1': 'Seçilen Türlere Göre Film Sayısı',
        'tur_chart2': 'Türlere Göre Ortalama IMDB Skoru',
        'tur_finding': 'Biyografi, Suç ve Dram türleri ortalamada en yüksek IMDB skorlarına sahiptir. Korku ve Komedi gibi yüksek hacimli türler ise ortalama skor bakımından daha düşük seviyelerde kalmaktadır.',

        # Bütçe & Gelir
        'butce_title': '💰 Bütçe & Gelir Analizi',
        'butce_desc': 'Filmlerin bütçesi ile gişe geliri arasındaki ilişki ve en kârlı filmler.',
        'butce_chart': 'Bütçe vs Gişe Geliri',
        'butce_top': '🏆 En Kârlı 10 Film',
        'butce_finding': 'Bütçe ile gişe geliri arasında pozitif bir ilişki gözlemlenmektedir, ancak yüksek bütçeli birçok film beklenen geliri sağlayamamıştır.',

        # Yönetmen & Oyuncu
        'yon_title': '🎬 Yönetmen & Oyuncu Analizi',
        'yon_desc': 'En yüksek ortalama IMDB skoruna sahip yönetmen ve oyuncular.',
        'yon_placeholder': 'Film adı yaz, yönetmen ve oyuncu analizini gör...',
        'yon_min_films': 'Minimum film sayısı',
        'yon_dir_chart': 'En Yüksek Ortalama Skora Sahip Yönetmenler',
        'yon_act_chart': 'En Yüksek Ortalama Skora Sahip Oyuncular',
        'yon_total': 'Toplam Film',
        'yon_avg': 'Ort. IMDB Skoru',
        'yon_best': 'En Yüksek Skor',
        'yon_avg_gross': 'Ort. Gişe Geliri',
        'yon_no_other': 'Veri setinde bu yönetmenin başka filmi bulunmuyor.',
        'yon_finding': 'Christopher Nolan, Quentin Tarantino ve James Cameron gibi yönetmenler en az 5 film çekmiş yönetmenler arasında en yüksek ortalama IMDB skoruna sahiptir.',

        # Veri Keşfi
        'veri_title': '🔍 Veri Keşfi',
        'veri_desc': 'Veri setini filtreleyerek ham haliyle inceleyin.',
        'veri_genre': 'Tür',
        'veri_year': 'Yıl Aralığı',
        'veri_score': 'IMDB Skoru Aralığı',
        'veri_search': 'Film adında ara',
        'veri_found': 'film bulundu.',
        'veri_download': 'CSV olarak indir',
        'veri_cols': ['Film', 'Yıl', 'Tür', 'Yönetmen', 'IMDB Skoru', 'Bütçe ($)', 'Gişe Geliri ($)', 'Kâr ($)', 'Süre (dk)'],

        # Popülerlik
        'pop_title': '📈 Popülerlik & Sosyal Medya Analizi',
        'pop_desc': 'Oy sayısı, eleştiri sayısı, Facebook beğenileri, ülke ve içerik derecesi bazlı analizler.',
        'pop_votes': 'Oy Sayısı',
        'pop_fb': 'Facebook Beğenisi',
        'pop_chart1': 'Oy Sayısı vs IMDB Skoru',
        'pop_chart2': 'Facebook Beğenisi vs Gişe Geliri',
        'pop_top_voted': '🗳️ En Çok Oy Alan 10 Film',
        'pop_country': '🌍 Ülke Analizi',
        'pop_rating': '🎟️ İçerik Derecesi Analizi',
        'pop_cols': ['Film', 'Yıl', 'Oy Sayısı', 'Eleştiri Sayısı', 'IMDB Skoru'],

        # Film Detay
        'detay_title': '🎞️ Film Detay',
        'detay_desc': 'Film adını yaz, listeden seç — tüm verileri ve analizini gör.',
        'detay_placeholder': 'Film adı yaz...',
        'detay_no_film': 'Aramak istediğin filmin adını yaz.',
        'detay_scores': '⭐ Skorlar & Popülerlik',
        'detay_crew': '🎭 Ekip',
        'detay_budget': '💰 Bütçe & Gişe',
        'detay_social': '📱 Sosyal Medya Beğenileri',
        'detay_similar': '🍿 Benzer Filmler',
        'detay_no_similar': 'Benzer film bulunamadı.',
        'detay_votes': 'Oy Sayısı',
        'detay_critics': 'Eleştiri Sayısı',
        'detay_users': 'Kullanıcı Yorumu',
        'detay_2nd': '2. Oyuncu',
        'detay_3rd': '3. Oyuncu',
        'detay_unrated': 'Belirtilmemiş',
        'detay_film_page': 'Film Sayfası',
        'detay_profit': 'Kâr / Zarar',
        'detay_bar_title': 'Bütçe & Gişe Karşılaştırması',
        'detay_no_director': 'Veri setinde bu yönetmenin başka filmi bulunmuyor.',
        'detay_similar_caption': 'Aynı tür · IMDB skoru',
    },

    'en': {
        # General
        'search_placeholder': 'Filter by film title...',
        'no_film_found': 'No film found.',
        'results_label': 'Results:',
        'film': 'Film',
        'director': 'Director',
        'actor': 'Lead Actor',
        'genre': 'Genre',
        'year': 'Year',
        'imdb': 'IMDB',
        'budget': 'Budget',
        'gross': 'Box Office',
        'profit': 'Profit',
        'finding': '📌 Finding',

        # Home page
        'hero_sub': 'Describe it. We find it.',
        'hero_desc': "Can't remember the title? Just describe the movie — genre, actor, director, mood, keyword. FilmRadar scans thousands of films and brings back the best matches.",
        'search_title': '🔍 Find that movie',
        'search_main_placeholder': 'e.g.  Nolan   psychological thriller   prison   space   Tom Hanks',
        'no_match': 'No matches found. Try different keywords.',
        'found': 'films found',
        'showing_top': 'showing top results',
        'lead_actor': 'Lead Actor',
        'genres': 'Genres',
        'watch_title': '🎬 What to Watch?',
        'watch_desc': 'Pick a genre, filter by year and score — we\'ll bring you the best.',
        'genre_select': 'Genre',
        'year_range': 'Year range',
        'min_score': 'Minimum IMDB score',
        'no_match_filter': 'No films match these filters. Try widening the range.',
        'db_title': '📊 Database Stats',
        'total_films': 'Total Films',
        'avg_imdb': 'Avg IMDB Score',
        'directors': 'Directors',
        'year_range_label': 'Year Range',
        'analysis_title': '📈 Deep Dive Analysis',
        'footer': 'FilmRadar · IMDB 5000 Movie Dataset · Built by Emel Yılmaz',
        'footer_desc': 'FilmRadar is an interactive movie discovery and analysis platform built on the IMDB 5000 dataset. Describe a film, get genre recommendations, and explore in-depth analytics.',
        'footer_dev': 'Developer',
        'footer_source': 'Source Code',
        'footer_platform': 'Platform',
        'footer_copy': '© 2024 FilmRadar · Built by Emel Yılmaz',
        'footer_stat_films': 'Films',
        'footer_stat_directors': 'Directors',
        'footer_stat_genres': 'Genres',
        'footer_stat_years': 'Years',
        'pages': [
            ("pages/8_Film_Detay.py", "🎞️ Film Detail", "See full data, crew and similar films for any movie."),
            ("pages/1_Yil_Analizi.py", "📅 Year Trends", "Film count and IMDB score trends over the decades."),
            ("pages/2_Tur_Analizi.py", "🎭 Genre Breakdown", "Genre distribution and average scores."),
            ("pages/3_Butce_Gelir_Analizi.py", "💰 Budget & Revenue", "Do bigger budgets mean bigger hits?"),
            ("pages/4_Yonetmen_Oyuncu_Analizi.py", "🎬 Directors & Actors", "Who consistently makes great films?"),
            ("pages/5_Veri_Kesfi.py", "🔍 Data Explorer", "Search, filter and download the raw dataset."),
            ("pages/6_Populerlik_Sosyal_Medya_Analizi.py", "📈 Popularity & Social", "Votes, likes, country and content rating breakdowns."),
        ],

        # Year Analysis
        'yil_title': '📅 Year Analysis',
        'yil_desc': 'Film distribution and average IMDB score trend over the years.',
        'yil_slider': 'Year Range',
        'yil_count': 'Films in Selected Range',
        'yil_avg': 'Avg Score in Selected Range',
        'yil_chart1': 'Number of Films by Year',
        'yil_chart2': 'Average IMDB Score by Year',
        'yil_finding': 'The number of films produced increased significantly after the 2000s, but there is a noticeable downward trend in average IMDB scores over time.',

        # Genre Analysis
        'tur_title': '🎭 Genre Analysis',
        'tur_desc': 'Distribution of film genres and average IMDB score by genre.',
        'tur_select': 'Select genres',
        'tur_chart1': 'Film Count by Selected Genres',
        'tur_chart2': 'Average IMDB Score by Genre',
        'tur_finding': 'Biography, Crime and Drama genres have the highest average IMDB scores. High-volume genres like Horror and Comedy tend to score lower on average.',

        # Budget & Revenue
        'butce_title': '💰 Budget & Revenue Analysis',
        'butce_desc': 'Relationship between budget and box office revenue, and the most profitable films.',
        'butce_chart': 'Budget vs Box Office Revenue',
        'butce_top': '🏆 Top 10 Most Profitable Films',
        'butce_finding': 'There is a positive relationship between budget and box office revenue, but many high-budget films failed to meet expectations.',

        # Director & Actor
        'yon_title': '🎬 Director & Actor Analysis',
        'yon_desc': 'Directors and actors with the highest average IMDB scores.',
        'yon_placeholder': 'Type a film title to see director & actor analysis...',
        'yon_min_films': 'Minimum number of films',
        'yon_dir_chart': 'Directors with Highest Average Score',
        'yon_act_chart': 'Actors with Highest Average Score',
        'yon_total': 'Total Films',
        'yon_avg': 'Avg IMDB Score',
        'yon_best': 'Highest Score',
        'yon_avg_gross': 'Avg Box Office',
        'yon_no_other': 'No other films by this director in the dataset.',
        'yon_finding': 'Directors like Christopher Nolan, Quentin Tarantino and James Cameron have the highest average IMDB scores among directors with at least 5 films.',

        # Data Explorer
        'veri_title': '🔍 Data Explorer',
        'veri_desc': 'Browse and filter the raw dataset.',
        'veri_genre': 'Genre',
        'veri_year': 'Year Range',
        'veri_score': 'IMDB Score Range',
        'veri_search': 'Search by film title',
        'veri_found': 'films found.',
        'veri_download': 'Download as CSV',
        'veri_cols': ['Film', 'Year', 'Genre', 'Director', 'IMDB Score', 'Budget ($)', 'Box Office ($)', 'Profit ($)', 'Duration (min)'],

        # Popularity
        'pop_title': '📈 Popularity & Social Media Analysis',
        'pop_desc': 'Analysis by vote count, critic count, Facebook likes, country and content rating.',
        'pop_votes': 'Vote Count',
        'pop_fb': 'Facebook Likes',
        'pop_chart1': 'Vote Count vs IMDB Score',
        'pop_chart2': 'Facebook Likes vs Box Office Revenue',
        'pop_top_voted': '🗳️ Top 10 Most Voted Films',
        'pop_country': '🌍 Country Analysis',
        'pop_rating': '🎟️ Content Rating Analysis',
        'pop_cols': ['Film', 'Year', 'Vote Count', 'Critic Count', 'IMDB Score'],

        # Film Detail
        'detay_title': '🎞️ Film Detail',
        'detay_desc': 'Type a film name, select from the list — see all data and analysis.',
        'detay_placeholder': 'Type a film name...',
        'detay_no_film': 'Type a film name to search.',
        'detay_scores': '⭐ Scores & Popularity',
        'detay_crew': '🎭 Crew',
        'detay_budget': '💰 Budget & Box Office',
        'detay_social': '📱 Social Media Likes',
        'detay_similar': '🍿 Similar Films',
        'detay_no_similar': 'No similar films found.',
        'detay_votes': 'Vote Count',
        'detay_critics': 'Critic Count',
        'detay_users': 'User Reviews',
        'detay_2nd': '2nd Actor',
        'detay_3rd': '3rd Actor',
        'detay_unrated': 'Not rated',
        'detay_film_page': 'Film Page',
        'detay_profit': 'Profit / Loss',
        'detay_bar_title': 'Budget & Box Office Comparison',
        'detay_no_director': 'No other films by this director in the dataset.',
        'detay_similar_caption': 'Same genre · IMDB score',
    }
}


def get_lang():
    import streamlit as st
    return st.session_state.get('lang', 'tr')


def t(key):
    import streamlit as st
    lang = st.session_state.get('lang', 'tr')
    return STRINGS[lang].get(key, key)


def render_lang_selector():
    import streamlit as st
    if 'lang' not in st.session_state:
        st.session_state['lang'] = 'tr'
    with st.sidebar:
        st.markdown("---")
        secim = st.radio("🌐 Dil / Language", ["🇹🇷 Türkçe", "🇬🇧 English"],
                         index=0 if st.session_state['lang'] == 'tr' else 1,
                         label_visibility="collapsed")
        yeni_lang = 'tr' if secim == "🇹🇷 Türkçe" else 'en'
        if yeni_lang != st.session_state['lang']:
            st.session_state['lang'] = yeni_lang
            st.rerun()
