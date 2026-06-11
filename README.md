# Footballers from Africa and the European Dream

> Data-driven investigation into African player migration, performance, and hidden talent in European football — 325 players, Big 5 leagues, 2024/25 season

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://john-african-football.streamlit.app)

---

## The Story

Africa produces world-class footballers — Salah, Mané, Drogba, Osimhen,
Lookman, Mbeumo. But the data story behind who makes it to Europe, which
nations dominate, where they go, and who the next generation of hidden
gems are — that story has never been told as a complete analytical piece.

Until now.

---

## Key Findings

### Finding 1 — France dominates African football migration

| League         | African Players | % of Total |
| -------------- | --------------- | ---------- |
| **Ligue 1**    | **159**         | **44%**    |
| La Liga        | 57              | 16%        |
| Serie A        | 55              | 15%        |
| Premier League | 54              | 15%        |
| Bundesliga     | 10              | 3%         |

France has **3x more African players than England** despite the Premier
League paying significantly higher wages. Historical colonial ties and
language links between France and West/North Africa create a pipeline
no other country matches.

### Finding 2 — West Africa dominates by volume, North Africa by quality

- West Africa: 197 players (60.6%) — Nigeria, Ivory Coast, Senegal, Ghana
- North Africa: 73 players (22.5%) — Morocco and Algeria rising rapidly
- Salah (Egypt) leads all African players with 1.255 goal contributions per 90

### Finding 3 — Premier League signs the youngest African talent

Average age of African players by league:

- Premier League: youngest — clubs are scouting earlier
- Ligue 1: most experienced — established pipeline

### Finding 4 — Brentford's African scouting strategy is statistically validated

Bryan Mbeumo (Cameroon) and Yoane Wissa (DR Congo) both rank in the
top 10 African performers in the Big 5 leagues. Two players from the
same mid-table Premier League club — not luck, strategy.

### Finding 5 — Hidden Gems identified

Top undervalued African players outperforming their league level:

1. **Amine Harit** (Morocco, Marseille) — Premier League level performance in Ligue 1
2. **Amine Gouiri** (Algeria, Marseille) — Two Marseille gems hiding in plain sight
3. **Ademola Lookman** (Nigeria, Atalanta) — 15G 5A, statistically belongs at a top PL club

---

## Tech Stack

| Tool                | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Core language             |
| soccerdata + FBref  | Player statistics API     |
| BeautifulSoup4      | Web scraping              |
| Geopandas           | Africa choropleth map     |
| Pandas, NumPy       | Data manipulation         |
| Matplotlib, Seaborn | Visualisations            |
| Scikit-learn        | Performance scoring model |
| Streamlit           | Interactive dashboard     |

---

## Project Structure

    african-football-migration/
    ├── data/
    │   ├── raw/
    │   └── processed/
    │       └── african_players_clean.csv
    ├── notebooks/
    │   ├── 01_data_collection.ipynb
    │   ├── 02_data_cleaning.ipynb
    │   ├── 03_visualisation.ipynb
    │   ├── 04_market_value_analysis.ipynb
    │   └── 05_ml_analysis.ipynb
    ├── reports/
    │   ├── africa_choropleth.png
    │   ├── top_nations.png
    │   ├── league_distribution.png
    │   ├── top_performers.png
    │   └── hidden_gems.png
    ├── dashboard/
    │   └── app.py
    ├── requirements.txt
    └── README.md

---

## Installation

```bash
git clone https://github.com/John-Ayomide/african-football-migration
cd african-football-migration
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

## Author

**John Ayomide**

- GitHub: [@John-Ayomide](https://github.com/John-Ayomide)
- LinkedIn: [Your Profile](https://linkedin.com/in/john-aiyenomuro-19aa26211)
