---
name: pest-card-builder
description: >
  Build a standardized pest knowledge card from user-supplied source material
  (PDF, plain text, paper excerpt, official guideline). Executes the full
  insect.skill injection pipeline: source registration → fact extraction →
  entity normalization → draft card generation → auto-validation → review gate.
  Always pauses before committing to the knowledge base. Part of insect.skill;
  depends on its protocols/, templates/, schemas/, scripts/.
  Trigger: "build a pest card", "generate knowledge card", "process this source",
  "注入知识卡片", or when user pastes pest-related source text with a build request.
---

# Pest Card Builder

Source → validated draft pest card. **Stop at Stage 6; await user approval
before Stage 7.**

Flow: `Register source → Extract facts → Normalize entity → Generate draft
→ Validate → Present for review → [user gate] → Commit.`

Output files (all relative to `insect.skill/`):

| Stage | Output |
|-------|--------|
| 1 | `sources/source_registry.json` (append) |
| 2 | `data/staging/fact_extracts/{pest_id}.facts.json` |
| 4 | `data/staging/pest_cards/{pest_id}.draft.md` |
| 7 | `data/pest_cards/{pest_id}.md` + index updates |

---

## Stage 1 — Register source

1. Read the source file. Assign `source_type` per `protocols/source_quality_policy.md` §1.
2. Extract metadata fields per `protocols/source_quality_policy.md` §2:
   title, source_type, publisher, url, accessed_at, license, reliability, notes.
3. Read `sources/source_registry.json`. Allocate next `source_id` (SRC_NNNN).
   If already registered, reuse. Append record, write back.
4. Report `source_id` + reliability.

---

## Stage 2 — Extract facts

1. Read `templates/pest_card.md` for the complete field list.
2. For each field, extract claims from the source. Record as:
   `{field, claim, source_id, evidence, confidence, notes}`.
   Confidence: `high` (explicit), `medium` (implied), `low` (inferred).
3. **No claim without evidence** → write `claim: null` with `notes: "Not in source."`.
4. Conflicting claims → record both, tag `notes: "CONFLICT: …"`.
5. Write to `data/staging/fact_extracts/{pest_id}.facts.json`.
6. Report field coverage (found / missing / low-confidence) before proceeding.

---

## Stage 3 — Normalize entity

1. Derive `pest_id` per `protocols/entity_normalization_policy.md` §1:
   `genus_species` (lowercase, underscore). No Latin name → provisional id.
2. Normalize names per §2 (cn / en / latin priority; aliases).
3. Check `data/pest_cards/` and `data/pest_ontology.json` for existing
   pest_id → flag if duplicate.
4. Report pest_id + normalized names.

---

## Stage 4 — Generate draft

1. Run stub generator:
   `python scripts/create_pest_card_stub.py --pest-id <id> --name-cn "<cn>" --name-latin "<latin>"`
2. Fill each section from fact extracts. Reference `templates/pest_card.md`
   for section structure and `protocols/pesticide_safety_policy.md` for §8.
3. **Hard rules**:
   - No fact without source evidence → use "待补充" or "当前来源不足".
   - No specific dosages (ml/mu, g/ha, 倍液).
   - Qualify uncertainty: "疑似", "可能", "需进一步确认".
   - Split morphology by egg / larva / pupa / adult.
4. Overwrite stub with filled content.

---

## Stage 5 — Validate

```bash
python scripts/validate_pest_card.py data/staging/pest_cards/{pest_id}.draft.md
```

Fix errors; review warnings. Loop until clean.

---

## Stage 6 — Present for review

**HARD STOP. Do not move the card.**

Summarize: (a) key card sections, (b) field coverage, (c) per-field confidence,
(d) validation result, (e) explicit question: "Approve card for official
knowledge base?"

**Wait for user confirmation.**

---

## Stage 7 — Commit

Only after explicit user approval:

1. Set `status: "reviewed"` + `reviewed_by`.
2. Move draft → `data/pest_cards/{pest_id}.md`.
3. Update index files (pest_ontology, crop_pest_map, similar_pests)
   per their schemas in `schemas/`.
4. Report final card location + index changes.

---

## Error table

| Situation | Action |
|-----------|--------|
| File unreadable / no pest info | Report; abort or ask for alternative |
| Multiple pests in source | Ask user which to process |
| pest_id exists | Ask: supplement or update? |
| reliability = `low`/`unknown` | Warn; proceed only with approval |
| No Latin name → no pest_id | Use provisional id; flag for expert review |
