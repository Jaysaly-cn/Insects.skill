"""
Comprehensive Reasoner — 综合推理节点

职责：
在多个子 Skill 返回结果后，进行综合思考和交叉比对。
汇总各 Skill 的候选、证据、冲突信息，形成候选诊断列表。
"""

from graph.state import PlantProtectionState
from typing import Dict, Any, List


def comprehensive_reasoner(state: PlantProtectionState) -> PlantProtectionState:
    """汇总多 Skill 结果，生成候选诊断列表"""
    candidates = []

    # 收集各 Skill 的候选人
    skill_results = {
        "insect": state.get("insect_result"),
        "disease": state.get("disease_result"),
        "weed": state.get("weed_result"),
        "pesticide": state.get("pesticide_result"),
        "pesticide_injury": state.get("pesticide_injury_result"),
        "soil": state.get("soil_result"),
        "nutrition": state.get("nutrition_result"),
        "comprehensive": state.get("comprehensive_result"),
    }

    for domain, result in skill_results.items():
        if not result:
            continue

        candidates_list = result.get("candidates", [])
        for cand in candidates_list:
            entry = {
                "diagnosis": cand.get("name", f"{domain}相关"),
                "related_domains": [domain],
                "confidence": cand.get("confidence", 0.0),
                "supporting_evidence": cand.get("evidence", []),
                "conflicting_evidence": cand.get("against_evidence", []),
                "needs_followup": cand.get("need_more_info", False),
            }
            candidates.append(entry)

    # 如果没有候选人，创建一个综合兜底
    if not candidates:
        candidates.append({
            "diagnosis": "需要更多信息进行综合诊断",
            "related_domains": list(skill_results.keys()),
            "confidence": 0.1,
            "supporting_evidence": ["当前信息不足以生成具体诊断"],
            "conflicting_evidence": [],
            "needs_followup": True,
        })

    # 按置信度排序
    candidates.sort(key=lambda x: x["confidence"], reverse=True)

    state["candidate_diagnoses"] = candidates

    return state
