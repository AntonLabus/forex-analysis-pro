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
ALPHA_VANTAGE_API_KEY = ''  # Optional: Get from https://www.alphavantage.co/support/#api-key
NEWS_API_KEY = ''           # Optional: Get from https://newsapi.org/
ECONOMIC_CALENDAR_API_KEY = ''  # Optional: For economic calendar data

# Data Source Configuration
PRIMARY_DATA_SOURCE = 'yahoo'  # 'yahoo' or 'alphavantage'
ENABLE_CACHING = True
CACHE_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30

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

# Update Intervals (seconds)
PRICE_UPDATE_INTERVAL = 5
SIGNAL_UPDATE_INTERVAL = 60
PORTFOLIO_UPDATE_INTERVAL = 300

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
