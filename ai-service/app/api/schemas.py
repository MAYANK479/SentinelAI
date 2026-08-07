from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class PredictRequest(BaseModel):
    customer_id: Optional[str] = Field(None, description="Unique identifier for the customer")
    Amount: float = Field(..., description="Transaction Amount in USD")
    MerchantCategoryRisk: float = Field(..., description="Risk score of the merchant category from 0.0 to 1.0")
    NightTime: int = Field(..., description="1 if transaction is during high-risk hours, 0 otherwise")
    Velocity: int = Field(..., description="Number of transactions by customer in the last hour")
    GeographicJump: int = Field(..., description="1 if distance from previous transaction is impossible, 0 otherwise")
    NewDevice: int = Field(..., description="1 if device is unrecognized, 0 otherwise")
    VPNUsed: int = Field(..., description="1 if customer is using a VPN/Proxy, 0 otherwise")
    SpendDeviation: float = Field(..., description="Ratio of amount to historical average transaction amount")
    FailedAttempts: int = Field(..., description="Number of consecutive failed PIN/CVV attempts prior to transaction")

class FeatureExplanation(BaseModel):
    feature: str
    value: float
    shap_value: float
    influence: str
    direction: str

class PredictResponse(BaseModel):
    ml_probability: float
    rule_score: float
    behavior_score: float
    composite_score: float
    risk_band: str
    is_fraud: int
    model_name: str
    explanations: List[FeatureExplanation]
    triggered_rules: List[str]
    narrative: str

class TrainRequest(BaseModel):
    pass # Currently retraining happens automatically on available dataset

class TrainResponse(BaseModel):
    status: str
    best_model: str
    num_train_samples: int
    metrics: Dict[str, Any]

class ModelInfoResponse(BaseModel):
    active_model: str
    features: List[str]
    num_train_samples: int
    training_date: Optional[str] = None

class MetricDetails(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    f2_score: float
    roc_auc: float
    pr_auc: float
    precision_at_100: float
    net_cost_saved: float

class MetricsResponse(BaseModel):
    models: Dict[str, MetricDetails]
