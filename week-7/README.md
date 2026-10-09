# Week 7 — The Adaptation Decision and a Production Dataset

Builds a labeled dataset for NailSalonApp's 8-intent support classifier (424
examples, 53/class) and adapts a zero-shot baseline with retrieval-selected
dynamic few-shot, reusing the same bi-encoder retrieval from Week 5/6.
Deliberately evaluates on two sets — an in-distribution 80-query split and
a separate 8-query boundary-probe set — so the probes can surface a method
difference the formal split alone couldn't. Traces one probe where dynamic
few-shot made classification worse down to the exact retrieved examples
that caused it.

## Contents
- `week7_adaptation.ipynb` — full notebook (run top to bottom; auto-clones
  this repo's `week-7/data` label files if not already present; needs
  `GEMINI_API_KEY` set as a Colab secret to run the live classification
  cells)
- `data/` — 8 markdown label files, one per intent (`ask_availability`,
  `ask_pricing`, `ask_service_menu`, `book_appointment`,
  `cancel_appointment`, `complain_service`, `request_refund`,
  `reschedule_appointment`), 56 raw bullet-list examples each under a
  `# <intent_name>` heading; source data the notebook cleans, dedupes, and
  splits into the 424-example train/eval set

## Headline results
- Data-quality pass on 448 raw rows (8 intents × 56) dropped 8 invalid and
  16 duplicate rows, leaving 424 clean examples split 320 train / 80 eval
  (40/10 per class); 0 train/eval near-duplicates by word 3-gram Jaccard
  (≥0.8)
- On the formal 80-query eval, zero-shot and dynamic few-shot tied at 99%
  (79/80) and missed the exact same query — the in-distribution eval
  couldn't separate the two methods at all
- A separate 8-query boundary-probe set did separate them: zero-shot 7/8
  (87.5%) vs. few-shot 6/8 (75%). Traced the one few-shot regression
  ("What's included in your pricing for a deluxe pedicure?", true
  `ask_pricing`) to its retrieved examples: 3 of 4 were lexically similar
  `ask_service_menu` neighbors that outvoted the single correct
  `ask_pricing` neighbor
- Decision: ship zero-shot as the default; dynamic few-shot added retrieval
  cost without a net accuracy gain on either eval

## Research log
Findings and methodology notes: #15
