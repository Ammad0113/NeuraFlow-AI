import streamlit as st

def render_kpi_card(title: str, value: str, subtitle: str = "", badge: str = "Active"):
    st.markdown(f"""
    <div class="nf-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 1.15rem; font-weight: 700; color: #F1F5F9;">{title}</span>
            <span class="kpi-badge">{badge}</span>
        </div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg, #F8FAFC, #A5B4FC, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem;">
            {value}
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; font-weight: 500;">
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)
