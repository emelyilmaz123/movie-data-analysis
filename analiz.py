import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

# ------------------------------------------------------------
# 1. VERİYİ YÜKLEME
# ------------------------------------------------------------
df = pd.read_csv('movie_metadata.csv')

print("--- Veri Setinin Boyutu ---")
print(df.shape)

print("\n--- İlk 5 Satır ---")
print(df.head())

print("\n--- Sütun Bilgisi ---")
print(df.info())

# ------------------------------------------------------------
# 2. VERİ TEMİZLEME
# ------------------------------------------------------------
print("\n--- Eksik Değer Sayıları ---")
print(df.isna().sum())

# Tekrarlanan satırları kaldır
df = df.drop_duplicates()

# Film adlarındaki gizli karakterleri temizle
df['movie_title'] = df['movie_title'].str.strip()

# Analiz için kritik sütunlarda eksik olanları çıkar
df = df.dropna(subset=['title_year', 'imdb_score', 'budget', 'gross'])

# Yıl sütununu int yap
df['title_year'] = df['title_year'].astype(int)

# Türleri ayır (ilk tür = ana tür)
df['main_genre'] = df['genres'].str.split('|').str[0]

# Kâr sütunu
df['profit'] = df['gross'] - df['budget']

print(f"\nTemizlik sonrası satır sayısı: {len(df)}")

# ------------------------------------------------------------
# 3. GENEL İSTATİSTİKLER
# ------------------------------------------------------------
print("\n--- IMDB Skoru İstatistikleri ---")
print(df['imdb_score'].describe())

print("\n--- Yıllara Göre Film Sayısı (son 10 yıl) ---")
print(df['title_year'].value_counts().sort_index().tail(10))

# ------------------------------------------------------------
# 4. TÜR ANALİZİ
# ------------------------------------------------------------
print("\n--- En Yaygın 10 Tür ---")
print(df['main_genre'].value_counts().head(10))

print("\n--- Türlere Göre Ortalama IMDB Skoru (en az 50 film) ---")
genre_counts = df['main_genre'].value_counts()
popular_genres = genre_counts[genre_counts >= 50].index
genre_avg_score = df[df['main_genre'].isin(popular_genres)].groupby('main_genre')['imdb_score'].mean().sort_values(ascending=False)
print(genre_avg_score)

# ------------------------------------------------------------
# 5. EN İYİ FİLMLER / YÖNETMENLER
# ------------------------------------------------------------
print("\n--- IMDB Skoruna Göre En Yüksek 10 Film ---")
print(df.sort_values('imdb_score', ascending=False).head(10)[['movie_title', 'director_name', 'title_year', 'imdb_score']])

print("\n--- En Kârlı 10 Film ---")
print(df.sort_values('profit', ascending=False).head(10)[['movie_title', 'title_year', 'budget', 'gross', 'profit']])

print("\n--- En Yüksek Ortalama Skora Sahip Yönetmenler (en az 5 film) ---")
director_counts = df['director_name'].value_counts()
frequent_directors = director_counts[director_counts >= 5].index
director_avg = df[df['director_name'].isin(frequent_directors)].groupby('director_name')['imdb_score'].mean().sort_values(ascending=False)
print(director_avg.head(10))

# ------------------------------------------------------------
# 6. GÖRSELLEŞTİRMELER
# ------------------------------------------------------------

# 6.1 Yıllara göre ortalama IMDB skoru
plt.figure(figsize=(10, 5))
yearly_avg = df.groupby('title_year')['imdb_score'].mean()
yearly_avg = yearly_avg[yearly_avg.index >= 1980]
sns.lineplot(x=yearly_avg.index, y=yearly_avg.values)
plt.title('Yıllara Göre Ortalama IMDB Skoru (1980 sonrası)')
plt.xlabel('Yıl')
plt.ylabel('Ortalama IMDB Skoru')
plt.tight_layout()
plt.savefig('yillara_gore_skor.png')
plt.close()

# 6.2 Türlere göre ortalama IMDB skoru - bar grafik
plt.figure(figsize=(10, 5))
sns.barplot(x=genre_avg_score.index, y=genre_avg_score.values, palette='viridis')
plt.title('Türlere Göre Ortalama IMDB Skoru')
plt.xlabel('Tür')
plt.ylabel('Ortalama IMDB Skoru')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('tur_ortalama_skor.png')
plt.close()

# 6.3 Bütçe vs Gişe geliri - scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='budget', y='gross', data=df, alpha=0.4)
plt.title('Bütçe vs Gişe Geliri')
plt.xlabel('Bütçe ($)')
plt.ylabel('Gişe Geliri ($)')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig('butce_vs_gelir.png')
plt.close()

# 6.4 Korelasyon ısı haritası
plt.figure(figsize=(10, 8))
numeric_cols = ['imdb_score', 'duration', 'budget', 'gross', 'profit',
                 'num_voted_users', 'num_critic_for_reviews', 'movie_facebook_likes']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Sayısal Değişkenler Arası Korelasyon')
plt.tight_layout()
plt.savefig('korelasyon_isi_haritasi.png')
plt.close()

print("\nGrafikler kaydedildi: yillara_gore_skor.png, tur_ortalama_skor.png, butce_vs_gelir.png, korelasyon_isi_haritasi.png")
