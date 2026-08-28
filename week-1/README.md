# Week 1 — Tokenization Analysis

Measures the multilingual tax between Vietnamese and English using
tiktoken, comparing the GPT-4 (cl100k_base) and GPT-4o (o200k_base)
tokenizers.

## Contents
- `week1_tokenization.ipynb` — full analysis notebook (run top to bottom)
- `week1_tokenization.html` — HTML export of the executed notebook, for
  the Canvas submission

## Headline results
- Vietnamese costs **2.23x** more tokens than English on GPT-4's
  tokenizer, but only **1.32x** more on GPT-4o's
- Same visible text can cost **50% more tokens** depending on Unicode
  normalization form (NFC vs. NFD) — see notebook for the failure case
  and mitigation

## Research log
Intermediate findings and methodology notes: #2
