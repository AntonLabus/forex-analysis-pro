@echo off
echo Updating Git Repository...
cd /d "C:\Users\labus\OneDrive\Documents\GitHub\Forex"

echo.
echo Adding changes to staging...
git add -A

echo.
echo Checking status...
git status --short

echo.
echo Committing changes...
git commit -m "Optimize crypto API requests and fix rate limiting issues

Major crypto API optimizations:
- Reduced crypto pairs from 36 to 12 most popular (67% reduction)
- Implemented market-specific concurrency (2 workers for crypto vs 4 for forex)
- Added conservative rate limits for CoinGecko (25/hr) and Binance (100/hr)
- Increased throttle delays for crypto APIs (1.5s CoinGecko, 1.0s Binance)
- Added 500ms delays between crypto requests to prevent overload
- Implemented comprehensive fallback system with realistic demo data
- Enhanced error handling with progressive API fallbacks
- Added clear data quality indicators for demo vs live data

Resolves 'All data sources failed' errors
Ensures crypto toggle works reliably even during API outages
Maintains full forex functionality with existing optimizations"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Git update completed!
pause
