from typing import Dict, Any

# Mock behavior DB linking to the baselines in synthetic generator for MVP
# In Phase 2, this would fetch from PostgreSQL `behavior_profiles` table.
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset"))
try:
    from app.dataset.synthetic_augment import CUSTOMER_BASELINES
except ImportError:
    CUSTOMER_BASELINES = {}

def calculate_behavior_score(transaction: Dict[str, Any]) -> float:
    """
    Calculates a risk score (0-100) based on deviation from customer's historical baseline.
    Uses z-score approximation.
    """
    customer_id = transaction.get("customer_id")
    if not customer_id or customer_id not in CUSTOMER_BASELINES:
        return 50.0 # Unknown customer, neutral behavior score
        
    baseline = CUSTOMER_BASELINES[customer_id]
    
    score = 0.0
    
    # Amount deviation (Z-score logic)
    amount = transaction.get("Amount", 0)
    avg_amount = max(1.0, baseline.get("avg_amount", 10.0))
    # Assume std_dev is roughly 0.5 * avg_amount for the lognormal distro we used
    std_dev = 0.5 * avg_amount
    z_amount = (amount - avg_amount) / max(1.0, std_dev)
    
    if z_amount > 2.0:
        score += min(50.0, z_amount * 10) # cap at +50 for amount
        
    # Velocity deviation
    velocity = transaction.get("Velocity", 0)
    avg_velocity = max(1.0, baseline.get("avg_velocity", 1.0))
    if velocity > avg_velocity * 3:
        score += 30.0
    elif velocity > avg_velocity * 2:
        score += 15.0
        
    return min(100.0, score)
