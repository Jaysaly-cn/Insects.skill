"""
Plant Protection Agent — 路由策略

定义 Intent Router 的领域判断规则和 Domain Dispatcher 的 Skill 调度策略。
当前使用关键词匹配 Mock 逻辑，后续应替换为 LLM 调用。
"""

from graph.state import PlantProtectionState


# ==================== 领域关键词规则 ====================

INSECT_KEYWORDS = [
    "虫", "害虫", "幼虫", "成虫", "若虫", "蛹", "卵块",
    "蛀", "咬", "啃", "刺吸", "飞虱", "叶蝉", "螟", "蛾",
    "蝶", "蝇", "蚊", "甲虫", "蜂", "蚜虫", "粉虱", "蓟马",
    "红蜘蛛", "螨", "钻心", "枯心", "枯鞘", "白穗",
    "食叶", "卷叶", "潜叶", "虫伤", "虫粪",
]

DISEASE_KEYWORDS = [
    "病斑", "霉", "腐烂", "病毒", "菌", "锈",
    "萎蔫", "猝倒", "立枯", "炭疽", "疫病", "白粉",
    "霜霉", "叶枯", "条斑", "环斑", "花叶", "矮缩",
    "坏死", "溃疡", "穿孔", "斑点", "病",
    "粉状", "霉层", "腐烂",
    "发黄", "卷曲", "枯",
]

WEED_KEYWORDS = [
    "杂草", "草害", "除草", "禾草", "阔叶草", "莎草",
    "稗草", "千金子", "牛筋草", "马唐", "香附子",
]

PESTICIDE_KEYWORDS = [
    "农药", "杀虫剂", "杀菌剂", "除草剂", "药剂",
    "有效成分", "作用机制", "登记", "安全间隔期",
    "抗药性", "轮换用药", "剂型",
    "可以治", "用什么药", "打什么药",
]

PESTICIDE_INJURY_KEYWORDS = [
    "药害", "打药后", "喷药后", "药斑", "药烧",
    "施药后出现", "农药伤害", "打药", "打了",
    "打完", "打过药",
]

SOIL_KEYWORDS = [
    "土壤", "板结", "盐渍", "酸化", "碱化", "排水",
    "根系", "根腐", "沤根", "根部", "根际",
]

NUTRITION_KEYWORDS = [
    "缺素", "缺氮", "缺磷", "缺钾", "缺镁", "缺铁",
    "缺锌", "缺钙", "叶脉间黄化", "老叶发黄",
    "新叶发黄", "营养不良", "叶脉", "缺绿",
    "矮小", "变小",
]


def detect_domains(text: str) -> list:
    """根据用户输入文本检测涉及的领域（多意图支持）

    Args:
        text: 用户输入文本

    Returns:
        匹配到的领域列表，按匹配度排序
    """
    if not text:
        return ["comprehensive"]

    domains = []

    if any(kw in text for kw in INSECT_KEYWORDS):
        domains.append("insect")
    if any(kw in text for kw in DISEASE_KEYWORDS):
        domains.append("disease")
    if any(kw in text for kw in WEED_KEYWORDS):
        domains.append("weed")
    if any(kw in text for kw in PESTICIDE_KEYWORDS):
        domains.append("pesticide")
    if any(kw in text for kw in PESTICIDE_INJURY_KEYWORDS):
        domains.append("pesticide_injury")
    if any(kw in text for kw in SOIL_KEYWORDS):
        domains.append("soil")
    if any(kw in text for kw in NUTRITION_KEYWORDS):
        domains.append("nutrition")

    if not domains:
        domains = ["comprehensive"]

    return domains


def get_dispatcher_domains(state: PlantProtectionState) -> list:
    """获取 Domain Dispatcher 需要调用的 Skill 列表"""
    return state.get("all_domains", ["comprehensive"])
