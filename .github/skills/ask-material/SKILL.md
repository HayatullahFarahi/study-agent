---
name: ask-material
description: 'Answer a question about a registered learning material (book, PDF, slide deck, video transcript, course, or article) by searching its source text, with exact page, slide, or timestamp citations and short quotes. Use when the user asks what the material says about something, wants a passage, term, or figure explained, asks why or how questions while studying or reading a summary, or wants to find where a topic is covered.'
argument-hint: '<question> [in <material-slug>]'
---

# Ask the Material

Follow the workspace conventions in `.github/copilot-instructions.md` (§3 resolving a material, §5 locating text). Answering a question never changes progress.

## Steps

1. **Resolve the material**: `in <slug>`, else the active session's material, else the most recently studied one. If that's still ambiguous, ask.
2. **Read the manifest** for the text file(s), `structure` titles and locations, and `keyConcepts`.
3. **Find the evidence**:
   1. Pick 3–6 search terms: key nouns, synonyms, the acronym and its expansion, and likely unit titles.
   2. Search the text in the terminal (it's gitignored): `grep -n -i -E "term1|term2" "<text file>" | head -40`. For multi-file materials, search each `structure[].source`.
   3. Rank hits by how many terms they match and whether they fall in a unit whose title fits. Read 30–60 lines around the best 2–4 hits, more if the answer spans pages.
   4. Cite each passage with the nearest location marker above it (§5).
4. **Answer**:
   - Lead with a direct answer in 1–3 sentences, then explain in plain language.
   - Cite every claim taken from the material. Quote the key sentence (25 words or fewer) when exact wording matters.
   - If passages disagree or are ambiguous, say so and show both.
   - If the material doesn't cover it, say "📭 The material doesn't cover this (searched: <terms>)." Then, only if useful, add a short, clearly separated **💬 Beyond the source** answer.
   - For engineering topics, add a minimal example or the practical implication when it helps (label it 💬 if it's not from the source).
   - Point to further reading, for example "Read more: 3.2 Replication Lag (pp. 161-167)".
5. **Log** the exchange in `temp/Notes/<slug>/qa-log.md` (create it with `# Q&A Log — <Title>` if missing):

   ```markdown
   ## <YYYY-MM-DD> — <question>

   **Answer:** <2–4 sentences>
   **Sources:** <citations>
   ```

6. If the question matches an unresolved entry in `pendingQuestions[]`, set `"resolved": true` and `"resolvedOn": "<YYYY-MM-DD>"`.
7. Offer one follow-up: save it as a note, deep-dive into it, or take a quick quiz on it.
