from typing import Dict, Any

def calculate_composite_score(
    ml_prob: float, 
    rule_score: float, 
    behavior_score: float = 0.0,
    w_ml: float = 0.5, 
    w_rule: float = 0.3,
    w_behavior: float = 0.2
) -> Dict[str, Any]:
    """
    Calculates the final composite risk score combining ML probability, Rule score, and Behavior score.
    Returns the final score and the assigned risk band.
    """
    
    # ml_prob is 0.0 to 1.0, scale to 0-100
    ml_score = ml_prob * 100.0
    
    # Ensure weights sum to 1.0
    total_w = w_ml + w_rule + w_behavior
    w_ml = w_ml / total_w
    w_rule = w_rule / total_w
    w_behavior = w_behavior / total_w
    
    final_score = (ml_score * w_ml) + (rule_score * w_rule) + (behavior_score * w_behavior)
    final_score = min(max(final_score, 0.0), 100.0)
    
    band = get_risk_band(final_score)
    
    return {
        "composite_score": final_score,
        "ml_score": ml_score,
        "rule_score": rule_score,
        "behavior_score": behavior_score,
        "risk_band": band
    }

def get_risk_band(score: float) -> str:
    """Maps a 0-100 score to a risk band."""
    if score <= 30:
        return "Safe"
    elif score <= 60:
        return "Low Risk"
    elif score <= 80:
        return "Suspicious"
    else:
        return "Fraud"
