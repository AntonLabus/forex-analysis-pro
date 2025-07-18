<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Forex Analysis Pro - Copilot Instructions

This is a comprehensive forex analysis and trading platform that combines technical and fundamental analysis to generate trading signals with confidence percentages.

## Project Structure
- `/backend/` - Flask API server with data fetching and analysis
- `/frontend/` - TradingView-style web interface
- `/analysis/` - Technical and fundamental analysis modules
- `/data/` - Data processing and storage modules
- `/signals/` - Trading signal generation system

## Key Technologies
- **Backend**: Flask, Python, NumPy, Pandas, TA-Lib
- **Frontend**: HTML5, CSS3, JavaScript ES6+, TradingView Charting Library
- **Data Sources**: Yahoo Finance, Alpha Vantage, Economic Calendar APIs
- **Analysis**: Technical indicators, fundamental analysis, machine learning

## Coding Guidelines
- Use type hints for all Python functions
- Implement proper error handling and logging
- Follow RESTful API design principles
- Ensure responsive design for mobile compatibility
- Use async/await for data fetching operations
- Implement proper caching for API responses

## Key Features to Implement
1. Real-time forex data feeds for all major currency pairs
2. Advanced technical analysis with 20+ indicators
3. Fundamental analysis with economic calendar integration
4. Signal generation with confidence scoring (0-100%)
5. Interactive TradingView-style charts
6. Risk management calculations
7. Portfolio tracking and analysis
8. Real-time notifications and alerts
