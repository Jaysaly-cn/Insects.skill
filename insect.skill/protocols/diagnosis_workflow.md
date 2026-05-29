# Agricultural Insect Diagnosis Workflow

This document defines the standard diagnostic procedure for agricultural
insect inquiries. Follow these steps in order, branching or looping as
needed.

## Step 0: Scope Check

- Determine whether the inquiry is about an **agricultural insect**.
- If the inquiry is about a non-insect problem (disease, weed, nutrient
  deficiency, abiotic stress), state the limitation and redirect.
- If the inquiry is about non-agricultural entomology, apply the
  uncertainty policy and optionally redirect.

## Step 1: Slot Extraction

Extract every piece of diagnostic information available from the user's
message, conversation history, and any uploaded images.

**Required slots reference** (see SKILL.md §4):

| Priority | Slots |
|----------|-------|
| Critical | Crop / host plant, Symptoms |
| High | Location, Season, Damaged plant part, Insect stage, Insect morphology, Images |
| Medium | Field distribution |
| Low | Recent field operations |

Record the source of each slot value (user text, image, inference).

## Step 2: Sufficiency Assessment

- If **any Critical slot is empty**: insufficient for diagnosis.
  → Go to Step 7 (Follow-up).
- If **Critical slots are filled but several High slots are empty**:
  partial sufficiency. Proceed with lower confidence.
- If **all Critical and most High slots are filled**: sufficient.
  Proceed normally.

## Step 3: Candidate Generation

Based on the filled slots:

1. Query `data/crop_pest_map.json` for pests associated with the
   reported crop, region, and growth stage.
2. Query `data/pest_ontology.json` for pests matching the described
   morphology, symptoms, and damaged parts.
3. Intersect and rank candidates.

**Framework note**: With the empty knowledge base (v0.1.0), this step
will return zero candidates. The Agent should respond:

> No matching pest records were found in the local knowledge base.
> Based on the information you provided, I cannot generate a reliable
> candidate list. Please consult your local plant protection station
> or provide additional details.

## Step 4: Differential Diagnosis

For each candidate pair that may be confused:

1. Check `data/similar_pests.json` for known distinguishing points.
2. Compare the user's evidence against each distinguishing point.
3. Score each candidate on how well it matches the evidence.

## Step 5: Confidence Calibration

Assign one of the following confidence levels:

- **High** — All critical slots filled, strong morphological evidence,
  clear images, unambiguous distinguishing features.
- **Medium** — Most slots filled, some ambiguity, images adequate.
- **Low** — Missing key slots, ambiguous symptoms, poor images.
- **Insufficient** — Critical slots missing; cannot diagnose.

## Step 6: Top-N Output

Present results as:

1. Primary candidate (highest confidence).
2. Alternative candidates (if any).
3. Confidence level for each.
4. Key evidence and distinguishing points.

## Step 7: Follow-up Questioning

When confidence is below High or slots are missing, ask targeted
follow-up questions using templates in `templates/followup_questions.md`.

Group questions logically and avoid overwhelming the user. Prioritise
critical missing slots.

## Step 8: Integrated Recommendation

For confirmed or suspected pests, provide IPM guidance:

1. Cultural controls (crop rotation, resistant varieties, sanitation).
2. Physical/mechanical controls (traps, barriers, manual removal).
3. Biological controls (natural enemies, biopesticides).
4. Chemical controls — only as a last resort and following
   `protocols/pesticide_safety_policy.md`.

## Step 9: Output Formatting

Use one of the templates in `templates/` depending on the audience:

- General user → `diagnosis_answer.md`
- Follow-up questions → `followup_questions.md`
- Agricultural technician → `expert_report.md`

Always include a safety disclaimer when pesticides are mentioned.

## Flow Diagram (text)

```
[User Inquiry]
     │
     ▼
[Scope Check] ─── Non-insect / Non-agricultural ──→ [Redirect / Refuse]
     │
     ▼
[Slot Extraction]
     │
     ▼
[Sufficiency?] ─── Insufficient ──→ [Follow-up Questions] ──→ [Wait for User]
     │
     ▼
[Candidate Generation] ──── Zero candidates ──→ [Report: no records]
     │
     ▼
[Differential Diagnosis]
     │
     ▼
[Confidence Calibration]
     │
     ▼
[Output + Recommendations]
```
