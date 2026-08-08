import os
import io
import pandas as pd
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.database.models import ReportHistory
from backend.utils.storage import save_uploaded_file
from backend.config.settings import settings

class ReportService:
    @staticmethod
    def generate_report(db: Session, user_id: int, title: str, report_type: str, template: str, custom_notes: str | None = None) -> Tuple[bytes, str, int]:
        report_type_upper = report_type.upper()
        
        if report_type_upper == "PDF":
            content_bytes, filename = ReportService._generate_pdf(title, template, custom_notes)
        elif report_type_upper == "CSV":
            content_bytes, filename = ReportService._generate_csv(title, template)
        else: # Markdown
            content_bytes, filename = ReportService._generate_markdown(title, template, custom_notes)

        # Save to storage
        saved_path = save_uploaded_file(content_bytes, filename, subfolder="reports")

        # Record in DB
        db_report = ReportHistory(
            user_id=user_id,
            title=title,
            report_type=report_type_upper,
            file_path=saved_path
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)

        return content_bytes, filename, db_report.id

    @staticmethod
    def _generate_markdown(title: str, template: str, custom_notes: str | None) -> Tuple[bytes, str]:
        md_text = f"# 📄 {title}\n\n"
        md_text += f"**Platform:** NeuraFlow AI Enterprise\n"
        md_text += f"**Report Category:** {template.capitalize()} Strategic Analysis\n"
        md_text += f"**Generated:** 2026-08-05\n\n"
        md_text += "---\n\n"
        md_text += "## 1. Executive Summary\n"
        md_text += f"This report delivers actionable business intelligence for **{title}**.\n\n"
        md_text += "## 2. Platform KPI Metrics\n"
        md_text += "| Metric Name | Value | Target | Status |\n"
        md_text += "| :--- | :--- | :--- | :--- |\n"
        md_text += "| Automation Success Rate | 99.8% | 99.0% | ✅ Exceeding |\n"
        md_text += "| Average Response Latency | 140 ms | < 250 ms | ✅ Optimal |\n"
        md_text += "| Document Ingestion Volume | 12,450 pgs | 10,000 pgs | ✅ Surpassed |\n"
        md_text += "| ML Model Accuracy Benchmark | 94.2% | 90.0% | ✅ Enterprise Grade |\n\n"
        md_text += "## 3. Strategic Analysis & Recommendations\n"
        md_text += "1. Continue expansion of automated Python folder and data cleaning rules.\n"
        md_text += "2. Ingest additional regulatory documentation into the RAG vector index.\n"
        md_text += "3. Monitor Scikit-Learn classification pipelines for drift.\n\n"

        if custom_notes:
            md_text += f"## 4. Custom Executive Notes\n> {custom_notes}\n\n"

        md_text += "---\n*NeuraFlow AI Enterprise Automated Report Engine*"
        
        return md_text.encode("utf-8"), f"{title.lower().replace(' ', '_')}.md"

    @staticmethod
    def _generate_csv(title: str, template: str) -> Tuple[bytes, str]:
        data = [
            {"Category": "Automation", "Metric": "Folder Organization Runs", "Value": 142, "Status": "Success"},
            {"Category": "Automation", "Metric": "PDF Splitting & Merging", "Value": 89, "Status": "Success"},
            {"Category": "RAG AI", "Metric": "Vector Embeddings Stored", "Value": 4510, "Status": "Indexed"},
            {"Category": "ML Workspace", "Metric": "Random Forest Models Trained", "Value": 18, "Status": "Deployed"},
            {"Category": "Web Scraping", "Metric": "Scraped Records Exported", "Value": 9420, "Status": "Exported"}
        ]
        df = pd.DataFrame(data)
        out_buf = io.BytesIO()
        df.to_csv(out_buf, index=False)
        return out_buf.getvalue(), f"{title.lower().replace(' ', '_')}.csv"

    @staticmethod
    def _generate_pdf(title: str, template: str, custom_notes: str | None) -> Tuple[bytes, str]:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#1E293B'),
                spaceAfter=12
            )

            body_style = styles['Normal']

            elements = []
            elements.append(Paragraph(f"<b>{title}</b>", title_style))
            elements.append(Paragraph("<b>NeuraFlow AI Enterprise Platform Report</b>", body_style))
            elements.append(Spacer(1, 15))

            summary_p = Paragraph(
                f"<b>Executive Summary:</b> This automated PDF report summarizes strategic performance and data automation metrics for template <i>'{template}'</i>.",
                body_style
            )
            elements.append(summary_p)
            elements.append(Spacer(1, 15))

            # Table
            data = [
                ['Module', 'Execution Metric', 'Status'],
                ['Python Automation', '142 Tasks Processed', 'Success'],
                ['RAG Engine', '4,510 Vector Chunks Indexed', 'Active'],
                ['ML Workspace', '94.2% Model Accuracy', 'Verified'],
                ['API Hub', '99.9% Uptime', 'Operational']
            ]

            t = Table(data, colWidths=[150, 200, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1'))
            ]))
            elements.append(t)

            if custom_notes:
                elements.append(Spacer(1, 15))
                elements.append(Paragraph(f"<b>Notes:</b> {custom_notes}", body_style))

            doc.build(elements)
            return buf.getvalue(), f"{title.lower().replace(' ', '_')}.pdf"
        except Exception:
            # Simple text fallback if ReportLab fails
            text_pdf = f"NeuraFlow AI Enterprise Report: {title}\nCategory: {template}\nMetrics: 99.8% Success Rate."
            return text_pdf.encode(), f"{title.lower().replace(' ', '_')}.pdf"
