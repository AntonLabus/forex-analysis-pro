"""
Data Validation Module for Forex Analysis Pro
Ensures data integrity and accuracy before displaying to users
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import re

logger = logging.getLogger(__name__)

class ForexDataValidator:
    """Comprehensive data validation for forex price data"""
    
    # Market hour ranges (UTC) for major sessions
    MARKET_SESSIONS = {
        'sydney': {'start': 21, 'end': 6},    # 9 PM - 6 AM UTC
        'tokyo': {'start': 23, 'end': 8},     # 11 PM - 8 AM UTC
        'london': {'start': 7, 'end': 16},    # 7 AM - 4 PM UTC
        'new_york': {'start': 12, 'end': 21}  # 12 PM - 9 PM UTC
    }
    
    # Realistic price ranges for major currency pairs (approximate bounds)
    PRICE_RANGES = {
        'EURUSD': {'min': 0.8000, 'max': 1.5000, 'typical_spread': 0.0001},
        'GBPUSD': {'min': 1.0000, 'max': 2.0000, 'typical_spread': 0.0001},
        'USDJPY': {'min': 80.00, 'max': 160.00, 'typical_spread': 0.01},
        'USDCHF': {'min': 0.7000, 'max': 1.2000, 'typical_spread': 0.0001},
        'AUDUSD': {'min': 0.5000, 'max': 1.1000, 'typical_spread': 0.0001},
        'USDCAD': {'min': 1.0000, 'max': 1.6000, 'typical_spread': 0.0001},
        'NZDUSD': {'min': 0.4000, 'max': 0.9000, 'typical_spread': 0.0001},
        'EURGBP': {'min': 0.7000, 'max': 1.0000, 'typical_spread': 0.0001}
    }
    
    # Maximum allowed price change percentage in short timeframes
    MAX_PRICE_CHANGE = {
        '1m': 0.005,   # 0.5% max change per minute
        '5m': 0.015,   # 1.5% max change per 5 minutes
        '15m': 0.025,  # 2.5% max change per 15 minutes
        '1h': 0.05,    # 5% max change per hour
        '1d': 0.15     # 15% max change per day
    }
    
    def __init__(self):
        self.last_valid_prices = {}
        self.validation_history = []
        
    def validate_price_data(self, pair: str, price: float, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Comprehensive price validation
        
        Args:
            pair: Currency pair symbol (e.g., 'EURUSD')
            price: Current price to validate
            timestamp: Price timestamp (defaults to now)
            
        Returns:
            Dict with validation results and details
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        validation_result = {
            'is_valid': True,
            'price': price,
            'pair': pair,
            'timestamp': timestamp,
            'warnings': [],
            'errors': [],
            'confidence_score': 100,
            'validation_checks': {}
        }
        
        try:
            # 1. Basic format validation
            self._validate_price_format(pair, price, validation_result)
            
            # 2. Range validation
            self._validate_price_range(pair, price, validation_result)
            
            # 3. Market hours validation
            self._validate_market_hours(timestamp, validation_result)
            
            # 4. Price change validation
            self._validate_price_change(pair, price, timestamp, validation_result)
            
            # 5. Timestamp validation
            self._validate_timestamp(timestamp, validation_result)
            
            # 6. Data freshness validation
            self._validate_data_freshness(timestamp, validation_result)
            
            # Calculate overall confidence score
            self._calculate_confidence_score(validation_result)
            
            # Store valid price for future comparisons
            if validation_result['is_valid'] and validation_result['confidence_score'] >= 70:
                self.last_valid_prices[pair] = {
                    'price': price,
                    'timestamp': timestamp
                }
            
            # Log validation result
            self._log_validation_result(validation_result)
            
        except Exception as e:
            logger.error(f"Validation error for {pair}: {e}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation exception: {str(e)}")
            validation_result['confidence_score'] = 0
            
        return validation_result
    
    def _validate_price_format(self, pair: str, price: float, result: Dict) -> None:
        """Validate price format and basic constraints"""
        checks = {}
        
        # Check if price is a valid number
        if not isinstance(price, (int, float)) or price <= 0:
            result['errors'].append(f"Invalid price format: {price}")
            result['is_valid'] = False
            checks['format'] = False
        else:
            checks['format'] = True
            
        # Check for reasonable decimal precision
        price_str = str(price)
        if '.' in price_str:
            decimal_places = len(price_str.split('.')[1])
            if pair.endswith('JPY'):
                # JPY pairs typically have 2-3 decimal places
                if decimal_places > 3:
                    result['warnings'].append(f"Unusual precision for JPY pair: {decimal_places} decimals")
                    checks['precision'] = False
                else:
                    checks['precision'] = True
            else:
                # Other pairs typically have 4-5 decimal places
                if decimal_places > 5:
                    result['warnings'].append(f"Unusual precision: {decimal_places} decimals")
                    checks['precision'] = False
                else:
                    checks['precision'] = True
        else:
            checks['precision'] = True
            
        result['validation_checks']['format'] = checks
    
    def _validate_price_range(self, pair: str, price: float, result: Dict) -> None:
        """Validate price is within reasonable range for the currency pair"""
        checks = {}
        
        if pair in self.PRICE_RANGES:
            price_range = self.PRICE_RANGES[pair]
            
            if price < price_range['min']:
                result['errors'].append(f"Price {price} below minimum expected range {price_range['min']}")
                result['is_valid'] = False
                checks['min_range'] = False
            else:
                checks['min_range'] = True
                
            if price > price_range['max']:
                result['errors'].append(f"Price {price} above maximum expected range {price_range['max']}")
                result['is_valid'] = False
                checks['max_range'] = False
            else:
                checks['max_range'] = True
                
            checks['within_range'] = checks['min_range'] and checks['max_range']
        else:
            result['warnings'].append(f"No price range validation available for {pair}")
            checks['within_range'] = True  # Assume valid if no range defined
            
        result['validation_checks']['range'] = checks
    
    def _validate_market_hours(self, timestamp: datetime, result: Dict) -> None:
        """Validate if timestamp falls within market hours"""
        checks = {}
        
        # Check if it's weekend (Saturday/Sunday)
        weekday = timestamp.weekday()
        if weekday >= 5:  # Saturday = 5, Sunday = 6
            # Check if it's during weekend market close
            if weekday == 5 and timestamp.hour >= 21:  # Friday after 9 PM UTC
                checks['weekend'] = True  # Still valid
            elif weekday == 6 and timestamp.hour < 21:  # Sunday before 9 PM UTC
                checks['weekend'] = True  # Still valid
            else:
                result['warnings'].append("Price during weekend market hours")
                checks['weekend'] = False
        else:
            checks['weekend'] = True
            
        # Check if during any major trading session
        hour = timestamp.hour
        in_session = False
        
        for session_name, session_hours in self.MARKET_SESSIONS.items():
            start = session_hours['start']
            end = session_hours['end']
            
            if start > end:  # Session crosses midnight
                if hour >= start or hour <= end:
                    in_session = True
                    break
            else:  # Normal session
                if start <= hour <= end:
                    in_session = True
                    break
                    
        checks['trading_session'] = in_session
        if not in_session:
            result['warnings'].append("Price outside major trading sessions")
            
        result['validation_checks']['market_hours'] = checks
    
    def _validate_price_change(self, pair: str, price: float, timestamp: datetime, result: Dict) -> None:
        """Validate price change against previous price"""
        checks = {}
        
        if pair in self.last_valid_prices:
            last_data = self.last_valid_prices[pair]
            last_price = last_data['price']
            last_timestamp = last_data['timestamp']
            
            # Calculate time difference
            time_diff = timestamp - last_timestamp
            time_diff_minutes = time_diff.total_seconds() / 60
            
            # Calculate price change percentage
            price_change = abs(price - last_price) / last_price
            
            # Determine appropriate threshold based on time difference
            threshold = self._get_price_change_threshold(time_diff_minutes)
            
            if price_change > threshold:
                if price_change > threshold * 2:  # Extreme change
                    result['errors'].append(
                        f"Extreme price change: {price_change:.4f} ({price_change*100:.2f}%) "
                        f"in {time_diff_minutes:.1f} minutes"
                    )
                    result['is_valid'] = False
                    checks['extreme_change'] = False
                else:  # Significant change
                    result['warnings'].append(
                        f"Significant price change: {price_change:.4f} ({price_change*100:.2f}%) "
                        f"in {time_diff_minutes:.1f} minutes"
                    )
                    checks['extreme_change'] = True
            else:
                checks['extreme_change'] = True
                
            checks['reasonable_change'] = price_change <= threshold
            checks['price_change_percent'] = price_change * 100
            checks['time_diff_minutes'] = time_diff_minutes
            
        else:
            # No previous price to compare
            checks['reasonable_change'] = True
            checks['extreme_change'] = True
            
        result['validation_checks']['price_change'] = checks
    
    def _get_price_change_threshold(self, minutes: float) -> float:
        """Get appropriate price change threshold based on time difference"""
        if minutes <= 1:
            return self.MAX_PRICE_CHANGE['1m']
        elif minutes <= 5:
            return self.MAX_PRICE_CHANGE['5m']
        elif minutes <= 15:
            return self.MAX_PRICE_CHANGE['15m']
        elif minutes <= 60:
            return self.MAX_PRICE_CHANGE['1h']
        else:
            return self.MAX_PRICE_CHANGE['1d']
    
    def _validate_timestamp(self, timestamp: datetime, result: Dict) -> None:
        """Validate timestamp is reasonable"""
        checks = {}
        now = datetime.utcnow()
        
        # Check if timestamp is in the future
        if timestamp > now + timedelta(minutes=5):  # Allow 5 minutes tolerance
            result['errors'].append(f"Timestamp is in the future: {timestamp}")
            result['is_valid'] = False
            checks['future'] = False
        else:
            checks['future'] = True
            
        # Check if timestamp is too old
        if timestamp < now - timedelta(hours=24):
            result['warnings'].append(f"Timestamp is older than 24 hours: {timestamp}")
            checks['stale'] = False
        else:
            checks['stale'] = True
            
        result['validation_checks']['timestamp'] = checks
    
    def _validate_data_freshness(self, timestamp: datetime, result: Dict) -> None:
        """Validate data freshness for real-time requirements"""
        checks = {}
        now = datetime.utcnow()
        age_seconds = (now - timestamp).total_seconds()
        
        if age_seconds > 300:  # 5 minutes
            result['warnings'].append(f"Data is {age_seconds/60:.1f} minutes old")
            checks['fresh'] = False
        else:
            checks['fresh'] = True
            
        if age_seconds > 3600:  # 1 hour
            result['errors'].append(f"Data is severely stale: {age_seconds/3600:.1f} hours old")
            result['is_valid'] = False
            checks['severely_stale'] = True
        else:
            checks['severely_stale'] = False
            
        checks['age_seconds'] = age_seconds
        result['validation_checks']['freshness'] = checks
    
    def _calculate_confidence_score(self, result: Dict) -> None:
        """Calculate overall confidence score based on validation results"""
        score = 100
        
        # Severe penalties for errors
        if not result['is_valid']:
            score -= 50
            
        # Penalties for each warning
        score -= len(result['warnings']) * 10
        
        # Specific check penalties
        checks = result['validation_checks']
        
        # Format issues
        if 'format' in checks and not checks['format'].get('format', True):
            score -= 30
            
        # Range issues
        if 'range' in checks and not checks['range'].get('within_range', True):
            score -= 25
            
        # Price change issues
        if 'price_change' in checks:
            pc_checks = checks['price_change']
            if not pc_checks.get('reasonable_change', True):
                score -= 15
            if not pc_checks.get('extreme_change', True):
                score -= 35
                
        # Freshness issues
        if 'freshness' in checks:
            fresh_checks = checks['freshness']
            if not fresh_checks.get('fresh', True):
                score -= 10
            if fresh_checks.get('severely_stale', False):
                score -= 30
                
        # Market hours issues
        if 'market_hours' in checks:
            mh_checks = checks['market_hours']
            if not mh_checks.get('trading_session', True):
                score -= 5
            if not mh_checks.get('weekend', True):
                score -= 10
                
        # Ensure score doesn't go below 0
        result['confidence_score'] = max(0, score)
    
    def _log_validation_result(self, result: Dict) -> None:
        """Log validation results for monitoring"""
        pair = result['pair']
        score = result['confidence_score']
        
        if not result['is_valid']:
            logger.error(f"INVALID price for {pair}: {result['price']} (errors: {result['errors']})")
        elif result['warnings']:
            logger.warning(f"Price warning for {pair}: {result['price']} (score: {score}, warnings: {result['warnings']})")
        else:
            logger.debug(f"Valid price for {pair}: {result['price']} (score: {score})")
            
        # Store in history for analysis
        self.validation_history.append({
            'timestamp': result['timestamp'],
            'pair': pair,
            'price': result['price'],
            'is_valid': result['is_valid'],
            'confidence_score': score,
            'error_count': len(result['errors']),
            'warning_count': len(result['warnings'])
        })
        
        # Keep only last 1000 validation records
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics for monitoring"""
        if not self.validation_history:
            return {
                'total_validations': 0,
                'valid_percentage': 0,
                'average_confidence_score': 0,
                'recent_validations_1h': 0,
                'last_validation': None
            }
            
        total = len(self.validation_history)
        valid_count = sum(1 for v in self.validation_history if v['is_valid'])
        avg_score = sum(v['confidence_score'] for v in self.validation_history) / total
        
        recent_validations = [v for v in self.validation_history 
                            if (datetime.utcnow() - v['timestamp']).total_seconds() < 3600]
        
        return {
            'total_validations': total,
            'valid_percentage': (valid_count / total) * 100,
            'average_confidence_score': avg_score,
            'recent_validations_1h': len(recent_validations),
            'last_validation': self.validation_history[-1] if self.validation_history else None
        }

# Global validator instance
validator = ForexDataValidator()

def validate_forex_data(pair: str, price: float, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
    """Convenience function for validating forex data"""
    return validator.validate_price_data(pair, price, timestamp)
