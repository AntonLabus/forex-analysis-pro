"""
Database Module
Handles data persistence for the Forex Analysis Pro application
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
import os

logger = logging.getLogger(__name__)

class Database:
    """
    Database manager for storing analysis results, signals, and user data
    """
    
    def __init__(self, db_path: str = 'forex_analysis.db'):
        self.db_path = db_path
        self.connection = None
    
    def init_db(self):
        """Initialize the database with required tables"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            
            # Create tables
            self._create_tables()
            
            logger.info(f"Database initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_tables(self):
        """Create all required database tables"""
        cursor = self.connection.cursor()
        
        # Price data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                open_price REAL NOT NULL,
                high_price REAL NOT NULL,
                low_price REAL NOT NULL,
                close_price REAL NOT NULL,
                volume REAL,
                timeframe TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pair, timestamp, timeframe)
            )
        ''')
        
        # Technical analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                timeframe TEXT NOT NULL,
                analysis_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pair, timestamp, timeframe)
            )
        ''')
        
        # Fundamental analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fundamental_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                analysis_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(pair, timestamp)
            )
        ''')
        
        # Trading signals
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                signal_direction TEXT NOT NULL,
                confidence REAL NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit_1 REAL,
                take_profit_2 REAL,
                signal_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User watchlist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                pair TEXT NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, pair)
            )
        ''')
        
        # Price alerts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                pair TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                target_price REAL NOT NULL,
                current_price REAL NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                triggered_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Signal performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signal_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id INTEGER NOT NULL,
                pair TEXT NOT NULL,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                entry_price REAL NOT NULL,
                exit_price REAL,
                pnl REAL,
                pnl_pips REAL,
                status TEXT DEFAULT 'OPEN',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (signal_id) REFERENCES trading_signals (id)
            )
        ''')
        
        self.connection.commit()
        logger.info("Database tables created successfully")
    
    def store_price_data(self, pair: str, data: pd.DataFrame, timeframe: str):
        """Store historical price data"""
        try:
            cursor = self.connection.cursor()
            
            for index, row in data.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO price_data 
                    (pair, timestamp, open_price, high_price, low_price, close_price, volume, timeframe)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pair,
                    index.isoformat(),
                    float(row['Open']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Close']),
                    float(row.get('Volume', 0)),
                    timeframe
                ))
            
            self.connection.commit()
            logger.info(f"Stored {len(data)} price records for {pair} ({timeframe})")
            
        except Exception as e:
            logger.error(f"Error storing price data: {e}")
            raise
    
    def store_technical_analysis(self, pair: str, timeframe: str, analysis: Dict[str, Any]):
        """Store technical analysis results"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO technical_analysis 
                (pair, timestamp, timeframe, analysis_data)
                VALUES (?, ?, ?, ?)
            ''', (
                pair,
                datetime.now().isoformat(),
                timeframe,
                json.dumps(analysis)
            ))
            
            self.connection.commit()
            logger.info(f"Stored technical analysis for {pair} ({timeframe})")
            
        except Exception as e:
            logger.error(f"Error storing technical analysis: {e}")
            raise
    
    def store_fundamental_analysis(self, pair: str, analysis: Dict[str, Any]):
        """Store fundamental analysis results"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO fundamental_analysis 
                (pair, timestamp, analysis_data)
                VALUES (?, ?, ?)
            ''', (
                pair,
                datetime.now().isoformat(),
                json.dumps(analysis)
            ))
            
            self.connection.commit()
            logger.info(f"Stored fundamental analysis for {pair}")
            
        except Exception as e:
            logger.error(f"Error storing fundamental analysis: {e}")
            raise
    
    def store_trading_signal(self, signal: Dict[str, Any]) -> int:
        """Store trading signal and return signal ID"""
        try:
            cursor = self.connection.cursor()
            
            levels = signal.get('levels', {})
            
            cursor.execute('''
                INSERT INTO trading_signals 
                (pair, timestamp, signal_direction, confidence, entry_price, 
                 stop_loss, take_profit_1, take_profit_2, signal_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                signal.get('pair'),
                signal.get('timestamp'),
                signal.get('signal', {}).get('direction'),
                signal.get('signal', {}).get('confidence', 0),
                levels.get('entry'),
                levels.get('stop_loss'),
                levels.get('take_profit_1'),
                levels.get('take_profit_2'),
                json.dumps(signal)
            ))
            
            signal_id = cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"Stored trading signal {signal_id} for {signal.get('pair')}")
            return signal_id
            
        except Exception as e:
            logger.error(f"Error storing trading signal: {e}")
            raise
    
    def get_recent_signals(self, pair: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent trading signals"""
        try:
            cursor = self.connection.cursor()
            
            if pair:
                cursor.execute('''
                    SELECT * FROM trading_signals 
                    WHERE pair = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (pair, limit))
            else:
                cursor.execute('''
                    SELECT * FROM trading_signals 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            
            signals = []
            for row in rows:
                signal_data = json.loads(row['signal_data'])
                signals.append({
                    'id': row['id'],
                    'pair': row['pair'],
                    'timestamp': row['timestamp'],
                    'direction': row['signal_direction'],
                    'confidence': row['confidence'],
                    'entry_price': row['entry_price'],
                    'stop_loss': row['stop_loss'],
                    'take_profit_1': row['take_profit_1'],
                    'take_profit_2': row['take_profit_2'],
                    'signal_data': signal_data,
                    'created_at': row['created_at']
                })
            
            return signals
            
        except Exception as e:
            logger.error(f"Error getting recent signals: {e}")
            return []
    
    def add_to_watchlist(self, user_id: str, pair: str):
        """Add a pair to user's watchlist"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO watchlist (user_id, pair)
                VALUES (?, ?)
            ''', (user_id, pair))
            
            self.connection.commit()
            logger.info(f"Added {pair} to watchlist for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")
            raise
    
    def get_watchlist(self, user_id: str) -> List[str]:
        """Get user's watchlist"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                SELECT pair FROM watchlist 
                WHERE user_id = ? 
                ORDER BY added_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            return [row['pair'] for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting watchlist: {e}")
            return []
    
    def create_price_alert(self, user_id: str, pair: str, alert_type: str, 
                          target_price: float, current_price: float):
        """Create a price alert"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO price_alerts 
                (user_id, pair, alert_type, target_price, current_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, pair, alert_type, target_price, current_price))
            
            alert_id = cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"Created price alert {alert_id} for {pair}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating price alert: {e}")
            raise
    
    def get_active_alerts(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active price alerts"""
        try:
            cursor = self.connection.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT * FROM price_alerts 
                    WHERE user_id = ? AND is_active = 1 
                    ORDER BY created_at DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT * FROM price_alerts 
                    WHERE is_active = 1 
                    ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            
            alerts = []
            for row in rows:
                alerts.append({
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'pair': row['pair'],
                    'alert_type': row['alert_type'],
                    'target_price': row['target_price'],
                    'current_price': row['current_price'],
                    'created_at': row['created_at']
                })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []
    
    def trigger_alert(self, alert_id: int):
        """Mark an alert as triggered"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                UPDATE price_alerts 
                SET is_active = 0, triggered_at = ? 
                WHERE id = ?
            ''', (datetime.now().isoformat(), alert_id))
            
            self.connection.commit()
            logger.info(f"Triggered alert {alert_id}")
            
        except Exception as e:
            logger.error(f"Error triggering alert: {e}")
            raise
    
    def get_signal_performance(self, days: int = 30) -> Dict[str, Any]:
        """Get signal performance statistics"""
        try:
            cursor = self.connection.cursor()
            
            # Get signals from the last N days
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_signals,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_signals,
                    SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losing_signals,
                    AVG(pnl) as avg_pnl,
                    SUM(pnl) as total_pnl,
                    AVG(confidence) as avg_confidence
                FROM signal_performance sp
                JOIN trading_signals ts ON sp.signal_id = ts.id
                WHERE sp.created_at >= ?
                AND sp.status = 'CLOSED'
            ''', (start_date,))
            
            row = cursor.fetchone()
            
            if row and row['total_signals']:
                win_rate = (row['winning_signals'] / row['total_signals']) * 100
                
                return {
                    'period_days': days,
                    'total_signals': row['total_signals'],
                    'winning_signals': row['winning_signals'],
                    'losing_signals': row['losing_signals'],
                    'win_rate': round(win_rate, 1),
                    'avg_pnl': round(row['avg_pnl'] or 0, 2),
                    'total_pnl': round(row['total_pnl'] or 0, 2),
                    'avg_confidence': round(row['avg_confidence'] or 0, 1)
                }
            else:
                return {
                    'period_days': days,
                    'total_signals': 0,
                    'winning_signals': 0,
                    'losing_signals': 0,
                    'win_rate': 0,
                    'avg_pnl': 0,
                    'total_pnl': 0,
                    'avg_confidence': 0
                }
            
        except Exception as e:
            logger.error(f"Error getting signal performance: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to maintain database size"""
        try:
            cursor = self.connection.cursor()
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            # Clean up old price data
            cursor.execute('''
                DELETE FROM price_data 
                WHERE created_at < ?
            ''', (cutoff_date,))
            
            # Clean up old analysis data
            cursor.execute('''
                DELETE FROM technical_analysis 
                WHERE created_at < ?
            ''', (cutoff_date,))
            
            cursor.execute('''
                DELETE FROM fundamental_analysis 
                WHERE created_at < ?
            ''', (cutoff_date,))
            
            self.connection.commit()
            logger.info(f"Cleaned up data older than {days_to_keep} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

def create_tables():
    """Standalone function to create database tables - used by startup script"""
    try:
        db = Database()
        db.init_db()
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False
