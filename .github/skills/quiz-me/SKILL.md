---
name: quiz-me
description: Quiz the user on a registered learning material based on what they have covered so far. Generates 5 mixed-type questions (MCQ, short-answer, explain-in-own-words). Can be scoped to a specific unit. Use when the user wants to test their knowledge or review a material.
argument-hint: <material-slug> [unit: <unit-id>]
---

# Quiz Mode

Read `.github/copilot-instructions.md` for full behavior rules.

## Steps

1. Resolve slug, read `temp/progress/<slug>/manifest.json`
2. Extract `coveredUnits[]` and `keyConcepts[]`
3. If `unit:` is specified in the prompt, scope questions to that unit only; otherwise use all covered content
4. Generate **5 questions** mixing all types:
    - **MCQ** — 4 options, one correct
    - **Short answer** — one or two sentences expected
    - **Explain in your own words** — open-ended, tests conceptual depth
5. Present **one question at a time** — wait for the user's answer before showing the next
6. After each answer: give immediate feedback — correct/incorrect, brief explanation
7. After all 5 questions, show:
    ```
    📊 Quiz Results — <Title>
    ━━━━━━━━━━━━━━━━━━━━━━━━
    Score    : <x>/5
    Weak areas: <concepts that were missed>
    Review   : <suggested units to revisit>
    ━━━━━━━━━━━━━━━━━━━━━━━━
    ```

## Notes

- Never reveal the answer before the user responds
- Base questions on actual `keyConcepts[]` and `coveredUnits[]` from the manifest — do not invent content the user hasn't studied yet
