# Forex Analysis Pro

A comprehensive multi-currency trading analysis platform that combines advanced technical and fundamental analysis to generate trading signals with confidence percentages. Features TradingView-style charts, real-time data feeds, and professional trading tools.

## 🚀 Features

### 📊 Advanced Analysis Engine
- **Technical Analysis**: 20+ indicators including RSI, MACD, Bollinger Bands, Moving Averages, ADX, Williams %R, CCI, Stochastic, and more
- **Fundamental Analysis**: Economic calendar integration, interest rate differentials, central bank policy tracking, inflation analysis
- **Pattern Recognition**: Support/resistance levels, trend detection, candlestick patterns
- **Signal Generation**: Combined technical + fundamental signals with confidence scoring (0-100%)

### � Trading Features
- **Multi-Currency Support**: All major forex pairs (EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CHF, USD/CAD, NZD/USD, GBP/JPY)
- **Multi-Timeframe Analysis**: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M
- **Real-Time Data**: Live price feeds with WebSocket connections
- **Risk Management**: Position sizing, stop-loss/take-profit calculations
- **Portfolio Tracking**: Performance metrics, trade history, win rate analysis

### 🎨 Professional Interface
- **TradingView-Style Charts**: Interactive Plotly.js charts with professional styling
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Themes**: Toggle between professional trading themes
- **Real-Time Updates**: Live price cards, signal notifications, market status
- **Dashboard Overview**: Market summary, active signals, portfolio performance

### 🔧 Technical Infrastructure
- **Flask Backend**: RESTful API with WebSocket support
- **SQLite Database**: Data persistence and signal tracking
- **Multi-Source Data**: Yahoo Finance, Alpha Vantage, economic calendars
- **Error Handling**: Comprehensive error handling and fallback mechanisms
- **Caching System**: Optimized data retrieval and storage

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for data feeds

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/forex-analysis-pro.git
cd forex-analysis-pro

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
# Configure environment variables (optional)
cp .env.example .env
# Edit .env with your API keys if you have them

# Run the application
python app.py
```

The application will start on `http://localhost:5000`

### Environment Variables (Optional)
Create a `.env` file for API keys (the app works with free data sources by default):

```env
# Optional: Alpha Vantage API key for additional data sources
ALPHA_VANTAGE_API_KEY=your_key_here

# Optional: News API key for sentiment analysis
NEWS_API_KEY=your_key_here

# Optional: Economic Calendar API key
ECONOMIC_CALENDAR_API_KEY=your_key_here

# Flask configuration
FLASK_ENV=development
DEBUG=True
```

## 🎯 How to Use

### 1. Dashboard Overview
- **Market Overview**: Real-time price cards for all major forex pairs
- **Signal Summary**: Active buy/sell signals with confidence percentages
- **Connection Status**: Live data feed status indicator
- **Quick Stats**: Portfolio performance and market metrics

### 2. Technical Analysis
- **Select Currency Pair**: Choose from EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CHF, USD/CAD, NZD/USD, GBP/JPY
- **Choose Timeframe**: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M
- **View Indicators**: Toggle between SMA, EMA, Bollinger Bands, RSI, MACD, and more
- **Analyze Results**: Review technical summary, trend analysis, and oscillator readings

### 3. Trading Signals
- **Signal Cards**: View buy/sell signals with confidence percentages
- **Signal Details**: Click for detailed analysis breakdown
- **Filter Signals**: Filter by currency pair, signal type, or confidence level
- **Real-Time Updates**: Signals update automatically as market conditions change

### 4. Fundamental Analysis
- **Economic Calendar**: View upcoming economic events and their impact
- **Interest Rate Analysis**: Monitor central bank rates and differentials
- **Market Sentiment**: Track news sentiment and market positioning
- **Currency Strength**: Compare relative strength across currencies

## 📊 Technical Indicators

### Trend Indicators
- **Simple Moving Average (SMA)**: 20, 50, 200 periods
- **Exponential Moving Average (EMA)**: 12, 26, 50 periods
- **Average Directional Index (ADX)**: Trend strength measurement
- **Parabolic SAR**: Stop and reverse points

### Momentum Oscillators
- **Relative Strength Index (RSI)**: 14-period momentum oscillator
- **MACD**: Moving Average Convergence Divergence with signal line
- **Stochastic**: %K and %D momentum indicators
- **Williams %R**: Momentum indicator measuring overbought/oversold
- **Commodity Channel Index (CCI)**: Cyclical trend indicator

### Volatility Indicators
- **Bollinger Bands**: Price envelope with standard deviation
- **Average True Range (ATR)**: Volatility measurement
- **Volatility Index**: Custom volatility calculation

### Volume Indicators
- **On-Balance Volume (OBV)**: Volume-price relationship
- **Volume Profile**: Price-volume distribution analysis

## 📈 Signal Generation

### Technical Signal Scoring
- **Trend Alignment**: Multiple timeframe trend confirmation
- **Momentum Confirmation**: RSI, MACD, Stochastic alignment
- **Support/Resistance**: Key level breaks and bounces
- **Pattern Recognition**: Candlestick and chart patterns

### Fundamental Signal Scoring
- **Interest Rate Differentials**: Central bank policy impact
- **Economic Data**: GDP, inflation, employment data
- **Market Sentiment**: News sentiment and positioning data
- **Calendar Events**: High-impact economic releases

### Combined Confidence Score
- **Technical Weight**: 60% (configurable)
- **Fundamental Weight**: 40% (configurable)
- **Risk Assessment**: Stop-loss and take-profit levels
- **Position Sizing**: Risk-based position calculations

## 🛠️ Architecture

### Backend Components
- **Flask Application** (`app.py`): Main server with REST API and WebSocket support
- **Data Fetcher** (`backend/data_fetcher.py`): Multi-source data retrieval with caching
- **Technical Analysis** (`backend/technical_analysis.py`): TA-Lib based indicator calculations
- **Fundamental Analysis** (`backend/fundamental_analysis.py`): Economic data analysis
- **Signal Generator** (`backend/signal_generator.py`): Combined signal scoring algorithm
- **Database Layer** (`backend/database.py`): SQLite data persistence

### Frontend Components
- **Main Application** (`frontend/static/js/app.js`): Application orchestration and WebSocket handling
- **Chart Manager** (`frontend/static/js/chart.js`): Plotly.js chart rendering and indicator plotting
- **Signal Manager** (`frontend/static/js/signals.js`): Signal display and filtering
- **Utilities** (`frontend/static/js/utils.js`): Helper functions and API communication
- **Configuration** (`frontend/static/js/config.js`): Application settings and constants

### Database Schema
- **price_data**: Historical and real-time price storage
- **signals**: Generated trading signals with metadata
- **analysis_results**: Technical and fundamental analysis cache
- **user_preferences**: Customizable settings and watchlists

## 🎛️ Configuration

### Currency Pairs
- EUR/USD, GBP/USD, USD/JPY, AUD/USD
- USD/CHF, USD/CAD, NZD/USD, GBP/JPY

### Timeframes
- 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M

### API Endpoints
- `/api/forex/pairs` - Available currency pairs
- `/api/forex/data/<pair>` - Historical price data
- `/api/analysis/technical/<pair>` - Technical analysis
- `/api/analysis/fundamental/<pair>` - Fundamental analysis
- `/api/signals/<pair>` - Trading signals
- `/api/portfolio` - Portfolio data

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with Docker
docker build -t forex-analysis-pro .
docker run -p 5000:5000 forex-analysis-pro
```

### Environment Setup
```bash
# Set production environment
export FLASK_ENV=production
export DEBUG=False

# Configure database URL
export DATABASE_URL=sqlite:///forex_data.db
```

## 📞 Support & Contributing

### Getting Help
- 📧 Email: support@forexanalysispro.com
- 💬 Discord: [Community Server](https://discord.gg/forexanalysis)
- 📖 Documentation: [Wiki](https://github.com/yourusername/forex-analysis-pro/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/forex-analysis-pro/issues)

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TA-Lib**: Technical analysis library
- **Plotly.js**: Interactive charting library
- **Flask**: Web framework
- **yfinance**: Yahoo Finance data
- **Alpha Vantage**: Financial data API
- **Socket.IO**: Real-time communication

## ⚠️ Disclaimer

This software is for educational and informational purposes only. It should not be considered financial advice. Trading forex involves substantial risk and may not be suitable for all investors. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making trading decisions.

---

**Forex Analysis Pro** - Professional Multi-Currency Trading Analysis Platform

*Built with ❤️ for traders by traders*
- **Utilities** (`frontend/static/js/utils.js`): Helper functions and API communication
- **Configuration** (`frontend/static/js/config.js`): Application settings and constants

### Database Schema
- **price_data**: Historical and real-time price storage
- **signals**: Generated trading signals with metadata
- **analysis_results**: Technical and fundamental analysis cache
- **user_preferences**: Customizable settings and watchlists

## 🔧 Customization

### Adding New Indicators
1. Implement indicator calculation in `backend/technical_analysis.py`
2. Add indicator to signal scoring in `backend/signal_generator.py`
3. Update chart rendering in `frontend/static/js/chart.js`
4. Add UI controls in `frontend/templates/index.html`

### Modifying Signal Logic
1. Edit scoring weights in `backend/signal_generator.py`
2. Adjust fundamental factors in `backend/fundamental_analysis.py`
3. Update confidence thresholds in configuration

### Customizing UI
1. Modify styles in `frontend/static/css/styles.css`
2. Update layouts in `frontend/templates/index.html`
3. Adjust themes and colors in CSS variables

## 📱 Mobile Support

The application is fully responsive and works on:
- **Desktop**: Full feature set with multiple panels
- **Tablet**: Optimized layouts with collapsible sidebars
- **Mobile**: Touch-friendly interface with swipe navigation

## ⚡ Performance

### Optimization Features
- **Data Caching**: Redis-based caching for API responses
- **WebSocket Updates**: Real-time data without polling
- **Lazy Loading**: Charts and data load on demand
- **Compression**: Gzipped responses for faster loading
- **CDN Integration**: Static assets served from CDN

### Monitoring
- **Health Checks**: API endpoint monitoring
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Response time tracking
- **User Analytics**: Usage pattern analysis

## 🔒 Security

### Data Protection
- **Input Validation**: All user inputs sanitized
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output encoding and CSP headers
- **Rate Limiting**: API request throttling

### API Security
- **CORS Configuration**: Restricted cross-origin requests
- **API Key Management**: Secure key storage and rotation
- **Authentication**: Token-based authentication (optional)
- **HTTPS Enforcement**: SSL/TLS encryption

## 🧪 Testing

### Running Tests
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Frontend tests
npm test
```

### Test Coverage
- **Backend**: Unit tests for all analysis modules
- **API**: Integration tests for all endpoints
- **Frontend**: JavaScript unit tests and UI tests
- **Performance**: Load testing and stress testing

4. **Trading Signals**
   - Review buy/sell signals with confidence percentages
   - Set up custom alerts and notifications
   - Track signal performance over time

## API Endpoints

### Market Data
- `GET /api/forex/pairs` - Get all available currency pairs
- `GET /api/forex/data/{pair}` - Get price data for specific pair
- `GET /api/forex/realtime/{pair}` - Get real-time quotes

### Analysis
- `GET /api/analysis/technical/{pair}` - Technical analysis results
- `GET /api/analysis/fundamental/{pair}` - Fundamental analysis scores
- `GET /api/signals/{pair}` - Current trading signals

### User Features
- `GET /api/watchlist` - User's watchlist
- `POST /api/alerts` - Create price alerts
- `GET /api/portfolio` - Portfolio analysis

## Technology Stack

### Backend
- **Flask**: Web framework and API server
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **TA-Lib**: Technical analysis library
- **Requests**: HTTP client for data fetching
- **SQLAlchemy**: Database ORM
- **Redis**: Caching and session storage

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript ES6+**: Modern JavaScript features
- **TradingView Charting Library**: Professional charts
- **WebSocket**: Real-time data updates
- **Chart.js**: Additional charting capabilities

### Data Sources
- **Yahoo Finance**: Free forex data
- **Alpha Vantage**: Premium forex and economic data
- **Economic Calendar API**: Fundamental events
- **News APIs**: Market sentiment analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational and informational purposes only. Trading forex involves substantial risk and may not be suitable for all investors. Past performance is not indicative of future results. Please consult with a financial advisor before making investment decisions.
#   f o r e x - a n a l y s i s - p r o  
 