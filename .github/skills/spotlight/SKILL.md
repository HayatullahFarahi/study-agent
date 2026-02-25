---
name: spotlight
description: Start a standalone focused session on a specific topic or content block, independent of any material's linear progress. Does not advance currentUnit or percentComplete. Use when the user wants to deep-dive into a specific concept, chapter excerpt, or topic without affecting tracked progress.
argument-hint: <topic> [in <material-slug>]
---

# Spotlight Session — Standalone Focused Study

Read `.github/copilot-instructions.md` for full behavior rules.

A spotlight session is **isolated** — it never modifies `currentUnit`, `percentComplete`, or `unitsCovered` in any manifest. Progress is logged only to `spotlight-log.md`.

## Steps

1. Parse the input:
    - Topic: everything before `in <slug>` (or the full input if no `in` keyword)
    - Linked material slug: the word after `in` (optional)
2. If a slug is provided, read `temp/progress/<slug>/manifest.json` for context (covered units, key concepts) — use it to calibrate the explanation depth
3. Print the spotlight header:
    ```
    🔦 SPOTLIGHT SESSION — <topic>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Material : <title or "Standalone">
    Focus    : <topic>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
4. Ask: _"Paste the content you want to study, or should I explain **[topic]** from scratch?"_
5. Enter **Active Teaching Mode** — scoped to the topic only
6. Track concepts introduced in memory (`conceptsIntroducedThisSession`)

## On `/end-session`

Append to `temp/progress/<slug>/spotlight-log.md` (or `temp/progress/spotlight-log.md` if standalone):

```markdown
## Spotlight — YYYY-MM-DD

- **Topic**: <topic>
- **Linked Material**: <title or "Standalone">
- **Duration**: <estimated>
- **Summary**: <1-2 sentences>
- **Key Takeaways**:
    - <concept 1>
    - <concept 2>
- **Questions Raised**: <logged questions or "none">
```

**Do NOT** modify `manifest.json` progress fields (`currentUnit`, `percentComplete`, `coveredUnits`).
