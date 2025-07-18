"""
Quick test server to verify technical analysis fixes
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.data_fetcher import DataFetcher
from backend.technical_analysis import TechnicalAnalysis
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
data_fetcher = DataFetcher()
technical_analysis = TechnicalAnalysis()

@app.route('/api/analysis/technical/<pair>')
def get_technical_analysis(pair):
    """Get technical analysis for a forex pair"""
    try:
        timeframe = request.args.get('timeframe', '1h')
        
        print(f"Fetching technical analysis for {pair}, timeframe: {timeframe}")
        
        # Get historical data
        data = data_fetcher.get_historical_data(pair, '3mo', timeframe)
        if data is None or data.empty:
            return jsonify({'success': False, 'error': 'No data available'}), 404
        
        print(f"Data fetched: {data.shape}, columns: {list(data.columns)}")
        
        # Standardize column names for technical analysis (expects lowercase)
        data.columns = [col.lower() for col in data.columns]
        print(f"Standardized columns: {list(data.columns)}")
        
        # Perform technical analysis
        analysis = technical_analysis.analyze_pair(data, pair, timeframe)
        print(f"Analysis result keys: {list(analysis.keys())}")
        
        if 'summary' in analysis:
            print(f"Summary: {analysis['summary']}")
        
        return jsonify({
            'success': True,
            'pair': pair,
            'timeframe': timeframe,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in technical analysis for {pair}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test')
def test_endpoint():
    """Test endpoint to verify server is running"""
    return jsonify({
        'success': True,
        'message': 'Test server is running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting test server on http://localhost:5001")
    print("Test technical analysis: http://localhost:5001/api/analysis/technical/EURUSD")
    app.run(debug=True, host='0.0.0.0', port=5001)
