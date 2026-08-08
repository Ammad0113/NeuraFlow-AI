import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 0.5rem 0; text-align: center;">
            <h2 style="margin:0; font-family:'Outfit', sans-serif; background: linear-gradient(90deg, #6366F1, #38BDF8, #A855F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:800; font-size:1.7rem;">NeuraFlow AI</h2>
            <p style="font-size:0.75rem; color:#94A3B8; margin-top:0.3rem; font-weight:500; letter-spacing:0.05em; text-transform:uppercase;">Enterprise AI Platform</p>
        </div>
        <hr style="border-color: rgba(255,255,255,0.08); margin: 0.5rem 0 1rem 0;" />
        """, unsafe_allow_html=True)

        if "user" in st.session_state and st.session_state["user"]:
            u = st.session_state["user"]
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.06); padding: 0.8rem; border-radius: 12px; margin-bottom: 1rem;">
                <div style="font-size:0.85rem; font-weight:700; color:#F8FAFC;">User: {u.get('full_name', 'Admin')}</div>
                <div style="font-size:0.72rem; color:#818CF8;">Role: {u.get('role', 'Administrator')}</div>
            </div>
            """, unsafe_allow_html=True)

        modules = {
            "Analytics Dashboard": "analytics",
            "AI Assistant": "assistant",
            "RAG Knowledge Base": "rag",
            "PDF Intelligence": "pdf",
            "Excel Intelligence": "excel",
            "Python Automation": "automation",
            "Web Scraping Studio": "scraping",
            "API Integration Hub": "api_hub",
            "ML Workspace": "ml",
            "Report Generator": "reports",
            "Settings & Profile": "settings"
        }

        selected_label = st.radio(
            "Platform Navigation",
            list(modules.keys()),
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 1rem 0;' />", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state["token"] = None
            st.session_state["user"] = None
            st.rerun()

        return modules[selected_label]
