import streamlit as st
from frontend.api_client import APIClient

def render_pdf_view():
    st.markdown('<div class="nf-title">PDF Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Extract Text, Executive Summaries, Key Terms, and Risk Clauses from Contracts & PDF Documents</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    uploaded_pdf = st.file_uploader("Upload PDF Document for Intelligence Analysis", type=["pdf"])

    if uploaded_pdf and st.button("Run PDF Deep Analysis", use_container_width=True):
        with st.spinner("Analyzing PDF pages, keywords, and compliance risks..."):
            files = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
            res = APIClient.post("/pdf/analyze", files=files, token=token)
            
            if res.status_code == 200:
                data = res.json()

                col1, col2, col3 = st.columns(3)
                col1.metric("Filename", data["filename"])
                col2.metric("Total Pages", data["total_pages"])
                col3.metric("Word Count", f"{data['word_count']:,}")

                st.subheader("Executive Summary")
                st.write(data["executive_summary"])

                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("Key Terms & Topics")
                    for kw in data["keywords"]:
                        st.markdown(f"- **{kw}**")

                with col_b:
                    st.subheader("Risk & Compliance Clauses")
                    for rk in data["identified_risks"]:
                        st.warning(f"• {rk}")

                with st.expander("Preview Raw Extracted Text"):
                    st.text(data["sample_text"])
            else:
                st.error("Failed to perform PDF analysis.")
