---
name: add-material
description: 'Register a new learning material in the study tracker: a PDF book or paper, slide deck, Word doc, article or web page, long video file, YouTube video or playlist, course folder, or zip. Extracts the text, auto-detects chapters, sections, slide groups, or video parts, and creates the manifest, logs, and a one-page overview. Use when the user wants to add, register, import, or start learning a new material.'
argument-hint: '<file path | folder | .zip | YouTube URL | web URL | title> [type: book|course|slides|article|video]'
---

# Register a New Learning Material

Follow the workspace conventions in `.github/copilot-instructions.md`.

## Steps

1. **Bootstrap** `temp/progress/_index.json` if it's missing (`{"materials": []}`).
2. **Identify the source** from the user's input:

   | Input                                   | Default `type`                                                                                                                      | `format`                                                     |
   | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
   | `.pdf`                                  | `book` if it has chapters or more than ~80 pages, else `article`                                                                    | `pdf`                                                        |
   | `.pptx`                                 | `slides`                                                                                                                            | `pptx`                                                       |
   | `.docx`, `.md`, `.txt`, `.html`         | `article`                                                                                                                           | the extension                                                |
   | Video or audio file, `.srt`, `.vtt`     | `video`                                                                                                                             | `video`, `audio`, or `subtitles`                             |
   | YouTube video URL                       | `video`                                                                                                                             | `youtube`                                                    |
   | YouTube playlist URL, folder, or `.zip` | `course`                                                                                                                            | `youtube` or `mixed`                                         |
   | Any other URL                           | `article`                                                                                                                           | `web` (fetch it and save as Markdown; see `ingest-material`) |
   | A title only                            | Ask for the file or link. If there is none, register in manual mode: the user pastes the table of contents and, later, the content. |                                                              |
   - Files can stay where they are (absolute paths are fine). Suggest `learning-materials/<slug>/` for new downloads. Never move or modify originals.
   - Ask only for what you can't infer, such as an ambiguous type. Offer choices with #tool:vscode/askQuestions.

3. **Slug**: the lowercase, hyphenated title. If it already exists in `_index.json`, ask whether to update that material or pick a new slug.
4. **Ingest**: run the `ingest-material` skill with `--out-dir "learning-materials/<slug>/_extracted"`. Use the extracted title if the user didn't give one.
5. **Propose the structure** compactly and confirm it:

   ```
   Detected 12 chapters / 47 sections from PDF bookmarks (skipped: Cover, Contents, Index)
   ch-1  Reliable, Scalable, and Maintainable Applications   pp. 21-44   5 sections
   ch-2  Data Models and Query Languages                    pp. 45-86   6 sections
   …
   Keep this structure, or edit it (rename / merge / drop / split)?
   ```

   - Video parts titled `Part N`: skim each part's first ~15 lines and propose descriptive titles.
   - `detected: none`: ask for the table of contents (book), module list (course), or outline, and map the titles to `lines` with `grep -n` where you can.
   - Units too long for one sitting (more than ~40 pages or ~25 minutes): offer to split them.

6. **Create the manifest** at `temp/progress/<slug>/manifest.json` from [the template](./assets/manifest.template.json). Fill `id`, `title`, `type`, `format`, `source`, `sourceText`, `addedOn`, and `structure`. Set `progress.totalUnits` to the number of leaf units, `currentUnit` to the first leaf, and `resumePoint` to `{"unit": "<first leaf>", "loc": "<its loc>", "note": "start", "savedOn": "<today>"}`.
7. **Register** the material in `_index.json`: `{"id", "title", "type", "addedOn", "lastStudiedOn": null}`.
8. **Create the logs**: `temp/progress/<slug>/session-log.md` (`# Session Log — <Title>`) and `temp/progress/<slug>/spotlight-log.md` (`# Spotlight Log — <Title>`).
9. **Create** `temp/Notes/<slug>/overview.md` (format below).
10. **Confirm**:

    ```
    ✓ Registered: <Title> (<type>, <format>)
      Slug     : <slug>
      Units    : <N> (<detected>)
      Text     : <sourceText>
      Manifest : temp/progress/<slug>/manifest.json
      Overview : temp/Notes/<slug>/overview.md
    ```

    Then suggest the next step: `/start-study <slug>` to begin, or `/summarize-chapter <slug> all` to map the whole material first.

## Overview file format

```markdown
# 📖 Overview — <Title>

> Type: <type> | Format: <format> | Added: <YYYY-MM-DD>

## 📋 At a Glance

| Field    | Value                                     |
| -------- | ----------------------------------------- |
| Title    | <title>                                   |
| Source   | <source path or URL>                      |
| Length   | <N pages · N slides · hh:mm:ss · N files> |
| Units    | <N>                                       |
| Progress | 0% — not started                          |

## 🗂️ <Chapters | Modules | Slide Groups | Parts | Sections>

| #    | Title           | Location | Status |
| ---- | --------------- | -------- | ------ |
| ch-1 | <chapter title> | <loc>    | ⬜     |
| 1.1  | <section title> | <loc>    | ⬜     |

Status: ⬜ not started · 🟡 in progress · ✅ covered

## 🎯 Study Goals

- [ ] _Add your goals, for example "be able to design a replication strategy"_

## 🧠 Key Themes

> _Filled in as you study and summarize._
```

Section heading by type: book → Chapters · course → Modules · slides → Slide Groups · video → Chapters (if the video has them) or Parts · article → Sections.
