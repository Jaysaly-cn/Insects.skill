#!/usr/bin/env python3
"""
Intent Evaluation — 意图识别评测脚本

评测方法：
1. 读取 test_cases/text_cases.jsonl 和 multi_intent_cases.jsonl
2. 对每条用例调用 intent_router 节点
3. 对比输出与 expected 中的 domains 列表
4. 计算主意图准确率和次意图召回率
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from graph.nodes.intent_router import intent_router


def evaluate():
    cases_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "text_cases.jsonl")
    multi_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "multi_intent_cases.jsonl")

    total = 0
    correct = 0
    multi_total = 0
    multi_correct = 0

    for path in [cases_path, multi_path]:
        if not os.path.exists(path):
            print(f"[SKIP] {path} not found")
            continue

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                case = json.loads(line)
                total += 1

                state = {"user_input": case["input"], "all_domains": [], "secondary_domains": []}
                result = intent_router(state)

                expected_domains = case["expected"].get("domains", [case["expected"].get("domain", "")])
                predicted_domains = result.get("all_domains", [])

                if set(predicted_domains) == set(expected_domains):
                    correct += 1
                else:
                    print(f"  FAIL id={case['id']}: expected {expected_domains}, got {predicted_domains}")

                if case.get("expected", {}).get("need_multi_skill"):
                    multi_total += 1
                    if result.get("need_multi_skill"):
                        multi_correct += 1

    print(f"\n=== Intent Eval Results ===")
    print(f"Total cases: {total}")
    print(f"Domain accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    if multi_total:
        print(f"Multi-intent recall: {multi_correct}/{multi_total} ({multi_correct/multi_total*100:.1f}%)")


if __name__ == "__main__":
    evaluate()
