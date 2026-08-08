import streamlit as st
import pandas as pd
import plotly.express as px
import json
from frontend.api_client import APIClient

def render_ml_view():
    st.markdown('<div class="nf-title">Machine Learning Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Train Classification & Regression Models (Scikit-Learn), Evaluate Performance Metrics, Feature Importance & Run Predictions</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    tab1, tab2, tab3 = st.tabs(["Train New Model", "Deployed Models", "Run Predictions"])

    with tab1:
        st.subheader("1. Model Configuration & Dataset Upload")

        uploaded_df = st.file_uploader("Upload Training Dataset (CSV / XLSX)", type=["csv", "xlsx"])

        if uploaded_df:
            if uploaded_df.name.endswith(".csv"):
                df_preview = pd.read_csv(uploaded_df)
            else:
                df_preview = pd.read_excel(uploaded_df)

            st.dataframe(df_preview.head(5), use_container_width=True)

            cols = list(df_preview.columns)
            target_col = st.selectbox("Target Column (Label to predict)", cols)

            c_task, c_algo = st.columns(2)
            task_type = c_task.selectbox("ML Task Type", ["classification", "regression"])

            algo_options = {
                "classification": ["random_forest", "logistic_regression", "decision_tree", "gradient_boosting"],
                "regression": ["random_forest", "linear_regression", "decision_tree", "gradient_boosting"]
            }

            algorithm = c_algo.selectbox("Algorithm Strategy", algo_options[task_type])
            test_size = st.slider("Validation Split Size (Test %)", 0.1, 0.4, 0.2)

            if st.button("Train Enterprise ML Model", use_container_width=True):
                with st.spinner("Training model, tuning hyperparameters, and computing evaluation metrics..."):
                    files = {"file": (uploaded_df.name, uploaded_df.getvalue(), "application/octet-stream")}
                    data = {
                        "target_column": target_col,
                        "task_type": task_type,
                        "algorithm": algorithm,
                        "test_size": test_size
                    }
                    res = APIClient.post("/ml/train", files=files, data=data, token=token)

                    if res.status_code == 200:
                        train_res = res.json()
                        st.session_state["last_trained_model"] = train_res
                        st.success(f"Successfully trained {train_res['model_name']}!")
                    else:
                        st.error("Failed to train model.")

        if "last_trained_model" in st.session_state:
            m = st.session_state["last_trained_model"]
            st.subheader(f"Evaluation Results: {m['model_name']}")

            metrics = m["metrics"]
            m_cols = st.columns(len(metrics))
            for i, (k, v) in enumerate(metrics.items()):
                m_cols[i].metric(k.upper().replace("_", " "), v)

            if m.get("feature_importance"):
                st.markdown("### Feature Importance")
                fi_df = pd.DataFrame(list(m["feature_importance"].items()), columns=["Feature", "Importance"]).sort_values(by="Importance", ascending=False)
                fig = px.bar(fi_df, x="Importance", y="Feature", orientation="h", title="Feature Impact Ranking", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Deployed Models Registry")
        res_models = APIClient.get("/ml/models", token=token)
        models = res_models.json() if res_models.status_code == 200 else []

        if models:
            for mod in models:
                st.markdown(f"**Model ID #{mod['id']}**: `{mod['name']}` ({mod['algorithm']}) | Score: `{mod['accuracy_or_r2']}`")
                st.caption(f"Created: {mod['created_at'][:19]}")
                st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:0.4rem 0;' />", unsafe_allow_html=True)
        else:
            st.caption("No models trained yet. Train a model in Tab 1.")

    with tab3:
        st.subheader("Live Inference Predictor")
        model_id = st.number_input("Trained Model ID", min_value=1, value=1)
        input_json_str = st.text_area("Input Feature JSON Payload", value='{"feature1": 25.5, "feature2": 102.0, "category": "Tech"}')

        if st.button("Run Prediction Inference", use_container_width=True):
            try:
                input_data = json.loads(input_json_str)
                res_p = APIClient.post("/ml/predict", json={"model_id": model_id, "input_data": input_data}, token=token)
                if res_p.status_code == 200:
                    st.success(f"Prediction Output: {res_p.json()['prediction']}")
                else:
                    st.error("Prediction failed. Ensure feature names match training dataset.")
            except Exception as e:
                st.error(f"Invalid JSON payload: {e}")
