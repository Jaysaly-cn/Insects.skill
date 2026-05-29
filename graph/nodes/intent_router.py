"""
Intent Router — 意图识别与多意图路由节点

职责：
1. 识别用户问题属于哪些植保子领域
2. 支持多意图输出（primary_domain + secondary_domains）
3. 判断是否需要多 Skill 并发

输出格式：
{
  "task_type": "diagnosis",
  "primary_domain": "insect",
  "secondary_domains": ["disease", "pesticide_injury"],
  "all_domains": ["insect", "disease", "pesticide_injury"],
  "need_multi_skill": true
}

Mock 实现：使用关键词匹配，后续替换为 LLM。
"""

from graph.state import PlantProtectionState
from graph.edges.routing_rules import detect_domains


def intent_router(state: PlantProtectionState) -> PlantProtectionState:
    """识别用户意图并填充路由信息"""
    text = state.get("user_input", "")
    domains = detect_domains(text)

    state["primary_domain"] = domains[0] if domains else "comprehensive"

    if len(domains) > 1:
        state["secondary_domains"] = domains[1:]
    else:
        state["secondary_domains"] = []

    state["all_domains"] = domains
    state["need_multi_skill"] = len(domains) > 1
    state["route_confidence"] = 0.7 if domains else 0.3

    # 任务类型
    if any(kw in text for kw in ["诊断", "什么病", "什么虫", "怎么回事", "为害"]):
        state["task_type"] = "diagnosis"
    elif any(kw in text for kw in ["防治", "用药", "打什么药", "怎么治", "防控"]):
        state["task_type"] = "control_advice"
    elif any(kw in text for kw in ["是什么", "识别", "鉴定"]):
        state["task_type"] = "identification"
    elif any(kw in text for kw in ["介绍", "什么是", "科普"]):
        state["task_type"] = "knowledge_query"
    else:
        state["task_type"] = "diagnosis"

    return state
