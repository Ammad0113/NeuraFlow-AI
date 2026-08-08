import streamlit as st
import os
from backend.config.settings import settings

def render_settings_view():
    st.markdown('<div class="nf-title">Settings & User Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Configure User Credentials, API Keys, Platform Preferences & Security Settings</div>', unsafe_allow_html=True)

    user = st.session_state.get("user", {})

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("User Profile Details")
        st.write(f"**Full Name:** {user.get('full_name', 'Enterprise Admin')}")
        st.write(f"**Work Email:** {user.get('email', 'demo@neuraflow.ai')}")
        st.write(f"**Role:** {user.get('role', 'Administrator')}")
        st.write(f"**Account Status:** Active")

    with col2:
        st.subheader("External LLM API Keys")
        st.caption("Provide a Groq API Key (`gsk_...`) or OpenAI API Key (`sk-...`) for ultra-fast, live generative AI responses across all topics.")
        
        groq_key = st.text_input("Groq API Key (Recommended)", type="password", placeholder="gsk_...", value=os.environ.get("GROQ_API_KEY", settings.GROQ_API_KEY or ""))
        openai_key = st.text_input("OpenAI API Key (Optional)", type="password", placeholder="sk-proj-...", value=os.environ.get("OPENAI_API_KEY", settings.OPENAI_API_KEY or ""))

        if st.button("Save API Configuration", use_container_width=True):
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key
                settings.GROQ_API_KEY = groq_key
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
                settings.OPENAI_API_KEY = openai_key
                
            st.success("API keys saved successfully.")
