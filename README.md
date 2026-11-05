# 🏏 CRICKET INSIGHTS — Match Analyzer

<p align="center">
  <b>Turn cricket match records into meaningful data insights.</b><br>
  A beginner-friendly Python data analysis project using <b>Pandas + NumPy</b> and a free cricket API.
</p>

<p align="center">
  <code>Python</code> · <code>Pandas</code> · <code>NumPy</code> · <code>REST API</code> · <code>CSV</code>
</p>

---

## ✨ What is this?

**Cricket Insights** is a terminal-based cricket analytics project. It collects match results from a free cricket data API (or uses included sample data), cleans the records with Pandas, performs calculations with NumPy, and creates useful summaries.

It is designed as a practical intermediate-level portfolio project: readable code, separate modules, real API integration, local data support, and exportable reports.

## 🚀 Features

- 🌐 Fetch match results from the Cricket Database API.
- 📴 Works offline with the included sample dataset.
- 📊 Match counts by format and competition.
- 🏆 Team wins and win percentage.
- 🧮 Average team score and highest recorded first-innings score.
- 📅 Year-wise match trends.
- 🔎 Filter matches by team or format.
- 💾 Save fetched data and export analysis reports to CSV.
- 🧹 Basic data cleaning and missing-value handling.
- 🔐 Keep your API key in a local `.env` file (never commit it).

## 🧰 Tech stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Main programming language |
| Pandas | Cleaning, filtering, grouping and analysis |
| NumPy | Numerical calculations |
| Cricket Database API | Free cricket match data |
| CSV | Local storage and reports |

## 📁 Project structure

```text
cricket_match_analyzer/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── sample_matches.csv
│
├── reports/
│   └── (generated CSV reports appear here)
│
└── cricket_analyzer/
    ├── __init__.py
    ├── api.py
    ├── analysis.py
    └── data_manager.py
```

## ⚙️ Setup

### 1. Download and extract

Extract the ZIP file, then open the project folder in VS Code.

### 2. Create a virtual environment (recommended)

**Windows CMD:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Run with sample data first

```bash
python app.py
```

Choose **Use sample dataset**. This does not need an API key or internet connection.

## 🔑 Connect the free API

This project uses the **Cricket Database API**.

1. Open [Cricket Database](https://cricketdatabase.com/documentation).
2. Create a free API key (no payment card required according to its current documentation).
3. Copy `.env.example` to a new file named `.env`.
4. Paste your key after `CDB_API_KEY=`.

Example:

```env
CDB_API_KEY=your_api_key_here
```

Then run the project and choose **Fetch from API**.

**Free-tier note:** The API currently documents 50 calls per day, 10 calls per minute, and a full match-list window of the last 30 days on its free key. Older archive coverage is limited. The project requests only one page by default to avoid wasting your daily quota. Check the provider's current limits before use.

API documentation:
- [Getting started](https://cricketdatabase.com/documentation/guides/getting-started)
- [Matches endpoint](https://cricketdatabase.com/documentation/matches)
- [Free plan limits](https://cricketdatabase.com/documentation/guides/plans)

## ▶️ How to use

Start the app:

```bash
python app.py
```

Menu options:

1. Use included sample dataset
2. Fetch recent matches from the API
3. View overall dashboard
4. Compare teams
5. Filter matches
6. Export cleaned data and reports
7. Exit

API data is saved to `data/matches.csv`. Generated summaries are saved inside `reports/`.

## 📈 Example analysis questions

Try answering these after loading the data:

- Which team has the most wins in the loaded dataset?
- Which match format appears most often?
- What is the average recorded first-innings score?
- Which competition has the largest number of matches?
- How does the number of matches change by year?
- Which teams have played at least five matches in the current dataset?

> Important: API data coverage depends on your free plan and the date range requested. Win percentages describe only the matches currently loaded, not a team's all-time record.

## 🧠 What you will learn

- Reading JSON from a REST API using Python's standard library.
- Working with CSV files.
- Cleaning data with Pandas.
- Using `groupby()`, `value_counts()`, filtering and sorting.
- Using NumPy for mean, median and standard deviation.
- Splitting a project into reusable Python modules.
- Handling missing values and API errors.
- Writing analysis results to files.

## 🛠️ Troubleshooting

**`ModuleNotFoundError: pandas` or `numpy`**
```bash
pip install -r requirements.txt
```

**API key error**
- Check that `.env` is in the project root.
- Make sure the key is copied correctly.
- Do not add quotes around the key.
- Check your provider dashboard and daily quota.

**No API results**
- Use the sample dataset to explore the project.
- Try again later or check the API status and documentation.
- The free plan has date and coverage limits.

## 🔒 Security

`.env` is ignored by Git. Never upload your real API key to GitHub, screenshots, or public code.

## 🌱 Future improvements

- Player-level scorecard analysis.
- Bowling economy and batting strike-rate analysis when scorecard data is available.
- Interactive charts with Matplotlib.
- Head-to-head team comparison.
- SQLite storage and a small dashboard.

## 👨‍💻 Made for learning

Built as a Python + NumPy + Pandas portfolio project. The code is intentionally split into small functions so a beginner can read, test and improve it.

**If you find it useful, give the repository a ⭐**
