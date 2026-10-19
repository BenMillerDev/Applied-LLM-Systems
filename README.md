# Applied-LLM-Systems

Coursework, notebooks, and code for COSC 650 Applied LLM Systems, built around hands-on projects that call real LLM APIs rather than just studying theory.

## Course context

This repository supports **COSC 650: Applied LLM Systems**, an 8-week course at Maryville University focused on the practical engineering side of working with large language models: prompting, evaluation, rate-limited API usage, and building small applications on top of an LLM backend.

## Repository organization

Work is organized by week, with one folder per week of the course:

- `week-0/` — Setup and prerequisites (environment, API keys, Colab/GitHub workflow)
- `week-1/` — Tokenization Analysis: multilingual tax between Vietnamese | [#2](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/2) | [#3](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/3)
- `week-2/` — Inference and Sampling: tracing a forward pass and comparing temperature, top-k, and top-p on a real model's next-token distribution | [#4](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/4) | [#5](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/5)
- `week-3/` — Prompts as Engineering Artifacts: versioning a code review triage prompt and testing whether an added rule improves it | [#6](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/6) | [#7](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/7)
- `week-4/` — Multi-Tool Function Calling: building a Gemini function-calling loop and fixing a fixing a failed file-lookup tool | [#8](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/8) | [#10](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/10)
- `week-5/` — RAG Pipeline with Retrieval Evaluation: comparing three chunking configurations on precision/recall@3 | [#11](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/11) | [#12](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/12)
- `week-6/` — Advanced Retrieval: Transform and Re-rank: adding a HyDE query transformation and cross-encoder reranking step on top of Week 5's worst-performing chunking config | [#13](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/13) | [#14](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/14) 
- `week-7/` — Adaptation and a production dataset | Zero-shot and dynamic few-shot tied at 99% in distribution; boundary probes split them 87.5% to 75%, so zero-shot shipped | [#15](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/15) | [#16](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/16) 
- `week-8/` - **Capstone: integrated assistant** | 72/72 model-free checks, judge 4.67 / 5.00 / 5.00, and one retrieval failure traced and fixed | [#17](https://github.com/BenMillerDev/Applied-LLM-Systems/issues/17) | [#18](https://github.com/BenMillerDev/Applied-LLM-Systems/pull/18)

Each `week-X/` folder contains that week's notebook(s) and any supporting files for the assignment covered that week.

## How the weeks connect

- **Weeks 1–2: how models read and write text.** Tokens, the forward pass, and sampling.
- **Weeks 3–4: treating prompts and tools as code.** Versioned prompts with measured changes, and a function-calling loop with validated arguments.
- **Weeks 5–7: my own product's data.** Retrieval over NailSalonApp's documentation, improved with HyDE and reranking, then a labeled dataset for its support classifier.
- **Week 8: putting it together.** The capstone reuses the Week 3–6 components almost unchanged and adds a slot-lookup tool, read-only and owner-scoped safety rules, and an LLM judge.

Each week was built on its own branch and merged through a pull request that summarizes the results and links that week's research note, so the commit history follows the course week by week.

## Capstone
A tool-calling assistant for owners of salons that use my app, [NailSalonApp](https://github.com/BenMillerDev/NailSalonApp). It answers from the app's docs (RAG), the owner's settings, and a Python port of the app's real time-slot algorithm.
- **Built from earlier weeks:** Week 3's versioned prompt, Week 4's function calling, Week 5's RAG pipeline, and Week 6's HyDE and reranking.
- **Measured:** on 18 held-out questions it passed all 72 model-free checks, and an LLM judge scored it 4.67 / 5.00 / 5.00 for correctness, groundedness and abstention.
- **Debugged:** one retrieval failure was traced to its cause and fixed, moving the answer from 7th to 1st.
- **See it run:** the [results page](https://benmillerdev.github.io/Applied-LLM-Systems/week-8/results/) shows every evaluation run, with each tool call, the answer and the judge's reasons. No setup or API key needed.

## Technologies

- **Python** for all coursework
- **Jupyter notebooks**, developed primarily in **Google Colab**, with local Jupyter as a fallback
- **Google Gemini API** (free tier) for LLM calls
- **python-dotenv** for local environment variable management (API keys are never committed to the repo)
- **Git / GitHub** for version control, synced directly from Colab
