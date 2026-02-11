from typing import TypedDict, List
from pydantic import BaseModel, Field, ValidationError
from typing import Literal

# -------------------------
# Input Schemas
# -------------------------

class TestMetrics(BaseModel):
    total: int = Field(..., ge=0)
    passed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)


class CoverageMetrics(BaseModel):
    percent: float = Field(..., ge=0, le=100)
    threshold: float = Field(..., ge=0, le=100)


class AnalysisInput(BaseModel):
    tests: TestMetrics
    coverage: CoverageMetrics

# -------------------------
# Output Schemas
# -------------------------

class QualitySummary(BaseModel):
    test_status: Literal["PASS", "FAIL"]
    coverage_status: Literal["PASS", "FAIL"]
    overall_status: Literal["PASS", "FAIL"]


class QualityMetrics(BaseModel):
    total_tests: int
    passed: int
    failed: int
    coverage_percent: float
    coverage_threshold: float


class Recommendation(BaseModel):
    message: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]


class AnalysisOutput(BaseModel):
    summary: QualitySummary
    metrics: QualityMetrics
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    recommendations: List[Recommendation] = []

class AIInsight(BaseModel):
    executive_summary: str
    risk_explanation: str
    improvement_suggestions: List[str]    
