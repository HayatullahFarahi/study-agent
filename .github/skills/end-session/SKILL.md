---
name: end-session
description: End the current learning session and flush all tracked progress to disk. Updates manifest.json with covered units, percentComplete, currentUnit, and lastStudiedOn. Appends a structured entry to session-log.md or spotlight-log.md. Always call this to save your work after studying.
---

# End Session and Save All Progress

Read `.github/copilot-instructions.md` for full behavior rules and exact file schemas.

## Steps

1. Determine what was covered during this session (from `activeSession` memory):
    - `unitsCoveredThisSession[]`
    - `conceptsIntroducedThisSession[]`
    - `questionsRaisedThisSession[]`
    - Session mode: `tracked` or `spotlight`

2. **For tracked sessions** — update `temp/progress/<slug>/manifest.json`:
    - Add all items in `unitsCoveredThisSession` to `coveredUnits[]` (avoid duplicates)
    - Recalculate `progress.unitsCovered = coveredUnits.length`
    - Recalculate `progress.percentComplete = round(unitsCovered / totalUnits * 100, 1)`
    - Set `progress.currentUnit` to the first unit in `structure[]` not in `coveredUnits[]`
    - Set `progress.lastStudiedOn` to today
    - Append to `sessions[]`:
        ```json
        {
            "date": "<YYYY-MM-DD>",
            "duration": "<estimated>",
            "mode": "tracked",
            "unitsCovered": ["<unit-ids>"],
            "summary": "<one-line>",
            "keyTakeaways": ["<concept 1>", "..."]
        }
        ```
    - Append to `temp/progress/<slug>/session-log.md`

3. **For spotlight sessions** — do NOT change `currentUnit` or `percentComplete`:
    - Only append to `temp/progress/<slug>/spotlight-log.md` (or global `temp/progress/spotlight-log.md`)
    - Do NOT append to `sessions[]` in the manifest

4. Print the closing summary:
    ```
    ✓ SESSION SAVED — <Title>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━
    Covered this session : <units or topic>
    New key concepts     : <count>
    Overall progress     : <x>/<y> (<z>%)
    Next up              : <next unit>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
