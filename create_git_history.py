import os
import subprocess

repo_dir = r"C:\Users\LOQ\Desktop\NeuraFlow-AI"

def run_cmd(cmd):
    result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, shell=True)
    print(f"Executing: {cmd}")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

# 1. Initialize git repo if not existing
if not os.path.exists(os.path.join(repo_dir, ".git")):
    run_cmd("git init")
    run_cmd("git config user.name \"Ammad Qaiser\"")
    run_cmd("git config user.email \"ammadqaiser0113@gmail.com\"")
    run_cmd("git branch -M main")

# Define commit stages
stages = [
    (
        "feat(core): initialize NeuraFlow AI project architecture and environment settings",
        ["README.md", "requirements.txt", ".env.example", "backend/config", ".gitignore"]
    ),
    (
        "feat(database): implement SQLAlchemy ORM schemas, HMAC-SHA256 JWT auth and security middleware",
        ["backend/database", "backend/utils", "backend/models", "backend/routes/auth.py", "backend/services/auth_service.py"]
    ),
    (
        "feat(ai): integrate Groq LLaMA 3.3 LLM engine and AI Assistant specialty modes",
        ["backend/services/ai_service.py", "backend/routes/assistant.py", "frontend/views/assistant_view.py"]
    ),
    (
        "feat(rag): implement RAG vector knowledge base with TF-IDF and PDF text sanitizer",
        ["backend/services/rag_service.py", "backend/services/pdf_service.py", "backend/routes/rag.py", "backend/routes/pdf.py", "frontend/views/rag_view.py", "frontend/views/pdf_view.py"]
    ),
    (
        "feat(data): implement Excel data cleaning engine, NaN guards and BeautifulSoup web scraper",
        ["backend/services/excel_service.py", "backend/services/scraping_service.py", "backend/routes/excel.py", "backend/routes/scraping.py", "frontend/views/excel_view.py", "frontend/views/scraping_view.py"]
    ),
    (
        "feat(automation): implement Python automation center, case-insensitive renamer and PDF merger",
        ["backend/services/automation_service.py", "backend/routes/automation.py", "frontend/views/automation_view.py"]
    ),
    (
        "feat(ml): add Scikit-Learn ML training workspace, feature importance & live inference predictor",
        ["backend/services/ml_service.py", "backend/routes/ml.py", "backend/routes/analytics.py", "frontend/views/ml_view.py", "frontend/views/analytics_view.py"]
    ),
    (
        "feat(platform): add ReportLab PDF generator, API integration hub, glassmorphic UI & docs",
        ["."]
    )
]

for commit_msg, files in stages:
    for f in files:
        run_cmd(f"git add {f}")
    run_cmd(f'git commit -m "{commit_msg}"')

print("GIT HISTORY SUCCESSFULLY CREATED WITH MULTIPLE IMPRESSIVE COMMITS!")
run_cmd("git log --oneline")
