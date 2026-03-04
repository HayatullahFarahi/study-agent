---
name: add-material
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
7. Create `temp/Notes/<slug>/overview.md` — a one-page overview of the material (see **Overview File Format** below)

## Overview File Format

Create `temp/Notes/<slug>/overview.md` immediately at registration. Use the appropriate type-specific template.

### All types — header block

```markdown
# 📖 Overview — <Title>

> Type: <type> | Format: <format> | Added: <YYYY-MM-DD>

---

## 📋 At a Glance

| Field       | Value                                 |
| ----------- | ------------------------------------- |
| Title       | <full title>                          |
| Type        | <book \| course \| slides \| article> |
| Format      | <pdf \| pptx \| zip \| mixed>         |
| Source      | <source path>                         |
| Added On    | <YYYY-MM-DD>                          |
| Total Units | <N — or TBD until ToC pasted>         |
| Progress    | 0% — not yet started                  |
```

### Type-specific structure block

**`book`** — Chapter table:

```markdown
## 🗂️ Chapters

| #   | Chapter                    | Status         |
| --- | -------------------------- | -------------- |
| 1   | <Chapter 1 Title — or TBD> | ⬜ Not started |
| …   | …                          | …              |

> Run `/start-study <slug>` and paste the Table of Contents to populate chapter titles.
```

**`course`** — Module table:

```markdown
## 🗂️ Modules

| #   | Module              | Status         |
| --- | ------------------- | -------------- |
| 1   | <Module 1 — or TBD> | ⬜ Not started |
| …   | …                   | …              |

> Run `/start-study <slug>` and paste the module list to populate.
```

**`slides`** — Slide group table:

```markdown
## 🗂️ Slide Groups

| #   | Group / Deck Section | Status         |
| --- | -------------------- | -------------- |
| 1   | <Group 1 — or TBD>   | ⬜ Not started |
| …   | …                    | …              |

> Run `/start-study <slug>` and paste the slide deck outline to populate.
```

**`article`** — Sections and key themes:

```markdown
## 🗂️ Sections

| #   | Section              | Status         |
| --- | -------------------- | -------------- |
| 1   | <Section 1 — or TBD> | ⬜ Not started |
| …   | …                    | …              |

## 🧩 Key Themes (from abstract/intro)

> _Paste the article abstract or intro and I will extract key themes here._
```

### All types — footer block

```markdown
## 🎯 Study Goals

- [ ] _Add your learning goals here_

## 🧠 Key Themes to Watch

> _Populated after the first session. Themes extracted from source during teaching will appear here._

---

_Run `/start-study <slug>` to begin a tracked session._  
_Run `/check-progress <slug>` at any time to see live progress stats._
```

### When ToC is provided at registration

If the user pastes the ToC / module list during the registration step:

- Fill in the structure table rows (chapter numbers + titles) in `overview.md` instead of placeholder rows
- Set statuses to `⬜ Not started` for all
- Update `progress.totalUnits` in `manifest.json` accordingly

## After Registration

Confirm to the user:

```
✓ Registered: <Title> (<type>)
  Slug        : <slug>
  Manifest    : temp/progress/<slug>/manifest.json
  Overview    : temp/Notes/<slug>/overview.md
```

Then ask: _"Do you want to paste the Table of Contents / module list now so I can populate the structure?"_

If yes, parse the ToC and:

- Fill `structure[]` in the manifest with proper `id` and `title` fields
- Update `progress.totalUnits`
- Replace the placeholder rows in `temp/Notes/<slug>/overview.md` with real chapter/module titles
