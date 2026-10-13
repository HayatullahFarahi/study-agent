---
name: end-session
description: 'End the current study or deep-dive session and save everything: covered units, the exact resume point, progress percentage, session history, logs, overview status, and the materials index. Use when the user says stop, pause, done for today, save, wrap up, or end session.'
---

# End Session and Save

Follow the workspace conventions in `.github/copilot-instructions.md` (§6 tracker protocol).

## Tracked session

1. Gather from `activeSession`: units covered, concepts introduced, questions raised, and the current position.
2. Update `temp/progress/<slug>/manifest.json`. Most of it is already checkpointed; make sure nothing is missing:
   - `coveredUnits` gets the session's units (no duplicates). Recompute `unitsCovered` and `percentComplete` (one decimal).
   - `currentUnit` = the first leaf in structure order that isn't covered (`null` when the material is finished).
   - `resumePoint` = the exact stop position: `{"unit", "loc", "note": "after '<last concept>'; next: '<next concept>'", "savedOn"}`. If the unit was finished, use the start of `currentUnit`.
   - Set `lastStudiedOn` to today and append to `sessions[]`:

     ```json
     {
       "date": "<YYYY-MM-DD>",
       "duration": "<estimate>",
       "mode": "tracked",
       "unitsCovered": ["2.1", "2.2"],
       "stoppedAt": "<resumePoint.loc>",
       "summary": "<one line>",
       "keyTakeaways": ["…"]
     }
     ```

3. Append to `temp/progress/<slug>/session-log.md`:

   ```markdown
   ## Session — <YYYY-MM-DD> [tracked]

   - **Duration**: <estimate>
   - **Covered**: <unit ids and titles>
   - **Stopped at**: <unit> — <loc> (<note>)
   - **Summary**: <1–2 sentences>
   - **Key takeaways**:
     - <concept>
   - **Questions raised**: <list or "none">
   ```

4. In `temp/Notes/<slug>/overview.md`, mark covered rows ✅ and a partly done resume unit 🟡, and update the progress line under At a Glance.
5. In `temp/progress/_index.json`, set the material's `lastStudiedOn`.

## Spotlight (deep-dive) session

- Append to `temp/progress/<slug>/spotlight-log.md`, or to `temp/progress/spotlight-log.md` for standalone deep-dives:

  ```markdown
  ## Spotlight — <YYYY-MM-DD>

  - **Topic**: <topic>
  - **Linked material**: <title or "Standalone">
  - **Duration**: <estimate>
  - **Summary**: <1–2 sentences>
  - **Key takeaways**:
    - <concept>
  - **Questions raised**: <list or "none">
  ```

- Don't change progress fields or `sessions[]`.

## Closing summary

```
✓ SESSION SAVED — <Title>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Covered this session : <units or topic>
New key concepts     : <count>
Overall progress     : <x>/<y> (<z>%)
Resume next time at  : <unit> — <loc>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Next time, the user only needs to say **"resume"** (or run `/start-study`).
