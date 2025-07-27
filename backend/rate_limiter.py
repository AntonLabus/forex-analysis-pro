"""
Advanced Rate Limiter for Forex Analysis Pro
Monitors and controls API request rates across all data sources
"""

import time
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class APIUsageStats:
    """Statistics for API usage"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rate_limited_requests: int = 0
    last_request_time: float = 0
    hourly_count: int = 0
    daily_count: int = 0
    last_reset: float = 0

class RateLimiter:
    """
    Advanced rate limiter with per-API tracking and smart throttling
    """
    
    def __init__(self):
        self.api_stats: Dict[str, APIUsageStats] = {}
        self.global_stats = APIUsageStats()
        self.request_history: List[Dict] = []
        
        # Rate limits per API (requests per hour)
        self.rate_limits = {
            'yahoo_finance': 100,
            'alpha_vantage': 20,  # Conservative for free tier
            'exchangerate_api': 50,
            'exchangerate_host': 500,
            'fawaz_currency': 1000
        }
        
        # Throttling delays (seconds)
        self.throttle_delays = {
            'yahoo_finance': 1.0,
            'alpha_vantage': 3.0,
            'exchangerate_api': 1.5,
            'exchangerate_host': 0.5,
            'fawaz_currency': 0.2
        }
        
        self.max_daily_requests = 5000
        self.max_hourly_requests = 300
        
    def get_or_create_stats(self, api_name: str) -> APIUsageStats:
        """Get or create stats for an API"""
        if api_name not in self.api_stats:
            self.api_stats[api_name] = APIUsageStats(last_reset=time.time())
        return self.api_stats[api_name]
    
    def reset_counters_if_needed(self, api_name: str) -> None:
        """Reset hourly/daily counters if time windows have passed"""
        stats = self.get_or_create_stats(api_name)
        current_time = time.time()
        
        # Reset hourly counter
        if current_time - stats.last_reset >= 3600:  # 1 hour
            stats.hourly_count = 0
            stats.last_reset = current_time
            
        # Reset daily counter
        if current_time - stats.last_reset >= 86400:  # 24 hours
            stats.daily_count = 0
    
    def can_make_request(self, api_name: str) -> bool:
        """
        Check if we can make a request to the specified API
        
        Args:
            api_name: Name of the API
            
        Returns:
            True if request is allowed, False if rate limited
        """
        self.reset_counters_if_needed(api_name)
        stats = self.get_or_create_stats(api_name)
        
        # Check global limits
        if self.global_stats.daily_count >= self.max_daily_requests:
            logger.warning(f"Global daily limit ({self.max_daily_requests}) reached")
            return False
            
        if self.global_stats.hourly_count >= self.max_hourly_requests:
            logger.warning(f"Global hourly limit ({self.max_hourly_requests}) reached")
            return False
        
        # Check API-specific limits
        api_limit = self.rate_limits.get(api_name, 100)
        if stats.hourly_count >= api_limit:
            logger.warning(f"{api_name} hourly limit ({api_limit}) reached")
            stats.rate_limited_requests += 1
            return False
        
        # Special handling for Alpha Vantage daily limit
        if api_name == 'alpha_vantage' and stats.daily_count >= 20:
            logger.warning(f"Alpha Vantage daily limit (20) reached")
            stats.rate_limited_requests += 1
            return False
        
        return True
    
    def record_request(self, api_name: str, success: bool = True, response_time: float = 0) -> None:
        """
        Record a request to the specified API
        
        Args:
            api_name: Name of the API
            success: Whether the request was successful
            response_time: Response time in seconds
        """
        stats = self.get_or_create_stats(api_name)
        current_time = time.time()
        
        # Update API stats
        stats.total_requests += 1
        stats.hourly_count += 1
        stats.daily_count += 1
        stats.last_request_time = current_time
        
        if success:
            stats.successful_requests += 1
        else:
            stats.failed_requests += 1
        
        # Update global stats
        self.global_stats.total_requests += 1
        self.global_stats.hourly_count += 1
        self.global_stats.daily_count += 1
        self.global_stats.last_request_time = current_time
        
        if success:
            self.global_stats.successful_requests += 1
        else:
            self.global_stats.failed_requests += 1
        
        # Add to request history (keep last 100 requests)
        self.request_history.append({
            'timestamp': current_time,
            'api': api_name,
            'success': success,
            'response_time': response_time
        })
        
        if len(self.request_history) > 100:
            self.request_history.pop(0)
        
        # Apply throttling delay
        delay = self.throttle_delays.get(api_name, 1.0)
        if delay > 0:
            time.sleep(delay)
        
        logger.debug(f"Recorded {api_name} request: success={success}, total={stats.total_requests}")
    
    def get_throttle_delay(self, api_name: str) -> float:
        """Get the throttling delay for an API"""
        return self.throttle_delays.get(api_name, 1.0)
    
    def get_usage_stats(self) -> Dict:
        """Get comprehensive usage statistics"""
        current_time = time.time()
        
        # Calculate request rates
        recent_requests = [r for r in self.request_history if current_time - r['timestamp'] <= 300]  # Last 5 minutes
        requests_per_minute = len(recent_requests) / 5 if recent_requests else 0
        
        return {
            'global': {
                'total_requests': self.global_stats.total_requests,
                'successful_requests': self.global_stats.successful_requests,
                'failed_requests': self.global_stats.failed_requests,
                'rate_limited_requests': self.global_stats.rate_limited_requests,
                'hourly_count': self.global_stats.hourly_count,
                'daily_count': self.global_stats.daily_count,
                'requests_per_minute': round(requests_per_minute, 2),
                'success_rate': round((self.global_stats.successful_requests / max(self.global_stats.total_requests, 1)) * 100, 2)
            },
            'by_api': {
                api_name: {
                    'total_requests': stats.total_requests,
                    'successful_requests': stats.successful_requests,
                    'failed_requests': stats.failed_requests,
                    'rate_limited_requests': stats.rate_limited_requests,
                    'hourly_count': stats.hourly_count,
                    'daily_count': stats.daily_count,
                    'hourly_limit': self.rate_limits.get(api_name, 100),
                    'usage_percentage': round((stats.hourly_count / self.rate_limits.get(api_name, 100)) * 100, 2)
                }
                for api_name, stats in self.api_stats.items()
            },
            'recent_requests': self.request_history[-10:],  # Last 10 requests
            'limits': {
                'daily_limit': self.max_daily_requests,
                'hourly_limit': self.max_hourly_requests,
                'daily_usage': self.global_stats.daily_count,
                'hourly_usage': self.global_stats.hourly_count
            }
        }
    
    def get_health_status(self) -> Dict:
        """Get system health status based on usage"""
        stats = self.get_usage_stats()
        global_stats = stats['global']
        
        # Calculate health score (0-100)
        health_score = 100
        
        # Deduct points for high usage
        daily_usage_pct = (global_stats['daily_count'] / self.max_daily_requests) * 100
        hourly_usage_pct = (global_stats['hourly_count'] / self.max_hourly_requests) * 100
        
        health_score -= max(0, daily_usage_pct - 50)  # Deduct after 50% daily usage
        health_score -= max(0, hourly_usage_pct - 70)  # Deduct after 70% hourly usage
        
        # Deduct points for failures
        if global_stats['total_requests'] > 0:
            failure_rate = (global_stats['failed_requests'] / global_stats['total_requests']) * 100
            health_score -= failure_rate
        
        health_score = max(0, min(100, health_score))
        
        # Determine status
        if health_score >= 80:
            status = 'healthy'
        elif health_score >= 60:
            status = 'warning'
        else:
            status = 'critical'
        
        return {
            'status': status,
            'health_score': round(health_score, 2),
            'daily_usage_pct': round(daily_usage_pct, 2),
            'hourly_usage_pct': round(hourly_usage_pct, 2),
            'success_rate': global_stats['success_rate'],
            'recommendations': self._get_recommendations(health_score, daily_usage_pct, hourly_usage_pct)
        }
    
    def _get_recommendations(self, health_score: float, daily_usage: float, hourly_usage: float) -> List[str]:
        """Get recommendations based on current usage"""
        recommendations = []
        
        if daily_usage > 80:
            recommendations.append("Daily usage is high. Consider caching more aggressively.")
        
        if hourly_usage > 80:
            recommendations.append("Hourly usage is high. Increase request intervals.")
        
        if health_score < 60:
            recommendations.append("System health is critical. Review API usage patterns.")
        
        # Check individual API usage
        for api_name, stats in self.api_stats.items():
            limit = self.rate_limits.get(api_name, 100)
            usage_pct = (stats.hourly_count / limit) * 100
            
            if usage_pct > 90:
                recommendations.append(f"{api_name} is near rate limit. Consider alternative sources.")
        
        return recommendations

# Global rate limiter instance
rate_limiter = RateLimiter()
