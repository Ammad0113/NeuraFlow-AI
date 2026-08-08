import streamlit as st
import pandas as pd
from frontend.api_client import APIClient

def render_scraping_view():
    st.markdown('<div class="nf-title">Web Scraping Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Scrape Product Catalog Data, News Headlines, HTML Tables, and Articles; Export to CSV, Excel, or JSON</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Target Scraper Configuration")
        url = st.text_input("Target URL", value="https://news.ycombinator.com")
        mode = st.selectbox("Scrape Targets", ["news", "product", "table", "generic"], format_func=lambda x: {
            "news": "News Headlines & Articles",
            "product": "Products & Prices",
            "table": "HTML Data Tables",
            "generic": "Links & Web Elements"
        }[x])
        max_items = st.slider("Maximum Items to Scrape", 5, 50, 15)

        if st.button("Launch Web Scraper", use_container_width=True):
            with st.spinner("Fetching target URL, parsing DOM structure, and extracting data..."):
                res = APIClient.post("/scraping/scrape", json={"url": url, "mode": mode, "max_items": max_items}, token=token)
                if res.status_code == 200:
                    st.session_state["scraped_result"] = res.json()
                    st.success("Web scrape completed!")
                else:
                    st.error("Failed to execute scrape job.")

    with col2:
        if "scraped_result" in st.session_state:
            result = st.session_state["scraped_result"]

            st.subheader(f"Results for: {result['title']}")
            st.caption(f"Target URL: {result['url']} | Extracted Items: {result['scraped_count']}")

            df = pd.DataFrame(result["data"])
            st.dataframe(df, use_container_width=True)

            st.markdown("### Export Scraped Data")
            c_exp1, c_exp2, c_exp3 = st.columns(3)
            
            if c_exp1.button("Export to CSV", use_container_width=True):
                res_exp = APIClient.post("/scraping/export?format_type=csv", json=result["data"], token=token)
                st.download_button("Download CSV", res_exp.content, "scraped_data.csv", "text/csv")

            if c_exp2.button("Export to Excel", use_container_width=True):
                res_exp = APIClient.post("/scraping/export?format_type=excel", json=result["data"], token=token)
                st.download_button("Download Excel", res_exp.content, "scraped_data.xlsx", "application/octet-stream")

            if c_exp3.button("Export to JSON", use_container_width=True):
                res_exp = APIClient.post("/scraping/export?format_type=json", json=result["data"], token=token)
                st.download_button("Download JSON", res_exp.content, "scraped_data.json", "application/json")
        else:
            st.caption("Configure target URL and click 'Launch Web Scraper' to inspect structured results here.")
