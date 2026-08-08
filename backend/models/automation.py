from pydantic import BaseModel
from typing import List, Optional

class FolderOrganizeRequest(BaseModel):
    directory_path: str

class FileRenameRequest(BaseModel):
    directory_path: str
    prefix: str
    extension_filter: Optional[str] = None

class PDFMergeRequest(BaseModel):
    file_paths: List[str]
    output_name: str

class ScheduleTaskRequest(BaseModel):
    task_name: str
    interval_seconds: int
    payload: str
