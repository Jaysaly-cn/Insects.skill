"""
Plant Protection Agent — API 路由

提供 REST API 接口，接收用户诊断请求并返回结构化结果。
当前为骨架，使用 Mock 节点。
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Plant Protection Agent API", version="0.1.0")


class DiagnosisRequest(BaseModel):
    """诊断请求体"""
    user_input: str
    image_paths: List[str] = []
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    location: Optional[str] = None


class DiagnosisResponse(BaseModel):
    """诊断响应体"""
    final_answer: str
    confidence: Optional[str] = None
    followup_questions: List[str] = []
    safety_warnings: List[str] = []


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(req: DiagnosisRequest):
    """执行植保诊断"""
    from graph.build_graph import build_plant_protection_graph
    from graph.state import PlantProtectionState

    initial_state: PlantProtectionState = {
        "user_input": req.user_input,
        "image_paths": req.image_paths,
        "conversation_id": req.conversation_id or "",
        "user_id": req.user_id,
        "location": req.location,
        "all_domains": [],
        "secondary_domains": [],
        "damaged_parts": [],
        "symptoms": [],
        "insect_morphology": [],
        "disease_signs": [],
        "image_observations": [],
        "visual_candidates": [],
        "missing_slots": [],
        "critical_missing_slots": [],
        "followup_questions": [],
        "candidate_diagnoses": [],
        "safety_warnings": [],
        "unsafe_expressions": [],
        "retrieved_docs": [],
    }

    app_graph = build_plant_protection_graph()
    try:
        result = app_graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return DiagnosisResponse(
        final_answer=result.get("final_answer", ""),
        confidence=result.get("uncertainty_level"),
        followup_questions=result.get("followup_questions", []),
        safety_warnings=result.get("safety_warnings", []),
    )
