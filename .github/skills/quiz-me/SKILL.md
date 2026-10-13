---
name: quiz-me
description: 'Quiz the user on a registered material with 5 source-grounded questions (multiple choice, short answer, explain in your own words, applied scenario), asked one at a time with immediate feedback and citations. Records the score and weak areas in the tracker. Use when the user wants to be tested, check understanding, review a chapter or summary, or prepare for an exam or interview.'
argument-hint: '<material-slug> [chapter: <N> | unit: <id> | weak]'
---

# Quiz Mode

Follow the workspace conventions in `.github/copilot-instructions.md` (§3, §5, §6).

## Steps

1. Resolve the material and read its manifest.
2. **Pick the scope**:
   - Default: covered units, weighted toward recent sessions and past weak areas.
   - `chapter:` or `unit:`: that range, even if it isn't covered yet, when the user read its summary or asks for it explicitly.
   - `weak`: the `weakAreas` and `reviewUnits` from earlier `quizzes[]`.
   - Nothing covered and no scope given: offer a quiz on the first chapter's summary, or to start studying.
3. **Load the source text** for the scope (§5) and the matching `keyConcepts[]`. Every question must be answerable from the source.
4. **Write 5 questions**: 2 recall (multiple choice, 4 options with plausible distractors), 1 short answer, 1 explain in your own words, and 1 applied scenario (for engineering material: "You're designing X. Which approach, and why?"). Tie each one to a citation, but don't show the citation until feedback.
5. **Ask one at a time** and never reveal an answer early. For multiple choice, use #tool:vscode/askQuestions (single choice, no free text) when available; otherwise ask in chat.
6. **Give feedback after each answer**: ✅ or ❌, the correct answer, why, and the citation. Grade open answers as ✅ correct, 🟡 partly correct (say what's missing), or ❌.
7. **Show the results**:

   ```
   📊 Quiz Results — <Title> (<scope>)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Score      : <x>/5 (partly correct = ½)
   Strong     : <concepts>
   Weak areas : <concepts>
   Review     : <unit ids, titles, and locations>
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

8. **Record** the result in the manifest's `quizzes[]`: `{"date", "scope", "score": "x/5", "weakAreas": [], "reviewUnits": []}`.
9. **Suggest the next step**: for weak areas, offer a focused `deep-dive` on the weakest concept. For a score of 4/5 or better on units not yet covered, offer to mark them covered (checkpoint per §6).
