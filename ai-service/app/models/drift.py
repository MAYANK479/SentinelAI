import numpy as np
import pandas as pd
from typing import Dict, Any, List

def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckettype: str = 'bins', buckets: int = 10) -> float:
    """
    Calculate the Population Stability Index (PSI).
    Args:
        expected: Array of expected values (e.g., training distribution).
        actual: Array of actual values (e.g., recent production predictions).
        buckettype: 'bins' (equal width) or 'quantiles' (equal frequency).
        buckets: Number of buckets.
    Returns:
        psi_value: The calculated PSI.
    """
    def scale_range (input, min, max):
        input += -(np.min(input))
        input /= np.max(input) / (max - min)
        input += min
        return input

    breakpoints = np.arange(0, buckets + 1) / (buckets) * 100

    if buckettype == 'bins':
        breakpoints = scale_range(breakpoints, np.min(expected), np.max(expected))
    elif buckettype == 'quantiles':
        breakpoints = np.percentile(expected, breakpoints)

    expected_percents = np.histogram(expected, breakpoints)[0] / len(expected)
    actual_percents = np.histogram(actual, breakpoints)[0] / len(actual)

    def sub_psi(e_perc, a_perc):
        """Calculate the actual PSI value from comparing the values."""
        if a_perc == 0:
            a_perc = 0.0001
        if e_perc == 0:
            e_perc = 0.0001
        return (e_perc - a_perc) * np.log(e_perc / a_perc)

    psi_value = np.sum(sub_psi(expected_percents[i], actual_percents[i]) for i in range(0, len(expected_percents)))

    return psi_value

def check_model_drift(recent_predictions: List[float], baseline_predictions: List[float] = None) -> Dict[str, Any]:
    """
    Checks for model drift using PSI.
    In MVP Phase 1, if baseline is None, we mock a healthy baseline distribution.
    """
    if not recent_predictions:
        return {
            "status": "Unknown",
            "drift_detected": False,
            "psi_score": 0.0,
            "message": "Not enough recent predictions to calculate drift."
        }
        
    actual = np.array(recent_predictions)
    
    if baseline_predictions is None:
        # Mock a baseline that looks somewhat like typical fraud probabilities (mostly 0s, some 1s)
        expected = np.random.beta(0.1, 0.9, size=max(1000, len(actual)))
    else:
        expected = np.array(baseline_predictions)
        
    psi_score = calculate_psi(expected, actual)
    
    drift_detected = psi_score > 0.2
    
    if psi_score < 0.1:
        status = "Healthy"
        msg = "No significant drift detected. Model distribution is stable."
    elif psi_score < 0.2:
        status = "Warning"
        msg = "Slight drift detected. Monitor model performance closely."
    else:
        status = "Critical"
        msg = "Significant model drift detected! Retraining recommended."
        
    return {
        "status": status,
        "drift_detected": bool(drift_detected),
        "psi_score": float(psi_score),
        "message": msg
    }
