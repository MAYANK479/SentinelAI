import os
import hashlib
from typing import List, Dict, Any

# Simple in-memory cache for MVP. For production, use Redis or SQLite.
_NARRATIVE_CACHE = {}

def _generate_transaction_hash(amount: float, features: List[Dict[str, Any]], rules: List[str]) -> str:
    """Creates a unique hash for the transaction to cache similar narratives."""
    key = f"{amount}_{str(rules)}_{str([f['feature'] for f in features])}"
    return hashlib.md5(key.encode()).hexdigest()

def generate_case_narrative(
    amount: float,
    fraud_prob: float,
    behavior_score: float,
    shap_features: List[Dict[str, Any]],
    triggered_rules: List[str],
    use_mock: bool = True
) -> str:
    """
    Generates a plain-English case narrative based on model explainability and rule triggers.
    Calls an LLM API (or a mock for MVP) and caches the result.
    """
    tx_hash = _generate_transaction_hash(amount, shap_features, triggered_rules)
    
    if tx_hash in _NARRATIVE_CACHE:
        return _NARRATIVE_CACHE[tx_hash]
        
    if use_mock or not os.getenv("LLM_API_KEY"):
        narrative = _mock_llm_generation(amount, fraud_prob, behavior_score, shap_features, triggered_rules)
    else:
        narrative = _call_real_llm_api(amount, fraud_prob, behavior_score, shap_features, triggered_rules)
        
    _NARRATIVE_CACHE[tx_hash] = narrative
    return narrative

def _mock_llm_generation(amount: float, fraud_prob: float, behavior_score: float, shap_features: List[Dict[str, Any]], triggered_rules: List[str]) -> str:
    """A deterministic mock to simulate an LLM response without an API key."""
    if fraud_prob < 0.3 and behavior_score < 40:
        return f"Transaction of ${amount:.2f} appears normal. Likely false positive - aligns with customer baseline. No action required."
        
    reasons = []
    if triggered_rules:
        reasons.append(f"triggered rules: {', '.join(triggered_rules)}")
        
    if shap_features:
        top_feature = shap_features[0]
        reasons.append(f"high contribution from {top_feature['feature']} ({top_feature['influence']} influence)")
        
    if behavior_score > 60:
        reasons.append("significant deviation from 30-day historical baseline")
        
    reason_str = " and ".join(reasons) if reasons else "anomalous patterns"
    
    if fraud_prob > 0.8 or behavior_score > 80:
        action = "Recommend hold + verify device and customer identity."
    elif fraud_prob > 0.5:
        action = "Suggest manual review of recent velocity."
    else:
        action = "Monitor for future anomalies."
    
    return f"Flagged due to {reason_str}. The model assigns a {(fraud_prob*100):.1f}% fraud probability. {action}"

def _call_real_llm_api(amount: float, fraud_prob: float, behavior_score: float, shap_features: List[Dict[str, Any]], triggered_rules: List[str]) -> str:
    """
    Calls OpenAI API to generate a narrative.
    Requires `openai` package and `OPENAI_API_KEY` env var.
    """
    try:
        import openai
        client = openai.OpenAI() # Automatically uses OPENAI_API_KEY
        
        prompt = f"Write a 2-sentence fraud analyst summary for a ${amount:.2f} transaction with {(fraud_prob*100):.1f}% fraud risk and behavior score {behavior_score}. Rules triggered: {triggered_rules}. Key SHAP features: {shap_features}. End with a clear recommended action (e.g., 'Recommend hold + verify device'). Be concise and professional."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return _mock_llm_generation(amount, fraud_prob, behavior_score, shap_features, triggered_rules)
