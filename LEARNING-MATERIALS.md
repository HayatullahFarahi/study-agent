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
4. Copilot creates `temp/progress/<slug>/manifest.json`, `session-log.md`, and `spotlight-log.md` automatically
5. Paste the Table of Contents when prompted — Copilot populates `structure[]` and sets `totalUnits`

---

## Naming Convention

Use a short, lowercase, hyphenated slug that is **consistent** across:

```
learning-materials/<slug>/       ← raw files (gitignored)
temp/progress/<slug>/            ← progress tracking (gitignored)
```

---

## Progress Files (per material)

| File | Purpose |
|---|---|
| `manifest.json` | Source of truth — progress, structure, concepts, questions |
| `session-log.md` | Chronological log of all tracked sessions |
| `spotlight-log.md` | Log of standalone deep-dive sessions |

---

## Session Types

| Type | Command | Saves to |
|---|---|---|
| **Tracked** | `/start-study`, `/resume` | `manifest.json` + `session-log.md` |
| **Deep Dive** | `/deep-dive` | `spotlight-log.md` only (no progress change) |
