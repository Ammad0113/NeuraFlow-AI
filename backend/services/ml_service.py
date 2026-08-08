import os
import io
import pickle
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from backend.database.models import MLModelArtifact
from backend.config.settings import settings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score, mean_absolute_error
from typing import Dict, Any, Tuple

# In-memory trained model cache
_MODEL_CACHE: Dict[int, Any] = {}

class MLService:
    @staticmethod
    def train_model(db: Session, user_id: int, file_bytes: bytes, filename: str, target_column: str, task_type: str, algorithm: str, test_size: float = 0.2) -> dict:
        # Load dataset
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset. Available columns: {list(df.columns)}")

        df = df.dropna()
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Basic Preprocessing: Encode categorical features
        X = pd.get_dummies(X, drop_first=True)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        # Select Algorithm
        model = MLService._instantiate_model(task_type, algorithm)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        metrics = {}
        feature_importance = {}

        if task_type == "classification":
            acc = float(accuracy_score(y_test, preds))
            f1 = float(f1_score(y_test, preds, average='weighted', zero_division=0))
            metrics = {
                "accuracy": round(acc, 4),
                "precision": round(float(precision_score(y_test, preds, average='weighted', zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, preds, average='weighted', zero_division=0)), 4),
                "f1_score": round(f1, 4)
            }
            score_val = acc
        else: # regression
            r2 = float(r2_score(y_test, preds))
            mse = float(mean_squared_error(y_test, preds))
            mae = float(mean_absolute_error(y_test, preds))
            metrics = {
                "r2_score": round(r2, 4),
                "mse": round(mse, 4),
                "rmse": round(np.sqrt(mse), 4),
                "mae": round(mae, 4)
            }
            score_val = r2

        # Extract Feature Importance if supported
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feat_names = list(X.columns)
            for fn, imp in zip(feat_names, importances):
                feature_importance[fn] = round(float(imp), 4)

        # Save model artifact
        model_name = f"{algorithm}_{task_type}"
        model_filename = f"{model_name}_{user_id}.pkl"
        model_path = os.path.join(settings.MODEL_DIR, model_filename)

        with open(model_path, "wb") as f:
            pickle.dump({"model": model, "feature_names": list(X.columns), "task_type": task_type}, f)

        # Record in DB
        db_artifact = MLModelArtifact(
            user_id=user_id,
            name=f"{filename} - {algorithm}",
            task_type=task_type,
            algorithm=algorithm,
            accuracy_or_r2=round(score_val, 4),
            metrics_json=metrics,
            file_path=model_path
        )
        db.add(db_artifact)
        db.commit()
        db.refresh(db_artifact)

        _MODEL_CACHE[db_artifact.id] = {"model": model, "feature_names": list(X.columns), "task_type": task_type}

        return {
            "model_id": db_artifact.id,
            "model_name": db_artifact.name,
            "task_type": task_type,
            "algorithm": algorithm,
            "metrics": metrics,
            "feature_importance": feature_importance
        }

    @staticmethod
    def predict(db: Session, model_id: int, input_data: Dict[str, Any]) -> Any:
        if model_id not in _MODEL_CACHE:
            artifact = db.query(MLModelArtifact).filter(MLModelArtifact.id == model_id).first()
            if not artifact or not os.path.exists(artifact.file_path):
                raise ValueError("Model artifact not found.")
            with open(artifact.file_path, "rb") as f:
                _MODEL_CACHE[model_id] = pickle.load(f)

        cache = _MODEL_CACHE[model_id]
        model = cache["model"]
        feature_names = cache["feature_names"]

        # Build feature DataFrame matching trained columns
        df_input = pd.DataFrame([input_data])
        df_input = pd.get_dummies(df_input)
        df_aligned = df_input.reindex(columns=feature_names, fill_value=0)

        prediction = model.predict(df_aligned)
        return float(prediction[0]) if isinstance(prediction[0], (np.floating, float)) else str(prediction[0])

    @staticmethod
    def _instantiate_model(task_type: str, algorithm: str):
        algo_lower = algorithm.lower()
        if task_type == "classification":
            if "random_forest" in algo_lower:
                return RandomForestClassifier(n_estimators=100, random_state=42)
            elif "gradient" in algo_lower:
                return GradientBoostingClassifier(random_state=42)
            elif "tree" in algo_lower:
                return DecisionTreeClassifier(random_state=42)
            else:
                return LogisticRegression(max_iter=500, random_state=42)
        else: # regression
            if "random_forest" in algo_lower:
                return RandomForestRegressor(n_estimators=100, random_state=42)
            elif "gradient" in algo_lower:
                return GradientBoostingRegressor(random_state=42)
            elif "tree" in algo_lower:
                return DecisionTreeRegressor(random_state=42)
            else:
                return LinearRegression()
