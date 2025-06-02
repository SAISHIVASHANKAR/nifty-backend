# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
# │ │ │ │ │
# │ │ │ │ │
# │ │ │ │ │
# ┴ ┴ ┴ ┴ ┴
# Run EOD fetch at 6:00 PM every day
0 18 * * * cd ~/Documents/Amazon/nifty-backend && /usr/bin/python3 fetch_and_cache_all.py >> logs/eod_fetch.log 2>&1

# Run technical indicators at 6:05 PM every day
5 18 * * * cd ~/Documents/Amazon/nifty-backend && /usr/bin/python3 run_indicators.py >> logs/indicators.log 2>&1

# Run hotnews fetch at 6:05 AM and 6:05 PM daily
5 6,18 * * * cd ~/Documents/Amazon/nifty-backend && /usr/bin/python3 fetch_and_cache_hotnews.py >> logs/hotnews.log 2>&1
