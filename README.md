---
title: Movie & Netflix Data Analysis Dashboard
emoji: 🎬
colorFrom: red
colorTo: gray
sdk: streamlit
sdk_version: "1.30.0"
app_file: app.py
pinned: false
license: mit
---

# 🎬 Movie & Netflix Data Analysis and Visualization Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4c72b0.svg)](https://seaborn.pydata.org/)

An interactive web-based data science dashboard built for the **Gujarat Technological University (GTU)** 5th Semester Computer Engineering subject **Python for Data Science (PDS)**.

> **Academic Note:** This project is **not** a streaming video platform clone. Its primary objective is to demonstrate core **Python for Data Science** concepts: data cleaning, descriptive statistics, feature engineering, exploratory data analysis (EDA), static plotting with Matplotlib/Seaborn, and deployment using Streamlit.

---

## 👥 Student Team Division (Group of 3)

| Student Role | Module | Key Contributions & Academic Concepts |
| :--- | :--- | :--- |
| **Student 1: Data Engineering** | `modules/data_cleaning.py` | CSV loading, null value imputation, duplicate removal, whitespace stripping, datetime parsing (`year_added`, `month_added`), numerical extraction of runtimes (`movie_duration_min`, `tv_seasons_count`). |
| **Student 2: Data Analysis** | `modules/analysis.py` | Overall KPI calculations, genre/country string splitting and explosion, release year distribution, descriptive statistics (Mean, Median, Std, IQR, Skewness), Pearson correlation analysis, dynamic filtering engine. |
| **Student 3: UI & Visualization** | `modules/visualization.py` & `app.py` | Matplotlib and Seaborn visualization functions (Donut, Bar, KDE, Heatmap), Streamlit dashboard architecture, KPI cards, CSV downloader, testing, and viva preparation. |

---

## 📁 Project Directory Structure

```
movie_netflix_analysis/
│
├── app.py                     # Main Streamlit dashboard application
├── requirements.txt           # Project dependencies
├── README.md                  # Comprehensive setup and project guide
│
├── data/
│   ├── netflix_titles.csv     # Primary dataset (1,000+ records)
│   └── generate_dataset.py    # Dataset generator script
│
├── modules/
│   ├── data_cleaning.py       # Module 1: Data loading, auditing, and cleaning (Student 1)
│   ├── analysis.py            # Module 2: Statistical analysis & filtering (Student 2)
│   └── visualization.py       # Module 3: Matplotlib & Seaborn visualizations (Student 3)
│
└── report/
    └── project_notes.md       # Comprehensive academic project notes & viva Q&A
```

---

## 🧭 Dashboard Navigation Structure (Dark Cinematic UI)

- **🎬 Header:** Movie & Netflix Data Analysis Dashboard
- **Sidebar Navigation:**
  - 🏠 **Dashboard:** Executive KPI cards (Total Titles, Movies, TV Shows, Countries, Avg Release Year), 2-column chart layout (Donut chart & Top Genres, Yearly Trend line chart & Top Countries), Rating Distribution bar chart, and 4–6 dynamic Key Insights.
  - 🎭 **Genre Analysis:** Total unique genres, most common genre, Top 10 genres chart, and genre frequency table.
  - 🌍 **Country Analysis:** Unique country counts, top country, Top 10 nations bar chart, and statistics table.
  - 📅 **Release Analysis:** Min/Max/Avg release years, temporal line chart, and yearly release volume bar chart.
  - ⭐ **Rating Analysis:** Most common rating, audience rating distribution chart, and breakdown table.
  - ⏱️ **Duration Analysis:** Movie runtime metrics (Mean, Min, Max, Std), histogram with KDE curve, and TV show seasons analysis.
  - 🔎 **Explore Data:** Title/Director/Cast live search, filtered records counter, interactive dataframe, and CSV dataset export.
  - ℹ️ **About Project:** Project details, GTU syllabus mapping, technology stack, and student group member placeholders.

- **Dynamic Sidebar Filters:**
  - Content Type (`All`, `Movie`, `TV Show`)
  - Release Year Slider
  - Country Multi-select
  - Rating Multi-select
  - Genre Multi-select

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your computer.
- A terminal (PowerShell, Command Prompt, or Bash).

### 1. Clone or Navigate to the Project Folder
```bash
cd path/to/movie_netflix_analysis
```

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt):
.\venv\Scripts\activate.bat

# Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Execute the following command in your terminal:
```bash
streamlit run app.py
```

Streamlit will launch a local development server and automatically open the application in your default web browser at:
```
http://localhost:8501
```

---

## 🧪 Testing the Modules Independently

Each module can be tested independently in the terminal to verify individual student work:

```bash
# Test Student 1's Data Cleaning Module:
python modules/data_cleaning.py

# Test Student 2's Statistical Analysis Module:
python modules/analysis.py

# Test Dataset Generator:
python data/generate_dataset.py
```

---

## 🎓 Academic Viva Questions Quick Reference

1. **How does Pandas handle missing data?**  
   Via `.isnull()`, `.isna()`, `.dropna()`, and `.fillna()`. We imputed missing text values (`'Unknown Director'`) rather than dropping them to preserve 40%+ of catalog records.
2. **Why extract numeric duration?**  
   Strings like `"90 min"` cannot be mathematically analyzed. Extracting the numeric value `90.0` allows calculating Mean, Median, and Standard Deviation with NumPy.
3. **Why avoid correlation on categorical variables?**  
   Pearson correlation requires continuous or discrete numeric data. Mapping arbitrary integers to nominal categories (e.g. Action=1, Comedy=2) imposes artificial ordinal ranking, producing invalid mathematical results.
4. **What is the purpose of `@st.cache_data`?**  
   It memoizes computationally expensive data loading and cleaning, preventing unnecessary disk I/O and reprocessing on every user interaction.

For full detailed notes, see [`report/project_notes.md`](file:///p:/Experience/movie_netflix_analysis/report/project_notes.md).
