# Saved model responses

This folder holds every model response the Week 8 notebook produced. Because they're saved here:

- **Anyone can rerun the notebook without an API key** and get the same results reported in the notebook and the main README.
- **Reruns don't spend API quota.**
- **The Part 2 and Part 3 scores can't drift between runs.** A model gives slightly different answers from one run to the next, even at temperature 0, so rerunning live would change the numbers.

## Files

| File | What's in it | Key |
|---|---|---|
| `runs.json` | Every full assistant run: the question, the owner it ran as, each tool call with its arguments and result, and the parsed answer, sources and rationale | model, prompt version, HyDE and rerank settings, chunking (only when it isn't `paragraph`), owner id, question |
| `hyde.json` | The hypothetical passage HyDE generated for each search query | model, query |
| `judge.json` | The LLM judge's correctness, groundedness and abstention scores, each with its reason, for every run it graded | judge model, judge prompt version, the run's key |

Each file is a single JSON object keyed by a string that joins those settings with `|`. Changing a setting in the notebook produces a different key, so the notebook makes a fresh run instead of reusing a saved one. That's how the Part 3 rerun with the fixed chunking got new runs while the Part 1 and Part 2 runs stayed as they were.

## How the notebook uses this folder

- **In Colab,** the notebook keeps its working cache in Google Drive (`MyDrive/cosc650_week8/cache`). When it clones the repo, it copies in any file from this folder that the Drive cache doesn't already have.
- **Outside Colab,** it reads and writes `cache/` next to the notebook, which is this folder.

When the notebook needs a model response, it checks the matching file first and only calls the API if the key isn't there. Each new response is saved before it's used.

## Regenerating

Delete a file (or the whole folder, plus the Drive copy in Colab) and run the notebook with `GEMINI_API_KEY` set. Every missing response is made again and saved. The new responses won't match these word for word, so the reported scores may shift slightly.

All salon data in these runs comes from the notebook's mock data. No API keys or real customer data are stored here.
