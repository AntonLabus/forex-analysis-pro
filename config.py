# Forex Analysis Pro - Configuration File
# Edit these settings to customize the application

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
DEBUG = True
SECRET_KEY = 'your-secret-key-change-this-in-production'

# Database Configuration
DATABASE_URL = 'sqlite:///forex_data.db'
DATABASE_POOL_SIZE = 5
DATABASE_POOL_TIMEOUT = 30

# API Configuration
ALPHA_VANTAGE_API_KEY = '9OIDA7CDTY0DJ69T'  # Alpha Vantage API key
NEWS_API_KEY = ''           # Optional: Get from https://newsapi.org/
ECONOMIC_CALENDAR_API_KEY = ''  # Optional: For economic calendar data

# Enhanced Rate Limiting Configuration
RATE_LIMIT_PER_MINUTE = 60
DAILY_REQUEST_LIMIT = 5000      # Conservative daily limit across all APIs
HOURLY_REQUEST_LIMIT = 300      # Conservative hourly limit
ALPHA_VANTAGE_DAILY_LIMIT = 20  # Leave buffer for free tier (25 max)
YAHOO_FINANCE_HOURLY_LIMIT = 100  # Conservative Yahoo Finance limit

# API-Specific Rate Limits (requests per hour)
API_RATE_LIMITS = {
    'yahoo_finance': 100,
    'alpha_vantage': 20,      # Daily limit spread across 24 hours
    'exchangerate_api': 50,   # Conservative for 1500/month limit
    'exchangerate_host': 500, # High tolerance
    'fawaz_currency': 1000    # GitHub CDN, very high tolerance
}

# Data Source Configuration
PRIMARY_DATA_SOURCE = 'yahoo'  # 'yahoo' or 'alphavantage'
ENABLE_CACHING = True
CACHE_TIMEOUT_SECONDS = 900  # 15 minutes (increased from 5 minutes)
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

# Smart Caching Configuration
PRICE_CACHE_TIMEOUT = 300       # 5 minutes for current prices
HISTORICAL_CACHE_TIMEOUT = 3600  # 1 hour for historical data
SIGNAL_CACHE_TIMEOUT = 900      # 15 minutes for signals
TECHNICAL_CACHE_TIMEOUT = 600   # 10 minutes for technical analysis

# Analysis Configuration
TECHNICAL_ANALYSIS_ENABLED = True
FUNDAMENTAL_ANALYSIS_ENABLED = True

# Technical Analysis Parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2
SMA_PERIODS = [20, 50, 200]
EMA_PERIODS = [12, 26, 50]

# Signal Generation Configuration
SIGNAL_CONFIDENCE_THRESHOLD = 60  # Minimum confidence percentage to show signal
TECHNICAL_WEIGHT = 0.6  # Technical analysis weight in combined signals
FUNDAMENTAL_WEIGHT = 0.4  # Fundamental analysis weight in combined signals

# Update Intervals (seconds) - Optimized for API limits
PRICE_UPDATE_INTERVAL = 30     # Increased from 5 seconds
SIGNAL_UPDATE_INTERVAL = 300   # Increased from 60 seconds (5 minutes)
PORTFOLIO_UPDATE_INTERVAL = 600 # Increased from 300 seconds (10 minutes)

# Request Priority System
HIGH_PRIORITY_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY']  # Most important pairs
MEDIUM_PRIORITY_PAIRS = ['AUDUSD', 'USDCHF', 'USDCAD']
LOW_PRIORITY_PAIRS = ['NZDUSD', 'EURGBP']

# Rate Limiting Strategies
ENABLE_SMART_THROTTLING = True  # Automatically adjust request frequency
ENABLE_REQUEST_QUEUING = True   # Queue requests when rate limited
MAX_QUEUE_SIZE = 100           # Maximum queued requests
QUEUE_TIMEOUT = 300            # 5 minutes queue timeout

# UI Configuration
DEFAULT_THEME = 'dark'  # 'dark' or 'light'
DEFAULT_CURRENCY_PAIR = 'EUR/USD'
DEFAULT_TIMEFRAME = '1h'
SHOW_VOLUME = True
SHOW_GRID = True

# WebSocket Configuration
WEBSOCKET_ENABLED = True
WEBSOCKET_PING_INTERVAL = 25
WEBSOCKET_PING_TIMEOUT = 60

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'forex_analysis.log'
LOG_MAX_SIZE = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# Security Configuration
CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
RATE_LIMIT_PER_MINUTE = 60
ENABLE_CSRF_PROTECTION = True

# Performance Configuration
ENABLE_COMPRESSION = True
STATIC_FILE_CACHE_TIMEOUT = 86400  # 24 hours
API_CACHE_TIMEOUT = 300  # 5 minutes

# Currency Pairs Configuration
SUPPORTED_PAIRS = [
    'EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD',
    'USD/CHF', 'USD/CAD', 'NZD/USD', 'GBP/JPY'
]

# Timeframes Configuration
SUPPORTED_TIMEFRAMES = [
    '1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'
]

# Risk Management Configuration
DEFAULT_RISK_PERCENTAGE = 2.0  # 2% risk per trade
DEFAULT_STOP_LOSS_PIPS = 50
DEFAULT_TAKE_PROFIT_RATIO = 2.0  # 2:1 reward to risk

# Notification Configuration
ENABLE_SIGNAL_NOTIFICATIONS = True
ENABLE_PRICE_ALERTS = True
NOTIFICATION_SOUND = True

# Advanced Features
ENABLE_BACKTESTING = False  # Feature for future implementation
ENABLE_PORTFOLIO_TRACKING = True
ENABLE_ECONOMIC_CALENDAR = True
ENABLE_NEWS_SENTIMENT = False  # Requires NEWS_API_KEY

# Development Configuration
ENABLE_DEBUG_TOOLBAR = False
ENABLE_PROFILING = False
MOCK_DATA_MODE = False  # Use mock data instead of real API calls
