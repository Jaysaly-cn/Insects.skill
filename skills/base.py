"""
Skill Base — 子 Skill 基类与统一协议

所有子 Skill 必须遵守此协议：
- 输入：接收 PlantProtectionState（完整 State，只读自己需要的字段）
- 输出：结构化 JSON（统一 candidates 格式）
- 不直接生成最终回答，只返回候选和分析结果
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from graph.state import PlantProtectionState


class SkillOutput:
    """Skill 统一输出结构"""

    def __init__(self, domain: str):
        self.domain = domain
        self.status: str = "completed"
        self.candidates: List[Dict[str, Any]] = []
        self.retrieved_evidence: List[Dict[str, Any]] = []
        self.risk_notes: List[str] = []
        self.followup_questions: List[str] = []

    def add_candidate(
        self,
        name: str,
        candidate_type: str = "pest",
        confidence: float = 0.0,
        evidence: Optional[List[str]] = None,
        against_evidence: Optional[List[str]] = None,
        need_more_info: bool = False,
        recommended_observations: Optional[List[str]] = None,
    ):
        """添加一个候选诊断对象"""
        cand = {
            "name": name,
            "type": candidate_type,
            "confidence": confidence,
            "evidence": evidence or [],
            "against_evidence": against_evidence or [],
            "need_more_info": need_more_info,
            "recommended_observations": recommended_observations or [],
        }
        self.candidates.append(cand)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "status": self.status,
            "candidates": self.candidates,
            "retrieved_evidence": self.retrieved_evidence,
            "risk_notes": self.risk_notes,
            "followup_questions": self.followup_questions,
        }


class BaseSkill(ABC):
    """Skill 抽象基类"""

    def __init__(self, domain: str):
        self.domain = domain

    @abstractmethod
    def run(self, state: PlantProtectionState) -> SkillOutput:
        """执行 Skill 诊断逻辑"""
        ...

    def __call__(self, state: PlantProtectionState) -> Dict[str, Any]:
        result = self.run(state)
        return result.to_dict()
