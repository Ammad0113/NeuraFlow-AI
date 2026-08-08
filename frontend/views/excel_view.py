import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.api_client import APIClient

def render_excel_view():
    st.markdown('<div class="nf-title">Excel Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Automated Data Cleaning, Duplicate Removal, Statistical Analysis, Insights & Interactive Visualizations</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    uploaded_file = st.file_uploader("Upload Excel or CSV Dataset", type=["csv", "xlsx"])

    if uploaded_file:
        if st.button("Inspect Dataset Structure", use_container_width=True):
            with st.spinner("Analyzing dataset rows, columns, duplicates, and statistics..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
                res = APIClient.post("/excel/inspect", files=files, token=token)
                
                if res.status_code == 200:
                    st.session_state["excel_info"] = res.json()

    if "excel_info" in st.session_state:
        info = st.session_state["excel_info"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", f"{info['rows']:,}")
        col2.metric("Columns", info["columns"])
        col3.metric("Duplicates", info["duplicates_count"])

        st.subheader("Dataset Insights")
        for ins in info["ai_insights"]:
            st.info(f"• {ins}")

        if info.get("preview_data"):
            df_preview = pd.DataFrame(info["preview_data"])
            st.subheader("Interactive Data Preview & Visualization")
            st.dataframe(df_preview, use_container_width=True)

            num_cols = df_preview.select_dtypes(include=['number']).columns.tolist()
            if len(num_cols) >= 1:
                selected_col = st.selectbox("Select Numeric Column to Plot Distribution", num_cols)
                fig = px.histogram(df_preview, x=selected_col, title=f"Distribution of {selected_col}", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Automated Cleaning & Export")
        c1, c2 = st.columns(2)
        rem_dup = c1.checkbox("Purge Duplicate Rows", value=True)
        fill_num = c2.selectbox("Fill Missing Quantitative Values", ["mean", "median", "zero"])

        if st.button("Execute Data Cleaning & Download Clean File", use_container_width=True) and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
            data = {"remove_duplicates": rem_dup, "fill_missing_numeric": fill_num}
            res_clean = APIClient.post("/excel/clean", files=files, data=data, token=token)
            
            if res_clean.status_code == 200:
                st.download_button(
                    label="Save Clean Dataset",
                    data=res_clean.content,
                    file_name=f"cleaned_{uploaded_file.name}",
                    mime="application/octet-stream",
                    use_container_width=True
                )
                st.success("Dataset successfully cleaned!")
            else:
                st.error("Failed to clean dataset.")
