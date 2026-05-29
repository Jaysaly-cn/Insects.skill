"""
Plant Protection Agent — API Schema 定义

Pydantic 模型，用于请求/响应的序列化与校验。
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class DiagnosisRequest(BaseModel):
    user_input: str = Field(..., description="用户输入的文本")
    image_paths: List[str] = Field(default=[], description="图片路径列表")
    conversation_id: Optional[str] = Field(default=None, description="会话ID")
    user_id: Optional[str] = Field(default=None, description="用户ID")
    location: Optional[str] = Field(default=None, description="地区信息")


class EvidenceItem(BaseModel):
    source_id: Optional[str] = None
    title: Optional[str] = None
    snippet: Optional[str] = None


class CandidateDiagnosis(BaseModel):
    diagnosis: str = ""
    related_domains: List[str] = []
    confidence: float = 0.0
    supporting_evidence: List[str] = []
    conflicting_evidence: List[str] = []
    needs_followup: bool = False


class FinalDiagnosis(BaseModel):
    primary_conclusion: str = ""
    secondary_possibilities: List[str] = []
    confidence: float = 0.0
    certainty_label: str = ""
    key_evidence: List[str] = []
    limitations: List[str] = []
    next_best_actions: List[str] = []


class DiagnosisResponse(BaseModel):
    final_answer: str = ""
    final_diagnosis: Optional[FinalDiagnosis] = None
    candidate_diagnoses: List[CandidateDiagnosis] = []
    uncertainty_level: Optional[str] = None
    confidence: Optional[float] = None
    followup_questions: List[str] = []
    safety_warnings: List[str] = []
    evidence: List[EvidenceItem] = []
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
