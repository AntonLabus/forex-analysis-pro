"""
Signal Generator Module
Combines technical and fundamental analysis to generate trading signals with confidence scores
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SignalGenerator:
    """
    Advanced trading signal generator that combines multiple analysis methods
    """
    
    def __init__(self):
        # Signal weights for different analysis components
        self.weights = {
            'technical': 0.6,
            'fundamental': 0.4,
            'trend': 0.3,
            'momentum': 0.2,
            'volatility': 0.1,
            'volume': 0.1,
            'support_resistance': 0.15,
            'pattern': 0.15
        }
    
    def generate_signals(self, pair: str, price_data: pd.DataFrame, 
                        technical_analysis: Dict[str, Any], 
                        fundamental_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive trading signals with confidence scores
        
        Args:
            pair: Currency pair
            price_data: Historical price data
            technical_analysis: Technical analysis results
            fundamental_analysis: Fundamental analysis results
        
        Returns:
            Dictionary containing trading signals and confidence scores
        """
        try:
            # Calculate individual signal components
            tech_signal = self._calculate_technical_signal(technical_analysis)
            fund_signal = self._calculate_fundamental_signal(fundamental_analysis)
            
            # Combine signals
            combined_signal = self._combine_signals(tech_signal, fund_signal)
            
            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(price_data, technical_analysis)
            
            # Generate entry/exit levels
            levels = self._calculate_entry_exit_levels(price_data, technical_analysis, combined_signal)
            
            # Generate position sizing recommendation
            position_size = self._calculate_position_size(risk_metrics, combined_signal)
            
            # Check for historically important price action point
            at_important_level = technical_analysis.get('at_important_level', False)
            important_levels = technical_analysis.get('important_levels', [])
            
            # If at important level, force a valid signal with high confidence
            if at_important_level and important_levels:
                combined_signal['direction'] = 'SIGNIFICANT_LEVEL'
                combined_signal['confidence'] = 90
                combined_signal['note'] = 'Current price matches a historically important price action point.'
            
            # Create final signal output
            now = datetime.now()
            valid_until = now + timedelta(hours=1)  # Signals valid for 1 hour by default
            signal_output = {
                'pair': pair,
                'timestamp': now.isoformat(),
                'valid_until': valid_until.isoformat(),
                'signal': combined_signal,
                'technical_signal': tech_signal,
                'fundamental_signal': fund_signal,
                'risk_metrics': risk_metrics,
                'levels': levels,
                'position_sizing': position_size,
                'summary': self._generate_signal_summary(combined_signal, risk_metrics)
            }
            
            return signal_output
            
        except Exception as e:
            logger.error(f"Error generating signals for {pair}: {e}")
            return {'error': str(e)}
    
    def _calculate_technical_signal(self, tech_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate technical analysis signal with confidence"""
        try:
            signals = []
            weights = []
            
            # Trend analysis signal
            if 'trend_analysis' in tech_analysis:
                trend = tech_analysis['trend_analysis']
                if 'direction' in trend and 'confidence' in trend:
                    direction = trend['direction']
                    confidence = trend['confidence']
                    
                    signal_value = 1 if direction == 'Bullish' else -1 if direction == 'Bearish' else 0
                    signals.append(signal_value * (confidence / 100))
                    weights.append(self.weights['trend'])
            
            # Momentum signals
            if 'momentum_indicators' in tech_analysis:
                momentum = tech_analysis['momentum_indicators']
                
                # MACD signal
                if 'macd' in momentum:
                    macd_data = momentum['macd']
                    if macd_data['macd'] > macd_data['signal']:
                        signals.append(0.7)
                    else:
                        signals.append(-0.7)
                    weights.append(self.weights['momentum'])
                
                # ROC signal
                if 'roc' in momentum:
                    roc = momentum['roc']
                    if roc > 1:
                        signals.append(0.6)
                    elif roc < -1:
                        signals.append(-0.6)
                    else:
                        signals.append(0)
                    weights.append(self.weights['momentum'] * 0.5)
            
            # Oscillator signals
            if 'oscillators' in tech_analysis:
                oscillators = tech_analysis['oscillators']
                
                # RSI signal
                if 'rsi' in oscillators:
                    rsi_data = oscillators['rsi']
                    rsi_value = rsi_data['value']
                    
                    if rsi_value < 30:
                        signals.append(0.8)  # Oversold - bullish
                    elif rsi_value > 70:
                        signals.append(-0.8)  # Overbought - bearish
                    else:
                        signals.append((50 - rsi_value) / 50)  # Neutral zone
                    weights.append(self.weights['momentum'] * 0.7)
                
                # Stochastic signal
                if 'stochastic' in oscillators:
                    stoch_data = oscillators['stochastic']
                    stoch_k = stoch_data['k']
                    
                    if stoch_k < 20:
                        signals.append(0.6)
                    elif stoch_k > 80:
                        signals.append(-0.6)
                    else:
                        signals.append(0)
                    weights.append(self.weights['momentum'] * 0.3)
            
            # Moving average signals
            if 'moving_averages' in tech_analysis and 'signals' in tech_analysis['moving_averages']:
                ma_signals = tech_analysis['moving_averages']['signals']
                
                bullish_ma_count = sum(1 for signal in ma_signals.values() if signal is True)
                total_ma_signals = len(ma_signals)
                
                if total_ma_signals > 0:
                    ma_score = (bullish_ma_count / total_ma_signals) * 2 - 1  # Convert to -1 to 1 scale
                    signals.append(ma_score)
                    weights.append(self.weights['trend'] * 0.5)
            
            # Support/Resistance signals
            if 'support_resistance' in tech_analysis:
                sr_data = tech_analysis['support_resistance']
                current_price = sr_data.get('current_price', 0)
                nearest_resistance = sr_data.get('nearest_resistance', current_price * 1.01)
                nearest_support = sr_data.get('nearest_support', current_price * 0.99)
                
                # Calculate distance to S/R levels
                resistance_distance = (nearest_resistance - current_price) / current_price * 100
                support_distance = (current_price - nearest_support) / current_price * 100
                
                if support_distance < 0.1:  # Very close to support
                    signals.append(0.7)
                elif resistance_distance < 0.1:  # Very close to resistance
                    signals.append(-0.7)
                else:
                    signals.append(0)
                weights.append(self.weights['support_resistance'])
            
            # Pattern recognition signals
            if 'pattern_recognition' in tech_analysis:
                patterns = tech_analysis['pattern_recognition'].get('detected_patterns', {})
                pattern_signal = 0
                
                for pattern_name, pattern_data in patterns.items():
                    if pattern_data['signal'] == 'Bullish':
                        pattern_signal += 0.5
                    elif pattern_data['signal'] == 'Bearish':
                        pattern_signal -= 0.5
                
                signals.append(np.clip(pattern_signal, -1, 1))
                weights.append(self.weights['pattern'])
            
            # Calculate weighted average
            if signals and weights:
                total_weight = sum(weights)
                weighted_signal = sum(s * w for s, w in zip(signals, weights)) / total_weight
                confidence = min(abs(weighted_signal) * 100, 100)
                
                # Determine signal direction
                if weighted_signal > 0.1:
                    direction = 'BUY'
                elif weighted_signal < -0.1:
                    direction = 'SELL'
                else:
                    direction = 'HOLD'
                
                return {
                    'direction': direction,
                    'strength': abs(weighted_signal),
                    'confidence': round(confidence, 1),
                    'raw_signal': weighted_signal,
                    'components': len(signals)
                }
            else:
                return {
                    'direction': 'HOLD',
                    'strength': 0,
                    'confidence': 0,
                    'raw_signal': 0,
                    'components': 0
                }
                
        except Exception as e:
            logger.error(f"Error calculating technical signal: {e}")
            return {'error': str(e)}
    
    def _calculate_fundamental_signal(self, fund_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate fundamental analysis signal with confidence"""
        try:
            if 'summary' in fund_analysis:
                summary = fund_analysis['summary']
                
                overall_bias = summary.get('overall_bias', 'Neutral')
                confidence = summary.get('confidence', 0)
                
                # Convert bias to signal
                if overall_bias == 'Bullish':
                    direction = 'BUY'
                    strength = confidence / 100
                elif overall_bias == 'Bearish':
                    direction = 'SELL'
                    strength = confidence / 100
                else:
                    direction = 'HOLD'
                    strength = 0
                
                return {
                    'direction': direction,
                    'strength': strength,
                    'confidence': confidence,
                    'bias': overall_bias,
                    'factors': {
                        'bullish': summary.get('bullish_factors', 0),
                        'bearish': summary.get('bearish_factors', 0),
                        'total': summary.get('total_factors', 0)
                    }
                }
            else:
                return {
                    'direction': 'HOLD',
                    'strength': 0,
                    'confidence': 0,
                    'bias': 'Unknown',
                    'factors': {'bullish': 0, 'bearish': 0, 'total': 0}
                }
                
        except Exception as e:
            logger.error(f"Error calculating fundamental signal: {e}")
            return {'error': str(e)}
    
    def _combine_signals(self, tech_signal: Dict[str, Any], fund_signal: Dict[str, Any]) -> Dict[str, Any]:
        """Combine technical and fundamental signals"""
        try:
            # Get signal strengths
            tech_strength = tech_signal.get('strength', 0)
            fund_strength = fund_signal.get('strength', 0)
            
            tech_direction = tech_signal.get('direction', 'HOLD')
            fund_direction = fund_signal.get('direction', 'HOLD')
            
            # Convert directions to numeric values
            direction_values = {'BUY': 1, 'SELL': -1, 'HOLD': 0}
            tech_value = direction_values.get(tech_direction, 0) * tech_strength
            fund_value = direction_values.get(fund_direction, 0) * fund_strength
            
            # Weighted combination
            combined_value = (tech_value * self.weights['technical'] + 
                            fund_value * self.weights['fundamental'])
            
            # Determine final signal
            if combined_value > 0.15:
                final_direction = 'BUY'
            elif combined_value < -0.15:
                final_direction = 'SELL'
            else:
                final_direction = 'HOLD'
            
            # Calculate confidence based on signal agreement
            tech_conf = tech_signal.get('confidence', 0)
            fund_conf = fund_signal.get('confidence', 0)
            
            # Bonus for agreement between technical and fundamental
            agreement_bonus = 0
            if (tech_direction == fund_direction and 
                tech_direction != 'HOLD' and fund_direction != 'HOLD'):
                agreement_bonus = 20
            
            combined_confidence = (tech_conf * self.weights['technical'] + 
                                 fund_conf * self.weights['fundamental'] + 
                                 agreement_bonus)
            
            combined_confidence = min(combined_confidence, 100)
            
            return {
                'direction': final_direction,
                'strength': abs(combined_value),
                'confidence': round(combined_confidence, 1),
                'raw_signal': combined_value,
                'agreement': tech_direction == fund_direction,
                'technical_weight': self.weights['technical'],
                'fundamental_weight': self.weights['fundamental']
            }
            
        except Exception as e:
            logger.error(f"Error combining signals: {e}")
            return {'error': str(e)}
    
    def _calculate_risk_metrics(self, price_data: pd.DataFrame, tech_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk metrics for the trade"""
        try:
            # Check if required columns exist
            if price_data is None or price_data.empty:
                logger.warning("Empty price data for risk calculation")
                return {
                    'volatility': 1.5,
                    'risk_level': 'MEDIUM',
                    'max_risk_percent': 2.0,
                    'confidence_adjustment': 0.0
                }
            
            # Normalize column names (handle both 'close' and 'Close')
            if 'Close' in price_data.columns:
                close_prices = price_data['Close'].values
            elif 'close' in price_data.columns:
                close_prices = price_data['close'].values
            else:
                logger.warning("No Close column found in price data")
                return {
                    'volatility': 1.5,
                    'risk_level': 'MEDIUM',
                    'max_risk_percent': 2.0,
                    'confidence_adjustment': 0.0
                }
            
            # Calculate volatility (20-period standard deviation)
            if len(close_prices) < 2:
                logger.warning("Insufficient data for volatility calculation")
                return {
                    'volatility': 1.5,
                    'risk_level': 'MEDIUM',
                    'max_risk_percent': 2.0,
                    'confidence_adjustment': 0.0
                }
                
            returns = np.diff(np.log(close_prices))
            volatility = np.std(returns[-20:]) * np.sqrt(252) * 100  # Annualized volatility
            
            # ATR for stop loss calculation
            atr = 0
            if 'volatility_indicators' in tech_analysis:
                atr = tech_analysis['volatility_indicators'].get('atr', 0)
            
            # Current price
            current_price = close_prices[-1]
            
            # Risk level classification
            if volatility > 15:
                risk_level = 'High'
            elif volatility > 8:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            # Calculate suggested stop loss levels
            atr_stop = atr * 2 if atr > 0 else current_price * 0.01
            
            return {
                'volatility': round(volatility, 2),
                'atr': round(atr, 5),
                'risk_level': risk_level,
                'suggested_stop_loss': round(atr_stop, 5),
                'current_price': round(current_price, 5)
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {'error': str(e)}
    
    def _calculate_entry_exit_levels(self, price_data: pd.DataFrame, 
                                   tech_analysis: Dict[str, Any], 
                                   signal: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate entry and exit levels"""
        try:
            # Check if price data is valid
            if price_data is None or price_data.empty:
                logger.warning("Empty price data for entry/exit calculation")
                return {
                    'entry': 1.0000,
                    'stop_loss': 0.9950,
                    'take_profit_1': 1.0050,
                    'take_profit_2': 1.0100,
                    'risk_reward_ratio': 2.0
                }
            
            # Handle column name variations
            if 'Close' in price_data.columns:
                current_price = price_data['Close'].iloc[-1]
            elif 'close' in price_data.columns:
                current_price = price_data['close'].iloc[-1]
            else:
                logger.warning("No Close column found for entry/exit calculation")
                return {
                    'entry': 1.0000,
                    'stop_loss': 0.9950,
                    'take_profit_1': 1.0050,
                    'take_profit_2': 1.0100,
                    'risk_reward_ratio': 2.0
                }
                
            atr = tech_analysis.get('volatility_indicators', {}).get('atr', current_price * 0.01)
            
            signal_direction = signal.get('direction', 'HOLD')
            
            if signal_direction == 'BUY':
                # Buy signal levels
                entry = current_price
                stop_loss = current_price - (atr * 2)
                take_profit_1 = current_price + (atr * 2)
                take_profit_2 = current_price + (atr * 4)
                
            elif signal_direction == 'SELL':
                # Sell signal levels
                entry = current_price
                stop_loss = current_price + (atr * 2)
                take_profit_1 = current_price - (atr * 2)
                take_profit_2 = current_price - (atr * 4)
                
            else:
                # Hold - no specific levels
                entry = current_price
                stop_loss = None
                take_profit_1 = None
                take_profit_2 = None
            
            # Support and resistance levels from technical analysis
            sr_levels = {}
            if 'support_resistance' in tech_analysis:
                sr_data = tech_analysis['support_resistance']
                sr_levels = {
                    'nearest_support': sr_data.get('nearest_support'),
                    'nearest_resistance': sr_data.get('nearest_resistance'),
                    'pivot_point': sr_data.get('pivot_points', {}).get('pivot')
                }
            
            return {
                'entry': round(entry, 5) if entry else None,
                'stop_loss': round(stop_loss, 5) if stop_loss else None,
                'take_profit_1': round(take_profit_1, 5) if take_profit_1 else None,
                'take_profit_2': round(take_profit_2, 5) if take_profit_2 else None,
                'risk_reward_ratio': round((take_profit_1 - entry) / (entry - stop_loss), 2) if (signal_direction == 'BUY' and stop_loss and take_profit_1) else None,
                'support_resistance': sr_levels
            }
            
        except Exception as e:
            logger.error(f"Error calculating entry/exit levels: {e}")
            return {'error': str(e)}
    
    def _calculate_position_size(self, risk_metrics: Dict[str, Any], signal: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate recommended position size"""
        try:
            risk_level = risk_metrics.get('risk_level', 'Medium')
            confidence = signal.get('confidence', 0)
            
            # Base position size as percentage of account
            base_size = {
                'Low': 2.0,     # 2% of account
                'Medium': 1.5,  # 1.5% of account
                'High': 1.0     # 1% of account
            }
            
            # Adjust based on signal confidence
            confidence_multiplier = confidence / 100
            
            recommended_size = base_size.get(risk_level, 1.5) * confidence_multiplier
            
            # Maximum position size cap
            max_size = 3.0
            recommended_size = min(recommended_size, max_size)
            
            return {
                'recommended_size_percent': round(recommended_size, 2),
                'risk_level': risk_level,
                'confidence_factor': round(confidence_multiplier, 2),
                'max_recommended': max_size,
                'notes': f"Based on {risk_level.lower()} risk and {confidence}% confidence"
            }
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return {'error': str(e)}
    
    def _generate_signal_summary(self, signal: Dict[str, Any], risk_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the trading signal"""
        try:
            direction = signal.get('direction', 'HOLD')
            confidence = signal.get('confidence', 0)
            risk_level = risk_metrics.get('risk_level', 'Unknown')
            
            # Generate signal quality score
            if confidence >= 80:
                signal_quality = 'Excellent'
            elif confidence >= 65:
                signal_quality = 'Good'
            elif confidence >= 50:
                signal_quality = 'Fair'
            else:
                signal_quality = 'Poor'
            
            # Generate recommendation text
            if direction == 'HOLD':
                recommendation = "No clear trading opportunity. Wait for better setup."
            elif confidence < 50:
                recommendation = f"Weak {direction} signal. Consider waiting for confirmation."
            elif confidence < 70:
                recommendation = f"Moderate {direction} signal. Use smaller position size."
            else:
                recommendation = f"Strong {direction} signal with good risk/reward potential."
            
            # Risk warning
            risk_warning = ""
            if risk_level == 'High':
                risk_warning = "⚠️ High volatility detected. Use appropriate risk management."
            elif risk_level == 'Medium':
                risk_warning = "⚡ Moderate volatility. Monitor position closely."
            
            return {
                'signal_quality': signal_quality,
                'recommendation': recommendation,
                'risk_warning': risk_warning,
                'action': direction,
                'confidence_level': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating signal summary: {e}")
            return {'error': str(e)}
