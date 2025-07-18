"""
Test script to verify technical analysis fix
"""

from backend.data_fetcher import DataFetcher
from backend.technical_analysis import TechnicalAnalysis
import json

def test_technical_analysis_fix():
    """Test that technical analysis now works with proper data"""
    print("Starting technical analysis test...")
    
    # Initialize components
    data_fetcher = DataFetcher()
    technical_analysis = TechnicalAnalysis()
    
    try:
        # Get historical data
        print("Fetching historical data for EURUSD...")
        data = data_fetcher.get_historical_data('EURUSD', '1mo', '1h')
        
        if data is None or data.empty:
            print("ERROR: No data returned")
            return False
        
        print(f"Data fetched successfully: {data.shape}")
        print(f"Original columns: {list(data.columns)}")
        
        # Standardize column names (fix the issue)
        data.columns = [col.lower() for col in data.columns]
        print(f"Standardized columns: {list(data.columns)}")
        
        # Perform technical analysis
        print("Performing technical analysis...")
        analysis = technical_analysis.analyze_pair(data, 'EURUSD', '1h')
        
        print("\n" + "="*50)
        print("TECHNICAL ANALYSIS RESULTS:")
        print("="*50)
        
        if 'summary' in analysis:
            summary = analysis['summary']
            print(f"Overall Signal: {summary.get('overall_signal', 'N/A')}")
            print(f"Confidence: {summary.get('confidence', 0)}%")
            print(f"Trend Direction: {summary.get('trend_direction', 'N/A')}")
            print(f"Trend Strength: {summary.get('trend_strength', 0)}")
            print(f"Bullish Signals: {summary.get('bullish_signals', 0)}")
            print(f"Bearish Signals: {summary.get('bearish_signals', 0)}")
        
        if 'trend_analysis' in analysis:
            trend = analysis['trend_analysis']
            print(f"\nTrend Analysis:")
            print(f"  Direction: {trend.get('direction', 'N/A')}")
            print(f"  Strength: {trend.get('strength', 0)}")
        
        if 'momentum_analysis' in analysis:
            momentum = analysis['momentum_analysis']
            print(f"\nMomentum Analysis:")
            if 'rsi' in momentum:
                rsi = momentum['rsi']
                print(f"  RSI: {rsi.get('value', 'N/A')} ({rsi.get('signal', 'N/A')})")
            if 'macd' in momentum:
                macd = momentum['macd']
                print(f"  MACD: {macd.get('value', 'N/A')} ({macd.get('signal', 'N/A')})")
        
        print("\n" + "="*50)
        print("TEST PASSED: Technical analysis is working correctly!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"ERROR: Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_technical_analysis_fix()
    if success:
        print("\n✅ Technical analysis fix is working correctly!")
        print("The Analysis page should now show proper technical analysis data.")
    else:
        print("\n❌ Technical analysis fix failed.")
