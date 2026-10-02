# Week 6 — Advanced Retrieval: Transform and Re-rank

Extends Week 5's RAG pipeline with a query transformation step (HyDE) and a
cross-encoder reranking step, run against the same 11-doc NailSalonApp
corpus. Deliberately keeps Week 5's worst-performing chunking config (small,
120/20) frozen as the retriever, so any change in precision/recall@3 can be
attributed to the transform + rerank step instead of chunk size. Traces one
query where the transformation made retrieval worse down to the exact
hypothetical passage that caused it.

## Contents
- `week6_transform_rerank.ipynb` — full notebook (run top to bottom;
  auto-clones this repo's `docs/` if not already present; needs
  `GEMINI_API_KEY` set as a Colab secret to run the live HyDE generation
  cells)

## Headline results
- HyDE + cross-encoder reranking moved mean precision@3 from 0.21 to 0.24
  and mean recall@3 from 0.64 to 0.73, but 8 of the 11 queries didn't change
  at all — the net gain comes from just 3 queries moving in opposite
  directions
- Of the 4 queries small chunking missed outright in Week 5, HyDE recovered
  2 by rewriting the question into a declarative passage that matches the
  docs' own statement-style wording; the other 2 stayed missed because the
  answer is a short list split across a 120-character chunk boundary, which
  rewording the query can't fix
- Traced one regression end to end: asked to answer "What does the owner
  app use for navigation?", HyDE confidently generated a passage about
  Apple MapKit and Google Maps SDK — the wrong sense of "navigation" — and
  that passage's embedding pulled the correct chunk (Expo Router) out of
  the candidate pool before the cross-encoder ever got to rerank it

## Research log
Findings and methodology notes: #13
