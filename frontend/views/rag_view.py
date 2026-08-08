import streamlit as st
from frontend.api_client import APIClient

def render_rag_view():
    st.markdown('<div class="nf-title">RAG Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Upload Enterprise Documents (PDF, DOCX, TXT), Index Embeddings, and Perform Grounded Semantic Retrieval</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("1. Document Ingestion")
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
        
        if uploaded_file and st.button("Parse & Index Document", use_container_width=True):
            with st.spinner("Parsing, chunking, and indexing document vectors..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                res = APIClient.post("/rag/upload", files=files, token=token)
                if res.status_code == 200:
                    st.success(f"Successfully indexed '{uploaded_file.name}' into vector knowledge base!")
                    st.rerun()
                else:
                    st.error("Failed to ingest document.")

        st.markdown("---")
        st.subheader("Indexed Documents")
        res_docs = APIClient.get("/rag/documents", token=token)
        docs = res_docs.json() if res_docs.status_code == 200 else []
        
        if docs:
            for d in docs:
                st.markdown(f"**{d['filename']}** ({d['chunks_count']} chunks)")
        else:
            st.caption("No documents indexed yet. Upload a document above.")

    with col2:
        st.subheader("2. Grounded Q&A Search")
        query = st.text_input("Ask a question grounded in your uploaded knowledge base documents...")
        top_k = st.slider("Max Search Citations (Top-K)", min_value=1, max_value=5, value=3)

        if st.button("Search Knowledge Base", use_container_width=True) and query:
            with st.spinner("Searching vector index for semantic context..."):
                res_q = APIClient.post("/rag/query", json={"query": query, "top_k": top_k}, token=token)
                if res_q.status_code == 200:
                    data = res_q.json()
                    st.markdown("### Grounded Answer")
                    st.info(data["answer"])

                    st.markdown("### Source Citations & Snippets")
                    if data["citations"]:
                        for idx, c in enumerate(data["citations"], 1):
                            with st.expander(f"Citation #{idx}: {c['filename']} (Relevance Score: {c['score']})"):
                                st.markdown(f"**Chunk {c['chunk_index']}:**")
                                st.code(c["snippet"], language="text")
                    else:
                        st.caption("No matching citation chunks found.")
                else:
                    st.error("Failed to execute RAG query.")
