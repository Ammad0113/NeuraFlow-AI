from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.database.models import User, MLModelArtifact
from backend.models.ml import MLTrainResponse, MLPredictRequest, MLPredictResponse
from backend.services.ml_service import MLService
from typing import List

router = APIRouter(prefix="/ml", tags=["Machine Learning Workspace"])

@router.post("/train", response_model=MLTrainResponse)
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    task_type: str = Form("classification"),
    algorithm: str = Form("random_forest"),
    test_size: float = Form(0.2),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_bytes = await file.read()
    return MLService.train_model(db, current_user.id, file_bytes, file.filename, target_column, task_type, algorithm, test_size)

@router.post("/predict", response_model=MLPredictResponse)
def predict(req: MLPredictRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pred = MLService.predict(db, req.model_id, req.input_data)
    return {"model_id": req.model_id, "prediction": pred}

@router.get("/models")
def list_models(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(MLModelArtifact).filter(MLModelArtifact.user_id == current_user.id).order_by(MLModelArtifact.created_at.desc()).all()
