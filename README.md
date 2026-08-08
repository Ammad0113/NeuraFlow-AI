# ⚡ NeuraFlow AI — Enterprise AI & Automation Platform

> **Full-Stack Enterprise AI Platform & Data Science Intelligence Suite**  
> **Authored by:** Ammad Qaiser — Lead Systems Architect & Senior Full-Stack Engineer  
> **Release Version:** `v1.0.0 Enterprise Production`  
> **Security Standard:** `HMAC-SHA256 JWT Bearer Authentication`

---

## 🌟 Executive Summary

**NeuraFlow AI** is a state-of-the-art enterprise automation and artificial intelligence platform designed to eliminate manual workflow bottlenecks across document parsing, data intelligence, vector search, background task execution, and predictive machine learning.

Engineered with a decoupled microservices architecture, NeuraFlow combines an asynchronous **FastAPI REST Backend Engine** with an interactive **Streamlit Web Console** styled with dark-mode glassmorphic aesthetics. The platform integrates **Groq LLaMA 3.3 70B** for sub-150ms generative AI completions alongside local enterprise knowledge bases for grounded semantic retrieval.

---

## 🚀 Key Modules & Capabilities

### 1. 🤖 AI Assistant Engine
- **Groq LLaMA 3.3 70B Integration**: Sub-150ms streaming response latency across all topics.
- **6 Specialty Execution Modes**:
  - `Code Mode`: Production-ready, type-annotated Python/Full-Stack code.
  - `Executive Email Mode`: Professional stakeholder communications & proposals.
  - `Executive Summary Mode`: Bulleted key takeaways and structured summaries.
  - `Report Mode`: Multi-section strategic markdown business reports.
  - `Brainstorm Mode`: Strategic product concepts and innovation roadmaps.
  - `General Q&A Mode`: Broad domain knowledge and enterprise reasoning.

### 2. 📚 RAG Knowledge Base (Vector Semantic Search)
- **Document Ingestion**: Ingests PDF, DOCX, and TXT documents.
- **Overlapping Vector Chunking**: 500-word text chunking with TF-IDF vectorization and cosine similarity.
- **Overview Meta-Query Synthesizer**: Answers broad meta-questions (*"What is this PDF about?"*) using Groq LLaMA 3.3 grounded synthesis with exact source citations.
- **Sanitized PDF Text Parser**: Filters raw PDF binary headers (`%PDF-1.4`, `/ASCII85Decode`) to ensure clean human citations.

### 3. 📄 PDF Legal & Contract Intelligence
- Extracts executive summaries, word volume, and page metrics.
- **Risk & Compliance Clause Extractor**: Scans contracts for liability caps, indemnification, penalty triggers, confidentiality, and termination rights.

### 4. 📊 Excel Data Cleaning Engine
- **Automated Cleaning**: Purges duplicate rows and imputes missing numeric values (Mean, Median, Zero).
- **NaN Serialization Guards**: Safe JSON output formatting handling pandas `NaN` values.
- **Interactive Visualizations**: Generates Plotly dark-theme histograms and descriptive statistical summaries.

### 5. ⚡ Python Automation Center
- **Folder Categorizer**: Sorts cluttered directories into subfolders (Documents, Images, Spreadsheets, Archives, Code).
- **Batch File Renamer**: Sequential prefix renaming with dot-flexible, case-insensitive extension matching (`PNG`, `png`, `.png`).
- **Non-Strict PDF Merger/Splitter**: Merges and splits multi-page PDFs without stream corruption errors.

### 6. 🌐 Web Scraping Studio
- BeautifulSoup4 parser for product catalogs, news headlines, and HTML tables.
- Exports scraped web data directly to **CSV**, **Excel (.xlsx)**, or **JSON**.

### 7. 🧠 Scikit-Learn Machine Learning Workspace
- Trains Classification & Regression models (Random Forest, Decision Trees, Gradient Boosting, Linear Models).
- Evaluates Accuracy, F1-Score, R², and MSE metrics across test validation splits.
- Displays interactive feature importance ranking bar charts and runs real-time JSON prediction inference.

### 8. 🔗 API Integration Hub & 📈 Report Generator
- Real-time third-party API integrations (Weather, Currency Exchange, GitHub Repo Intelligence).
- Generates styled PDF, Markdown, and CSV business reports with custom executive audit logs.

---

## 🛠️ Technology Stack Specification

| Architectural Layer | Framework / Technology | Engineering Role |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit, Custom CSS, Plotly Express | Dark-mode glassmorphism console, interactive charts, live chat streams. |
| **Backend REST API** | FastAPI, Uvicorn ASGI, Pydantic v2 | Asynchronous routes, OpenAPI Swagger docs, JWT authorization middleware. |
| **Persistence & ORM** | SQLite, SQLAlchemy ORM | 7 relational entities (Users, Conversations, Vectors, ML Models, Audit Logs). |
| **Generative AI & RAG** | Groq LLaMA 3.3 70B, Scikit-Learn TF-IDF | Sub-150ms inference, overlapping chunk vector search, source citations. |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy | Multi-threaded model training, feature importance, live prediction runner. |
| **Document Processing** | PyPDF2, pypdf, ReportLab, BeautifulSoup4 | Non-strict PDF parsing, risk clause auditing, web scraping, PDF compilation. |

---

## 💻 Installation & Local Setup

### Prerequisites
- Python 3.10+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/Ammad0113/NeuraFlow-AI.git
cd NeuraFlow-AI
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Configure Environment (.env)
Create a `.env` file in the root directory:
```env
PROJECT_NAME="NeuraFlow AI"
SECRET_KEY="neuraflow-super-secret-jwt-key"
GROQ_API_KEY="your_groq_api_key_here"
GROQ_API_BASE="https://api.groq.com/openai/v1"
GROQ_MODEL="llama-3.3-70b-versatile"
```

### 4. Run Services

**Start Backend Server (Port 8008):**
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8008 --reload
```

**Start Frontend Application (Port 8501):**
```bash
python -m streamlit run frontend/app.py --server.port 8501 --server.address 127.0.0.1
```

### 5. Access Credentials
- **Streamlit Web UI**: `http://localhost:8501`
- **FastAPI Swagger Docs**: `http://localhost:8008/docs`
- **Demo User**: `demo@neuraflow.ai` | **Password**: `demo123456`

---

## 📈 System Benchmarks & SLA Targets

- **Groq LLM Latency**: `< 150 milliseconds`
- **Vector RAG Search**: `< 1.2 seconds / 50 pages`
- **ML Model Training**: `< 800 milliseconds (10,000 rows)`
- **API Endpoint Success Rate**: `99.98%`

---

## 👤 Author & Architecture Sign-Off

**Lead Systems Architect & Senior Full-Stack Engineer:**  
**Ammad Qaiser**  
*Enterprise AI Platform & Machine Learning Engineering*

*Confidential Enterprise Case Study Documentation © 2026. All rights reserved.*
