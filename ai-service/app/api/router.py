from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.api.schemas import (
    PredictRequest, PredictResponse, TrainResponse, 
    ModelInfoResponse, MetricsResponse
)
from app.models.trainer import get_loaded_model, train_and_evaluate_models
from app.models.explainability import explain_prediction
from app.models.narrative import generate_case_narrative
from app.rules.engine import evaluate_rules
from app.rules.composite import calculate_composite_score
from app.rules.behavior import calculate_behavior_score
from app.models.drift import check_model_drift
from app.db import get_db_connection

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    model, metadata = get_loaded_model()
    
    input_data = request.model_dump()
    features = metadata["features"]
    
    # Ensure missing features (if any are expected by model) are filled with 0
    model_input = {f: input_data.get(f, 0.0) for f in features}
    
    import pandas as pd
    df = pd.DataFrame([model_input])
    
    # ML Prediction
    fraud_probability = float(model.predict_proba(df)[0][1]) if hasattr(model, "predict_proba") else float(model.predict(df)[0])
    
    # Rules Evaluation
    rule_score, triggered_rules = evaluate_rules(input_data)
    
    # Behavioral Evaluation
    behavior_score = calculate_behavior_score(input_data)
    
    # Composite Score
    composite_result = calculate_composite_score(fraud_probability, rule_score, behavior_score)
    final_score = composite_result["composite_score"]
    risk_band = composite_result["risk_band"]
    is_fraud = 1 if final_score > 80 else 0 # 80 is the threshold for Fraud band
    
    # Explainability (SHAP)
    explanations = explain_prediction(model, features, model_input)
    
    # Narrative Generation
    narrative = generate_case_narrative(
        amount=input_data.get("Amount", 0),
        fraud_prob=fraud_probability,
        behavior_score=behavior_score,
        shap_features=explanations,
        triggered_rules=triggered_rules,
        use_mock=True # MVP defaults to mock
    )
    
    return PredictResponse(
        ml_probability=fraud_probability,
        rule_score=rule_score,
        behavior_score=behavior_score,
        composite_score=final_score,
        risk_band=risk_band,
        is_fraud=is_fraud,
        model_name=metadata["best_model"],
        explanations=explanations,
        triggered_rules=triggered_rules,
        narrative=narrative
    )

@router.post("/train", response_model=TrainResponse)
def train():
    metadata = train_and_evaluate_models()
    return TrainResponse(
        status="Model trained successfully",
        best_model=metadata["best_model"],
        num_train_samples=metadata["num_train_samples"],
        metrics=metadata["metrics"]
    )

@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_info():
    _, metadata = get_loaded_model()
    return ModelInfoResponse(
        active_model=metadata["best_model"],
        features=metadata["features"],
        num_train_samples=metadata["num_train_samples"],
        training_date=metadata.get("training_date")
    )

@router.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    _, metadata = get_loaded_model()
    return MetricsResponse(models=metadata["metrics"])

@router.get("/drift-check")
def check_drift():
    # Fetch recent predictions from SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ml_probability FROM transactions ORDER BY timestamp DESC LIMIT 1000")
        rows = cursor.fetchall()
        conn.close()
        
        recent_preds = [row["ml_probability"] for row in rows]
        
        if len(recent_preds) < 50:
            return {
                "status": "Pending",
                "drift_detected": False,
                "psi_score": 0.0,
                "message": "Not enough data points yet. Need at least 50 transactions."
            }
            
        drift_result = check_model_drift(recent_preds)
        return drift_result
        
    except Exception as e:
        return {
            "status": "Error",
            "drift_detected": False,
            "psi_score": 0.0,
            "message": f"Failed to check drift: {e}"
        }
