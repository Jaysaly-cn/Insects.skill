"""
Slot Extractor — 诊断槽位抽取节点

职责：
从用户输入中抽取植保诊断所需的通用槽位：
- 作物、地区、季节、生育期
- 受害部位、症状
- 是否看到虫、虫态/形态
- 用药史、施肥史、灌溉史、土壤状况、田间分布

Mock 实现：使用关键词简单匹配，后续替换为 LLM 调用。
"""

import re
from graph.state import PlantProtectionState


CROP_KEYWORDS = [
    "水稻", "小麦", "玉米", "大豆", "花生", "棉花", "油菜",
    "番茄", "辣椒", "茄子", "黄瓜", "西瓜", "南瓜", "冬瓜",
    "白菜", "萝卜", "菠菜", "生菜", "芹菜", "韭菜", "葱", "蒜",
    "苹果", "梨", "桃", "葡萄", "柑橘", "香蕉", "荔枝", "芒果",
    "茶叶", "烟草", "甘蔗", "马铃薯", "甘薯",
]


def slot_extractor(state: PlantProtectionState) -> PlantProtectionState:
    """从 user_input 中抽取诊断槽位"""
    text = state.get("user_input", "")

    # 作物
    for crop in CROP_KEYWORDS:
        if crop in text:
            state["crop"] = crop
            break

    # 地区
    region_keywords = [
        "浙江", "江苏", "安徽", "福建", "江西", "湖南", "湖北",
        "广东", "广西", "海南", "四川", "云南", "贵州", "山东",
        "河南", "河北", "山西", "陕西", "甘肃", "辽宁", "吉林",
        "黑龙江", "内蒙古", "新疆", "西藏",
    ]
    for kw in region_keywords:
        if kw in text:
            state["region"] = kw
            break

    # 季节
    for kw in ["春", "夏", "秋", "冬"]:
        if kw in text:
            state["season"] = f"{kw}季"
            break

    # 受害部位
    part_map = {"叶": "leaf", "茎": "stem", "根": "root", "果": "fruit",
                "花": "flower", "穗": "seed", "苗": "seedling"}
    parts = []
    for cn, en in part_map.items():
        if cn in text:
            parts.append(en)
    if parts:
        state["damaged_parts"] = parts

    # 症状
    symptoms = []
    symptom_indicators = ["枯", "黄", "萎", "斑", "霉", "腐", "烂",
                          "卷", "缩", "矮", "畸", "裂", "孔", "洞"]
    for ind in symptom_indicators:
        idx = text.find(ind)
        if idx >= 0:
            start = max(0, idx - 5)
            end = min(len(text), idx + 6)
            snippet = text[start:end].strip()
            if snippet not in symptoms:
                symptoms.append(snippet)
    if symptoms:
        state["symptoms"] = symptoms

    # 虫害检测
    for kw in ["虫", "害虫", "幼虫", "成虫"]:
        if kw in text:
            state["pest_seen"] = True
            break

    # 用药史
    for kw in ["打药", "喷药", "施药", "农药"]:
        if kw in text:
            state["pesticide_history"] = text[:50] + "..."
            break

    return state
