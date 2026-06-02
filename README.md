#  Movie and TV Series Search Engine

A Streamlit-based web application for searching movies and TV series using the OMDB API, with multi-filter support and detailed information display.

---

##  Features

- **Full-text search** — Search any movie or TV series by title via OMDB
- **Advanced filtering** — Filter results by release year range, minimum IMDB rating, and genre(s)
- **Paginated results** — Fetches up to 20 results per search with pagination support
- **Detail view** — Expand any title to see its full plot, cast, director, runtime, and IMDB score
- **Poster display** — Movie/series posters rendered in a clean 3-column grid layout
- **Type filtering** — Automatically excludes non-movie/series results (e.g. games, episodes)

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Framework | Python, Streamlit |
| Data Source | OMDB API |
| Environment | python-dotenv |

---

##  Installation

**1. Clone the repository**
```bash
git clone https://github.com/yusufilingi/film-dizi-arama-sitesi.git
cd film-dizi-arama-sitesi
```

**2. Install dependencies**
```bash
pip install streamlit requests python-dotenv
```

**3. Set up environment variables**

Create a `.env` file in the root directory:
```
OMDB_API_KEY=your_omdb_api_key_here
```

**4. Run the app**
```bash
streamlit run site.py
```

Then open `http://localhost:8501` in your browser.

---

##  API Key

Get your free OMDB API key at [omdbapi.com](https://www.omdbapi.com/apikey.aspx). The free tier allows up to 1,000 requests per day.

---

## 📋 How It Works

1. Enter a movie or series title in the search box
2. Optionally apply filters: year range, minimum IMDB rating, genre(s)
3. The app fetches up to 20 results from OMDB and runs type/year filters client-side
4. For rating and genre filtering, individual detail API calls are made per result
5. Results are displayed in a 3-column grid with posters and basic info
6. Click **"Detayları Gör"** on any title to expand full details

> Note: Applying IMDB rating or genre filters requires one additional API call per result, which may slow down the response time for large result sets.

---

## Project Structure

```
├── site.py       # Main Streamlit app — search, filter, display logic
└── .env          # OMDB API key (not committed)
```

---

##  Interface

- Search bar with placeholder text
- Year range inputs (start / end)
- IMDB rating slider (0.0 – 10.0)
- Genre multi-select (Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller, Adventure, Animation, Crime)
- 3-column poster grid with expandable detail panels

---

## Author

**Yusuf İlingi** — Management Information Systems student at Istanbul Gelişim University

[GitHub](https://github.com/yusufilingi)
