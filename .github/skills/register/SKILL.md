---
name: register
description: Register a new learning material (book, course, slides, or article) into the study-agent tracking system. Use this when the user wants to add a new book, course, slide deck, or article to track. Creates manifest.json, session-log.md, and spotlight-log.md for the material.
argument-hint: <material-name> [type: book|course|slides|article]
---

# Register a New Learning Material

Read `.github/copilot-instructions.md` first for the full system behavior and file schemas.

## Steps

1. Derive a **slug** from the given name: lowercase, hyphenated (e.g. "Clean Code" → `clean-code`)
2. Read `temp/progress/_template.json` to get the schema
3. Create `temp/progress/<slug>/manifest.json` — fill in:
    - `id`: the slug
    - `title`: the full name provided by the user
    - `type`: ask the user if not provided (`book` | `course` | `slides` | `article`)
    - `format`: ask the user if not provided (`pdf` | `pptx` | `zip` | `mixed`)
    - `source`: e.g. `learning-materials/<slug>/`
    - `addedOn`: today's date (YYYY-MM-DD)
    - Leave `structure`, `progress`, `coveredUnits`, `sessions`, `keyConcepts`, `pendingQuestions` at their template defaults
4. Add an entry to `temp/progress/_index.json`:
    ```json
    {
        "id": "<slug>",
        "title": "<title>",
        "type": "<type>",
        "addedOn": "<date>"
    }
    ```
5. Create `temp/progress/<slug>/session-log.md` with a header:
    ```markdown
    # Session Log — <Title>
    ```
6. Create `temp/progress/<slug>/spotlight-log.md` with a header:
    ```markdown
    # Spotlight Log — <Title>
    ```

## After Registration

Confirm to the user:

```
✓ Registered: <Title> (<type>)
  Slug        : <slug>
  Manifest    : temp/progress/<slug>/manifest.json
```

Then ask: _"Do you want to paste the Table of Contents / module list now so I can populate the structure?"_

If yes, parse the ToC and fill `structure[]` in the manifest with proper `id` and `title` fields for each chapter/module/section, then update `progress.totalUnits` accordingly.
