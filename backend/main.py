from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.database import init_db, SessionLocal, User
from backend.utils.security import get_password_hash
from backend.routes import (
    auth_router, assistant_router, rag_router, pdf_router,
    excel_router, automation_router, scraping_router,
    api_hub_router, ml_router, analytics_router, reports_router
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise AI Automation Platform Backend API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(assistant_router, prefix="/api")
app.include_router(rag_router, prefix="/api")
app.include_router(pdf_router, prefix="/api")
app.include_router(excel_router, prefix="/api")
app.include_router(automation_router, prefix="/api")
app.include_router(scraping_router, prefix="/api")
app.include_router(api_hub_router, prefix="/api")
app.include_router(ml_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(reports_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@neuraflow.ai").first()
        if not demo_user:
            demo = User(
                email="demo@neuraflow.ai",
                full_name="Demo User",
                hashed_password=get_password_hash("demo123456"),
                role="Admin"
            )
            db.add(demo)
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
