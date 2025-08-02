"""
Technical Analysis Module - Simplified Version
Provides technical analysis for forex pairs without TA-Lib dependency
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    """
    Simplified technical analysis engine for forex data
    """
    
    def __init__(self):
        self.last_analysis = None
        self.cache_timeout = 300  # 5 minutes
        
    def calculate_sma(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return data.rolling(window=period, min_periods=1).mean()
    
    def calculate_ema(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, data: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()
        
        # Avoid division by zero
        rs = gain / loss.replace(0, np.inf)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)  # Fill NaN with neutral value
    
    def calculate_macd(self, data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD"""
        ema_fast = self.calculate_ema(data, fast)
        ema_slow = self.calculate_ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self.calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(self, data: pd.Series, period: int = 20, std_dev: float = 2) -> Dict:
        """Calculate Bollinger Bands"""
        sma = self.calculate_sma(data, period)
        std = data.rolling(window=period, min_periods=1).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        return {
            'upper': upper,
            'middle': sma,
            'lower': lower
        }
    
    def calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                           k_period: int = 14, d_period: int = 3) -> Dict:
        """Calculate Stochastic Oscillator"""
        lowest_low = low.rolling(window=k_period, min_periods=1).min()
        highest_high = high.rolling(window=k_period, min_periods=1).max()
        
        # Avoid division by zero
        denominator = highest_high - lowest_low
        denominator = denominator.replace(0, 0.0001)  # Small value to avoid division by zero
        
        k_percent = 100 * ((close - lowest_low) / denominator)
        d_percent = self.calculate_sma(k_percent, d_period)
        
        return {
            'k': k_percent.fillna(50),
            'd': d_percent.fillna(50)
        }
    
    def calculate_williams_r(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Williams %R"""
        highest_high = high.rolling(window=period, min_periods=1).max()
        lowest_low = low.rolling(window=period, min_periods=1).min()
        
        denominator = highest_high - lowest_low
        denominator = denominator.replace(0, 0.0001)
        
        williams_r = -100 * ((highest_high - close) / denominator)
        return williams_r.fillna(-50)
    
    def find_important_price_points(self, df: pd.DataFrame, window: int = 30, years: int = 10) -> list[float]:
        """
        Identify important price action points from up to 10 years of historical data.
        Args:
            df: DataFrame with 'close' prices, indexed by date.
            window: Rolling window to find local extrema.
            years: Number of years to look back.
        Returns:
            List of price levels (floats) considered important.
        """
        if df.empty or 'close' not in df.columns:
            return []
        # Filter last N years
        if 'date' in df.columns:
            df = df[df['date'] >= (datetime.now() - pd.DateOffset(years=years))]
        highs = df['close'][(df['close'] == df['close'].rolling(window, center=True).max())]
        lows = df['close'][(df['close'] == df['close'].rolling(window, center=True).min())]
        levels = pd.concat([highs, lows]).dropna().unique()
        return sorted(levels)

    def is_at_important_level(self, current_price: float, levels: list[float], threshold: float = 0.001) -> bool:
        """
        Check if current price is near any important price action point.
        Args:
            current_price: Latest price.
            levels: List of important price levels.
            threshold: Relative proximity (e.g., 0.1%).
        Returns:
            True if near a level, else False.
        """
        return any(abs(current_price - lvl) / lvl < threshold for lvl in levels)

    def analyze_pair(self, df: pd.DataFrame, pair: str, timeframe: str = '1h') -> Dict[str, Any]:
        """
        Perform comprehensive technical analysis on a currency pair
        
        Args:
            df: DataFrame with OHLCV data
            pair: Currency pair symbol
            timeframe: Analysis timeframe
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            if df.empty or len(df) < 20:
                return self._get_default_analysis(pair)
            
            # Convert to numeric and handle missing data
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.dropna()
            
            if len(df) < 10:
                return self._get_default_analysis(pair)
            
            close = df['close']
            high = df['high']
            low = df['low']
            volume = df.get('volume', pd.Series([0] * len(df)))
            
            # Calculate indicators
            trend_analysis = self._analyze_trend(close, high, low)
            momentum_analysis = self._analyze_momentum(close, high, low)
            volatility_analysis = self._analyze_volatility(close, high, low)
            volume_analysis = self._analyze_volume(close, volume)
            
            # --- Important price action points logic ---
            important_levels = self.find_important_price_points(df)
            at_important_level = self.is_at_important_level(float(close.iloc[-1]), important_levels)
            
            # Generate summary
            summary = self._generate_summary(trend_analysis, momentum_analysis, volatility_analysis)
            
            analysis_result = {
                'pair': pair,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'summary': summary,
                'trend_analysis': trend_analysis,
                'momentum_indicators': momentum_analysis,  # Renamed for signal_generator compatibility
                'oscillators': self._analyze_oscillators(close, high, low),
                'moving_averages': self._analyze_moving_averages(close),
                'support_resistance': self._analyze_support_resistance(close),
                'pattern_recognition': self._analyze_patterns(close, high, low),
                'volatility_analysis': volatility_analysis,
                'volume_analysis': volume_analysis,
                'last_price': float(close.iloc[-1]) if len(close) > 0 else 0,
                'price_change': float(close.iloc[-1] - close.iloc[-2]) if len(close) > 1 else 0,
                'price_change_percent': float(((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100) if len(close) > 1 and close.iloc[-2] != 0 else 0,
                'important_levels': important_levels,
                'at_important_level': at_important_level
            }
            
            self.last_analysis = analysis_result
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in technical analysis for {pair}: {e}")
            return self._get_default_analysis(pair)
    
    def _analyze_trend(self, close: pd.Series, high: pd.Series, low: pd.Series) -> Dict[str, Any]:
        """Analyze trend indicators"""
        try:
            # Moving averages
            sma_20 = self.calculate_sma(close, 20)
            sma_50 = self.calculate_sma(close, 50)
            ema_12 = self.calculate_ema(close, 12)
            ema_26 = self.calculate_ema(close, 26)
            
            current_price = close.iloc[-1]
            
            # Trend direction
            trend_signals = []
            if current_price > sma_20.iloc[-1]:
                trend_signals.append(1)
            else:
                trend_signals.append(-1)
                
            if sma_20.iloc[-1] > sma_50.iloc[-1]:
                trend_signals.append(1)
            else:
                trend_signals.append(-1)
                
            if ema_12.iloc[-1] > ema_26.iloc[-1]:
                trend_signals.append(1)
            else:
                trend_signals.append(-1)
            
            trend_score = sum(trend_signals)
            
            if trend_score >= 2:
                direction = "BULLISH"
            elif trend_score <= -2:
                direction = "BEARISH"
            else:
                direction = "NEUTRAL"
            
            # Trend strength
            price_change_20 = (current_price - close.iloc[-20]) / close.iloc[-20] * 100 if len(close) >= 20 else 0
            strength = min(abs(price_change_20) * 10, 100)
            
            return {
                'direction': direction,
                'strength': round(strength, 2),
                'sma_20': float(sma_20.iloc[-1]),
                'sma_50': float(sma_50.iloc[-1]),
                'ema_12': float(ema_12.iloc[-1]),
                'ema_26': float(ema_26.iloc[-1]),
                'trend_score': trend_score
            }
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return {'direction': 'NEUTRAL', 'strength': 0}
    
    def _analyze_momentum(self, close: pd.Series, high: pd.Series, low: pd.Series) -> Dict[str, Any]:
        """Analyze momentum indicators"""
        try:
            rsi = self.calculate_rsi(close)
            macd_data = self.calculate_macd(close)
            stoch_data = self.calculate_stochastic(high, low, close)
            williams_r = self.calculate_williams_r(high, low, close)
            
            current_rsi = rsi.iloc[-1]
            current_macd = macd_data['macd'].iloc[-1]
            current_signal = macd_data['signal'].iloc[-1]
            current_stoch_k = stoch_data['k'].iloc[-1]
            current_williams = williams_r.iloc[-1]
            
            # Momentum signals
            momentum_signals = []
            
            # RSI signals
            if current_rsi > 70:
                rsi_signal = "OVERBOUGHT"
                momentum_signals.append(-1)
            elif current_rsi < 30:
                rsi_signal = "OVERSOLD"
                momentum_signals.append(1)
            else:
                rsi_signal = "NEUTRAL"
                momentum_signals.append(0)
            
            # MACD signals
            if current_macd > current_signal:
                macd_signal = "BULLISH"
                momentum_signals.append(1)
            else:
                macd_signal = "BEARISH"
                momentum_signals.append(-1)
            
            # Stochastic signals
            if current_stoch_k > 80:
                stoch_signal = "OVERBOUGHT"
                momentum_signals.append(-1)
            elif current_stoch_k < 20:
                stoch_signal = "OVERSOLD"
                momentum_signals.append(1)
            else:
                stoch_signal = "NEUTRAL"
                momentum_signals.append(0)
            
            momentum_score = sum(momentum_signals)
            
            return {
                'rsi': {
                    'value': round(current_rsi, 2),
                    'signal': rsi_signal
                },
                'macd': {
                    'value': round(current_macd, 6),
                    'signal_line': round(current_signal, 6),
                    'signal': macd_signal
                },
                'stochastic': {
                    'k': round(current_stoch_k, 2),
                    'd': round(stoch_data['d'].iloc[-1], 2),
                    'signal': stoch_signal
                },
                'williams_r': {
                    'value': round(current_williams, 2),
                    'signal': "OVERBOUGHT" if current_williams > -20 else "OVERSOLD" if current_williams < -80 else "NEUTRAL"
                },
                'momentum_score': momentum_score
            }
            
        except Exception as e:
            logger.error(f"Error in momentum analysis: {e}")
            return {'momentum_score': 0}
    
    def _analyze_volatility(self, close: pd.Series, high: pd.Series, low: pd.Series) -> Dict[str, Any]:
        """Analyze volatility indicators"""
        try:
            bb_data = self.calculate_bollinger_bands(close)
            
            current_price = close.iloc[-1]
            bb_upper = bb_data['upper'].iloc[-1]
            bb_lower = bb_data['lower'].iloc[-1]
            bb_middle = bb_data['middle'].iloc[-1]
            
            # Bollinger Band position
            if current_price > bb_upper:
                bb_signal = "OVERBOUGHT"
            elif current_price < bb_lower:
                bb_signal = "OVERSOLD"
            else:
                bb_signal = "NORMAL"
            
            # Calculate Average True Range manually
            high_low = high - low
            high_close = (high - close.shift(1)).abs()
            low_close = (low - close.shift(1)).abs()
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(window=14, min_periods=1).mean().iloc[-1]
            
            # Volatility percentage
            volatility_pct = (atr / current_price) * 100
            
            return {
                'bollinger_bands': {
                    'upper': round(bb_upper, 5),
                    'middle': round(bb_middle, 5),
                    'lower': round(bb_lower, 5),
                    'signal': bb_signal
                },
                'atr': round(atr, 5),
                'volatility_percent': round(volatility_pct, 2)
            }
            
        except Exception as e:
            logger.error(f"Error in volatility analysis: {e}")
            return {'volatility_percent': 0}
    
    def _analyze_volume(self, close: pd.Series, volume: pd.Series) -> Dict[str, Any]:
        """Analyze volume indicators"""
        try:
            if volume.sum() == 0:  # No volume data
                return {'volume_analysis': 'No volume data available'}
            
            # Volume moving average
            volume_sma = self.calculate_sma(volume, 20)
            current_volume = volume.iloc[-1]
            avg_volume = volume_sma.iloc[-1]
            
            # Volume trend
            if current_volume > avg_volume * 1.5:
                volume_signal = "HIGH"
            elif current_volume < avg_volume * 0.5:
                volume_signal = "LOW"
            else:
                volume_signal = "NORMAL"
            
            return {
                'current_volume': int(current_volume),
                'average_volume': int(avg_volume),
                'volume_signal': volume_signal,
                'volume_ratio': round(current_volume / avg_volume, 2) if avg_volume > 0 else 1
            }
            
        except Exception as e:
            logger.error(f"Error in volume analysis: {e}")
            return {'volume_signal': 'NORMAL'}
    
    def _generate_summary(self, trend: Dict, momentum: Dict, volatility: Dict) -> Dict[str, Any]:
        """Generate overall analysis summary"""
        try:
            # Overall signal calculation
            trend_score = trend.get('trend_score', 0)
            momentum_score = momentum.get('momentum_score', 0)
            
            total_score = trend_score + momentum_score
            
            if total_score >= 3:
                overall_signal = "STRONG_BUY"
                confidence = 85
            elif total_score >= 1:
                overall_signal = "BUY"
                confidence = 70
            elif total_score <= -3:
                overall_signal = "STRONG_SELL"
                confidence = 85
            elif total_score <= -1:
                overall_signal = "SELL"
                confidence = 70
            else:
                overall_signal = "HOLD"
                confidence = 50
            
            # Count bullish and bearish signals
            bullish_signals = max(0, trend_score) + max(0, momentum_score)
            bearish_signals = abs(min(0, trend_score)) + abs(min(0, momentum_score))
            
            return {
                'overall_signal': overall_signal,
                'confidence': confidence,
                'trend_direction': trend.get('direction', 'NEUTRAL'),
                'trend_strength': trend.get('strength', 0),
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals,
                'total_score': total_score
            }
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {
                'overall_signal': 'HOLD',
                'confidence': 50,
                'trend_direction': 'NEUTRAL',
                'trend_strength': 0,
                'bullish_signals': 0,
                'bearish_signals': 0,
                'total_score': 0
            }
    
    def _get_default_analysis(self, pair: str) -> Dict[str, Any]:
        """Return default analysis when calculation fails"""
        return {
            'pair': pair,
            'timeframe': '1h',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'overall_signal': 'HOLD',
                'confidence': 50,
                'trend_direction': 'NEUTRAL',
                'trend_strength': 0,
                'bullish_signals': 0,
                'bearish_signals': 0,
                'total_score': 0
            },
            'trend_analysis': {'direction': 'NEUTRAL', 'strength': 0},
            'momentum_analysis': {'momentum_score': 0},
            'volatility_analysis': {'volatility_percent': 0},
            'volume_analysis': {'volume_signal': 'NORMAL'},
            'last_price': 0,
            'price_change': 0,
            'price_change_percent': 0,
            'error': 'Insufficient data for analysis'
        }
    
    def get_support_resistance_levels(self, df: pd.DataFrame, pair: str) -> Dict[str, List[float]]:
        """Calculate support and resistance levels"""
        try:
            if len(df) < 20:
                return {'support': [], 'resistance': []}
            
            high = df['high'].astype(float)
            low = df['low'].astype(float)
            close = df['close'].astype(float)
            
            # Simple pivot points calculation
            highs = []
            lows = []
            
            for i in range(2, len(df) - 2):
                # Local highs
                if (high.iloc[i] > high.iloc[i-1] and high.iloc[i] > high.iloc[i+1] and
                    high.iloc[i] > high.iloc[i-2] and high.iloc[i] > high.iloc[i+2]):
                    highs.append(high.iloc[i])
                
                # Local lows
                if (low.iloc[i] < low.iloc[i-1] and low.iloc[i] < low.iloc[i+1] and
                    low.iloc[i] < low.iloc[i-2] and low.iloc[i] < low.iloc[i+2]):
                    lows.append(low.iloc[i])
            
            # Get the most recent levels
            resistance = sorted(highs, reverse=True)[:3] if highs else []
            support = sorted(lows, reverse=True)[:3] if lows else []
            
            return {
                'support': [round(level, 5) for level in support],
                'resistance': [round(level, 5) for level in resistance]
            }
            
        except Exception as e:
            logger.error(f"Error calculating support/resistance levels: {e}")
            return {'support': [], 'resistance': []}
    
    def _analyze_oscillators(self, close: pd.Series, high: pd.Series, low: pd.Series) -> dict:
        """Stub for oscillators analysis (RSI, Stochastic, Williams %R)"""
        return {
            'rsi': {'value': self.calculate_rsi(close).iloc[-1]},
            'stochastic': {'k': self.calculate_stochastic(high, low, close)['k'].iloc[-1]},
            'williams_r': {'value': self.calculate_williams_r(high, low, close).iloc[-1]}
        }

    def _analyze_moving_averages(self, close: pd.Series) -> dict:
        """Stub for moving averages analysis"""
        return {
            'sma_20': self.calculate_sma(close, 20).iloc[-1],
            'sma_50': self.calculate_sma(close, 50).iloc[-1],
            'signals': {'sma_20_above_50': self.calculate_sma(close, 20).iloc[-1] > self.calculate_sma(close, 50).iloc[-1]}
        }

    def _analyze_support_resistance(self, close: pd.Series) -> dict:
        """Stub for support/resistance analysis"""
        return {
            'nearest_support': min(close.tail(20)),
            'nearest_resistance': max(close.tail(20)),
            'current_price': close.iloc[-1]
        }

    def _analyze_patterns(self, close: pd.Series, high: pd.Series, low: pd.Series) -> dict:
        """Stub for pattern recognition"""
        return {'detected_patterns': {}}
