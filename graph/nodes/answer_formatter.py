"""
Answer Formatter — 回答格式化节点

职责：
将最终诊断、安全提示、证据和追问整理为用户可读的结构化回答。
面向农技人员的标准输出格式。
"""

from graph.state import PlantProtectionState


def answer_formatter(state: PlantProtectionState) -> PlantProtectionState:
    """生成最终格式化回答"""
    final_diag = state.get("final_diagnosis", {}) or {}
    candidates = state.get("candidate_diagnoses", [])
    followup_qs = state.get("followup_questions", [])
    warnings = state.get("safety_warnings", [])
    uncertainty = state.get("uncertainty_level", "insufficient")

    # 如果还在追问阶段，输出追问
    if followup_qs and state.get("need_followup"):
        lines = [
            "## 需要补充信息",
            "",
            "目前的信息还不足以做高置信判断。请补充以下信息：",
            "",
        ]
        for i, q in enumerate(followup_qs, 1):
            lines.append(f"{i}. {q}")
        lines.append("")
        lines.append("补充信息后，我可以为您做更准确的诊断。")
        state["final_answer"] = "\n".join(lines)
        state["answer_format"] = "followup"
        return state

    # 构建标准诊断回答
    primary = final_diag.get("primary_conclusion", "待确定")
    secondary = final_diag.get("secondary_possibilities", [])
    key_evidence = final_diag.get("key_evidence", [])
    limitations = final_diag.get("limitations", [])
    confidence = final_diag.get("confidence", 0.0)

    lines = [
        "## 1. 初步判断",
        "",
        f"根据当前信息，较可能为：**{primary}**。",
        "",
        f"置信度：{_confidence_label(uncertainty)}（{confidence:.0%}）",
        "",
    ]

    # 次要可能
    if secondary:
        lines.append("### 需要排除的可能")
        lines.append("")
        for s in secondary:
            if s:
                lines.append(f"- {s}")
        lines.append("")

    # 关键依据
    if key_evidence:
        lines.append("## 2. 关键依据")
        lines.append("")
        for ev in key_evidence:
            lines.append(f"- {ev}")
        lines.append("")

    # 局限性
    if limitations:
        lines.append("## 3. 当前局限性")
        lines.append("")
        for lim in limitations:
            lines.append(f"- {lim}")
        lines.append("")

    lines.append("## 4. 建议补充的信息")
    lines.append("")
    lines.append("- 补充受害部位和症状的近照")
    lines.append("- 记录近期农事操作（用药、施肥、灌溉等）")
    lines.append("- 调查田间分布和发生范围")
    lines.append("")

    lines.append("## 5. 综合防控建议")
    lines.append("")
    lines.append("- 优先进行监测和确认，不要急于用药")
    lines.append("- 结合农业防治（轮作、清园、抗性品种）")
    lines.append("- 结合物理防治（灯光诱杀、色板）")
    lines.append("- 结合生物防治（天敌保护、微生物农药）")
    lines.append("- 达到当地防治指标后，再考虑化学防治")
    lines.append("")

    lines.append("## 6. 用药与安全提示")
    lines.append("")
    lines.append("> 如需用药，应以当地植保部门建议和农药标签为准，确认登记作物、")
    lines.append("> 防治对象、安全间隔期和使用方法。当前不建议在诊断未确认前直接用药。")
    lines.append("> 注意药剂轮换，延缓抗药性发展。")
    lines.append("")

    # 安全警告
    for w in warnings:
        lines.append(f"> ⚠️ {w}")
    if warnings:
        lines.append("")

    # 参考
    lines.append("---")
    lines.append("*本诊断基于当前提供的信息生成。补充更多信息后可提高诊断准确性。*")

    state["final_answer"] = "\n".join(lines)
    state["answer_format"] = "concise"

    return state


def _confidence_label(level: str) -> str:
    mapping = {
        "high": "高",
        "medium": "中",
        "low": "低",
        "insufficient": "信息不足",
    }
    return mapping.get(level, level)
