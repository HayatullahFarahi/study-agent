---
name: start-study
description: 'Start or resume a tracked study session for a registered material (book, PDF, slides, video, course, or article), continuing exactly from the saved resume point. Teaches unit by unit from the source text with citations, checks understanding, and saves progress after every unit. Use when the user wants to study, continue, resume, pick up where they left off, or go to the next section. With no argument, resumes the most recently studied material.'
argument-hint: '[material slug or name] [unit id, e.g. 3.2] — omit both to resume the last material'
---

# Start or Resume a Study Session

Follow the workspace conventions in `.github/copilot-instructions.md`: §3 resolving a material, §5 locating text, §6 tracker protocol, §7 explanation block.

> The manifest tracks **where** you are; the source text is **what** you learn. Never teach a registered material from notes, summaries, or general knowledge.

## Steps

1. **Resolve the material** (§3): a slug or name → match it; nothing or "resume" → the latest `lastStudiedOn`; `demo` → bootstrap the demo.
2. **Read the manifest** for progress only. Add any missing v2 fields. If `structure` is empty, run `ingest-material` when a source exists, otherwise ask for the table of contents; then fill `structure`, `totalUnits`, and the overview rows.
3. **Print the header**:

   ```
   ▶ SESSION — <Title>
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Progress     : <unitsCovered>/<totalUnits> (<percent>%)  [████░░░░░░]
   Last studied : <lastStudiedOn or "never">
   Resume at    : <unit id> <unit title> — <resumePoint.loc> (<resumePoint.note>)
   Pending Qs   : <unresolved count> · Weak areas: <from the last quiz, or "—">
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

4. **Ask once**: continue from the resume point, jump to a unit, or review first. If `temp/Notes/<slug>/summary/<slug>-ch<N>-summary.md` exists for the current chapter, offer "read the 2-minute summary first". If the last quiz listed review units, offer a quick review of those first.
5. **Load the unit text** (§5): exactly the unit's line range. A `null` `resumePoint` means the start of `currentUnit`. When resuming mid-unit, find `resumePoint.loc` with `grep -n` and start reading there.
6. **Take a concept inventory**: list every named concept, definition, framework, list, process, formula, comparison, and example the source introduces in this unit. Keep it as an internal `unitConcepts[]` checklist.
7. **Teach** one concept at a time with the explanation block (§7), citing locations. After each concept, ask "Clear? Want an example, an analogy, or more depth?" Every three concepts, ask one quick check question. Answer side questions from the source the way `ask-material` does; park off-topic ones with `ask-later`.
8. **Close the unit**: sweep `unitConcepts[]`, and give anything not yet covered at least a one-line 📌 callout. Then offer a three-question mini-quiz.
9. **Checkpoint now** (§6): update `coveredUnits`, the progress numbers, `currentUnit`, `resumePoint` (start of the next unit), and the overview row (✅). Then say: "✓ Saved — <x>/<y> (<z>%). Next: <unit> — continue?"
10. Repeat steps 5–9. Suggest `/end-session` after 45–60 minutes or at a chapter boundary. If the user stops mid-unit, set `resumePoint` to the exact position and run `end-session`.

## By material type

| Type      | How to teach                                                                                                                                                    | Cite as         |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| `book`    | Section by section; open each chapter with three bullets on "what this chapter answers"                                                                         | `(p. N)`        |
| `slides`  | One slide group at a time. Speaker notes carry the explanation and slide text is the outline. Don't guess what a visual shows unless the notes describe it.     | `(slide N)`     |
| `video`   | One part or chapter at a time. Give a timestamp for every concept so the learner can re-watch it, and end each part with a 🎬 re-watch list of 2–3 key moments. | `(hh:mm:ss)`    |
| `course`  | Module by module; theory first, then exercises or code                                                                                                          | file + location |
| `article` | Section summary → key concepts → how to apply them                                                                                                              | `(§ Section)`   |
