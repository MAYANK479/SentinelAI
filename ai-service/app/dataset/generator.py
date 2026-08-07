import numpy as np
import pandas as pd
import random
from typing import Tuple

def generate_synthetic_transactions(num_samples: int = 5000) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generates a realistic synthetic transaction dataset with fraud labels.
    Features:
        - Amount (numerical)
        - MerchantCategoryRisk (0 to 1, higher is riskier e.g., electronics, gambling)
        - NightTime (0 or 1, late night hours)
        - Velocity (count of transactions in last 1 hour)
        - GeographicJump (0 or 1, sudden change in location)
        - NewDevice (0 or 1, transaction from an unrecognized device)
        - VPNUsed (0 or 1, transaction through a proxy/VPN)
        - SpendDeviation (ratio of transaction amount to historical average)
        - FailedAttempts (count of failed payment attempts prior to transaction)
    """
    np.random.seed(42)
    random.seed(42)
    
    # Base distributions
    amounts = np.random.exponential(scale=75.0, size=num_samples) + 2.0  # min $2, mean ~$77
    merchant_risk = np.random.beta(a=1, b=3, size=num_samples)  # skewed towards low risk
    night_time = np.random.choice([0, 1], size=num_samples, p=[0.85, 0.15])
    velocity = np.random.poisson(lam=1.5, size=num_samples) + 1
    geo_jump = np.random.choice([0, 1], size=num_samples, p=[0.97, 0.03])
    new_device = np.random.choice([0, 1], size=num_samples, p=[0.90, 0.10])
    vpn_used = np.random.choice([0, 1], size=num_samples, p=[0.95, 0.05])
    spend_deviation = np.random.lognormal(mean=0, sigma=0.5, size=num_samples)
    failed_attempts = np.random.choice([0, 1, 2, 3], size=num_samples, p=[0.85, 0.10, 0.03, 0.02])
    
    # Create DataFrame
    df = pd.DataFrame({
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
    # Fraud occurs when multiple indicators are high, or specific critical triggers fire
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
    
    # Clip probability to [0, 1]
    fraud_prob = np.clip(fraud_prob, 0.0, 1.0)
    
    # Label generation
    is_fraud = np.random.binomial(n=1, p=fraud_prob)
    
    # Make features correlate even more strongly with labels to make it interesting
    # Inject some noise and structured features
    df['Amount'] = np.where(is_fraud == 1, df['Amount'] * np.random.uniform(1.5, 3.5, size=num_samples), df['Amount'])
    df['SpendDeviation'] = np.where(is_fraud == 1, df['SpendDeviation'] * np.random.uniform(2.0, 5.0, size=num_samples), df['SpendDeviation'])
    df['MerchantCategoryRisk'] = np.where(is_fraud == 1, np.minimum(1.0, df['MerchantCategoryRisk'] + np.random.uniform(0.3, 0.6, size=num_samples)), df['MerchantCategoryRisk'])
    
    return df, pd.Series(is_fraud, name='IsFraud')
