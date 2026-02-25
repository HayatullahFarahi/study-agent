---
name: check-progress
description: Show learning progress across all registered materials, or detailed progress for a single material. Reads all manifests and _index.json to display progress percentages, last studied dates, current units, and pending questions. Use when the user wants to check how far they are or review saved questions.
argument-hint: [material-slug] (omit to see all materials)
---

# Show Learning Progress

Read `.github/copilot-instructions.md` for full behavior rules.

## Without a slug — show all materials

1. Read `temp/progress/_index.json` for the list of registered materials
2. For each slug, read `temp/progress/<slug>/manifest.json`
3. Display:
    ```
    ╔══════════════════════════════════════════════════════════╗
    ║                 study-agent — Progress                   ║
    ╠══════════════════════╦══════════╦════════════╦═══════════╣
    ║ Material             ║ Type     ║  Progress  ║ Last      ║
    ╠══════════════════════╬══════════╬════════════╬═══════════╣
    ║ <title>              ║ <type>   ║  x/y (z%)  ║ <date>    ║
    ╚══════════════════════╩══════════╩════════════╩═══════════╝
    ```

## With a slug — show detailed progress

1. Read `temp/progress/<slug>/manifest.json`
2. Display:
    - Title, type, format
    - Progress bar: `[████████░░] 80%`
    - `unitsCovered` / `totalUnits`
    - `currentUnit` (next to study)
    - `lastStudiedOn`
    - List of `coveredUnits[]`
    - Count and list of `keyConcepts[]`
    - Each unresolved entry in `pendingQuestions[]`, numbered
3. After listing pending questions (if any), ask: _"Want to tackle any of these now?"_ — if yes, answer the question, then offer to mark it `resolved: true` in the manifest.
