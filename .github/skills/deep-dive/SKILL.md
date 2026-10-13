---
name: deep-dive
description: "Focused, standalone session to deeply understand one concept or topic, optionally grounded in a registered material. Explains it the way engineers learn best: intuition, mechanism, runnable code, trade-offs, pitfalls, then check questions. Doesn't change tracked progress. Use when the user wants to understand, grasp, or master a specific concept, wants it explained for an engineer, or wants to explore a topic outside the linear study order."
argument-hint: '<topic> [in <material-slug>]'
---

# Deep Dive: Grasp One Concept

Follow the workspace conventions in `.github/copilot-instructions.md` (§5, §7). A deep-dive is isolated: it never changes `currentUnit`, `percentComplete`, `coveredUnits`, or `sessions[]`, and it's logged only to a spotlight log.

## Steps

1. **Parse** the input: the topic is everything before ` in <slug>`; the slug is optional. If a tracked session is active, offer to link the deep-dive to that material.
2. **Find the source**:
   - **With a material**: locate where it covers the topic (search the text the way `ask-material` does) and load those passages. Follow the author's framing with citations, and label any extras 💬.
   - **Standalone**: general knowledge is the source. Say so in the header, stay accurate, and flag anything uncertain or version-dependent.
3. **Print the header**:

   ```
   🔦 DEEP DIVE — <topic>
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Source : <material title (locations)> or "Standalone (general knowledge)"
   Level  : <ask: new to it · know the basics · want internals>
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

4. **Teach in layers**, and after each layer ask whether to go deeper:
   1. **Intuition**: 🎯 why it exists, a 💡 analogy, and a one-sentence definition.
   2. **Mechanism**: step by step with an ASCII diagram; math in KaTeX when relevant.
   3. **In practice**: a minimal runnable example with comments, how it shows up in real systems, and its cost or complexity.
   4. **Trade-offs and pitfalls**: when to use it, when not to, common mistakes, and alternatives compared in a table.
   5. **Check**: 2–3 questions, including one applied scenario, with feedback.
5. **Track** the concepts in `activeSession` (mode `spotlight`) and offer `/save-note` for the key insight.
6. On `/end-session`, write the spotlight log entry (see `end-session`).
