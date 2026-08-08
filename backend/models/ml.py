from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class MLTrainRequest(BaseModel):
    dataset_name: str
    target_column: str
    task_type: str # classification, regression
    algorithm: str # random_forest, logistic_regression, decision_tree, linear_regression, gradient_boosting
    test_size: float = 0.2

class MLPredictRequest(BaseModel):
    model_id: int
    input_data: Dict[str, Any]

class MLTrainResponse(BaseModel):
    model_id: int
    model_name: str
    task_type: str
    algorithm: str
    metrics: Dict[str, Any]
    feature_importance: Optional[Dict[str, float]] = None

class MLPredictResponse(BaseModel):
    model_id: int
    prediction: Any
