import sqlite3
import os
import json
from typing import Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sentinel.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # MVP Schema
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            amount REAL,
            merchant_risk REAL,
            night_time INTEGER,
            velocity INTEGER,
            geo_jump INTEGER,
            new_device INTEGER,
            vpn_used INTEGER,
            spend_deviation REAL,
            failed_attempts INTEGER,
            ml_probability REAL,
            rule_score REAL,
            behavior_score REAL,
            composite_score REAL,
            risk_band TEXT,
            is_fraud INTEGER,
            narrative TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS model_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            pr_auc REAL,
            f2_score REAL,
            net_cost_saved REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def save_transaction(tx_data: Dict[str, Any], prediction: Dict[str, Any]):
    """Saves a processed transaction and its prediction to SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (
            customer_id, amount, merchant_risk, night_time, velocity, geo_jump, new_device,
            vpn_used, spend_deviation, failed_attempts, ml_probability, rule_score, behavior_score,
            composite_score, risk_band, is_fraud, narrative
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        tx_data.get("customer_id", ""), tx_data.get("Amount", 0), tx_data.get("MerchantCategoryRisk", 0), tx_data.get("NightTime", 0),
        tx_data.get("Velocity", 0), tx_data.get("GeographicJump", 0), tx_data.get("NewDevice", 0),
        tx_data.get("VPNUsed", 0), tx_data.get("SpendDeviation", 0), tx_data.get("FailedAttempts", 0),
        prediction.get("ml_probability", 0), prediction.get("rule_score", 0), prediction.get("behavior_score", 0), prediction.get("composite_score", 0),
        prediction.get("risk_band", "Safe"), prediction.get("is_fraud", 0), prediction.get("narrative", "")
    ))
    conn.commit()
    conn.close()

# Initialize on module load for MVP
init_db()
