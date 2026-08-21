# Applied-LLM-Systems

Coursework, notebooks, and code for COSC 650 Applied LLM Systems, built around hands-on projects that call real LLM APIs rather than just studying theory.

## Course context

This repository supports **COSC 650: Applied LLM Systems**, an 8-week course at Maryville University focused on the practical engineering side of working with large language models: prompting, evaluation, rate-limited API usage, and building small applications on top of an LLM backend.

## Repository organization

Work is organized by week, with one folder per week of the course:

\```
week-00/   Setup and prerequisites (environment, API keys, Colab/GitHub workflow)
week-01/   ...
week-02/   ...
...
week-08/   ...
\```

Each `week-XX/` folder contains that week's notebook(s) and any supporting files for the assignment covered that week.

## Technologies

- **Python** for all coursework
- **Jupyter notebooks**, developed primarily in **Google Colab**, with local Jupyter as a fallback
- **Google Gemini API** (free tier) for LLM calls
- **python-dotenv** for local environment variable management (API keys are never committed to the repo)
- **Git / GitHub** for version control, synced directly from Colab
