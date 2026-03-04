---
name: summarize-chapter
description: Generate a creative visual summary of a single chapter from a registered learning material and save it to temp/Notes/<slug>/summary/. Use when the user wants a structured recap of a chapter with ASCII diagrams, analogies, and mental models. Does not update coveredUnits or session progress.
argument-hint: <material-slug> chapter: <chapter-id> [format: pdf]
---

# Summarize a Chapter from a Learning Material

Read `.github/copilot-instructions.md` first for the full system behavior and **creative explanation format (§3.5)**.

## Command

```
/summarize-chapter {material-slug} chapter: {chapter-id} [format: pdf]
```

**Alias**: `/summarize {chapter-id} in {material-slug} [--pdf]`

**Output format options:**

| Parameter     | Output                        | Default |
| ------------- | ----------------------------- | ------- |
| _(omitted)_   | `.md` markdown file           | ✅ yes  |
| `format: pdf` | `.pdf` file (markdown → PDF)  | no      |
| `--pdf`       | Same as `format: pdf` (alias) | no      |

When `format: pdf` is given, the `.md` file is **also kept** as the source — the PDF is generated alongside it.

---

## Steps

1. Resolve the slug from the user's input. Check `temp/progress/_index.json` if unsure.
2. Detect the requested output format — look for `format: pdf` or `--pdf` in the command. Store as `outputFormat = "pdf" | "md"` (default `"md"`).
3. Read `temp/progress/<slug>/manifest.json` to find the chapter entry in `structure[]`.
4. Identify all sections under that chapter from the manifest.
5. Check `coveredUnits[]` — note which sections are already covered vs. not yet studied.
6. Generate a **creative visual summary** of the chapter (see Format Rules below).
7. Save the `.md` summary file to:
    ```
    temp/Notes/<slug>/summary/<slug>-ch<chapter-id>-summary.md
    ```
    Use `temp/Notes/standalone/summary/ch<chapter-id>-summary.md` if no slug is known.
8. If `outputFormat == "pdf"`: run the **PDF conversion procedure** (see below) to produce:
    ```
    temp/Notes/<slug>/summary/<slug>-ch<chapter-id>-summary.pdf
    ```
9. Confirm the save path(s) to the user.
10. Ask: _"Want me to quiz you on this chapter, or continue to the next section?"_

---

## PDF Conversion Procedure

Run when `format: pdf` or `--pdf` is present. Always generate the `.md` file first, then convert.

**Step 1 — Check / install dependencies:**

```bash
pip install markdown weasyprint
```

> `markdown` converts the `.md` to HTML; `weasyprint` renders the HTML to PDF with CSS styling. No LaTeX or external binaries required.

**Step 2 — Convert:**

Replace `<md_path>` and `<pdf_path>` with the actual absolute file paths:

```python
python -c "
import markdown, pathlib
from weasyprint import HTML, CSS

md_path  = r'<md_path>'
pdf_path = r'<pdf_path>'

md_text = pathlib.Path(md_path).read_text(encoding='utf-8')
html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

full_html = '''
<!DOCTYPE html><html><head><meta charset=\"utf-8\">
<style>
  body  { font-family: Segoe UI, sans-serif; margin: 40px; color: #1a1a1a; }
  h1,h2 { color: #2c3e50; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
  pre   { background: #f4f4f4; padding: 12px; border-radius: 4px; font-size: 0.85em; }
  code  { background: #f0f0f0; padding: 2px 4px; border-radius: 3px; }
  table { border-collapse: collapse; width: 100%%; }
  th,td { border: 1px solid #ccc; padding: 6px 10px; }
  th    { background: #eaf0fb; }
  blockquote { border-left: 4px solid #aaa; margin-left: 0; padding-left: 12px; color: #555; }
</style></head><body>''' + html_body + '''</body></html>'''

HTML(string=full_html).write_pdf(pdf_path)
print('PDF saved:', pdf_path)
"
```

**Step 3 — Error handling:**

| Error                       | Resolution                                                                                          |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`       | Run `pip install markdown weasyprint` and retry                                                     |
| `OSError` on weasyprint     | May need `pip install weasyprint --upgrade`; on Windows also try `pip install weasyprint cairocffi` |
| Garbled PDF / missing fonts | Add `font-family: Arial, sans-serif` to the CSS block                                               |
| Emoji missing in PDF        | This is a known weasyprint limitation — emoji appear as boxes; the `.md` file always preserves them |

> If conversion fails after one retry attempt, confirm the `.md` was saved and inform the user that PDF generation failed with the error message, then ask if they want to try a different converter (e.g. Pandoc).

---

## Format Rules

Every chapter summary **must** follow this structure — no plain prose summaries allowed:

```
# Chapter <N> — <Title>
> <Material Title> | Creative Summary | <YYYY-MM-DD>

---

## 🗺️ Big Picture
[1 ASCII comparison table or paradigm shift diagram showing the chapter's core idea]

---

## <section-id> — <Section Title>
[For each section in the chapter:]

📌 Key Concept: <name>
[Core explanation — 2-4 sentences]

[ASCII diagram if the concept involves structure, flow, or comparison]

💡 Analogy: [1-2 sentence real-world parallel]

⚠️ Common Mistake (if applicable): [1 sentence]

🔧 In Practice (if applicable): [code snippet or real usage]

---

## 🧠 Chapter <N> — One-Sentence Mental Model
> [One sticky-note sentence that captures the whole chapter]

---
*Covered: §<ids> | Summarized: <YYYY-MM-DD>*
```

**Acronym expansion rule:**

Every time an acronym or abbreviation is used in a summary, **always write the full form first**, followed by the short form in parentheses — or the short form followed by the full form in parentheses on first use. Examples:

- ✅ `Supervised Finetuning (SFT)`
- ✅ `Reinforcement Learning from Human Feedback (RLHF)`
- ✅ `Mixture of Experts (MoE)`
- ❌ `SFT` alone — never use a bare acronym without expanding it at least once per summary

On **subsequent uses** within the same section block, the short form alone is fine.

---

**Concept inventory rule (prevents gaps without inflating length):**

Before writing each section block:

1. List every named concept, framework, model, technique, ladder, loop, taxonomy, or comparison table the author introduces in that section — hold this as `sectionConcepts[]`
2. Write the summary block, covering each item in `sectionConcepts[]`
3. Any concept not given a full block gets at minimum a 📌 one-liner so it is not invisible
4. Do **not** add more depth per concept — keep the same tight format. The goal is zero omissions, not longer entries.

**Visual tools required:**

| Tool                   | Required when                                   |
| ---------------------- | ----------------------------------------------- |
| ASCII diagram          | Any concept with structure, flow, or comparison |
| Comparison table       | Contrasting 2+ ideas or before/after paradigms  |
| Code block             | Any programmatic or API-related concept         |
| KaTeX math ($formula$) | Equations, metrics, probability                 |
| 💡 Analogy             | Every abstract concept                          |
| ⚠️ Common Mistake      | Whenever a frequent misunderstanding exists     |

---

## Behavior Rules

- If the chapter has **not been studied yet** (no sections in `coveredUnits[]`), add a notice at the top:
    > ⚠️ _This chapter has not been studied yet. This summary is based on the book's structure — paste chapter content for a deeper summary._
- If the chapter is **partially covered**, note which sections are summarized from study vs. inferred from structure.
- **Never fabricate content** for uncovered sections — write structure-only placeholders and prompt user to paste the content.
- The summary file is a **standalone artifact** — it must make sense without the manifest or session log.
- Do **not** update `coveredUnits[]` or session progress — this is a reference document, not a tracked session.

---

## Output File Naming

| Scenario                          | Markdown path                                        | PDF path (if `format: pdf`)                           |
| --------------------------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| Active session, material known    | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.md` | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.pdf` |
| No active session, material known | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.md` | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.pdf` |
| Standalone (no material linked)   | `temp/Notes/standalone/summary/ch<id>-summary.md`    | `temp/Notes/standalone/summary/ch<id>-summary.pdf`    |

The `.md` file is **always** written first and kept — the PDF is an additional artifact alongside it.

---

## Quick Reference

| Command                                                    | Action                                          |
| ---------------------------------------------------------- | ----------------------------------------------- |
| `/summarize-chapter ai-engineering chapter: 1`             | Summarize Chapter 1 — markdown output           |
| `/summarize-chapter ai-engineering chapter: 1 format: pdf` | Summarize Chapter 1 — markdown + PDF output     |
| `/summarize-chapter ai-engineering chapter: 1 --pdf`       | Same as above (shorthand)                       |
| `/summarize ch-2 in ai-engineering`                        | Alias form — markdown output                    |
| `/summarize ch-2 in ai-engineering --pdf`                  | Alias form — markdown + PDF output              |
| `/summarize-chapter ml-a-z chapter: 3`                     | Summarize Chapter 3 of ML A-Z — markdown output |
