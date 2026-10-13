---
name: check-progress
description: "Show study progress across all registered materials, or details for one: percent complete, exact resume point, last studied date, quiz scores and weak areas, available summaries, and pending questions. Use when the user asks about progress, status, what's next, where they left off, or wants to review saved questions."
argument-hint: '[material-slug] (omit to see all materials)'
---

# Show Learning Progress

Follow the workspace conventions in `.github/copilot-instructions.md` (§3, §4).

## All materials (no slug)

1. Read `temp/progress/_index.json` (bootstrap it if missing), then each manifest.
2. Show them, most recently studied first:

   ```
   📚 Study Progress
   | Material | Type | Progress | Resume at | Last studied |
   |---|---|---|---|---|
   | <title> | <type> | ████░░░░░░ 42% (5/12) | 2.3 · p. 87 | 2026-10-12 |
   ```

3. Suggest: "Resume **<most recent>**? (`/start-study`)"

## One material (with slug)

1. Read the manifest and list the files in `temp/Notes/<slug>/summary/`.
2. Show:
   - Title, type, format, and source
   - Progress bar `[████████░░] 80%` and `<covered>/<total>` units
   - **Resume point**: unit, title, location, and note
   - Units per chapter as ✅ covered, 🟡 in progress, or ⬜ not started (compact)
   - The last 3 sessions: date, units, one-line summary
   - Quizzes: recent scores and weak areas
   - Available summaries (as links)
   - Saved key concepts: count and the last 5
   - Unresolved `pendingQuestions[]`, numbered
3. If there are pending questions, ask: "Want to tackle any of these now?" Answer the chosen one with `ask-material`, then mark it `"resolved": true`.
