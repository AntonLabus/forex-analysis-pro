"""
Debug script to test technical analysis
"""

from backend.data_fetcher import DataFetcher
from backend.technical_analysis import TechnicalAnalysis
import pandas as pd

def test_technical_analysis():
    # Initialize components
    data_fetcher = DataFetcher()
    technical_analysis = TechnicalAnalysis()
    
    # Get sample data
    print("Fetching historical data...")
    data = data_fetcher.get_historical_data('EURUSD', '1mo', '1h')
    
    if data is not None:
        print(f"Data shape: {data.shape}")
        print(f"Data columns: {list(data.columns)}")
        print("First few rows:")
        print(data.head())
        
        # Standardize column names for technical analysis (it expects lowercase)
        data_copy = data.copy()
        data_copy.columns = [col.lower() for col in data_copy.columns]
        print(f"Standardized columns: {list(data_copy.columns)}")
        
        # Perform technical analysis
        print("\nPerforming technical analysis...")
        analysis = technical_analysis.analyze_pair(data_copy, 'EURUSD', '1h')
        
        print("\nAnalysis result:")
        print(f"Keys: {list(analysis.keys())}")
        
        if 'summary' in analysis:
            print(f"Summary: {analysis['summary']}")
        
        if 'trend_analysis' in analysis:
            print(f"Trend analysis: {analysis['trend_analysis']}")
        
        if 'error' in analysis:
            print(f"Error: {analysis['error']}")
            
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    test_technical_analysis()
