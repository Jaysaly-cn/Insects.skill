"""
Diagnostic Arbiter — 诊断仲裁节点

职责：
从候选诊断列表中形成最终诊断策略：
1. 主因是什么（primary）
2. 次因是什么（secondary）
3. 哪些因素需要排除
4. 是否可以给出诊断/只能给出候选
5. 是否需要再次追问
6. 是否可以给出防控建议
"""

from graph.state import PlantProtectionState
from typing import Dict, Any


def diagnostic_arbiter(state: PlantProtectionState) -> PlantProtectionState:
    """从候选列表中仲裁最终诊断"""
    candidates = state.get("candidate_diagnoses", [])
    need_followup = state.get("need_followup", False)

    if not candidates:
        state["final_diagnosis"] = {
            "primary_conclusion": "信息不足，无法做出诊断",
            "secondary_possibilities": [],
            "confidence": 0.0,
            "certainty_label": "insufficient",
            "key_evidence": [],
            "limitations": ["缺少足够的诊断信息"],
            "next_best_actions": ["请补充作物、症状和图片信息"],
        }
        state["uncertainty_level"] = "insufficient"
        state["confidence"] = 0.0
        return state

    # 取置信度最高的候选为主诊断
    top = candidates[0]
    remaining = candidates[1:3] if len(candidates) > 1 else []

    # 确定不确定等级
    confidence = top.get("confidence", 0.0)
    if need_followup:
        certainty_label = "insufficient"
    elif confidence >= 0.7:
        certainty_label = "low"
    elif confidence >= 0.4:
        certainty_label = "medium"
    else:
        certainty_label = "high"

    limitations = []
    for cand in candidates:
        limitations.extend(cand.get("conflicting_evidence", []))

    state["final_diagnosis"] = {
        "primary_conclusion": top.get("diagnosis", "未确定"),
        "secondary_possibilities": [
            r.get("diagnosis", "") for r in remaining
        ],
        "confidence": confidence,
        "certainty_label": certainty_label,
        "key_evidence": top.get("supporting_evidence", []),
        "limitations": limitations[:5],
        "next_best_actions": [
            "补充作物和症状信息",
            "拍摄受害部位和虫体近照",
            "记录近期农事操作",
        ],
    }
    state["uncertainty_level"] = certainty_label
    state["confidence"] = confidence

    return state
