import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="SentinelAI Fraud Intelligence", page_icon="🛡️", layout="wide")

st.title("🛡️ SentinelAI Fraud Intelligence Platform")
st.markdown("Enterprise-grade real-time transaction monitoring and explainable AI.")

tabs = st.tabs(["Live Monitoring", "Business Impact", "Rule & Behavior Engine"])

def fetch_metrics():
    try:
        response = requests.get(f"{API_URL}/metrics")
        return response.json().get("models", {})
    except Exception as e:
        return {}

def fetch_model_info():
    try:
        response = requests.get(f"{API_URL}/model-info")
        return response.json()
    except Exception as e:
        return {}

def fetch_drift_status():
    try:
        response = requests.get(f"{API_URL}/drift-check")
        return response.json()
    except Exception as e:
        return {}

def trigger_prediction(tx_data):
    try:
        response = requests.post(f"{API_URL}/predict", json=tx_data)
        return response.json()
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None

# Generate some mock live data by importing the synthetic generator from backend
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai-service", "app"))
try:
    from dataset.synthetic_augment import generate_synthetic_stream_batch
    HAVE_GENERATOR = True
except ImportError:
    HAVE_GENERATOR = False

with tabs[0]:
    st.header("Live Transaction Feed")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Generate & Process Transaction Batch"):
            if HAVE_GENERATOR:
                with st.spinner("Processing batch..."):
                    df = generate_synthetic_stream_batch(5)
                    results = []
                    for _, row in df.iterrows():
                        tx_data = {
                            "customer_id": row["customer_id"],
                            "Amount": row["Amount"],
                            "MerchantCategoryRisk": row["MerchantCategoryRisk"],
                            "NightTime": int(row["NightTime"]),
                            "Velocity": int(row["Velocity"]),
                            "GeographicJump": int(row["GeographicJump"]),
                            "NewDevice": int(row["NewDevice"]),
                            "VPNUsed": int(row["VPNUsed"]),
                            "SpendDeviation": row["SpendDeviation"],
                            "FailedAttempts": int(row["FailedAttempts"])
                        }
                        pred = trigger_prediction(tx_data)
                        if pred:
                            pred["Amount"] = tx_data["Amount"]
                            pred["customer_id"] = tx_data["customer_id"]
                            results.append(pred)
                    
                    if results:
                        for idx, res in enumerate(results):
                            risk_color = "red" if res["is_fraud"] else "orange" if res["risk_band"] == "Suspicious" else "green"
                            with st.expander(f"Tx #{idx+1} | {res['customer_id']} | Amount: ${res['Amount']:.2f} | Risk: {res['risk_band']} | Score: {res['composite_score']:.1f}"):
                                
                                st.markdown(f"**AI Narrative & Action Plan:** {res['narrative']}")
                                
                                subcol1, subcol2, subcol3 = st.columns(3)
                                subcol1.metric("ML Prob", f"{res['ml_probability']*100:.1f}%")
                                subcol2.metric("Rule Score", f"{res['rule_score']:.1f}")
                                subcol3.metric("Behavior Score", f"{res['behavior_score']:.1f}")
                                
                                st.write(f"**Triggered Rules:** {', '.join(res['triggered_rules']) if res['triggered_rules'] else 'None'}")
                                
                                # SHAP Waterfall visualization
                                shap_data = res.get("explanations", [])
                                if shap_data:
                                    shap_df = pd.DataFrame(shap_data)
                                    fig = go.Figure(go.Waterfall(
                                        name="SHAP", orientation="h",
                                        measure=["relative"] * len(shap_df),
                                        y=shap_df["feature"],
                                        x=shap_df["shap_value"],
                                        connector={"line":{"color":"rgb(63, 63, 63)"}},
                                    ))
                                    fig.update_layout(title="Feature Contributions (SHAP)", height=300)
                                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Generator not available. Ensure ai-service is in Python path.")

with tabs[1]:
    st.header("Business Impact & Model Health")
    if st.button("Refresh Metrics & Drift Status"):
        metrics = fetch_metrics()
        info = fetch_model_info()
        drift = fetch_drift_status()
        
        st.markdown("### 💰 ROI Statement")
        # Find best model to quote in ROI
        if metrics:
            best_model = info.get("active_model", list(metrics.keys())[0])
            best_m_data = metrics.get(best_model, {})
            cost_saved = best_m_data.get('net_cost_saved', 0)
            precision_top = best_m_data.get('precision_at_100', 0)
            st.success(f"**Reduced estimated fraud loss by ${cost_saved:,.2f}** while maintaining a **{(precision_top*100):.1f}% precision** on the top 100 flagged transactions.")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Model Performance")
            if info:
                st.info(f"Active Model: {info.get('active_model')} | Training Samples: {info.get('num_train_samples')} | Date: {info.get('training_date', 'N/A')}")
                
            if metrics:
                for m_name, m_data in metrics.items():
                    with st.expander(f"{m_name} Metrics", expanded=(m_name == info.get('active_model'))):
                        mcols = st.columns(3)
                        mcols[0].metric("PR-AUC", f"{m_data.get('pr_auc', 0):.4f}")
                        mcols[1].metric("F2-Score", f"{m_data.get('f2_score', 0):.4f}")
                        mcols[2].metric("Precision@100", f"{m_data.get('precision_at_100', 0):.4f}")
            else:
                st.warning("No metrics found. Try training the model first.")
                
        with col2:
            st.subheader("Model Drift Monitoring")
            if drift:
                d_status = drift.get("status", "Unknown")
                if d_status == "Healthy":
                    st.success(f"Status: {d_status} - {drift.get('message')}")
                elif d_status == "Warning":
                    st.warning(f"Status: {d_status} - {drift.get('message')}")
                else:
                    st.error(f"Status: {d_status} - {drift.get('message')}")
                    
                st.metric("Population Stability Index (PSI)", f"{drift.get('psi_score', 0):.4f}")
            else:
                st.info("Drift status unavailable.")

with tabs[2]:
    st.header("Rule & Behavior Engine Configuration")
    st.markdown("Phase 1: Configured to use a 3-part composite score blending ML, Heuristics, and Behavior.")
    
    st.subheader("Composite Scoring Formula")
    st.latex(r"Risk = (ML \times W_{ml}) + (Rules \times W_{rule}) + (Behavior \times W_{behavior})")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.slider("W_ml (ML Model Weight)", 0.0, 1.0, 0.5, 0.1, disabled=True)
    with col2:
        st.slider("W_rule (Heuristic Rule Weight)", 0.0, 1.0, 0.3, 0.1, disabled=True)
    with col3:
        st.slider("W_behavior (Behavior Baseline Weight)", 0.0, 1.0, 0.2, 0.1, disabled=True)
        
    st.markdown("---")
    st.subheader("Active Heuristic Rules")
    st.json([
        {"name": "High Amount", "weight": 30},
        {"name": "Extreme Velocity", "weight": 40},
        {"name": "Geographic Jump", "weight": 50},
        {"name": "New Device + High Value", "weight": 45},
        {"name": "VPN Used", "weight": 20},
        {"name": "High Spend Deviation", "weight": 35},
        {"name": "Multiple Failed Attempts", "weight": 50},
    ])
