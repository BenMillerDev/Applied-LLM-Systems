# Week 2 — Inference and Sampling

Traces a full forward pass on distilgpt2 and builds a sampling explorer
comparing temperature, top-k, and top-p against the model's real
next-token distribution.

## Contents
- `week2_inference_sampling.ipynb` — full analysis notebook (run top to bottom)

## Headline results
- Raising temperature from 0.5 to 2.0 drops the top-token probability
  from **70.6%** to **0.5%**, while the number of tokens realistically
  competing for the pick grows from about 4 to over **20,000**
- At temperature 0.2, the top token has a **98.9%** chance of being
  picked, yet **50,235 of 50,257** vocabulary tokens still carry
  nonzero probability — see notebook for the failure case and mitigation

## Research log
Intermediate findings and methodology notes: #4