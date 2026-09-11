# Week 3 — Prompts as Engineering Artifacts
 
Builds a versioned code review triage prompt (bug/security/performance/style
classification with a one-sentence rationale) and tests whether one added
rule actually improves it, or just trades one failure for another.
 
## Contents
- `week3_prompt_engineering.ipynb` — full analysis notebook (run top to bottom)
- `prompts/code_review_v1.md` — baseline prompt
- `prompts/code_review_v2.md` — v1 + one added severity-priority rule
## Headline results
- v1 and v2 both score **92% exact-match** (11/12) on the test suite, but on
  different cases — v2's added rule fixes a bug buried behind naming
  complaints, but misclassifies a comment that merely contains the word
  "security" without an actual vulnerability
- Average semantic-similarity actually **drops from 0.764 to 0.684** between
  v1 and v2, showing exact-match and semantic-similarity don't always move
  together — see notebook for the failure case and mitigation
## Research log
Findings and methodology notes: #6
