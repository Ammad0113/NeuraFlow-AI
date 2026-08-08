import streamlit as st
from frontend.api_client import APIClient

def render_reports_view():
    st.markdown('<div class="nf-title">Report Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Generate Custom PDF, Markdown & CSV Business Reports with Styled Branding & Tables</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Generate New Report")
        title = st.text_input("Report Title", value="Q3 AI Automation & Operational Intelligence Report")
        report_type = st.selectbox("Output Format", ["PDF", "Markdown", "CSV"])
        template = st.selectbox("Report Template", ["executive", "technical", "financial", "analytics"])
        custom_notes = st.text_area("Executive Notes / Recommendations (Optional)", value="System metrics show 99.8% compliance rate across all automated workflows.")

        if st.button("Generate & Download Report", use_container_width=True):
            with st.spinner("Compiling metrics, rendering tables, and generating document..."):
                res = APIClient.post("/reports/generate", json={
                    "title": title,
                    "report_type": report_type,
                    "template": template,
                    "custom_notes": custom_notes
                }, token=token)

                if res.status_code == 200:
                    ext = report_type.lower()
                    if ext == "markdown":
                        ext = "md"
                    filename = f"{title.lower().replace(' ', '_')}.{ext}"

                    st.download_button(
                        label=f"Download {report_type} Document",
                        data=res.content,
                        file_name=filename,
                        mime="application/pdf" if report_type == "PDF" else "text/plain",
                        use_container_width=True
                    )
                    st.success("Report successfully generated!")
                else:
                    st.error("Failed to generate report.")

    with col2:
        st.subheader("Report History Audit Trail")
        res_h = APIClient.get("/reports/history", token=token)
        reports = res_h.json() if res_h.status_code == 200 else []

        if reports:
            for r in reports:
                st.markdown(f"**{r['title']}** (`{r['report_type']}`) — {r['created_at'][:10]}")
                st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:0.4rem 0;' />", unsafe_allow_html=True)
        else:
            st.caption("No reports generated yet.")
