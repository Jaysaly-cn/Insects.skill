"""
Plant Protection Agent — LangGraph 主图构建

编排所有节点和边，构成完整的植保诊断工作流。
支持多意图并发、多路由分发、综合诊断仲裁。

工作流：
START → Input Normalizer → Slot Extractor → Intent Router
  → [有图] Image Analyzer → Sufficiency Checker
  → [无图] Sufficiency Checker
  → [不足] Follow-up Generator → END
  → [充分] Domain Dispatcher → Comprehensive Reasoner
  → Diagnostic Arbiter → Safety Guard → Answer Formatter → END
"""

from langgraph.graph import StateGraph, END
from graph.state import PlantProtectionState

from graph.nodes.input_normalizer import input_normalizer
from graph.nodes.slot_extractor import slot_extractor
from graph.nodes.intent_router import intent_router
from graph.nodes.image_analyzer import image_analyzer
from graph.nodes.sufficiency_checker import sufficiency_checker
from graph.nodes.followup_generator import followup_generator
from graph.nodes.domain_dispatcher import domain_dispatcher
from graph.nodes.comprehensive_reasoner import comprehensive_reasoner
from graph.nodes.diagnostic_arbiter import diagnostic_arbiter
from graph.nodes.safety_guard import safety_guard
from graph.nodes.answer_formatter import answer_formatter

from graph.edges.conditions import after_intent, after_sufficiency


def build_plant_protection_graph() -> StateGraph:
    """构建并编译植保诊断 LangGraph"""

    graph = StateGraph(PlantProtectionState)

    # ==================== 添加节点 ====================
    graph.add_node("input_normalizer", input_normalizer)
    graph.add_node("slot_extractor", slot_extractor)
    graph.add_node("intent_router", intent_router)
    graph.add_node("image_analyzer", image_analyzer)
    graph.add_node("sufficiency_checker", sufficiency_checker)
    graph.add_node("followup_generator", followup_generator)
    graph.add_node("domain_dispatcher", domain_dispatcher)
    graph.add_node("comprehensive_reasoner", comprehensive_reasoner)
    graph.add_node("diagnostic_arbiter", diagnostic_arbiter)
    graph.add_node("safety_guard", safety_guard)
    graph.add_node("answer_formatter", answer_formatter)

    # ==================== 设置入口 ====================
    graph.set_entry_point("input_normalizer")

    # ==================== 顺序边 ====================
    graph.add_edge("input_normalizer", "slot_extractor")
    graph.add_edge("slot_extractor", "intent_router")

    # ==================== 条件边：是否有图片 ====================
    graph.add_conditional_edges(
        "intent_router",
        after_intent,
        {
            "yes": "image_analyzer",
            "no": "sufficiency_checker",
        },
    )

    # 图片分析后也进入充分性检查
    graph.add_edge("image_analyzer", "sufficiency_checker")

    # ==================== 条件边：是否需追问 ====================
    graph.add_conditional_edges(
        "sufficiency_checker",
        after_sufficiency,
        {
            "followup": "followup_generator",
            "dispatch": "domain_dispatcher",
        },
    )

    # 追问后结束本回合
    graph.add_edge("followup_generator", END)

    # ==================== 多 Skill 分发 → 综合推理 → 仲裁 → 安全 → 格式化 ====================
    graph.add_edge("domain_dispatcher", "comprehensive_reasoner")
    graph.add_edge("comprehensive_reasoner", "diagnostic_arbiter")
    graph.add_edge("diagnostic_arbiter", "safety_guard")
    graph.add_edge("safety_guard", "answer_formatter")
    graph.add_edge("answer_formatter", END)

    # ==================== 编译 ====================
    return graph.compile()
