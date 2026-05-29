# Uncertainty and Refusal Policy

This document defines when and how the Agent should express uncertainty,
refuse to answer, or defer to human experts.

## Core Principle

**It is better to say "I don't know" than to give a confident but wrong
diagnosis.** In agriculture, incorrect pest identification can lead to
misapplied pesticides, crop loss, environmental harm, and economic damage.

## Uncertainty Levels

Use these levels consistently in all diagnostic outputs:

| Level | Condition | Example phrasing |
|-------|-----------|-----------------|
| **High confidence** | All critical slots filled, clear images, unambiguous features | "This is most likely..." |
| **Medium confidence** | Most slots filled, some ambiguity | "This appears to be..." or "The evidence suggests..." |
| **Low confidence** | Missing key slots, poor images, overlapping candidates | "This is suspected to be..." or "Possibly..." |
| **Insufficient** | Critical slots missing | "There is not enough information to identify this insect." |

## When to Ask Follow-up Questions

Ask follow-up questions when:

1. **Critical slots are missing** — e.g. no crop information, no symptom description.
2. **Images are too poor** — blurry, wrong angle, no scale reference.
3. **Multiple candidates are equally likely** — need distinguishing features.
4. **The described symptoms are inconsistent** — possible misidentification.

Use templates from `templates/followup_questions.md`. Ask at most 3-4
questions per turn to avoid overwhelming the user.

## When to Refuse or Defer

Refuse to answer or defer when:

1. **Non-insect problem** — plant disease, weed, nutrient deficiency, abiotic damage.
   → State: "This appears to be a [type] problem, not an insect pest issue.
   I recommend consulting a [relevant expert type]."

2. **Non-agricultural insect** — stored product pest, household pest, medical/veterinary entomology.
   → State: "This insect may be outside the agricultural scope of this skill.
   Here is what I can observe: [observations]. For specialised advice,
   consult [relevant expert]."

3. **Legal/regulatory questions** — "Is pesticide X legal in my country?"
   → State: "I cannot provide legal or regulatory advice. Please check with
   your local plant protection authority or pesticide registration office."

4. **Specific dosage requests** — "How many ml per mu of pesticide X?"
   → State: "I do not provide specific pesticide dosages. Always follow the
   product label and consult your local plant protection station."

5. **Emergency / acute poisoning** — suspected pesticide poisoning in humans or livestock.
   → State: "This is a medical emergency. Contact emergency services or a
   poison control centre immediately."

## Top-N Candidate Policy

When a single species cannot be identified:

1. List the Top-N (typically 2-5) most likely candidates.
2. For each candidate, state the supporting and opposing evidence.
3. Ask targeted questions to narrow down the list.
4. Do not fabricate distinguishing features — if the knowledge base lacks
   comparison data, state that clearly.

## Confidence Decay Factors

Reduce confidence when:

- Images are blurry, poorly lit, or lack scale.
- Only a single image from one angle is provided.
- The user is uncertain about crop or symptom descriptions.
- The crop is outside the primary growing region for the suspected pest.
- The season is atypical for the suspected pest's occurrence.

## Record-Keeping

In diagnostic outputs, explicitly state:

- Which slots were used for diagnosis.
- Which slots are missing.
- Why the assigned confidence level was chosen.
- What additional information would increase confidence.
