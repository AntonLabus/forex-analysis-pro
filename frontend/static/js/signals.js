/**
 * Signal management for Forex Analysis Pro
 */

class SignalManager {
    constructor() {
        this.signals = new Map();
        this.signalHistory = [];
        this.currentFilterType = 'all'; // Track current filter type
        this.currentTimeframe = '1h'; // Track current timeframe
        this.filters = {
            pair: '',
            direction: '',
            confidence: 0
        };
        
        // Enhanced request management
        this.requestQueue = [];
        this.isProcessingQueue = false;
        this.maxConcurrentRequests = 3;
        this.activeRequests = 0;
        this.lastRequestTime = 0;
        this.minRequestInterval = 1000; // 1 second between requests
        
        // Request priority system
        this.priorityPairs = CONFIG.HIGH_PRIORITY_PAIRS || ['EURUSD', 'GBPUSD', 'USDJPY'];
        
        // Cache for signals to reduce API calls
        this.signalCache = new Map();
        this.cacheExpiry = new Map();
        this.defaultCacheTime = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Check if we have valid cached signal data
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe
     * @returns {Object|null} Cached signal data or null
     */
    getCachedSignal(pair, timeframe) {
        const cacheKey = `${pair}_${timeframe}`;
        const cached = this.signalCache.get(cacheKey);
        const expiry = this.cacheExpiry.get(cacheKey);
        
        if (cached && expiry && Date.now() < expiry) {
            console.log(`Using cached signal for ${pair} ${timeframe}`);
            return cached;
        }
        
        return null;
    }
    
    /**
     * Cache signal data
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe
     * @param {Object} data - Signal data
     */
    setCachedSignal(pair, timeframe, data) {
        const cacheKey = `${pair}_${timeframe}`;
        this.signalCache.set(cacheKey, data);
        this.cacheExpiry.set(cacheKey, Date.now() + this.defaultCacheTime);
        console.log(`Cached signal for ${pair} ${timeframe}`);
    }
    
    /**
     * Smart rate limiting - wait if necessary
     */
    async waitForRateLimit() {
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        
        if (timeSinceLastRequest < this.minRequestInterval) {
            const waitTime = this.minRequestInterval - timeSinceLastRequest;
            console.log(`Rate limiting: waiting ${waitTime}ms`);
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }
        
        this.lastRequestTime = Date.now();
    }

    /**
     * Fetch signals for a specific pair or all pairs with enhanced rate limiting
     * @param {string} pair - Currency pair (optional)
     * @returns {Promise} Signal data
     */
    async fetchSignals(pair = '') {
        try {
            // Check cache first for single pair requests
            if (pair) {
                const cached = this.getCachedSignal(pair, this.currentTimeframe);
                if (cached) {
                    this.signals.set(pair, cached);
                    this.updateSignalDisplay();
                    return { success: true, signals: cached };
                }
            }
            
            // Rate limiting
            await this.waitForRateLimit();
            
            const url = pair ? 
                `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.SIGNALS}/${pair}?timeframe=${this.currentTimeframe}` :
                `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.SIGNALS}/all?timeframe=${this.currentTimeframe}`;
            
            const response = await Utils.request(url);
            
            if (response.success) {
                if (pair) {
                    // Cache single pair response
                    this.setCachedSignal(pair, this.currentTimeframe, response.signals);
                    this.signals.set(pair, response.signals);
                } else {
                    // Handle multiple pairs - response.signals is an object with pair names as keys
                    for (const [pairName, signalData] of Object.entries(response.signals || {})) {
                        // Add the pair name to the signal data
                        signalData.pair = pairName;
                        signalData.timeframe = this.currentTimeframe;
                        
                        // Cache each pair's signal
                        this.setCachedSignal(pairName, this.currentTimeframe, signalData);
                        this.signals.set(pairName, signalData);
                    }
                }
                
                this.updateSignalDisplay();
                return response;
            } else {
                throw new Error(response.error || 'Failed to fetch signals');
            }
        } catch (error) {
            console.error('Error fetching signals:', error);
            Utils.showNotification('Failed to fetch signals', 'error');
            throw error;
        }
    }

    /**
     * Fetch signals for all currency pairs with smart batching and priority
     * @returns {Promise} All signals data
     */
    async fetchAllSignals() {
        try {
            // Check if we can use batch API endpoint
            const cached = this.getCachedSignal('ALL', this.currentTimeframe);
            if (cached) {
                console.log('Using cached batch signals');
                // Process cached batch data
                for (const [pairName, signalData] of Object.entries(cached)) {
                    signalData.pair = pairName;
                    signalData.timeframe = this.currentTimeframe;
                    this.signals.set(pairName, signalData);
                }
                this.updateSignalDisplay();
                this.updateQuickStats();
                return { success: true, signals: cached };
            }
            
            // Use batch endpoint for better efficiency
            await this.waitForRateLimit();
            
            const url = `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.SIGNALS}/all?timeframe=${this.currentTimeframe}`;
            const response = await Utils.request(url);
            
            if (response.success && response.signals) {
                // Cache the batch result
                this.setCachedSignal('ALL', this.currentTimeframe, response.signals);
                
                // Process batch response
                for (const [pairName, signalData] of Object.entries(response.signals)) {
                    signalData.pair = pairName;
                    signalData.timeframe = this.currentTimeframe;
                    this.signals.set(pairName, signalData);
                    
                    // Also cache individual pairs
                    this.setCachedSignal(pairName, this.currentTimeframe, signalData);
                }
                
                this.updateSignalDisplay();
                this.updateQuickStats();
                return response;
            } else {
                // Fallback to individual requests with priority ordering
                return await this.fetchSignalsWithPriority();
            }
        } catch (error) {
            console.error('Error fetching all signals:', error);
            Utils.showNotification('Failed to fetch some signals', 'warning');
            
            // Fallback to individual requests
            return await this.fetchSignalsWithPriority();
        }
    }
    
    /**
     * Fetch signals with priority ordering and rate limiting
     * @returns {Promise} Signals data
     */
    async fetchSignalsWithPriority() {
        const allPairs = CONFIG.CURRENCY_PAIRS.map(pair => pair.symbol);
        
        // Sort pairs by priority
        const prioritizedPairs = [
            ...this.priorityPairs.filter(pair => allPairs.includes(pair)),
            ...allPairs.filter(pair => !this.priorityPairs.includes(pair))
        ];
        
        const results = [];
        let successCount = 0;
        
        for (const pair of prioritizedPairs) {
            try {
                // Check cache first
                const cached = this.getCachedSignal(pair, this.currentTimeframe);
                if (cached) {
                    this.signals.set(pair, cached);
                    results.push({ status: 'fulfilled', value: cached });
                    successCount++;
                    continue;
                }
                
                // Rate limiting between individual requests
                await this.waitForRateLimit();
                
                const signalData = await this.fetchSignalForPair(pair);
                if (signalData) {
                    results.push({ status: 'fulfilled', value: signalData });
                    successCount++;
                } else {
                    results.push({ status: 'rejected', reason: `Failed to fetch ${pair}` });
                }
                
                // Give priority pairs more immediate processing
                if (!this.priorityPairs.includes(pair)) {
                    await new Promise(resolve => setTimeout(resolve, 500)); // Extra delay for low priority
                }
                
            } catch (error) {
                console.warn(`Failed to fetch signal for ${pair}:`, error);
                results.push({ status: 'rejected', reason: error.message });
            }
        }
        
        console.log(`Fetched ${successCount}/${prioritizedPairs.length} signals successfully`);
        
        this.updateSignalDisplay();
        this.updateQuickStats();
        return results;
    }

    /**
     * Fetch signal for a specific pair with timeframe
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe (optional, uses current if not provided)
     * @returns {Promise} Signal data
     */
    async fetchSignalForPair(pair, timeframe = null) {
        try {
            const selectedTimeframe = timeframe || this.currentTimeframe;
            const url = `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.SIGNALS}/${pair}?timeframe=${selectedTimeframe}`;
            const response = await Utils.request(url);
            
            if (response.success) {
                // Add the pair name and timeframe to the signal data
                response.signals.pair = pair;
                response.signals.timeframe = selectedTimeframe;
                this.signals.set(pair, response.signals);
                return response.signals;
            } else {
                throw new Error(response.error || 'Failed to fetch signal');
            }
        } catch (error) {
            console.error(`Error fetching signal for ${pair}:`, error);
            return null;
        }
    }

    /**
     * Update signals for a specific timeframe
     * @param {string} timeframe - New timeframe to use
     */
    async updateSignalsForTimeframe(timeframe) {
        console.log(`Updating signals for timeframe: ${timeframe}`);
        this.currentTimeframe = timeframe;
        
        // Clear existing signals
        this.signals.clear();
        
        // Show loading state
        const container = document.getElementById('signals-container');
        if (container) {
            container.innerHTML = '<div class="loading-placeholder"><i class="fas fa-spinner fa-spin"></i><span>Loading signals for ' + timeframe + '...</span></div>';
        }
        
        // Update signals display with timeframe indicator
        this.updateSignalsHeader();
        
        // Fetch new signals for current timeframe
        await this.fetchAllSignals();
        
        Utils.showNotification(`Signals updated for ${timeframe} timeframe`, 'info');
    }

    /**
     * Update signals header to show current timeframe
     */
    updateSignalsHeader() {
        const timeframeLabels = {
            '5m': '5 Minutes',
            '15m': '15 Minutes', 
            '30m': '30 Minutes',
            '1h': '1 Hour',
            '4h': '4 Hours',
            '1d': '1 Day'
        };
        
        // Find or create timeframe indicator
        let timeframeIndicator = document.querySelector('.signals-timeframe-indicator');
        const signalsContainer = document.getElementById('signals-container');
        
        if (!timeframeIndicator && signalsContainer) {
            timeframeIndicator = document.createElement('div');
            timeframeIndicator.className = 'signals-timeframe-indicator';
            signalsContainer.parentNode.insertBefore(timeframeIndicator, signalsContainer);
        }
        
        if (timeframeIndicator) {
            timeframeIndicator.innerHTML = `
                <div class="timeframe-indicator-content">
                    <i class="fas fa-clock"></i>
                    <span>Signals for ${timeframeLabels[this.currentTimeframe] || this.currentTimeframe}</span>
                </div>
            `;
        }
    }

    /**
     * Update the signal display in the UI
     */
    updateSignalDisplay() {
        const container = document.getElementById('signals-container');
        if (!container) return;

        // Clear existing signals
        container.innerHTML = '';

        // Get filtered signals
        const filteredSignals = this.getFilteredSignals();

        if (filteredSignals.length === 0) {
            this.showNoSignalsMessage(container);
            return;
        }

        // Create signal cards
        filteredSignals.forEach(signal => {
            const card = this.createSignalCard(signal);
            container.appendChild(card);
        });
    }

    /**
     * Get signals filtered by current filters
     * @returns {Array} Filtered signals
     */
    getFilteredSignals() {
        const allSignals = Array.from(this.signals.values()).filter(signal => signal);
        
        let filteredSignals = allSignals.filter(signal => {
            // Filter by pair
            if (this.filters.pair && signal.pair !== this.filters.pair) {
                return false;
            }
            
            // Filter by direction
            if (this.filters.direction && signal.signal?.direction !== this.filters.direction) {
                return false;
            }
            
            // Filter by minimum confidence
            if (this.filters.confidence > 0 && 
                (signal.signal?.confidence || 0) < this.filters.confidence) {
                return false;
            }
            
            return true;
        });

        // Sort by confidence if it's a confidence-based filter
        if (this.currentFilterType === 'confidence') {
            filteredSignals.sort((a, b) => {
                const confidenceA = a.signal?.confidence || 0;
                const confidenceB = b.signal?.confidence || 0;
                return confidenceB - confidenceA; // Highest confidence first
            });
        }

        return filteredSignals;
    }

    /**
     * Create a signal card element
     * @param {Object} signal - Signal data
     * @returns {HTMLElement} Signal card element
     */
    createSignalCard(signal) {
        const card = document.createElement('div');
        card.className = 'signal-card';
        card.setAttribute('data-pair', signal.pair);

        const direction = signal.signal?.direction || 'HOLD';
        const confidence = signal.signal?.confidence || 0;
        const strength = signal.signal?.strength || 0;
        
        const directionClass = direction.toLowerCase();
        const confidenceColor = Utils.getConfidenceColor(confidence);
        const signalColor = Utils.getSignalColor(direction);

        card.innerHTML = `
            <div class="signal-header">
                <div class="signal-pair">${signal.pair}</div>
                <div class="signal-time">${Utils.getRelativeTime(signal.timestamp)}</div>
            </div>
            
            <div class="signal-action">
                <div class="signal-direction ${directionClass}" style="background-color: ${signalColor}; color: white;">
                    ${direction}
                </div>
                <div class="signal-confidence">
                    <span class="confidence-text">${confidence.toFixed(1)}%</span>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidence}%; background-color: ${confidenceColor}"></div>
                    </div>
                </div>
            </div>

            ${this.renderSignalDetails(signal)}
            
            ${this.renderTradingLevels(signal.levels)}
            
            <div class="signal-summary">
                <div class="summary-text">${signal.summary?.recommendation || 'No recommendation available'}</div>
                ${signal.summary?.risk_warning ? `<div class="risk-warning">${signal.summary.risk_warning}</div>` : ''}
            </div>
        `;

        // Add click handler for more details
        card.addEventListener('click', () => this.showSignalDetails(signal));

        return card;
    }

    /**
     * Render signal details section
     * @param {Object} signal - Signal data
     * @returns {string} HTML string
     */
    renderSignalDetails(signal) {
        const technical = signal.technical_signal || {};
        const fundamental = signal.fundamental_signal || {};
        
        return `
            <div class="signal-details">
                <div class="analysis-breakdown">
                    <div class="analysis-item">
                        <span class="analysis-label">Technical:</span>
                        <span class="analysis-value ${technical.direction?.toLowerCase() || ''}">${technical.direction || 'N/A'}</span>
                        <span class="analysis-confidence">(${(technical.confidence || 0).toFixed(1)}%)</span>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-label">Fundamental:</span>
                        <span class="analysis-value ${fundamental.direction?.toLowerCase() || ''}">${fundamental.direction || 'N/A'}</span>
                        <span class="analysis-confidence">(${(fundamental.confidence || 0).toFixed(1)}%)</span>
                    </div>
                </div>
                
                <div class="signal-agreement">
                    <span class="agreement-label">Agreement:</span>
                    <span class="agreement-status ${signal.signal?.agreement ? 'positive' : 'negative'}">
                        ${signal.signal?.agreement ? 'Yes' : 'No'}
                    </span>
                </div>
            </div>
        `;
    }

    /**
     * Render trading levels section
     * @param {Object} levels - Trading levels data
     * @returns {string} HTML string
     */
    renderTradingLevels(levels) {
        if (!levels) return '';

        return `
            <div class="signal-levels">
                <div class="level-item">
                    <span class="level-label">Entry:</span>
                    <span class="level-value">${levels.entry || 'N/A'}</span>
                </div>
                <div class="level-item">
                    <span class="level-label">Stop Loss:</span>
                    <span class="level-value">${levels.stop_loss || 'N/A'}</span>
                </div>
                <div class="level-item">
                    <span class="level-label">Take Profit 1:</span>
                    <span class="level-value">${levels.take_profit_1 || 'N/A'}</span>
                </div>
                <div class="level-item">
                    <span class="level-label">Take Profit 2:</span>
                    <span class="level-value">${levels.take_profit_2 || 'N/A'}</span>
                </div>
                ${levels.risk_reward_ratio ? `
                <div class="level-item">
                    <span class="level-label">Risk/Reward:</span>
                    <span class="level-value">1:${levels.risk_reward_ratio}</span>
                </div>
                ` : ''}
            </div>
        `;
    }

    /**
     * Show detailed signal information in a modal or expanded view
     * @param {Object} signal - Signal data
     */
    showSignalDetails(signal) {
        // Create detailed signal view
        const modal = document.createElement('div');
        modal.className = 'signal-modal';
        modal.innerHTML = `
            <div class="signal-modal-content">
                <div class="signal-modal-header">
                    <h3>${signal.pair} - Signal Details</h3>
                    <button class="close-modal">&times;</button>
                </div>
                
                <div class="signal-modal-body">
                    ${this.renderDetailedSignalInfo(signal)}
                </div>
            </div>
        `;

        // Add modal styles and behavior
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        `;

        const content = modal.querySelector('.signal-modal-content');
        content.style.cssText = `
            background: var(--bg-primary);
            color: var(--text-primary);
            border-radius: 0.75rem;
            padding: 2rem;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        `;

        // Close modal functionality
        const closeBtn = modal.querySelector('.close-modal');
        closeBtn.addEventListener('click', () => modal.remove());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        document.body.appendChild(modal);
    }

    /**
     * Render detailed signal information
     * @param {Object} signal - Signal data
     * @returns {string} HTML string
     */
    renderDetailedSignalInfo(signal) {
        return `
            <div class="detailed-signal-info">
                <div class="signal-overview">
                    <h4>Signal Overview</h4>
                    <p><strong>Direction:</strong> ${signal.signal?.direction || 'N/A'}</p>
                    <p><strong>Confidence:</strong> ${(signal.signal?.confidence || 0).toFixed(1)}%</p>
                    <p><strong>Strength:</strong> ${(signal.signal?.strength || 0).toFixed(2)}</p>
                    <p><strong>Agreement:</strong> ${signal.signal?.agreement ? 'Yes' : 'No'}</p>
                </div>

                <div class="technical-breakdown">
                    <h4>Technical Analysis</h4>
                    ${this.renderTechnicalBreakdown(signal.technical_signal)}
                </div>

                <div class="fundamental-breakdown">
                    <h4>Fundamental Analysis</h4>
                    ${this.renderFundamentalBreakdown(signal.fundamental_signal)}
                </div>

                <div class="risk-management">
                    <h4>Risk Management</h4>
                    ${this.renderRiskManagement(signal.risk_metrics, signal.position_sizing)}
                </div>

                <div class="trading-plan">
                    <h4>Trading Plan</h4>
                    ${this.renderTradingPlan(signal.levels)}
                </div>
            </div>
        `;
    }

    /**
     * Update quick stats in the dashboard
     */
    updateQuickStats() {
        const signals = Array.from(this.signals.values()).filter(s => s);
        
        const totalSignals = signals.length;
        const bullishSignals = signals.filter(s => s.signal?.direction === 'BUY').length;
        const bearishSignals = signals.filter(s => s.signal?.direction === 'SELL').length;
        const avgConfidence = totalSignals > 0 ? 
            signals.reduce((sum, s) => sum + (s.signal?.confidence || 0), 0) / totalSignals : 0;

        // Update UI elements
        this.updateStatElement('total-signals', totalSignals);
        this.updateStatElement('bullish-signals', bullishSignals);
        this.updateStatElement('bearish-signals', bearishSignals);
        this.updateStatElement('avg-confidence', `${avgConfidence.toFixed(1)}%`);
    }

    /**
     * Update a stat element
     * @param {string} elementId - Element ID
     * @param {string|number} value - Value to display
     */
    updateStatElement(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    /**
     * Show no signals message
     * @param {HTMLElement} container - Container element
     */
    showNoSignalsMessage(container) {
        container.innerHTML = `
            <div class="no-signals-message">
                <div class="no-signals-icon">
                    <i class="fas fa-bell-slash"></i>
                </div>
                <div class="no-signals-text">
                    <h3>No signals available</h3>
                    <p>No trading signals match your current filters. Try adjusting the filters or check back later.</p>
                </div>
            </div>
        `;
    }

    /**
     * Set signal filters
     * @param {Object} filters - Filter object
     */
    setFilters(filters) {
        this.filters = { ...this.filters, ...filters };
        this.updateSignalDisplay();
    }

    /**
     * Clear all filters
     */
    clearFilters() {
        this.filters = { pair: '', direction: '', confidence: 0 };
        this.updateSignalDisplay();
    }

    /**
     * Start auto-refresh of signals
     * @param {number} interval - Refresh interval in milliseconds
     */
    startAutoRefresh(interval = CONFIG.UPDATE_INTERVALS.SIGNALS) {
        this.autoRefreshInterval = setInterval(() => {
            this.fetchAllSignals().catch(error => {
                console.error('Auto-refresh failed:', error);
            });
        }, interval);
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    /**
     * Manual refresh of all signals
     */
    async refreshSignals() {
        Utils.showLoading('Refreshing signals...');
        
        try {
            await this.fetchAllSignals();
            Utils.showNotification('Signals updated successfully', 'success');
        } catch (error) {
            Utils.showNotification('Failed to refresh signals', 'error');
        } finally {
            Utils.hideLoading();
        }
    }

    // Helper methods for detailed signal rendering
    renderTechnicalBreakdown(technical) {
        if (!technical) return '<p>No technical analysis available</p>';
        
        return `
            <p><strong>Direction:</strong> ${technical.direction || 'N/A'}</p>
            <p><strong>Confidence:</strong> ${(technical.confidence || 0).toFixed(1)}%</p>
            <p><strong>Strength:</strong> ${(technical.strength || 0).toFixed(2)}</p>
            <p><strong>Components:</strong> ${technical.components || 0}</p>
        `;
    }

    renderFundamentalBreakdown(fundamental) {
        if (!fundamental) return '<p>No fundamental analysis available</p>';
        
        return `
            <p><strong>Direction:</strong> ${fundamental.direction || 'N/A'}</p>
            <p><strong>Confidence:</strong> ${(fundamental.confidence || 0).toFixed(1)}%</p>
            <p><strong>Bias:</strong> ${fundamental.bias || 'N/A'}</p>
            <p><strong>Bullish Factors:</strong> ${fundamental.factors?.bullish || 0}</p>
            <p><strong>Bearish Factors:</strong> ${fundamental.factors?.bearish || 0}</p>
        `;
    }

    renderRiskManagement(riskMetrics, positionSizing) {
        let html = '<p>No risk management data available</p>';
        
        if (riskMetrics) {
            html = `
                <p><strong>Volatility:</strong> ${riskMetrics.volatility?.toFixed(2) || 'N/A'}%</p>
                <p><strong>Risk Level:</strong> ${riskMetrics.risk_level || 'N/A'}</p>
                <p><strong>ATR:</strong> ${riskMetrics.atr?.toFixed(5) || 'N/A'}</p>
            `;
        }
        
        if (positionSizing) {
            html += `
                <p><strong>Recommended Size:</strong> ${positionSizing.recommended_size_percent || 0}% of account</p>
                <p><strong>Notes:</strong> ${positionSizing.notes || 'N/A'}</p>
            `;
        }
        
        return html;
    }

    renderTradingPlan(levels) {
        if (!levels) return '<p>No trading levels available</p>';
        
        return `
            <p><strong>Entry:</strong> ${levels.entry || 'N/A'}</p>
            <p><strong>Stop Loss:</strong> ${levels.stop_loss || 'N/A'}</p>
            <p><strong>Take Profit 1:</strong> ${levels.take_profit_1 || 'N/A'}</p>
            <p><strong>Take Profit 2:</strong> ${levels.take_profit_2 || 'N/A'}</p>
            ${levels.risk_reward_ratio ? `<p><strong>Risk/Reward Ratio:</strong> 1:${levels.risk_reward_ratio}</p>` : ''}
        `;
    }

    /**
     * Apply filter to signals based on dashboard stats navigation
     * @param {string} filterType - Type of filter to apply
     */
    applyFilter(filterType) {
        // Reset current filters
        this.filters = {
            pair: '',
            direction: '',
            confidence: 0
        };

        // Store current filter type for sorting
        this.currentFilterType = filterType;

        // Apply specific filter based on type
        switch (filterType) {
            case 'all':
                // No additional filtering, show all signals
                break;
            case 'bullish':
                this.filters.direction = 'BUY';
                break;
            case 'bearish':
                this.filters.direction = 'SELL';
                break;
            case 'confidence':
                // Will be sorted in getFilteredSignals method
                break;
        }

        // Update the display with filtered results
        this.updateSignalDisplay();

        // Scroll to signals container
        const container = document.getElementById('signals-container');
        if (container) {
            container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Update filter indicator in UI if it exists
        this.updateFilterIndicator(filterType);
    }

    /**
     * Update filter indicator in the UI
     * @param {string} filterType - Active filter type
     */
    updateFilterIndicator(filterType) {
        // Remove existing filter indicators
        const existingIndicator = document.querySelector('.signals-filter-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }

        // Add new filter indicator if not showing all
        if (filterType !== 'all') {
            const signalsContainer = document.getElementById('signals-container');
            if (signalsContainer) {
                const indicator = document.createElement('div');
                indicator.className = 'signals-filter-indicator';
                
                const filterLabels = {
                    'bullish': 'Bullish Signals Only',
                    'bearish': 'Bearish Signals Only',
                    'confidence': 'Sorted by Confidence'
                };

                indicator.innerHTML = `
                    <div class="filter-indicator-content">
                        <i class="fas fa-filter"></i>
                        <span>${filterLabels[filterType]}</span>
                        <button class="clear-filter-btn" onclick="window.signalManager.applyFilter('all')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;

                signalsContainer.parentNode.insertBefore(indicator, signalsContainer);
            }
        }
    }
}

// Global signal manager instance
window.signalManager = new SignalManager();

// Initialize signals timeframe selector event listener
document.addEventListener('DOMContentLoaded', () => {
    const signalsTimeframeSelector = document.getElementById('signals-timeframe');
    if (signalsTimeframeSelector) {
        signalsTimeframeSelector.addEventListener('change', (event) => {
            const selectedTimeframe = event.target.value;
            console.log('Signals timeframe changed to:', selectedTimeframe);
            
            // Update the signal manager's current timeframe
            window.signalManager.currentTimeframe = selectedTimeframe;
            
            // Refresh signals with new timeframe
            window.signalManager.updateSignalsForTimeframe(selectedTimeframe);
        });
    }
});
