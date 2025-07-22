/**
 * Configuration settings for Forex Analysis Pro
 * Optimized for Netlify deployment with Render backend
 */

/**
 * Determine API base URL based on environment
 * @returns {string} API base URL
 */
const getApiBaseUrl = () => {
    // Runtime environment detection
    const hostname = window.location.hostname;
    
    // Development environment
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000';
    }
    
    // Production environment (Netlify deployment)
    return 'https://forex-analysis-pro.onrender.com';
};

const CONFIG = {
    // API endpoints
    API_BASE_URL: getApiBaseUrl(),
    WEBSOCKET_URL: getApiBaseUrl(),
    
    // API endpoints
    ENDPOINTS: {
        FOREX_PAIRS: '/api/forex/pairs',
        FOREX_DATA: '/api/forex/data',
        TECHNICAL_ANALYSIS: '/api/technical-analysis',
        FUNDAMENTAL_ANALYSIS: '/api/fundamental-analysis',
        SIGNALS_ALL: '/api/signals/all',
        SIGNALS_PAIR: '/api/signals'
    },
    
    // Currency pairs configuration
    CURRENCY_PAIRS: [
        { symbol: 'EURUSD', name: 'EUR/USD', base: 'EUR', quote: 'USD' },
        { symbol: 'GBPUSD', name: 'GBP/USD', base: 'GBP', quote: 'USD' },
        { symbol: 'USDJPY', name: 'USD/JPY', base: 'USD', quote: 'JPY' },
        { symbol: 'USDCHF', name: 'USD/CHF', base: 'USD', quote: 'CHF' },
        { symbol: 'AUDUSD', name: 'AUD/USD', base: 'AUD', quote: 'USD' },
        { symbol: 'USDCAD', name: 'USD/CAD', base: 'USD', quote: 'CAD' },
        { symbol: 'NZDUSD', name: 'NZD/USD', base: 'NZD', quote: 'USD' },
        { symbol: 'EURGBP', name: 'EUR/GBP', base: 'EUR', quote: 'GBP' }
    ],
    
    // Timeframes
    TIMEFRAMES: [
        { value: '1m', label: '1 Minute' },
        { value: '5m', label: '5 Minutes' },
        { value: '15m', label: '15 Minutes' },
        { value: '30m', label: '30 Minutes' },
        { value: '1h', label: '1 Hour' },
        { value: '4h', label: '4 Hours' },
        { value: '1d', label: '1 Day' },
        { value: '1wk', label: '1 Week' },
        { value: '1mo', label: '1 Month' }
    ],
    
    // Chart configuration
    CHART: {
        DEFAULT_HEIGHT: 500,
        THEME: {
            DARK: {
                background: '#0f172a',
                gridColor: '#334155',
                textColor: '#f8fafc'
            },
            LIGHT: {
                background: '#ffffff',
                gridColor: '#e2e8f0',
                textColor: '#1e293b'
            }
        },
        COLORS: {
            BULLISH: '#10b981',
            BEARISH: '#ef4444',
            VOLUME: '#64748b',
            MA: '#3b82f6',
            RSI: '#8b5cf6',
            MACD: '#f59e0b'
        }
    },
    
    // Signal thresholds
    SIGNALS: {
        CONFIDENCE_THRESHOLDS: {
            EXCELLENT: 80,
            GOOD: 65,
            FAIR: 50,
            POOR: 0
        },
        COLORS: {
            BUY: '#10b981',
            SELL: '#ef4444',
            HOLD: '#f59e0b'
        }
    },
    
    // Update intervals (in milliseconds)
    UPDATE_INTERVALS: {
        PRICE_DATA: 30000,      // 30 seconds
        SIGNALS: 60000,         // 1 minute
        ANALYSIS: 300000        // 5 minutes
    },
    
    // Notification settings
    NOTIFICATIONS: {
        DURATION: 5000,         // 5 seconds
        MAX_COUNT: 5
    },
    
    // Local storage keys
    STORAGE_KEYS: {
        THEME: 'forex_theme',
        WATCHLIST: 'forex_watchlist',
        SETTINGS: 'forex_settings'
    },
    
    // Error messages
    ERRORS: {
        NETWORK_ERROR: 'Network connection error. Please check your internet connection.',
        API_ERROR: 'API request failed. Please try again later.',
        DATA_ERROR: 'Unable to load data. Please refresh the page.',
        WEBSOCKET_ERROR: 'Real-time connection lost. Operating in polling mode.'
    }
};

// Environment-specific logging
if (CONFIG.API_BASE_URL.includes('localhost')) {
    console.log('🚀 Forex Analysis Pro - Development Mode');
    console.log('📡 API Base URL:', CONFIG.API_BASE_URL);
    console.log('🔌 WebSocket URL:', CONFIG.WEBSOCKET_URL);
} else {
    console.log('🚀 Forex Analysis Pro - Production Mode');
    console.log('📡 Connected to:', CONFIG.API_BASE_URL);
}

// Make CONFIG globally available
window.CONFIG = CONFIG;
    ERROR_MESSAGES: {
        NETWORK_ERROR: 'Network error. Please check your connection.',
        API_ERROR: 'Unable to fetch data. Please try again.',
        INVALID_PAIR: 'Invalid currency pair selected.',
        NO_DATA: 'No data available for the selected timeframe.'
    }
};

// Freeze the configuration to prevent accidental modifications
Object.freeze(CONFIG);
Object.freeze(CONFIG.CURRENCY_PAIRS);
Object.freeze(CONFIG.TIMEFRAMES);
Object.freeze(CONFIG.CHART);
Object.freeze(CONFIG.SIGNALS);
Object.freeze(CONFIG.UPDATE_INTERVALS);
Object.freeze(CONFIG.NOTIFICATIONS);
Object.freeze(CONFIG.STORAGE_KEYS);
Object.freeze(CONFIG.ERROR_MESSAGES);
