"""
Insect Skill — 工具函数

桥接 insect.skill 知识库的查询函数。
当前使用 Mock 数据或直接读取 pest_ontology.json。
"""

import json
import os
from typing import List, Dict, Any, Optional


PEST_ONTOLOGY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "insect.skill", "data", "pest_ontology.json"
)

PEST_CARDS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "insect.skill", "data", "pest_cards"
)


def load_pest_ontology() -> List[Dict[str, Any]]:
    """加载害虫本体数据"""
    path = os.path.normpath(PEST_ONTOLOGY_PATH)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def query_pest_ontology(text: str, crop: str) -> List[Dict[str, Any]]:
    """根据文本和作物查询害虫本体"""
    ontology = load_pest_ontology()
    if not ontology:
        return []

    results = []
    text_lower = text.lower()
    crop_in_text = crop in text if crop else False

    for entry in ontology:
        score = 0
        # 中文名匹配
        if entry.get("name_cn", "") in text:
            score += 3
        # 寄主作物匹配
        if crop and crop in entry.get("major_hosts", []):
            score += 2
        if crop_in_text:
            score += 1
        # 症状匹配
        for symptom in entry.get("typical_symptoms", []):
            if any(kw in text for kw in symptom):
                score += 1

        if score > 0:
            entry["match_score"] = score
            results.append(entry)

    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return results[:5]


def query_pest_card(pest_id: str) -> Optional[Dict[str, Any]]:
    """查询害虫知识卡片"""
    # 优先查找正式卡片
    for ext in [".md"]:
        card_path = os.path.normpath(
            os.path.join(PEST_CARDS_DIR, f"{pest_id}{ext}")
        )
        if os.path.exists(card_path):
            # 简单读取 frontmatter
            try:
                with open(card_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # 提取 YAML frontmatter 中的关键信息
                name_cn = ""
                for line in content.split("\n"):
                    if line.startswith("  name_cn:"):
                        name_cn = line.split(":", 1)[1].strip().strip('"')
                        break
                return {"pest_id": pest_id, "name_cn": name_cn}
            except OSError:
                pass

    return None
