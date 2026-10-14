from pydantic import BaseModel, ConfigDict, Field

class ErrorRecoverySchema(BaseModel):
    error_type: str
    explanation: str
    corrected_code: str

    model_config = ConfigDict(extra="forbid", strict=True)

class CoderSchema(BaseModel):
    explanation: str
    code: str

    model_config = ConfigDict(extra="forbid", strict=True)

class MetricsSchema(BaseModel):
    train_rmse: float= Field(ge=0)
    test_rmse: float = Field(ge=0)

    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
