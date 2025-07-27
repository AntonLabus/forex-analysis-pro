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
            // Initialize theme
            this.initTheme();
            
            // Load initial data
            await this.loadFeaturedPairData();
            await this.loadMarketStats();
            
            // Load mini chart
            await this.loadMiniChart();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Start auto-refresh
            this.startAutoRefresh();
            
            // Initialize WebSocket connection
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
            const apiUrl = window.CONFIG?.API_BASE_URL || 'http://localhost:5000';
            const response = await fetch(`${apiUrl}/api/signals?pair=${this.featuredPair}&timeframe=1h`);
            const data = await response.json();
            
            if (data.success && data.signals && data.signals.length > 0) {
                const signal = data.signals[0];
                this.updateSignalDisplay(signal);
            } else {
                this.showFallbackSignal();
            }
        } catch (error) {
            console.error('Error loading signal data:', error);
            this.showFallbackSignal();
        }
    }

    async loadMiniChart() {
        try {
            const miniChartContainer = document.getElementById('mini-chart');
            if (!miniChartContainer) return;

            // Create a simple price chart using Chart.js
            const canvas = document.createElement('canvas');
            canvas.id = 'mini-chart-canvas';
            canvas.width = 300;
            canvas.height = 150;
            
            // Clear the placeholder and add canvas
            miniChartContainer.innerHTML = '';
            miniChartContainer.appendChild(canvas);

            // Generate sample price data (in a real app, this would come from your API)
            const sampleData = this.generateSampleChartData();
            
            // Create the chart
            new Chart(canvas, {
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
            
        } catch (error) {
            console.error('Error loading mini chart:', error);
            // Show fallback chart placeholder
            const miniChartContainer = document.getElementById('mini-chart');
            if (miniChartContainer) {
                miniChartContainer.innerHTML = `
                    <div class="chart-placeholder">
                        <i class="fas fa-chart-line"></i>
                        <span>Chart unavailable</span>
                    </div>
                `;
            }
        }
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

        const direction = signal.signal?.direction || 'HOLD';
        const confidence = signal.signal?.confidence || 85;
        const strength = signal.signal?.strength || 0.7;
        
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

        // Update signal metrics (mock data for demonstration)
        const currentPrice = parseFloat(document.getElementById('featured-price')?.textContent || '1.0850');
        const entry = direction === 'BUY' ? currentPrice - 0.0005 : currentPrice + 0.0005;
        const target = direction === 'BUY' ? entry + 0.0075 : entry - 0.0075;
        const stop = direction === 'BUY' ? entry - 0.0055 : entry + 0.0055;
        const riskReward = Math.abs(target - entry) / Math.abs(entry - stop);

        const metrics = signalElement.querySelectorAll('.metric-value');
        if (metrics.length >= 4) {
            metrics[0].textContent = entry.toFixed(4);
            metrics[1].textContent = target.toFixed(4);
            metrics[2].textContent = stop.toFixed(4);
            metrics[3].textContent = `1:${riskReward.toFixed(2)}`;
        }
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
    window.location.href = `app.html#${tab}`;
}

function navigateToAnalysis(pair = 'EURUSD') {
    // Navigate to analysis page with specific pair
    window.location.href = `app.html#analysis?pair=${pair}`;
}

function navigateToChart(pair = 'EURUSD') {
    // Navigate to analysis page with chart focus
    window.location.href = `app.html#analysis?pair=${pair}&chart=true`;
}

function navigateToSignals() {
    // Navigate to signals page
    window.location.href = `app.html#signals`;
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
