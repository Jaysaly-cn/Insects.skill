"""
Insect Skill — Prompt 模板

后续 LLM 模式下使用的 Prompt，当前 Mock 模式未使用。
"""

INSECT_SKILL_PROMPT = """你是一个农业昆虫学专家。
请根据以下信息进行害虫诊断分析：

作物：{crop}
症状：{symptoms}
地区：{region}
季节：{season}
虫体描述：{morphology}
图片观察：{image_obs}

请输出结构化JSON：
{{
  "candidates": [
    {{
      "name": "害虫中文名",
      "name_latin": "拉丁学名",
      "confidence": 0.0-1.0,
      "evidence": ["支持证据"],
      "against_evidence": ["不支持证据"],
      "need_more_info": true/false,
      "recommended_observations": ["建议补充观察"]
    }}
  ]
}}
"""
