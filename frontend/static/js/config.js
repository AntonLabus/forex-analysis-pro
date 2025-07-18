/**
 * Configuration settings for Forex Analysis Pro
 */

const CONFIG = {
    // API endpoints
    API_BASE_URL: window.location.origin,
    WEBSOCKET_URL: window.location.origin,
    
    // API endpoints
    ENDPOINTS: {
        FOREX_PAIRS: '/api/forex/pairs',
        FOREX_DATA: '/api/forex/data',
        TECHNICAL_ANALYSIS: '/api/analysis/technical',
        FUNDAMENTAL_ANALYSIS: '/api/analysis/fundamental',
        SIGNALS: '/api/signals'
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
