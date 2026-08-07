from typing import Dict, Any, List, Tuple

# Default Rules (in MVP these are hardcoded/in-memory, Phase 2 will be DB-backed)
DEFAULT_RULES = [
    {"name": "High Amount", "condition": lambda tx: tx.get("Amount", 0) > 1000, "weight": 30, "active": True},
    {"name": "Extreme Velocity", "condition": lambda tx: tx.get("Velocity", 0) > 10, "weight": 40, "active": True},
    {"name": "Geographic Jump", "condition": lambda tx: tx.get("GeographicJump", 0) == 1, "weight": 50, "active": True},
    {"name": "New Device + High Value", "condition": lambda tx: tx.get("NewDevice", 0) == 1 and tx.get("Amount", 0) > 500, "weight": 45, "active": True},
    {"name": "VPN Used", "condition": lambda tx: tx.get("VPNUsed", 0) == 1, "weight": 20, "active": True},
    {"name": "High Spend Deviation", "condition": lambda tx: tx.get("SpendDeviation", 0) > 4.0, "weight": 35, "active": True},
    {"name": "Multiple Failed Attempts", "condition": lambda tx: tx.get("FailedAttempts", 0) >= 3, "weight": 50, "active": True},
]

def evaluate_rules(transaction: Dict[str, Any], rules: List[Dict[str, Any]] = None) -> Tuple[float, List[str]]:
    """
    Evaluates a transaction against a set of rules.
    Returns a raw rule score (capped at 100) and a list of triggered rule names.
    """
    if rules is None:
        rules = DEFAULT_RULES
        
    score = 0.0
    triggered = []
    
    for rule in rules:
        if rule.get("active", True):
            try:
                if rule["condition"](transaction):
                    score += rule["weight"]
                    triggered.append(rule["name"])
            except Exception as e:
                print(f"Error evaluating rule {rule['name']}: {e}")
                
    # Normalize or cap score to 0-100 range
    final_score = min(score, 100.0)
    
    return final_score, triggered
