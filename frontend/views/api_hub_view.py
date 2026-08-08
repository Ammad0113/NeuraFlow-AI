import streamlit as st
import json
from frontend.api_client import APIClient

def render_api_hub_view():
    st.markdown('<div class="nf-title">API Integration Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Pre-built Enterprise Integrations & REST API Testing Console</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    tab1, tab2, tab3, tab4 = st.tabs(["Weather API", "Currency Exchange", "GitHub API", "REST API Console"])

    with tab1:
        st.subheader("Global Live Weather API")
        city = st.text_input("City Name", value="San Francisco")
        if st.button("Fetch Live Weather", key="btn_w"):
            res = APIClient.get(f"/api-hub/weather?city={city}", token=token)
            if res.status_code == 200:
                w = res.json()
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("City", w["city"])
                c2.metric("Temperature", f"{w['temp_C']}°C / {w['temp_F']}°F")
                c3.metric("Condition", w["condition"])
                c4.metric("Humidity", f"{w['humidity']}%")

    with tab2:
        st.subheader("Real-Time Currency Exchange API")
        base = st.selectbox("Base Currency", ["USD", "EUR", "GBP", "CAD", "AUD"])
        if st.button("Fetch Exchange Rates", key="btn_c"):
            res = APIClient.get(f"/api-hub/currency?base={base}", token=token)
            if res.status_code == 200:
                c_data = res.json()
                st.caption(f"Last updated: {c_data['date']}")
                st.json(c_data["rates"])

    with tab3:
        st.subheader("GitHub Repository Intelligence")
        col_g1, col_g2 = st.columns(2)
        owner = col_g1.text_input("Owner", value="fastapi")
        repo = col_g2.text_input("Repository", value="fastapi")
        
        if st.button("Inspect GitHub Repo", key="btn_gh"):
            res = APIClient.get(f"/api-hub/github?owner={owner}&repo={repo}", token=token)
            if res.status_code == 200:
                gh = res.json()
                c1, c2, c3 = st.columns(3)
                c1.metric("Stars", f"{gh['stars']:,}")
                c2.metric("Forks", f"{gh['forks']:,}")
                c3.metric("Open Issues", gh["open_issues"])
                st.write(f"**Description:** {gh['description']}")
                st.caption(f"Language: {gh['language']} | License: {gh['license']}")

    with tab4:
        st.subheader("Generic REST API Tester Console")
        method = st.radio("HTTP Method", ["GET", "POST"], horizontal=True)
        url_input = st.text_input("Endpoint URL", value="https://jsonplaceholder.typicode.com/todos/1")
        
        body_input = None
        if method == "POST":
            body_text = st.text_area("JSON Body", value='{"title": "NeuraFlow Task", "completed": false}')
            try:
                body_input = json.loads(body_text)
            except Exception:
                pass

        if st.button("Execute REST Request", key="btn_exec"):
            res = APIClient.post("/api-hub/execute", json={
                "url": url_input, "method": method, "body": body_input
            }, token=token)
            if res.status_code == 200:
                resp_json = res.json()
                st.markdown(f"**Status Code:** `{resp_json.get('status_code', 200)}`")
                st.json(resp_json.get("data", {}))
