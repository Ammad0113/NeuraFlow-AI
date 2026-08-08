import streamlit as st
from frontend.api_client import APIClient

def render_assistant_view():
    st.markdown('<div class="nf-title">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="nf-subtitle">Conversational AI Engine for Coding, Business Writing, Document Summarization & Strategy</div>', unsafe_allow_html=True)

    token = st.session_state.get("token")

    col1, col2 = st.columns([7, 3])

    with col2:
        st.subheader("Assistant Specialty")
        mode = st.selectbox(
            "Select AI Mode",
            ["general", "code", "email", "summary", "report", "brainstorm"],
            format_func=lambda x: {
                "general": "General Q&A",
                "code": "Code Generation & Review",
                "email": "Business Email Writer",
                "summary": "Executive Summarizer",
                "report": "Strategy Report Writer",
                "brainstorm": "Product Brainstorming"
            }[x]
        )

        st.caption("Active Specialty Focus:")
        descriptions = {
            "general": "Enterprise assistant with broad technical & business domain knowledge.",
            "code": "Writes clean, type-annotated, high-performance Python / Full-stack code.",
            "email": "Crafts professional executive emails and stakeholder communications.",
            "summary": "Extracts key takeaways and structured summaries from dense topics.",
            "report": "Generates structured multi-section strategic reports.",
            "brainstorm": "Produces strategic product concepts and technical solutions."
        }
        st.info(descriptions[mode])

    with col1:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hello! I am your AI Assistant. How can I accelerate your workflow today?"}
            ]

        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

        prompt = st.chat_input("Ask a question, request code, or summarize a topic...")
        if prompt:
            st.session_state["messages"].append({"role": "user", "content": prompt})
            st.rerun()

    if len(st.session_state["messages"]) > 0 and st.session_state["messages"][-1]["role"] == "user":
        latest_prompt = st.session_state["messages"][-1]["content"]
        with st.spinner("Processing request..."):
            res = APIClient.post("/assistant/chat", json={"prompt": latest_prompt, "mode": mode}, token=token)
            if res.status_code == 200:
                answer = res.json()["assistant_response"]
            else:
                answer = "Unable to process assistant request. Please check API server connection."
            
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.rerun()
