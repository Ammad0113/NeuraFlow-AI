import io
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

class ExcelService:
    @staticmethod
    def inspect_dataset(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        df = ExcelService._load_dataframe(file_bytes, filename)
        
        duplicates_count = int(df.duplicated().sum())
        missing_dict = {str(col): int(df[col].isna().sum()) for col in df.columns}
        
        # Summary statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        stats = {}
        if numeric_cols:
            describe_df = df[numeric_cols].describe().to_dict()
            for col in numeric_cols:
                mean_val = describe_df[col].get("mean", 0)
                std_val = describe_df[col].get("std", 0)
                min_val = describe_df[col].get("min", 0)
                max_val = describe_df[col].get("max", 0)

                stats[str(col)] = {
                    "mean": round(float(mean_val), 2) if pd.notna(mean_val) else 0.0,
                    "std": round(float(std_val), 2) if pd.notna(std_val) else 0.0,
                    "min": round(float(min_val), 2) if pd.notna(min_val) else 0.0,
                    "max": round(float(max_val), 2) if pd.notna(max_val) else 0.0
                }

        # Generate AI Data Insights
        insights = []
        if duplicates_count > 0:
            insights.append(f"Detected {duplicates_count} duplicate row(s) that should be purged.")
        total_missing = sum(missing_dict.values())
        if total_missing > 0:
            insights.append(f"Found {total_missing} missing entry/entries across dataset columns.")
        else:
            insights.append("Dataset has zero missing values. Clean structural integrity!")
        if numeric_cols:
            insights.append(f"Identified {len(numeric_cols)} quantitative column(s): {', '.join(numeric_cols[:3])}.")
        if len(df) > 100:
            insights.append(f"Robust dataset size with {len(df)} records ready for ML model training.")

        # Clean NaNs in preview data for JSON serialization safety
        df_preview = df.head(10).replace({np.nan: None})

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": [str(c) for c in df.columns],
            "missing_values": missing_dict,
            "duplicates_count": duplicates_count,
            "summary_stats": stats,
            "ai_insights": insights,
            "preview_data": df_preview.to_dict(orient="records")
        }

    @staticmethod
    def clean_dataset(file_bytes: bytes, filename: str, remove_duplicates: bool = True, fill_missing_numeric: str = "mean", fill_missing_text: str = "Unknown") -> Tuple[bytes, str]:
        df = ExcelService._load_dataframe(file_bytes, filename)

        if remove_duplicates:
            df = df.drop_duplicates()

        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        text_cols = df.select_dtypes(include=['object', 'category']).columns

        for col in numeric_cols:
            if fill_missing_numeric == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif fill_missing_numeric == "median":
                df[col] = df[col].fillna(df[col].median())
            elif fill_missing_numeric == "zero":
                df[col] = df[col].fillna(0)

        for col in text_cols:
            df[col] = df[col].fillna(fill_missing_text)

        out_buffer = io.BytesIO()
        cleaned_filename = f"cleaned_{filename}"
        if filename.endswith(".csv"):
            df.to_csv(out_buffer, index=False)
        else:
            df.to_excel(out_buffer, index=False)

        return out_buffer.getvalue(), cleaned_filename

    @staticmethod
    def _load_dataframe(file_bytes: bytes, filename: str) -> pd.DataFrame:
        if filename.endswith(".csv"):
            return pd.read_csv(io.BytesIO(file_bytes))
        else:
            return pd.read_excel(io.BytesIO(file_bytes))
