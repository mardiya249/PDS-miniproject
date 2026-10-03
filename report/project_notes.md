# Academic Project Report & Notes
## Movie & Netflix Data Analysis and Visualization Dashboard

**Subject:** Python for Data Science (PDS)  
**Academic Program:** Bachelor of Engineering (B.E.) in Computer Engineering (Semester 5)  
**Affiliation:** Gujarat Technological University (GTU)  
**Team Structure:** Group of 3 Students  

---

## 1. Project Title & Overview
- **Project Title:** Movie & Netflix Data Analysis and Visualization Dashboard
- **Domain:** Exploratory Data Analysis (EDA), Statistical Computing & Interactive Data Science
- **Technologies Used:** Python 3.x, Pandas, NumPy, Matplotlib, Seaborn, Streamlit

### Project Purpose & Academic Intent
This academic project is **not** a streaming platform clone or video streaming system. Instead, it is an end-to-end data analytics dashboard designed to demonstrate practical mastery over core Python for Data Science concepts, specifically:
1. Ingestion of real-world tabular data from CSV files.
2. Robust data cleaning and handling of missing, duplicate, and unstandardized data.
3. Feature engineering to extract numerical variables from text strings.
4. Rigorous descriptive statistics using **Pandas** and **NumPy**.
5. Static and statistical plotting using **Matplotlib** and **Seaborn**.
6. Deployment of an interactive, responsive web-based data dashboard using **Streamlit**.

---

## 2. Team Division & Responsibilities (Group of 3)

The project architecture is cleanly divided into three distinct modules to reflect balanced individual contributions:

### Student 1: Data Engineering & Preprocessing Lead
- **Primary Module:** `modules/data_cleaning.py`
- **Core Responsibilities:**
  - Designed the CSV ingestion engine with exception handling (`FileNotFoundError`, malformed headers).
  - Implemented missing value audit (`check_missing_values`) calculating counts and percentages.
  - Implemented duplicate detection and row deduplication (`drop_duplicates`).
  - Standardized string columns by trimming extraneous whitespace (`.str.strip()`).
  - Implemented missing value imputation strategies (e.g., `'Unknown Director'`, `'NR'`).
  - Parsed unstructured date strings into `datetime` objects and extracted `year_added` and `month_added`.
  - Engineered numerical variables from duration strings (`movie_duration_min` and `tv_seasons_count`).
  - Monitored and documented memory usage optimization.

### Student 2: Data Analysis & Statistical Lead
- **Primary Module:** `modules/analysis.py`
- **Core Responsibilities:**
  - Implemented KPI computation functions (total titles, format ratios, country coverage, averages).
  - Developed algorithm to explode comma-separated genre tokens (`listed_in`) to eliminate undercounting.
  - Developed multi-country co-production decomposition logic for geographic distribution.
  - Computed five-number summary and dispersion metrics (Mean, Median, Std Dev, Variance, IQR, Skewness) using **Pandas** and **NumPy**.
  - Formulated Pearson correlation matrix strictly across valid continuous/discrete numerical features.
  - Engineered dynamic multi-attribute filter engine (type, year range, country, rating, genre, keyword).
  - Built the heuristic rule engine to generate automated textual insights.

### Student 3: UI Architecture & Visualization Lead
- **Primary Modules:** `modules/visualization.py` & `app.py`
- **Core Responsibilities:**
  - Configured Matplotlib and Seaborn styles, themes, and high-DPI rendering (`Agg` headless backend).
  - Created specialized plotting functions:
    - Donut & Bar chart for content format ratio.
    - Horizontal Seaborn bar chart for Top 10 genres.
    - Geographic bar chart for Top 10 producing nations.
    - Time-series timeline with filled area and peak annotation.
    - Grouped bar chart for audience rating breakdown.
    - Seaborn Histogram + KDE plot with Mean and Median reference lines.
    - Correlation heatmap with triangular mask and annotations.
  - Architected the Streamlit multi-view dashboard layout with custom CSS cards and responsive navigation.
  - Integrated dataset file uploader and interactive CSV download engine.
  - Prepared viva-voce documentation and presentation walkthrough.

---

## 3. Dataset Description & Inherent Challenges

The project utilizes a tabular CSV dataset (`netflix_titles.csv`) matching Kaggle's industry-standard Netflix dataset schema:

| Column Name | Data Type | Description | Data Cleaning Challenge |
| :--- | :--- | :--- | :--- |
| `show_id` | String | Unique record identifier (e.g., `s1`, `s2`) | Check for duplicate records |
| `type` | Categorical | Content format (`Movie` or `TV Show`) | Standardize casing |
| `title` | String | Title of film or television show | Strip leading/trailing whitespaces |
| `director` | String | Director name(s) | 41.7% missing; imputed as `'Unknown Director'` |
| `cast` | String | Lead actors (comma-separated) | 13.4% missing; imputed as `'Unknown Cast'` |
| `country` | String | Producing countries | Contains multiple countries (co-productions) |
| `date_added` | String | Date added to platform | Inconsistent string dates; converted to datetime |
| `release_year` | Integer | Original theatrical/TV release year | Handled as discrete time variable |
| `rating` | Categorical | Maturity rating code (e.g., `TV-MA`, `PG-13`) | Imputed missing values with mode / `'NR'` |
| `duration` | String | Runtime / Season length (e.g., `"90 min"`) | Mixed units; extracted into numeric minutes and seasons |
| `listed_in` | String | Genre tags (comma-separated) | Multiple categories in single string; exploded |
| `description` | String | Short synopsis | Text search enabled |

---

## 4. System Architecture & Workflow

```
[Raw CSV Dataset / User Upload]
               │
               ▼
[Module 1: data_cleaning.py]
  ├── check_missing_values()
  ├── check_duplicates() & drop_duplicates()
  ├── str.strip() & fillna()
  ├── pd.to_datetime() -> year_added, month_added
  └── regex extraction -> movie_duration_min, tv_seasons_count
               │
               ▼
       [Cleaned DataFrame]
               │
       ┌───────┴────────────────────────┐
       ▼                                ▼
[Module 2: analysis.py]       [Sidebar Dynamic Filters]
  ├── get_overall_kpis()          ├── Type (Movie / TV)
  ├── explode genres/countries    ├── Release Year Slider
  ├── calculate_descriptive_stats ├── Country Multi-select
  ├── calculate_correlation()     ├── Rating Multi-select
  └── generate_key_insights()     └── Title / Cast Search
       │                                │
       └───────┬────────────────────────┘
               ▼
       [Filtered Dataset]
               │
       ┌───────┴────────────────────────┐
       ▼                                ▼
[Module 3: visualization.py]    [Streamlit UI: app.py]
  ├── Matplotlib Donut / Area     ├── KPI Metric Cards
  ├── Seaborn Barplots            ├── 12 Interactive Modules
  ├── Seaborn Histplot + KDE      ├── Data Explorer
  └── Seaborn Heatmap             └── CSV Export Engine
```

---

## 5. Descriptive Statistics Implementation (GTU PDS Compliance)

The project leverages both **Pandas** and **NumPy** for descriptive statistical evaluations:

1. **Measures of Central Tendency:**
   - **Mean ($\mu$):** Calculated via `np.mean()` for continuous variables (e.g., movie duration: ~101.4 minutes).
   - **Median:** Computed using `np.median()`, providing a robust statistic immune to extreme outliers.
   - **Mode:** Calculated via `.mode()` for ratings and genres.

2. **Measures of Dispersion & Spread:**
   - **Standard Deviation ($\sigma$):** Calculated with degree of freedom adjustment (`np.std(ddof=1)`).
   - **Variance ($\sigma^2$):** Calculated with `np.var(ddof=1)`.
   - **Range:** Computed using `np.ptp()` (Peak-to-Peak: $Max - Min$).
   - **Interquartile Range (IQR):** Computed as $Q_3 (75th percentile) - Q_1 (25th percentile)$ using `np.percentile()`.

3. **Measures of Distribution Shape:**
   - **Skewness:** Calculated via `series.skew()`, measuring distribution asymmetry. Movie durations typically exhibit near-normal distribution with slight positive skew.

4. **Pearson Correlation Analysis:**
   $$r = \frac{\sum (X - \bar{X})(Y - \bar{Y})}{\sqrt{\sum (X - \bar{X})^2 \sum (Y - \bar{Y})^2}}$$
   - Computed exclusively on numerical features: `release_year`, `year_added`, `movie_duration_min`, and `tv_seasons_count`.
   - Categorical attributes are purposefully excluded to prevent spurious correlation from arbitrary ordinal integer encoding.

---

## 6. Key Analytical Findings & Observations

1. **Format Predominance:** Movies constitute approximately 69% of the catalog, while TV Shows comprise 31%.
2. **Dominant Genres:** Comedies, Dramas, and Action & Adventure rank as the most abundant content categories globally.
3. **Leading Production Nations:** The United States and India lead in overall title production, followed by the United Kingdom, France, and Canada.
4. **Historical Release Surge:** Content production saw an exponential surge post-2015, peaking between 2018 and 2021.
5. **Runtime Centrality:** Feature films cluster around a mean duration of ~101 minutes with an IQR of ~30 minutes.
6. **TV Show Longevity:** Over 65% of television titles feature only a single season, reflecting high competition and selective renewals.
7. **Target Audience:** `TV-MA` and `TV-14` represent the largest rating categories, indicating a library skew toward young adults and mature audiences.

---

## 7. Comprehensive Viva Voce Questions & Answers

### Q1: What is the difference between Pandas and NumPy, and how are they used together in this project?
**Answer:** NumPy is the foundational library for scientific computing in Python, providing support for multi-dimensional arrays (`ndarray`) and vectorized mathematical operations implemented in C. Pandas is built on top of NumPy and provides high-level labeled data structures (`Series` and `DataFrame`) tailored for tabular data analysis. In our project, Pandas handles CSV loading, string splitting, grouping, and date parsing, while NumPy executes fast vectorized numerical calculations such as `np.mean()`, `np.median()`, `np.std()`, and conditional filtering with `np.where()`.

### Q2: Why did you use `.str.split().explode()` on the `listed_in` column?
**Answer:** The `listed_in` column stores multiple genre tags separated by commas within a single string (e.g., `"Dramas, International Movies"`). If we simply counted unique values in this column, compound strings would be treated as independent, unique genres, severely undercounting individual categories like "Dramas" and "International Movies". By using `.str.split(',')` followed by `.explode()`, each genre token is unwrapped into its own row, enabling an exact frequency count of every distinct genre.

### Q3: How did you clean and transform the `duration` column?
**Answer:** The raw `duration` column contained string representations with mixed units: minutes for Movies (e.g., `"90 min"`) and seasons for TV Shows (e.g., `"2 Seasons"`). Averaging these together would be mathematically invalid. Using regular expression extraction `df['duration'].str.extract(r'(\d+)')`, we isolated the numeric magnitude. We then created two distinct features: `movie_duration_min` (numeric minutes for movies, NaN for TV shows) and `tv_seasons_count` (numeric season counts for TV shows, NaN for movies).

### Q4: What imputation techniques did you use for missing values?
**Answer:**
- For `director`, `cast`, and `country`, missing entries were imputed with categorical placeholders (`'Unknown Director'`, `'Unknown Cast'`, `'Unknown Country'`) rather than dropping rows, because dropping them would discard more than 40% of the dataset.
- For `rating`, missing values were imputed with the mode or `'NR'` (Not Rated).
- For `date_added`, values were parsed to `datetime` objects, and any residual nulls were imputed using the release year.

### Q5: Why shouldn't we compute correlation on categorical variables like Genre or Director?
**Answer:** Pearson correlation measures linear relationships between continuous or discrete numerical variables. Assigning arbitrary integers to nominal categorical features (e.g., Action = 1, Drama = 2, Comedy = 3) introduces an artificial order and distance that does not exist in reality. Calculating correlation on such encoded numbers produces mathematically meaningless and deceptive coefficients. Therefore, our correlation analysis is strictly restricted to valid numerical features: `release_year`, `year_added`, `movie_duration_min`, and `tv_seasons_count`.

### Q6: What does the Kernel Density Estimation (KDE) plot show in duration analysis?
**Answer:** A histogram segments data into discrete bins, which can be sensitive to bin-width choices. A Kernel Density Estimation (KDE) curve applies a continuous kernel smoothing function over the data points, estimating the continuous probability density function. It clearly illustrates the central peak (unimodal concentration around 100 minutes) and the spread of movie runtimes.

### Q7: What is the purpose of `@st.cache_data` in Streamlit?
**Answer:** Every time a user interacts with a widget (such as a dropdown, slider, or search input), Streamlit reruns the Python script from top to bottom. If we did not use `@st.cache_data`, the application would re-read the CSV file from disk and execute the entire data cleaning pipeline on every single interaction, creating significant latency. Caching stores the cleaned DataFrame in memory, enabling instantaneous UI reactivity.

### Q8: What is the difference between Mean and Median, and when should Median be preferred?
**Answer:** The Mean is the arithmetic average, calculated by dividing the sum of values by their count. The Median is the middle value of an ordered dataset (50th percentile). The Mean is sensitive to extreme outliers, whereas the Median is non-parametric and resistant to outliers. For example, if a dataset contains a 10-hour documentary, the Mean runtime shifts upward, but the Median remains unaffected.

### Q9: What is the Interquartile Range (IQR) and how is it used in data science?
**Answer:** IQR is the difference between the 75th percentile ($Q_3$) and the 25th percentile ($Q_1$): $IQR = Q_3 - Q_1$. It measures the spread of the middle 50% of the data. IQR is commonly used in Tukey's method for outlier detection, where values below $Q_1 - 1.5 \times IQR$ or above $Q_3 + 1.5 \times IQR$ are flagged as potential anomalies.

### Q10: Why did you set `matplotlib.use('Agg')`?
**Answer:** Matplotlib defaults to GUI backends (like TkAgg, QtAgg, or WX) on desktop operating systems, which attempt to launch an interactive operating system window. In web environments, servers, and Streamlit, running GUI backends can cause execution hangs or thread-blocking issues. The `'Agg'` backend is a headless raster graphics engine that renders figures directly into memory buffers, which Streamlit cleanly displays via `st.pyplot(fig)`.

---

## 8. Future Scope & System Enhancements

1. **Natural Language Processing (NLP) on Descriptions:** Implement TF-IDF vectorization and word clouds to analyze common narrative themes across genres.
2. **Content-Based Recommendation Engine:** Build a cosine-similarity recommendation module matching titles based on genre, director, and cast overlap.
3. **Sentiment Analysis:** Analyze viewer reviews or sentiment scores to correlate ratings with critical reception.
4. **Cloud Database Integration:** Connect the pipeline to a Cloud SQL or PostgreSQL database for real-time data ingestion.
