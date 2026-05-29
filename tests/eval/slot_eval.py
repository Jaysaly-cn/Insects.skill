#!/usr/bin/env python3
"""
Slot Extraction Evaluation — 槽位抽取评测脚本
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from graph.nodes.slot_extractor import slot_extractor


def evaluate():
    cases_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "text_cases.jsonl")
    total = 0
    correct = 0

    if not os.path.exists(cases_path):
        print("[SKIP] test cases not found")
        return

    with open(cases_path, "r", encoding="utf-8") as f:
        for line in f:
            case = json.loads(line)
            total += 1
            state = {"user_input": case["input"]}
            result = slot_extractor(state)

            expected = case["expected"]
            ok = True

            for key in ["crop", "pest_seen", "pesticide_history"]:
                if key in expected:
                    if result.get(key) != expected[key]:
                        print(f"  FAIL id={case['id']} slot={key}: expected {expected[key]}, got {result.get(key)}")
                        ok = False

            if ok:
                correct += 1

    print(f"\n=== Slot Eval Results ===")
    print(f"Total: {total}, Correct: {correct} ({correct/total*100:.1f}%)")


if __name__ == "__main__":
    evaluate()
