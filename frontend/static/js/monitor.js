/**
 * System Monitoring Dashboard
 * Displays API rate limiting status, health metrics, and system statistics
 */

class SystemMonitor {
    constructor() {
        this.updateInterval = 30000; // Update every 30 seconds
        this.intervalId = null;
        this.isVisible = false;
        this.rateLimitData = null;
        this.healthData = null;
        
        this.initializeMonitor();
    }

    initializeMonitor() {
        this.createMonitorUI();
        this.bindEvents();
        this.startMonitoring();
    }

    createMonitorUI() {
        // Create monitor toggle button
        const toggleButton = document.createElement('button');
        toggleButton.id = 'monitor-toggle';
        toggleButton.className = 'monitor-toggle';
        toggleButton.innerHTML = '📊 Monitor';
        toggleButton.title = 'System Monitor';
        document.body.appendChild(toggleButton);

        // Create monitor panel
        const monitorPanel = document.createElement('div');
        monitorPanel.id = 'system-monitor';
        monitorPanel.className = 'system-monitor hidden';
        monitorPanel.innerHTML = `
            <div class="monitor-header">
                <h3>System Monitor</h3>
                <button id="monitor-close" class="monitor-close">×</button>
            </div>
            <div class="monitor-content">
                <div class="monitor-section">
                    <h4>API Rate Limits</h4>
                    <div id="rate-limits-status" class="status-grid">
                        <div class="loading">Loading...</div>
                    </div>
                </div>
                <div class="monitor-section">
                    <h4>System Health</h4>
                    <div id="system-health-status" class="health-grid">
                        <div class="loading">Loading...</div>
                    </div>
                </div>
                <div class="monitor-section">
                    <h4>Recommendations</h4>
                    <div id="system-recommendations" class="recommendations-list">
                        <div class="loading">Loading...</div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(monitorPanel);
    }

    bindEvents() {
        const toggleButton = document.getElementById('monitor-toggle');
        const closeButton = document.getElementById('monitor-close');
        const monitorPanel = document.getElementById('system-monitor');

        toggleButton.addEventListener('click', () => this.toggleMonitor());
        closeButton.addEventListener('click', () => this.hideMonitor());
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (this.isVisible && 
                !monitorPanel.contains(e.target) && 
                !toggleButton.contains(e.target)) {
                this.hideMonitor();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isVisible) {
                this.hideMonitor();
            }
        });
    }

    toggleMonitor() {
        if (this.isVisible) {
            this.hideMonitor();
        } else {
            this.showMonitor();
        }
    }

    showMonitor() {
        const monitorPanel = document.getElementById('system-monitor');
        monitorPanel.classList.remove('hidden');
        this.isVisible = true;
        this.updateMonitorData();
    }

    hideMonitor() {
        const monitorPanel = document.getElementById('system-monitor');
        monitorPanel.classList.add('hidden');
        this.isVisible = false;
    }

    startMonitoring() {
        this.updateMonitorData();
        this.intervalId = setInterval(() => {
            this.updateMonitorData();
        }, this.updateInterval);
    }

    stopMonitoring() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    async updateMonitorData() {
        try {
            // Fetch rate limits and health data in parallel
            const [rateLimitsResponse, healthResponse] = await Promise.all([
                fetch(CONFIG.ENDPOINTS.RATE_LIMITS),
                fetch(CONFIG.ENDPOINTS.SYSTEM_HEALTH)
            ]);

            if (rateLimitsResponse.ok) {
                this.rateLimitData = await rateLimitsResponse.json();
                this.updateRateLimitsDisplay();
            }

            if (healthResponse.ok) {
                this.healthData = await healthResponse.json();
                this.updateHealthDisplay();
                this.updateRecommendationsDisplay();
            }

            // Update monitor toggle button color based on health
            this.updateToggleButtonStatus();

        } catch (error) {
            console.error('Failed to update monitor data:', error);
            this.showErrorState();
        }
    }

    updateRateLimitsDisplay() {
        const container = document.getElementById('rate-limits-status');
        if (!this.rateLimitData) return;

        const html = Object.entries(this.rateLimitData.limits || {}).map(([api, data]) => {
            const usagePercent = (data.current / data.limit) * 100;
            const statusClass = this.getRateLimitStatusClass(usagePercent);
            const timeRemaining = this.formatTimeRemaining(data.reset_time);

            return `
                <div class="rate-limit-item ${statusClass}">
                    <div class="api-name">${this.formatApiName(api)}</div>
                    <div class="usage-bar">
                        <div class="usage-fill" style="width: ${usagePercent}%"></div>
                    </div>
                    <div class="usage-text">${data.current}/${data.limit}</div>
                    <div class="reset-time">Resets in ${timeRemaining}</div>
                </div>
            `;
        }).join('');

        container.innerHTML = html || '<div class="no-data">No rate limit data available</div>';
    }

    updateHealthDisplay() {
        const container = document.getElementById('system-health-status');
        if (!this.healthData) return;

        const health = this.healthData;
        const overallStatus = this.getHealthStatusClass(health.health_score);

        const html = `
            <div class="health-overview ${overallStatus}">
                <div class="health-score">
                    <span class="score-value">${health.health_score}</span>
                    <span class="score-label">Health Score</span>
                </div>
                <div class="health-status">
                    <span class="status-label">${this.getHealthStatusLabel(health.health_score)}</span>
                </div>
            </div>
            <div class="health-metrics">
                <div class="metric">
                    <span class="metric-label">Uptime</span>
                    <span class="metric-value">${this.formatUptime(health.uptime_seconds)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Requests</span>
                    <span class="metric-value">${health.total_requests.toLocaleString()}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Error Rate</span>
                    <span class="metric-value">${health.error_rate.toFixed(2)}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Avg Response</span>
                    <span class="metric-value">${health.avg_response_time}ms</span>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    updateRecommendationsDisplay() {
        const container = document.getElementById('system-recommendations');
        if (!this.healthData || !this.healthData.recommendations) return;

        const recommendations = this.healthData.recommendations;
        if (recommendations.length === 0) {
            container.innerHTML = '<div class="no-recommendations">✅ All systems operating optimally</div>';
            return;
        }

        const html = recommendations.map(rec => `
            <div class="recommendation-item ${rec.priority}">
                <div class="rec-priority">${rec.priority.toUpperCase()}</div>
                <div class="rec-message">${rec.message}</div>
                ${rec.action ? `<div class="rec-action">${rec.action}</div>` : ''}
            </div>
        `).join('');

        container.innerHTML = html;
    }

    updateToggleButtonStatus() {
        const toggleButton = document.getElementById('monitor-toggle');
        if (!this.healthData) return;

        const healthScore = this.healthData.health_score;
        toggleButton.className = `monitor-toggle ${this.getHealthStatusClass(healthScore)}`;
        
        // Add warning indicator for critical issues
        if (healthScore < 50) {
            toggleButton.innerHTML = '⚠️ Monitor';
        } else if (healthScore < 80) {
            toggleButton.innerHTML = '⚡ Monitor';
        } else {
            toggleButton.innerHTML = '📊 Monitor';
        }
    }

    showErrorState() {
        const rateLimitsContainer = document.getElementById('rate-limits-status');
        const healthContainer = document.getElementById('system-health-status');
        const recsContainer = document.getElementById('system-recommendations');

        rateLimitsContainer.innerHTML = '<div class="error-state">❌ Failed to load rate limits</div>';
        healthContainer.innerHTML = '<div class="error-state">❌ Failed to load health data</div>';
        recsContainer.innerHTML = '<div class="error-state">❌ Failed to load recommendations</div>';
    }

    // Utility methods
    getRateLimitStatusClass(usagePercent) {
        if (usagePercent >= 90) return 'critical';
        if (usagePercent >= 75) return 'warning';
        if (usagePercent >= 50) return 'caution';
        return 'good';
    }

    getHealthStatusClass(score) {
        if (score >= 80) return 'healthy';
        if (score >= 60) return 'warning';
        return 'critical';
    }

    getHealthStatusLabel(score) {
        if (score >= 80) return 'Healthy';
        if (score >= 60) return 'Warning';
        return 'Critical';
    }

    formatApiName(api) {
        return api.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatTimeRemaining(resetTime) {
        if (!resetTime) return 'Unknown';
        
        const now = new Date();
        const reset = new Date(resetTime);
        const diff = reset - now;
        
        if (diff <= 0) return 'Now';
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 0) return `${hours}h ${minutes}m`;
        return `${minutes}m`;
    }

    formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (days > 0) return `${days}d ${hours}h ${minutes}m`;
        if (hours > 0) return `${hours}h ${minutes}m`;
        return `${minutes}m`;
    }

    // Public methods for external control
    destroy() {
        this.stopMonitoring();
        
        // Remove UI elements
        const toggleButton = document.getElementById('monitor-toggle');
        const monitorPanel = document.getElementById('system-monitor');
        
        if (toggleButton) toggleButton.remove();
        if (monitorPanel) monitorPanel.remove();
    }

    refresh() {
        this.updateMonitorData();
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.systemMonitor = new SystemMonitor();
});
