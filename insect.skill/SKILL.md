---
name: agricultural-insect-skill
description: >
  Use this skill when the user asks about agricultural insects, crop pests,
  insect pest diagnosis, pest morphology, pest damage symptoms, occurrence
  patterns, or integrated pest management (IPM). This skill provides a
  structured diagnostic workflow, image observation protocols,
  uncertainty-handling policies, pesticide safety rules, and reusable
  answer templates. It does NOT contain real pest knowledge data — it is
  a framework that guides reasoning and output formatting.
version: 0.1.0
---

# Agricultural Insect Skill (Framework)

## 1. Purpose

This skill equips a general-purpose Agent to handle agricultural insect
inquiries in a professional, reproducible, and safe manner. It supplies
diagnostic protocols, output templates, and safety guardrails, but
contains **no real pest knowledge data** at this stage.

## 2. When to Use

Trigger this skill when a user request involves any of the following:

- Identifying an agricultural insect or crop pest
- Diagnosing insect damage on crops
- Asking about pest morphology, life stages, or behaviour
- Requesting integrated pest management (IPM) advice
- Uploading insect or crop-damage images for analysis
- Asking about pesticide use (the skill enforces safety policies)

## 3. When Not to Use

- Non-insect agricultural problems (diseases, weeds, nutrient deficiencies)
  — redirect to the appropriate skill or state the limitation.
- General entomology unrelated to agriculture (e.g. forensic entomology,
  pet insects, biodiversity surveys) — handle with a generic response and
  note that the agricultural focus may not apply.
- Requests for exact pesticide dosages or prescriptions — refuse and
  defer to local plant protection authorities.

## 4. Required Diagnostic Slots

Before producing a diagnosis, attempt to fill these slots. If critical
slots are missing, follow the uncertainty policy and ask the user.

| Slot | Priority | Description |
|------|----------|-------------|
| Crop / host plant | Critical | Species, variety, growth stage |
| Location / region | High | Province / county, climate zone |
| Season / date | High | Month, crop phenology stage |
| Damaged plant part | High | Leaf, stem, root, fruit, flower, seedling |
| Symptoms | Critical | Holes, discolouration, wilting, galls, mines |
| Insect stage observed | High | Egg, larva/nymph, pupa, adult |
| Insect morphology | High | Size, colour, shape, wings, antennae, legs |
| Field distribution | Medium | Sporadic, patchy, edge effect, uniform |
| Images | High | In-focus, multiple angles, scale reference |
| Recent field operations | Low | Pesticide applications, irrigation, fertilisation |

## 5. Reasoning Procedure

Follow this ordered workflow (detailed in `protocols/diagnosis_workflow.md`):

1. **Scope check** — Is this an agricultural insect question?
2. **Slot extraction** — Pull all available diagnostic slots from the user's
   message and any uploaded images.
3. **Sufficiency assessment** — Are the critical slots filled?
4. **Candidate generation** — Based on available evidence, list candidate
   pests. With an empty knowledge base, respond that no matching records
   were found and suggest the user consult local experts or provide more
   details.
5. **Differential diagnosis** — Compare similar candidates using
   distinguishing features.
6. **Confidence calibration** — Assign a confidence level (High / Medium /
   Low / Insufficient).
7. **Follow-up questioning** — If confidence is low or slots are missing,
   use templates in `templates/followup_questions.md`.
8. **Recommendation** — Produce IPM advice following
   `protocols/pesticide_safety_policy.md`.
9. **Output** — Format the response using one of the templates in
   `templates/`.

## 6. Image Handling Principles

When the user provides images, apply the checklist in
`protocols/image_observation_checklist.md`:

- Describe observable features objectively before inferring species.
- Note image quality (blur, lighting, angle, scale).
- If an image is too poor to identify, state that clearly and request
  better images.
- Never claim high-confidence species-level ID from a single blurry photo.

## 7. Uncertainty and Refusal Policy

See `protocols/uncertainty_policy.md` for full details. Core rules:

- If information is insufficient, ask targeted follow-up questions.
- If images are blurry, reduce confidence and request re-shooting.
- Do not force a species-level identification when evidence is weak;
  use "suspected", "possibly", or "needs further confirmation".
- Offer a Top-N candidate list when narrowing down is possible.
- For non-insect problems, state the limitation and suggest redirection.

## 8. Pesticide Safety Principles

See `protocols/pesticide_safety_policy.md` for full details. Core rules:

- Prioritise cultural, physical, and biological controls (IPM).
- Do not provide specific pesticide dosages.
- Do not recommend banned or restricted active ingredients.
- Remind the user to check local pesticide registration, target crops,
  pre-harvest intervals, and resistance management.
- Always advise consulting local plant protection authorities before
  application.

## 9. Output Requirements

Every agricultural insect diagnosis response must:

- State the confidence level explicitly.
- List the key evidence supporting the conclusion.
- Mention alternative candidates when confidence is not High.
- Include a safety disclaimer when pesticides are discussed.
- Use clear, professional language suitable for farmers and technicians.

Use the templates in `templates/` as starting points:

- `diagnosis_answer.md` — consumer-facing diagnosis reply
- `followup_questions.md` — structured follow-up question sets
- `expert_report.md` — technical report for extension workers

## 10. Available Local Resources

| Path | Purpose |
|------|---------|
| `data/pest_ontology.json` | Pest knowledge base (empty in framework) |
| `data/crop_pest_map.json` | Crop–pest association table (empty) |
| `data/similar_pests.json` | Similar-pest differential table (empty) |
| `data/pest_cards/` | Individual pest reference cards (empty) |
| `schemas/` | JSON Schema definitions for all data files |
| `protocols/` | Diagnostic workflows and safety policies |
| `templates/` | Reusable answer templates |
| `scripts/` | Utility scripts for search and name normalisation |
| `tests/` | Test scaffolding (no real test cases yet) |
