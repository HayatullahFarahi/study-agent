# Learning Materials

> This guide lives at the project root so it stays tracked by git.
> The `learning-materials/` folder itself is **gitignored** — paste your raw files there freely.

---

## Folder Layout

```
learning-materials/
  <slug>/          ← one subfolder per material, matching temp/progress/<slug>/
    <your files>
```

| What you have | Where to put it |
|---|---|
| A PDF book | `learning-materials/<slug>/<book>.pdf` |
| A course ZIP | `learning-materials/<slug>/<course>.zip` |
| Slide decks | `learning-materials/<slug>/slides/` |
| Mixed assets | `learning-materials/<slug>/` (any structure) |

---

## Adding a New Material

1. Create a subfolder: `learning-materials/<your-slug>/`
2. Drop your files in
3. Use the slash command in Copilot Chat:
   ```
   /add-material <name>
   ```
4. Copilot automatically creates:
   - `temp/progress/<slug>/manifest.json` — progress state and structure
   - `temp/progress/<slug>/session-log.md`
   - `temp/progress/<slug>/spotlight-log.md`
   - `temp/Notes/<slug>/overview.md` — **one-page overview** with an At-a-Glance table, chapter/module structure, Study Goals, and Key Themes
5. Paste the Table of Contents when prompted — Copilot populates `structure[]`, sets `totalUnits`, and fills the chapter table in `overview.md`

---

## Naming Convention

Use a short, lowercase, hyphenated slug that is **consistent** across:

```
learning-materials/<slug>/       ← raw files (gitignored)
temp/progress/<slug>/            ← progress tracking (gitignored)
```

---

## Progress & Notes Files (per material)

| File | Location | Purpose |
|------|----------|---------|
| `manifest.json` | `temp/progress/<slug>/` | Source of truth — progress, structure, concepts, questions |
| `session-log.md` | `temp/progress/<slug>/` | Chronological log of all tracked sessions |
| `spotlight-log.md` | `temp/progress/<slug>/` | Log of standalone deep-dive sessions |
| `overview.md` | `temp/Notes/<slug>/` | One-page overview created at registration — At-a-Glance, chapter list, Study Goals |
| `<N>-<ch>-<concept>.md` | `temp/Notes/<slug>/` | Concept notes saved via `/save-note` |
| `<slug>-ch<id>-summary.md` | `temp/Notes/<slug>/summary/` | Chapter summary (markdown) via `/summarize-chapter` |
| `<slug>-ch<id>-summary.pdf` | `temp/Notes/<slug>/summary/` | Chapter summary (PDF) via `/summarize-chapter … format: pdf` |

---

## Session Types

| Type | Command | Saves to |
|---|---|---|
| **Tracked** | `/start-study`, `/resume` | `manifest.json` + `session-log.md` |
| **Deep Dive** | `/deep-dive` | `spotlight-log.md` only (no progress change) |

---

## Chapter Summaries

Generate a visual summary of any chapter at any time with:

```
/summarize-chapter <slug> chapter: <id>               ← saves a .md file
/summarize-chapter <slug> chapter: <id> format: pdf   ← saves .md + .pdf
```

Summaries are saved to `temp/Notes/<slug>/summary/` and do **not** affect session progress or `coveredUnits`.

The PDF output uses `markdown` + `weasyprint` (pure Python). If those aren't installed, Copilot will install them automatically before converting.
