import os
import shutil
import glob
import io
import logging
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.database.models import AutomationLog

logger = logging.getLogger(__name__)

class AutomationService:
    @staticmethod
    def organize_folder(db: Session, user_id: int, directory_path: str) -> dict:
        if not os.path.exists(directory_path):
            return {"status": "Error", "message": f"Directory '{directory_path}' does not exist."}

        categories = {
            "Documents": [".pdf", ".docx", ".txt", ".rtf"],
            "Spreadsheets": [".csv", ".xlsx", ".xls"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Code_Data": [".json", ".py", ".html", ".css", ".js"],
            "Archives": [".zip", ".tar", ".gz", ".rar"]
        }

        moved_count = 0
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                for cat_name, cat_exts in categories.items():
                    if ext in cat_exts:
                        cat_dir = os.path.join(directory_path, cat_name)
                        os.makedirs(cat_dir, exist_ok=True)
                        shutil.move(item_path, os.path.join(cat_dir, item))
                        moved_count += 1
                        break

        log = AutomationLog(
            user_id=user_id,
            task_name="Folder Organization",
            status="Success",
            result_summary=f"Organized {moved_count} file(s) into category subfolders in {directory_path}."
        )
        db.add(log)
        db.commit()

        return {"status": "Success", "moved_files": moved_count, "target_dir": directory_path}

    @staticmethod
    def batch_rename(db: Session, user_id: int, directory_path: str, prefix: str, ext_filter: str | None = None) -> dict:
        if not os.path.exists(directory_path):
            return {"status": "Error", "message": f"Directory '{directory_path}' does not exist."}

        clean_filter = None
        if ext_filter and ext_filter.strip():
            clean_filter = ext_filter.strip().lower()
            if not clean_filter.startswith("."):
                clean_filter = "." + clean_filter

        renamed_count = 0
        files = os.listdir(directory_path)
        for idx, item in enumerate(files, 1):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1]
                if clean_filter and not item.lower().endswith(clean_filter):
                    continue
                new_name = f"{prefix}_{idx:03d}{ext}"
                new_path = os.path.join(directory_path, new_name)
                os.rename(item_path, new_path)
                renamed_count += 1

        log = AutomationLog(
            user_id=user_id,
            task_name="Batch File Renaming",
            status="Success",
            result_summary=f"Renamed {renamed_count} file(s) with prefix '{prefix}'."
        )
        db.add(log)
        db.commit()

        return {"status": "Success", "renamed_files": renamed_count}

    @staticmethod
    def merge_pdfs(db: Session, user_id: int, file_bytes_list: List[bytes], filenames: List[str]) -> Tuple[bytes, str]:
        try:
            import pypdf
            writer = pypdf.PdfWriter()
            reader_cls = pypdf.PdfReader
        except ImportError:
            import PyPDF2
            writer = PyPDF2.PdfWriter()
            reader_cls = PyPDF2.PdfReader

        for b, name in zip(file_bytes_list, filenames):
            try:
                reader = reader_cls(io.BytesIO(b), strict=False)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                logger.warning(f"Error parsing PDF '{name}': {e}")
                continue

        out_buffer = io.BytesIO()
        writer.write(out_buffer)
        writer.close()

        output_name = "merged_documents.pdf"

        log = AutomationLog(
            user_id=user_id,
            task_name="PDF Merge",
            status="Success",
            result_summary=f"Successfully merged {len(filenames)} PDF documents into {output_name}."
        )
        db.add(log)
        db.commit()

        return out_buffer.getvalue(), output_name

    @staticmethod
    def split_pdf(db: Session, user_id: int, file_bytes: bytes, filename: str) -> List[Tuple[bytes, str]]:
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes), strict=False)
            writer_cls = pypdf.PdfWriter
        except ImportError:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes), strict=False)
            writer_cls = PyPDF2.PdfWriter

        split_results = []
        base_name = os.path.splitext(filename)[0]

        for idx, page in enumerate(reader.pages, 1):
            writer = writer_cls()
            writer.add_page(page)
            out_buf = io.BytesIO()
            writer.write(out_buf)
            split_filename = f"{base_name}_page_{idx}.pdf"
            split_results.append((out_buf.getvalue(), split_filename))

        log = AutomationLog(
            user_id=user_id,
            task_name="PDF Split",
            status="Success",
            result_summary=f"Split '{filename}' into {len(split_results)} single-page PDFs."
        )
        db.add(log)
        db.commit()

        return split_results
