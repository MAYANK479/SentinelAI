import numpy as np
import pandas as pd
import random
from typing import Tuple

# Pre-generate some mock customer baselines for Phase 1
NUM_CUSTOMERS = 1000
np.random.seed(42)
CUSTOMER_BASELINES = {
    f"CUST_{i:04d}": {
        "avg_amount": np.random.lognormal(mean=3.5, sigma=0.8), # $33 typical
        "avg_velocity": np.random.poisson(lam=1.5),
    } for i in range(NUM_CUSTOMERS)
}

def generate_synthetic_stream_batch(num_samples: int = 100) -> pd.DataFrame:
    """
    Generates a realistic synthetic transaction dataset for live streaming demo.
    Phase 1: Added customer_id and baseline tracking.
    """
    # Pick random customers
    customer_ids = [f"CUST_{np.random.randint(0, NUM_CUSTOMERS):04d}" for _ in range(num_samples)]
    
    # Base distributions based on customer baseline
    amounts = np.array([np.random.exponential(scale=CUSTOMER_BASELINES[cid]["avg_amount"]) for cid in customer_ids])
    merchant_risk = np.random.beta(a=1, b=3, size=num_samples)  
    night_time = np.random.choice([0, 1], size=num_samples, p=[0.85, 0.15])
    velocity = np.array([np.random.poisson(lam=CUSTOMER_BASELINES[cid]["avg_velocity"]) + 1 for cid in customer_ids])
    geo_jump = np.random.choice([0, 1], size=num_samples, p=[0.97, 0.03])
    new_device = np.random.choice([0, 1], size=num_samples, p=[0.90, 0.10])
    vpn_used = np.random.choice([0, 1], size=num_samples, p=[0.95, 0.05])
    
    # SpendDeviation is now explicitly tied to the customer baseline
    spend_deviation = np.array([amounts[i] / max(1.0, CUSTOMER_BASELINES[cid]["avg_amount"]) for i, cid in enumerate(customer_ids)])
    failed_attempts = np.random.choice([0, 1, 2, 3], size=num_samples, p=[0.85, 0.10, 0.03, 0.02])
    
    # Create DataFrame
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'Amount': amounts,
        'MerchantCategoryRisk': merchant_risk,
        'NightTime': night_time,
        'Velocity': velocity,
        'GeographicJump': geo_jump,
        'NewDevice': new_device,
        'VPNUsed': vpn_used,
        'SpendDeviation': spend_deviation,
        'FailedAttempts': failed_attempts
    })
    
    # Constructing a realistic fraud logic (ground truth generation)
    fraud_prob = (
        0.02 +  # base rate
        0.25 * df['GeographicJump'] +
        0.20 * df['VPNUsed'] * df['NewDevice'] +
        0.15 * (df['Amount'] > 500).astype(int) * df['NewDevice'] +
        0.10 * df['MerchantCategoryRisk'] * (df['SpendDeviation'] > 3.0).astype(int) +
        0.12 * (df['Velocity'] > 5).astype(int) +
        0.10 * (df['FailedAttempts'] >= 2).astype(int) +
        0.05 * df['NightTime'] * (df['Amount'] > 200).astype(int)
    )
    
    fraud_prob = np.clip(fraud_prob, 0.0, 1.0)
    is_fraud = np.random.binomial(n=1, p=fraud_prob)
    
    # Inject some noise and structured features for frauds
    df['Amount'] = np.where(is_fraud == 1, df['Amount'] * np.random.uniform(2.5, 5.5, size=num_samples), df['Amount'])
    df['SpendDeviation'] = np.where(is_fraud == 1, df['SpendDeviation'] * np.random.uniform(3.0, 6.0, size=num_samples), df['SpendDeviation'])
    df['MerchantCategoryRisk'] = np.where(is_fraud == 1, np.minimum(1.0, df['MerchantCategoryRisk'] + np.random.uniform(0.3, 0.6, size=num_samples)), df['MerchantCategoryRisk'])
    
    df['IsFraud'] = is_fraud
    
    return df
