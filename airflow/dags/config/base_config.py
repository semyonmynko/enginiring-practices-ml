from typing import Literal, Optional

from pydantic import BaseModel, Field, validator


class ModelConfig(BaseModel):
    algorithm: Literal["RandomForest", "GradientBoosting", "LogisticRegression"]
    n_estimators: Optional[int] = None
    max_depth: Optional[int] = None
    learning_rate: Optional[float] = None

    @validator("n_estimators", always=True)
    def check_estimators(cls, v, values):
        if values["algorithm"] in ["RandomForest", "GradientBoosting"] and v is None:
            raise ValueError("n_estimators must be set for ensemble algorithms.")
        return v


class DatasetConfig(BaseModel):
    test_size: float = Field(..., ge=0.05, le=0.5)
    random_state: int = 42


class FullConfig(BaseModel):
    model: ModelConfig
    dataset: DatasetConfig
