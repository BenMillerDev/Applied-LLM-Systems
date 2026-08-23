# CLAUDE.md

## Project
Course repository for COSC 650: Applied LLM Systems (Maryville University).
8-week graduate course covering tokenization, transformer architecture,
prompt engineering, function calling, retrieval-augmented generation,
fine-tuning, and evaluation.

## Structure
- week-0/ : environment setup and prerequisites
- week-1/ through week-8/ : weekly assignments and notebooks
- notes/ : research notes and reading annotations (added as needed)
- project/ : final project code and documentation (added later in the course)
- CLAUDE.md : this file
- README.md : human-facing project description

## Conventions
- Notebooks are saved from Google Colab via File > Save a copy in GitHub
- All code is Python 3.11+
- tiktoken is used for tokenization experiments; the Gemini API is used for assignments that call a live model
- API keys are stored in Colab Secrets (or a local .env file when running Jupyter) — never hardcoded in a notebook
- Weekly work happens on a feature branch (e.g. week-1-tokenization), merged into main via pull request — not committed directly to main
- Commits use descriptive messages, not "update" or "fix"

## Do Not
- Delete files or directories without confirming first
- Push to main without checking what is staged
- Commit API keys or any file in .env
