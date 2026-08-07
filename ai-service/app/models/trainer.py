import os
import joblib
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

from app.dataset.loader import load_and_preprocess_data, get_temporal_split

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models_store")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

def precision_at_k(y_true, y_prob, k=100):
    """Calculates precision at top k ranked predictions."""
    if len(y_prob) == 0:
        return 0.0
    k = min(k, len(y_prob))
    order = np.argsort(y_prob)[::-1]
    y_true_sorted = np.array(y_true)[order]
    return np.mean(y_true_sorted[:k])

def f2_score(y_true, y_pred):
    """Calculates F2 score, weighing recall higher than precision."""
    # Fbeta = (1 + beta^2) * (precision * recall) / ( (beta^2 * precision) + recall )
    # Beta = 2
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    if prec + rec == 0:
        return 0.0
    return (5 * prec * rec) / ((4 * prec) + rec)

def train_and_evaluate_models() -> Dict[str, Any]:
    """
    Trains LR, RF, XGBoost.
    Evaluates PR-AUC, F2, Precision@100, cost-saved.
    Saves best model based on PR-AUC.
    """
    X, y = load_and_preprocess_data()
    
    # Split
    X_train, X_val, X_test, y_train, y_val, y_test = get_temporal_split(X, y, train_size=0.7, val_size=0.15)
    
    # SMOTE on training fold only
    print("Applying SMOTE on training data...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Calculate scale_pos_weight for XGBoost
    neg_count = sum(y_train_resampled == 0)
    pos_count = sum(y_train_resampled == 1)
    scale_pos_weight = neg_count / max(1, pos_count)
    
    # Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, scale_pos_weight=scale_pos_weight)
    }
    
    metrics_summary = {}
    best_pr_auc = -1.0
    best_model_name = None
    best_model = None
    
    avg_fraud_amount = 500  # Assumed for cost estimate
    avg_review_cost = 25    # Assumed for cost estimate
    
    for name, clf in models.items():
        print(f"Training {name}...")
        clf.fit(X_train_resampled, y_train_resampled)
        
        # We validate and test on the unseen temporal split
        # Using X_test for final metrics report
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        f2 = f2_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        prec_at_100 = precision_at_k(y_test, y_prob, k=100)
        
        # Cost Estimate
        true_positives = np.sum((y_test == 1) & (y_pred == 1))
        false_positives = np.sum((y_test == 0) & (y_pred == 1))
        
        fraud_caught_value = true_positives * avg_fraud_amount
        wasted_review_cost = false_positives * avg_review_cost
        net_saved = fraud_caught_value - wasted_review_cost
        
        metrics_summary[name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "f2_score": float(f2),
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "precision_at_100": float(prec_at_100),
            "net_cost_saved": float(net_saved)
        }
        
        if pr_auc > best_pr_auc:
            best_pr_auc = pr_auc
            best_model_name = name
            best_model = clf

    print(f"Best model: {best_model_name} with PR-AUC: {best_pr_auc:.4f}")
    
    # Save best model and metadata
    metadata = {
        "best_model": best_model_name,
        "features": list(X.columns),
        "metrics": metrics_summary,
        "num_train_samples": len(X_train),
        "training_date": pd.Timestamp.now().isoformat()
    }
    
    joblib.dump(best_model, MODEL_PATH)
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
        
    return metadata

def get_loaded_model() -> Tuple[Any, Dict[str, Any]]:
    """Loads active model and metadata from store, retraining if missing."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(METADATA_PATH):
        train_and_evaluate_models()
        
    model = joblib.load(MODEL_PATH)
    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)
        
    return model, metadata
