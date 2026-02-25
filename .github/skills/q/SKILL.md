---
name: q
description: Log a question to revisit later, saving it to the material's pendingQuestions array. Use when the user has a question they don't want to lose but want to continue studying. Also triggered by phrases like "remember this question" or "ask later".
argument-hint: <question text> [in <material-slug>]
---

# Log a Pending Question

Read `.github/copilot-instructions.md` for full behavior rules.

## Steps

1. Parse the input:
    - Question text: everything before `in <slug>` (or the full input if no `in` keyword)
    - Slug: if provided after `in`, use it; if there is an active session, use that session's slug; otherwise ask the user which material this belongs to
2. Read `temp/progress/<slug>/manifest.json`
3. Append to `pendingQuestions[]`:
    ```json
    {
        "question": "<the full question text>",
        "unit": "<current active unit id, or null>",
        "addedOn": "<today YYYY-MM-DD>",
        "resolved": false
    }
    ```
4. Save the manifest
5. Confirm: _"Logged for later: **[question]**"_

The question is saved but NOT answered now — the user can review all pending questions with `/questions` and resolve them in a future session.
