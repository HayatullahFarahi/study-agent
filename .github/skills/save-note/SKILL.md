---
name: save-note
description: "Save a key concept immediately, during or outside a session: appends it to the material's keyConcepts[] with its source location and writes a rich, linked note file to temp/Notes/<slug>/. Use when the user says note this, save this, remember this concept, or wants to record something important they just learned."
argument-hint: '<concept text> [in <material-slug>]'
---

# Save a Key Concept

Follow the workspace conventions in `.github/copilot-instructions.md` (§3, §7).

## Steps

1. Parse the input:
   - Concept text: everything before `in <slug>` (or the full input if no `in` keyword)
   - Slug: if provided after `in`, use it; if there is an active session, use that session's slug; otherwise ask the user which material this belongs to
2. Read `temp/progress/<slug>/manifest.json`
3. Determine the **order number**: count the existing entries in `keyConcepts[]` and add 1 (first note = 1, second = 2, …)
4. Determine the **chapter**: if `unit` is set (e.g. `"1.4"`), derive chapter as `"Chapter <major>"` (e.g. `"Chapter 1"`); otherwise use `"General"`
5. Append to `keyConcepts[]`:
   ```json
   {
       "order": <next integer>,
       "concept": "<short name derived from the text>",
       "unit": "<current active unit id, or null>",
       "chapter": "<Chapter N or General>",
       "loc": "<source location, e.g. p. 87 · slide 12 · 00:42:10, or null>",
       "summary": "<one-line definition / what was said>",
       "learnedOn": "<today YYYY-MM-DD>"
   }
   ```
6. Save the manifest
7. **Create or update the note file** at `temp/Notes/<slug>/<order>-<chapter-slug>-<concept-slug>.md`:
   - `<order>`: zero-padded 2-digit number matching the `order` field (e.g. `01`, `02`, `12`)
   - `<chapter-slug>`: `"General"` → `general`; `"Chapter 1"` → `ch1`; `"Chapter 10"` → `ch10`
   - `<concept-slug>`: concept name lowercased and hyphenated (e.g. `"Decision Ladder"` → `decision-ladder`)
   - Full example: `temp/Notes/ai-engineering/02-ch1-decision-ladder.md`
   - **If the file does not exist**: create it with the full rich note template (see Note File Format below)
   - **If the file already exists**: append a new dated section at the bottom (see Append Format below)
8. Confirm: _"Saved concept: **[concept name]** (Note #<order>) → `temp/Notes/<slug>/<order>-<chapter-slug>-<concept-slug>.md`"_

---

## Note File Format (new file)

Ground the note in the source text of its unit (cite it); label tutor-provided analogies and examples 💬.

````markdown
# <Concept Name>

> 📋 **Note #<order>** | **Chapter**: <Chapter N or General> | **Unit**: <unit id or "General"> | **Material**: <material title> | **Source**: <loc> | **Added**: <YYYY-MM-DD>

---

🎯 **Why It Matters**
<1-2 sentences: what problem this solves / why you need to know it>

📌 **Key Concept**
<core explanation in plain words, with citation>

```
<ASCII diagram, when the concept has structure, flow, or comparison>
```

💡 **Analogy**
<real-world parallel in 2-3 sentences>

🔧 **In Practice**
<code snippet or real-world usage example with inline comments>

⚠️ **Common Mistake**
<frequent misunderstanding to avoid, if there is one>

🧠 **Mental Model**
<one sticky-note sentence that captures the entire concept>

---

_Last updated: <YYYY-MM-DD>_
````

## Append Format (existing file — add at bottom)

````markdown
---

## Update — <YYYY-MM-DD> | Unit: <unit id or "General"> | Source: <loc>

<new insight, clarification, or additional detail about this concept>

```
<new ASCII diagram or chart, if relevant>
```

_Last updated: <YYYY-MM-DD>_
````

> ⚠️ Always update the `*Last updated:*` line at the very bottom of the file whenever appending.

```

```
