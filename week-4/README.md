# Week 4 — Multi-Tool Assistant
 
Builds a PR-triage assistant around three tools (file lookup, size classification,
a guarded code-runner) and wires a real Gemini function-calling loop against them —
including a genuine failure the live model produced on its own, and the fix that
resolved it.
 
## Contents
- `week4_tool_use.ipynb` — full notebook (run top to bottom; needs `GEMINI_API_KEY`
  set as a Colab secret to run the live model cells)
## Headline results
- All three live Part 3 queries matched `classify_pr_size`'s rules exactly,
  including both tier-shift directions — a 512-line mechanical change dropped
  from high to medium, a 251-line substantial change rose from medium to high
- `get_file_stats`'s open-string `path` field failed on every natural-language
  query in Part 4 — the model guessed Rails, Laravel, and generic SQL file
  conventions against a Python repo and never converged in 6 turns — one
  addition to the tool's description (listing the PR's actual files) fixed it,
  taking the same query from 6 failed guesses to a 2-call success — see
  notebook for the full failure and fix
## Research log
Findings and methodology notes: #8
