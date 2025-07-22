"""
Data Fetcher Module - No Dependencies Version
Handles fetching real-time and historical forex data without pandas
"""

import yfinance as yf
import requests
from datetime import datetime, timedelta
import logging
import os
from typing import Optional, Dict, Any, List
import time
import json
import random

logger = logging.getLogger(__name__)

class DataFetcher:
    """
    Fetches forex data from multiple sources with fallback mechanisms
    """
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.cache = {}
        self.cache_expiry = {}
        
        # Yahoo Finance forex pair mapping
        self.yahoo_pairs = {
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X',
            'USDJPY': 'USDJPY=X',
            'USDCHF': 'USDCHF=X',
            'AUDUSD': 'AUDUSD=X',
            'USDCAD': 'USDCAD=X',
            'NZDUSD': 'NZDUSD=X',
            'EURGBP': 'EURGBP=X',
            'EURJPY': 'EURJPY=X',
            'GBPJPY': 'GBPJPY=X'
        }
        
        # Cache duration in seconds
        self.cache_duration = 60  # 1 minute for live data
        
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[key]
    
    def _set_cache(self, key: str, data: Any, duration: int = None):
        """Set cache with expiry"""
        if duration is None:
            duration = self.cache_duration
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=duration)
    
    def get_live_price(self, pair: str) -> Optional[Dict[str, Any]]:
        """
        Get current live price for a forex pair
        """
        cache_key = f"live_{pair}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        try:
            # Try Yahoo Finance first
            yahoo_symbol = self.yahoo_pairs.get(pair)
            if yahoo_symbol:
                price_data = self._fetch_yahoo_live_price(yahoo_symbol, pair)
                if price_data:
                    self._set_cache(cache_key, price_data)
                    return price_data
            
            # Fallback to mock data for demo
            price_data = self._generate_mock_price(pair)
            self._set_cache(cache_key, price_data, 30)  # Cache mock data for 30 seconds
            return price_data
            
        except Exception as e:
            logger.error(f"Error fetching live price for {pair}: {str(e)}")
            return self._generate_mock_price(pair)
    
    def _fetch_yahoo_live_price(self, yahoo_symbol: str, pair: str) -> Optional[Dict[str, Any]]:
        """Fetch live price from Yahoo Finance"""
        try:
            ticker = yf.Ticker(yahoo_symbol)
            info = ticker.info
            
            if 'regularMarketPrice' in info:
                current_price = info['regularMarketPrice']
                previous_close = info.get('previousClose', current_price)
                
                # Calculate change
                daily_change = current_price - previous_close
                daily_change_percent = (daily_change / previous_close * 100) if previous_close > 0 else 0
                
                return {
                    'symbol': pair,
                    'current_price': current_price,
                    'previous_close': previous_close,
                    'daily_change': daily_change,
                    'daily_change_percent': daily_change_percent,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'yahoo_finance'
                }
        except Exception as e:
            logger.warning(f"Yahoo Finance failed for {yahoo_symbol}: {str(e)}")
            return None
    
    def _generate_mock_price(self, pair: str) -> Dict[str, Any]:
        """Generate realistic mock price data for demo purposes"""
        
        # Base prices for major pairs
        base_prices = {
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'USDJPY': 149.50,
            'USDCHF': 0.8750,
            'AUDUSD': 0.6650,
            'USDCAD': 1.3580,
            'NZDUSD': 0.6150,
            'EURGBP': 0.8580
        }
        
        base_price = base_prices.get(pair, 1.0000)
        
        # Add some realistic random movement
        price_movement = random.uniform(-0.002, 0.002)  # +/- 0.2%
        current_price = base_price * (1 + price_movement)
        
        # Calculate previous close (slight variation)
        previous_close = base_price * (1 + random.uniform(-0.001, 0.001))
        
        daily_change = current_price - previous_close
        daily_change_percent = (daily_change / previous_close * 100) if previous_close > 0 else 0
        
        return {
            'symbol': pair,
            'current_price': round(current_price, 5),
            'previous_close': round(previous_close, 5),
            'daily_change': round(daily_change, 5),
            'daily_change_percent': round(daily_change_percent, 3),
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_data'
        }
    
    def get_historical_data(self, pair: str, period: str = "3mo", interval: str = "1h") -> List[Dict[str, Any]]:
        """
        Get historical price data for a forex pair
        """
        cache_key = f"historical_{pair}_{period}_{interval}"
        
        # Check cache (longer duration for historical data)
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        try:
            # Try Yahoo Finance
            yahoo_symbol = self.yahoo_pairs.get(pair)
            if yahoo_symbol:
                historical_data = self._fetch_yahoo_historical(yahoo_symbol, period, interval)
                if historical_data:
                    self._set_cache(cache_key, historical_data, 300)  # Cache for 5 minutes
                    return historical_data
            
            # Fallback to mock historical data
            historical_data = self._generate_mock_historical(pair, period, interval)
            self._set_cache(cache_key, historical_data, 300)
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {pair}: {str(e)}")
            return self._generate_mock_historical(pair, period, interval)
    
    def _fetch_yahoo_historical(self, yahoo_symbol: str, period: str, interval: str) -> List[Dict[str, Any]]:
        """Fetch historical data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(yahoo_symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                return []
            
            # Convert to list of dictionaries
            data = []
            for timestamp, row in hist.iterrows():
                data.append({
                    'timestamp': timestamp.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']) if row['Volume'] == row['Volume'] else 0  # Check for NaN
                })
            
            logger.info(f"Fetched {len(data)} historical data points for {yahoo_symbol}")
            return data
            
        except Exception as e:
            logger.warning(f"Yahoo Finance historical data failed for {yahoo_symbol}: {str(e)}")
            return []
    
    def _generate_mock_historical(self, pair: str, period: str, interval: str) -> List[Dict[str, Any]]:
        """Generate mock historical data for demo purposes"""
        
        # Determine number of data points based on period and interval
        period_hours = {
            "1d": 24,
            "5d": 120,
            "1mo": 720,
            "3mo": 2160,
            "6mo": 4320,
            "1y": 8760
        }
        
        interval_hours = {
            "1m": 1/60,
            "5m": 5/60,
            "15m": 15/60,
            "30m": 0.5,
            "1h": 1,
            "1d": 24
        }
        
        total_hours = period_hours.get(period, 720)
        interval_hour = interval_hours.get(interval, 1)
        num_points = min(int(total_hours / interval_hour), 1000)  # Limit to 1000 points
        
        # Base price for the pair
        base_prices = {
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'USDJPY': 149.50,
            'USDCHF': 0.8750,
            'AUDUSD': 0.6650,
            'USDCAD': 1.3580,
            'NZDUSD': 0.6150,
            'EURGBP': 0.8580
        }
        
        base_price = base_prices.get(pair, 1.0000)
        current_price = base_price
        
        data = []
        now = datetime.now()
        
        for i in range(num_points):
            # Create timestamp
            timestamp = now - timedelta(hours=(num_points - i) * interval_hour)
            
            # Generate realistic OHLC data
            price_change = random.uniform(-0.001, 0.001)  # +/- 0.1% per interval
            current_price *= (1 + price_change)
            
            # Generate OHLC around current price
            volatility = random.uniform(0.0001, 0.0005)  # Intraday volatility
            
            open_price = current_price * (1 + random.uniform(-volatility, volatility))
            close_price = current_price * (1 + random.uniform(-volatility, volatility))
            high_price = max(open_price, close_price) * (1 + random.uniform(0, volatility))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, volatility))
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'open': round(open_price, 5),
                'high': round(high_price, 5),
                'low': round(low_price, 5),
                'close': round(close_price, 5),
                'volume': random.randint(1000, 10000)
            })
        
        logger.info(f"Generated {len(data)} mock historical data points for {pair}")
        return data
    
    def get_forex_pairs_data(self) -> List[Dict[str, Any]]:
        """Get live data for all major forex pairs"""
        pairs_data = []
        
        for pair in self.yahoo_pairs.keys():
            try:
                price_data = self.get_live_price(pair)
                if price_data:
                    pairs_data.append(price_data)
                    
                # Small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error fetching data for {pair}: {str(e)}")
                continue
        
        logger.info(f"Fetched data for {len(pairs_data)} forex pairs")
        return pairs_data

# Global instance
data_fetcher = DataFetcher()
