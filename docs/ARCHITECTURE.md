# NeuraFlow AI - Enterprise Architecture Guide

## Overview
NeuraFlow AI is designed following clean microservice patterns with an asynchronous FastAPI backend and a Streamlit UI frontend.

```
+-------------------------------------------------------------+
|                     Streamlit Web UI                        |
|            (Components, Views, CSS Theme, Plotly)           |
+------------------------------+------------------------------+
                               | HTTP (JWT Auth)
+------------------------------v------------------------------+
|                     FastAPI Backend Router                  |
+---------------+--------------+--------------+---------------+
| Auth Router   | RAG Router   | ML Router    | Excel Router  |
+---------------+--------------+--------------+---------------+
                               |
+------------------------------v------------------------------+
|                      Service Layer                          |
|  AuthService | RAGService | MLService | PDFService | etc.   |
+---------------+--------------+--------------+---------------+
                               |
+------------------------------v------------------------------+
|             Database & In-Memory Vector Storage             |
|   SQLAlchemy ORM + SQLite + TF-IDF Vectorizer + PKL Cache   |
+-------------------------------------------------------------+
```

## Security & Auth
- JWT (JSON Web Tokens) with standard SHA-256 / bcrypt password hashing.
- Role-Based Access Control (Admin / Member).

## Intelligence Engines
1. **RAG Vector Search Engine**: TF-IDF Matrix Vectorizer with Cosine Similarity index over chunked PDF/DOCX/TXT files.
2. **ML Workspace**: Scikit-Learn Classification (RandomForest, Logistic Regression, DecisionTree, GradientBoosting) and Regression pipelines with automated preprocessing.
3. **Document & Data Intelligence**: PDF clause/risk extraction, Excel deduplication & numeric mean/median imputation.
