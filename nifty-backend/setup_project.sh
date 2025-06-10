#!/bin/bash

# Navigate to the project folder
cd ~/Documents/Amazon/nifty-backend

# Create necessary folders if they don't exist
mkdir -p static templates

echo "✅ Downloading backend Python files..."
# Backend scripts
wget -O app.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/app.py
wget -O utils.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/utils.py
wget -O fetch_and_cache_all.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/fetch_and_cache_all.py
wget -O run_indicators.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/run_indicators.py
wget -O indicators.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/indicators.py
wget -O stocks.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/stocks.py
wget -O create_nifty_db.py https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/create_nifty_db.py

echo "✅ Downloading frontend files..."
# Frontend files
wget -O templates/grid.html https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/templates/grid.html
wget -O static/style.css https://raw.githubusercontent.com/SAISHIVASHANKAR/nifty-backend/main/static/style.css

echo "✅ All files downloaded and ready."
