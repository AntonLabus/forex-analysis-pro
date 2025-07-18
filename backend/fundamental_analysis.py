"""
Fundamental Analysis Module
Provides comprehensive fundamental analysis for forex pairs
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
import os
import json

logger = logging.getLogger(__name__)

class FundamentalAnalysis:
    """
    Comprehensive fundamental analysis engine for forex pairs
    """
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.economic_calendar_key = os.getenv('ECONOMIC_CALENDAR_API_KEY')
        
        # Central bank interest rates (mock data - in production, fetch from API)
        self.interest_rates = {
            'USD': 5.25, 'EUR': 3.75, 'GBP': 5.00, 'JPY': -0.10,
            'CHF': 1.50, 'AUD': 4.10, 'CAD': 4.75, 'NZD': 5.25
        }
        
        # Economic strength scores (mock data)
        self.economic_scores = {
            'USD': 75, 'EUR': 68, 'GBP': 72, 'JPY': 65,
            'CHF': 78, 'AUD': 70, 'CAD': 73, 'NZD': 69
        }
    
    def analyze(self, pair: str) -> Dict[str, Any]:
        """
        Perform comprehensive fundamental analysis on a forex pair
        
        Args:
            pair: Currency pair (e.g., 'EURUSD')
        
        Returns:
            Dictionary containing fundamental analysis results
        """
        try:
            if len(pair) != 6:
                return {'error': 'Invalid currency pair format'}
            
            base_currency = pair[:3]
            quote_currency = pair[3:]
            
            analysis = {
                'pair': pair,
                'base_currency': base_currency,
                'quote_currency': quote_currency,
                'interest_rate_analysis': self._analyze_interest_rates(base_currency, quote_currency),
                'economic_calendar': self._get_economic_events(base_currency, quote_currency),
                'central_bank_analysis': self._analyze_central_banks(base_currency, quote_currency),
                'economic_indicators': self._analyze_economic_indicators(base_currency, quote_currency),
                'market_sentiment': self._analyze_market_sentiment(pair),
                'inflation_analysis': self._analyze_inflation(base_currency, quote_currency),
                'employment_analysis': self._analyze_employment(base_currency, quote_currency),
                'gdp_analysis': self._analyze_gdp(base_currency, quote_currency),
                'trade_balance': self._analyze_trade_balance(base_currency, quote_currency),
                'summary': None  # Will be populated at the end
            }
            
            # Generate overall fundamental summary
            analysis['summary'] = self._generate_fundamental_summary(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis for {pair}: {e}")
            return {'error': str(e)}
    
    def _analyze_interest_rates(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze interest rate differentials"""
        try:
            base_rate = self.interest_rates.get(base, 0)
            quote_rate = self.interest_rates.get(quote, 0)
            
            differential = base_rate - quote_rate
            
            # Determine impact
            if differential > 1.0:
                impact = f"Strongly favors {base}"
                strength = "Strong"
            elif differential > 0.25:
                impact = f"Moderately favors {base}"
                strength = "Moderate"
            elif differential < -1.0:
                impact = f"Strongly favors {quote}"
                strength = "Strong"
            elif differential < -0.25:
                impact = f"Moderately favors {quote}"
                strength = "Moderate"
            else:
                impact = "Neutral impact"
                strength = "Neutral"
            
            return {
                'base_rate': base_rate,
                'quote_rate': quote_rate,
                'differential': round(differential, 2),
                'impact': impact,
                'strength': strength,
                'carry_trade_potential': differential > 1.0,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing interest rates: {e}")
            return {'error': str(e)}
    
    def _get_economic_events(self, base: str, quote: str) -> Dict[str, Any]:
        """Get upcoming economic events for both currencies"""
        try:
            # Mock economic events (in production, fetch from economic calendar API)
            events = [
                {
                    'time': '2025-07-18 14:30:00',
                    'currency': base,
                    'event': 'Non-Farm Payrolls' if base == 'USD' else 'Employment Change',
                    'impact': 'High',
                    'forecast': '200K' if base == 'USD' else '15K',
                    'previous': '180K' if base == 'USD' else '12K',
                    'importance': 9
                },
                {
                    'time': '2025-07-18 12:30:00',
                    'currency': quote,
                    'event': 'Interest Rate Decision',
                    'impact': 'High',
                    'forecast': f"{self.interest_rates.get(quote, 0)}%",
                    'previous': f"{self.interest_rates.get(quote, 0)}%",
                    'importance': 10
                },
                {
                    'time': '2025-07-19 09:30:00',
                    'currency': base,
                    'event': 'Inflation Rate YoY',
                    'impact': 'Medium',
                    'forecast': '2.1%',
                    'previous': '2.3%',
                    'importance': 7
                }
            ]
            
            # Filter events for next 7 days
            upcoming_events = []
            for event in events:
                event_date = datetime.strptime(event['time'], '%Y-%m-%d %H:%M:%S')
                if event_date > datetime.now():
                    upcoming_events.append(event)
            
            return {
                'upcoming_events': upcoming_events,
                'high_impact_count': sum(1 for e in upcoming_events if e['impact'] == 'High'),
                'total_events': len(upcoming_events)
            }
            
        except Exception as e:
            logger.error(f"Error getting economic events: {e}")
            return {'error': str(e)}
    
    def _analyze_central_banks(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze central bank policies and stances"""
        try:
            # Mock central bank analysis
            cb_data = {
                'USD': {'bank': 'Federal Reserve', 'stance': 'Hawkish', 'next_meeting': '2025-07-31'},
                'EUR': {'bank': 'ECB', 'stance': 'Neutral', 'next_meeting': '2025-07-25'},
                'GBP': {'bank': 'Bank of England', 'stance': 'Hawkish', 'next_meeting': '2025-08-01'},
                'JPY': {'bank': 'Bank of Japan', 'stance': 'Dovish', 'next_meeting': '2025-07-30'},
                'CHF': {'bank': 'SNB', 'stance': 'Neutral', 'next_meeting': '2025-09-19'},
                'AUD': {'bank': 'RBA', 'stance': 'Neutral', 'next_meeting': '2025-08-06'},
                'CAD': {'bank': 'Bank of Canada', 'stance': 'Hawkish', 'next_meeting': '2025-07-24'},
                'NZD': {'bank': 'RBNZ', 'stance': 'Hawkish', 'next_meeting': '2025-08-14'}
            }
            
            base_cb = cb_data.get(base, {})
            quote_cb = cb_data.get(quote, {})
            
            # Determine relative stance
            stance_scores = {'Hawkish': 1, 'Neutral': 0, 'Dovish': -1}
            base_score = stance_scores.get(base_cb.get('stance', 'Neutral'), 0)
            quote_score = stance_scores.get(quote_cb.get('stance', 'Neutral'), 0)
            
            relative_stance = base_score - quote_score
            
            if relative_stance > 0:
                relative_impact = f"{base} central bank more hawkish"
            elif relative_stance < 0:
                relative_impact = f"{quote} central bank more hawkish"
            else:
                relative_impact = "Similar central bank stances"
            
            return {
                'base_currency_cb': base_cb,
                'quote_currency_cb': quote_cb,
                'relative_stance': relative_stance,
                'relative_impact': relative_impact
            }
            
        except Exception as e:
            logger.error(f"Error analyzing central banks: {e}")
            return {'error': str(e)}
    
    def _analyze_economic_indicators(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze key economic indicators"""
        try:
            # Mock economic indicator data
            indicators = {
                'USD': {
                    'gdp_growth': 2.3,
                    'unemployment': 3.7,
                    'inflation': 3.2,
                    'manufacturing_pmi': 49.2,
                    'services_pmi': 51.8
                },
                'EUR': {
                    'gdp_growth': 0.8,
                    'unemployment': 6.5,
                    'inflation': 2.9,
                    'manufacturing_pmi': 45.8,
                    'services_pmi': 48.9
                },
                'GBP': {
                    'gdp_growth': 1.1,
                    'unemployment': 4.2,
                    'inflation': 4.0,
                    'manufacturing_pmi': 47.1,
                    'services_pmi': 50.2
                },
                'JPY': {
                    'gdp_growth': 0.9,
                    'unemployment': 2.6,
                    'inflation': 1.8,
                    'manufacturing_pmi': 48.5,
                    'services_pmi': 49.7
                }
            }
            
            base_indicators = indicators.get(base, {})
            quote_indicators = indicators.get(quote, {})
            
            # Calculate relative strength
            strengths = {}
            for indicator in ['gdp_growth', 'manufacturing_pmi', 'services_pmi']:
                if indicator in base_indicators and indicator in quote_indicators:
                    base_val = base_indicators[indicator]
                    quote_val = quote_indicators[indicator]
                    
                    if base_val > quote_val:
                        strengths[indicator] = f"{base} stronger"
                    elif quote_val > base_val:
                        strengths[indicator] = f"{quote} stronger"
                    else:
                        strengths[indicator] = "Equal"
            
            return {
                'base_indicators': base_indicators,
                'quote_indicators': quote_indicators,
                'relative_strengths': strengths
            }
            
        except Exception as e:
            logger.error(f"Error analyzing economic indicators: {e}")
            return {'error': str(e)}
    
    def _analyze_market_sentiment(self, pair: str) -> Dict[str, Any]:
        """Analyze market sentiment and positioning"""
        try:
            # Mock sentiment analysis (in production, analyze news sentiment and COT data)
            import random
            
            sentiment_score = random.uniform(-1, 1)
            
            # Generate COT (Commitment of Traders) mock data
            cot_data = {
                'large_speculators_net': random.randint(-50000, 50000),
                'commercial_net': random.randint(-30000, 30000),
                'small_traders_net': random.randint(-10000, 10000),
                'week_change': random.randint(-5000, 5000)
            }
            
            # News sentiment
            news_sentiment = {
                'score': sentiment_score,
                'label': 'Bullish' if sentiment_score > 0.1 else 'Bearish' if sentiment_score < -0.1 else 'Neutral',
                'confidence': abs(sentiment_score) * 100,
                'recent_headlines': [
                    f"{pair} shows strength amid economic data",
                    f"Central bank decision impacts {pair} outlook",
                    f"Market volatility affects {pair} trading"
                ]
            }
            
            return {
                'news_sentiment': news_sentiment,
                'cot_data': cot_data,
                'overall_sentiment': news_sentiment['label']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market sentiment: {e}")
            return {'error': str(e)}
    
    def _analyze_inflation(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze inflation trends and differentials"""
        try:
            # Mock inflation data
            inflation_data = {
                'USD': {'current': 3.2, 'target': 2.0, 'trend': 'Decreasing'},
                'EUR': {'current': 2.9, 'target': 2.0, 'trend': 'Stable'},
                'GBP': {'current': 4.0, 'target': 2.0, 'trend': 'Decreasing'},
                'JPY': {'current': 1.8, 'target': 2.0, 'trend': 'Increasing'},
                'CHF': {'current': 1.2, 'target': 2.0, 'trend': 'Stable'},
                'AUD': {'current': 3.8, 'target': 2.5, 'trend': 'Decreasing'},
                'CAD': {'current': 3.1, 'target': 2.0, 'trend': 'Decreasing'},
                'NZD': {'current': 3.5, 'target': 2.0, 'trend': 'Stable'}
            }
            
            base_inflation = inflation_data.get(base, {})
            quote_inflation = inflation_data.get(quote, {})
            
            # Calculate differential
            differential = base_inflation.get('current', 0) - quote_inflation.get('current', 0)
            
            return {
                'base_inflation': base_inflation,
                'quote_inflation': quote_inflation,
                'differential': round(differential, 1),
                'impact': f"Favors {base}" if differential > 0.5 else f"Favors {quote}" if differential < -0.5 else "Neutral"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing inflation: {e}")
            return {'error': str(e)}
    
    def _analyze_employment(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze employment data and trends"""
        try:
            # Mock employment data
            employment_data = {
                'USD': {'unemployment_rate': 3.7, 'change': -0.1, 'trend': 'Improving'},
                'EUR': {'unemployment_rate': 6.5, 'change': -0.2, 'trend': 'Improving'},
                'GBP': {'unemployment_rate': 4.2, 'change': 0.1, 'trend': 'Stable'},
                'JPY': {'unemployment_rate': 2.6, 'change': 0.0, 'trend': 'Stable'},
                'CHF': {'unemployment_rate': 2.1, 'change': -0.1, 'trend': 'Improving'},
                'AUD': {'unemployment_rate': 3.8, 'change': 0.0, 'trend': 'Stable'},
                'CAD': {'unemployment_rate': 5.2, 'change': -0.1, 'trend': 'Improving'},
                'NZD': {'unemployment_rate': 3.4, 'change': -0.2, 'trend': 'Improving'}
            }
            
            base_employment = employment_data.get(base, {})
            quote_employment = employment_data.get(quote, {})
            
            return {
                'base_employment': base_employment,
                'quote_employment': quote_employment,
                'relative_strength': (
                    f"{base} employment stronger" if base_employment.get('unemployment_rate', 10) < quote_employment.get('unemployment_rate', 10)
                    else f"{quote} employment stronger" if quote_employment.get('unemployment_rate', 10) < base_employment.get('unemployment_rate', 10)
                    else "Similar employment conditions"
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing employment: {e}")
            return {'error': str(e)}
    
    def _analyze_gdp(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze GDP growth and economic performance"""
        try:
            # Mock GDP data
            gdp_data = {
                'USD': {'growth_rate': 2.3, 'forecast': 2.1, 'trend': 'Stable'},
                'EUR': {'growth_rate': 0.8, 'forecast': 1.2, 'trend': 'Improving'},
                'GBP': {'growth_rate': 1.1, 'forecast': 1.5, 'trend': 'Improving'},
                'JPY': {'growth_rate': 0.9, 'forecast': 1.0, 'trend': 'Stable'},
                'CHF': {'growth_rate': 1.8, 'forecast': 1.6, 'trend': 'Stable'},
                'AUD': {'growth_rate': 1.5, 'forecast': 1.8, 'trend': 'Improving'},
                'CAD': {'growth_rate': 1.9, 'forecast': 2.0, 'trend': 'Stable'},
                'NZD': {'growth_rate': 1.3, 'forecast': 1.7, 'trend': 'Improving'}
            }
            
            base_gdp = gdp_data.get(base, {})
            quote_gdp = gdp_data.get(quote, {})
            
            return {
                'base_gdp': base_gdp,
                'quote_gdp': quote_gdp,
                'relative_performance': (
                    f"{base} economy stronger" if base_gdp.get('growth_rate', 0) > quote_gdp.get('growth_rate', 0)
                    else f"{quote} economy stronger" if quote_gdp.get('growth_rate', 0) > base_gdp.get('growth_rate', 0)
                    else "Similar economic performance"
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing GDP: {e}")
            return {'error': str(e)}
    
    def _analyze_trade_balance(self, base: str, quote: str) -> Dict[str, Any]:
        """Analyze trade balance and current account"""
        try:
            # Mock trade balance data
            trade_data = {
                'USD': {'trade_balance': -70.5, 'trend': 'Improving'},
                'EUR': {'trade_balance': 15.2, 'trend': 'Stable'},
                'GBP': {'trade_balance': -12.8, 'trend': 'Worsening'},
                'JPY': {'trade_balance': 8.9, 'trend': 'Stable'},
                'CHF': {'trade_balance': 25.1, 'trend': 'Improving'},
                'AUD': {'trade_balance': -2.1, 'trend': 'Stable'},
                'CAD': {'trade_balance': 3.2, 'trend': 'Improving'},
                'NZD': {'trade_balance': -1.8, 'trend': 'Stable'}
            }
            
            base_trade = trade_data.get(base, {})
            quote_trade = trade_data.get(quote, {})
            
            return {
                'base_trade_balance': base_trade,
                'quote_trade_balance': quote_trade,
                'relative_position': (
                    f"{base} trade position stronger" if base_trade.get('trade_balance', 0) > quote_trade.get('trade_balance', 0)
                    else f"{quote} trade position stronger" if quote_trade.get('trade_balance', 0) > base_trade.get('trade_balance', 0)
                    else "Similar trade positions"
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trade balance: {e}")
            return {'error': str(e)}
    
    def _generate_fundamental_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall fundamental analysis summary"""
        try:
            bullish_factors = 0
            bearish_factors = 0
            total_factors = 0
            
            # Analyze interest rate differential
            if 'interest_rate_analysis' in analysis and 'differential' in analysis['interest_rate_analysis']:
                total_factors += 1
                if analysis['interest_rate_analysis']['differential'] > 0.25:
                    bullish_factors += 1
                elif analysis['interest_rate_analysis']['differential'] < -0.25:
                    bearish_factors += 1
            
            # Analyze economic indicators
            if 'economic_indicators' in analysis and 'relative_strengths' in analysis['economic_indicators']:
                strengths = analysis['economic_indicators']['relative_strengths']
                base_currency = analysis.get('base_currency', '')
                
                for indicator, strength in strengths.items():
                    total_factors += 1
                    if f"{base_currency} stronger" in strength:
                        bullish_factors += 1
                    elif base_currency not in strength and "stronger" in strength:
                        bearish_factors += 1
            
            # Analyze central bank stance
            if 'central_bank_analysis' in analysis and 'relative_stance' in analysis['central_bank_analysis']:
                total_factors += 1
                stance = analysis['central_bank_analysis']['relative_stance']
                if stance > 0:
                    bullish_factors += 1
                elif stance < 0:
                    bearish_factors += 1
            
            # Analyze market sentiment
            if 'market_sentiment' in analysis and 'overall_sentiment' in analysis['market_sentiment']:
                total_factors += 1
                sentiment = analysis['market_sentiment']['overall_sentiment']
                if sentiment == 'Bullish':
                    bullish_factors += 1
                elif sentiment == 'Bearish':
                    bearish_factors += 1
            
            # Calculate overall fundamental bias
            if total_factors == 0:
                overall_bias = 'Neutral'
                confidence = 0
            else:
                bullish_ratio = bullish_factors / total_factors
                bearish_ratio = bearish_factors / total_factors
                
                if bullish_ratio > 0.6:
                    overall_bias = 'Bullish'
                    confidence = bullish_ratio * 100
                elif bearish_ratio > 0.6:
                    overall_bias = 'Bearish'
                    confidence = bearish_ratio * 100
                else:
                    overall_bias = 'Neutral'
                    confidence = 50
            
            # Generate key insights
            key_insights = []
            
            if 'interest_rate_analysis' in analysis:
                differential = analysis['interest_rate_analysis'].get('differential', 0)
                if abs(differential) > 1.0:
                    key_insights.append(f"Significant interest rate differential of {differential}%")
            
            if 'economic_calendar' in analysis:
                high_impact = analysis['economic_calendar'].get('high_impact_count', 0)
                if high_impact > 0:
                    key_insights.append(f"{high_impact} high-impact economic events upcoming")
            
            return {
                'overall_bias': overall_bias,
                'confidence': round(confidence, 1),
                'bullish_factors': bullish_factors,
                'bearish_factors': bearish_factors,
                'total_factors': total_factors,
                'key_insights': key_insights,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating fundamental summary: {e}")
            return {
                'overall_bias': 'Unknown',
                'confidence': 0,
                'error': str(e)
            }
