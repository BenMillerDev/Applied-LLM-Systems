"""
Build index.html, a static page that shows every saved evaluation run from
week8_capstone.ipynb: the tool calls, what they returned, the answer, the
model-free checks and the judge's scores.

Everything on the page comes from files already in week-8/:
  - cache/runs.json, cache/judge.json, cache/hyde.json   the saved model responses
  - week8_capstone.ipynb                                 the model settings, EVAL_CASES and EXAMPLE_QUESTIONS

No model or API key is needed. Run it from anywhere:
    python build_results_page.py
"""
import ast
import json
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent  # week-8/results
WEEK_DIR = HERE.parent                          # week-8, where the notebook and cache live
NOTEBOOK_PATH = WEEK_DIR / 'week8_capstone.ipynb'
CACHE_DIR = WEEK_DIR / 'cache'
TEMPLATE_PATH = HERE / 'results_template.html'
OUTPUT_PATH = HERE / 'index.html'  # index.html, so GitHub Pages serves it at .../week-8/results/

REPO_URL = 'https://github.com/BenMillerDev/Applied-LLM-Systems'

# Notebook settings the page needs. They're read from the notebook's code, so
# the page always matches whatever the notebook last ran with. BRANCH sets where
# the page's notebook and README links point.
NOTEBOOK_CONSTANTS = ['MODEL', 'JUDGE_MODEL', 'TEMPERATURE', 'PROMPT_VERSION', 'JUDGE_PROMPT_VERSION',
                      'USE_HYDE', 'USE_RERANK', 'CHUNKING', 'FIXED_CHUNKING', 'OWNER_ID', 'BRANCH']
NOTEBOOK_LISTS = ['EVAL_CASES', 'EXAMPLE_QUESTIONS']

JUDGE_DIMENSIONS = ['correctness', 'groundedness', 'abstention']

# Part 3's retrieval measurements use the embedding model, which this script
# doesn't load, so they're copied from the outputs of the notebook's Part 3 cells.
PART3_FINDINGS = {
    'case_id': 14,
    'chunk_count_before': 42,
    'chunk_count_after': 40,
    'rank_before': 7,
    'rank_doc_wording': 6,
    'rank_after': 1,
    'sim_whole_paragraph': 0.269,
    'sim_staff_item': 0.499,
    'found_at_3_before': 0.95,
    'found_at_3_after': 1.00,
    'found_at_3_questions': 19,
}


# ---------------------------------------------------------------- notebook


def notebook_code_cells(notebook_path):
    """The source of each code cell, with Colab-only lines (!pip, %magic) removed so it parses as Python."""
    notebook = json.loads(notebook_path.read_text())
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        lines = ''.join(cell['source']).splitlines()
        yield '\n'.join(line for line in lines if not line.lstrip().startswith(('!', '%')))


class ReplaceNames(ast.NodeTransformer):
    """Swap known constant names (like OWNER_ID) for their values, so literal_eval can read the expression."""

    def __init__(self, known_values):
        self.known_values = known_values

    def visit_Name(self, node):
        if node.id in self.known_values:
            return ast.Constant(self.known_values[node.id])
        return node


def read_notebook_values(notebook_path):
    """The NOTEBOOK_CONSTANTS and NOTEBOOK_LISTS assignments, read without running any notebook code."""
    values = {}
    wanted = NOTEBOOK_CONSTANTS + NOTEBOOK_LISTS
    for source in notebook_code_cells(notebook_path):
        for node in ast.parse(source).body:
            if not (isinstance(node, ast.Assign) and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name) and node.targets[0].id in wanted):
                continue
            expression = ReplaceNames(values).visit(node.value)
            values[node.targets[0].id] = ast.literal_eval(expression)
    missing = [name for name in wanted if name not in values]
    if missing:
        raise SystemExit(f'not found in {notebook_path.name}: {", ".join(missing)}')
    return values


# ---------------------------------------------------------------- cache


def load_cache(file_name):
    return json.loads((CACHE_DIR / file_name).read_text())


def run_config(settings, chunking):
    """The settings part of a runs.json key, matching the notebook's run_cache_key."""
    config = (f"{settings['MODEL']}|{settings['PROMPT_VERSION']}"
              f"|hyde={settings['USE_HYDE']}|rerank={settings['USE_RERANK']}")
    if chunking != 'paragraph':
        config += f'|chunking={chunking}'
    return config


def run_key(config, owner_id, question):
    return f'{config}|{owner_id}|{question}'


def judge_key(settings, key_of_run):
    """judge.json keys: judge model | judge prompt version | the graded run's key."""
    return f"{settings['JUDGE_MODEL']}|{settings['JUDGE_PROMPT_VERSION']}|{key_of_run}"


# ---------------------------------------------------------------- model-free checks
# The same checks as the notebook's "Model-free metrics" cell. semantic_sim is left
# out because it needs the embedding model.


def tool_calls(run):
    return [entry for entry in run['call_log'] if 'name' in entry]


def check_tools_called(case, run):
    called = {call['name'] for call in tool_calls(run)}
    return all(called.intersection(acceptable) for acceptable in case['required_tools'])


def check_slot_lookup(case, run):
    expected = case['expected_slot_call']
    if expected is None:
        return None
    for call in tool_calls(run):
        if call['name'] != 'get_available_slots':
            continue
        requested = list(call['args'].get('service_ids', [])) + list(call['args'].get('add_on_ids', []))
        if call['args'].get('date') == expected['date'] and sorted(requested) == sorted(expected['ids']):
            return True
    return False


def passage_has_answer(case, passage):
    return (case.get('fact') is not None and passage['doc'] == case['source_doc']
            and case['fact'].lower() in passage['text'].lower())


def check_evidence_retrieved(case, run):
    if case['fact'] is None:
        return None
    for call in tool_calls(run):
        if call['name'] == 'search_docs' and call['result']['ok']:
            if any(passage_has_answer(case, passage) for passage in call['result']['output']['passages']):
                return True
    return False


def normalize_text(text):
    return text.lower().replace('’', "'")


def check_key_facts(case, run):
    if not case['key_facts']:
        return None
    answer = normalize_text(run['answer'])
    found = sum(any(normalize_text(phrasing) in answer for phrasing in phrasings)
                for phrasings in case['key_facts'])
    return found == len(case['key_facts'])


def check_source_cited(case, run):
    if case['source_doc'] is None:
        return None
    return case['source_doc'] in run['sources']


CHECKS = [
    ('Right tools called', check_tools_called),
    ('Slot lookup used the right date and services', check_slot_lookup),
    ('Search returned the passage with the answer', check_evidence_retrieved),
    ('Key facts in the answer', check_key_facts),
    ('Right doc cited', check_source_cited),
    ('Valid JSON reply', lambda case, run: not run['parse_error']),
]


# ---------------------------------------------------------------- page data


def describe_run(run, case, hyde_passages, settings):
    """A saved run trimmed to what the page shows, with each search passage marked if it holds the answer."""
    steps = []
    for entry in run['call_log']:
        if 'name' not in entry:
            continue
        step = {'turn': entry['turn'], 'tool': entry['name'], 'args': entry['args'], 'result': entry['result']}
        if entry['name'] == 'search_docs' and entry['result']['ok']:
            query = entry['args'].get('query', '')
            step['hyde'] = hyde_passages.get(f"{settings['MODEL']}|{query}") if settings['USE_HYDE'] else None
            for passage in entry['result']['output']['passages']:
                passage['has_answer'] = bool(case) and passage_has_answer(case, passage)
        steps.append(step)
    return {
        'answer': run['answer'],
        'sources': run['sources'],
        'rationale': run['rationale'],
        'parse_error': run['parse_error'],
        'steps': steps,
        'model_calls': run['call_log'][-1]['turn'] + 1,  # one model call per turn, the last one writes the answer
    }


def describe_case(case, run, judgment, hyde_passages, settings):
    if run is None:
        return None
    checks = []
    for label, check in CHECKS:
        result = check(case, run)
        if result is not None:
            checks.append({'label': label, 'passed': bool(result)})
    return {
        'run': describe_run(run, case, hyde_passages, settings),
        'checks': checks,
        'judgment': judgment,
    }


def mean(values):
    values = list(values)
    return round(sum(values) / len(values), 2) if values else None


def summarize(described_cases):
    """Headline numbers for one set of runs: judge means, checks passed, and tool and model calls per answer."""
    described_cases = list(described_cases)
    judged = [described['judgment'] for described in described_cases if described and described['judgment']]
    checks = [check for described in described_cases if described for check in described['checks']]
    runs = [described['run'] for described in described_cases if described]
    return {
        'judge': {dimension: mean(j[dimension]['score'] for j in judged) for dimension in JUDGE_DIMENSIONS},
        'judged_count': len(judged),
        'checks_passed': sum(check['passed'] for check in checks),
        'checks_total': len(checks),
        'tool_calls_per_answer': mean(len(run['steps']) for run in runs),
        'model_calls_per_answer': mean(run['model_calls'] for run in runs),
        'searches_per_answer': mean(sum(step['tool'] == 'search_docs' for step in run['steps']) for run in runs),
    }


def build_page_data(settings, runs, judgments, hyde_passages):
    base_config = run_config(settings, settings['CHUNKING'])
    fixed_config = run_config(settings, settings['FIXED_CHUNKING'])

    def lookup(config, case):
        key = run_key(config, case['owner_id'], case['question'])
        run = runs.get(key)
        judgment = judgments.get(judge_key(settings, key))
        return describe_case(case, run, judgment, hyde_passages, settings)

    cases = []
    for case in settings['EVAL_CASES']:
        cases.append({
            'id': case['id'],
            'category': case['category'],
            'owner_id': case['owner_id'],
            'question': case['question'],
            'reference_answer': case['reference_answer'],
            'should_decline': case['should_decline'],
            'part2': lookup(base_config, case),
            'fixed': lookup(fixed_config, case),
        })

    examples = []
    for number, question in enumerate(settings['EXAMPLE_QUESTIONS'], start=1):
        run = runs.get(run_key(base_config, settings['OWNER_ID'], question))
        if run is not None:
            examples.append({
                'id': f'e{number}',
                'category': 'example',
                'owner_id': settings['OWNER_ID'],
                'question': question,
                'run': describe_run(run, None, hyde_passages, settings),
            })

    return {
        'built': date.today().isoformat(),
        'repo_url': REPO_URL,
        'settings': {name: settings[name] for name in NOTEBOOK_CONSTANTS},
        'summary': {
            'part2': summarize(case['part2'] for case in cases),
            'fixed': summarize(case['fixed'] for case in cases),
        },
        'cases': cases,
        'examples': examples,
        'part3': {**PART3_FINDINGS, 'hyde_for_question': hyde_for_failing_question(settings, hyde_passages)},
    }


def hyde_for_failing_question(settings, hyde_passages):
    """The HyDE passage Part 3 generated for the failing case's full question (not one of the assistant's searches)."""
    for case in settings['EVAL_CASES']:
        if case['id'] == PART3_FINDINGS['case_id']:
            return hyde_passages.get(f"{settings['MODEL']}|{case['question']}")
    return None


def main():
    settings = read_notebook_values(NOTEBOOK_PATH)
    page_data = build_page_data(settings, load_cache('runs.json'), load_cache('judge.json'), load_cache('hyde.json'))

    # '</' inside the embedded JSON would close the <script> tag early
    data_json = json.dumps(page_data, ensure_ascii=False).replace('</', '<\\/')
    page = TEMPLATE_PATH.read_text().replace('__PAGE_DATA__', data_json)
    OUTPUT_PATH.write_text(page)

    part2 = page_data['summary']['part2']
    print(f'wrote {OUTPUT_PATH.name}: {len(page_data["cases"])} cases, {len(page_data["examples"])} examples')
    print(f"  judge means: {part2['judge']}")
    print(f"  checks passed: {part2['checks_passed']} of {part2['checks_total']}")


if __name__ == '__main__':
    main()
