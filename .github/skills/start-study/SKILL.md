---
name: start-study
description: Start or resume a full tracked learning session for a registered material. Use this when the user wants to begin or continue studying a book, course, slides, or article. Loads the manifest, prints session state, then enters active teaching mode with dynamic progress tracking.
argument-hint: <material-slug> [or material name]
---

# Start or Resume a Tracked Learning Session

Read `.github/copilot-instructions.md` first for the full system behavior, active teaching rules, dynamic tracking spec, and **creative explanation format (§3.5)**.

## Steps

1. Resolve the slug from the user's input. Check `temp/progress/_index.json` if unsure.
2. Read `temp/progress/<slug>/manifest.json`
3. Print the session header:
    ```
    ▶ SESSION STARTED — <Title>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Type        : <type>
    Progress    : <unitsCovered>/<totalUnits> (<percentComplete>%)
    Last Studied: <lastStudiedOn>
    Current Unit: <currentUnit>
    Pending Qs  : <count of unresolved pendingQuestions>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
4. If `structure[]` is empty or contains `tbd`, ask the user to paste the Table of Contents first, then populate `structure[]` and update `progress.totalUnits`.
5. Ask: _"Continue from **[currentUnit]** or jump to a specific section?"_
6. Enter **Active Teaching Mode**:
    - Teach one concept at a time
    - **Use the creative format from §3.5** — always open with 🎯 Why It Matters, include an ASCII diagram, a 💡 Analogy, a 🔧 In Practice example, and close with 🧠 Mental Model
    - Ask a comprehension check every 3 concepts
    - Offer a 3-question mini-quiz after each major unit
    - Auto-track all covered units and concepts in memory (do NOT wait for user to say "mark as covered")
    - Flush to disk only on `/end-session` or when the user says "save progress"

## Inline Save Triggers (during the session)

| User says                | Action                                      |
| ------------------------ | ------------------------------------------- |
| "save" / "save progress" | Write covered units to manifest immediately |
| `/note <text>`           | Save concept to `keyConcepts[]` immediately |
| `/q <question>`          | Append to `pendingQuestions[]` immediately  |
| "done with [unit]"       | Mark that unit as covered immediately       |

## Type-specific Behavior

| Type      | Approach                                                   |
| --------- | ---------------------------------------------------------- |
| `book`    | Chapter summaries first, then deep-dive section by section |
| `course`  | Theory first, then practical exercises per module          |
| `slides`  | Slide-by-slide, comprehension check after each group       |
| `article` | Section summaries → key concepts → application discussion  |
