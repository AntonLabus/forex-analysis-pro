"""
Technical Analysis Module - No Dependencies Version
Provides basic technical analysis for forex pairs without pandas/numpy
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import statistics

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    """
    Simple technical analysis engine for forex data using only Python built-ins
    """
    
    def __init__(self):
        self.last_analysis = None
        self.cache_timeout = 300  # 5 minutes
        
    def calculate_sma(self, data: List[float], period: int) -> List[float]:
        """Calculate Simple Moving Average"""
        if len(data) < period:
            return [statistics.mean(data[:i+1]) for i in range(len(data))]
        
        sma = []
        for i in range(len(data)):
            if i < period - 1:
                sma.append(statistics.mean(data[:i+1]))
            else:
                sma.append(statistics.mean(data[i-period+1:i+1]))
        return sma
    
    def calculate_rsi(self, data: List[float], period: int = 14) -> float:
        """Calculate current RSI value"""
        if len(data) < period + 1:
            return 50.0  # Neutral RSI
            
        changes = [data[i] - data[i-1] for i in range(1, len(data))]
        gains = [max(0, change) for change in changes[-period:]]
        losses = [max(0, -change) for change in changes[-period:]]
        
        avg_gain = statistics.mean(gains) if gains else 0
        avg_loss = statistics.mean(losses) if losses else 0
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: List[float], fast: int = 12, slow: int = 26) -> Dict:
        """Calculate basic MACD"""
        if len(data) < slow:
            return {"value": 0.0, "signal": "NEUTRAL"}
            
        # Simple approximation using moving averages
        fast_ma = self.calculate_sma(data, fast)[-1] if len(data) >= fast else statistics.mean(data)
        slow_ma = self.calculate_sma(data, slow)[-1] if len(data) >= slow else statistics.mean(data)
        
        macd_value = fast_ma - slow_ma
        
        # Simple signal determination
        if macd_value > 0:
            signal = "BULLISH"
        elif macd_value < 0:
            signal = "BEARISH"
        else:
            signal = "NEUTRAL"
            
        return {"value": macd_value, "signal": signal}
    
    def analyze_trend(self, data: List[float]) -> Dict[str, Any]:
        """Analyze price trend"""
        if len(data) < 3:
            return {"direction": "UNKNOWN", "strength": "WEAK"}
        
        # Calculate short and long term averages
        short_period = min(5, len(data) // 2)
        long_period = min(20, len(data))
        
        short_ma = statistics.mean(data[-short_period:])
        long_ma = statistics.mean(data[-long_period:])
        current_price = data[-1]
        
        # Determine trend direction
        if short_ma > long_ma and current_price > short_ma:
            direction = "UPTREND"
        elif short_ma < long_ma and current_price < short_ma:
            direction = "DOWNTREND"
        else:
            direction = "SIDEWAYS"
        
        # Calculate trend strength based on price consistency
        recent_changes = [data[i] - data[i-1] for i in range(-min(5, len(data)-1), 0)]
        positive_changes = sum(1 for change in recent_changes if change > 0)
        
        if positive_changes >= 4:
            strength = "STRONG"
        elif positive_changes >= 3:
            strength = "MODERATE"
        else:
            strength = "WEAK"
        
        return {
            "direction": direction,
            "strength": strength,
            "short_ma": short_ma,
            "long_ma": long_ma,
            "current_price": current_price
        }
    
    def analyze(self, pair: str, data: List[Dict], timeframe: str = "1h") -> Dict[str, Any]:
        """
        Perform technical analysis on forex data
        
        Args:
            pair: Currency pair symbol (e.g., 'EURUSD')
            data: List of price data dictionaries with keys: timestamp, open, high, low, close, volume
            timeframe: Timeframe for analysis
            
        Returns:
            Dict containing technical analysis results
        """
        try:
            if not data or len(data) < 2:
                return self._get_empty_analysis(pair)
            
            # Extract close prices
            close_prices = [float(candle.get('close', 0)) for candle in data if candle.get('close')]
            
            if len(close_prices) < 2:
                return self._get_empty_analysis(pair)
            
            # Calculate indicators
            trend_analysis = self.analyze_trend(close_prices)
            rsi_value = self.calculate_rsi(close_prices)
            macd_analysis = self.calculate_macd(close_prices)
            
            # Calculate volatility
            price_changes = [abs(close_prices[i] - close_prices[i-1]) for i in range(1, len(close_prices))]
            avg_change = statistics.mean(price_changes) if price_changes else 0
            volatility_percent = (avg_change / close_prices[-1] * 100) if close_prices[-1] > 0 else 0
            
            # Generate signals
            bullish_signals = 0
            bearish_signals = 0
            
            # RSI signals
            if rsi_value < 30:
                bullish_signals += 1
            elif rsi_value > 70:
                bearish_signals += 1
            
            # Trend signals
            if trend_analysis["direction"] == "UPTREND":
                bullish_signals += 1
            elif trend_analysis["direction"] == "DOWNTREND":
                bearish_signals += 1
            
            # MACD signals
            if macd_analysis["signal"] == "BULLISH":
                bullish_signals += 1
            elif macd_analysis["signal"] == "BEARISH":
                bearish_signals += 1
            
            # Overall signal
            if bullish_signals > bearish_signals:
                overall_signal = "BUY"
                confidence = min(80, 40 + (bullish_signals * 15))
            elif bearish_signals > bullish_signals:
                overall_signal = "SELL"
                confidence = min(80, 40 + (bearish_signals * 15))
            else:
                overall_signal = "HOLD"
                confidence = 30
            
            analysis_result = {
                "pair": pair,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "overall_signal": overall_signal,
                    "confidence": confidence,
                    "bullish_signals": bullish_signals,
                    "bearish_signals": bearish_signals
                },
                "trend_analysis": trend_analysis,
                "momentum_analysis": {
                    "rsi": {
                        "value": rsi_value,
                        "signal": self._get_rsi_signal(rsi_value)
                    },
                    "macd": macd_analysis
                },
                "volatility_analysis": {
                    "volatility_percent": volatility_percent,
                    "classification": self._classify_volatility(volatility_percent)
                },
                "current_price": close_prices[-1] if close_prices else 0,
                "data_points": len(close_prices)
            }
            
            self.last_analysis = analysis_result
            logger.info(f"Technical analysis completed for {pair}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in technical analysis for {pair}: {str(e)}")
            return self._get_empty_analysis(pair, error=str(e))
    
    def _get_rsi_signal(self, rsi: float) -> str:
        """Get RSI signal interpretation"""
        if rsi < 30:
            return "OVERSOLD"
        elif rsi > 70:
            return "OVERBOUGHT"
        elif rsi < 40:
            return "BEARISH"
        elif rsi > 60:
            return "BULLISH"
        else:
            return "NEUTRAL"
    
    def _classify_volatility(self, volatility_percent: float) -> str:
        """Classify volatility level"""
        if volatility_percent < 0.5:
            return "LOW"
        elif volatility_percent < 1.0:
            return "MODERATE"
        elif volatility_percent < 2.0:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    def _get_empty_analysis(self, pair: str, error: str = None) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            "pair": pair,
            "timeframe": "1h",
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "summary": {
                "overall_signal": "HOLD",
                "confidence": 0,
                "bullish_signals": 0,
                "bearish_signals": 0
            },
            "trend_analysis": {
                "direction": "UNKNOWN",
                "strength": "WEAK"
            },
            "momentum_analysis": {
                "rsi": {"value": 50, "signal": "NEUTRAL"},
                "macd": {"value": 0, "signal": "NEUTRAL"}
            },
            "volatility_analysis": {
                "volatility_percent": 0,
                "classification": "UNKNOWN"
            },
            "current_price": 0,
            "data_points": 0
        }

# Global instance
technical_analyzer = TechnicalAnalysis()
