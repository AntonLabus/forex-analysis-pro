/**
 * Main application logic for Forex Analysis Pro
 */

// Global market type variable
let MARKET_TYPE = 'forex';

// Test function to verify onclick handlers work
window.testClick = function() {
    console.log('Test click function works!');
    alert('JavaScript is working!');
};

// Global function to set market type
function setMarketType(type) {
    console.log('=== setMarketType called with:', type, '===');
    console.log('Current MARKET_TYPE before change:', MARKET_TYPE);
    
    MARKET_TYPE = type;
    
    // Update button states
    const forexBtn = document.getElementById('forex-btn');
    const cryptoBtn = document.getElementById('crypto-btn');
    
    console.log('Found forex button:', !!forexBtn);
    console.log('Found crypto button:', !!cryptoBtn);
    
    if (forexBtn) forexBtn.classList.toggle('active', type === 'forex');
    if (cryptoBtn) cryptoBtn.classList.toggle('active', type === 'crypto');
    
    console.log('Button states updated');
    
    // Update dropdown options based on market type
    updatePairDropdowns(type);
    
    // Clear existing currency data to force refresh
    if (window.app && window.app.currencyData) {
        console.log('Clearing existing currency data');
        window.app.currencyData.clear();
        
        // Clear any cached requests
        if ('caches' in window) {
            caches.keys().then(names => {
                names.forEach(name => {
                    if (name.includes('api')) {
                        caches.delete(name);
                    }
                });
            });
        }
        
        // Show loading state immediately
        const grid = document.getElementById('currency-grid');
        if (grid) {
            grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-secondary);">
                <i class="fas fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>Loading ${type} pairs...</p>
                <p style="font-size: 0.9em; color: #888;">Switching from ${MARKET_TYPE === 'forex' ? 'crypto' : 'forex'} to ${type}</p>
            </div>`;
        }
    }
    
    // Refresh all data with new market type
    if (window.app) {
        console.log('Calling app.refreshAllData()');
        window.app.refreshAllData();
        
        // Re-subscribe to WebSocket updates for new market type
        if (window.app.socket && window.app.socket.connected) {
            console.log('Re-subscribing to WebSocket for market type:', type);
            window.app.subscribeToMarketUpdates();
        }
        
        // Also refresh the analysis section if we're on that tab
        const analysisSection = document.getElementById('analysis');
        if (analysisSection && analysisSection.classList.contains('active')) {
            console.log('Refreshing analysis section for new market type');
            setTimeout(() => {
                // Trigger analysis update for the first pair of new market type
                const analysisPairSelect = document.getElementById('analysis-pair');
                if (analysisPairSelect && analysisPairSelect.options.length > 0) {
                    // Update chart title
                    const chartTitle = document.getElementById('chart-title');
                    if (chartTitle) {
                        const selectedPair = analysisPairSelect.value;
                        const selectedLabel = analysisPairSelect.options[analysisPairSelect.selectedIndex].text;
                        chartTitle.textContent = `${selectedLabel} - 1 Hour Chart`;
                    }
                }
            }, 100);
        }
    } else {
        console.log('window.app not available');
    }
    
    // Update other parts of the app
    if (window.signalManager) {
        console.log('Calling signalManager.loadSignals()');
        window.signalManager.loadSignals();
    } else {
        console.log('window.signalManager not available');
    }
    
    console.log('Market type set to:', type);
    console.log('=== setMarketType completed ===');
}

/**
 * Test WebSocket connection function for debugging
 */
function testWebSocket() {
    console.log('=== WEBSOCKET CONNECTION TEST ===');
    
    if (!window.app) {
        console.log('❌ window.app not available');
        alert('App not initialized');
        return;
    }
    
    if (!window.app.socket) {
        console.log('❌ Socket not initialized');
        alert('WebSocket not initialized');
        return;
    }
    
    console.log('Socket object:', window.app.socket);
    console.log('Socket connected:', window.app.socket.connected);
    console.log('Socket id:', window.app.socket.id);
    console.log('Socket transport:', window.app.socket.io?.engine?.transport?.name);
    
    if (window.app.socket.connected) {
        console.log('✅ WebSocket is connected!');
        window.app.updateConnectionStatus(true, 'Connected (Test)');
        alert('WebSocket is CONNECTED ✅');
    } else {
        console.log('❌ WebSocket is NOT connected');
        window.app.updateConnectionStatus(false, 'Disconnected (Test)');
        alert('WebSocket is DISCONNECTED ❌');
        
        // Try to reconnect
        console.log('Attempting to reconnect...');
        window.app.socket.connect();
    }
}

/**
 * Test API connection and crypto pairs
 */
function testCrypto() {
    console.log('=== CRYPTO API TEST ===');
    
    // Test the API directly
    const testUrl = `${CONFIG.API_BASE_URL}/api/forex/pairs?market_type=crypto&force_refresh=true&_t=${Date.now()}`;
    console.log('Testing URL:', testUrl);
    
    fetch(testUrl)
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            return response.json();
        })
        .then(data => {
            console.log('✅ API Response:', data);
            console.log('Market type returned:', data.market_type);
            console.log('Pairs count:', data.data?.length);
            console.log('First few pairs:', data.data?.slice(0, 5).map(p => p.symbol));
            
            if (data.market_type === 'crypto') {
                alert(`✅ SUCCESS: Got ${data.data?.length} crypto pairs!`);
            } else {
                alert(`❌ WRONG DATA: Got ${data.market_type} instead of crypto`);
            }
        })
        .catch(error => {
            console.error('❌ API Error:', error);
            alert(`❌ API Error: ${error.message}`);
        });
}

// Function to update pair dropdowns based on market type
function updatePairDropdowns(marketType) {
    console.log('Updating pair dropdowns for market type:', marketType);
    
    const forexPairs = [
        { value: 'EURUSD', label: 'EUR/USD' },
        { value: 'GBPUSD', label: 'GBP/USD' },
        { value: 'USDJPY', label: 'USD/JPY' },
        { value: 'USDCHF', label: 'USD/CHF' },
        { value: 'AUDUSD', label: 'AUD/USD' },
        { value: 'USDCAD', label: 'USD/CAD' },
        { value: 'NZDUSD', label: 'NZD/USD' },
        { value: 'EURGBP', label: 'EUR/GBP' }
    ];
    
    const cryptoPairs = [
        { value: 'BTCUSD', label: 'BTC/USD' },
        { value: 'ETHUSD', label: 'ETH/USD' },
        { value: 'BNBUSD', label: 'BNB/USD' },
        { value: 'SOLUSD', label: 'SOL/USD' },
        { value: 'XRPUSD', label: 'XRP/USD' },
        { value: 'ADAUSD', label: 'ADA/USD' },
        { value: 'DOGEUSD', label: 'DOGE/USD' },
        { value: 'DOTUSD', label: 'DOT/USD' },
        { value: 'LTCUSD', label: 'LTC/USD' },
        { value: 'BCHUSD', label: 'BCH/USD' },
        { value: 'AVAXUSD', label: 'AVAX/USD' },
        { value: 'SHIBUSD', label: 'SHIB/USD' }
    ];
    
    const pairs = marketType === 'crypto' ? cryptoPairs : forexPairs;
    
    // Update analysis pair dropdown
    const analysisPairSelect = document.getElementById('analysis-pair');
    if (analysisPairSelect) {
        analysisPairSelect.innerHTML = '';
        pairs.forEach(pair => {
            const option = document.createElement('option');
            option.value = pair.value;
            option.textContent = pair.label;
            analysisPairSelect.appendChild(option);
        });
        console.log('Updated analysis pair dropdown with', pairs.length, 'pairs');
    }
    
    // Update signal pair filter dropdown
    const signalPairFilter = document.getElementById('signal-pair-filter');
    if (signalPairFilter) {
        signalPairFilter.innerHTML = '<option value="">All Pairs</option>';
        pairs.forEach(pair => {
            const option = document.createElement('option');
            option.value = pair.value;
            option.textContent = pair.label;
            signalPairFilter.appendChild(option);
        });
        console.log('Updated signal pair filter dropdown with', pairs.length, 'pairs');
    }
    
    // Update chart title to reflect the first pair of the new market type
    const chartTitle = document.getElementById('chart-title');
    if (chartTitle && pairs.length > 0) {
        const firstPair = pairs[0];
        chartTitle.textContent = `${firstPair.label} - 1 Hour Chart`;
        console.log('Updated chart title to:', firstPair.label);
    }
}

// Ensure the function is available globally
window.setMarketType = setMarketType;

class ForexAnalysisApp {
    constructor() {
        this.socket = null;
        this.currentTab = 'dashboard';
        this.currencyData = new Map();
        this.analysisData = new Map();
        this.autoRefreshIntervals = new Map();
        this.fallbackUpdateInterval = null;
        
        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            // Initialize theme
            Utils.setTheme(Utils.getTheme());
            
            // Initialize debug panel (hidden by default)
            this.initDebugPanel();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Initialize WebSocket connection
            this.initWebSocket();
            
            // Handle URL hash navigation
            this.handleUrlHash();
            
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
     * Initialize debug panel
     */
    initDebugPanel() {
        const debugPanel = document.getElementById('debug-panel');
        const debugToggle = document.getElementById('debug-toggle');
        
        if (debugPanel) {
            // Hide debug panel by default
            debugPanel.classList.remove('visible');
        }
        
        if (debugToggle) {
            debugToggle.classList.remove('active');
            debugToggle.setAttribute('aria-label', 'Show debug panel');
        }
        
        console.log('Debug panel initialized (hidden by default)');
    }

    /**
     * Set up event listeners for UI interactions
     */
    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const navMenu = document.getElementById('nav-menu');
        
        if (mobileMenuToggle && navMenu) {
            mobileMenuToggle.addEventListener('click', () => {
                mobileMenuToggle.classList.toggle('active');
                navMenu.classList.toggle('active');
            });
            
            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!mobileMenuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                    mobileMenuToggle.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            });
            
            // Close mobile menu when selecting a tab
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', () => {
                    mobileMenuToggle.classList.remove('active');
                    navMenu.classList.remove('active');
                });
            });
        }
        
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

        // Main refresh button
        const refreshBtn = document.querySelector('.refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.refreshAllData();
            });
        }

        // Make refresh function globally available for inline onclick handlers
        window.forceRefreshData = () => this.refreshAllData();

        // Make debug panel toggle function globally available
        window.toggleDebugPanel = () => this.toggleDebugPanel();

        // Make navigation function globally available for stat cards
        window.navigateToSignals = (filterType) => {
            console.log('navigateToSignals called with filterType:', filterType);
            
            // Switch to signals tab
            this.switchTab('signals');
            
            // Apply filter if signal manager exists
            if (window.signalManager && typeof window.signalManager.applyFilter === 'function') {
                setTimeout(() => {
                    console.log('Applying filter:', filterType);
                    window.signalManager.applyFilter(filterType);
                }, 100);
            } else {
                console.warn('signalManager not available or applyFilter method missing');
            }
            
            // Show notification about the filter
            const filterMessages = {
                'all': 'Showing all active signals',
                'bullish': 'Showing bullish signals only',
                'bearish': 'Showing bearish signals only',
                'confidence': 'Signals sorted by confidence level'
            };
            
            Utils.showNotification(filterMessages[filterType] || 'Viewing signals', 'info');
        };

        // Analysis controls
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => this.performAnalysis());
        }

        // Timeframe selector for signal updates
        const timeframeSelector = document.getElementById('analysis-timeframe');
        if (timeframeSelector) {
            timeframeSelector.addEventListener('change', (e) => {
                const newTimeframe = e.target.value;
                console.log('Timeframe changed to:', newTimeframe);
                
                // Update signals if on signals tab
                if (this.currentTab === 'signals' && window.signalManager) {
                    window.signalManager.updateSignalsForTimeframe(newTimeframe);
                }
                
                // Store timeframe for future signal updates
                if (window.signalManager) {
                    window.signalManager.currentTimeframe = newTimeframe;
                }
            });
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
            refreshSignalsBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                
                // Show loading state
                const originalText = refreshSignalsBtn.innerHTML;
                refreshSignalsBtn.disabled = true;
                refreshSignalsBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
                
                try {
                    if (window.signalManager) {
                        await window.signalManager.fetchAllSignals();
                        Utils.showNotification('Signals refreshed successfully', 'success');
                    }
                } catch (error) {
                    console.error('Failed to refresh signals:', error);
                    Utils.showNotification('Failed to refresh signals', 'error');
                } finally {
                    // Restore button
                    refreshSignalsBtn.disabled = false;
                    refreshSignalsBtn.innerHTML = originalText;
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
            // Skip WebSocket for now if Socket.io is not available
            if (typeof io === 'undefined') {
                console.warn('Socket.io not available, skipping WebSocket connection');
                this.updateConnectionStatus(false);
                return;
            }

            console.log('Initializing WebSocket connection to:', CONFIG.WEBSOCKET_URL);
            
            // Start with fallback updates immediately, then try WebSocket
            this.startFallbackUpdates();
            
            // Enhanced WebSocket configuration for real-time data
            this.socket = io(CONFIG.WEBSOCKET_URL, {
                timeout: 20000,  // Longer timeout for connection
                reconnection: true,
                reconnectionAttempts: 10,  // More attempts
                reconnectionDelay: 2000,  // Shorter delay between attempts
                transports: ['websocket', 'polling'],  // Try WebSocket first, fallback to polling
                upgrade: true,  // Allow upgrade to WebSocket
                forceNew: true,
                autoConnect: true
            });

            this.socket.on('connect', () => {
                console.log('WebSocket connected successfully to:', CONFIG.WEBSOCKET_URL);
                console.log('Transport used:', this.socket.io.engine.transport.name);
                this.updateConnectionStatus(true);
                
                // Stop fallback updates since WebSocket is now connected
                this.stopFallbackUpdates();
                
                // Subscribe to price updates for current market type
                this.subscribeToMarketUpdates();
            });

            this.socket.on('disconnect', (reason) => {
                console.warn('❌ WebSocket disconnected:', reason);
                this.updateConnectionStatus(false, `Disconnected: ${reason}`);
                
                // Restart fallback updates when WebSocket disconnects
                this.startFallbackUpdates();
            });

            this.socket.on('connect_error', (error) => {
                console.error('❌ WebSocket connection error:', error);
                console.error('Error details:', error.message);
                this.updateConnectionStatus(false, `Connection Error: ${error.message}`);
                
                // If WebSocket fails, continue with polling-only updates
                if (!this.fallbackUpdateInterval) {
                    this.startFallbackUpdates();
                }
            });

            this.socket.on('reconnect', (attemptNumber) => {
                console.log('WebSocket reconnected after', attemptNumber, 'attempts');
                console.log('Transport used:', this.socket.io.engine.transport.name);
                this.updateConnectionStatus(true);
                this.subscribeToMarketUpdates();
            });

            this.socket.on('reconnect_error', (error) => {
                console.warn('WebSocket reconnection failed:', error);
            });

            this.socket.on('price_update', (data) => {
                this.handlePriceUpdate(data);
            });

            this.socket.on('signal_update', (data) => {
                this.handleSignalUpdate(data);
            });

            this.socket.on('status', (data) => {
                console.log('WebSocket status:', data.message);
            });

            this.socket.on('subscription_confirmed', (data) => {
                console.log('Pair subscription confirmed:', data.pair);
            });

            this.socket.on('market_subscription_confirmed', (data) => {
                console.log('Market subscription confirmed:', data.market_type);
            });

            // Add immediate connection test
            this.socket.on('connect', () => {
                console.log('✅ WebSocket connect event fired!');
                // Force update the display to ensure it shows connected
                setTimeout(() => {
                    if (this.socket && this.socket.connected) {
                        console.log('✅ Confirming connection status...');
                        this.updateConnectionStatus(true);
                    }
                }, 100);
            });

            // Shorter timeout since we already started fallback updates
            setTimeout(() => {
                if (!this.socket || !this.socket.connected) {
                    console.log('WebSocket connection timeout - continuing with polling mode');
                    this.updateConnectionStatus(false, 'Using polling mode');
                }
            }, 15000);  // Reduced from 30 to 15 seconds

        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            this.updateConnectionStatus(false);
            this.startFallbackUpdates();
        }
    }

    /**
     * Start fallback polling updates when WebSocket is not available
     */
    startFallbackUpdates() {
        if (this.fallbackUpdateInterval) {
            return; // Already running
        }

        console.log('Starting fallback polling updates...');
        this.updateConnectionStatus(false, 'Using polling updates');
        
        // Update data every 30 seconds via REST API
        this.fallbackUpdateInterval = setInterval(async () => {
            try {
                console.log('Fallback update: refreshing data...');
                await this.loadCurrencyPairs();
                
                if (window.signalManager) {
                    await window.signalManager.fetchAllSignals();
                }
            } catch (error) {
                console.error('Fallback update failed:', error);
            }
        }, 30000);
    }

    /**
     * Stop fallback updates
     */
    stopFallbackUpdates() {
        if (this.fallbackUpdateInterval) {
            clearInterval(this.fallbackUpdateInterval);
            this.fallbackUpdateInterval = null;
            console.log('Fallback polling updates stopped');
        }
    }

    /**
     * Subscribe to price updates for current market type
     */
    subscribeToMarketUpdates() {
        if (!this.socket || !this.socket.connected) {
            console.warn('Cannot subscribe to market updates - socket not connected');
            return;
        }

        console.log('Subscribing to price updates for market type:', MARKET_TYPE);
        
        // Subscribe to market type updates
        this.socket.emit('subscribe_market', { market_type: MARKET_TYPE });
        
        // Also subscribe to specific pairs based on current market
        if (MARKET_TYPE === 'crypto') {
            // Subscribe to major crypto pairs
            const cryptoPairs = ['BTCUSD', 'ETHUSD', 'ADAUSD', 'DOTUSD', 'LINKUSD'];
            cryptoPairs.forEach(pair => {
                this.socket.emit('subscribe_pair', { pair: pair });
            });
        } else {
            // Subscribe to major forex pairs
            const forexPairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD'];
            forexPairs.forEach(pair => {
                this.socket.emit('subscribe_pair', { pair: pair });
            });
        }
    }

    /**
     * Load initial application data
     */
    async loadInitialData() {
        console.log('Loading initial application data...');
        Utils.showLoading('Loading market data...');

        try {
            console.log('Starting to load initial data...');
            
            // Try to load data with timeout
            const loadPromise = this.loadDataWithRetry();
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Loading timeout - backend may be cold starting')), 45000)
            );
            
            await Promise.race([loadPromise, timeoutPromise]);
            
            // Update last refresh time
            this.updateLastRefreshTime();
            
            console.log('Initial data loaded successfully');
            Utils.showNotification('Market data loaded successfully', 'success');
            
        } catch (error) {
            console.error('Failed to load initial data:', error);
            
            if (error.message.includes('timeout')) {
                Utils.showNotification('Backend is starting up (this can take 30-60 seconds). Please wait and try refreshing.', 'warning');
                this.showFallbackData();
            } else {
                Utils.showNotification('Some data could not be loaded. The app will continue with limited functionality.', 'warning');
            }
        } finally {
            Utils.hideLoading();
        }
    }

    /**
     * Load data with retry mechanism
     */
    async loadDataWithRetry() {
        let attempts = 0;
        const maxAttempts = 3;
        
        while (attempts < maxAttempts) {
            try {
                console.log(`Data loading attempt ${attempts + 1}/${maxAttempts}`);
                
                // Load currency pairs data first
                await this.loadCurrencyPairs();
                
                // Load signals for all pairs
                if (window.signalManager) {
                    console.log('Loading initial signals...');
                    await window.signalManager.fetchAllSignals();
                }
                
                return; // Success
                
            } catch (error) {
                attempts++;
                console.warn(`Attempt ${attempts} failed:`, error.message);
                
                if (attempts < maxAttempts) {
                    console.log(`Retrying in ${attempts * 2} seconds...`);
                    await new Promise(resolve => setTimeout(resolve, attempts * 2000));
                } else {
                    throw error;
                }
            }
        }
    }

    /**
     * Show fallback data when API is unavailable
     */
    showFallbackData() {
        console.log('Showing fallback data while backend starts up...');
        
        const grid = document.getElementById('currency-grid');
        if (grid) {
            grid.innerHTML = `
                <div class="fallback-message" style="grid-column: 1 / -1; text-align: center; padding: 40px; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border: 1px dashed #3b82f6;">
                    <i class="fas fa-cloud" style="font-size: 48px; color: #3b82f6; margin-bottom: 16px;"></i>
                    <h3 style="color: #3b82f6; margin-bottom: 8px;">Backend Starting Up</h3>
                    <p style="color: #94a3b8; margin-bottom: 16px;">
                        The Render backend is currently starting up. This can take 30-60 seconds for the first request.
                    </p>
                    <button onclick="window.app.refreshAllData()" style="background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer;">
                        <i class="fas fa-sync-alt"></i> Try Again
                    </button>
                </div>
            `;
        }
        
        // Update connection status
        this.updateConnectionStatus(false, 'Backend starting...');
    }

    /**
     * Refresh all application data (for manual refresh button)
     */
    async refreshAllData() {
        console.log('Manually refreshing all data...');
        
        // Show loading state on refresh button
        const refreshBtn = document.querySelector('.refresh-btn');
        const refreshIcon = refreshBtn?.querySelector('i');
        const originalText = refreshBtn?.textContent;
        
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        }

        try {
            // Show loading for currency pairs grid
            const loadingPlaceholder = document.querySelector('.loading-placeholder');
            if (loadingPlaceholder) {
                loadingPlaceholder.style.display = 'flex';
            }
            
            console.log('Refreshing currency pairs...');
            await this.loadCurrencyPairs();
            
            // Refresh signals
            if (window.signalManager) {
                console.log('Refreshing signals via signalManager...');
                await window.signalManager.fetchAllSignals();
            }
            
            // Update last refresh time
            this.updateLastRefreshTime();
            
            console.log('Data refresh completed successfully');
            Utils.showNotification('Data refreshed successfully', 'success');
            
        } catch (error) {
            console.error('Data refresh failed:', error);
            Utils.showNotification('Failed to refresh data. Please try again.', 'error');
        } finally {
            // Restore refresh button
            if (refreshBtn) {
                refreshBtn.disabled = false;
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Data';
            }
            
            // Hide loading placeholder
            const loadingPlaceholder = document.querySelector('.loading-placeholder');
            if (loadingPlaceholder) {
                loadingPlaceholder.style.display = 'none';
            }
        }
    }

    /**
     * Update the last refresh time display
     */
    updateLastRefreshTime() {
        const lastUpdatedElement = document.getElementById('last-updated-time');
        if (lastUpdatedElement) {
            const now = new Date();
            lastUpdatedElement.textContent = now.toLocaleTimeString();
        }
    }

    /**
     * Load currency pairs data
     */
    async loadCurrencyPairs() {
        try {
            const apiUrl = `${CONFIG.API_BASE_URL}${CONFIG.ENDPOINTS.FOREX_PAIRS}?market_type=${MARKET_TYPE}&force_refresh=true&_t=${Date.now()}`;
            console.log('Fetching currency pairs from:', apiUrl);
            console.log('Current MARKET_TYPE:', MARKET_TYPE);
            
            const response = await Utils.request(apiUrl);
            
            console.log('API Response:', response);
            console.log('Response market_type:', response.market_type);
            console.log('Response data length:', response.data?.length);
            
            if (response.success && response.data) {
                // Validate that we got the correct market type data
                if (response.market_type !== MARKET_TYPE) {
                    console.warn(`❌ Received ${response.market_type} data but requested ${MARKET_TYPE}!`);
                    throw new Error(`Server returned ${response.market_type} data but ${MARKET_TYPE} was requested`);
                }
                
                console.log('✅ Processing', response.data.length, 'currency pairs for market type:', MARKET_TYPE);
                
                // Clear existing data
                this.currencyData.clear();
                
                response.data.forEach(pair => {
                    this.currencyData.set(pair.symbol, pair);
                });
                
                this.updateCurrencyGrid();
                this.updateLastRefreshTime();
                console.log('✅ Currency pairs loaded successfully for', MARKET_TYPE);
            } else {
                throw new Error(response.error || 'Failed to load currency pairs - invalid response structure');
            }
        } catch (error) {
            console.error('❌ Error loading currency pairs:', error);
            Utils.showNotification(`Failed to load live ${MARKET_TYPE} data. Please check your connection.`, 'error');
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

        // Use the actual fetched data instead of CONFIG.CURRENCY_PAIRS
        console.log('Updating currency grid with', this.currencyData.size, 'pairs for market type:', MARKET_TYPE);
        
        this.currencyData.forEach((pairData, symbol) => {
            // Create a simple config object for each pair
            const pairConfig = {
                symbol: symbol,
                name: symbol.replace('USD', '/USD').replace('EUR', '/EUR').replace('GBP', '/GBP')
            };
            const card = this.createCurrencyCard(pairConfig, pairData);
            grid.appendChild(card);
        });
        
        // If no data available, show message
        if (this.currencyData.size === 0) {
            grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-secondary);">
                <i class="fas fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>Loading ${MARKET_TYPE} pairs...</p>
            </div>`;
        }
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
        
        // Data validation information
        const dataQuality = pairData?.data_quality || 'Unknown';
        const confidenceScore = pairData?.confidence_score || 0;
        const validationWarnings = pairData?.validation_warnings || 0;
        
        // Get signal for this pair
        const signal = window.signalManager?.signals.get(pairConfig.symbol);
        const signalDirection = signal?.signal?.direction || 'HOLD';
        const signalConfidence = signal?.signal?.confidence || 0;

        const changeClass = change >= 0 ? 'positive' : 'negative';
        const signalClass = `signal-${signalDirection.toLowerCase()}`;
        
        // Determine data quality indicator
        const qualityClass = this.getDataQualityClass(dataQuality, confidenceScore);
        const qualityIcon = this.getDataQualityIcon(dataQuality);
        const qualityTooltip = this.getDataQualityTooltip(dataQuality, confidenceScore, validationWarnings);

        card.innerHTML = `
            <div class="currency-header">
                <div class="currency-pair">${pairConfig.name}</div>
                <div class="currency-meta">
                    <div class="currency-flag">
                        <span class="flag">${this.getCurrencyFlag(pairConfig.base)}</span>
                        <span class="flag">${this.getCurrencyFlag(pairConfig.quote)}</span>
                    </div>
                    <div class="data-quality ${qualityClass}" title="${qualityTooltip}">
                        <i class="fas fa-${qualityIcon}"></i>
                    </div>
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
            
            ${confidenceScore > 0 ? `
            <div class="currency-validation">
                <div class="validation-score">
                    Data Quality: <span class="${qualityClass}">${dataQuality}</span>
                    ${confidenceScore > 0 ? `(${confidenceScore}%)` : ''}
                </div>
            </div>
            ` : ''}
        `;

        return card;
    }

    /**
     * Get data quality CSS class
     * @param {string} quality - Data quality rating
     * @param {number} score - Confidence score
     * @returns {string} CSS class
     */
    getDataQualityClass(quality, score) {
        if (score >= 90 || quality === 'Excellent') return 'quality-excellent';
        if (score >= 80 || quality === 'Good') return 'quality-good';
        if (score >= 70 || quality === 'Fair') return 'quality-fair';
        if (score >= 50 || quality === 'Poor') return 'quality-poor';
        return 'quality-unreliable';
    }

    /**
     * Get data quality icon
     * @param {string} quality - Data quality rating
     * @returns {string} Icon class
     */
    getDataQualityIcon(quality) {
        switch (quality) {
            case 'Excellent': return 'check-circle';
            case 'Good': return 'check';
            case 'Fair': return 'exclamation-triangle';
            case 'Poor': return 'exclamation-circle';
            case 'Unreliable': return 'times-circle';
            default: return 'question-circle';
        }
    }

    /**
     * Get data quality tooltip
     * @param {string} quality - Data quality rating
     * @param {number} score - Confidence score
     * @param {number} warnings - Number of validation warnings
     * @returns {string} Tooltip text
     */
    getDataQualityTooltip(quality, score, warnings) {
        let tooltip = `Data Quality: ${quality}`;
        if (score > 0) {
            tooltip += ` (${score}% confidence)`;
        }
        if (warnings > 0) {
            tooltip += `\n${warnings} validation warning${warnings > 1 ? 's' : ''}`;
        }
        
        switch (quality) {
            case 'Excellent':
                tooltip += '\nHigh-quality real-time data from reliable sources';
                break;
            case 'Good':
                tooltip += '\nReliable data with minor validation checks';
                break;
            case 'Fair':
                tooltip += '\nAcceptable data quality with some limitations';
                break;
            case 'Poor':
                tooltip += '\nLimited data quality, use with caution';
                break;
            case 'Unreliable':
                tooltip += '\nData quality issues detected, verify independently';
                break;
        }
        
        return tooltip;
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
     * Handle URL hash navigation for deep linking
     */
    handleUrlHash() {
        const hash = window.location.hash;
        if (!hash) return;

        // Remove the # and parse the hash
        const hashContent = hash.substring(1);
        const [tab, queryString] = hashContent.split('?');
        
        // Parse query parameters
        const params = new URLSearchParams(queryString || '');
        
        // Switch to the appropriate tab
        if (tab && ['dashboard', 'analysis', 'signals'].includes(tab)) {
            this.switchTab(tab);
            
            // Handle specific parameters for analysis tab
            if (tab === 'analysis') {
                const pair = params.get('pair');
                const showChart = params.get('chart');
                
                if (pair) {
                    // Set the selected pair in the dropdown
                    const pairSelect = document.getElementById('analysis-pair');
                    if (pairSelect) {
                        pairSelect.value = pair;
                    }
                }
                
                // If chart parameter is present, we could trigger chart loading
                if (showChart === 'true') {
                    // Add a small delay to ensure the tab is fully loaded
                    setTimeout(() => {
                        const analyzeBtn = document.getElementById('analyze-btn');
                        if (analyzeBtn) {
                            analyzeBtn.click();
                        }
                    }, 500);
                }
            }
        }
    }

    /**
     * Load data for specific tab
     * @param {string} tabName - Tab name
     */
    async loadTabData(tabName) {
        switch (tabName) {
            case 'signals':
                if (window.signalManager) {
                    // Get current timeframe from analysis tab
                    const timeframeSelector = document.getElementById('analysis-timeframe');
                    const currentTimeframe = timeframeSelector?.value || '1h';
                    
                    // Update signal manager timeframe and fetch signals
                    await window.signalManager.updateSignalsForTimeframe(currentTimeframe);
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
        const analyzeBtn = document.getElementById('analyze-btn');

        if (!pair || !timeframe) {
            Utils.showNotification('Please select a currency pair and timeframe', 'warning');
            return;
        }

        // Start loading animation
        this.startAnalysisLoading();

        try {
            console.log('Starting analysis for pair:', pair, 'timeframe:', timeframe);
            
            // Step 1: Fetch price data (25% progress)
            this.updateAnalysisProgress(25, 'Fetching price data...');
            const priceData = await this.fetchPriceData(pair, timeframe);
            console.log('Price data fetched:', priceData);
            await new Promise(resolve => setTimeout(resolve, 200)); // Small delay for UX
            
            // Step 2: Fetch technical analysis (50% progress)
            this.updateAnalysisProgress(50, 'Performing technical analysis...');
            const technicalAnalysis = await this.fetchTechnicalAnalysis(pair, timeframe);
            console.log('Technical analysis fetched:', technicalAnalysis);
            await new Promise(resolve => setTimeout(resolve, 300)); // Small delay for UX
            
            // Step 3: Fetch fundamental analysis (75% progress)
            this.updateAnalysisProgress(75, 'Analyzing fundamentals...');
            const fundamentalAnalysis = await this.fetchFundamentalAnalysis(pair);
            console.log('Fundamental analysis fetched:', fundamentalAnalysis);
            await new Promise(resolve => setTimeout(resolve, 200)); // Small delay for UX

            // Step 4: Update chart and results (100% progress)
            this.updateAnalysisProgress(90, 'Generating chart...');
            await new Promise(resolve => setTimeout(resolve, 200)); // Small delay for UX
            
            // Update chart
            if (window.chartManager && priceData) {
                console.log('Creating chart with chartManager and priceData available');
                window.chartManager.createChart(priceData, pair, timeframe);
            } else {
                console.warn('Chart not created - chartManager:', !!window.chartManager, 'priceData:', !!priceData);
            }

            // Update analysis results
            this.updateAnalysisResults(technicalAnalysis, fundamentalAnalysis);
            
            // Complete
            this.updateAnalysisProgress(100, 'Analysis complete!');
            
            // Small delay to show completion
            await new Promise(resolve => setTimeout(resolve, 500));

        } catch (error) {
            console.error('Analysis failed:', error);
            Utils.showNotification('Analysis failed. Please try again.', 'error');
        } finally {
            this.stopAnalysisLoading();
        }
    }

    /**
     * Start analysis loading animation
     */
    startAnalysisLoading() {
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.classList.add('loading');
            analyzeBtn.disabled = true;
        }
    }

    /**
     * Update analysis progress
     * @param {number} percentage - Progress percentage (0-100)
     * @param {string} message - Progress message
     */
    updateAnalysisProgress(percentage, message) {
        const progressFill = document.querySelector('.analyze-progress-fill');
        const progressText = document.querySelector('.analyze-progress-text');
        
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = message;
        }
        
        console.log(`Analysis progress: ${percentage}% - ${message}`);
    }

    /**
     * Stop analysis loading animation
     */
    stopAnalysisLoading() {
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.classList.remove('loading');
            analyzeBtn.disabled = false;
        }
        
        // Reset progress
        const progressFill = document.querySelector('.analyze-progress-fill');
        if (progressFill) {
            setTimeout(() => {
                progressFill.style.width = '0%';
            }, 300);
        }
    }

    /**
     * Toggle debug panel visibility
     */
    toggleDebugPanel() {
        const debugPanel = document.getElementById('debug-panel');
        const debugToggle = document.getElementById('debug-toggle');
        
        if (debugPanel && debugToggle) {
            const isVisible = debugPanel.classList.contains('visible');
            
            if (isVisible) {
                // Hide panel
                debugPanel.classList.remove('visible');
                debugToggle.classList.remove('active');
                debugToggle.setAttribute('aria-label', 'Show debug panel');
                console.log('Debug panel hidden');
            } else {
                // Show panel
                debugPanel.classList.add('visible');
                debugToggle.classList.add('active');
                debugToggle.setAttribute('aria-label', 'Hide debug panel');
                console.log('Debug panel shown');
            }
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
        this.updateLastRefreshTime();
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
     * @param {string} customText - Custom status text
     */
    updateConnectionStatus(connected, customText = null) {
        const status = document.getElementById('connection-status');
        if (!status) return;

        const icon = status.querySelector('i');
        const text = status.querySelector('span');

        if (connected) {
            status.className = 'connection-status connected';
            text.textContent = customText || 'Connected';
        } else {
            status.className = 'connection-status disconnected';
            text.textContent = customText || 'Disconnected';
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
    console.log('Application loading...');
    
    window.app = new ForexAnalysisApp();
    window.forexApp = window.app; // Keep both for compatibility
    window.chartManager = new ChartManager();
    window.signalManager = new SignalManager();
    
    // Initialize market type to forex (default) and populate dropdowns
    setTimeout(() => {
        updatePairDropdowns('forex'); // Populate dropdowns first
        setMarketType('forex'); // Then set market type
        console.log('Market type initialized, toggle buttons should be ready');
    }, 500);
    
    console.log('Application initialized with chartManager:', !!window.chartManager);
    console.log('Application initialized with app:', !!window.app);
});
