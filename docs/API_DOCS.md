# NeuraFlow AI API Documentation

## Auth Endpoints
- `POST /api/auth/signup` - Register a new user account.
- `POST /api/auth/login` - Authenticate user and receive JWT access token.
- `POST /api/auth/forgot-password` - Reset account password.
- `GET /api/auth/me` - Retrieve authenticated user profile.

## Assistant Endpoints
- `POST /api/assistant/chat` - Process multi-mode chat (general, code, email, summary, report, brainstorm).
- `GET /api/assistant/conversations` - Fetch user conversation history.

## RAG Knowledge Base
- `POST /api/rag/upload` - Upload PDF/DOCX/TXT file for vector chunk indexing.
- `POST /api/rag/query` - Perform semantic search & grounded Q&A query.
- `GET /api/rag/documents` - List indexed documents.

## Document & Data Intelligence
- `POST /api/pdf/analyze` - Extract summary, keywords, and compliance risks from PDF.
- `POST /api/excel/inspect` - Inspect dataset dimensions, duplicates, and missing values.
- `POST /api/excel/clean` - Clean dataset and download cleaned output file.

## Python Automation
- `POST /api/automation/organize-folder` - Categorize directory files into subfolders.
- `POST /api/automation/batch-rename` - Batch rename files with prefix.
- `POST /api/automation/pdf-merge` - Combine multiple PDF files.

## Web Scraping Studio
- `POST /api/scraping/scrape` - Scrape target URL (news, product, table, generic).
- `POST /api/scraping/export` - Export scraped data to CSV/Excel/JSON.

## Machine Learning Workspace
- `POST /api/ml/train` - Train classification/regression model on dataset.
- `POST /api/ml/predict` - Execute prediction inference using trained model.
- `GET /api/ml/models` - List trained model artifacts.
