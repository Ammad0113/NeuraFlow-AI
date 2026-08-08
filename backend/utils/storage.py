import os
import uuid
from backend.config.settings import settings

def save_uploaded_file(file_bytes: bytes, filename: str, subfolder: str = "uploads") -> str:
    target_dir = os.path.join(settings.BASE_DIR, "storage", subfolder)
    os.makedirs(target_dir, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    file_path = os.path.join(target_dir, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(file_bytes)
        
    return file_path

def get_storage_path(filename: str, subfolder: str = "uploads") -> str:
    return os.path.join(settings.BASE_DIR, "storage", subfolder, filename)
