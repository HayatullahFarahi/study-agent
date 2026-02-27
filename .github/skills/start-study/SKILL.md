---
name: start-study
description: Start or resume a full tracked learning session for a registered material. Use this when the user wants to begin or continue studying a book, course, slides, or article. Loads the manifest, prints session state, then enters active teaching mode with dynamic progress tracking.
argument-hint: <material-slug> [or material name]
---

# Start or Resume a Tracked Learning Session

Read `.github/copilot-instructions.md` first for the full system behavior, active teaching rules, dynamic tracking spec, and **creative explanation format (§3.5)**.

---

## Design Principle

> **The manifest tracks WHERE you are. The source material is WHAT you learn from. These are separate concerns.**
>
> - `manifest.json` = progress state only (covered units, percent, session history, saved concepts)
> - `learning-materials/<slug>/` = the actual book, slides, or article — the authoritative teaching source
> - Teaching must ALWAYS be grounded in the source material, never in general knowledge alone

---

## Steps

1. Resolve the slug from the user's input. Check `temp/progress/_index.json` if unsure.
2. Read `temp/progress/<slug>/manifest.json` — for progress state only, not for content.
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

---

## Step 6 — Load Source Content Before Teaching

**Before teaching any unit**, resolve the source content using this decision tree:

```
manifest.sourceText set?
      │ YES → read that .txt file directly → go to Step 7
      │ NO  ↓
manifest.source extension?
      │ .md / .txt / .html → read directly → go to Step 7
      │ .pdf / .pptx / .docx ↓
            │
      .txt counterpart already exists?
      │ YES → read it → add manifest.sourceText → go to Step 7
      │ NO  ↓
            │
      Run auto-conversion (see table below)
      │ SUCCESS → save .txt, set manifest.sourceText → go to Step 7
      │ FAIL    → ask user to paste section text → go to Step 7
```

**Auto-conversion commands** (replace `<src>` and `<out>` with actual absolute paths):

| Format  | Install (if needed)        | Conversion command                                                                                                                                                                                                 |
| ------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.pdf`  | `pip install pdfminer.six` | `python -c "import pdfminer.high_level as p; open(r'<out>', 'w', encoding='utf-8').write(p.extract_text(r'<src>'))"`                                                                                               |
| `.pptx` | `pip install python-pptx`  | `python -c "from pptx import Presentation; prs=Presentation(r'<src>'); open(r'<out>','w',encoding='utf-8').write('\n'.join(shp.text_frame.text for sl in prs.slides for shp in sl.shapes if shp.has_text_frame))"` |
| `.docx` | `pip install python-docx`  | `python -c "from docx import Document; doc=Document(r'<src>'); open(r'<out>','w',encoding='utf-8').write('\n'.join(p.text for p in doc.paragraphs))"`                                                              |

**Output path convention:** same directory as the original, same base name, `.txt` extension.

- Example: `learning-materials/ai-engineering/AI-Engineering.pdf` → `learning-materials/ai-engineering/AI-Engineering.txt`

**After a successful conversion:**

1. Write the `.txt` path into `manifest.sourceText` in `temp/progress/<slug>/manifest.json`
2. Confirm to the user: _"Converted **[filename]** to text and saved alongside the original. Future sessions will use the cached version."_

**After loading content (any path above):**

- Hold the loaded text as `activeUnitSource` for that unit only — do NOT reuse it across units
- If `pages` is set on the section in `structure[]`, use that to locate the correct region
- **NEVER use `temp/Notes/<slug>/` as a teaching source** — notes are read-only cross-reference only
- The fallback _"Teaching from general knowledge"_ is **not permitted** — if source is unavailable and conversion failed, ask the user to paste it and wait

**Rules for source-grounded teaching:**

- **NEVER teach a unit without source content.** If the format is unreadable, auto-conversion failed, and the user has not yet pasted text, ask and wait — do not proceed.
- Extract the `sectionConcepts[]` inventory from `activeUnitSource` exclusively, not from prior notes or general knowledge.

---

## Step 7 — Enter Active Teaching Mode

- **Before teaching each section, perform a concept inventory from the source:**
    1. Scan `activeUnitSource` for every named concept, framework, model, technique, list, ladder, loop, or taxonomy the author introduces
    2. Hold these as an internal `sectionConcepts[]` checklist
    3. Teach each one using the §3.5 creative format (one concept at a time)
    4. After finishing the section, sweep `sectionConcepts[]` — any concept not yet addressed gets at minimum a 📌 one-sentence callout before moving on
    5. Only mark the section as covered when every item in `sectionConcepts[]` has been touched
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
