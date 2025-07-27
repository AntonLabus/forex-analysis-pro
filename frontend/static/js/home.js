/**
 * Home Page JavaScript
 * Handles home page interactions and data loading
 */

class HomePage {
    constructor() {
        this.featuredPair = 'EURUSD';
        this.updateInterval = null;
        this.socket = null;
        
        this.init();
    }

    async init() {
        try {
            console.log('Starting home page initialization...');
            // Initialize theme
            this.initTheme();
            console.log('Theme initialized');
            
            // Load initial data
            console.log('Loading featured pair data...');
            await this.loadFeaturedPairData();
            console.log('Featured pair data loaded');
            
            console.log('Loading market stats...');
            await this.loadMarketStats();
            console.log('Market stats loaded');
            
            // Load mini chart with delay to ensure Chart.js is ready
            console.log('Setting up chart loading timeout...');
            // Show CSS fallback immediately for better UX
            this.showFallbackChart(document.getElementById('mini-chart'));
            setTimeout(() => {
                console.log('Chart loading timeout triggered, calling loadMiniChart...');
                this.loadMiniChart();
            }, 1000);
            
            // Set up event listeners
            console.log('Setting up event listeners...');
            this.setupEventListeners();
            
            // Start auto-refresh
            console.log('Starting auto-refresh...');
            this.startAutoRefresh();
            
            // Initialize WebSocket connection
            console.log('Initializing WebSocket...');
            this.initWebSocket();
            
            console.log('Home page initialized successfully');
        } catch (error) {
            console.error('Failed to initialize home page:', error);
        }
    }

    initTheme() {
        const themeToggle = document.getElementById('theme-toggle');
        const savedTheme = localStorage.getItem('forex_theme') || 'dark';
        
        // Set initial theme
        document.body.classList.toggle('dark-theme', savedTheme === 'dark');
        document.body.setAttribute('data-theme', savedTheme);
        
        // Update theme toggle icon
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Add smooth scrolling for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add hover effects to provider cards
        document.querySelectorAll('.provider-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    toggleTheme() {
        const currentTheme = document.body.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.body.classList.toggle('dark-theme', newTheme === 'dark');
        document.body.setAttribute('data-theme', newTheme);
        
        // Save theme preference
        localStorage.setItem('forex_theme', newTheme);
        
        // Update theme toggle icon
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    async loadFeaturedPairData() {
        try {
            const apiUrl = window.CONFIG?.API_BASE_URL || 'http://localhost:5000';
            
            // Fetch current price data
            const response = await fetch(`${apiUrl}/api/forex/pairs`);
            const data = await response.json();
            
            if (data.success && data.data) {
                const pairData = data.data.find(pair => pair.symbol === this.featuredPair);
                if (pairData) {
                    this.updateFeaturedPairDisplay(pairData);
                }
            }

            // Fetch signal data
            await this.loadFeaturedSignal();
            
        } catch (error) {
            console.error('Error loading featured pair data:', error);
            this.showFallbackData();
        }
    }

    updateFeaturedPairDisplay(pairData) {
        // Update price
        const priceElement = document.getElementById('featured-price');
        if (priceElement) {
            priceElement.textContent = this.formatPrice(pairData.current_price);
        }

        // Update change
        const changeElement = document.getElementById('featured-change');
        if (changeElement) {
            const change = pairData.daily_change || 0;
            const changePercent = pairData.daily_change_percent || 0;
            const isPositive = change >= 0;
            
            changeElement.className = `price-change ${isPositive ? 'positive' : 'negative'}`;
            changeElement.innerHTML = `
                <i class="fas fa-${isPositive ? 'arrow-up' : 'arrow-down'}"></i>
                <span>${isPositive ? '+' : ''}${change.toFixed(4)} (${isPositive ? '+' : ''}${changePercent.toFixed(2)}%)</span>
            `;
        }

        // Update data quality badge
        const qualityBadge = document.querySelector('.data-quality-badge');
        if (qualityBadge && pairData.data_quality) {
            const quality = pairData.data_quality;
            const confidence = pairData.confidence_score || 0;
            
            qualityBadge.className = `data-quality-badge ${this.getQualityClass(quality)}`;
            qualityBadge.innerHTML = `
                <i class="fas fa-${this.getQualityIcon(quality)}"></i>
                <span>${quality} Quality</span>
            `;
            qualityBadge.title = `Data Quality: ${quality} (${confidence}% confidence)`;
        }
    }

    async loadFeaturedSignal() {
        try {
            console.log('Loading featured signal for:', this.featuredPair);
            const apiUrl = window.CONFIG?.API_BASE_URL || 'http://localhost:5000';
            const signalUrl = `${apiUrl}/api/signals/${this.featuredPair}?timeframe=1h`;
            console.log('Fetching signal from:', signalUrl);
            
            const response = await fetch(signalUrl);
            const data = await response.json();
            
            console.log('Signal API response:', data);
            
            if (data.success && data.signals && data.signals.length > 0) {
                const signal = data.signals[0];
                console.log('Using real signal:', signal);
                this.updateSignalDisplay(signal);
            } else {
                console.log('No signals found, showing fallback');
                this.showFallbackSignal();
            }
        } catch (error) {
            console.error('Error loading signal data:', error);
            this.showFallbackSignal();
        }
    }

    async loadMiniChart() {
        try {
            console.log('Loading mini chart...');
            const miniChartContainer = document.getElementById('mini-chart');
            if (!miniChartContainer) {
                console.error('Mini chart container not found');
                return;
            }

            // Add multiple attempts to load Chart.js with fallback
            let chartAttempts = 0;
            const maxAttempts = 3;
            
            const tryLoadChart = () => {
                chartAttempts++;
                console.log(`Chart loading attempt ${chartAttempts}/${maxAttempts}`);
                
                // Check if Chart.js is available
                if (typeof Chart === 'undefined') {
                    console.warn(`Chart.js not available on attempt ${chartAttempts}`);
                    
                    if (chartAttempts < maxAttempts) {
                        // Try again after a delay
                        setTimeout(tryLoadChart, 1000);
                        return;
                    } else {
                        // After max attempts, show a visual fallback
                        console.log('Max attempts reached, showing CSS-based chart fallback');
                        this.showFallbackChart(miniChartContainer);
                        return;
                    }
                }

                console.log('Chart.js is available, creating chart...');
                this.createActualChart(miniChartContainer);
            };
            
            // Start the first attempt
            tryLoadChart();
            
        } catch (error) {
            console.error('Error in loadMiniChart:', error);
            const miniChartContainer = document.getElementById('mini-chart');
            if (miniChartContainer) {
                this.showFallbackChart(miniChartContainer);
            }
        }
    }

    showFallbackChart(container) {
        // Create a CSS-based visual chart as fallback
        console.log('Creating CSS fallback chart');
        container.innerHTML = `
            <div class="css-chart-container">
                <div class="chart-header">
                    <span class="chart-pair">EUR/USD</span>
                    <span class="chart-price">1.0850</span>
                    <span class="chart-change positive">+0.21%</span>
                </div>
                <div class="css-chart">
                    <div class="chart-line">
                        <div class="chart-point" style="left: 0%; bottom: 45%;"></div>
                        <div class="chart-point" style="left: 12%; bottom: 48%;"></div>
                        <div class="chart-point" style="left: 25%; bottom: 42%;"></div>
                        <div class="chart-point" style="left: 37%; bottom: 55%;"></div>
                        <div class="chart-point" style="left: 50%; bottom: 52%;"></div>
                        <div class="chart-point" style="left: 62%; bottom: 58%;"></div>
                        <div class="chart-point" style="left: 75%; bottom: 60%;"></div>
                        <div class="chart-point" style="left: 87%; bottom: 65%;"></div>
                        <div class="chart-point" style="left: 100%; bottom: 62%;"></div>
                        <svg class="chart-svg">
                            <polyline 
                                points="0,55 12,52 25,58 37,45 50,48 62,42 75,40 87,35 100,38"
                                fill="none" 
                                stroke="rgba(96, 165, 250, 0.8)" 
                                stroke-width="2"
                                vector-effect="non-scaling-stroke">
                            </polyline>
                        </svg>
                    </div>
                </div>
            </div>
        `;
    }

    createActualChart(container) {
        // Create a simple price chart using Chart.js
        const canvas = document.createElement('canvas');
        canvas.id = 'mini-chart-canvas';
        canvas.width = 300;
        canvas.height = 150;
        
        // Clear the placeholder and add canvas
        container.innerHTML = '';
        container.appendChild(canvas);

        // Generate sample price data (in a real app, this would come from your API)
        const sampleData = this.generateSampleChartData();
        console.log('Sample data generated:', sampleData);
        
        // Create the chart
        const chart = new Chart(canvas, {
            type: 'line',
            data: {
                labels: sampleData.labels,
                datasets: [{
                    label: 'EUR/USD',
                    data: sampleData.prices,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        display: false
                    }
                },
                elements: {
                    point: {
                        radius: 0
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
        
        console.log('Chart created successfully:', chart);
    }

    generateSampleChartData() {
        const labels = [];
        const prices = [];
        const basePrice = 1.0850;
        const hours = 24;
        
        for (let i = 0; i < hours; i++) {
            const time = new Date();
            time.setHours(time.getHours() - (hours - i));
            labels.push(time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }));
            
            // Generate realistic price movement
            const volatility = 0.002;
            const trend = Math.sin(i / 6) * 0.001;
            const random = (Math.random() - 0.5) * volatility;
            const price = basePrice + trend + random;
            prices.push(price.toFixed(4));
        }
        
        return { labels, prices };
    }

    updateSignalDisplay(signal) {
        const signalElement = document.getElementById('featured-signal');
        if (!signalElement) return;

        console.log('Updating signal display with:', signal);

        const direction = signal.signal?.direction || signal.direction || 'HOLD';
        const confidence = signal.signal?.confidence || signal.confidence || 85;
        const strength = signal.signal?.strength || signal.strength || 0.7;
        
        // Update signal indicator
        const signalIndicator = signalElement.querySelector('.signal-indicator');
        if (signalIndicator) {
            signalIndicator.className = `signal-indicator ${direction.toLowerCase()}`;
            signalIndicator.innerHTML = `
                <i class="fas fa-${this.getSignalIcon(direction)}"></i>
                <span>${direction} Signal</span>
            `;
        }

        // Update confidence score
        const confidenceScore = signalElement.querySelector('.confidence-score');
        if (confidenceScore) {
            confidenceScore.textContent = `${Math.round(confidence)}%`;
        }

        // Update signal metrics with REAL data from API
        const metrics = signalElement.querySelectorAll('.metric-value');
        if (metrics.length >= 4) {
            // Use real signal data if available, otherwise calculate reasonable defaults
            const entry = signal.entry_price || signal.signal?.entry_price || 
                         (signal.current_price ? parseFloat(signal.current_price) : 1.0850);
            const target = signal.target_price || signal.signal?.target_price || 
                          (direction === 'BUY' ? entry + 0.0075 : entry - 0.0075);
            const stop = signal.stop_loss || signal.signal?.stop_loss || 
                        (direction === 'BUY' ? entry - 0.0055 : entry + 0.0055);
            
            const riskReward = Math.abs(target - entry) / Math.abs(entry - stop);

            metrics[0].textContent = typeof entry === 'number' ? entry.toFixed(4) : entry;
            metrics[1].textContent = typeof target === 'number' ? target.toFixed(4) : target;
            metrics[2].textContent = typeof stop === 'number' ? stop.toFixed(4) : stop;
            metrics[3].textContent = `1:${riskReward.toFixed(2)}`;
        }

        console.log('Signal display updated successfully');
    }

    async loadMarketStats() {
        try {
            const apiUrl = window.CONFIG?.API_BASE_URL || 'http://localhost:5000';
            
            // Load total signals
            const signalsResponse = await fetch(`${apiUrl}/api/signals/all`);
            const signalsData = await signalsResponse.json();
            
            if (signalsData.success) {
                const totalSignals = signalsData.signals?.length || 0;
                const activeSignalsElement = document.getElementById('active-signals');
                if (activeSignalsElement) {
                    activeSignalsElement.textContent = totalSignals;
                }
            }

            // Load data quality average
            const pairsResponse = await fetch(`${apiUrl}/api/forex/pairs`);
            const pairsData = await pairsResponse.json();
            
            if (pairsData.success && pairsData.data) {
                const qualityScores = pairsData.data
                    .map(pair => pair.confidence_score)
                    .filter(score => score > 0);
                
                if (qualityScores.length > 0) {
                    const avgQuality = qualityScores.reduce((a, b) => a + b, 0) / qualityScores.length;
                    const dataQualityElement = document.getElementById('data-quality');
                    if (dataQualityElement) {
                        dataQualityElement.textContent = `${Math.round(avgQuality)}%`;
                    }
                }
            }
            
        } catch (error) {
            console.error('Error loading market stats:', error);
        }
    }

    showFallbackData() {
        // Show realistic fallback data
        const priceElement = document.getElementById('featured-price');
        if (priceElement) {
            priceElement.textContent = '1.0850';
        }

        const changeElement = document.getElementById('featured-change');
        if (changeElement) {
            changeElement.className = 'price-change positive';
            changeElement.innerHTML = `
                <i class="fas fa-arrow-up"></i>
                <span>+0.0023 (+0.21%)</span>
            `;
        }
    }

    showFallbackSignal() {
        // Show fallback signal data
        const signalElement = document.getElementById('featured-signal');
        if (!signalElement) return;

        const signalIndicator = signalElement.querySelector('.signal-indicator');
        if (signalIndicator) {
            signalIndicator.className = 'signal-indicator buy';
            signalIndicator.innerHTML = `
                <i class="fas fa-arrow-trend-up"></i>
                <span>BUY Signal</span>
            `;
        }

        const confidenceScore = signalElement.querySelector('.confidence-score');
        if (confidenceScore) {
            confidenceScore.textContent = '85%';
        }
    }

    startAutoRefresh() {
        // Refresh data every 30 seconds
        this.updateInterval = setInterval(() => {
            this.loadFeaturedPairData();
            this.loadMarketStats();
        }, 30000);
    }

    initWebSocket() {
        try {
            const wsUrl = window.CONFIG?.WEBSOCKET_URL || 'http://localhost:5000';
            this.socket = io(wsUrl);
            
            this.socket.on('connect', () => {
                console.log('WebSocket connected');
                this.updateConnectionStatus(true);
            });
            
            this.socket.on('disconnect', () => {
                console.log('WebSocket disconnected');
                this.updateConnectionStatus(false);
            });
            
            this.socket.on('price_update', (data) => {
                if (data.pair === this.featuredPair) {
                    this.updateFeaturedPairDisplay(data);
                }
            });
            
        } catch (error) {
            console.error('WebSocket initialization failed:', error);
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            const icon = statusElement.querySelector('i');
            const text = statusElement.querySelector('span');
            
            if (connected) {
                icon.className = 'fas fa-circle';
                icon.style.color = 'var(--success-color)';
                text.textContent = 'Live';
                statusElement.style.color = 'var(--success-color)';
            } else {
                icon.className = 'fas fa-circle';
                icon.style.color = 'var(--warning-color)';
                text.textContent = 'Offline';
                statusElement.style.color = 'var(--warning-color)';
            }
        }
    }

    // Utility methods
    formatPrice(price) {
        if (typeof price !== 'number') return '0.0000';
        return price.toFixed(4);
    }

    getQualityClass(quality) {
        const qualityMap = {
            'Excellent': 'excellent',
            'Good': 'good',
            'Fair': 'fair',
            'Poor': 'poor',
            'Unreliable': 'unreliable'
        };
        return qualityMap[quality] || 'fair';
    }

    getQualityIcon(quality) {
        const iconMap = {
            'Excellent': 'check-circle',
            'Good': 'check',
            'Fair': 'exclamation-triangle',
            'Poor': 'exclamation-circle',
            'Unreliable': 'times-circle'
        };
        return iconMap[quality] || 'question-circle';
    }

    getSignalIcon(direction) {
        const iconMap = {
            'BUY': 'arrow-trend-up',
            'SELL': 'arrow-trend-down',
            'HOLD': 'minus'
        };
        return iconMap[direction] || 'minus';
    }

    // Cleanup
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.socket) {
            this.socket.disconnect();
        }
    }
}

// Modal functions
function showTermsModal() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus trap for accessibility
        const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];
        
        if (firstFocusableElement) {
            firstFocusableElement.focus();
        }
        
        // Handle tab key for focus trap
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusableElement) {
                        lastFocusableElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastFocusableElement) {
                        firstFocusableElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
        
        // Handle escape key
        modal.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeTermsModal();
            }
        });
    }
}

function closeTermsModal() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Navigation functions
function navigateToApp(tab = 'dashboard') {
    // Navigate to main app with specific tab
    console.log('navigateToApp called with tab:', tab);
    console.log('Current location:', window.location.href);
    const targetUrl = `app.html#${tab}`;
    console.log('Navigating to:', targetUrl);
    window.location.href = targetUrl;
}

function navigateToAnalysis(pair = 'EURUSD') {
    // Navigate to analysis page with specific pair
    console.log('navigateToAnalysis called with pair:', pair);
    console.log('Current location:', window.location.href);
    const targetUrl = `app.html#analysis?pair=${pair}`;
    console.log('Navigating to:', targetUrl);
    window.location.href = targetUrl;
}

function navigateToChart(pair = 'EURUSD') {
    // Navigate to analysis page with chart focus
    console.log('navigateToChart called with pair:', pair);
    console.log('Current location:', window.location.href);
    const targetUrl = `app.html#analysis?pair=${pair}&chart=true`;
    console.log('Navigating to:', targetUrl);
    window.location.href = targetUrl;
}

function navigateToSignals() {
    // Navigate to signals page
    console.log('navigateToSignals called');
    console.log('Current location:', window.location.href);
    const targetUrl = 'app.html#signals';
    console.log('Navigating to:', targetUrl);
    window.location.href = targetUrl;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.homePage = new HomePage();
});

// Cleanup when page unloads
window.addEventListener('beforeunload', () => {
    if (window.homePage) {
        window.homePage.destroy();
    }
});
