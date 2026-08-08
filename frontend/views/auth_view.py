import streamlit as st
from frontend.api_client import APIClient

def render_auth_view():
    st.markdown("""
    <div style="text-align: center; max-width: 580px; margin: 3rem auto 1.5rem auto;">
        <div style="display:inline-block; padding: 0.5rem 1.2rem; background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2)); border: 1px solid rgba(129,140,248,0.3); border-radius: 9999px; margin-bottom: 1rem; box-shadow: 0 0 20px rgba(99,102,241,0.3);">
            <span style="font-size:0.85rem; font-weight:700; color:#A5B4FC; letter-spacing:0.05em; text-transform:uppercase;">Enterprise AI & Automation Platform</span>
        </div>
        <h1 style="font-family:'Outfit', sans-serif; font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 40%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">NeuraFlow AI</h1>
        <p style="color: #94A3B8; font-size: 1.1rem;">Next-Generation Business Intelligence, RAG Vector Search & ML Automation Platform</p>
    </div>
    """, unsafe_allow_html=True)

    c_center = st.columns([1, 2, 1])[1]

    with c_center:
        tab1, tab2, tab3 = st.tabs(["Sign In", "Create Account", "Reset Password"])

        with tab1:
            st.subheader("Sign In")
            email = st.text_input("Work Email", value="demo@neuraflow.ai", key="login_email")
            password = st.text_input("Password", value="demo123456", type="password", key="login_pass")
            
            if st.button("Authenticate", use_container_width=True, key="btn_login"):
                res = APIClient.post("/auth/login", json={"email": email, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state["token"] = data["access_token"]
                    st.session_state["user"] = data["user"]
                    st.success("Successfully authenticated!")
                    st.rerun()
                else:
                    st.error("Authentication failed. Please check your credentials.")

        with tab2:
            st.subheader("Register Account")
            full_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Work Email", key="reg_email")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Create Account", use_container_width=True, key="btn_reg"):
                if not full_name or not reg_email or not reg_pass:
                    st.warning("Please fill in all fields.")
                else:
                    res = APIClient.post("/auth/signup", json={"full_name": full_name, "email": reg_email, "password": reg_pass})
                    if res.status_code == 200:
                        st.success("Account created! Please sign in using your credentials.")
                    else:
                        st.error(res.json().get("detail", "Registration failed."))

        with tab3:
            st.subheader("Reset Password")
            reset_email = st.text_input("Registered Email", key="rst_email")
            new_pass = st.text_input("New Password", type="password", key="rst_pass")
            
            if st.button("Reset Password", use_container_width=True, key="btn_rst"):
                res = APIClient.post("/auth/forgot-password", json={"email": reset_email, "new_password": new_pass})
                if res.status_code == 200:
                    st.success("Password reset successfully!")
                else:
                    st.error(res.json().get("detail", "Password reset failed."))
