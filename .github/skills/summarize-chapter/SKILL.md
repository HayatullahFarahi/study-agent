---
name: summarize-chapter
description: 'Write a precise, easy-to-study summary of one chapter, section, slide group, or video part, or of an entire material. Grounded in the source text with page, slide, or timestamp citations, key terms, a diagram, and self-check questions. Saves Markdown (optional PDF) to temp/Notes/<slug>/summary/. Use when the user wants a summary, recap, cheat sheet, study guide, TL;DR, or overview of a book, chapter, deck, or video.'
argument-hint: '<material-slug> chapter: <N> | unit: <id> | all [format: pdf]'
---

# Summarize a Chapter, Unit, or Whole Material

Follow the workspace conventions in `.github/copilot-instructions.md` (§3 resolving a material, §5 locating text). Summaries are reference documents: they never change `coveredUnits` or progress.

## Arguments

| Argument                 | Scope                                              |
| ------------------------ | -------------------------------------------------- |
| `chapter: <N>`           | structure `ch-N` and all its sections              |
| `unit: <id>`             | one section or video part, for example `3.2`       |
| `all`                    | every chapter, plus a full summary of the material |
| `format: pdf` or `--pdf` | also render a PDF next to the Markdown             |

Alias: `/summarize <id> in <slug> [--pdf]`.

## Steps (one chapter or unit)

1. Resolve the material and find the unit(s) in `structure`.
2. Load the source text for the range (§5). For ranges over ~1,500 lines, go section by section: read, take notes, move on.
3. Take a **concept inventory** per section: every defined term, claim, framework, list, process, number, formula, example, and comparison. Each one gets at least one line in the summary, so nothing is silently dropped.
4. Write the summary in the format below, following the precision rules.
5. Save it as `temp/Notes/<slug>/summary/<slug>-ch<N>-summary.md`, or `<slug>-<unit-id>-summary.md` for a single unit (for example `ddia-3.2-summary.md`).
6. If a PDF was requested, run the PDF step.
7. Confirm the path(s), then offer: a quiz on it (`/quiz-me <slug> chapter: <N>`), questions about it, or studying it.

## Precision rules

- Every key idea carries a citation: `(p. 23)`, `(slide 7)`, `(00:42:10)`, `(§ Section)`.
- Keep the author's terms, definitions, numbers, list items, and their order. Quote short phrases (20 words or fewer) when the wording matters.
- Plain language first. Define jargon at first use and expand every acronym on first use.
- Label anything not from the source (analogies, extra examples) with 💬.
- Length: roughly one page per 10–15 source pages, 10 slides, or 10 minutes of video. Never pad.
- If the source text can't be loaded, write the structure only, mark it "⏳ Not summarized: source text unavailable", and ask the user to paste the text. Never invent content.

## Summary format

```markdown
# <Chapter or unit id> — <Title>

> <Material title> · <loc> · Summarized <YYYY-MM-DD> · Source-grounded

## ⚡ TL;DR

- <3–5 bullets: the chapter's main claims, each with a citation>

## 🗺️ Big Picture

<one ASCII diagram or table showing how the chapter's ideas connect>

## 🔑 Key Ideas

### 1. <Idea> (p. 23)

**What it is**: <precise definition or claim, in plain words>
**Why it matters**: <one sentence>
**How it works**: <steps, mechanism, or formula, only if the source describes one>
**Example**: <from the source, or a 💬 tutor example>
⚠️ <limitation or pitfall, if the source names one>

### 2. …

## 📖 Key Terms

| Term | Meaning in this chapter | Where |
| ---- | ----------------------- | ----- |

## 🔗 Connections

- **Builds on**: <earlier chapter or concept> · **Leads to**: <later chapter or concept>

## ✅ Self-Check

<details><summary>1. <question></summary>

<answer, with citation>

</details>

<!-- 3–5 questions: recall, understanding, application -->

## 🧠 Mental Model

> <one sentence that captures the chapter>

---

_Source: <material title>, <loc> · Units: <ids>_
```

- **Videos**: add `## 🎬 Re-watch` after Key Ideas, with 3–5 key moments as `hh:mm:ss — what happens`.
- **Slides**: cite slide numbers and say when a point comes from the speaker notes.
- **Engineering content**: may add `## 🔧 In Practice` with a short annotated code example or real-world usage (label it 💬 if it's not from the source).

## `all`: summarize the whole material

1. Confirm first: "This will summarize <N> chapters (~<pages or hours>). Continue?"
2. For each chapter without an up-to-date summary file, run one subagent at a time with #tool:agent/runSubagent. Give it the material title and slug, the chapter id, title, and loc, the text path and line range, this skill file to follow, the save path, and the instruction "return only the TL;DR bullets and five key terms".
3. Write `temp/Notes/<slug>/summary/<slug>-full-summary.md`:

   ```markdown
   # <Title> — Full Summary

   > <type> · <length> · Summarized <YYYY-MM-DD>

   ## ⚡ The whole material in 5 bullets

   ## 🗺️ Map

   | #   | Chapter | One-line takeaway | Summary                         |
   | --- | ------- | ----------------- | ------------------------------- |
   | 1   | <title> | <takeaway>        | [read](./<slug>-ch1-summary.md) |

   ## 🔑 Core ideas across chapters (5–10, each with chapter references)

   ## 🧭 Suggested study path (what to read first or skip, for the user's goal)
   ```

4. Fill the "Key Themes" section of `temp/Notes/<slug>/overview.md`.

## PDF step

```bash
.venv/bin/python -m pip install markdown weasyprint   # once; macOS also needs: brew install pango
.venv/bin/python .github/skills/summarize-chapter/scripts/md_to_pdf.py "<summary.md>"
```

[md_to_pdf.py](./scripts/md_to_pdf.py) writes `<summary>.pdf` next to the Markdown, which stays the master copy, and never fetches external resources. Emoji may render as boxes (a WeasyPrint limitation). If rendering still fails after one retry, keep the `.md`, report the error, and suggest VS Code's Markdown preview as an alternative.
