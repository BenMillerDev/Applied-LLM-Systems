# Week 5 — RAG Pipeline with Retrieval Evaluation

Builds a RAG pipeline over 11 real docs from my NailSalonApp project: chunking,
local embeddings with sentence-transformers, a FAISS index, and grounded
generation with Gemini. Compares three chunking configurations on
precision/recall@3 across 11 hand-labeled queries, then traces one retrieval
failure down to the exact chunk that got outranked and why.

## Contents
- `week5_RAG_pipeline2.ipynb` — full notebook (run top to bottom; auto-clones
  this repo's `docs/` if not already present; needs `GEMINI_API_KEY` set as a
  Colab secret to run the live Part 3 generation cells)

## Headline results
- By-paragraph chunking retrieved the correct chunk for all 11 test queries
  (recall@3 = 1.00); large (320/40) missed 1, small (120/20) missed 4
- Small chunking's failures trace back to a single generic chunk
  (`customer_booking_flow`'s "Booking happens in four steps...") repeatedly
  outranking the actual answer on shared vocabulary alone, not a fact split
  across a chunk boundary
- Traced one failure (the analytics time-filter query) end to end: the
  correct chunk ranked 8th of 127 under small chunking, beaten by its own
  overlapping neighbor and two unrelated chunks that shared only the word
  "time" — confirmed fixed by both larger chunks and a higher `k`, each with
  a different tradeoff

## Research log
Findings and methodology notes: #11
