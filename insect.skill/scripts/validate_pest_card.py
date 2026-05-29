#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_pest_card.py — Validate a pest knowledge card markdown file.

Usage:
    python scripts/validate_pest_card.py <path/to/pest_card.md>

Checks:
    1. YAML frontmatter exists and is parseable
    2. pest_id is not empty
    3. status is one of: draft, reviewed, deprecated
    4. Required sections are present
    5. No risky language patterns (e.g. "一定是", "保证防治")
    6. No suspected dosage expressions (e.g. "毫升/亩", "倍液")

Exits with code 0 if all checks pass, 1 if errors found.
"""

import re
import sys
import os


# Required section headings (case-insensitive partial match)
REQUIRED_SECTIONS = [
    "基本信息",
    "形态识别特征",
    "危害症状",
    "发生规律",
    "诊断要点",
    "相似害虫鉴别",
    "田间调查建议",
    "综合防控原则",
    "不确定性与注意事项",
    "参考来源",
]

# Risky language patterns — flag as errors
RISKY_PATTERNS = [
    (r"一定是", "RISKY_ASSERTION: '一定是' found — avoid absolute certainty claims"),
    (r"必然是", "RISKY_ASSERTION: '必然是' found — avoid absolute certainty claims"),
    (r"保证防治", "RISKY_ASSERTION: '保证防治' found — avoid guaranteeing control efficacy"),
    (r"完全消灭", "RISKY_ASSERTION: '完全消灭' found — avoid claims of complete eradication"),
    (r"无需进一步确认", "RISKY_ASSERTION: '无需进一步确认' found — always leave room for verification"),
    (r"确定为", "RISKY_ASSERTION: '确定为' found — prefer qualified language (e.g. '鉴定为', '判断为')"),
]

# Suspected dosage patterns — flag as warnings
DOSAGE_PATTERNS = [
    (r"\d+\s*毫升\s*/\s*亩", "DOSAGE_WARNING: suspected dosage expression (ml/mu)"),
    (r"\d+\s*克\s*/\s*亩", "DOSAGE_WARNING: suspected dosage expression (g/mu)"),
    (r"\d+\s*倍液", "DOSAGE_WARNING: suspected dosage expression (倍液)"),
    (r"\d+\s*ml\s*/\s*(亩|mu|ha)", "DOSAGE_WARNING: suspected dosage expression"),
    (r"\d+\s*g\s*/\s*(亩|mu|ha)", "DOSAGE_WARNING: suspected dosage expression"),
]


def extract_frontmatter(text: str):
    """Extract YAML frontmatter between --- delimiters.

    Returns (frontmatter_dict, error_message).
    """
    # Match YAML frontmatter between --- lines
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return None, "ERROR: No YAML frontmatter found (expected between --- delimiters)."

    yaml_text = match.group(1)
    frontmatter = {}
    for line in yaml_text.split("\n"):
        # Simple key: value parser for flat YAML (no nesting)
        kv_match = re.match(r'^(\w[\w_]*)\s*:\s*(.*)', line)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip().strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter, None


def check_frontmatter(fm: dict) -> list:
    """Check frontmatter for required fields and valid values.

    Returns list of error/warning strings.
    """
    issues = []

    if not fm:
        return issues  # Already reported as error above

    # pest_id
    pest_id = fm.get("pest_id", "")
    if not pest_id:
        issues.append("ERROR: pest_id is empty in frontmatter.")

    # status
    status = fm.get("status", "")
    valid_status = {"draft", "reviewed", "deprecated"}
    if status not in valid_status:
        issues.append(
            f"ERROR: status '{status}' is invalid. Must be one of: {valid_status}."
        )

    return issues


def check_sections(text: str) -> list:
    """Check that all required sections are present in the markdown body.

    Returns list of error strings.
    """
    issues = []
    for section in REQUIRED_SECTIONS:
        # Look for a markdown heading containing the section name
        pattern = re.compile(
            r"^#{1,3}\s+.*" + re.escape(section) + r".*$",
            re.MULTILINE | re.IGNORECASE
        )
        if not pattern.search(text):
            issues.append(f"ERROR: Required section not found: '{section}'")
    return issues


def check_risky_patterns(text: str) -> list:
    """Scan for risky language patterns.

    Returns list of error/warning strings.
    """
    issues = []
    for pattern, message in RISKY_PATTERNS:
        if re.search(pattern, text):
            issues.append(f"ERROR: {message}")
    return issues


def check_dosage_patterns(text: str) -> list:
    """Scan for suspected dosage expressions.

    Returns list of warning strings.
    """
    issues = []
    for pattern, message in DOSAGE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(f"WARNING: {message}")
    return issues


def validate_file(filepath: str) -> tuple:
    """Run all checks on a pest card file.

    Returns (errors, warnings) where each is a list of strings.
    """
    if not os.path.exists(filepath):
        return (["ERROR: File not found: " + filepath], [])

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    errors = []
    warnings = []

    # Check 1: YAML frontmatter
    fm, fm_error = extract_frontmatter(text)
    if fm_error:
        errors.append(fm_error)
    else:
        errors.extend(check_frontmatter(fm))

    # Check 2: Required sections
    errors.extend(check_sections(text))

    # Check 3: Risky patterns
    errors.extend(check_risky_patterns(text))

    # Check 4: Dosage patterns (warnings, not errors)
    warnings.extend(check_dosage_patterns(text))

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_pest_card.py <path/to/pest_card.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    errors, warnings = validate_file(filepath)

    if errors:
        print(f"Validation FAILED for: {filepath}")
        print(f"  {len(errors)} error(s), {len(warnings)} warning(s)")
        print("-" * 50)
        for e in errors:
            print(f"  {e}")
        if warnings:
            print("-" * 50)
            for w in warnings:
                print(f"  {w}")
        print("-" * 50)
        sys.exit(1)
    else:
        print(f"Validation PASSED for: {filepath}")
        if warnings:
            print(f"  {len(warnings)} warning(s):")
            for w in warnings:
                print(f"  {w}")
        else:
            print("  No issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
