---
name: save-note
description: Save a key concept to a material's manifest immediately, during or outside a session. Use when the user wants to record something important they just learned. Appends to keyConcepts[] in the manifest.
argument-hint: <concept text> [in <material-slug>]
---

# Save a Key Concept

Read `.github/copilot-instructions.md` for full behavior rules.

## Steps

1. Parse the input:
    - Concept text: everything before `in <slug>` (or the full input if no `in` keyword)
    - Slug: if provided after `in`, use it; if there is an active session, use that session's slug; otherwise ask the user which material this belongs to
2. Read `temp/progress/<slug>/manifest.json`
3. Append to `keyConcepts[]`:
    ```json
    {
        "concept": "<short name derived from the text>",
        "unit": "<current active unit id, or null>",
        "summary": "<one-line definition / what was said>",
        "learnedOn": "<today YYYY-MM-DD>"
    }
    ```
4. Save the manifest
5. Confirm: _"Saved concept: **[concept name]**"_
