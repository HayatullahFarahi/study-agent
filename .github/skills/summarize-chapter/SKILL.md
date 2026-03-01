---
name: summarize-chapter
description: Generate a creative visual summary of a single chapter from a registered learning material and save it to temp/Notes/<slug>/summary/. Use when the user wants a structured recap of a chapter with ASCII diagrams, analogies, and mental models. Does not update coveredUnits or session progress.
argument-hint: <material-slug> chapter: <chapter-id>
---

# Summarize a Chapter from a Learning Material

Read `.github/copilot-instructions.md` first for the full system behavior and **creative explanation format (§3.5)**.

## Command

```
/summarize-chapter {material-slug} chapter: {chapter-id}
```

**Alias**: `/summarize {chapter-id} in {material-slug}`

---

## Steps

1. Resolve the slug from the user's input. Check `temp/progress/_index.json` if unsure.
2. Read `temp/progress/<slug>/manifest.json` to find the chapter entry in `structure[]`.
3. Identify all sections under that chapter from the manifest.
4. Check `coveredUnits[]` — note which sections are already covered vs. not yet studied.
5. Generate a **creative visual summary** of the chapter (see Format Rules below).
6. Save the summary file to:
    ```
    temp/Notes/<slug>/summary/<slug>-ch<chapter-id>-summary.md
    ```
    Use `temp/Notes/standalone/summary/ch<chapter-id>-summary.md` if no slug is known.
7. Confirm the save path to the user.
8. Ask: _"Want me to quiz you on this chapter, or continue to the next section?"_

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

| Scenario                          | File path                                            |
| --------------------------------- | ---------------------------------------------------- |
| Active session, material known    | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.md` |
| No active session, material known | `temp/Notes/<slug>/summary/<slug>-ch<id>-summary.md` |
| Standalone (no material linked)   | `temp/Notes/standalone/summary/ch<id>-summary.md`    |

---

## Quick Reference

| Command                                        | Action                                |
| ---------------------------------------------- | ------------------------------------- |
| `/summarize-chapter ai-engineering chapter: 1` | Summarize Chapter 1 of AI Engineering |
| `/summarize ch-2 in ai-engineering`            | Alias form                            |
| `/summarize-chapter ml-a-z chapter: 3`         | Summarize Chapter 3 of ML A-Z         |
