import streamlit as st
import os

st.set_page_config(
    page_title="NeuraFlow AI | Enterprise AI Automation Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None

from frontend.views.auth_view import render_auth_view
from frontend.views.analytics_view import render_analytics_view
from frontend.views.assistant_view import render_assistant_view
from frontend.views.rag_view import render_rag_view
from frontend.views.pdf_view import render_pdf_view
from frontend.views.excel_view import render_excel_view
from frontend.views.automation_view import render_automation_view
from frontend.views.scraping_view import render_scraping_view
from frontend.views.api_hub_view import render_api_hub_view
from frontend.views.ml_view import render_ml_view
from frontend.views.reports_view import render_reports_view
from frontend.views.settings_view import render_settings_view
from frontend.components.sidebar import render_sidebar

# Auth Check Routing
if not st.session_state["token"]:
    render_auth_view()
else:
    active_view = render_sidebar()

    if active_view == "analytics":
        render_analytics_view()
    elif active_view == "assistant":
        render_assistant_view()
    elif active_view == "rag":
        render_rag_view()
    elif active_view == "pdf":
        render_pdf_view()
    elif active_view == "excel":
        render_excel_view()
    elif active_view == "automation":
        render_automation_view()
    elif active_view == "scraping":
        render_scraping_view()
    elif active_view == "api_hub":
        render_api_hub_view()
    elif active_view == "ml":
        render_ml_view()
    elif active_view == "reports":
        render_reports_view()
    elif active_view == "settings":
        render_settings_view()
