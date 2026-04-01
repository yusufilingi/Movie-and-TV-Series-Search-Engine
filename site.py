##python -m streamlit run movie_app.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# API key'i oku
API_KEY = os.getenv("OMDB_API_KEY")

# Sayfa başlığı
st.title("🎬 Film Ve Dizi Arama Motoru")

# API key kontrol et
if API_KEY:
    st.success("✅ API Key başarıyla yüklendi!")
else:
    st.error("❌ API Key bulunamadı! .env dosyasını kontrol et.")

# OMDB API base URL
BASE_URL = "http://www.omdbapi.com/"


def search_movies(query):
    """
    Film adına göre OMDB'den arama yapar ve sayfalama ile MAKSİMUM 50 sonuca kadar çeker (max_pages=5).
    """
    all_results = []
    page = 1
    total_results = 0
    max_pages = 2

    while True:
        params = {
            "apikey": API_KEY,
            "s": query,
            "page": page
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            break

        data = response.json()

        if data.get("Response") == "True":
            # KRİTİK DÜZELTME: 'Search' anahtarı büyük harf olmalı.
            current_page_results = data.get("Search", [])
            all_results.extend(current_page_results)

            if page == 1:
                total_results = int(data.get("totalResults", 0))

            # Sonuç sınırı veya toplam sonuç sayısına ulaşıldıysa döngüyü kır
            if len(all_results) >= total_results or page >= max_pages:
                break

            page += 1

        else:
            break

    return all_results


def get_movie_details(imdb_id):
    # Film id'sine göre detaylı bilgi verir
    params = {
        "apikey": API_KEY,
        "i": imdb_id,
        "plot": "full"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            return None
    else:
        return None


# filmleri, yıl puan ve türe göre filtreler
def filter_movies(movies, start_year, end_year, min_rating, selected_genres):
    """
    Filmleri yıl, puan ve türe göre filtreler (Puan ve Tür filtreleri ek API isteği gerektirir).
    """
    filtered = []
    status_text = st.empty()
    allowed_types = ["movie", "series"]  # Sadece film ve dizi tiplerini içeren liste

    for index, movie in enumerate(movies):
        status_text.text(f"Detaylar çekiliyor ve filtre uygulanıyor... ({index + 1}/{len(movies)})")

        # 🔥 TİP KONTROLÜ: Sadece film ve dizileri dahil et
        movie_type = movie.get("Type", "").lower()
        if movie_type not in allowed_types:
            continue

        # Yıl kontrolü
        year = movie.get("Year", "N/A")
        if year != "N/A":
            try:
                year_val = int(year[:4])
                if not (start_year <= year_val <= end_year):
                    continue
            except:
                continue

        # IMDB puanı ve tür kontrolü için detay al (Bu kısım YAVAŞLATAN kısımdır)
        details = get_movie_details(movie['imdbID'])

        if details:
            # Puan kontrolü
            rating = details.get('imdbRating', 'N/A')
            if rating != 'N/A':
                try:
                    rating_val = float(rating)
                    if rating_val < min_rating:
                        continue
                except:
                    continue

            # Tür kontrolü
            if selected_genres:
                movie_genres = details.get('Genre', '')
                genre_match = False
                for selected_genre in selected_genres:
                    if selected_genre.lower() in movie_genres.lower():
                        genre_match = True
                        break

                if not genre_match:
                    continue

        filtered.append(movie)

    status_text.empty()
    return filtered


# Arama arayüzü
st.markdown("---")
st.subheader("🔍 Film Ara")

search_query = st.text_input("Film adı girin:", placeholder="Örn: Inception")

# filtreleme yapma
if search_query:
    st.markdown("### 🎛️ Filtreler")

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Başlangıç yılı", min_value=1900, max_value=2024, value=1900)

    with col2:
        end_year = st.number_input("Bitiş yılı", min_value=1900, max_value=2024, value=2024)

    min_rating = st.slider("IMDB Puanı", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

    genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Adventure", "Animation", "Crime"]
    selected_genres = st.multiselect("🎬 Film Türleri", options=genres, default=None)

if search_query:
    movies = search_movies(search_query)

    if movies:
        # Uyarı: 50 sonuç için detaylar çekiliyor, yine de yavaş sürecektir.
        st.info(
            f"🔍 Toplam {len(movies)} içerik bulundu. Puan ve Tür filtreleri için detaylar kontrol ediliyor. Bu biraz sürebilir...")

        with st.spinner("Filmler Filtreleniyor..."):
            # 🔥 TÜM FİLTRELER KORUNDU: min_rating ve selected_genres gönderildi.
            filtered_movies = filter_movies(movies, start_year, end_year, min_rating, selected_genres)

        if filtered_movies:
            st.success(f"✅ {len(filtered_movies)} film bulundu!")
            movies_to_display = filtered_movies
        else:
            st.warning("😢 Filtrelere uygun film bulunamadı.")
            movies_to_display = []

        # Filmleri 3'lü kolonlarda göster
        for i in range(0, len(movies_to_display), 3):
            cols = st.columns(3)

            for idx, col in enumerate(cols):
                if i + idx < len(movies_to_display):
                    movie = movies_to_display[i + idx]

                    with col:
                        # Film posterini getir
                        if movie.get("Poster") and movie["Poster"] != "N/A":
                            st.image(movie["Poster"], use_container_width=True)
                        else:
                            st.info("📽️ Poster yok")

                        # Film bilgileri
                        st.subheader(movie.get("Title", "Bilinmiyor"))
                        st.write(f"📅 Yıl: {movie.get('Year', 'Bilinmiyor')}")
                        st.write(f"🎬 Tip: {movie.get('Type', 'Bilinmiyor')}")

                        # Detay butonu
                        if st.button("📖 Detayları Gör", key=f"btn_{movie['imdbID']}_{i}_{idx}"):
                            with st.spinner("Yükleniyor..."):
                                details = get_movie_details(movie['imdbID'])

                                if details:
                                    st.markdown("---")
                                    st.write(f"⭐ **IMDB Puanı:** {details.get('imdbRating', 'N/A')}/10")
                                    st.write(f"🎭 **Türler:** {details.get('Genre', 'N/A')}")
                                    st.write(f"⏱️ **Süre:** {details.get('Runtime', 'N/A')}")
                                    st.write(f"🎬 **Yönetmen:** {details.get('Director', 'N/A')}")
                                    st.write(f"🎭 **Oyuncular:** {details.get('Actors', 'N/A')}")
                                    st.write(f"📝 **Özet:** {details.get('Plot', 'N/A')}")

    else:
        st.warning("😭 Üzgünüm film bulunamadı, başka bir film deneyin.")


