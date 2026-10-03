"""
=============================================================================
MODULE 3: DATA VISUALIZATION WITH MATPLOTLIB & SEABORN (Student 3 Responsibility)
=============================================================================
Subject: Python for Data Science (GTU)
Project: Movie & Netflix Data Analysis and Visualization Dashboard

Design: Modern Dark Cinematic & Sleek Light Analytics Aesthetics
- Dark Theme:
  - Background: #0F1117 (App) | #181B24 (Card)
  - Grid: #282D3D | Spine: #282D3D
  - Primary: #E50914 (Cinema Red) | Secondary: #00B8D9 (Cyan)
  - Text: #FFFFFF | Muted: #A7A7A7
- Light Theme:
  - Background: #F5F7FA (App) | #FFFFFF (Card)
  - Grid: #E5E7EB | Spine: #E5E7EB
  - Primary: #D90429 (Crimson) | Secondary: #0077B6 (Ocean Blue)
  - Text: #1F2937 | Muted: #6B7280
=============================================================================
"""

import matplotlib
matplotlib.use('Agg')  # Headless backend for web servers and Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import html
import base64

# =============================================================================
# THEME CONFIGURATION & COLOR TOKENS
# =============================================================================
THEME_TOKENS = {
    "dark": {
        "name": "dark",
        "app_bg": "#0F1117",
        "card_bg": "#181B24",
        "grid": "#282D3D",
        "spine": "#282D3D",
        "text": "#FFFFFF",
        "text_muted": "#A7A7A7",
        "primary": "#E50914",
        "secondary": "#00B8D9",
        "movie": "#E50914",
        "tv": "#00B8D9",
        "emerald": "#10B981",
        "amber": "#F59E0B",
        "purple": "#8B5CF6"
    },
    "light": {
        "name": "light",
        "app_bg": "#F5F7FA",
        "card_bg": "#FFFFFF",
        "grid": "#E5E7EB",
        "spine": "#E5E7EB",
        "text": "#1F2937",
        "text_muted": "#6B7280",
        "primary": "#D90429",
        "secondary": "#0077B6",
        "movie": "#D90429",
        "tv": "#0077B6",
        "emerald": "#059669",
        "amber": "#D97706",
        "purple": "#7C3AED"
    }
}

# Backward-compatibility color constants
DARK_BG = "#181B24"
DARK_GRID = "#282D3D"
TEXT_LIGHT = "#FFFFFF"
TEXT_MUTED = "#B8B8B8"
COLOR_PRIMARY = "#E50914"
COLOR_CYAN = "#00B4D8"
COLOR_EMERALD = "#10B981"
COLOR_AMBER = "#F59E0B"
COLOR_PURPLE = "#8B5CF6"
MOVIE_COLOR = "#E50914"
TV_COLOR = "#00B4D8"


def get_theme_tokens(theme="Dark"):
    """Return dictionary of color tokens for the specified theme ('Dark' or 'Light')."""
    key = "light" if str(theme).lower() == "light" else "dark"
    return THEME_TOKENS[key]


def apply_theme(fig, ax, title="", theme="Dark"):
    """
    Apply cohesive visual styling to any Matplotlib axis based on active theme.
    """
    t = get_theme_tokens(theme)
    fig.patch.set_facecolor(t["card_bg"])
    ax.set_facecolor(t["card_bg"])
    
    if title:
        ax.set_title(title, fontsize=12.5, weight='bold', color=t["text"], pad=14)
        
    ax.tick_params(colors=t["text_muted"], which='both', labelsize=9.5)
    ax.xaxis.label.set_color(t["text_muted"])
    ax.yaxis.label.set_color(t["text_muted"])
    ax.xaxis.label.set_fontsize(10.0)
    ax.yaxis.label.set_fontsize(10.0)
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_weight('bold')
    
    ax.grid(True, color=t["grid"], linestyle='--', linewidth=0.8, alpha=0.7)
    
    for spine in ax.spines.values():
        spine.set_edgecolor(t["spine"])
        spine.set_linewidth(1.0)


def apply_dark_theme(fig, ax, title=""):
    """Helper to apply consistent dark cinematic styling (maintained for backward compatibility)."""
    apply_theme(fig, ax, title=title, theme="Dark")


__all__ = [
    "get_theme_tokens",
    "apply_theme",
    "apply_dark_theme",
    "plot_type_donut",
    "plot_type_distribution",
    "plot_top_genres",
    "plot_top_countries",
    "plot_release_trend",
    "plot_release_bar",
    "plot_rating_distribution",
    "plot_movie_duration_dist",
    "plot_tv_seasons_dist",
    "plot_correlation_heatmap",
    "plot_monthly_added_trend",
    "plot_missing_values_bar",
    "create_poster_placeholder",
    "render_poster_card"
]


# =============================================================================
# 1. CONTENT TYPE PLOTS (DONUT & DUAL VIEW)
# =============================================================================
def plot_type_donut(filtered_df, theme="Dark"):
    """
    Generate a professional donut chart comparing Movies vs TV Shows
    from the filtered DataFrame.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(6, 4.8), dpi=100)
    fig.patch.set_facecolor(t["card_bg"])
    ax.set_facecolor(t["card_bg"])
    
    if filtered_df is None or filtered_df.empty or 'type' not in filtered_df.columns:
        ax.text(0.5, 0.5, "No data available", ha='center', va='center', color=t["text_muted"])
        ax.axis('off')
        return fig
        
    counts = filtered_df['type'].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()
    colors = [t["movie"] if lbl.lower() == 'movie' else t["tv"] for lbl in labels]
    
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        explode=[0.04] * len(values),
        wedgeprops=dict(width=0.45, edgecolor=t["card_bg"], linewidth=2.5),
        pctdistance=0.75,
        textprops={'fontsize': 10.5, 'weight': 'bold', 'color': t["text"]}
    )
    for at in autotexts:
        at.set_color('#FFFFFF')
        at.set_fontsize(10.5)
        at.set_weight('bold')
        
    for txt in texts:
        txt.set_color(t["text"])
        txt.set_fontsize(10.5)
        txt.set_weight('bold')
        
    total_count = sum(values)
    ax.text(0, 0, f"Total\n{total_count:,}", ha='center', va='center', fontsize=11.5, weight='bold', color=t["text"])
    ax.set_title("Movies vs TV Shows Ratio", fontsize=12.5, weight='bold', color=t["text"], pad=14)
    
    plt.tight_layout()
    return fig


def plot_type_distribution(df, theme="Dark"):
    """
    Generate side-by-side Donut Chart and Bar Chart comparing Movies vs TV Shows.
    Maintained for full backward compatibility and dual-chart views.
    """
    t = get_theme_tokens(theme)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=100)
    fig.patch.set_facecolor(t["card_bg"])
    
    if df is None or df.empty or 'type' not in df.columns:
        ax1.text(0.5, 0.5, "No data available", ha='center', va='center', color=t["text_muted"])
        ax1.axis('off')
        ax2.axis('off')
        return fig
        
    counts = df['type'].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()
    colors = [t["movie"] if lbl.lower() == 'movie' else t["tv"] for lbl in labels]
    
    # 1. Donut Chart (Left)
    ax1.set_facecolor(t["card_bg"])
    wedges, texts, autotexts = ax1.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        explode=[0.04] * len(values),
        wedgeprops=dict(width=0.45, edgecolor=t["card_bg"], linewidth=2),
        pctdistance=0.75,
        textprops={'fontsize': 10.5, 'weight': 'bold', 'color': t["text"]}
    )
    for at in autotexts:
        at.set_color('#FFFFFF')
        at.set_fontsize(10.5)
        at.set_weight('bold')
    for txt in texts:
        txt.set_color(t["text"])
        
    total_count = sum(values)
    ax1.text(0, 0, f"Total\n{total_count:,}", ha='center', va='center', fontsize=11, weight='bold', color=t["text"])
    ax1.set_title("Catalog Composition (% Share)", fontsize=12, weight='bold', color=t["text"], pad=12)
    
    # 2. Count Bar Chart (Right)
    apply_theme(fig, ax2, "Title Count by Format", theme=theme)
    bars = ax2.bar(labels, values, color=colors, width=0.42, edgecolor='none', alpha=0.95)
    ax2.set_ylabel("Number of Titles")
    ax2.set_ylim(0, max(values) * 1.18 if values else 10)
    
    for bar in bars:
        h = bar.get_height()
        pct = (h / total_count) * 100 if total_count > 0 else 0
        ax2.annotate(
            f"{int(h):,} ({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 5),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=10, weight='bold', color=t["text"]
        )
        
    plt.tight_layout()
    return fig


# =============================================================================
# 2. GENRE PLOT (HORIZONTAL BAR)
# =============================================================================
def plot_top_genres(genre_df, top_n=10, theme="Dark"):
    """
    Generate horizontal bar chart of top genres adapting to active theme.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    apply_theme(fig, ax, f"Top {top_n} Genres", theme=theme)
    
    if genre_df is None or genre_df.empty:
        ax.text(0.5, 0.5, "No genre data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    plot_df = genre_df.head(top_n).iloc[::-1].reset_index(drop=True)
    
    # Vibrant gradient palette tailored to theme
    palette = sns.light_palette(t["primary"], n_colors=len(plot_df) + 3, reverse=False)[3:]
    bars = ax.barh(plot_df['Genre'], plot_df['Count'], color=palette, edgecolor='none', height=0.62)
    
    ax.set_xlabel("Number of Titles")
    ax.set_xlim(0, max(plot_df['Count']) * 1.25 if not plot_df.empty else 10)
    
    for bar, pct in zip(bars, plot_df['Percentage']):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.annotate(
            f"{int(w):,} ({pct:.1f}%)",
            xy=(w, y),
            xytext=(6, 0),
            textcoords="offset points",
            ha='left', va='center',
            fontsize=9, weight='bold', color=t["text"]
        )
        
    plt.tight_layout()
    return fig


# =============================================================================
# 3. COUNTRY PLOT (VERTICAL BAR)
# =============================================================================
def plot_top_countries(country_df, top_n=10, theme="Dark"):
    """
    Generate vertical bar chart of top content-producing nations.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    apply_theme(fig, ax, f"Top {top_n} Producing Countries", theme=theme)
    
    if country_df is None or country_df.empty:
        ax.text(0.5, 0.5, "No country data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    plot_df = country_df.head(top_n)
    
    palette = sns.light_palette(t["secondary"], n_colors=len(plot_df) + 4, reverse=True)[:-4]
    bars = ax.bar(plot_df['Country'], plot_df['Count'], color=palette, width=0.55, edgecolor='none')
    
    ax.set_ylabel("Total Titles")
    ax.set_ylim(0, max(plot_df['Count']) * 1.25 if not plot_df.empty else 10)
    plt.xticks(rotation=35, ha='right', fontsize=9, color=t["text_muted"])
    
    for bar, pct in zip(bars, plot_df['Percentage']):
        h = bar.get_height()
        ax.annotate(
            f"{int(h):,}\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=8.5, weight='bold', color=t["text"]
        )
        
    plt.tight_layout()
    return fig


# =============================================================================
# 4. RELEASE YEAR PLOTS (LINE & BAR)
# =============================================================================
def plot_release_trend(release_data, theme="Dark"):
    """
    Generate time series line chart with filled area for release years.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    apply_theme(fig, ax, "Content Released by Year (Timeline)", theme=theme)
    
    yearly_df = release_data.get("yearly_trend", pd.DataFrame())
    if yearly_df.empty or 'Year' not in yearly_df.columns:
        ax.text(0.5, 0.5, "No timeline data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    years = yearly_df['Year'].values
    total_counts = yearly_df['Total'].values
    
    # Primary line with soft glow fill
    ax.plot(years, total_counts, color=t["primary"], linewidth=2.5, marker='o', markersize=3.5, label='Total Releases')
    ax.fill_between(years, total_counts, color=t["primary"], alpha=0.18)
    
    if 'Movie' in yearly_df.columns:
        ax.plot(years, yearly_df['Movie'].values, color='#EF4444', linestyle='--', linewidth=1.6, label='Movies')
    if 'TV Show' in yearly_df.columns:
        ax.plot(years, yearly_df['TV Show'].values, color=t["secondary"], linestyle=':', linewidth=1.8, label='TV Shows')
        
    peak_y = release_data.get("peak_year")
    peak_c = release_data.get("peak_count")
    if peak_y and peak_c:
        gold_color = '#D97706' if t['name'] == 'light' else '#FBBF24'
        ax.scatter([peak_y], [peak_c], color=gold_color, s=70, zorder=5)
        ax.annotate(
            f"Peak: {peak_y} ({peak_c})",
            xy=(peak_y, peak_c),
            xytext=(0, 12),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=9.5, weight='bold', color=gold_color,
            arrowprops=dict(arrowstyle="->", color=gold_color, lw=1.2)
        )
        
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Titles Released")
    ax.legend(frameon=True, facecolor=t["card_bg"], edgecolor=t["grid"], labelcolor=t["text"], fontsize=9)
    
    plt.tight_layout()
    return fig


def plot_release_bar(release_data, theme="Dark"):
    """
    Generate bar chart of content releases by year.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)
    apply_theme(fig, ax, "Yearly Release Volume (Bar Distribution)", theme=theme)
    
    yearly_df = release_data.get("yearly_trend", pd.DataFrame())
    if yearly_df.empty or 'Year' not in yearly_df.columns:
        ax.text(0.5, 0.5, "No release data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    years = yearly_df['Year'].values
    counts = yearly_df['Total'].values
    
    bars = ax.bar(years, counts, color=t["primary"], width=0.7, edgecolor='none', alpha=0.9)
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Titles")
    ax.set_ylim(0, max(counts) * 1.15 if len(counts) > 0 else 10)
    
    plt.tight_layout()
    return fig


# =============================================================================
# 5. RATING DISTRIBUTION PLOT
# =============================================================================
def plot_rating_distribution(ratings_df=None, ratings_table=None, theme="Dark"):
    """
    Generate bar chart showing ratings distribution across content.
    Accepts ratings_df or ratings_table.
    """
    if ratings_df is None:
        ratings_df = ratings_table
        
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=100)
    apply_theme(fig, ax, "Content Rating Distribution", theme=theme)
    
    if ratings_df is None or ratings_df.empty:
        ax.text(0.5, 0.5, "No rating data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    x = np.arange(len(ratings_df))
    width = 0.38
    
    bars_movie = ax.bar(x - width/2, ratings_df['Movies'], width, label='Movies', color=t["movie"], alpha=0.9)
    bars_tv = ax.bar(x + width/2, ratings_df['TV Shows'], width, label='TV Shows', color=t["tv"], alpha=0.9)
    
    ax.set_xlabel("Maturity Rating Code")
    ax.set_ylabel("Number of Titles")
    ax.set_xticks(x)
    ax.set_xticklabels(ratings_df['Rating'], rotation=25, ha='right', fontsize=9.5, color=t["text_muted"])
    ax.legend(frameon=True, facecolor=t["card_bg"], edgecolor=t["grid"], labelcolor=t["text"], fontsize=9.5)
    
    for i, total in enumerate(ratings_df['Total']):
        top_y = max(ratings_df['Movies'].iloc[i], ratings_df['TV Shows'].iloc[i])
        pct = ratings_df['Percentage'].iloc[i]
        ax.annotate(
            f"{total}\n({pct}%)",
            xy=(i, top_y),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=8, weight='bold', color=t["text"]
        )
        
    ax.set_ylim(0, max(ratings_df['Total']) * 1.18 if not ratings_df.empty else 10)
    plt.tight_layout()
    return fig


# =============================================================================
# 6. DURATION & SEASONS PLOTS
# =============================================================================
def plot_movie_duration_dist(movie_series, movie_stats=None, theme="Dark"):
    """
    Generate histogram with Kernel Density Estimate (KDE) for movie duration in minutes,
    featuring Mean line and Median line.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=100)
    apply_theme(fig, ax, "Movie Duration Distribution (Minutes)", theme=theme)
    
    if movie_series is None or movie_series.empty:
        ax.text(0.5, 0.5, "No movie duration data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    sns.histplot(
        movie_series,
        bins=25,
        kde=True,
        color=t["primary"],
        edgecolor=t["card_bg"],
        linewidth=1.0,
        alpha=0.65,
        ax=ax
    )
    
    mean_val = movie_stats.get('mean', float(np.mean(movie_series))) if movie_stats else float(np.mean(movie_series))
    median_val = movie_stats.get('median', float(np.median(movie_series))) if movie_stats else float(np.median(movie_series))
    
    ax.axvline(mean_val, color="#EF4444", linestyle='--', linewidth=2, label=f"Mean: {mean_val:.1f} min")
    ax.axvline(median_val, color=t["amber"], linestyle='-.', linewidth=2, label=f"Median: {median_val:.1f} min")
    
    ax.set_xlabel("Movie Duration (Minutes)")
    ax.set_ylabel("Number of Movies")
    ax.legend(frameon=True, facecolor=t["card_bg"], edgecolor=t["grid"], labelcolor=t["text"], fontsize=9.5)
    
    plt.tight_layout()
    return fig


def plot_tv_seasons_dist(tv_series, tv_stats=None, theme="Dark"):
    """
    Generate frequency distribution bar plot of TV Show season counts.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    apply_theme(fig, ax, "TV Show Longevity: Season Count Distribution", theme=theme)
    
    if tv_series is None or tv_series.empty:
        ax.text(0.5, 0.5, "No TV Show season data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    season_counts = tv_series.value_counts().sort_index()
    seasons = [f"S{int(s)}" if s > 1 else "1 Season" for s in season_counts.index]
    counts = season_counts.values
    total = sum(counts)
    
    palette = sns.light_palette(t["secondary"], n_colors=len(seasons) + 2, reverse=True)[:-2]
    bars = ax.bar(seasons, counts, color=palette, width=0.52, edgecolor='none')
    
    ax.set_xlabel("Number of Seasons")
    ax.set_ylabel("Number of TV Series")
    ax.set_ylim(0, max(counts) * 1.2 if len(counts) > 0 else 10)
    
    for bar in bars:
        h = bar.get_height()
        pct = (h / total) * 100 if total > 0 else 0
        ax.annotate(
            f"{int(h)}\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=9, weight='bold', color=t["text"]
        )
        
    plt.tight_layout()
    return fig


# =============================================================================
# 7. CORRELATION HEATMAP
# =============================================================================
def plot_correlation_heatmap(corr_df, theme="Dark"):
    """
    Generate Pearson correlation heatmap strictly on numeric variables.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(7, 5.2), dpi=100)
    apply_theme(fig, ax, "Pearson Correlation Heatmap", theme=theme)
    
    if corr_df is None or corr_df.empty:
        ax.text(0.5, 0.5, "No correlation data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    mask = np.triu(np.ones_like(corr_df, dtype=bool))
    
    sns.heatmap(
        corr_df,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=1.5,
        linecolor=t["card_bg"],
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation (r)"},
        annot_kws={"fontsize": 10.5, "weight": "bold", "color": t["text"]},
        ax=ax
    )
    
    plt.xticks(rotation=25, ha='right', fontsize=9.5, color=t["text_muted"])
    plt.yticks(rotation=0, fontsize=9.5, color=t["text_muted"])
    
    plt.tight_layout()
    return fig


# =============================================================================
# 8. MONTHLY ADDITION TREND PLOT
# =============================================================================
def plot_monthly_added_trend(df, theme="Dark"):
    """
    Generate bar chart of content addition volume across calendar months.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)
    apply_theme(fig, ax, "Seasonal Trend: Titles Added by Calendar Month", theme=theme)
    
    if df is None or df.empty or 'month_name_added' not in df.columns:
        ax.text(0.5, 0.5, "No monthly addition data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    counts = df['month_name_added'].value_counts()
    reordered_counts = [counts.get(m, 0) for m in month_order]
    short_months = [m[:3] for m in month_order]
    
    palette = sns.light_palette(t["emerald"], n_colors=14, reverse=False)[2:]
    bars = ax.bar(short_months, reordered_counts, color=palette, width=0.58, edgecolor='none')
    
    ax.set_xlabel("Month of Addition")
    ax.set_ylabel("Titles Added")
    ax.set_ylim(0, max(reordered_counts) * 1.18 if reordered_counts else 10)
    
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(
                f"{int(h)}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8.5, weight='bold', color=t["text"]
            )
            
    plt.tight_layout()
    return fig


# =============================================================================
# 9. MISSING VALUES AUDIT PLOT
# =============================================================================
def plot_missing_values_bar(missing_df, theme="Dark"):
    """
    Generate horizontal bar chart depicting percentage of missing values per column.
    """
    t = get_theme_tokens(theme)
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    apply_theme(fig, ax, "Missing Values Audit (% of Total Rows)", theme=theme)
    
    if missing_df is None or missing_df.empty:
        ax.text(0.5, 0.5, "No missing value data available", ha='center', va='center', color=t["text_muted"])
        return fig
        
    plot_df = missing_df[missing_df['Missing_Count'] > 0].iloc[::-1]
    
    if plot_df.empty:
        ax.text(0.5, 0.5, "Zero Missing Values in Cleaned Dataset!", ha='center', va='center', fontsize=11, weight='bold', color=t["emerald"])
        ax.axis('off')
        return fig
        
    palette = sns.light_palette(t["primary"], n_colors=len(plot_df) + 2, reverse=False)[2:]
    bars = ax.barh(plot_df['Column'], plot_df['Missing_Percentage'], color=palette, height=0.55)
    
    ax.set_xlabel("Missing Percentage (%)")
    ax.set_xlim(0, max(plot_df['Missing_Percentage']) * 1.25)
    
    for bar, cnt in zip(bars, plot_df['Missing_Count']):
        w = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.annotate(
            f"{w:.1f}% ({int(cnt)} rows)",
            xy=(w, y),
            xytext=(6, 0),
            textcoords="offset points",
            ha='left', va='center',
            fontsize=8.5, weight='bold', color=t["text"]
        )
        
    plt.tight_layout()
    return fig


# =============================================================================
# 10. MOVIE POSTERS & FEATURED TITLE CARD GENERATION
# =============================================================================
def create_poster_placeholder(title, content_type="Movie", release_year="", rating="", genre="", theme="Dark"):
    """
    Generate an elegant vector SVG cinema poster placeholder.
    Safe, deterministic, zero-network, zero-API dependency.
    
    Parameters:
        title (str): Title of the show/movie
        content_type (str): 'Movie' or 'TV Show'
        release_year (int/str): Release year
        rating (str): Content rating (e.g., 'TV-MA', 'PG-13')
        genre (str): Genre or tags
        theme (str): 'Dark' or 'Light'
        
    Returns:
        str: Clean SVG XML string
    """
    is_light = str(theme).lower() == "light"
    
    bg_start = "#FFFFFF" if is_light else "#1A1D27"
    bg_end = "#E5E7EB" if is_light else "#0E1017"
    border_col = "#D1D5DB" if is_light else "#2C3142"
    text_col = "#111827" if is_light else "#FFFFFF"
    subtext_col = "#6B7280" if is_light else "#94A3B8"
    
    is_movie = str(content_type).lower() == "movie"
    accent_col = ("#D90429" if is_light else "#E50914") if is_movie else ("#0077B6" if is_light else "#00B8D9")
    format_label = "MOVIE" if is_movie else "TV SHOW"
    
    clean_title = html.escape(str(title).strip() if title else "Untitled")
    clean_rating = html.escape(str(rating).strip() if rating and str(rating) != "nan" else "NR")
    clean_year = str(release_year).strip() if release_year and str(release_year) != "nan" else ""
    clean_genre = html.escape(str(genre).split(',')[0].strip() if genre and str(genre) != "nan" else "General")
    
    # Simple, reliable word wrap
    words = clean_title.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 <= 16:
            curr.append(w)
            curr_len += len(w) + 1
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        if len(lines) >= 3:
            break
    if curr and len(lines) < 3:
        lines.append(" ".join(curr))
    if not lines:
        lines = [clean_title[:16]]
        
    tspan_html = ""
    start_y = 214 if len(lines) == 1 else (200 if len(lines) == 2 else 186)
    for i, line in enumerate(lines):
        y = start_y + (i * 22)
        tspan_html += f'<tspan x="120" y="{y}">{line}</tspan>'
        
    # Vector art inside poster
    if is_movie:
        cinema_art = f'''
        <path d="M72 104 h96 a6 6 0 0 1 6 6 v48 a6 6 0 0 1 -6 6 h-96 a6 6 0 0 1 -6 -6 v-48 a6 6 0 0 1 6 -6 z" fill="none" stroke="{accent_col}" stroke-width="2.2"/>
        <path d="M66 104 l24 -24 h86 l-20 24 z" fill="{accent_col}" opacity="0.3"/>
        <line x1="88" y1="80" x2="102" y2="104" stroke="{accent_col}" stroke-width="2"/>
        <line x1="116" y1="80" x2="130" y2="104" stroke="{accent_col}" stroke-width="2"/>
        <line x1="144" y1="80" x2="158" y2="104" stroke="{accent_col}" stroke-width="2"/>
        <circle cx="120" cy="134" r="14" fill="{accent_col}" opacity="0.25"/>
        <polygon points="116,127 128,134 116,141" fill="{text_col}"/>
        '''
    else:
        cinema_art = f'''
        <rect x="74" y="90" width="92" height="60" rx="6" fill="none" stroke="{accent_col}" stroke-width="2.2"/>
        <line x1="102" y1="150" x2="92" y2="164" stroke="{accent_col}" stroke-width="2.2"/>
        <line x1="138" y1="150" x2="148" y2="164" stroke="{accent_col}" stroke-width="2.2"/>
        <line x1="84" y1="164" x2="156" y2="164" stroke="{accent_col}" stroke-width="2.2" stroke-linecap="round"/>
        <circle cx="120" cy="120" r="14" fill="{accent_col}" opacity="0.25"/>
        <polygon points="116,113 128,120 116,127" fill="{text_col}"/>
        '''

    grad_id = f"bg_{abs(hash(clean_title)) % 100000}"
    glow_id = f"glow_{abs(hash(clean_title)) % 100000}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 340" width="100%" height="100%" style="border-radius: 10px; display: block; box-shadow: 0 4px 14px rgba(0,0,0,{"0.12" if is_light else "0.35"});">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{bg_start}"/>
      <stop offset="100%" stop-color="{bg_end}"/>
    </linearGradient>
    <radialGradient id="{glow_id}" cx="50%" cy="35%" r="60%">
      <stop offset="0%" stop-color="{accent_col}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{bg_end}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="240" height="340" rx="10" fill="url(#{grad_id})" stroke="{border_col}" stroke-width="1.2"/>
  <rect width="240" height="340" rx="10" fill="url(#{glow_id})"/>
  
  <rect x="14" y="14" width="76" height="20" rx="10" fill="{accent_col}" fill-opacity="0.18" stroke="{accent_col}" stroke-width="1"/>
  <text x="52" y="28" fill="{accent_col}" font-size="8.5" font-weight="bold" font-family="-apple-system, sans-serif" text-anchor="middle" letter-spacing="0.5">{format_label}</text>
  
  <rect x="176" y="14" width="50" height="20" rx="10" fill="{"rgba(0,0,0,0.06)" if is_light else "rgba(255,255,255,0.08)"}" stroke="{border_col}" stroke-width="1"/>
  <text x="201" y="28" fill="{subtext_col}" font-size="8.5" font-weight="bold" font-family="-apple-system, sans-serif" text-anchor="middle">{clean_rating}</text>
  
  {cinema_art}
  
  <line x1="36" y1="168" x2="204" y2="168" stroke="{border_col}" stroke-width="0.8" opacity="0.6"/>
  
  <text fill="{text_col}" font-size="14" font-weight="800" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" text-anchor="middle">
    {tspan_html}
  </text>
  
  <line x1="20" y1="298" x2="220" y2="298" stroke="{border_col}" stroke-width="0.8" opacity="0.6"/>
  <text x="20" y="318" fill="{accent_col}" font-size="10.5" font-weight="600" font-family="-apple-system, sans-serif">{clean_genre[:16]}</text>
  <text x="220" y="318" fill="{subtext_col}" font-size="10.5" font-weight="bold" font-family="-apple-system, sans-serif" text-anchor="end">{clean_year}</text>
</svg>'''
    return svg


def render_poster_card(item, theme="Dark"):
    """
    Render a responsive HTML card showing Poster, Title, Type, Release Year, and Rating.
    Safely utilizes poster_url column if present in item, falling back to clean vector placeholder.
    """
    if isinstance(item, pd.Series):
        item = item.to_dict()
        
    t = get_theme_tokens(theme)
    title = item.get('title', 'Unknown Title')
    ctype = item.get('type', 'Movie')
    year = item.get('release_year', '')
    rating = item.get('rating', 'NR')
    genre = item.get('listed_in', '')
    
    # Check if a custom poster URL exists
    poster_url = item.get('poster_url', None)
    has_valid_url = poster_url and isinstance(poster_url, str) and (poster_url.startswith('http://') or poster_url.startswith('https://'))
    
    if has_valid_url:
        img_html = f'<img src="{poster_url}" alt="{html.escape(str(title))}" style="width: 100%; height: 260px; object-fit: cover; border-radius: 8px; display: block;"/>'
    else:
        svg_code = create_poster_placeholder(title, ctype, year, rating, genre, theme=theme)
        svg_b64 = base64.b64encode(svg_code.encode('utf-8')).decode('utf-8')
        img_html = f'<img src="data:image/svg+xml;base64,{svg_b64}" alt="{html.escape(str(title))}" style="width: 100%; height: auto; border-radius: 8px; display: block;"/>'
        
    card_html = f"""
    <div style="background-color: {t['card_bg']}; border: 1px solid {t['spine']}; border-radius: 10px; padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,{'0.06' if t['name'] == 'light' else '0.25'}); transition: transform 0.2s ease;">
        {img_html}
        <div style="margin-top: 10px; font-weight: 700; font-size: 0.95rem; color: {t['text']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{html.escape(str(title))}">
            {html.escape(str(title))}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px; font-size: 0.8rem; color: {t['text_muted']};">
            <span style="color: {t['movie'] if str(ctype).lower() == 'movie' else t['tv']}; font-weight: 600;">{ctype}</span>
            <span>{year} &bull; <strong>{rating}</strong></span>
        </div>
    </div>
    """
    return card_html
