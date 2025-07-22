/**
 * Utility functions for Forex Analysis Pro
 */

class Utils {
    /**
     * Format a number as currency
     * @param {number} value - The value to format
     * @param {number} decimals - Number of decimal places
     * @param {string} currency - Currency symbol
     * @returns {string} Formatted currency string
     */
    static formatCurrency(value, decimals = 2, currency = '$') {
        if (typeof value !== 'number') return 'N/A';
        return `${currency}${value.toFixed(decimals)}`;
    }

    /**
     * Format a number as percentage
     * @param {number} value - The value to format (as decimal)
     * @param {number} decimals - Number of decimal places
     * @returns {string} Formatted percentage string
     */
    static formatPercentage(value, decimals = 2) {
        if (typeof value !== 'number') return 'N/A';
        const sign = value >= 0 ? '+' : '';
        return `${sign}${(value * 100).toFixed(decimals)}%`;
    }

    /**
     * Format a number with appropriate decimal places for forex
     * @param {number} value - The value to format
     * @param {string} pair - Currency pair for determining decimal places
     * @returns {string} Formatted price string
     */
    static formatPrice(value, pair = 'EURUSD') {
        if (typeof value !== 'number') return 'N/A';
        
        // JPY pairs typically have 2-3 decimal places, others have 4-5
        const decimals = pair.includes('JPY') ? 3 : 5;
        return value.toFixed(decimals);
    }

    /**
     * Format timestamp to readable date/time
     * @param {string|number} timestamp - ISO string or Unix timestamp
     * @param {boolean} includeTime - Whether to include time
     * @returns {string} Formatted date string
     */
    static formatDateTime(timestamp, includeTime = true) {
        if (!timestamp) return 'N/A';
        
        const date = new Date(timestamp);
        if (isNaN(date.getTime())) return 'Invalid Date';
        
        const options = {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        };
        
        if (includeTime) {
            options.hour = '2-digit';
            options.minute = '2-digit';
        }
        
        return date.toLocaleDateString('en-US', options);
    }

    /**
     * Get relative time (e.g., "2 minutes ago")
     * @param {string|number} timestamp - ISO string or Unix timestamp
     * @returns {string} Relative time string
     */
    static getRelativeTime(timestamp) {
        if (!timestamp) return 'Unknown';
        
        const date = new Date(timestamp);
        if (isNaN(date.getTime())) return 'Invalid Date';
        
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`;
        
        return this.formatDateTime(timestamp, false);
    }

    /**
     * Debounce function calls
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @returns {Function} Debounced function
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Throttle function calls
     * @param {Function} func - Function to throttle
     * @param {number} limit - Time limit in milliseconds
     * @returns {Function} Throttled function
     */
    static throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Make HTTP request with error handling
     * @param {string} url - Request URL
     * @param {Object} options - Fetch options
     * @returns {Promise} Response promise
     */
    static async request(url, options = {}) {
        try {
            console.log('Making request to:', url);
            
            const response = await fetch(url, {
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Response data:', data);
            return data;
        } catch (error) {
            console.error('Request failed:', error);
            console.error('URL:', url);
            console.error('Options:', options);
            throw error;
        }
    }

    /**
     * Show notification to user
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, warning, info)
     * @param {number} duration - Display duration in milliseconds
     */
    static showNotification(message, type = 'info', duration = CONFIG.NOTIFICATIONS.DURATION) {
        const container = document.getElementById('notification-container');
        if (!container) return;

        // Remove oldest notification if at max count
        const notifications = container.querySelectorAll('.notification');
        if (notifications.length >= CONFIG.NOTIFICATIONS.MAX_COUNT) {
            notifications[0].remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        container.appendChild(notification);

        // Auto remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }

    /**
     * Show loading overlay
     * @param {string} message - Loading message
     */
    static showLoading(message = 'Loading...') {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            const spinner = overlay.querySelector('.loading-spinner span');
            if (spinner) spinner.textContent = message;
            overlay.classList.add('show');
        }
    }

    /**
     * Hide loading overlay
     */
    static hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('show');
        }
    }

    /**
     * Get theme preference
     * @returns {string} Theme preference ('light' or 'dark')
     */
    static getTheme() {
        return localStorage.getItem(CONFIG.STORAGE_KEYS.THEME) || 'dark';
    }

    /**
     * Set theme preference
     * @param {string} theme - Theme to set ('light' or 'dark')
     */
    static setTheme(theme) {
        localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, theme);
        document.body.className = theme === 'dark' ? 'dark-theme' : '';
        
        // Update theme toggle icon
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    /**
     * Get watchlist from local storage
     * @returns {Array} Array of currency pairs
     */
    static getWatchlist() {
        const stored = localStorage.getItem(CONFIG.STORAGE_KEYS.WATCHLIST);
        return stored ? JSON.parse(stored) : [];
    }

    /**
     * Save watchlist to local storage
     * @param {Array} watchlist - Array of currency pairs
     */
    static saveWatchlist(watchlist) {
        localStorage.setItem(CONFIG.STORAGE_KEYS.WATCHLIST, JSON.stringify(watchlist));
    }

    /**
     * Add pair to watchlist
     * @param {string} pair - Currency pair to add
     */
    static addToWatchlist(pair) {
        const watchlist = this.getWatchlist();
        if (!watchlist.includes(pair)) {
            watchlist.push(pair);
            this.saveWatchlist(watchlist);
            this.showNotification(`${pair} added to watchlist`, 'success');
        }
    }

    /**
     * Remove pair from watchlist
     * @param {string} pair - Currency pair to remove
     */
    static removeFromWatchlist(pair) {
        let watchlist = this.getWatchlist();
        watchlist = watchlist.filter(p => p !== pair);
        this.saveWatchlist(watchlist);
        this.showNotification(`${pair} removed from watchlist`, 'info');
    }

    /**
     * Calculate confidence color based on value
     * @param {number} confidence - Confidence percentage (0-100)
     * @returns {string} CSS color value
     */
    static getConfidenceColor(confidence) {
        if (confidence >= CONFIG.SIGNALS.CONFIDENCE_THRESHOLDS.EXCELLENT) {
            return '#10b981'; // Green
        } else if (confidence >= CONFIG.SIGNALS.CONFIDENCE_THRESHOLDS.GOOD) {
            return '#3b82f6'; // Blue
        } else if (confidence >= CONFIG.SIGNALS.CONFIDENCE_THRESHOLDS.FAIR) {
            return '#f59e0b'; // Orange
        } else {
            return '#ef4444'; // Red
        }
    }

    /**
     * Get signal color based on direction
     * @param {string} direction - Signal direction (BUY, SELL, HOLD)
     * @returns {string} CSS color value
     */
    static getSignalColor(direction) {
        switch (direction?.toUpperCase()) {
            case 'BUY':
                return CONFIG.SIGNALS.COLORS.BUY;
            case 'SELL':
                return CONFIG.SIGNALS.COLORS.SELL;
            case 'HOLD':
            default:
                return CONFIG.SIGNALS.COLORS.HOLD;
        }
    }

    /**
     * Validate currency pair format
     * @param {string} pair - Currency pair to validate
     * @returns {boolean} True if valid
     */
    static isValidCurrencyPair(pair) {
        if (!pair || typeof pair !== 'string') return false;
        return CONFIG.CURRENCY_PAIRS.some(p => p.symbol === pair.toUpperCase());
    }

    /**
     * Get currency pair information
     * @param {string} symbol - Currency pair symbol
     * @returns {Object|null} Currency pair object or null
     */
    static getCurrencyPairInfo(symbol) {
        return CONFIG.CURRENCY_PAIRS.find(p => p.symbol === symbol.toUpperCase()) || null;
    }

    /**
     * Calculate pip value for a currency pair
     * @param {string} pair - Currency pair
     * @param {number} price1 - First price
     * @param {number} price2 - Second price
     * @returns {number} Pip difference
     */
    static calculatePips(pair, price1, price2) {
        if (!pair || typeof price1 !== 'number' || typeof price2 !== 'number') {
            return 0;
        }
        
        const multiplier = pair.includes('JPY') ? 100 : 10000;
        return Math.round((price2 - price1) * multiplier);
    }

    /**
     * Escape HTML to prevent XSS
     * @param {string} unsafe - Unsafe HTML string
     * @returns {string} Safe HTML string
     */
    static escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    /**
     * Deep clone an object
     * @param {any} obj - Object to clone
     * @returns {any} Cloned object
     */
    static deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => this.deepClone(item));
        
        const cloned = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                cloned[key] = this.deepClone(obj[key]);
            }
        }
        return cloned;
    }

    /**
     * Check if device is mobile
     * @returns {boolean} True if mobile device
     */
    static isMobile() {
        return window.innerWidth <= 768;
    }

    /**
     * Get URL parameters
     * @param {string} param - Parameter name
     * @returns {string|null} Parameter value or null
     */
    static getUrlParameter(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    /**
     * Set URL parameter without page reload
     * @param {string} param - Parameter name
     * @param {string} value - Parameter value
     */
    static setUrlParameter(param, value) {
        const url = new URL(window.location);
        if (value) {
            url.searchParams.set(param, value);
        } else {
            url.searchParams.delete(param);
        }
        window.history.replaceState({}, '', url);
    }
}
