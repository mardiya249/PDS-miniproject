"""
=============================================================================
MODULE 1: DATA LOADING, INSPECTION, AND CLEANING (Student 1 Responsibility)
=============================================================================
Subject: Python for Data Science (GTU)
Project: Movie & Netflix Data Analysis and Visualization Dashboard

This module handles:
1. Safe CSV file loading with error checking
2. Dataset inspection (shape, schema, dtypes, memory usage)
3. Missing value identification and reporting
4. Duplicate record detection and removal
5. String standardization and whitespace stripping
6. Date-time parsing and extraction (year_added, month_added, month_name)
7. Numerical extraction from duration strings (movie_duration_min, tv_seasons_count)
8. Production of a clean, analysis-ready DataFrame
=============================================================================
"""

import os
import pandas as pd
import numpy as np


def load_raw_data(file_path_or_buffer):
    """
    Safely load dataset from a file path or file-like buffer (e.g., Streamlit UploadedFile).
    
    Parameters:
        file_path_or_buffer: str path to CSV or UploadedFile object
        
    Returns:
        tuple: (pd.DataFrame or None, str status_message, bool is_success)
    """
    try:
        if isinstance(file_path_or_buffer, str):
            if not os.path.exists(file_path_or_buffer):
                return None, f"File not found at path: {file_path_or_buffer}", False
            df = pd.read_csv(file_path_or_buffer)
        else:
            df = pd.read_csv(file_path_or_buffer)
            
        if df.empty:
            return None, "The uploaded CSV file is empty.", False
            
        # Verify essential columns exist (or warn)
        expected_cols = ['show_id', 'type', 'title', 'release_year', 'duration', 'listed_in']
        missing_expected = [c for c in expected_cols if c not in df.columns]
        if missing_expected:
            return None, f"Dataset is missing critical columns: {missing_expected}", False
            
        return df, f"Successfully loaded dataset with {len(df)} records.", True
        
    except Exception as e:
        return None, f"Error reading CSV file: {str(e)}", False


def get_dataset_summary(df):
    """
    Compute structural metadata about the DataFrame.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        dict: Summary statistics including rows, columns, memory usage, and dtypes.
    """
    if df is None or df.empty:
        return {}
        
    memory_bytes = df.memory_usage(deep=True).sum()
    memory_mb = memory_bytes / (1024 * 1024)
    
    return {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "memory_usage_mb": round(memory_mb, 2),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }


def check_missing_values(df):
    """
    Analyze missing values (nulls/NaNs) across all columns.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Table with columns ['Column', 'Missing_Count', 'Missing_Percentage']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=['Column', 'Missing_Count', 'Missing_Percentage'])
        
    null_counts = df.isnull().sum()
    null_percentages = (null_counts / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': null_counts.index,
        'Missing_Count': null_counts.values,
        'Missing_Percentage': null_percentages.round(2).values
    })
    
    # Sort descending by missing count
    return missing_df.sort_values(by='Missing_Count', ascending=False).reset_index(drop=True)


def check_duplicates(df, subset=None):
    """
    Detect duplicate rows in the dataset.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        subset (list, optional): Columns to evaluate for duplicates. Defaults to None (all columns).
        
    Returns:
        tuple: (int duplicate_count, pd.DataFrame sample_duplicates)
    """
    if df is None or df.empty:
        return 0, pd.DataFrame()
        
    # Check duplicates based on show_id if available, or entire row
    check_cols = ['show_id'] if (subset is None and 'show_id' in df.columns) else subset
    duplicates = df[df.duplicated(subset=check_cols, keep=False)]
    dup_count = int(df.duplicated(subset=check_cols).sum())
    
    return dup_count, duplicates


def clean_dataset(raw_df):
    """
    Comprehensive data cleaning and feature engineering pipeline.
    
    Operations performed:
    1. Removes duplicate rows
    2. Trims leading/trailing whitespace across all text columns
    3. Handles missing values appropriately:
       - 'director': 'Unknown Director'
       - 'cast': 'Unknown Cast'
       - 'country': 'Unknown Country'
       - 'rating': Mode or 'NR' (Not Rated)
       - 'date_added': Forward fill / median or parsed as NaT with fallback
    4. Converts 'date_added' to datetime, extracting:
       - 'year_added' (int)
       - 'month_added' (int)
       - 'month_name_added' (str)
    5. Extracts numerical duration values:
       - 'duration_num': Raw numerical magnitude
       - 'duration_unit': 'min' or 'Season(s)'
       - 'movie_duration_min': Duration in minutes for Movies (float, NaN for TV)
       - 'tv_seasons_count': Season count for TV Shows (float, NaN for Movies)
    6. Standardizes categorical columns
    
    Parameters:
        raw_df (pd.DataFrame): Uncleaned raw dataset
        
    Returns:
        tuple: (pd.DataFrame cleaned_df, dict cleaning_metrics)
    """
    if raw_df is None or raw_df.empty:
        return None, {}
        
    df = raw_df.copy()
    
    initial_rows = len(df)
    initial_nulls = int(df.isnull().sum().sum())
    
    # Step 1: Remove duplicates based on show_id or all columns
    if 'show_id' in df.columns:
        dup_count = int(df.duplicated(subset=['show_id']).sum())
        df = df.drop_duplicates(subset=['show_id'], keep='first').reset_index(drop=True)
    else:
        dup_count = int(df.duplicated().sum())
        df = df.drop_duplicates(keep='first').reset_index(drop=True)
        
    # Step 2: Trim whitespace from all string/object columns
    object_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
        # Convert string 'nan' or 'None' back to np.nan for uniform handling
        df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})
        
    # Step 3: Handle missing values in text columns
    if 'director' in df.columns:
        df['director'] = df['director'].fillna('Unknown Director')
        
    if 'cast' in df.columns:
        df['cast'] = df['cast'].fillna('Unknown Cast')
        
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('Unknown Country')
        
    if 'rating' in df.columns:
        # If rating is missing, fill with 'NR' (Not Rated)
        df['rating'] = df['rating'].fillna('NR')
        
    # Step 4: Date parsing & date feature extraction
    if 'date_added' in df.columns:
        # Convert date_added to datetime
        # Kaggle format: "September 25, 2021"
        df['date_added_dt'] = pd.to_datetime(df['date_added'], errors='coerce')
        
        # Extract features
        df['year_added'] = df['date_added_dt'].dt.year
        df['month_added'] = df['date_added_dt'].dt.month
        df['month_name_added'] = df['date_added_dt'].dt.month_name()
        
        # If year_added has NaNs due to unparseable dates, impute with release_year
        if 'release_year' in df.columns:
            df['year_added'] = df['year_added'].fillna(df['release_year']).astype(int)
        else:
            df['year_added'] = df['year_added'].fillna(df['year_added'].median()).astype(int)
            
        df['month_name_added'] = df['month_name_added'].fillna('Unknown Month')
        
    # Step 5: Duration analysis & numerical extraction
    # Standard formats: "90 min", "115 min", "1 Season", "2 Seasons"
    if 'duration' in df.columns:
        # Extract the leading integer value using regex
        df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
        
        # Determine unit: 'min' or 'Season'
        df['duration_unit'] = np.where(
            df['duration'].str.contains('min', case=False, na=False),
            'min',
            np.where(df['duration'].str.contains('Season', case=False, na=False), 'Season', 'Other')
        )
        
        # Separate Movie duration (minutes) and TV Show duration (seasons)
        if 'type' in df.columns:
            # For Movies, movie_duration_min is numeric minutes
            df['movie_duration_min'] = np.where(
                df['type'].str.lower() == 'movie',
                df['duration_num'],
                np.nan
            )
            # For TV Shows, tv_seasons_count is number of seasons
            df['tv_seasons_count'] = np.where(
                df['type'].str.lower() == 'tv show',
                df['duration_num'],
                np.nan
            )
        else:
            df['movie_duration_min'] = np.where(df['duration_unit'] == 'min', df['duration_num'], np.nan)
            df['tv_seasons_count'] = np.where(df['duration_unit'] == 'Season', df['duration_num'], np.nan)
            
    # Step 6: Standardize release_year if present
    if 'release_year' in df.columns:
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df['release_year'] = df['release_year'].fillna(df['release_year'].median()).astype(int)
        
    final_rows = len(df)
    final_nulls = int(df[['show_id', 'type', 'title', 'release_year', 'rating']].isnull().sum().sum())
    
    cleaning_metrics = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "initial_columns": int(raw_df.shape[1]),
        "final_columns": int(df.shape[1]),
        "duplicates_removed": dup_count,
        "initial_duplicates": dup_count,
        "initial_total_nulls": initial_nulls,
        "final_unhandled_core_nulls": final_nulls,
        "remaining_missing_values": int(df.isnull().sum().sum()),
        "new_features_engineered": [
            "year_added", "month_added", "month_name_added",
            "duration_num", "duration_unit", "movie_duration_min", "tv_seasons_count"
        ],
        "memory_before_mb": round(raw_df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "memory_after_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }
    
    return df, cleaning_metrics


if __name__ == "__main__":
    # Test module standalone
    test_path = "p:/Experience/movie_netflix_analysis/data/netflix_titles.csv"
    raw, msg, ok = load_raw_data(test_path)
    print(f"Load Status: {ok} | {msg}")
    if ok:
        print("\nMissing values before cleaning:")
        print(check_missing_values(raw))
        dups, _ = check_duplicates(raw)
        print(f"\nDuplicates found: {dups}")
        cleaned, metrics = clean_dataset(raw)
        print("\nCleaning Metrics:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
        print("\nCleaned DataFrame shape:", cleaned.shape)
        print("Cleaned Columns:", list(cleaned.columns))
