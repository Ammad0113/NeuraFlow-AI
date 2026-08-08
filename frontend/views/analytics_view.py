import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.api_client import APIClient
from frontend.components.kpi_card import render_kpi_card

def render_analytics_view():
    st.markdown('<div class="nf-title">Enterprise Data Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Platform KPI Performance, Automated Task Tracking, AI Model Statistics & Usage Metrics</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    res = APIClient.get("/analytics/dashboard", token=token)
    data = res.json() if res.status_code == 200 else {
        "kpi": {"conversations": 12, "documents_indexed": 8, "models_trained": 4, "automations_run": 84, "reports_generated": 15, "system_health": "99.99%"},
        "recent_activity": [],
        "usage_trends": {"months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"], "automations": [10, 25, 40, 60, 85, 110, 140, 160], "ai_queries": [50, 100, 160, 240, 350, 500, 650, 800]}
    }

    kpi = data["kpi"]

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Python Automations", f"{kpi['automations_run']:,}", "Executed Workflows", "Active")
    with col2:
        render_kpi_card("RAG Knowledge Base", f"{kpi['documents_indexed']} Docs", "Vector Embeddings", "Indexed")
    with col3:
        render_kpi_card("ML Models Trained", f"{kpi['models_trained']} Models", "Deployed Algorithms", "Verified")

    st.markdown("<br/>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Automation & AI Usage Growth")
        df_trends = pd.DataFrame({
            "Month": data["usage_trends"]["months"],
            "Automations Executed": data["usage_trends"]["automations"],
            "AI Queries": data["usage_trends"]["ai_queries"]
        })
        fig = px.line(df_trends, x="Month", y=["Automations Executed", "AI Queries"], markers=True, template="plotly_dark", title="Monthly Activity Volume")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Recent System Automations Log")
        if data["recent_activity"]:
            for item in data["recent_activity"]:
                st.markdown(f"• **{item['task']}**: <span style='color:#34D399;'>{item['status']}</span> — {item['summary']}", unsafe_allow_html=True)
        else:
            st.caption("No recent automation logs.")
