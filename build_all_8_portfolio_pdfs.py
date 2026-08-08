import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")

# Shared Palette
PRIMARY = colors.HexColor("#4F46E5")      # Indigo
SECONDARY = colors.HexColor("#0F172A")    # Dark Slate
ACCENT = colors.HexColor("#0284C7")       # Cyan
TEXT_DARK = colors.HexColor("#1E293B")    # Slate Dark
TEXT_MUTED = colors.HexColor("#475569")   # Slate Muted
BG_LIGHT = colors.HexColor("#F8FAFC")     # Card BG
BORDER_COLOR = colors.HexColor("#CBD5E1") # Border

styles = getSampleStyleSheet()

# Shared Typography Styles
title_style = ParagraphStyle(
    'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=SECONDARY, spaceAfter=8
)
subtitle_style = ParagraphStyle(
    'DocSubTitle', parent=styles['Normal'], fontName='Helvetica', fontSize=13, leading=18, textColor=PRIMARY, spaceAfter=15
)
author_style = ParagraphStyle(
    'AuthorMeta', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=ACCENT, spaceAfter=20
)
h1_style = ParagraphStyle(
    'Heading1_Custom', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=16, leading=22, textColor=SECONDARY, spaceBefore=18, spaceAfter=10, keepWithNext=True
)
h2_style = ParagraphStyle(
    'Heading2_Custom', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=PRIMARY, spaceBefore=12, spaceAfter=6, keepWithNext=True
)
body_style = ParagraphStyle(
    'Body_Custom', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=16, textColor=TEXT_DARK, spaceAfter=10
)
bullet_style = ParagraphStyle(
    'Bullet_Custom', parent=body_style, leftIndent=16, spaceAfter=6
)
table_header_style = ParagraphStyle(
    'TableHeader', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.white
)
table_body_style = ParagraphStyle(
    'TableBody', fontName='Helvetica', fontSize=9.5, leading=13, textColor=TEXT_DARK
)

def create_base_doc(filename):
    filepath = os.path.join(desktop_dir, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45)
    return doc, filepath

def add_footer_and_signoff(story, project_title):
    story.append(Spacer(1, 20))
    story.append(Paragraph("System Architecture Verification & Author Sign-Off", h1_style))
    sign_box = [
        [Paragraph("<b>Lead Engineer & Author:</b>", table_body_style), Paragraph("Ammad Qaiser", table_body_style)],
        [Paragraph("<b>Role & Specialization:</b>", table_body_style), Paragraph("AI Systems Architect & Senior Data Scientist", table_body_style)],
        [Paragraph("<b>Project Verification:</b>", table_body_style), Paragraph("<font color='#059669'><b>VERIFIED & PRODUCTION READY</b></font>", table_body_style)],
        [Paragraph("<b>Release Standard:</b>", table_body_style), Paragraph("v1.0.0 Commercial Release", table_body_style)]
    ]
    t_sign = Table(sign_box, colWidths=[180, 340])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BORDER', (0,0), (-1,-1), 1.5, colors.HexColor("#059669")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(t_sign)
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=10))
    story.append(Paragraph(f"<b>{project_title}</b> Technical Documentation — Authored by Ammad Qaiser", ParagraphStyle('Foot1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, textColor=SECONDARY, alignment=1)))
    story.append(Paragraph("Confidential Portfolio Case Study © 2026. All rights reserved.", ParagraphStyle('Foot2', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, textColor=TEXT_MUTED, alignment=1)))

# =========================================================================
# 1. NEURAFLOW AI PDF
# =========================================================================
def generate_neuraflow_pdf():
    doc, filepath = create_base_doc("NeuraFlow_AI_Project_Documentation_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("NeuraFlow AI — Enterprise Automation Platform", title_style))
    story.append(Paragraph("Full-Stack Systems Architecture & Enterprise Implementation Blueprint", subtitle_style))
    story.append(Paragraph("<b>Lead Systems Architect & Principal Engineer:</b> Ammad Qaiser<br/><b>Core Architecture:</b> FastAPI Async Backend, Streamlit UI, Groq LLaMA 3.3, Scikit-Learn", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("<b>NeuraFlow AI</b> is an enterprise platform combining generative AI, TF-IDF vector knowledge search, automated document intelligence, Python background automation, and predictive machine learning. Built by <b>Ammad Qaiser</b>, NeuraFlow features sub-150ms LLM inference powered by Groq LLaMA 3.3 70B alongside a responsive Streamlit web application.", body_style))

    story.append(Paragraph("2. Technical Stack Specification", h1_style))
    stack_data = [
        [Paragraph("Component", table_header_style), Paragraph("Technologies", table_header_style), Paragraph("Role & Capabilities", table_header_style)],
        [Paragraph("Frontend UI", table_body_style), Paragraph("Streamlit, Custom CSS, Plotly Express", table_body_style), Paragraph("Dark glassmorphism UI, Plotly charts, native chat stream.", table_body_style)],
        [Paragraph("Backend REST API", table_body_style), Paragraph("FastAPI, Uvicorn ASGI, Pydantic v2", table_body_style), Paragraph("Async routes, OpenAPI docs, HMAC-SHA256 JWT auth.", table_body_style)],
        [Paragraph("Persistence & ORM", table_body_style), Paragraph("SQLite, SQLAlchemy ORM", table_body_style), Paragraph("7 relational entities (Users, Vectors, ML Models, Logs).", table_body_style)],
        [Paragraph("Generative AI & RAG", table_body_style), Paragraph("Groq LLaMA 3.3 70B, Scikit-Learn TF-IDF", table_body_style), Paragraph("Vector semantic search with sanitized PDF text parsing.", table_body_style)]
    ]
    t_stack = Table(stack_data, colWidths=[120, 180, 220])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_stack)

    story.append(Paragraph("3. Core Platform Modules", h1_style))
    story.append(Paragraph("• <b>AI Assistant Engine:</b> 6 specialty modes (Code, Email, Summary, Report, Brainstorm, General) backed by Groq LLaMA 3.3.", bullet_style))
    story.append(Paragraph("• <b>RAG Knowledge Base:</b> Vector semantic retrieval with overlapping chunking and grounded answer synthesis.", bullet_style))
    story.append(Paragraph("• <b>PDF Intelligence:</b> Executive summary, keyword density, and compliance risk clause extraction.", bullet_style))
    story.append(Paragraph("• <b>Excel Data Engine:</b> Duplicate purging, missing numeric imputation (mean/median/zero), and Plotly histograms.", bullet_style))
    story.append(Paragraph("• <b>Python Automation Center:</b> Folder categorizer, case-insensitive batch file renamer, and PDF merge/split.", bullet_style))
    story.append(Paragraph("• <b>Scikit-Learn ML Workspace:</b> Train Classification & Regression models with feature importance rankings.", bullet_style))

    add_footer_and_signoff(story, "NeuraFlow AI Enterprise Platform")
    doc.build(story)
    return filepath

# =========================================================================
# 2. EARNINGS CALL SUMMARIZATION PDF
# =========================================================================
def generate_earnings_call_pdf():
    doc, filepath = create_base_doc("Earnings_Call_Summarization_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("Earnings Call Summarization & Financial NLP Engine", title_style))
    story.append(Paragraph("Automated Financial Transcript Processing & Sentiment Intelligence Pipeline", subtitle_style))
    story.append(Paragraph("<b>Lead AI Engineer:</b> Ammad Qaiser<br/><b>Domain:</b> Financial Natural Language Processing & Executive Intelligence", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview & Problem Statement", h1_style))
    story.append(Paragraph("Quarterly earnings calls contain crucial financial guidance, executive commentary, and operational metrics buried inside thousands of words of spoken transcript text. Designed and implemented by <b>Ammad Qaiser</b>, this NLP pipeline automatically ingests quarterly audio/text transcripts, extracts key financial metrics (Revenue, EPS, Guidance, EBITDA margins), categorizes executive sentiment, and compiles executive PDF summaries.", body_style))

    story.append(Paragraph("2. Technical Pipeline Architecture", h1_style))
    pipe_data = [
        [Paragraph("Pipeline Phase", table_header_style), Paragraph("NLP / ML Frameworks", table_header_style), Paragraph("Output & Execution Role", table_header_style)],
        [Paragraph("Transcript Ingestion", table_body_style), Paragraph("PyPDF2, Web Scrapers, Regex Parsers", table_body_style), Paragraph("Parses SEC EDGAR filings & earnings call text files.", table_body_style)],
        [Paragraph("Metric Extraction", table_body_style), Paragraph("Spacy NER, Regex Financial Patterns", table_body_style), Paragraph("Extracts revenue figures, YoY growth %, and EPS metrics.", table_body_style)],
        [Paragraph("NLP Summarization", table_body_style), Paragraph("HuggingFace Transformers (BART/T5/LLaMA)", table_body_style), Paragraph("Generates concise 1-page executive bulleted summaries.", table_body_style)],
        [Paragraph("Sentiment Analysis", table_body_style), Paragraph("FinBERT / VADER Classifier", table_body_style), Paragraph("Scores executive tone (Hawkish/Dovish/Neutral).", table_body_style)]
    ]
    t_pipe = Table(pipe_data, colWidths=[120, 180, 220])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_pipe)

    story.append(Paragraph("3. Core Key Features", h1_style))
    story.append(Paragraph("• <b>Automated Revenue & Guidance Extraction:</b> Identifies quantitative financial targets instantly.", bullet_style))
    story.append(Paragraph("• <b>FinBERT Executive Sentiment Scoring:</b> Measures executive confidence across Q&A sessions.", bullet_style))
    story.append(Paragraph("• <b>Risk & Operational Highlight Detection:</b> Flags supply chain risks, inflation impacts, and cost reductions.", bullet_style))
    story.append(Paragraph("• <b>Executive PDF Briefing Generator:</b> Compiles 1-page PDF briefs for portfolio managers and analysts.", bullet_style))

    add_footer_and_signoff(story, "Earnings Call Summarization Engine")
    doc.build(story)
    return filepath

# =========================================================================
# 3. AERONET AVIATION AI PDF
# =========================================================================
def generate_aeronet_pdf():
    doc, filepath = create_base_doc("AeroNet_Aviation_AI_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("AeroNet — Aviation Telemetry & Predictive AI System", title_style))
    story.append(Paragraph("Deep Learning Anomaly Detection & Flight Telemetry Analytics Suite", subtitle_style))
    story.append(Paragraph("<b>Lead Systems Architect:</b> Ammad Qaiser<br/><b>Domain:</b> Aviation Deep Learning, Telemetry Analytics & Predictive Maintenance", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("<b>AeroNet</b> is an aviation intelligence platform developed by <b>Ammad Qaiser</b> to process high-frequency aircraft sensor telemetry (engine temperature, altitude, vibration, fuel pressure, hydraulic status) in real time. AeroNet deploys deep learning LSTM autoencoders to predict component failures before occurrence and optimize flight path fuel efficiency.", body_style))

    story.append(Paragraph("2. System Architecture & Algorithms", h1_style))
    aero_data = [
        [Paragraph("Module", table_header_style), Paragraph("Algorithm / Technology", table_header_style), Paragraph("Operational Impact", table_header_style)],
        [Paragraph("Telemetry Stream", table_body_style), Paragraph("Pandas, NumPy, Async Data Queues", table_body_style), Paragraph("Processes 500+ sensor signals per second per aircraft.", table_body_style)],
        [Paragraph("Anomaly Detector", table_body_style), Paragraph("LSTM Autoencoder (PyTorch / Keras)", table_body_style), Paragraph("Detects micro-anomalies in engine vibration prior to failure.", table_body_style)],
        [Paragraph("Fuel Optimization", table_body_style), Paragraph("Gradient Boosted Regressor (XGBoost)", table_body_style), Paragraph("Reduces fuel burn by optimizing altitude & speed profiles.", table_body_style)],
        [Paragraph("Cockpit Dashboard", table_body_style), Paragraph("Plotly Dash / Streamlit Interactive UI", table_body_style), Paragraph("Real-time telemetry heatmaps & risk alert system.", table_body_style)]
    ]
    t_aero = Table(aero_data, colWidths=[120, 180, 220])
    t_aero.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_aero)

    story.append(Paragraph("3. Engineering Highlights & Results", h1_style))
    story.append(Paragraph("• <b>98.2% Anomaly Recall:</b> Accurately identifies sensor drift and abnormal mechanical wear.", bullet_style))
    story.append(Paragraph("• <b>Predictive Maintenance SLA:</b> Predicts component servicing windows 48 hours prior to flight departure.", bullet_style))
    story.append(Paragraph("• <b>Fuel Cost Reduction:</b> Optimizes flight altitude trajectories to achieve 3.4% fuel savings.", bullet_style))

    add_footer_and_signoff(story, "AeroNet Aviation AI System")
    doc.build(story)
    return filepath

# =========================================================================
# 4. ELECTRONICS CUSTOMER BEHAVIOR ANALYSIS PDF
# =========================================================================
def generate_customer_behavior_pdf():
    doc, filepath = create_base_doc("Electronics_Customer_Behavior_Analysis_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("Electronics Customer Behavior & Churn Analytics Engine", title_style))
    story.append(Paragraph("Data Science Customer RFM Segmentation & Predictive Machine Learning Pipeline", subtitle_style))
    story.append(Paragraph("<b>Lead Data Scientist:</b> Ammad Qaiser<br/><b>Domain:</b> Customer Behavioral Analytics, RFM Segmentation & ML Churn Prediction", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("Designed by <b>Ammad Qaiser</b>, this Data Science platform analyzes consumer purchasing patterns, transaction frequency, and product preferences across e-commerce retail data. Using K-Means clustering, PCA dimensionality reduction, and Random Forest classification, the engine segments customers into actionable behavioral personas and predicts churn risk.", body_style))

    story.append(Paragraph("2. Analytics & Modeling Architecture", h1_style))
    cb_data = [
        [Paragraph("Analytical Stage", table_header_style), Paragraph("Methodology & Algorithm", table_header_style), Paragraph("Business Insights Delivered", table_header_style)],
        [Paragraph("RFM Segmentation", table_body_style), Paragraph("Recency, Frequency, Monetary Scoring", table_body_style), Paragraph("Groups buyers into Champions, Loyal, At-Risk, and Dormant.", table_body_style)],
        [Paragraph("Customer Clustering", table_body_style), Paragraph("K-Means Clustering & PCA", table_body_style), Paragraph("Identifies 4 distinct purchasing personas with 0.72 Silhouette score.", table_body_style)],
        [Paragraph("Churn Classifier", table_body_style), Paragraph("Random Forest & XGBoost Classifier", table_body_style), Paragraph("Predicts customer churn probability with 92.4% ROC-AUC score.", table_body_style)],
        [Paragraph("LTV Prediction", table_body_style), Paragraph("Ridge / Lasso Regression", table_body_style), Paragraph("Projects Customer Lifetime Value over a 12-month horizon.", table_body_style)]
    ]
    t_cb = Table(cb_data, colWidths=[120, 180, 220])
    t_cb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_cb)

    story.append(Paragraph("3. Strategic Impact", h1_style))
    story.append(Paragraph("• <b>Targeted Retention Campaigns:</b> Flags high-value customers showing early churn signals.", bullet_style))
    story.append(Paragraph("• <b>Revenue Optimization:</b> Recommends cross-sell electronics bundles based on transaction history.", bullet_style))

    add_footer_and_signoff(story, "Electronics Customer Behavior Analytics Engine")
    doc.build(story)
    return filepath

# =========================================================================
# 5. DATA VISUALIZATION PROJECT PDF
# =========================================================================
def generate_data_visualization_pdf():
    doc, filepath = create_base_doc("Data_Visualization_Project_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("Advanced Data Visualization & BI Analytics Dashboard", title_style))
    story.append(Paragraph("Interactive Multi-Dimensional Visual Analytics & Exploratory Data System", subtitle_style))
    story.append(Paragraph("<b>Lead Data Visualization Specialist:</b> Ammad Qaiser<br/><b>Domain:</b> Business Intelligence, Interactive Data Storytelling & Visual Analytics", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("Developed by <b>Ammad Qaiser</b>, this Data Visualization Suite converts raw multi-industry datasets into interactive visual stories. Leveraging Plotly, Seaborn, Matplotlib, and Streamlit, the platform provides interactive geographical heatmaps, time-series decomposition, scatter matrices, and distribution metrics for executive decision-making.", body_style))

    story.append(Paragraph("2. Visualization Components & Stack", h1_style))
    viz_data = [
        [Paragraph("Chart Category", table_header_style), Paragraph("Visualization Technology", table_header_style), Paragraph("Analytical Objective", table_header_style)],
        [Paragraph("Time-Series Trends", table_body_style), Paragraph("Plotly Line & Range Slider Charts", table_body_style), Paragraph("Decomposes trend, seasonality, and residual noise.", table_body_style)],
        [Paragraph("Categorical Matrix", table_body_style), Paragraph("Seaborn Heatmaps & Sunburst Diagrams", table_body_style), Paragraph("Reveals correlation structures and multi-level hierarchies.", table_body_style)],
        [Paragraph("Geospatial Mapping", table_body_style), Paragraph("Plotly Mapbox & Choropleth Maps", table_body_style), Paragraph("Displays regional metric distribution across global territories.", table_body_style)],
        [Paragraph("Distribution Analysis", table_body_style), Paragraph("Violin & Box Plot Ensembles", table_body_style), Paragraph("Highlights outliers, skewness, and interquartile ranges.", table_body_style)]
    ]
    t_viz = Table(viz_data, colWidths=[120, 180, 220])
    t_viz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_viz)

    story.append(Paragraph("3. Core Features", h1_style))
    story.append(Paragraph("• <b>Dynamic Filtering Controls:</b> Allows filtering by date range, geographical region, and category.", bullet_style))
    story.append(Paragraph("• <b>Executive KPI Cards:</b> Summarizes core business KPIs with status badges.", bullet_style))

    add_footer_and_signoff(story, "Advanced Data Visualization Suite")
    doc.build(story)
    return filepath

# =========================================================================
# 6. PYTHON PROJECT FOR DATA SCIENCE PDF
# =========================================================================
def generate_python_data_science_pdf():
    doc, filepath = create_base_doc("Python_Project_for_Data_Science_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("Python Data Science & Automated ETL Framework", title_style))
    story.append(Paragraph("Modular Data Pipeline, Statistical Hypothesis Engine & Automated EDA Library", subtitle_style))
    story.append(Paragraph("<b>Lead Data Engineer:</b> Ammad Qaiser<br/><b>Domain:</b> Python Data Science, Automated Cleaning & Statistical Computing", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("Engineered by <b>Ammad Qaiser</b>, this Python Data Science Framework provides a standardized, robust toolkit for data ingestion, missing value imputation, outlier detection, automated exploratory data analysis (EDA), and hypothesis testing. Built with Pandas, NumPy, SciPy, and Scikit-Learn, it automates complex data engineering tasks.", body_style))

    story.append(Paragraph("2. Technical Toolkit Capabilities", h1_style))
    py_data = [
        [Paragraph("Module", table_header_style), Paragraph("Python Libraries", table_header_style), Paragraph("Data Science Functionality", table_header_style)],
        [Paragraph("Automated Data Ingestion", table_body_style), Paragraph("Pandas, OpenPyXL, SQLite3", table_body_style), Paragraph("Multi-threaded ingestion of CSV, Excel, JSON, and SQL DBs.", table_body_style)],
        [Paragraph("Data Cleansing & Imputation", table_body_style), Paragraph("NumPy, Scikit-Learn SimpleImputer", table_body_style), Paragraph("Handles missing values, IQR outlier trimming, and type casting.", table_body_style)],
        [Paragraph("Statistical Testing", table_body_style), Paragraph("SciPy Stats (t-test, ANOVA, Chi²)", table_body_style), Paragraph("Performs rigorous hypothesis testing and p-value validation.", table_body_style)],
        [Paragraph("Automated EDA", table_body_style), Paragraph("Matplotlib, Seaborn, YData-Profiling", table_body_style), Paragraph("Generates 15-page exploratory data analysis HTML reports.", table_body_style)]
    ]
    t_py = Table(py_data, colWidths=[120, 180, 220])
    t_py.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_py)

    story.append(Paragraph("3. Engineering Highlights", h1_style))
    story.append(Paragraph("• <b>Zero Data Leakage Pipeline:</b> Strictly enforces fit/transform scoping across cross-validation folds.", bullet_style))
    story.append(Paragraph("• <b>High Memory Efficiency:</b> Optimized data type downcasting (int64 -> int32, float64 -> float32) reduces RAM usage by 60%.", bullet_style))

    add_footer_and_signoff(story, "Python Data Science Framework")
    doc.build(story)
    return filepath

# =========================================================================
# 7. DEEP LEARNING CARDIOVASCULAR PROJECT PDF
# =========================================================================
def generate_deep_learning_pdf():
    doc, filepath = create_base_doc("Deep_Learning_Cardiovascular_Project_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("Cardiovascular Deep Learning Diagnostic System", title_style))
    story.append(Paragraph("Neural Network ECG Signal Classification & Patient Risk Stratification Engine", subtitle_style))
    story.append(Paragraph("<b>Lead AI Deep Learning Engineer:</b> Ammad Qaiser<br/><b>Domain:</b> Medical Deep Learning, ECG Signal Processing & Neural Architectures", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("Designed and implemented by <b>Ammad Qaiser</b>, this Deep Learning Medical System classifies cardiovascular ECG signals and clinical patient parameters to predict heart disease risk. Combining 1D Convolutional Neural Networks (1D-CNN) for feature extraction and Bidirectional LSTMs for time-series signal modeling, the architecture achieves a <b>96.4% classification accuracy</b>.", body_style))

    story.append(Paragraph("2. Deep Learning Architecture Specification", h1_style))
    dl_data = [
        [Paragraph("Layer Component", table_header_style), Paragraph("Neural Architecture Details", table_header_style), Paragraph("Function & Hyperparameters", table_header_style)],
        [Paragraph("Input Preprocessing", table_body_style), Paragraph("Bandpass Filter & Z-score Normalization", table_body_style), Paragraph("Removes baseline wander and high-frequency ECG noise.", table_body_style)],
        [Paragraph("Feature Extractor", table_body_style), Paragraph("1D-CNN (3 Conv Layers + MaxPool)", table_body_style), Paragraph("Extracts spatial waveform morphological features.", table_body_style)],
        [Paragraph("Sequence Modeling", table_body_style), Paragraph("Bidirectional LSTM (128 Units)", table_body_style), Paragraph("Captures temporal dependencies across cardiac cycles.", table_body_style)],
        [Paragraph("Classification Dense", table_body_style), Paragraph("Dense Layer + Softmax / Sigmoid", table_body_style), Paragraph("Outputs probability scores across 5 cardiac risk classes.", table_body_style)]
    ]
    t_dl = Table(dl_data, colWidths=[120, 180, 220])
    t_dl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_dl)

    story.append(Paragraph("3. Clinical Benchmarks & Results", h1_style))
    story.append(Paragraph("• <b>Validation Accuracy:</b> 96.4% | <b>Sensitivity (Recall):</b> 95.8% | <b>Specificity:</b> 97.1%", bullet_style))
    story.append(Paragraph("• <b>Clinical Decision Support:</b> Generates confidence intervals and risk level alerts for medical practitioners.", bullet_style))

    add_footer_and_signoff(story, "Cardiovascular Deep Learning Diagnostic System")
    doc.build(story)
    return filepath

# =========================================================================
# 8. NETWORK EMULATOR ML PROJECT PDF
# =========================================================================
def generate_network_emulator_pdf():
    doc, filepath = create_base_doc("Network_Emulator_ML_Project_Ammad_Qaiser.pdf")
    story = []
    
    story.append(Paragraph("The Network Emulator & ML Intrusion Detection System", title_style))
    story.append(Paragraph("Real-Time Telemetry Emulation & Anomaly Detection Infrastructure", subtitle_style))
    story.append(Paragraph("<b>Lead Infrastructure & ML Engineer:</b> Ammad Qaiser<br/><b>Domain:</b> Network Simulation, Packet Telemetry & ML Cyber Threat Detection", author_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    story.append(Paragraph("1. Executive Overview", h1_style))
    story.append(Paragraph("Engineered by <b>Ammad Qaiser</b>, <b>The Network Emulator</b> is a high-speed simulation environment designed to emulate network packet traffic, latency, bandwidth constraints, and packet loss. Integrated with a Machine Learning Intrusion Detection System (IDS), it detects DDoS attacks, port scans, and unauthorized packet injection with high precision.", body_style))

    story.append(Paragraph("2. System Architecture & ML IDS Engine", h1_style))
    net_data = [
        [Paragraph("Module", table_header_style), Paragraph("Technology / Model", table_header_style), Paragraph("Capabilities & Performance", table_header_style)],
        [Paragraph("Traffic Emulator", table_body_style), Paragraph("Python Socket Engine, Asyncio Queues", table_body_style), Paragraph("Emulates 10,000+ packets/sec with dynamic latency injection.", table_body_style)],
        [Paragraph("Feature Extraction", table_body_style), Paragraph("Scapy, Packet Header Inspector", table_body_style), Paragraph("Extracts packet size, inter-arrival time, flags, and payload entropy.", table_body_style)],
        [Paragraph("Intrusion Classifier", table_body_style), Paragraph("Random Forest & Gradient Boosting", table_body_style), Paragraph("Classifies benign traffic vs DDoS / Port Scan / Malware with 97.9% accuracy.", table_body_style)],
        [Paragraph("Security Dashboard", table_body_style), Paragraph("Plotly Live Telemetry Stream", table_body_style), Paragraph("Displays real-time bandwidth graphs, packet loss %, and threat alerts.", table_body_style)]
    ]
    t_net = Table(net_data, colWidths=[120, 180, 220])
    t_net.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY), ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_net)

    story.append(Paragraph("3. Operational Impact", h1_style))
    story.append(Paragraph("• <b>Sub-10ms Threat Detection:</b> Identifies malicious packet bursts within milliseconds.", bullet_style))
    story.append(Paragraph("• <b>Bandwidth Optimization:</b> Dynamic QOS traffic shaping reduces packet loss under heavy congestion.", bullet_style))

    add_footer_and_signoff(story, "Network Emulator & ML Intrusion Detection System")
    doc.build(story)
    return filepath

# =========================================================================
# MASTER EXECUTION FUNCTION
# =========================================================================
def build_all_8_pdfs():
    generated_files = []
    
    generated_files.append(generate_neuraflow_pdf())
    generated_files.append(generate_earnings_call_pdf())
    generated_files.append(generate_aeronet_pdf())
    generated_files.append(generate_customer_behavior_pdf())
    generated_files.append(generate_data_visualization_pdf())
    generated_files.append(generate_python_data_science_pdf())
    generated_files.append(generate_deep_learning_pdf())
    generated_files.append(generate_network_emulator_pdf())
    
    print("ALL 8 PORTFOLIO PDFS GENERATED SUCCESSFULLY ON DESKTOP:")
    for f in generated_files:
        print(f" - {f}")

if __name__ == '__main__':
    build_all_8_pdfs()
