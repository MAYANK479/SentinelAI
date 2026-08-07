import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import RobustScaler
from typing import Tuple

def load_and_preprocess_data(data_path: str = "data/creditcard.csv") -> Tuple[pd.DataFrame, pd.Series]:
    """
    Loads the Kaggle Credit Card Fraud dataset, sorts by Time (to prevent leakage),
    and applies basic preprocessing (scaling).
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, data_path)
    
    if not os.path.exists(full_path):
        # Fallback for testing/MVP if real dataset isn't available yet
        print(f"Warning: {full_path} not found. Using small synthetic fallback for MVP test.")
        return generate_fallback_data()

    print(f"Loading dataset from {full_path}...")
    df = pd.read_csv(full_path)
    
    # Sort by time to ensure temporal split
    df = df.sort_values('Time').reset_index(drop=True)
    
    # Scale Amount and Time features using RobustScaler (less sensitive to outliers)
    scaler = RobustScaler()
    df['Amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df['Time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
    
    y = df['Class']
    X = df.drop(['Class'], axis=1)
    
    return X, y

def generate_fallback_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Generate a small fallback dataset if the real Kaggle CSV isn't found."""
    from .synthetic_augment import generate_synthetic_stream_batch
    # Generate 5000 records for the fallback
    df = generate_synthetic_stream_batch(5000)
    
    # Convert synthetic specific columns to match Kaggle structure roughly
    # Kaggle features: Time, V1-V28, Amount, Class
    # We will just use the synthetic features directly if fallback happens,
    # but the caller expects `X` and `y` where `y` is the label.
    y = df['IsFraud']
    X = df.drop(['IsFraud'], axis=1)
    
    if 'customer_id' in X.columns:
        X = X.drop(['customer_id'], axis=1)
    
    # Add a mock 'Time' if it doesn't exist to prevent errors in sorting
    if 'Time' not in X.columns:
         X['Time'] = np.arange(len(X))
         
    return X, y

def get_temporal_split(X: pd.DataFrame, y: pd.Series, train_size=0.7, val_size=0.15) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Splits the data temporally (70/15/15) assuming it's already sorted by Time.
    """
    n = len(X)
    train_end = int(n * train_size)
    val_end = train_end + int(n * val_size)
    
    X_train = X.iloc[:train_end]
    y_train = y.iloc[:train_end]
    
    X_val = X.iloc[train_end:val_end]
    y_val = y.iloc[train_end:val_end]
    
    X_test = X.iloc[val_end:]
    y_test = y.iloc[val_end:]
    
    return X_train, X_val, X_test, y_train, y_val, y_test
