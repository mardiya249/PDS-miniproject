"""
=============================================================================
MODULE 2: STATISTICAL ANALYSIS & DATA PROCESSING (Student 2 Responsibility)
=============================================================================
Subject: Python for Data Science (GTU)
Project: Movie & Netflix Data Analysis and Visualization Dashboard

This module handles:
1. Overall KPI computation (totals, averages, dominant categories)
2. Content Type breakdown (Movies vs TV Shows)
3. Genre frequency analysis with comma-separated list explosion
4. Country production analysis with multi-country splitting
5. Release year distribution & historical timeline trends
6. Content rating distribution (with cross-tabulation by type)
7. Duration & season analytics using Pandas & NumPy
8. Comprehensive descriptive statistics (Mean, Median, Std, IQR, Skewness)
9. Pearson correlation analysis on valid numerical features
10. Dynamic multi-criteria dataset filtering
11. Automated algorithmic key insights generation
=============================================================================
"""

import pandas as pd
import numpy as np


def get_overall_kpis(df):
    """
    Compute core Executive Key Performance Indicators (KPIs) from the dataset.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        dict: Key statistical metrics for dashboard header cards
    """
    if df is None or df.empty:
        return {
            "total_titles": 0, "total_movies": 0, "total_tv_shows": 0,
            "pct_movies": 0.0, "pct_tv_shows": 0.0, "movie_to_tv_ratio": "0:0",
            "total_countries": 0, "avg_release_year": 0, "median_release_year": 0,
            "most_common_genre": "N/A", "most_common_rating": "N/A",
            "avg_movie_duration": 0.0, "max_tv_seasons": 0
        }
        
    total_titles = len(df)
    
    # Movie & TV Show counts
    movie_mask = df['type'].str.lower() == 'movie'
    tv_mask = df['type'].str.lower() == 'tv show'
    
    total_movies = int(movie_mask.sum())
    total_tv_shows = int(tv_mask.sum())
    
    pct_movies = round((total_movies / total_titles) * 100, 1) if total_titles > 0 else 0.0
    pct_tv_shows = round((total_tv_shows / total_titles) * 100, 1) if total_titles > 0 else 0.0
    
    # Movie to TV Show Ratio
    if total_tv_shows > 0:
        movie_to_tv_ratio = f"{round(total_movies / total_tv_shows, 1)}:1"
    elif total_movies > 0:
        movie_to_tv_ratio = f"{total_movies}:0"
    else:
        movie_to_tv_ratio = "0:0"
    
    # Country counting (exploding comma-separated countries)
    all_countries = set()
    for item in df['country'].dropna():
        for c in str(item).split(','):
            c_clean = c.strip()
            if c_clean and c_clean != 'Unknown Country':
                all_countries.add(c_clean)
    total_countries = len(all_countries)
    
    # Average and Median Release Year
    if 'release_year' in df.columns and not df['release_year'].dropna().empty:
        avg_release_year = int(round(df['release_year'].mean()))
        median_release_year = int(round(df['release_year'].median()))
    else:
        avg_release_year = 0
        median_release_year = 0
    
    # Most Common Genre
    all_genres = []
    for g_list in df['listed_in'].dropna():
        for g in str(g_list).split(','):
            g_clean = g.strip()
            if g_clean:
                all_genres.append(g_clean)
    most_common_genre = pd.Series(all_genres).mode().iloc[0] if all_genres else "N/A"
    
    # Most Common Rating
    most_common_rating = df['rating'].mode().iloc[0] if 'rating' in df.columns and not df['rating'].dropna().empty else "N/A"
    
    # Average Movie Duration (minutes) using NumPy
    if 'movie_duration_min' in df.columns:
        valid_movie_dur = df['movie_duration_min'].dropna()
        avg_movie_dur = round(float(np.mean(valid_movie_dur)), 1) if not valid_movie_dur.empty else 0.0
    else:
        avg_movie_dur = 0.0
        
    # Max TV seasons
    if 'tv_seasons_count' in df.columns:
        valid_seasons = df['tv_seasons_count'].dropna()
        max_seasons = int(np.max(valid_seasons)) if not valid_seasons.empty else 0
    else:
        max_seasons = 0
        
    return {
        "total_titles": total_titles,
        "total_movies": total_movies,
        "total_tv_shows": total_tv_shows,
        "pct_movies": pct_movies,
        "pct_tv_shows": pct_tv_shows,
        "movie_to_tv_ratio": movie_to_tv_ratio,
        "total_countries": total_countries,
        "avg_release_year": avg_release_year,
        "median_release_year": median_release_year,
        "most_common_genre": most_common_genre,
        "most_common_rating": most_common_rating,
        "avg_movie_duration": avg_movie_dur,
        "max_tv_seasons": max_seasons
    }


def analyze_content_type(df):
    """
    Analyze the distribution between Movies and TV Shows.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        pd.DataFrame: Summary table with Type, Count, and Percentage
    """
    if df is None or df.empty or 'type' not in df.columns:
        return pd.DataFrame(columns=['Type', 'Count', 'Percentage'])
        
    counts = df['type'].value_counts()
    percentages = (counts / len(df)) * 100
    
    summary = pd.DataFrame({
        'Type': counts.index,
        'Count': counts.values,
        'Percentage': percentages.round(1).values
    })
    return summary


def analyze_genres(df, top_n=10, content_type='All'):
    """
    Analyze genre frequencies by splitting and exploding the comma-separated 'listed_in' column.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        top_n (int): Number of top genres to return
        content_type (str): 'All', 'Movie', or 'TV Show'
        
    Returns:
        pd.DataFrame: Table of top genres with Count and Percentage of titles
    """
    if df is None or df.empty or 'listed_in' not in df.columns:
        return pd.DataFrame(columns=['Genre', 'Count', 'Percentage'])
        
    target_df = df
    if content_type in ['Movie', 'TV Show']:
        target_df = df[df['type'].str.lower() == content_type.lower()]
        
    if target_df.empty:
        return pd.DataFrame(columns=['Genre', 'Count', 'Percentage'])
        
    # Split each comma-separated string into a list and explode into individual rows
    genre_series = target_df['listed_in'].dropna().str.split(',').explode().str.strip()
    genre_series = genre_series[genre_series != '']
    
    counts = genre_series.value_counts().head(top_n)
    total_records = len(target_df)
    
    # Percentage represents the share of catalog titles featuring this genre
    pcts = (counts / total_records) * 100
    
    result = pd.DataFrame({
        'Genre': counts.index,
        'Count': counts.values,
        'Percentage': pcts.round(1).values
    })
    return result


def analyze_countries(df, top_n=10, exclude_unknown=True):
    """
    Analyze content production by country, correctly handling co-productions
    by splitting multiple comma-separated country entries.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        top_n (int): Number of top countries to return
        exclude_unknown (bool): Whether to omit 'Unknown Country' from ranking
        
    Returns:
        pd.DataFrame: Top countries with Count and Percentage
    """
    if df is None or df.empty or 'country' not in df.columns:
        return pd.DataFrame(columns=['Country', 'Count', 'Percentage'])
        
    country_series = df['country'].dropna().str.split(',').explode().str.strip()
    country_series = country_series[country_series != '']
    
    if exclude_unknown:
        country_series = country_series[country_series != 'Unknown Country']
        
    counts = country_series.value_counts().head(top_n)
    total_count = len(country_series)
    pcts = (counts / total_count) * 100 if total_count > 0 else 0
    
    result = pd.DataFrame({
        'Country': counts.index,
        'Count': counts.values,
        'Percentage': pcts.round(1).values
    })
    return result


def analyze_release_years(df):
    """
    Analyze content releases over time.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        dict: Contains overall yearly counts, breakdown by Movie/TV, peak year, and earliest/latest years.
    """
    if df is None or df.empty or 'release_year' not in df.columns:
        return {
            "yearly_trend": pd.DataFrame(),
            "peak_year": None,
            "peak_count": 0,
            "min_year": None,
            "max_year": None
        }
        
    yearly_counts = df['release_year'].value_counts().sort_index()
    
    # Cross-tabulate release_year by type
    if 'type' in df.columns:
        crosstab = pd.crosstab(df['release_year'], df['type']).fillna(0)
    else:
        crosstab = pd.DataFrame({'Total': yearly_counts})
        
    crosstab['Total'] = yearly_counts
    yearly_df = crosstab.reset_index().rename(columns={'release_year': 'Year'})
    
    # Year-wise content growth (net increase / change)
    if not yearly_df.empty and 'Total' in yearly_df.columns:
        yearly_df['YoY_Growth'] = yearly_df['Total'].diff().fillna(0).astype(int)
    
    peak_year = int(yearly_counts.idxmax()) if not yearly_counts.empty else None
    peak_count = int(yearly_counts.max()) if not yearly_counts.empty else 0
    min_year = int(df['release_year'].min()) if not df['release_year'].empty else None
    max_year = int(df['release_year'].max()) if not df['release_year'].empty else None
    median_year = int(round(df['release_year'].median())) if not df['release_year'].empty else None
    avg_year = int(round(df['release_year'].mean())) if not df['release_year'].empty else None
    
    return {
        "yearly_trend": yearly_df,
        "peak_year": peak_year,
        "peak_count": peak_count,
        "min_year": min_year,
        "max_year": max_year,
        "median_year": median_year,
        "avg_year": avg_year
    }


def analyze_ratings(df):
    """
    Analyze rating distribution, including cross-tabulation across Movies vs TV Shows.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        pd.DataFrame: Table with Rating, Total, Movie Count, TV Show Count, and Percentage
    """
    if df is None or df.empty or 'rating' not in df.columns:
        return pd.DataFrame(columns=['Rating', 'Total', 'Movies', 'TV Shows', 'Percentage'])
        
    if 'type' in df.columns:
        crosstab = pd.crosstab(df['rating'], df['type'])
        if 'Movie' not in crosstab.columns:
            crosstab['Movie'] = 0
        if 'TV Show' not in crosstab.columns:
            crosstab['TV Show'] = 0
    else:
        counts = df['rating'].value_counts()
        crosstab = pd.DataFrame({'Total': counts, 'Movie': 0, 'TV Show': 0})
        
    crosstab['Total'] = crosstab['Movie'] + crosstab['TV Show']
    crosstab['Percentage'] = ((crosstab['Total'] / len(df)) * 100).round(1)
    
    result = crosstab.reset_index().rename(columns={
        'rating': 'Rating',
        'Movie': 'Movies',
        'TV Show': 'TV Shows'
    })
    
    return result.sort_values(by='Total', ascending=False).reset_index(drop=True)


def analyze_durations(df):
    """
    Detailed statistical analysis of Movie durations (minutes) and TV Show season counts.
    Uses Pandas and NumPy for descriptive metrics.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        dict: Detailed statistics for both Movies and TV Shows
    """
    stats = {
        "movie_stats": {},
        "tv_stats": {},
        "movie_series": pd.Series(dtype=float),
        "tv_series": pd.Series(dtype=float)
    }
    
    if df is None or df.empty:
        return stats
        
    # Movie Duration Analysis
    if 'movie_duration_min' in df.columns:
        movie_dur = df['movie_duration_min'].dropna()
        stats["movie_series"] = movie_dur
        if not movie_dur.empty:
            q25, q75 = np.percentile(movie_dur, [25, 75])
            stats["movie_stats"] = {
                "count": int(len(movie_dur)),
                "mean": round(float(np.mean(movie_dur)), 2),
                "median": round(float(np.median(movie_dur)), 2),
                "std": round(float(np.std(movie_dur, ddof=1)), 2) if len(movie_dur) > 1 else 0.0,
                "min": int(np.min(movie_dur)),
                "max": int(np.max(movie_dur)),
                "range": int(np.max(movie_dur) - np.min(movie_dur)),
                "q25": round(float(q25), 2),
                "q75": round(float(q75), 2),
                "iqr": round(float(q75 - q25), 2)
            }
            
    # TV Show Season Analysis
    if 'tv_seasons_count' in df.columns:
        tv_seasons = df['tv_seasons_count'].dropna()
        stats["tv_series"] = tv_seasons
        if not tv_seasons.empty:
            season_counts = tv_seasons.value_counts().sort_index()
            single_season_pct = round(float((season_counts.get(1, 0) / len(tv_seasons)) * 100), 1)
            stats["tv_stats"] = {
                "count": int(len(tv_seasons)),
                "mean": round(float(np.mean(tv_seasons)), 2),
                "median": round(float(np.median(tv_seasons)), 2),
                "mode": int(tv_seasons.mode().iloc[0]),
                "std": round(float(np.std(tv_seasons, ddof=1)), 2) if len(tv_seasons) > 1 else 0.0,
                "min": int(np.min(tv_seasons)),
                "max": int(np.max(tv_seasons)),
                "single_season_pct": single_season_pct,
                "multi_season_pct": round(100.0 - single_season_pct, 1),
                "season_distribution": season_counts
            }
            
    return stats


def calculate_descriptive_statistics(df):
    """
    Compute rigorous descriptive statistics using Pandas and NumPy for all valid numeric columns.
    Demonstrates GTU syllabus requirements: Count, Mean, Median, Min, Max, Std, Variance, Skewness.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        pd.DataFrame: Formatted statistical summary table
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    candidate_cols = ['release_year', 'year_added', 'movie_duration_min', 'tv_seasons_count']
    numeric_cols = [c for c in candidate_cols if c in df.columns and not df[c].dropna().empty]
    
    records = []
    col_labels = {
        'release_year': 'Release Year',
        'year_added': 'Year Added to Platform',
        'movie_duration_min': 'Movie Duration (Minutes)',
        'tv_seasons_count': 'TV Show Seasons'
    }
    
    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            continue
            
        vals = series.values
        cnt = int(len(vals))
        mean_val = float(np.mean(vals))
        median_val = float(np.median(vals))
        std_val = float(np.std(vals, ddof=1)) if cnt > 1 else 0.0
        var_val = float(np.var(vals, ddof=1)) if cnt > 1 else 0.0
        min_val = float(np.min(vals))
        max_val = float(np.max(vals))
        ptp_val = max_val - min_val
        q25, q75 = np.percentile(vals, [25, 75])
        iqr_val = q75 - q25
        skew_val = float(series.skew()) if cnt > 2 else 0.0
        
        records.append({
            'Feature': col_labels.get(col, col),
            'Count': cnt,
            'Mean': round(mean_val, 2),
            'Median': round(median_val, 2),
            'Std Dev': round(std_val, 2),
            'Variance': round(var_val, 2),
            'Min': round(min_val, 1),
            '25% (Q1)': round(q25, 1),
            '75% (Q3)': round(q75, 1),
            'Max': round(max_val, 1),
            'Range': round(ptp_val, 1),
            'IQR': round(iqr_val, 1),
            'Skewness': round(skew_val, 2)
        })
        
    return pd.DataFrame(records)


def calculate_correlation(df):
    """
    Perform Pearson correlation analysis strictly on valid continuous/discrete numeric columns.
    
    Academic Note:
    Categorical columns (Title, Director, Genre, Country, Rating) are NOT assigned arbitrary
    ordinal integers, preventing pseudoscientific spurious correlations.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        tuple: (pd.DataFrame correlation_matrix, list numeric_features_used)
    """
    if df is None or df.empty:
        return pd.DataFrame(), []
        
    valid_cols = ['release_year', 'year_added', 'movie_duration_min', 'tv_seasons_count']
    available_cols = [c for c in valid_cols if c in df.columns]
    
    # Calculate pairwise Pearson correlation with pairwise deletion of NaNs
    corr_df = df[available_cols].corr(method='pearson')
    
    friendly_names = {
        'release_year': 'Release Year',
        'year_added': 'Year Added',
        'movie_duration_min': 'Movie Dur (min)',
        'tv_seasons_count': 'TV Seasons'
    }
    
    corr_df = corr_df.rename(index=friendly_names, columns=friendly_names)
    return corr_df.round(3), list(friendly_names.values())


def filter_dataset(df, content_type='All', year_range=None, countries=None, ratings=None, genres=None, search_query=None, title_query=None):
    """
    Multi-faceted dynamic filter engine for Streamlit dashboard.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        content_type (str): 'All', 'Movie', or 'TV Show'
        year_range (tuple): (min_year, max_year)
        countries (list): Selected countries to match against
        ratings (list): Selected ratings
        genres (list): Selected genres
        search_query (str): Keyword to match in title, director, cast, or description
        title_query (str): Specific title search (case-insensitive substring match)
        
    Returns:
        pd.DataFrame: Filtered subset
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    filtered = df.copy()
    
    # 1. Content Type Filter
    if content_type and content_type != 'All':
        filtered = filtered[filtered['type'].str.lower() == content_type.lower()]
        
    # 2. Release Year Range
    if year_range and 'release_year' in filtered.columns:
        filtered = filtered[(filtered['release_year'] >= year_range[0]) & 
                            (filtered['release_year'] <= year_range[1])]
        
    # 3. Country Filter (matches if ANY selected country appears in record's list)
    if countries and len(countries) > 0 and 'country' in filtered.columns:
        pattern = '|'.join([re_escape(c) for c in countries])
        filtered = filtered[filtered['country'].str.contains(pattern, case=False, na=False)]
        
    # 4. Rating Filter
    if ratings and len(ratings) > 0 and 'rating' in filtered.columns:
        filtered = filtered[filtered['rating'].isin(ratings)]
        
    # 5. Genre Filter (matches if ANY selected genre appears in listed_in)
    if genres and len(genres) > 0 and 'listed_in' in filtered.columns:
        pattern = '|'.join([re_escape(g) for g in genres])
        filtered = filtered[filtered['listed_in'].str.contains(pattern, case=False, na=False)]
        
    # 6. Specific Title Search (case-insensitive)
    if title_query and title_query.strip() and 'title' in filtered.columns:
        t_q = title_query.strip().lower()
        filtered = filtered[filtered['title'].str.lower().str.contains(t_q, na=False)]
        
    # 7. General Keyword Search Query (Title, Director, Cast, Description)
    if search_query and search_query.strip():
        q = search_query.strip().lower()
        search_mask = (
            filtered['title'].str.lower().str.contains(q, na=False) |
            filtered['director'].str.lower().str.contains(q, na=False) |
            filtered['cast'].str.lower().str.contains(q, na=False) |
            filtered['description'].str.lower().str.contains(q, na=False)
        )
        filtered = filtered[search_mask]
        
    return filtered


def re_escape(text):
    """Safely escape special regex characters in user filter strings."""
    import re
    return re.escape(text.strip())


def generate_key_insights(df):
    """
    Generate automatic data-driven analytical takeaways and executive summary points.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        
    Returns:
        list of dict: Insights with 'title', 'value', 'badge', and 'description'
    """
    if df is None or df.empty:
        return []
        
    kpis = get_overall_kpis(df)
    genre_df = analyze_genres(df, top_n=1)
    country_df = analyze_countries(df, top_n=1)
    ratings_df = analyze_ratings(df)
    durations = analyze_durations(df)
    years = analyze_release_years(df)
    
    insights = []
    
    # 1. Catalog Composition
    dominant_type = "Movies" if kpis['pct_movies'] >= kpis['pct_tv_shows'] else "TV Shows"
    dom_pct = max(kpis['pct_movies'], kpis['pct_tv_shows'])
    insights.append({
        "title": "Catalog Dominance",
        "value": f"{dominant_type} ({dom_pct}%)",
        "badge": "Content Ratio",
        "description": f"The platform library is predominantly composed of {dominant_type.lower()}, representing {dom_pct}% of total catalog items compared to {min(kpis['pct_movies'], kpis['pct_tv_shows'])}% for the alternative format."
    })
    
    # 2. Leading Genre
    if not genre_df.empty:
        top_g = genre_df.iloc[0]['Genre']
        top_g_cnt = genre_df.iloc[0]['Count']
        top_g_pct = genre_df.iloc[0]['Percentage']
        insights.append({
            "title": "Most Prevalent Genre",
            "value": f"{top_g}",
            "badge": f"{top_g_cnt} Titles ({top_g_pct}%)",
            "description": f"'{top_g}' ranks as the single most abundant category, featured in {top_g_cnt} titles ({top_g_pct}% of the catalog), highlighting a strong curation focus on this genre."
        })
        
    # 3. Leading Production Hub
    if not country_df.empty:
        top_c = country_df.iloc[0]['Country']
        top_c_cnt = country_df.iloc[0]['Count']
        top_c_pct = country_df.iloc[0]['Percentage']
        insights.append({
            "title": "Primary Content Producer",
            "value": f"{top_c}",
            "badge": f"{top_c_cnt} Productions ({top_c_pct}%)",
            "description": f"{top_c} is the largest content contributor, accounting for {top_c_cnt} total production participations ({top_c_pct}% share of global titles)."
        })
        
    # 4. Target Audience / Rating
    if not ratings_df.empty:
        top_r = ratings_df.iloc[0]['Rating']
        top_r_cnt = ratings_df.iloc[0]['Total']
        top_r_pct = ratings_df.iloc[0]['Percentage']
        insights.append({
            "title": "Dominant Content Rating",
            "value": f"{top_r}",
            "badge": f"{top_r_pct}% Share",
            "description": f"The rating '{top_r}' is the most common across the library ({top_r_cnt} titles), demonstrating that a substantial portion of content is targeted towards mature / adult audiences."
        })
        
    # 5. Peak Release Era
    if years['peak_year']:
        insights.append({
            "title": "Peak Production Year",
            "value": f"{years['peak_year']}",
            "badge": f"{years['peak_count']} Releases",
            "description": f"The catalog features the highest density of content released in {years['peak_year']} with {years['peak_count']} titles, indicating significant acquisition of modern content."
        })
        
    # 6. Average Movie Duration
    m_stats = durations.get('movie_stats', {})
    if m_stats:
        insights.append({
            "title": "Movie Runtime Profile",
            "value": f"{m_stats['mean']} min (Median: {m_stats['median']} min)",
            "badge": f"Range: {m_stats['min']}-{m_stats['max']} min",
            "description": f"Feature films average {m_stats['mean']} minutes (standard deviation ±{m_stats['std']} min), with 50% of movies falling within the typical interquartile range of {m_stats['q25']} to {m_stats['q75']} minutes."
        })
        
    # 7. TV Show Longevity
    tv_stats = durations.get('tv_stats', {})
    if tv_stats:
        insights.append({
            "title": "TV Series Season Lifespan",
            "value": f"{tv_stats['single_season_pct']}% Single Season",
            "badge": f"Max {tv_stats['max']} Seasons",
            "description": f"Approximately {tv_stats['single_season_pct']}% of television titles conclude or currently remain at a single season, while multi-season franchises represent {tv_stats['multi_season_pct']}%."
        })
        
    # 8. Release Year Horizon
    if years['min_year'] and years['max_year']:
        span = years['max_year'] - years['min_year']
        med_y = years.get('median_year', kpis.get('avg_release_year'))
        insights.append({
            "title": "Historical Release Horizon",
            "value": f"{years['min_year']} – {years['max_year']}",
            "badge": f"{span} Year Span (Median: {med_y})",
            "description": f"The collection spans {span} years of cinematography from {years['min_year']} to {years['max_year']}, with 50% of titles distributed around or after {med_y}."
        })
        
    return insights


def generate_recommendations(df):
    """
    Generate dynamic data-based observations, practical recommendations, and an analysis summary.
    
    Academic/Data Science Note:
    All recommendations are derived from empirical dataset properties and clearly presented
    as observational analysis rather than speculative predictions.
    
    Parameters:
        df (pd.DataFrame): Cleaned or filtered DataFrame
        
    Returns:
        dict: Contains 'key_insights', 'observations', 'recommendations', and 'summary'
    """
    if df is None or df.empty:
        return {
            "key_insights": [],
            "observations": [],
            "recommendations": [],
            "summary": {
                "dataset_size": 0,
                "most_common_genre": "N/A",
                "leading_country": "N/A",
                "most_common_rating": "N/A",
                "avg_movie_duration": "0 min",
                "peak_release_year": "N/A"
            }
        }
        
    kpis = get_overall_kpis(df)
    genre_df = analyze_genres(df, top_n=5)
    country_df = analyze_countries(df, top_n=5)
    ratings_df = analyze_ratings(df)
    durations = analyze_durations(df)
    years = analyze_release_years(df)
    key_insights = generate_key_insights(df)
    
    m_stats = durations.get('movie_stats', {})
    tv_stats = durations.get('tv_stats', {})
    
    top_genre = genre_df.iloc[0]['Genre'] if not genre_df.empty else "N/A"
    top_genre_pct = genre_df.iloc[0]['Percentage'] if not genre_df.empty else 0.0
    second_genre = genre_df.iloc[1]['Genre'] if len(genre_df) > 1 else ""
    
    top_country = country_df.iloc[0]['Country'] if not country_df.empty else "N/A"
    top_country_pct = country_df.iloc[0]['Percentage'] if not country_df.empty else 0.0
    
    top_rating = ratings_df.iloc[0]['Rating'] if not ratings_df.empty else "N/A"
    top_rating_pct = ratings_df.iloc[0]['Percentage'] if not ratings_df.empty else 0.0
    
    peak_yr = years.get('peak_year', 'N/A')
    peak_cnt = years.get('peak_count', 0)
    avg_dur = f"{m_stats.get('mean', 0.0)} min" if m_stats else "N/A"
    
    # -------------------------------------------------------------------------
    # B. DATA-BASED OBSERVATIONS (Plain English Explanations)
    # -------------------------------------------------------------------------
    observations = []
    
    # Obs 1: Content Type Dominance
    if kpis['pct_movies'] >= kpis['pct_tv_shows']:
        observations.append(
            f"Based on the filtered dataset, Movies are substantially more prevalent than TV Shows, representing {kpis['pct_movies']}% of catalog titles with a movie-to-TV ratio of {kpis['movie_to_tv_ratio']}."
        )
    else:
        observations.append(
            f"Based on the filtered dataset, TV Shows represent the majority format ({kpis['pct_tv_shows']}%) over Movies ({kpis['pct_movies']}%), indicating an episodic-focused catalog selection."
        )
        
    # Obs 2: Genre Clustering
    if second_genre:
        observations.append(
            f"'{top_genre}' ({top_genre_pct}%) and '{second_genre}' are among the most frequently appearing genres, demonstrating strong viewer engagement and catalog clustering around these core themes."
        )
    else:
        observations.append(
            f"'{top_genre}' accounts for {top_genre_pct}% of total genre representations, serving as the single primary thematic pillar."
        )
        
    # Obs 3: Geographic Concentration
    observations.append(
        f"{top_country} stands as the primary production hub ({top_country_pct}% of productions), with the top 5 countries together accounting for a substantial concentration of total titles."
    )
    
    # Obs 4: Maturity Rating Target
    observations.append(
        f"The maturity rating '{top_rating}' is the most common classification ({top_rating_pct}% share), indicating that the content catalog caters significantly to teen and mature demographic segments."
    )
    
    # Obs 5: Runtime Profile
    if m_stats:
        observations.append(
            f"Feature films center around an average runtime of {m_stats.get('mean')} minutes (median {m_stats.get('median')} minutes), with 50% of films falling cleanly between {m_stats.get('q25')} and {m_stats.get('q75')} minutes."
        )
        
    # Obs 6: TV Longevity
    if tv_stats:
        observations.append(
            f"Among television titles, {tv_stats.get('single_season_pct')}% have a single season recorded, while multi-season franchises account for {tv_stats.get('multi_season_pct')}%, with the longest franchise reaching {tv_stats.get('max')} seasons."
        )
        
    # -------------------------------------------------------------------------
    # C. DATA-BASED RECOMMENDATIONS (Actionable Strategy Insights)
    # -------------------------------------------------------------------------
    recommendations = [
        {
            "category": "Content Acquisition & Portfolio Balance",
            "recommendation": f"Content providers may consider analyzing popular genres such as '{top_genre}' and '{second_genre if second_genre else top_genre}' when planning future content acquisitions to align with dominant catalog demand.",
            "rationale": f"High genre concentration ({top_genre_pct}% in '{top_genre}') confirms stable core viewer interest."
        },
        {
            "category": "Regional Diversification & Global Reach",
            "recommendation": "Country-level analysis can help identify regions with high content representation versus underrepresented geographic markets suitable for localized content expansion.",
            "rationale": f"Production remains heavily concentrated in {top_country} ({top_country_pct}%), presenting untapped potential in emerging international film hubs."
        },
        {
            "category": "Format & Franchise Longevity Strategy",
            "recommendation": "Studios and streaming platforms should evaluate the conversion rate of single-season shows into sustained multi-season franchises to improve long-term subscriber retention.",
            "rationale": f"{tv_stats.get('single_season_pct', 70)}% of television series currently conclude at season 1, whereas multi-season offerings drive extended platform loyalty."
        },
        {
            "category": "Release Timing & Content Cadence",
            "recommendation": "Release-year trends can be used to understand changes in content production velocity and optimize scheduling around peak historical acquisition periods.",
            "rationale": f"Catalog volume peaked in {peak_yr} ({peak_cnt} releases), reflecting historical licensing cycles that can guide future procurement windows."
        },
        {
            "category": "Audience Demographic Alignment",
            "recommendation": "Platforms should maintain a balanced rating mix to address both adult viewers (e.g., TV-MA / R) and family-friendly segments (PG / TV-PG / G) across diverse households.",
            "rationale": f"'{top_rating}' represents {top_rating_pct}% of the current slice, highlighting the need for intentional family-oriented counter-programming."
        }
    ]
    
    # -------------------------------------------------------------------------
    # D. ANALYSIS SUMMARY
    # -------------------------------------------------------------------------
    summary = {
        "dataset_size": f"{kpis['total_titles']:,} Titles",
        "most_common_genre": top_genre,
        "leading_country": top_country,
        "most_common_rating": top_rating,
        "avg_movie_duration": avg_dur,
        "peak_release_year": f"{peak_yr} ({peak_cnt:,} releases)" if peak_yr != 'N/A' else "N/A"
    }
    
    return {
        "key_insights": key_insights,
        "observations": observations,
        "recommendations": recommendations,
        "summary": summary
    }


def get_data_quality_summary(raw_df, cleaned_df, cleaning_metrics):
    """
    Generate structured Data Quality Audit metrics comparing Before Cleaning vs After Cleaning.
    
    Parameters:
        raw_df (pd.DataFrame): Raw DataFrame before cleaning
        cleaned_df (pd.DataFrame): Processed DataFrame after cleaning
        cleaning_metrics (dict): Cleaning metadata dictionary
        
    Returns:
        pd.DataFrame: Comparative audit table with 'Metric', 'Before Cleaning', 'After Cleaning', 'Change'
    """
    if raw_df is None or cleaned_df is None:
        return pd.DataFrame()
        
    before_rows = cleaning_metrics.get("initial_rows", len(raw_df))
    after_rows = cleaning_metrics.get("final_rows", len(cleaned_df))
    
    before_cols = cleaning_metrics.get("initial_columns", raw_df.shape[1])
    after_cols = cleaning_metrics.get("final_columns", cleaned_df.shape[1])
    
    before_missing = cleaning_metrics.get("initial_total_nulls", int(raw_df.isnull().sum().sum()))
    after_missing = cleaning_metrics.get("remaining_missing_values", int(cleaned_df.isnull().sum().sum()))
    
    duplicates_removed = cleaning_metrics.get("duplicates_removed", 0)
    
    data = [
        {
            "Metric": "Total Rows (Observations)",
            "Before Cleaning": f"{before_rows:,}",
            "After Cleaning": f"{after_rows:,}",
            "Transformation / Impact": f"-{before_rows - after_rows} rows removed (duplicates)" if before_rows > after_rows else "Retained all valid rows"
        },
        {
            "Metric": "Total Columns (Features)",
            "Before Cleaning": f"{before_cols}",
            "After Cleaning": f"{after_cols}",
            "Transformation / Impact": f"+{after_cols - before_cols} engineered features" if after_cols > before_cols else "Standardized schema"
        },
        {
            "Metric": "Missing / Null Cells",
            "Before Cleaning": f"{before_missing:,}",
            "After Cleaning": f"{after_missing:,}",
            "Transformation / Impact": f"{before_missing - after_missing:,} nulls imputed ('Unknown' / 'NR')"
        },
        {
            "Metric": "Duplicate Records",
            "Before Cleaning": f"{duplicates_removed:,} detected",
            "After Cleaning": "0 duplicates",
            "Transformation / Impact": f"{duplicates_removed:,} redundant rows pruned"
        }
    ]
    return pd.DataFrame(data)


if __name__ == "__main__":
    # Test module standalone
    from data_cleaning import load_raw_data, clean_dataset
    test_path = "p:/Experience/movie_netflix_analysis/data/netflix_titles.csv"
    raw, _, ok = load_raw_data(test_path)
    if ok:
        cleaned, _ = clean_dataset(raw)
        print("KPIs:", get_overall_kpis(cleaned))
        print("\nContent Types:")
        print(analyze_content_type(cleaned))
        print("\nTop 5 Genres:")
        print(analyze_genres(cleaned, top_n=5))
        print("\nTop 5 Countries:")
        print(analyze_countries(cleaned, top_n=5))
        print("\nDescriptive Statistics:")
        print(calculate_descriptive_statistics(cleaned))
        print("\nCorrelation Matrix:")
        corr, _ = calculate_correlation(cleaned)
        print(corr)
