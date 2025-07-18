/**
 * Main application logic for Forex Analysis Pro
 */

class ForexAnalysisApp {
    constructor() {
        this.socket = null;
        this.currentTab = 'dashboard';
        this.currencyData = new Map();
        this.analysisData = new Map();
        this.autoRefreshIntervals = new Map();
        
        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            // Initialize theme
            Utils.setTheme(Utils.getTheme());
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Initialize WebSocket connection
            this.initWebSocket();
            
            // Load initial data
            await this.loadInitialData();
            
            // Start auto-refresh intervals
            this.startAutoRefresh();
            
            console.log('Forex Analysis Pro initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            Utils.showNotification('Failed to initialize application', 'error');
        }
    }

    /**
     * Set up event listeners for UI interactions
     */
    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const tab = item.getAttribute('data-tab');
                this.switchTab(tab);
            });
        });

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = Utils.getTheme();
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                Utils.setTheme(newTheme);
                
                // Update chart theme
                if (window.chartManager) {
                    window.chartManager.updateTheme(newTheme);
                }
            });
        }

        // Analysis controls
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.performAnalysis());
        }

        // Chart indicator toggles
        document.querySelectorAll('.chart-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const indicator = btn.getAttribute('data-indicator');
                if (window.chartManager) {
                    window.chartManager.toggleIndicator(indicator);
                }
            });
        });

        // Signal controls
        const refreshSignalsBtn = document.getElementById('refresh-signals');
        if (refreshSignalsBtn) {
            refreshSignalsBtn.addEventListener('click', () => {
                if (window.signalManager) {
                    window.signalManager.refreshSignals();
                }
            });
        }

        // Signal filter
        const signalPairFilter = document.getElementById('signal-pair-filter');
        if (signalPairFilter) {
            signalPairFilter.addEventListener('change', (e) => {
                if (window.signalManager) {
                    window.signalManager.setFilters({ pair: e.target.value });
                }
            });
        }

        // Currency card clicks
        document.addEventListener('click', (e) => {
            const currencyCard = e.target.closest('.currency-card');
            if (currencyCard) {
                const pair = currencyCard.getAttribute('data-pair');
                if (pair) {
                    this.selectCurrencyPair(pair);
                }
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Window resize handler
        window.addEventListener('resize', Utils.debounce(() => {
            this.handleWindowResize();
        }, 250));
    }

    /**
     * Initialize WebSocket connection for real-time updates
     */
    initWebSocket() {
        try {
            this.socket = io(CONFIG.WEBSOCKET_URL);

            this.socket.on('connect', () => {
                console.log('WebSocket connected');
                this.updateConnectionStatus(true);
                
                // Subscribe to price updates for all pairs
                CONFIG.CURRENCY_PAIRS.forEach(pair => {
                    this.socket.emit('subscribe_pair', { pair: pair.symbol });
                });
            });

            this.socket.on('disconnect', () => {
                console.log('WebSocket disconnected');
                this.updateConnectionStatus(false);
            });

            this.socket.on('price_update', (data) => {
                this.handlePriceUpdate(data);
            });

            this.socket.on('signal_update', (data) => {
                this.handleSignalUpdate(data);
            });

            this.socket.on('status', (data) => {
                console.log('Status:', data.message);
            });

        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            this.updateConnectionStatus(false);
        }
    }

    /**
     * Load initial application data
     */
    async loadInitialData() {
        Utils.showLoading('Loading market data...');

        try {
            // Load currency pairs data
            await this.loadCurrencyPairs();
            
            // Load signals for all pairs
            if (window.signalManager) {
                await window.signalManager.fetchAllSignals();
            }
            
        } catch (error) {
            console.error('Failed to load initial data:', error);
            Utils.showNotification('Failed to load some data', 'warning');
        } finally {
            Utils.hideLoading();
        }
    }

    /**
     * Load currency pairs data
     */
    async loadCurrencyPairs() {
        try {
            const response = await Utils.request(`${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.FOREX_PAIRS}`);
            
            if (response.success) {
                response.data.forEach(pair => {
                    this.currencyData.set(pair.symbol, pair);
                });
                
                this.updateCurrencyGrid();
                this.updateLastUpdatedTime();
            } else {
                throw new Error(response.error || 'Failed to load currency pairs');
            }
        } catch (error) {
            console.error('Error loading currency pairs:', error);
            throw error;
        }
    }

    /**
     * Update currency grid display
     */
    updateCurrencyGrid() {
        const grid = document.getElementById('currency-grid');
        if (!grid) return;

        grid.innerHTML = '';

        CONFIG.CURRENCY_PAIRS.forEach(pairConfig => {
            const pairData = this.currencyData.get(pairConfig.symbol);
            const card = this.createCurrencyCard(pairConfig, pairData);
            grid.appendChild(card);
        });
    }

    /**
     * Create a currency card element
     * @param {Object} pairConfig - Pair configuration
     * @param {Object} pairData - Pair data
     * @returns {HTMLElement} Currency card element
     */
    createCurrencyCard(pairConfig, pairData) {
        const card = document.createElement('div');
        card.className = 'currency-card';
        card.setAttribute('data-pair', pairConfig.symbol);

        const price = pairData?.current_price || 0;
        const change = pairData?.daily_change || 0;
        const changePercent = pairData?.daily_change_percent || 0;
        
        // Get signal for this pair
        const signal = window.signalManager?.signals.get(pairConfig.symbol);
        const signalDirection = signal?.signal?.direction || 'HOLD';
        const signalConfidence = signal?.signal?.confidence || 0;

        const changeClass = change >= 0 ? 'positive' : 'negative';
        const signalClass = `signal-${signalDirection.toLowerCase()}`;

        card.innerHTML = `
            <div class="currency-header">
                <div class="currency-pair">${pairConfig.name}</div>
                <div class="currency-flag">
                    <span class="flag">${this.getCurrencyFlag(pairConfig.base)}</span>
                    <span class="flag">${this.getCurrencyFlag(pairConfig.quote)}</span>
                </div>
            </div>
            
            <div class="currency-price">${Utils.formatPrice(price, pairConfig.symbol)}</div>
            
            <div class="currency-change ${changeClass}">
                <i class="fas fa-${change >= 0 ? 'arrow-up' : 'arrow-down'}"></i>
                <span>${change >= 0 ? '+' : ''}${change.toFixed(4)}</span>
                <span>(${Utils.formatPercentage(changePercent / 100)})</span>
            </div>
            
            <div class="currency-signal ${signalClass}">
                <i class="fas fa-${this.getSignalIcon(signalDirection)}"></i>
                ${signalDirection} ${signalConfidence > 0 ? `(${signalConfidence.toFixed(0)}%)` : ''}
            </div>
        `;

        return card;
    }

    /**
     * Get currency flag emoji
     * @param {string} currency - Currency code
     * @returns {string} Flag emoji
     */
    getCurrencyFlag(currency) {
        const flags = {
            'USD': '🇺🇸', 'EUR': '🇪🇺', 'GBP': '🇬🇧', 'JPY': '🇯🇵',
            'CHF': '🇨🇭', 'AUD': '🇦🇺', 'CAD': '🇨🇦', 'NZD': '🇳🇿'
        };
        return flags[currency] || '🏳️';
    }

    /**
     * Get signal icon
     * @param {string} direction - Signal direction
     * @returns {string} Icon class
     */
    getSignalIcon(direction) {
        switch (direction) {
            case 'BUY': return 'arrow-up';
            case 'SELL': return 'arrow-down';
            default: return 'minus';
        }
    }

    /**
     * Switch between tabs
     * @param {string} tabName - Tab to switch to
     */
    switchTab(tabName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        document.getElementById(tabName)?.classList.add('active');

        this.currentTab = tabName;

        // Load tab-specific data
        this.loadTabData(tabName);
    }

    /**
     * Load data for specific tab
     * @param {string} tabName - Tab name
     */
    async loadTabData(tabName) {
        switch (tabName) {
            case 'signals':
                if (window.signalManager) {
                    await window.signalManager.fetchAllSignals();
                }
                break;
            case 'analysis':
                // Analysis tab loads data on demand
                break;
        }
    }

    /**
     * Perform analysis for selected pair and timeframe
     */
    async performAnalysis() {
        const pair = document.getElementById('analysis-pair')?.value;
        const timeframe = document.getElementById('analysis-timeframe')?.value;

        if (!pair || !timeframe) {
            Utils.showNotification('Please select a currency pair and timeframe', 'warning');
            return;
        }

        Utils.showLoading('Performing analysis...');

        try {
            console.log('Starting analysis for pair:', pair, 'timeframe:', timeframe);
            
            // Fetch price data
            const priceData = await this.fetchPriceData(pair, timeframe);
            console.log('Price data fetched:', priceData);
            
            // Fetch technical analysis
            const technicalAnalysis = await this.fetchTechnicalAnalysis(pair, timeframe);
            console.log('Technical analysis fetched:', technicalAnalysis);
            
            // Fetch fundamental analysis
            const fundamentalAnalysis = await this.fetchFundamentalAnalysis(pair);
            console.log('Fundamental analysis fetched:', fundamentalAnalysis);

            // Update chart
            if (window.chartManager && priceData) {
                console.log('Creating chart with chartManager and priceData available');
                window.chartManager.createChart(priceData, pair, timeframe);
            } else {
                console.warn('Chart not created - chartManager:', !!window.chartManager, 'priceData:', !!priceData);
            }

            // Update analysis results
            this.updateAnalysisResults(technicalAnalysis, fundamentalAnalysis);

        } catch (error) {
            console.error('Analysis failed:', error);
            Utils.showNotification('Analysis failed. Please try again.', 'error');
        } finally {
            Utils.hideLoading();
        }
    }

    /**
     * Fetch price data for analysis
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe
     * @returns {Promise<Array>} Price data
     */
    async fetchPriceData(pair, timeframe) {
        const response = await Utils.request(
            `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.FOREX_DATA}/${pair}?timeframe=${timeframe}&period=3mo`
        );

        if (response.success) {
            return response.data;
        } else {
            throw new Error(response.error || 'Failed to fetch price data');
        }
    }

    /**
     * Fetch technical analysis
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe
     * @returns {Promise<Object>} Technical analysis
     */
    async fetchTechnicalAnalysis(pair, timeframe) {
        const response = await Utils.request(
            `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.TECHNICAL_ANALYSIS}/${pair}?timeframe=${timeframe}`
        );

        if (response.success) {
            return response.analysis;
        } else {
            throw new Error(response.error || 'Failed to fetch technical analysis');
        }
    }

    /**
     * Fetch fundamental analysis
     * @param {string} pair - Currency pair
     * @returns {Promise<Object>} Fundamental analysis
     */
    async fetchFundamentalAnalysis(pair) {
        const response = await Utils.request(
            `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.FUNDAMENTAL_ANALYSIS}/${pair}`
        );

        if (response.success) {
            return response.analysis;
        } else {
            throw new Error(response.error || 'Failed to fetch fundamental analysis');
        }
    }

    /**
     * Update analysis results display
     * @param {Object} technical - Technical analysis
     * @param {Object} fundamental - Fundamental analysis
     */
    updateAnalysisResults(technical, fundamental) {
        this.updateTechnicalResults(technical);
        this.updateFundamentalResults(fundamental);
    }

    /**
     * Update technical analysis results
     * @param {Object} technical - Technical analysis data
     */
    updateTechnicalResults(technical) {
        const container = document.getElementById('technical-results');
        if (!container || !technical) return;

        const summary = technical.summary || {};
        
        container.innerHTML = `
            <div class="analysis-summary">
                <div class="summary-item">
                    <span class="summary-label">Overall Signal:</span>
                    <span class="summary-value ${summary.overall_signal?.toLowerCase() || ''}">${summary.overall_signal || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Confidence:</span>
                    <span class="summary-value">${summary.confidence || 0}%</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Bullish Signals:</span>
                    <span class="summary-value">${summary.bullish_signals || 0}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Bearish Signals:</span>
                    <span class="summary-value">${summary.bearish_signals || 0}</span>
                </div>
            </div>
            
            <div class="technical-details">
                ${this.renderTechnicalDetails(technical)}
            </div>
        `;
    }

    /**
     * Update fundamental analysis results
     * @param {Object} fundamental - Fundamental analysis data
     */
    updateFundamentalResults(fundamental) {
        const container = document.getElementById('fundamental-results');
        if (!container || !fundamental) return;

        const summary = fundamental.summary || {};
        
        container.innerHTML = `
            <div class="analysis-summary">
                <div class="summary-item">
                    <span class="summary-label">Overall Bias:</span>
                    <span class="summary-value ${summary.overall_bias?.toLowerCase() || ''}">${summary.overall_bias || 'N/A'}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Confidence:</span>
                    <span class="summary-value">${summary.confidence || 0}%</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Bullish Factors:</span>
                    <span class="summary-value">${summary.bullish_factors || 0}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Bearish Factors:</span>
                    <span class="summary-value">${summary.bearish_factors || 0}</span>
                </div>
            </div>
            
            <div class="fundamental-details">
                ${this.renderFundamentalDetails(fundamental)}
            </div>
        `;
    }

    /**
     * Handle real-time price updates
     * @param {Object} data - Price update data
     */
    handlePriceUpdate(data) {
        const { pair, price, timestamp } = data;
        
        // Update stored data
        const existingData = this.currencyData.get(pair) || {};
        this.currencyData.set(pair, {
            ...existingData,
            current_price: price,
            last_updated: timestamp
        });

        // Update UI
        this.updateCurrencyCard(pair);
        this.updateLastUpdatedTime();
    }

    /**
     * Handle real-time signal updates
     * @param {Object} data - Signal update data
     */
    handleSignalUpdate(data) {
        if (window.signalManager) {
            window.signalManager.signals.set(data.pair, data);
            window.signalManager.updateSignalDisplay();
            window.signalManager.updateQuickStats();
        }

        // Update currency card
        this.updateCurrencyCard(data.pair);
    }

    /**
     * Update a specific currency card
     * @param {string} pair - Currency pair
     */
    updateCurrencyCard(pair) {
        const card = document.querySelector(`[data-pair="${pair}"]`);
        if (!card) return;

        const pairConfig = CONFIG.CURRENCY_PAIRS.find(p => p.symbol === pair);
        const pairData = this.currencyData.get(pair);
        
        if (pairConfig && pairData) {
            const newCard = this.createCurrencyCard(pairConfig, pairData);
            card.replaceWith(newCard);
        }
    }

    /**
     * Update connection status indicator
     * @param {boolean} connected - Connection status
     */
    updateConnectionStatus(connected) {
        const status = document.getElementById('connection-status');
        if (!status) return;

        const icon = status.querySelector('i');
        const text = status.querySelector('span');

        if (connected) {
            status.className = 'connection-status connected';
            text.textContent = 'Connected';
        } else {
            status.className = 'connection-status disconnected';
            text.textContent = 'Disconnected';
        }
    }

    /**
     * Update last updated time
     */
    updateLastUpdatedTime() {
        const element = document.getElementById('last-updated-time');
        if (element) {
            element.textContent = new Date().toLocaleTimeString();
        }
    }

    /**
     * Select a currency pair (switch to analysis tab)
     * @param {string} pair - Currency pair
     */
    selectCurrencyPair(pair) {
        // Switch to analysis tab
        this.switchTab('analysis');
        
        // Set the selected pair
        const pairSelect = document.getElementById('analysis-pair');
        if (pairSelect) {
            pairSelect.value = pair;
        }
        
        // Optionally trigger analysis
        // this.performAnalysis();
    }

    /**
     * Start auto-refresh intervals
     */
    startAutoRefresh() {
        // Currency pairs data
        this.autoRefreshIntervals.set('currency-pairs', setInterval(() => {
            this.loadCurrencyPairs().catch(console.error);
        }, CONFIG.UPDATE_INTERVALS.PRICE_DATA));

        // Signals
        if (window.signalManager) {
            window.signalManager.startAutoRefresh();
        }
    }

    /**
     * Stop auto-refresh intervals
     */
    stopAutoRefresh() {
        this.autoRefreshIntervals.forEach((interval, key) => {
            clearInterval(interval);
        });
        this.autoRefreshIntervals.clear();

        if (window.signalManager) {
            window.signalManager.stopAutoRefresh();
        }
    }

    /**
     * Handle keyboard shortcuts
     * @param {KeyboardEvent} e - Keyboard event
     */
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + number keys for tab switching
        if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '3') {
            e.preventDefault();
            const tabs = ['dashboard', 'analysis', 'signals'];
            const tabIndex = parseInt(e.key) - 1;
            if (tabs[tabIndex]) {
                this.switchTab(tabs[tabIndex]);
            }
        }

        // Escape key to close modals
        if (e.key === 'Escape') {
            document.querySelectorAll('.signal-modal').forEach(modal => modal.remove());
        }
    }

    /**
     * Handle window resize
     */
    handleWindowResize() {
        // Redraw charts if visible
        if (this.currentTab === 'analysis' && window.chartManager?.currentChart) {
            const pair = document.getElementById('analysis-pair')?.value;
            const timeframe = document.getElementById('analysis-timeframe')?.value;
            if (pair && timeframe && window.chartManager.currentData) {
                window.chartManager.createChart(window.chartManager.currentData, pair, timeframe);
            }
        }
    }

    // Helper methods for rendering analysis details
    renderTechnicalDetails(technical) {
        let html = '';
        
        if (technical.trend_analysis) {
            html += `<h5>Trend Analysis</h5>`;
            html += `<p>Direction: ${technical.trend_analysis.direction}</p>`;
            html += `<p>Strength: ${technical.trend_analysis.strength}</p>`;
            if (technical.trend_analysis.sma_20) {
                html += `<p>SMA 20: ${technical.trend_analysis.sma_20.toFixed(5)}</p>`;
            }
        }
        
        if (technical.momentum_analysis) {
            html += `<h5>Momentum Analysis</h5>`;
            if (technical.momentum_analysis.rsi) {
                html += `<p>RSI: ${technical.momentum_analysis.rsi.value?.toFixed(2)} (${technical.momentum_analysis.rsi.signal})</p>`;
            }
            if (technical.momentum_analysis.macd) {
                html += `<p>MACD: ${technical.momentum_analysis.macd.value?.toFixed(5)} (${technical.momentum_analysis.macd.signal})</p>`;
            }
            if (technical.momentum_analysis.stochastic) {
                html += `<p>Stochastic: ${technical.momentum_analysis.stochastic.k?.toFixed(2)} (${technical.momentum_analysis.stochastic.signal})</p>`;
            }
        }
        
        if (technical.volatility_analysis) {
            html += `<h5>Volatility Analysis</h5>`;
            if (technical.volatility_analysis.volatility_percent) {
                html += `<p>Volatility: ${technical.volatility_analysis.volatility_percent.toFixed(2)}%</p>`;
            }
        }
        
        return html || '<p>No detailed technical data available</p>';
    }

    renderFundamentalDetails(fundamental) {
        let html = '';
        
        if (fundamental.interest_rate_analysis) {
            html += `<h5>Interest Rate Analysis</h5>`;
            html += `<p>Differential: ${fundamental.interest_rate_analysis.differential}%</p>`;
            html += `<p>Impact: ${fundamental.interest_rate_analysis.impact}</p>`;
        }
        
        if (fundamental.economic_calendar) {
            html += `<h5>Economic Events</h5>`;
            html += `<p>Upcoming Events: ${fundamental.economic_calendar.total_events}</p>`;
            html += `<p>High Impact: ${fundamental.economic_calendar.high_impact_count}</p>`;
        }
        
        return html || '<p>No detailed fundamental data available</p>';
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.forexApp = new ForexAnalysisApp();
    window.chartManager = new ChartManager();
    window.signalManager = new SignalManager();
    
    console.log('Application initialized with chartManager:', !!window.chartManager);
});
