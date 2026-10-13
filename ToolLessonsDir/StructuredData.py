from pydantic import BaseModel, ConfigDict

class ErrorRecoverySchema(BaseModel):
    error_type: str
    explanation: str
    corrected_code: str

    model_config = ConfigDict(extra="forbid", strict=True)

class CoderSchema(BaseModel):
    explanation: str
    code: str

    model_config = ConfigDict(extra="forbid", strict=True)
