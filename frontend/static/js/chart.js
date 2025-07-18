/**
 * Chart management for Forex Analysis Pro
 */

class ChartManager {
    constructor() {
        this.currentChart = null;
        this.currentData = null;
        this.indicators = new Set();
        this.theme = Utils.getTheme();
    }

    /**
     * Initialize chart with price data
     * @param {Array} data - OHLCV data array
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Chart timeframe
     */
    createChart(data, pair, timeframe) {
        console.log('Creating chart with data:', data, 'pair:', pair, 'timeframe:', timeframe);
        
        if (!data || data.length === 0) {
            console.warn('No data available for chart');
            this.showNoDataMessage();
            return;
        }

        this.currentData = data;
        const chartDiv = document.getElementById('price-chart');
        
        if (!chartDiv) {
            console.error('Chart container not found');
            return;
        }
        
        console.log('Chart container found, preparing traces...');
        
        // Prepare data for Plotly
        const traces = this.prepareTraces(data);
        const layout = this.createLayout(pair, timeframe);
        const config = this.getChartConfig();

        console.log('Traces prepared:', traces.length, 'Creating Plotly chart...');

        // Create the chart with enhanced interactivity
        Plotly.newPlot(chartDiv, traces, layout, config)
            .then(() => {
                console.log('Chart created successfully');
                this.currentChart = chartDiv;
                this.updateChartTitle(pair, timeframe);
                
                // Add custom event listeners for better UX
                this.setupChartInteractivity(chartDiv);
            })
            .catch(error => {
                console.error('Error creating chart:', error);
                Utils.showNotification('Failed to create chart', 'error');
            });
    }

    /**
     * Prepare chart traces (candlestick, volume, indicators)
     * @param {Array} data - OHLCV data
     * @returns {Array} Array of Plotly traces
     */
    prepareTraces(data) {
        const traces = [];

        // Prepare data arrays
        const timestamps = data.map(d => new Date(d.timestamp));
        const opens = data.map(d => d.open);
        const highs = data.map(d => d.high);
        const lows = data.map(d => d.low);
        const closes = data.map(d => d.close);
        const volumes = data.map(d => d.volume || 0);

        // Main candlestick trace with enhanced styling
        const candlestickTrace = {
            type: 'candlestick',
            x: timestamps,
            open: opens,
            high: highs,
            low: lows,
            close: closes,
            name: 'Price',
            yaxis: 'y',
            increasing: { 
                line: { color: CONFIG.CHART.COLORS.BULLISH, width: 1 },
                fillcolor: CONFIG.CHART.COLORS.BULLISH
            },
            decreasing: { 
                line: { color: CONFIG.CHART.COLORS.BEARISH, width: 1 },
                fillcolor: CONFIG.CHART.COLORS.BEARISH
            },
            showlegend: false,
            hovertemplate: 
                '<b>%{x}</b><br>' +
                'Open: %{open:.5f}<br>' +
                'High: %{high:.5f}<br>' +
                'Low: %{low:.5f}<br>' +
                'Close: %{close:.5f}<br>' +
                '<extra></extra>'
        };
        traces.push(candlestickTrace);

        // Enhanced Volume trace - make it optional and less intrusive
        const hasVolume = volumes.some(v => v > 0);
        if (hasVolume && this.indicators.has('volume')) {  // Only show if volume indicator is enabled
            // Color volume bars based on price direction
            const volumeColors = [];
            for (let i = 0; i < volumes.length; i++) {
                if (i === 0) {
                    volumeColors.push(CONFIG.CHART.COLORS.VOLUME);
                } else {
                    const color = closes[i] >= closes[i-1] ? 
                        CONFIG.CHART.COLORS.BULLISH : CONFIG.CHART.COLORS.BEARISH;
                    volumeColors.push(color);
                }
            }
            
            // Enhanced Volume trace - only when explicitly enabled
            const volumeTrace = {
                type: 'bar',
                x: timestamps,
                y: volumes,
                name: 'Volume',
                yaxis: 'y2',
                marker: {
                    color: volumeColors,
                    opacity: 0.2,  // Very transparent
                    line: { width: 0 }
                },
                showlegend: false,
                hovertemplate: 
                    '<b>%{x}</b><br>' +
                    'Volume: %{y:,.0f}<br>' +
                    '<extra></extra>'
            };
            traces.push(volumeTrace);
        }

        // Add indicator traces if active
        this.addIndicatorTraces(traces, timestamps, opens, highs, lows, closes, volumes);

        return traces;
    }

    /**
     * Add technical indicator traces to the chart
     * @param {Array} traces - Existing traces array
     * @param {Array} timestamps - Time data
     * @param {Array} opens - Open prices
     * @param {Array} highs - High prices
     * @param {Array} lows - Low prices
     * @param {Array} closes - Close prices
     * @param {Array} volumes - Volume data
     */
    addIndicatorTraces(traces, timestamps, opens, highs, lows, closes, volumes) {
        // Simple Moving Average
        if (this.indicators.has('sma')) {
            const sma20 = this.calculateSMA(closes, 20);
            const sma50 = this.calculateSMA(closes, 50);
            
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: sma20,
                name: 'SMA 20',
                line: { color: CONFIG.CHART.COLORS.MA, width: 2 },
                yaxis: 'y'
            });

            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: sma50,
                name: 'SMA 50',
                line: { color: '#8b5cf6', width: 2 },
                yaxis: 'y'
            });
        }

        // Exponential Moving Average
        if (this.indicators.has('ema')) {
            const ema12 = this.calculateEMA(closes, 12);
            const ema26 = this.calculateEMA(closes, 26);
            
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: ema12,
                name: 'EMA 12',
                line: { color: '#06b6d4', width: 2 },
                yaxis: 'y'
            });

            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: ema26,
                name: 'EMA 26',
                line: { color: '#84cc16', width: 2 },
                yaxis: 'y'
            });
        }

        // Bollinger Bands
        if (this.indicators.has('bollinger')) {
            const bollinger = this.calculateBollingerBands(closes, 20, 2);
            
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: bollinger.upper,
                name: 'BB Upper',
                line: { color: '#94a3b8', dash: 'dash' },
                yaxis: 'y'
            });

            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: bollinger.lower,
                name: 'BB Lower',
                line: { color: '#94a3b8', dash: 'dash' },
                yaxis: 'y',
                fill: 'tonexty',
                fillcolor: 'rgba(148, 163, 184, 0.1)'
            });
        }

        // RSI
        if (this.indicators.has('rsi')) {
            const rsi = this.calculateRSI(closes, 14);
            
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: rsi,
                name: 'RSI',
                line: { color: CONFIG.CHART.COLORS.RSI, width: 2 },
                yaxis: 'y3'
            });

            // RSI overbought/oversold lines
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: [timestamps[0], timestamps[timestamps.length - 1]],
                y: [70, 70],
                name: 'Overbought',
                line: { color: '#ef4444', dash: 'dash', width: 1 },
                yaxis: 'y3',
                showlegend: false
            });

            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: [timestamps[0], timestamps[timestamps.length - 1]],
                y: [30, 30],
                name: 'Oversold',
                line: { color: '#10b981', dash: 'dash', width: 1 },
                yaxis: 'y3',
                showlegend: false
            });
        }

        // MACD
        if (this.indicators.has('macd')) {
            const macd = this.calculateMACD(closes, 12, 26, 9);
            
            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: macd.macd,
                name: 'MACD',
                line: { color: CONFIG.CHART.COLORS.MACD, width: 2 },
                yaxis: 'y4'
            });

            traces.push({
                type: 'scatter',
                mode: 'lines',
                x: timestamps,
                y: macd.signal,
                name: 'Signal',
                line: { color: '#ef4444', width: 2 },
                yaxis: 'y4'
            });

            traces.push({
                type: 'bar',
                x: timestamps,
                y: macd.histogram,
                name: 'Histogram',
                marker: { color: '#64748b' },
                yaxis: 'y4'
            });
        }
    }

    /**
     * Create chart layout configuration
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Chart timeframe
     * @returns {Object} Plotly layout object
     */
    createLayout(pair, timeframe) {
        const themeColors = this.theme === 'dark' ? 
            CONFIG.CHART.THEME.DARK : CONFIG.CHART.THEME.LIGHT;

        const layout = {
            title: {
                text: `${pair} - ${timeframe.toUpperCase()}`,
                font: { color: themeColors.textColor, size: 18 },
                x: 0.05
            },
            paper_bgcolor: themeColors.background,
            plot_bgcolor: themeColors.background,
            font: { color: themeColors.textColor, size: 12 },
            
            // Enhanced X-axis with better navigation
            xaxis: {
                type: 'date',
                gridcolor: themeColors.gridColor,
                showgrid: true,
                rangeslider: { 
                    visible: true,
                    bgcolor: 'rgba(0,0,0,0.1)',
                    bordercolor: themeColors.gridColor,
                    thickness: 0.08
                },
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1H', step: 'hour', stepmode: 'backward' },
                        { count: 4, label: '4H', step: 'hour', stepmode: 'backward' },
                        { count: 1, label: '1D', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1W', step: 'day', stepmode: 'backward' },
                        { step: 'all', label: 'All' }
                    ],
                    bgcolor: 'rgba(0,0,0,0.1)',
                    bordercolor: themeColors.gridColor,
                    font: { color: themeColors.textColor }
                },
                tickformat: '%H:%M\n%b %d'
            },
            
            // Enhanced Y-axis for price
            yaxis: {
                title: { text: 'Price', font: { size: 14 } },
                side: 'right',
                gridcolor: themeColors.gridColor,
                showgrid: true,
                domain: this.getYAxisDomain('price'),
                tickformat: '.5f',
                fixedrange: false,
                autorange: true
            },
            
            // Better margins and spacing
            margin: { t: 80, r: 100, b: 80, l: 20 },
            
            // Enhanced legend
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.1)',
                bordercolor: themeColors.gridColor,
                borderwidth: 1,
                font: { color: themeColors.textColor, size: 11 }
            },
            
            // Add crossfilter cursor
            hovermode: 'x unified',
            dragmode: 'zoom'
        };

        // Add additional y-axes for indicators with better spacing
        if (this.indicators.has('rsi')) {
            layout.yaxis3 = {
                title: { text: 'RSI', font: { size: 12 } },
                side: 'left',
                overlaying: 'y',
                position: 0.02,
                domain: [0.75, 0.95],
                range: [0, 100],
                gridcolor: themeColors.gridColor,
                showgrid: true,
                tickformat: '.0f'
            };
        }

        if (this.indicators.has('macd')) {
            layout.yaxis4 = {
                title: { text: 'MACD', font: { size: 12 } },
                side: 'left',
                overlaying: 'y',
                position: 0.02,
                domain: [0.05, 0.25],
                gridcolor: themeColors.gridColor,
                showgrid: true,
                tickformat: '.5f'
            };
        }

        // Enhanced Volume y-axis - only show when volume indicator is active
        if (this.indicators.has('volume')) {
            layout.yaxis2 = {
                title: { text: 'Vol', font: { size: 8 } },
                side: 'left',
                overlaying: 'y',
                position: 0.02,
                domain: [0.92, 0.98],  // Very tiny area at bottom
                gridcolor: themeColors.gridColor,
                showgrid: false,
                tickformat: '.1s',
                showticklabels: false
            };
        }

        return layout;
    }

    /**
     * Get chart configuration
     * @returns {Object} Plotly config object
     */
    getChartConfig() {
        return {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: [
                'lasso2d', 'select2d', 'autoScale2d'
            ],
            modeBarButtonsToAdd: [
                {
                    name: 'Toggle Crosshair',
                    icon: {
                        width: 857.1,
                        height: 1000,
                        path: 'm214-142 285-285 285 285-285 285-285-285ZM0 571h200v571H0V571Zm657 571V571h200v571H657Z'
                    },
                    click: function(gd) {
                        const layout = gd.layout;
                        layout.hovermode = layout.hovermode === 'x unified' ? 'closest' : 'x unified';
                        Plotly.redraw(gd);
                    }
                }
            ],
            toImageButtonOptions: {
                format: 'png',
                filename: 'forex-chart',
                height: 600,
                width: 1200,
                scale: 2
            },
            scrollZoom: true,
            doubleClick: 'reset+autosize'
        };
    }

    /**
     * Calculate Y-axis domain based on active indicators
     * @param {string} axis - Axis type
     * @returns {Array} Domain array [min, max]
     */
    getYAxisDomain(axis) {
        if (axis === 'price') {
            let bottomMargin = 0.02;  // Start very low - no volume interference by default
            let topMargin = 0.95;     // Give price chart maximum space
            
            // Adjust for volume if explicitly enabled
            if (this.indicators.has('volume')) {
                topMargin = 0.90;  // Small adjustment for volume
            }
            
            // Adjust for RSI at top
            if (this.indicators.has('rsi')) {
                topMargin = this.indicators.has('volume') ? 0.70 : 0.72;
            }
            
            // Adjust for MACD at bottom
            if (this.indicators.has('macd')) {
                bottomMargin = 0.28;  // Leave room for MACD at bottom
                if (this.indicators.has('rsi')) {
                    topMargin = this.indicators.has('volume') ? 0.70 : 0.72;
                } else {
                    topMargin = this.indicators.has('volume') ? 0.90 : 0.95;
                }
            }
            
            return [bottomMargin, topMargin];
        }
        
        return [0, 1];
    }

    /**
     * Toggle indicator on/off with enhanced visual feedback
     * @param {string} indicator - Indicator name
     */
    toggleIndicator(indicator) {
        const wasActive = this.indicators.has(indicator);
        
        if (wasActive) {
            this.indicators.delete(indicator);
        } else {
            this.indicators.add(indicator);
        }

        // Update chart button state with animation
        const button = document.querySelector(`[data-indicator="${indicator}"]`);
        if (button) {
            button.classList.toggle('active', !wasActive);
            
            // Add visual feedback
            if (!wasActive) {
                button.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    button.style.transform = '';
                }, 150);
                
                // Show tooltip
                this.showIndicatorTooltip(button, `${indicator.toUpperCase()} enabled`);
            } else {
                this.showIndicatorTooltip(button, `${indicator.toUpperCase()} disabled`);
            }
        }

        // Redraw chart if we have data
        if (this.currentData) {
            const pair = document.getElementById('analysis-pair')?.value || 'EURUSD';
            const timeframe = document.getElementById('analysis-timeframe')?.value || '1h';
            this.createChart(this.currentData, pair, timeframe);
        }
    }

    /**
     * Setup enhanced chart interactivity
     * @param {HTMLElement} chartDiv - Chart container element
     */
    setupChartInteractivity(chartDiv) {
        // Add hover effect for better data exploration
        chartDiv.on('plotly_hover', (data) => {
            if (data.points && data.points.length > 0) {
                const point = data.points[0];
                
                // Show crosshair cursor
                chartDiv.style.cursor = 'crosshair';
                
                // Optional: Add custom info panel
                this.updateInfoPanel(point);
            }
        });

        // Reset cursor on unhover
        chartDiv.on('plotly_unhover', () => {
            chartDiv.style.cursor = 'default';
        });

        // Add double-click to reset zoom
        chartDiv.on('plotly_doubleclick', () => {
            Plotly.relayout(chartDiv, {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
        });
    }

    /**
     * Update info panel with current data point
     * @param {Object} point - Plotly data point
     */
    updateInfoPanel(point) {
        // This could be expanded to show a custom info panel
        // For now, we rely on the enhanced hover templates
        console.log('Hover data:', point);
    }

    /**
     * Show indicator tooltip
     * @param {HTMLElement} button - Button element
     * @param {string} message - Tooltip message
     */
    showIndicatorTooltip(button, message) {
        // Remove existing tooltip
        const existingTooltip = document.querySelector('.indicator-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        // Create new tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'indicator-tooltip';
        tooltip.textContent = message;
        tooltip.style.cssText = `
            position: absolute;
            background: var(--bg-tertiary);
            color: var(--text-primary);
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.75rem;
            white-space: nowrap;
            z-index: 1000;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
            pointer-events: none;
        `;

        // Position tooltip
        const rect = button.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.bottom + 5) + 'px';

        document.body.appendChild(tooltip);

        // Remove tooltip after delay
        setTimeout(() => {
            tooltip.remove();
        }, 2000);
    }

    /**
     * Update chart title
     * @param {string} pair - Currency pair
     * @param {string} timeframe - Timeframe
     */
    updateChartTitle(pair, timeframe) {
        const titleElement = document.getElementById('chart-title');
        if (titleElement) {
            titleElement.textContent = `${pair} - ${timeframe.toUpperCase()} Chart`;
        }
    }

    /**
     * Show no data message
     */
    showNoDataMessage() {
        const chartDiv = document.getElementById('price-chart');
        if (chartDiv) {
            chartDiv.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; height: 400px; color: var(--text-secondary);">
                    <div style="text-align: center;">
                        <i class="fas fa-chart-line" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                        <div style="font-size: 1.125rem;">No chart data available</div>
                        <div style="font-size: 0.875rem; margin-top: 0.5rem;">Select a currency pair and click "Analyze" to view chart</div>
                    </div>
                </div>
            `;
        }
    }

    // Technical Indicator Calculations

    /**
     * Calculate Simple Moving Average
     * @param {Array} data - Price data
     * @param {number} period - Period for calculation
     * @returns {Array} SMA values
     */
    calculateSMA(data, period) {
        const sma = [];
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                sma.push(null);
            } else {
                const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                sma.push(sum / period);
            }
        }
        return sma;
    }

    /**
     * Calculate Exponential Moving Average
     * @param {Array} data - Price data
     * @param {number} period - Period for calculation
     * @returns {Array} EMA values
     */
    calculateEMA(data, period) {
        const ema = [];
        const multiplier = 2 / (period + 1);
        
        for (let i = 0; i < data.length; i++) {
            if (i === 0) {
                ema.push(data[i]);
            } else {
                ema.push((data[i] * multiplier) + (ema[i - 1] * (1 - multiplier)));
            }
        }
        return ema;
    }

    /**
     * Calculate Bollinger Bands
     * @param {Array} data - Price data
     * @param {number} period - Period for calculation
     * @param {number} stdDev - Standard deviation multiplier
     * @returns {Object} Bollinger Bands object
     */
    calculateBollingerBands(data, period, stdDev) {
        const sma = this.calculateSMA(data, period);
        const upper = [];
        const lower = [];
        
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                upper.push(null);
                lower.push(null);
            } else {
                const slice = data.slice(i - period + 1, i + 1);
                const mean = sma[i];
                const variance = slice.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / period;
                const standardDeviation = Math.sqrt(variance);
                
                upper.push(mean + (standardDeviation * stdDev));
                lower.push(mean - (standardDeviation * stdDev));
            }
        }
        
        return { upper, middle: sma, lower };
    }

    /**
     * Calculate RSI
     * @param {Array} data - Price data
     * @param {number} period - Period for calculation
     * @returns {Array} RSI values
     */
    calculateRSI(data, period) {
        const rsi = [];
        const gains = [];
        const losses = [];
        
        for (let i = 1; i < data.length; i++) {
            const change = data[i] - data[i - 1];
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }
        
        for (let i = 0; i < data.length; i++) {
            if (i < period) {
                rsi.push(null);
            } else {
                const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                
                if (avgLoss === 0) {
                    rsi.push(100);
                } else {
                    const rs = avgGain / avgLoss;
                    rsi.push(100 - (100 / (1 + rs)));
                }
            }
        }
        
        return rsi;
    }

    /**
     * Calculate MACD
     * @param {Array} data - Price data
     * @param {number} fastPeriod - Fast EMA period
     * @param {number} slowPeriod - Slow EMA period
     * @param {number} signalPeriod - Signal line period
     * @returns {Object} MACD object
     */
    calculateMACD(data, fastPeriod, slowPeriod, signalPeriod) {
        const fastEMA = this.calculateEMA(data, fastPeriod);
        const slowEMA = this.calculateEMA(data, slowPeriod);
        
        const macdLine = fastEMA.map((fast, i) => fast - slowEMA[i]);
        const signalLine = this.calculateEMA(macdLine.filter(val => val !== null), signalPeriod);
        
        // Pad signal line with nulls to match length
        const paddedSignal = new Array(slowPeriod - 1).fill(null).concat(signalLine);
        
        const histogram = macdLine.map((macd, i) => {
            if (macd === null || paddedSignal[i] === null) return null;
            return macd - paddedSignal[i];
        });
        
        return {
            macd: macdLine,
            signal: paddedSignal,
            histogram: histogram
        };
    }

    /**
     * Update chart theme
     * @param {string} newTheme - New theme ('light' or 'dark')
     */
    updateTheme(newTheme) {
        this.theme = newTheme;
        
        if (this.currentChart && this.currentData) {
            const pair = document.getElementById('analysis-pair').value;
            const timeframe = document.getElementById('analysis-timeframe').value;
            this.createChart(this.currentData, pair, timeframe);
        }
    }
}

// Global chart manager instance
window.chartManager = new ChartManager();
