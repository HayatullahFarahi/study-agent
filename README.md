# Agentic Learning Flow (ALF)

A Copilot-powered personal learning system that tracks your progress across books, courses, and slide decks — session by session.

---

## How It Works

```
Type /start <material>  →  Copilot teaches it  →  Progress auto-tracked  →  /end-session saves all
```

Copilot acts as your personal tutor via **agent skills** — slash commands that appear in the chat `/` menu. It knows where you left off, dynamically tracks what you've covered, saves key concepts, and can quiz you at any time.

---

## Folder Structure

```
<workspace-root>/
  .github/
    copilot-instructions.md     ← master behavior rules for the agent
    skills/                     ← agent skills (slash commands)
      register/SKILL.md
      start/SKILL.md
      spotlight/SKILL.md
      quiz/SKILL.md
      progress/SKILL.md
      note/SKILL.md
      q/SKILL.md
      end-session/SKILL.md
  LEARNING-MATERIALS.md         ← guide for adding materials (tracked by git)
  learning-materials/           ← (gitignored) paste your PDFs, PPTs, ZIPs here
    <slug>/
  temp/
    progress/                   ← (gitignored) all progress tracking lives here
      _index.json               ← index of all registered materials
      _template.json            ← schema template for new materials
      <slug>/
        manifest.json           ← progress state for this material
        session-log.md          ← tracked session history
        spotlight-log.md        ← standalone spotlight session history
```

---

## Slash Commands

Type `/` in Copilot Chat to see all available skills. VS Code agent mode required.

| Command | What it does |
|---|---|
| `/register <name>` | Register a new learning material |
| `/start <slug>` | Start or resume a session (any type — book, course, slides, article) |
| `/spotlight <topic> [in <slug>]` | Standalone focused deep-dive, no progress change |
| `/quiz <slug> [unit: <id>]` | Quiz yourself on covered material |
| `/progress [slug]` | Show progress across all or one material |
| `/note <text> [in <slug>]` | Save a key concept immediately |
| `/q <question> [in <slug>]` | Log a question for later |
| `/end-session` | End session and flush all progress to disk |

---

## Quick Start

```
/register Clean Code          ← adds a new material
/start clean-code             ← begins or resumes a tracked session
/spotlight backpropagation in ml-a-z  ← focused topic, no progress change
/quiz ml-a-z                  ← test yourself on covered material
/end-session                  ← saves everything to disk
/progress                     ← see all materials
```

---

## How Progress Tracking Works

- **Automatic** — Copilot tracks units and concepts as the session flows; you never need to say "mark as covered"
- **Inline saves** — saying `"save progress"`, `/note`, or `/q` triggers an immediate write to disk
- **Full flush** — `/end-session` writes all covered units, updates `percentComplete`, and logs the session
- **Spotlight isolation** — `/spotlight` sessions never pollute tracked progress
