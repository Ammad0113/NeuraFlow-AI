from .auth import router as auth_router
from .assistant import router as assistant_router
from .rag import router as rag_router
from .pdf import router as pdf_router
from .excel import router as excel_router
from .automation import router as automation_router
from .scraping import router as scraping_router
from .api_hub import router as api_hub_router
from .ml import router as ml_router
from .analytics import router as analytics_router
from .reports import router as reports_router

__all__ = [
    "auth_router", "assistant_router", "rag_router", "pdf_router",
    "excel_router", "automation_router", "scraping_router",
    "api_hub_router", "ml_router", "analytics_router", "reports_router"
]
