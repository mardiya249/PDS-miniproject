"""
=============================================================================
MOVIE & NETFLIX DATA ANALYSIS AND VISUALIZATION DASHBOARD
=============================================================================
Subject: Python for Data Science (GTU)
Purpose: Academic Mini Project demonstrating exploratory data analysis,
         statistical computing, dynamic filtering, and interactive web visualization.
Architecture:
- Data Cleaning & Preprocessing (Student 1)
- Statistical Analysis & Filtering (Student 2)
- Visualization & Streamlit UI (Student 3)
Theme: Dynamic Dual-Theme Engine (Dark Cinematic & Sleek Light Analytics)
=============================================================================
"""

import os
import sys
import datetime
import streamlit as st
import pandas as pd
import numpy as np

# Ensure custom modules in 'modules/' can be imported directly
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, "modules")
if modules_dir not in sys.path:
    sys.path.insert(0, modules_dir)

import importlib
import data_cleaning
import analysis
import visualization

# Ensure sub-modules are always reloaded if modified
importlib.reload(data_cleaning)
importlib.reload(analysis)
importlib.reload(visualization)

# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Movie & Netflix Data Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Current date string for downloads and reports
today_date_str = datetime.date.today().strftime('%Y-%m-%d')


# =============================================================================
# 2. DATA LOADING & PREPROCESSING (CACHED)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_and_clean_data(csv_file_path):
    """
    Safely load and clean the dataset once.
    Memoized with Streamlit cache for instant dashboard responsiveness.
    """
    raw_df, msg, ok = data_cleaning.load_raw_data(csv_file_path)
    if not ok or raw_df is None:
        return None, None, {}, msg, False
    cleaned_df, metrics = data_cleaning.clean_dataset(raw_df)
    return raw_df, cleaned_df, metrics, msg, True


default_csv_path = os.path.join(current_dir, "data", "netflix_titles.csv")
raw_df, cleaned_df, cleaning_metrics, load_status, load_ok = load_and_clean_data(default_csv_path)

if not load_ok or cleaned_df is None:
    st.error(f"❌ Failed to load dataset: {load_status}")
    st.info(f"Please ensure `netflix_titles.csv` is present in `{default_csv_path}`.")
    st.stop()


# =============================================================================
# 3. SESSION STATE INITIALIZATION FOR FILTERS & APPEARANCE
# =============================================================================
min_dataset_year = int(cleaned_df['release_year'].min())
max_dataset_year = int(cleaned_df['release_year'].max())

if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"
if 'filter_content_type' not in st.session_state:
    st.session_state.filter_content_type = "All"
if 'filter_year_range' not in st.session_state:
    st.session_state.filter_year_range = (min_dataset_year, max_dataset_year)
if 'filter_countries' not in st.session_state:
    st.session_state.filter_countries = []
if 'filter_ratings' not in st.session_state:
    st.session_state.filter_ratings = []
if 'filter_genres' not in st.session_state:
    st.session_state.filter_genres = []
if 'filter_title_search' not in st.session_state:
    st.session_state.filter_title_search = ""


# =============================================================================
# 4. DYNAMIC THEME CSS INJECTION (DARK & LIGHT THEMES)
# =============================================================================
theme_name = st.session_state.theme
is_dark = theme_name == "Dark"

theme_tokens = visualization.get_theme_tokens(theme_name)

if is_dark:
    # DARK THEME: Background: #0F1117 | Card: #181B24 | Primary: #E50914 | Secondary: #00B8D9 | Text: #FFFFFF | Muted: #A7A7A7
    theme_css = """
    <style>
        .stApp {
            background-color: #0F1117;
            color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 100%;
        }
        [data-testid="stSidebar"] {
            background-color: #12141D;
            border-right: 1px solid #232736;
        }
        [data-testid="stSidebar"] hr {
            border-color: #282D3D;
            margin: 0.9rem 0;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #FFFFFF !important;
            font-weight: 500;
        }
        [data-testid="stSidebar"] label {
            color: #E2E8F0 !important;
            font-weight: 600;
        }
        header[data-testid="stHeader"] {
            background-color: #0F1117;
        }
        .dashboard-hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #FFFFFF;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }
        .dashboard-hero-title span {
            color: #E50914;
        }
        .dashboard-subtitle {
            color: #A7A7A7;
            font-size: 1.05rem;
            font-weight: 400;
            margin-bottom: 1.5rem;
        }
        [data-testid="stMetric"] {
            background-color: #181B24;
            border: 1px solid #282D3D;
            border-left: 4px solid #E50914;
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        [data-testid="stMetricLabel"] {
            color: #A7A7A7 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }
        .content-card {
            background-color: #181B24;
            border: 1px solid #282D3D;
            border-radius: 10px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
            color: #FFFFFF;
        }
        .content-card-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .insight-card {
            background-color: #181B24;
            border: 1px solid #282D3D;
            border-left: 4px solid #E50914;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.9rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .insight-card:hover {
            transform: translateY(-2px);
            border-color: #3B4256;
        }
        .insight-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.3rem;
        }
        .insight-label {
            font-weight: 700;
            font-size: 0.92rem;
            color: #FFFFFF;
        }
        .insight-badge {
            background-color: rgba(229, 9, 20, 0.18);
            color: #FF6B6B;
            border: 1px solid rgba(229, 9, 20, 0.35);
            padding: 0.15rem 0.55rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .insight-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.25rem;
        }
        .insight-text {
            font-size: 0.88rem;
            color: #A7A7A7;
            line-height: 1.45;
        }
        [data-testid="stDataFrame"] {
            background-color: #181B24;
            border: 1px solid #282D3D;
            border-radius: 8px;
        }
        div.stButton > button {
            background-color: #E50914 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.2rem !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #B80710 !important;
            box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4) !important;
        }
        div.stDownloadButton > button {
            background-color: #E50914 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.2rem !important;
            font-weight: 600 !important;
        }
        div.stDownloadButton > button:hover {
            background-color: #B80710 !important;
        }
        .page-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.25rem;
        }
        .page-subtitle {
            color: #A7A7A7;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
        .section-divider {
            border-top: 1px solid #282D3D;
            margin: 1.5rem 0;
        }
        .filter-counter-badge {
            background-color: #181B24;
            border: 1px solid #282D3D;
            padding: 0.5rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #00B8D9;
            text-align: center;
            margin: 0.5rem 0;
        }
    </style>
    """
else:
    # LIGHT THEME: Background: #F5F7FA | Card: #FFFFFF | Primary: #D90429 | Secondary: #0077B6 | Text: #1F2937 | Muted: #6B7280
    theme_css = """
    <style>
        .stApp {
            background-color: #F5F7FA;
            color: #1F2937;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 100%;
        }
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E7EB;
        }
        [data-testid="stSidebar"] hr {
            border-color: #E5E7EB;
            margin: 0.9rem 0;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #1F2937 !important;
            font-weight: 500;
        }
        [data-testid="stSidebar"] label {
            color: #1F2937 !important;
            font-weight: 600;
        }
        header[data-testid="stHeader"] {
            background-color: #F5F7FA;
        }
        .dashboard-hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #1F2937;
            line-height: 1.15;
            margin-bottom: 0.35rem;
        }
        .dashboard-hero-title span {
            color: #D90429;
        }
        .dashboard-subtitle {
            color: #6B7280;
            font-size: 1.05rem;
            font-weight: 400;
            margin-bottom: 1.5rem;
        }
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-left: 4px solid #D90429;
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        [data-testid="stMetricLabel"] {
            color: #6B7280 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        [data-testid="stMetricValue"] {
            color: #1F2937 !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }
        .content-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            color: #1F2937;
        }
        .content-card-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .insight-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-left: 4px solid #D90429;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: transform 0.15s ease, border-color 0.15s ease;
        }
        .insight-card:hover {
            transform: translateY(-2px);
            border-color: #D1D5DB;
        }
        .insight-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.3rem;
        }
        .insight-label {
            font-weight: 700;
            font-size: 0.92rem;
            color: #1F2937;
        }
        .insight-badge {
            background-color: rgba(217, 4, 41, 0.12);
            color: #D90429;
            border: 1px solid rgba(217, 4, 41, 0.3);
            padding: 0.15rem 0.55rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .insight-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 0.25rem;
        }
        .insight-text {
            font-size: 0.88rem;
            color: #6B7280;
            line-height: 1.45;
        }
        [data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        }
        div.stButton > button {
            background-color: #D90429 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.2rem !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #B20322 !important;
            box-shadow: 0 4px 12px rgba(217, 4, 41, 0.3) !important;
        }
        div.stDownloadButton > button {
            background-color: #D90429 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.2rem !important;
            font-weight: 600 !important;
        }
        div.stDownloadButton > button:hover {
            background-color: #B20322 !important;
        }
        .page-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 0.25rem;
        }
        .page-subtitle {
            color: #6B7280;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
        .section-divider {
            border-top: 1px solid #E5E7EB;
            margin: 1.5rem 0;
        }
        .filter-counter-badge {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            padding: 0.5rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #0077B6;
            text-align: center;
            margin: 0.5rem 0;
        }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)


# =============================================================================
# 5. SIDEBAR STRUCTURE: NAVIGATION, GLOBAL FILTERS, APPEARANCE, RESET
# =============================================================================
st.sidebar.markdown("## 🎬 Movie Analytics")
st.sidebar.caption("Python for Data Science | Academic Mini Project")

# Navigation Menu (includes all existing pages + new Insights & Recommendations)
nav_selection = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎭 Genre Analysis",
        "🌍 Country Analysis",
        "📅 Release Analysis",
        "⭐ Rating Analysis",
        "⏱️ Duration Analysis",
        "🔎 Explore Data",
        "💡 Insights & Recommendations",
        "ℹ️ About Project"
    ],
    index=0
)

st.sidebar.divider()

# -----------------------------------------------------------------------------
# GLOBAL FILTERS SECTION
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🔍 GLOBAL FILTERS")

# Filter 1: Content Type
type_options = ["All", "Movie", "TV Show"]
filter_type = st.sidebar.selectbox(
    "Content Type",
    type_options,
    key="filter_content_type"
)

# Filter 2: Release Year Slider
filter_year_range = st.sidebar.slider(
    "Release Year",
    min_value=min_dataset_year,
    max_value=max_dataset_year,
    step=1,
    key="filter_year_range"
)

# Filter 3: Country (Multi-select)
all_countries_clean = set()
for c_item in cleaned_df['country'].dropna():
    for c in str(c_item).split(','):
        c_clean = c.strip()
        if c_clean and c_clean != 'Unknown Country':
            all_countries_clean.add(c_clean)
country_options = sorted(list(all_countries_clean))

filter_countries = st.sidebar.multiselect(
    "Country",
    country_options,
    placeholder="All countries",
    key="filter_countries"
)

# Filter 4: Genre (Multi-select)
all_genres_clean = set()
for g_item in cleaned_df['listed_in'].dropna():
    for g in str(g_item).split(','):
        g_clean = g.strip()
        if g_clean:
            all_genres_clean.add(g_clean)
genre_options = sorted(list(all_genres_clean))

filter_genres = st.sidebar.multiselect(
    "Genre",
    genre_options,
    placeholder="All genres",
    key="filter_genres"
)

# Filter 5: Rating (Multi-select)
rating_options = sorted(list(cleaned_df['rating'].dropna().unique()))
filter_ratings = st.sidebar.multiselect(
    "Rating",
    rating_options,
    placeholder="All ratings",
    key="filter_ratings"
)

# Filter 6: Movie/Show Title Search (case-insensitive substring match)
filter_title_search = st.sidebar.text_input(
    "Title Search",
    placeholder="Search by title...",
    key="filter_title_search"
)

# Apply dynamic multi-criteria filtering
filtered_df = analysis.filter_dataset(
    cleaned_df,
    content_type=filter_type,
    year_range=filter_year_range,
    countries=filter_countries,
    ratings=filter_ratings,
    genres=filter_genres,
    title_query=filter_title_search
)

# Filtered records counter display in sidebar
total_records_count = len(cleaned_df)
matched_records_count = len(filtered_df)

st.sidebar.markdown(f"""
<div class="filter-counter-badge">
    FILTERED RESULTS: {matched_records_count:,} TITLES<br>
    <span style="font-size: 0.75rem; color: {'#A7A7A7' if is_dark else '#6B7280'};">({matched_records_count / total_records_count * 100:.1f}% of {total_records_count:,} total)</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# -----------------------------------------------------------------------------
# APPEARANCE SECTION: THEME TOGGLE (DARK / LIGHT)
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🎨 APPEARANCE")
theme_choice = st.sidebar.radio(
    "Theme Selector",
    ["Dark", "Light"],
    index=0 if st.session_state.theme == "Dark" else 1,
    horizontal=True,
    label_visibility="collapsed"
)

if theme_choice != st.session_state.theme:
    st.session_state.theme = theme_choice
    st.rerun()

st.sidebar.divider()

# -----------------------------------------------------------------------------
# RESET FILTERS BUTTON (VIA PRE-RUN CALLBACK)
# -----------------------------------------------------------------------------
def reset_filters_callback():
    st.session_state.filter_content_type = "All"
    st.session_state.filter_year_range = (min_dataset_year, max_dataset_year)
    st.session_state.filter_countries = []
    st.session_state.filter_ratings = []
    st.session_state.filter_genres = []
    st.session_state.filter_title_search = ""

st.sidebar.button("🔄 Reset Filters", on_click=reset_filters_callback, use_container_width=True)


# =============================================================================
# VIEW 1: DASHBOARD (MAIN DASHBOARD)
# =============================================================================
if nav_selection == "🏠 Dashboard":
    # Hero Title Header
    st.markdown("""
    <div class="dashboard-hero-title">
        Movie & Netflix<br><span>Data Analysis Dashboard</span>
    </div>
    <div class="dashboard-subtitle">
        Interactive Data Science Exploratory Analysis & Visualization
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate KPIs dynamically from filtered dataset
    kpis = analysis.get_overall_kpis(filtered_df)
    
    # -------------------------------------------------------------------------
    # TOP KPI CARDS ROW (5 METRICS)
    # -------------------------------------------------------------------------
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    with kpi_col1:
        st.metric(label="TOTAL TITLES", value=f"{kpis['total_titles']:,}")
    with kpi_col2:
        st.metric(label="TOTAL MOVIES", value=f"{kpis['total_movies']:,}", delta=f"{kpis['pct_movies']}% share")
    with kpi_col3:
        st.metric(label="TOTAL TV SHOWS", value=f"{kpis['total_tv_shows']:,}", delta=f"{kpis['pct_tv_shows']}% share")
    with kpi_col4:
        st.metric(label="COUNTRIES", value=f"{kpis['total_countries']}")
    with kpi_col5:
        st.metric(label="AVERAGE RELEASE YEAR", value=f"{kpis['avg_release_year']}")
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Check if records matched
    if matched_records_count == 0:
        st.warning("⚠️ No titles match the selected filters. Please adjust your criteria or click 'Reset Filters' in the sidebar.")
    else:
        # ---------------------------------------------------------------------
        # ROW 1 CHARTS: Movies vs TV Shows & Top 10 Genres
        # ---------------------------------------------------------------------
        row1_left, row1_right = st.columns(2)
        with row1_left:
            st.markdown("#### 🎬 Movies vs TV Shows")
            fig_donut = visualization.plot_type_donut(filtered_df, theme=theme_name)
            st.pyplot(fig_donut)
        with row1_right:
            st.markdown("#### 🎭 Top 10 Genres")
            genre_data = analysis.analyze_genres(filtered_df, top_n=10)
            fig_genres = visualization.plot_top_genres(genre_data, top_n=10, theme=theme_name)
            st.pyplot(fig_genres)
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # ROW 2 CHARTS: Content Released by Year & Top 10 Countries
        # ---------------------------------------------------------------------
        row2_left, row2_right = st.columns(2)
        with row2_left:
            st.markdown("#### 📅 Content Released by Year")
            year_data = analysis.analyze_release_years(filtered_df)
            fig_timeline = visualization.plot_release_trend(year_data, theme=theme_name)
            st.pyplot(fig_timeline)
        with row2_right:
            st.markdown("#### 🌍 Top 10 Countries")
            country_data = analysis.analyze_countries(filtered_df, top_n=10)
            fig_countries = visualization.plot_top_countries(country_data, top_n=10, theme=theme_name)
            st.pyplot(fig_countries)
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # ROW 3 CHARTS: Rating Distribution & Movie Duration Distribution
        # ---------------------------------------------------------------------
        row3_left, row3_right = st.columns(2)
        with row3_left:
            st.markdown("#### ⭐ Rating Distribution")
            ratings_df = analysis.analyze_ratings(filtered_df)
            fig_ratings = visualization.plot_rating_distribution(ratings_df, theme=theme_name)
            st.pyplot(fig_ratings)
        with row3_right:
            st.markdown("#### ⏱️ Movie Duration Distribution")
            duration_data = analysis.analyze_durations(filtered_df)
            fig_duration = visualization.plot_movie_duration_dist(
                duration_data["movie_series"],
                duration_data["movie_stats"],
                theme=theme_name
            )
            st.pyplot(fig_duration)
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # ROW 4: FEATURED TITLES & POSTER GALLERY
        # ---------------------------------------------------------------------
        st.markdown("### 🎬 Featured Titles")
        st.caption("Inspect individual movie or TV show title details with cinema poster presentation.")
        
        # Title Selection / Search within current filtered records
        title_options = filtered_df['title'].dropna().tolist()
        if title_options:
            selected_title = st.selectbox(
                "Select a Title to Inspect:",
                title_options,
                index=0,
                key="featured_title_selector"
            )
            
            selected_row = filtered_df[filtered_df['title'] == selected_title].iloc[0]
            
            # 2-Column Inspector: Left = Poster Card, Right = Detailed Metadata Card
            p_col_left, p_col_right = st.columns([1, 2.2])
            
            with p_col_left:
                poster_card_markup = visualization.render_poster_card(selected_row, theme=theme_name)
                st.markdown(poster_card_markup, unsafe_allow_html=True)
                
            with p_col_right:
                st.markdown(f"""
                <div class="content-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                        <div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: {theme_tokens['text']}; line-height: 1.2;">
                                {selected_row.get('title', 'N/A')}
                            </div>
                            <div style="color: {theme_tokens['text_muted']}; font-size: 0.95rem; margin-top: 0.2rem;">
                                Directed by: <strong style="color: {theme_tokens['text']};">{selected_row.get('director', 'Unknown')}</strong>
                            </div>
                        </div>
                        <span class="insight-badge">{selected_row.get('type', 'Movie')}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin: 1rem 0; padding: 0.8rem; background-color: {'#12141D' if is_dark else '#F8FAFC'}; border-radius: 8px;">
                        <div>
                            <span style="font-size: 0.75rem; text-transform: uppercase; color: {theme_tokens['text_muted']}; font-weight: 700;">Release Year</span><br>
                            <strong style="color: {theme_tokens['text']}; font-size: 1.1rem;">{selected_row.get('release_year', 'N/A')}</strong>
                        </div>
                        <div>
                            <span style="font-size: 0.75rem; text-transform: uppercase; color: {theme_tokens['text_muted']}; font-weight: 700;">Maturity Rating</span><br>
                            <strong style="color: {theme_tokens['text']}; font-size: 1.1rem;">{selected_row.get('rating', 'NR')}</strong>
                        </div>
                        <div>
                            <span style="font-size: 0.75rem; text-transform: uppercase; color: {theme_tokens['text_muted']}; font-weight: 700;">Runtime / Seasons</span><br>
                            <strong style="color: {theme_tokens['text']}; font-size: 1.1rem;">{selected_row.get('duration', 'N/A')}</strong>
                        </div>
                    </div>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: {theme_tokens['text_muted']};">
                        <strong>Genre:</strong> {selected_row.get('listed_in', 'N/A')}
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: {theme_tokens['text_muted']};">
                        <strong>Production Countries:</strong> {selected_row.get('country', 'Unknown Country')}
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: {theme_tokens['text_muted']};">
                        <strong>Cast:</strong> {selected_row.get('cast', 'Unknown Cast')}
                    </p>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid {theme_tokens['grid']};">
                        <strong style="color: {theme_tokens['text']};">Synopsis:</strong>
                        <p style="margin-top: 0.3rem; font-size: 0.92rem; color: {theme_tokens['text_muted']}; line-height: 1.5;">
                            {selected_row.get('description', 'No synopsis available.')}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Featured Titles Showcase Row (3 to 4 sample cards)
            sample_count = min(4, len(filtered_df))
            if sample_count >= 2:
                st.markdown("##### 🌟 More Featured Highlights from Current Selection")
                sample_titles_df = filtered_df.drop_duplicates(subset=['title']).head(sample_count)
                f_cols = st.columns(sample_count)
                for idx, (_, item_row) in enumerate(sample_titles_df.iterrows()):
                    with f_cols[idx]:
                        card_code = visualization.render_poster_card(item_row, theme=theme_name)
                        st.markdown(card_code, unsafe_allow_html=True)
                        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # ROW 5: QUICK INSIGHTS (3 SHORT DYNAMICALLY GENERATED INSIGHTS)
        # ---------------------------------------------------------------------
        st.markdown("### 💡 Quick Insights")
        st.caption("Key empirical takeaways computed from the active filter selection.")
        
        all_insights = analysis.generate_key_insights(filtered_df)
        if all_insights:
            q_cols = st.columns(3)
            for i, ins in enumerate(all_insights[:3]):
                with q_cols[i % 3]:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-header">
                            <span class="insight-label">{ins['title']}</span>
                            <span class="insight-badge">{ins['badge']}</span>
                        </div>
                        <div class="insight-value">{ins['value']}</div>
                        <div class="insight-text">{ins['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)


# =============================================================================
# VIEW 2: GENRE ANALYSIS
# =============================================================================
elif nav_selection == "🎭 Genre Analysis":
    st.markdown('<div class="page-title">🎭 Genre Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Exploration of catalog genres with comma-separated tag decomposition</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters.")
    else:
        # Calculate genre metrics
        genre_series = filtered_df['listed_in'].dropna().str.split(',').explode().str.strip()
        genre_series = genre_series[genre_series != '']
        
        total_unique_genres = int(genre_series.nunique()) if not genre_series.empty else 0
        most_common_genre = genre_series.mode().iloc[0] if not genre_series.empty else "N/A"
        
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.metric("Total Unique Genres", total_unique_genres)
        with mcol2:
            st.metric("Most Common Genre", most_common_genre)
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        genre_table = analysis.analyze_genres(filtered_df, top_n=10)
        
        col_chart, col_table = st.columns([1.3, 1])
        with col_chart:
            st.markdown("#### Genre Distribution (Top 10)")
            fig_g = visualization.plot_top_genres(genre_table, top_n=10, theme=theme_name)
            st.pyplot(fig_g)
        with col_table:
            st.markdown("#### Genre Statistics Table")
            st.dataframe(genre_table, use_container_width=True)


# =============================================================================
# VIEW 3: COUNTRY ANALYSIS
# =============================================================================
elif nav_selection == "🌍 Country Analysis":
    st.markdown('<div class="page-title">🌍 Country Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Geographic distribution and co-production country attribution</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters.")
    else:
        country_series = filtered_df['country'].dropna().str.split(',').explode().str.strip()
        country_series = country_series[(country_series != '') & (country_series != 'Unknown Country')]
        
        num_countries = int(country_series.nunique()) if not country_series.empty else 0
        top_country = country_series.mode().iloc[0] if not country_series.empty else "N/A"
        
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.metric("Total Unique Countries", num_countries)
        with mcol2:
            st.metric("Leading Production Country", top_country)
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        country_table = analysis.analyze_countries(filtered_df, top_n=10)
        
        col_c_chart, col_c_table = st.columns([1.3, 1])
        with col_c_chart:
            st.markdown("#### Top 10 Countries Content Distribution")
            fig_c = visualization.plot_top_countries(country_table, top_n=10, theme=theme_name)
            st.pyplot(fig_c)
        with col_c_table:
            st.markdown("#### Country Statistics Table")
            st.dataframe(country_table, use_container_width=True)


# =============================================================================
# VIEW 4: RELEASE ANALYSIS
# =============================================================================
elif nav_selection == "📅 Release Analysis":
    st.markdown('<div class="page-title">📅 Release Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Temporal content distribution, release surges, and historical timelines</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters.")
    else:
        year_summary = analysis.analyze_release_years(filtered_df)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Minimum Release Year", year_summary.get('min_year', 'N/A'))
        with m2:
            st.metric("Maximum Release Year", year_summary.get('max_year', 'N/A'))
        with m3:
            st.metric("Average Release Year", year_summary.get('avg_year', 'N/A'))
        with m4:
            st.metric("Peak Release Year", f"{year_summary.get('peak_year', 'N/A')}", f"{year_summary.get('peak_count', 0)} titles")
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        col_line, col_bar = st.columns(2)
        with col_line:
            st.markdown("##### Temporal Trend (Line Chart)")
            fig_r_line = visualization.plot_release_trend(year_summary, theme=theme_name)
            st.pyplot(fig_r_line)
        with col_bar:
            st.markdown("##### Yearly Volume (Bar Chart)")
            fig_r_bar = visualization.plot_release_bar(year_summary, theme=theme_name)
            st.pyplot(fig_r_bar)
            
        st.markdown("#### Yearly Growth Table")
        st.dataframe(year_summary.get('yearly_trend', pd.DataFrame()), use_container_width=True)


# =============================================================================
# VIEW 5: RATING ANALYSIS
# =============================================================================
elif nav_selection == "⭐ Rating Analysis":
    st.markdown('<div class="page-title">⭐ Rating Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Maturity rating codes and target audience classification</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters.")
    else:
        ratings_table = analysis.analyze_ratings(filtered_df)
        most_common_rating = ratings_table.iloc[0]['Rating'] if not ratings_table.empty else "N/A"
        most_common_cnt = int(ratings_table.iloc[0]['Total']) if not ratings_table.empty else 0
        most_common_pct = float(ratings_table.iloc[0]['Percentage']) if not ratings_table.empty else 0.0
        
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Most Common Rating", most_common_rating, f"{most_common_cnt:,} titles")
        with r2:
            st.metric("Dominant Rating Share", f"{most_common_pct}%")
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("#### Rating Distribution Chart")
        fig_rate = visualization.plot_rating_distribution(ratings_table, theme=theme_name)
        st.pyplot(fig_rate)
        
        st.markdown("#### Rating-Wise Content Count Table")
        st.dataframe(ratings_table, use_container_width=True)


# =============================================================================
# VIEW 6: DURATION ANALYSIS
# =============================================================================
elif nav_selection == "⏱️ Duration Analysis":
    st.markdown('<div class="page-title">⏱️ Duration Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Feature film runtime distribution and television series season longevity</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters.")
    else:
        duration_data = analysis.analyze_durations(filtered_df)
        m_stats = duration_data.get("movie_stats", {})
        tv_stats = duration_data.get("tv_stats", {})
        
        # 1. Movie Duration Statistics
        st.markdown("### 🎥 Movie Runtime Analytics")
        if m_stats:
            dcol1, dcol2, dcol3, dcol4 = st.columns(4)
            with dcol1:
                st.metric("Average Movie Duration", f"{m_stats['mean']} min")
            with dcol2:
                st.metric("Median Duration", f"{m_stats['median']} min")
            with dcol3:
                st.metric("Duration Range", f"{m_stats['min']} - {m_stats['max']} min")
            with dcol4:
                st.metric("Standard Deviation", f"±{m_stats['std']} min")
                
            fig_dur_hist = visualization.plot_movie_duration_dist(duration_data["movie_series"], m_stats, theme=theme_name)
            st.pyplot(fig_dur_hist)
        else:
            st.info("No movie duration records available in the filtered dataset.")
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # 2. TV Show Seasons Statistics
        st.markdown("### 📺 TV Show Seasons Analytics")
        if tv_stats:
            tvcol1, tvcol2, tvcol3, tvcol4 = st.columns(4)
            with tvcol1:
                st.metric("Single Season Shows", f"{tv_stats['single_season_pct']}%")
            with tvcol2:
                st.metric("Multi-Season Shows", f"{tv_stats['multi_season_pct']}%")
            with tvcol3:
                st.metric("Maximum Seasons", f"{tv_stats['max']} Seasons")
            with tvcol4:
                st.metric("Most Common Seasons", f"{tv_stats.get('mode', 1)} Season(s)")
                
            fig_tv = visualization.plot_tv_seasons_dist(duration_data["tv_series"], tv_stats, theme=theme_name)
            st.pyplot(fig_tv)
        else:
            st.info("No TV show season records available in the filtered dataset.")
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # 3. Descriptive Statistics Table
        st.markdown("### 📊 Descriptive Statistics (Pandas & NumPy)")
        st.caption("Empirical summary statistics computed strictly on meaningful continuous/discrete numerical features.")
        desc_df = analysis.calculate_descriptive_statistics(filtered_df)
        st.dataframe(desc_df, use_container_width=True)


# =============================================================================
# VIEW 7: EXPLORE DATA (WITH IMPROVED CSV DOWNLOADS & COLUMN SELECTOR)
# =============================================================================
elif nav_selection == "🔎 Explore Data":
    st.markdown('<div class="page-title">🔎 Explore Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Interactive search, filtering, schema inspection, and CSV dataset export</div>', unsafe_allow_html=True)
    
    # In-page title search input
    search_keyword = st.text_input(
        "Search Catalog (Title, Director, Cast, or Description):",
        placeholder="e.g. Inception, Leonardo DiCaprio, Nolan, Dark...",
        key="explore_page_search"
    )
    
    if search_keyword.strip():
        q = search_keyword.strip().lower()
        search_mask = (
            filtered_df['title'].str.lower().str.contains(q, na=False) |
            filtered_df['director'].str.lower().str.contains(q, na=False) |
            filtered_df['cast'].str.lower().str.contains(q, na=False) |
            filtered_df['description'].str.lower().str.contains(q, na=False)
        )
        display_df = filtered_df[search_mask]
    else:
        display_df = filtered_df
        
    # Metrics Bar
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Total Filtered Records", f"{len(display_df):,}")
    with col_info2:
        st.metric("Total Columns Available", f"{len(display_df.columns)}")
    with col_info3:
        st.metric("Platform Catalog Share", f"{len(display_df) / len(cleaned_df) * 100:.1f}%")
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Download Action Buttons
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        filtered_csv_bytes = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset (CSV)",
            data=filtered_csv_bytes,
            file_name=f"movie_analysis_filtered_{today_date_str}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption(f"Includes only currently filtered records ({len(display_df):,} rows).")
        
    with d_col2:
        cleaned_csv_bytes = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete Cleaned Dataset (CSV)",
            data=cleaned_csv_bytes,
            file_name=f"movie_analysis_cleaned_{today_date_str}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption(f"Includes entire preprocessed dataset ({len(cleaned_df):,} rows).")
        
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Column Selector for Custom View
    all_cols = list(display_df.columns)
    default_cols = ['show_id', 'type', 'title', 'director', 'release_year', 'rating', 'duration', 'listed_in', 'country']
    default_selected = [c for c in default_cols if c in all_cols]
    
    selected_cols = st.multiselect(
        "Select Columns to Display in Table:",
        all_cols,
        default=default_selected,
        key="explore_col_selector"
    )
    
    if selected_cols:
        view_table = display_df[selected_cols]
    else:
        view_table = display_df
        
    st.dataframe(view_table, use_container_width=True, height=480)
    
    # Data Quality Section on Explore Data Page
    with st.expander("📋 Data Quality & Ingestion Audit (Before vs After Cleaning)", expanded=False):
        dq_table = analysis.get_data_quality_summary(raw_df, cleaned_df, cleaning_metrics)
        st.dataframe(dq_table, use_container_width=True)


# =============================================================================
# VIEW 8: INSIGHTS & RECOMMENDATIONS (NEW PAGE)
# =============================================================================
elif nav_selection == "💡 Insights & Recommendations":
    st.markdown('<div class="page-title">💡 Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Dynamic data science observations, empirical takeaways, and strategic recommendations</div>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("⚠️ No titles match the selected filters. Please adjust your criteria to compute insights.")
    else:
        rec_data = analysis.generate_recommendations(filtered_df)
        
        # ---------------------------------------------------------------------
        # D. ANALYSIS SUMMARY
        # ---------------------------------------------------------------------
        st.markdown("### 📊 Analysis Summary")
        summary_dict = rec_data.get("summary", {})
        
        s1, s2, s3, s4, s5, s6 = st.columns(6)
        with s1:
            st.metric("Dataset Size", summary_dict.get("dataset_size", "0"))
        with s2:
            st.metric("Most Common Genre", summary_dict.get("most_common_genre", "N/A"))
        with s3:
            st.metric("Leading Country", summary_dict.get("leading_country", "N/A"))
        with s4:
            st.metric("Most Common Rating", summary_dict.get("most_common_rating", "N/A"))
        with s5:
            st.metric("Avg Movie Duration", summary_dict.get("avg_movie_duration", "N/A"))
        with s6:
            st.metric("Peak Release Year", summary_dict.get("peak_release_year", "N/A"))
            
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # A. KEY INSIGHTS (6-8 DYNAMIC INSIGHT CARDS)
        # ---------------------------------------------------------------------
        st.markdown("### 🔍 Key Insights")
        st.caption("Empirical findings calculated directly from the active dataset subset.")
        
        key_insights = rec_data.get("key_insights", [])
        if key_insights:
            k_cols = st.columns(3)
            for i, ins in enumerate(key_insights):
                with k_cols[i % 3]:
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-header">
                            <span class="insight-label">{ins['title']}</span>
                            <span class="insight-badge">{ins['badge']}</span>
                        </div>
                        <div class="insight-value">{ins['value']}</div>
                        <div class="insight-text">{ins['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # B. DATA-BASED OBSERVATIONS (PLAIN ENGLISH)
        # ---------------------------------------------------------------------
        st.markdown("### 📝 Data-Based Observations")
        st.caption("Statistical patterns explained in plain, accessible language.")
        
        observations = rec_data.get("observations", [])
        obs_col1, obs_col2 = st.columns(2)
        for idx, obs in enumerate(observations):
            target_col = obs_col1 if idx % 2 == 0 else obs_col2
            with target_col:
                st.markdown(f"""
                <div class="content-card">
                    <p style="margin: 0; line-height: 1.6; font-size: 0.95rem; color: {theme_tokens['text']};">
                        <strong>Observation {idx + 1}:</strong> {obs}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ---------------------------------------------------------------------
        # C. STRATEGIC RECOMMENDATIONS
        # ---------------------------------------------------------------------
        st.markdown("### 🎯 Data-Informed Recommendations")
        st.caption("Actionable recommendations presented strictly as data-analysis observations and portfolio strategy guidance.")
        
        recommendations = rec_data.get("recommendations", [])
        for rec in recommendations:
            st.markdown(f"""
            <div class="content-card" style="border-left: 4px solid {theme_tokens['secondary']};">
                <div class="content-card-title">💡 {rec['category']}</div>
                <p style="font-size: 0.96rem; font-weight: 500; color: {theme_tokens['text']}; margin-bottom: 0.4rem;">
                    {rec['recommendation']}
                </p>
                <div style="font-size: 0.85rem; color: {theme_tokens['text_muted']};">
                    <strong>Analytical Rationale:</strong> {rec['rationale']}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# VIEW 9: ABOUT PROJECT
# =============================================================================
elif nav_selection == "ℹ️ About Project":
    st.markdown('<div class="page-title">ℹ️ About Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Academic Project Overview, Syllabus Mapping, and Team Information</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="content-card">
        <div class="content-card-title">📌 Project Information</div>
        <p><strong>Project Title:</strong> Movie & Netflix Data Analysis and Visualization Dashboard</p>
        <p><strong>Subject:</strong> Python for Data Science</p>
        <p><strong>Objective:</strong> To analyze entertainment catalog data using Python data science libraries (Pandas, NumPy, Matplotlib, Seaborn, Streamlit) and communicate analytical insights through responsive, dual-themed visualizations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_tech, col_concepts = st.columns(2)
    
    with col_tech:
        st.markdown(f"""
        <div class="content-card">
            <div class="content-card-title">🛠️ Technologies & Stack</div>
            <ul style="color: {theme_tokens['text_muted']}; line-height: 1.8; margin-bottom: 0;">
                <li><strong>Python</strong> (Core programming & scripting)</li>
                <li><strong>Pandas</strong> (Data cleaning, transformation & tabular manipulation)</li>
                <li><strong>NumPy</strong> (Descriptive statistical computing & array ops)</li>
                <li><strong>Matplotlib</strong> (Custom dual-theme figure rendering)</li>
                <li><strong>Seaborn</strong> (Statistical plotting & gradient palettes)</li>
                <li><strong>Streamlit</strong> (Interactive reactive web application framework)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_concepts:
        st.markdown(f"""
        <div class="content-card">
            <div class="content-card-title">📚 Concepts Demonstrated</div>
            <ul style="color: {theme_tokens['text_muted']}; line-height: 1.8; margin-bottom: 0;">
                <li>Data Ingestion & CSV Parsing</li>
                <li>Missing Value Handling & Duplicate Pruning</li>
                <li>Feature Engineering (durations, date features)</li>
                <li>Multi-Dimensional Filtering Engine</li>
                <li>Descriptive Statistics (Mean, Median, Std, IQR)</li>
                <li>Responsive Dual-Theme Design (Dark & Light)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
    <div class="content-card">
        <div class="content-card-title">📋 Data Ingestion & Quality Audit (Before vs After Cleaning)</div>
        <p style="font-size: 0.9rem; color: {theme_tokens['text_muted']};">
            Comparison of raw input records versus analysis-ready preprocessed data:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    dq_table = analysis.get_data_quality_summary(raw_df, cleaned_df, cleaning_metrics)
    st.dataframe(dq_table, use_container_width=True)
    
    st.markdown(f"""
    <div class="content-card">
        <div class="content-card-title">👥 Group Members & Responsibilities</div>
        <ul style="color: {theme_tokens['text_muted']}; line-height: 2; margin-bottom: 0;">
            <li><strong>Student 1:</strong> [Mardiya Prashant] — <em>Data Loading, Cleaning & Preprocessing (Pandas/NumPy)</em></li>
            <li><strong>Student 2:</strong> [Vasoya Krisha] — <em>Statistical Analysis, Aggregation & Dynamic Filtering</em></li>
            <li><strong>Student 3:</strong> [Student 3] — <em>Streamlit UI Architecture, Visualizations & Presentation</em></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="section-divider"></div>
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 0.5rem 0;">
    Movie & Netflix Data Analysis and Visualization Dashboard | Python for Data Science Project
</div>
""", unsafe_allow_html=True)
