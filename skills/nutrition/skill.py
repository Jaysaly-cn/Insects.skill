"""
Nutrition Skill — 营养诊断子 Skill

职责：
- 判断缺氮、缺磷、缺钾、缺镁、缺铁等营养问题
- 结合叶片部位、新老叶表现、叶脉间黄化等特征
- 与病害、药害、土壤问题区分
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import NUTRITION_KEYWORDS


# 缺素症状快速对照
NUTRIENT_SYMPTOMS = {
    "缺氮": ["老叶发黄", "植株矮小", "全株黄化"],
    "缺磷": ["叶片暗绿", "茎叶紫红", "根系不良"],
    "缺钾": ["老叶边缘焦枯", "叶脉间黄化", "茎秆柔弱"],
    "缺镁": ["叶脉间黄化", "老叶先显症", "叶脉保持绿色"],
    "缺铁": ["新叶黄化", "叶脉间失绿", "幼叶白化"],
    "缺锌": ["小叶丛生", "叶片簇生", "节间缩短"],
    "缺钙": ["新叶畸形", "生长点枯死", "果实脐腐"],
}


def run_nutrition_skill(state: PlantProtectionState) -> dict:
    """执行营养 Skill"""
    output = SkillOutput(domain="nutrition")
    text = state.get("user_input", "")

    if not any(kw in text for kw in NUTRITION_KEYWORDS):
        output.status = "skipped"
        return output.to_dict()

    # 尝试匹配缺素类型
    matched = []
    for nutrient, symptoms in NUTRIENT_SYMPTOMS.items():
        for sym in symptoms:
            if sym in text:
                matched.append(nutrient)
                break

    if matched:
        label = "+".join(set(matched))
    else:
        label = "缺素（待确定具体元素）"

    output.add_candidate(
        name=label,
        candidate_type="nutrition",
        confidence=0.5,
        evidence=[f"用户描述的症状与{label}相符"] if matched else ["用户提到了缺素相关描述"],
        against_evidence=["需排除病害和药害可能性", "缺乏土壤检测数据"],
        need_more_info=True,
        recommended_observations=[
            "确认是新叶还是老叶先出现症状",
            "记录叶片黄化形态（叶脉间/全叶/边缘）",
            "进行土壤养分检测",
            "回顾近期施肥记录",
        ],
    )

    output.status = "completed"
    return output.to_dict()
