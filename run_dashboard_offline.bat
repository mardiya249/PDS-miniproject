@echo off
title Movie & Netflix Dashboard (Offline Mode)
cd /d "%~dp0"

echo ================================================================
echo   MOVIE & NETFLIX DATA ANALYSIS DASHBOARD (OFFLINE LOCAL MODE)
echo ================================================================
echo.
echo  Opening browser at http://localhost:8501 ...
echo  (This works 100%% offline with NO internet or network required)
echo.

start http://localhost:8501
python -m streamlit run app.py

pause
