# gen_demo_art_experiment_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_2` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-10 06:04:45 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO
```

### [2] SYSTEM-USER prompt · 2026-08-10 06:04:51 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_tceB4eOwcBAO
type: experiment
title: Real-Data Cache Policy Replay Comparison
summary: >-
  method.py fixes iter-1's silent synthetic-data fallback: it now loads art_T0onLH9xokqw's real-content versioned-resource
  corpus (full_data_out.json, 5307 rows, 30 episodes) via a loud fail-fast dependency loader (asserts the file exists and
  has >=5000 rows, aborting hard rather than silently substituting synthetic data), parses each row's JSON input/version_schedule
  into per-episode call streams and per-resource version schedules, and replays six cache policies against the shared call
  stream: FixedTTL (naive baseline, ttl in {1,3,7,14,30}), literal Robbins-Monro d-TTL (target_hit_rate in {0.5,0.7,0.9}),
  EWMA-adaptive TTL (alpha in {0.1,0.3,0.5}), FreshCache exponential-hazard gating in both a raw per-call-site fit and a resource-class-pooled
  fit (error_budget in {0.10,0.20,0.35}), and AIMD window adaptation with a widened 9-combo (a,b) grid (a in {0.1,0.25,0.5}
  x b in {0.5,0.7,0.9}). All policies share one PolicyBase decide/update interface keyed by call_site_signature, so the only
  difference between methods is the adaptation rule, eliminating implementation confounds. Each policy decides serve_cache
  vs refresh at every call, and staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check
  (ablated over spot_check_rate in {0.10,0.20,0.40}, with the 0.20 headline rate swept for every policy and the full ablation
  reserved for AIMD to bound grid size, an explicit scoping decision logged at runtime). An explicit synthetic Zipf-popularity
  simulator (30 episodes, ~1600 calls, static/periodic/bursty resources with matching schedule-generation logic) is run side-by-side
  as a second, clearly-labeled data_source -- never as a silent fallback for the real corpus. The full grid (2 data sources
  x 44 scoped (policy,knob,spot_rate) cells x 20 replicate seeds = 1760 replicate rows) runs in under 8 seconds on CPU since
  the replay loop is pure-Python dict manipulation over ~5307 (real) or ~1600 (synthetic) calls per replicate. Rather than
  emitting one row per raw call event (which would produce millions of rows), method_out.json emits one row per (data_source,
  policy_name, knob_value, spot_check_rate, seed) replicate, aggregating n_calls, n_served_from_cache, hit_rate, n_stale_served,
  stale_rate_of_served, stale_rate_of_calls, n_spot_checked, mean_adapted_param (mean TTL/window/hazard value at decision
  time), redundant_calls_avoided, and a per-volatility-regime (static/periodic/bursty) breakdown of hit_rate and stale_rate
  -- giving downstream evaluation code everything needed to build Pareto frontiers (hit-rate vs staleness) and Wilson-interval
  confidence bands across the n=20 replicates per cell, without requiring per-call granularity. Output conforms to the exp_gen_sol_out.json
  schema (top-level {metadata, datasets: [{dataset, examples: [{input, output, metadata_*}]}]}), validated via the aii-json
  skill (PASSED). Full/mini/preview variants were generated via the aii-json skill's format script using --format exp_gen_sol_out
  (which slices the nested datasets->examples arrays), and both full_method_out.json and method_out.json (2.4MB each) are
  far under the 100MB file-size-limit threshold. Sanity results: FixedTTL baseline achieves hit_rate~0.82 / stale_rate_of_served~0.13
  on the real corpus vs ~0.03 on synthetic (the real corpus's periodic/bursty resources genuinely churn, unlike most synthetic
  Zipf resources), while FreshCache (raw and pooled) achieves the best combination on real data (hit_rate~0.90, comparable
  staleness to FixedTTL) by adaptively gating reuse per call-site/resource-class hazard estimates -- a clear, non-trivial
  hit-rate/staleness tradeoff surface across all six policies and both data sources, ready for evaluation-stage Pareto-frontier
  and CI analysis.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually
Raw data URL: https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json"
import json, os

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    if os.path.exists("mini_demo_data.json"):
        with open("mini_demo_data.json") as f: return json.load(f)
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-10 06:04:51 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [4] TOOL CALL — Bash · 2026-08-10 06:04:57 UTC

```
ls -la && ls /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/
```

### [5] TOOL RESULT — Bash · 2026-08-10 06:04:57 UTC

```
{"stdout": "total 1996\ndrwxr-xr-x 2 root root 1003502 Aug 10 06:04 .\ndrwxr-xr-x 4 root root 1003502 Aug 10 05:33 ..\n-rw-r--r-- 1 root root   35863 Aug 10 06:04 .repl_agent.ptylog\nfull_method_out.json\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\npreview_method_out.json\npyproject.toml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Skill · 2026-08-10 06:04:57 UTC

```
aii-colab
```

### [7] TOOL CALL — Skill · 2026-08-10 06:04:57 UTC

```
aii-long-running-tasks
```

### [8] TOOL RESULT — Skill · 2026-08-10 06:04:57 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [9] TOOL RESULT — Skill · 2026-08-10 06:04:57 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [10] TOOL CALL — Read · 2026-08-10 06:05:01 UTC

```
/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/method.py
```

### [11] TOOL RESULT — Read · 2026-08-10 06:05:01 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/method.py", "content": "#!/usr/bin/env python3\n\"\"\"Cache-policy replay comparison over a real-content versioned corpus + a synthetic Zipf simulator.\n\nImplements 5 cache policies (fixed TTL, literal d-TTL, EWMA-adaptive TTL, FreshCache\nhazard-gate [raw + resource-class-pooled variants], AIMD window) and replays them against\na per-call ev... [truncated, 28490 chars total]
```

### [12] TOOL CALL — Bash · 2026-08-10 06:05:01 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/ && head -c 3000 preview_method_out.json; echo; echo "---"; python3 -c "
import json
d=json.load(open('preview_method_out.json'))
print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
"
```

### [13] TOOL RESULT — Bash · 2026-08-10 06:05:01 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"description\": \"Cache-policy replay comparison (fixed TTL, d-TTL, EWMA-adaptive, FreshCache raw+pooled, AIMD) over the real versioned-resource corpus (art_T0onLH9xokqw) and an explicit synthetic Zipf-popularity simul...\",\n    \"policies_and_knobs\": {\n      \"fixed_ttl\": [\n        1,\n        3,\n        7\n      ],\n      \"d_ttl\": [\n        0.5,\n        0.7,\n        0.9\n      ],\n      \"ewma_adaptive\": [\n        0.1,\n        0.3,\n        0.5\n      ],\n      \"freshcache_raw\": [\n        0.1,\n        0.2,\n        0.35\n      ],\n      \"freshcache_pooled\": [\n        0.1,\n        0.2,\n        0.35\n      ],\n      \"aimd\": [\n        [\n          0.1,\n          0.5\n        ],\n        [\n          0.1,\n          0.7\n        ],\n        [\n          0.1,\n          0.9\n        ]\n      ]\n    },\n    \"n_replicates\": 20,\n    \"spot_check_rates_tested\": [\n      0.1,\n      0.2,\n      0.4\n    ],\n    \"headline_spot_check_rate\": 0.2,\n    \"data_sources\": [\n      \"real_corpus\",\n      \"synthetic_zipf\"\n    ],\n    \"dependency_verified\": {\n      \"path\": \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json\",\n      \"n_rows_loaded\": 5307\n    },\n    \"n_cells\": 88,\n    \"n_total_replicate_rows\": 1760,\n    \"mode\": \"full\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"cache_policy_replay_real_corpus\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"data_source\\\": \\\"real_corpus\\\", \\\"policy_name\\\": \\\"fixed_ttl\\\", \\\"knob_value\\\": 1, \\\"spot_check_rate\\\": 0.2, \\\"seed\\\": 0, \\\"n_episodes\\\": 30, \\\"n_calls\\\": 5307}\",\n          \"output\": \"{\\\"hit_rate\\\": 0.6947427925381572, \\\"stale_rate_of_served\\\": 0.11282885815025766, \\\"mean_adapted_param\\\": 1.0}\",\n          \"metadata_policy_name\": \"fixed_ttl\",\n          \"metadata_knob_value\": \"1\",\n          \"metadata_data_source\": \"real_corpus\",\n          \"metadata_spot_check_rate\": 0.2,\n          \"metadata_seed\": 0,\n          \"metadata_n_calls\": 5307,\n          \"metadata_n_served_from_cache\": 3687,\n          \"metadata_hit_rate\": 0.6947427925381572,\n          \"metadata_n_stale_served\": 416,\n          \"metadata_stale_rate_of_served\": 0.11282885815025766,\n          \"metadata_stale_rate_of_calls\": 0.07838703599020162,\n          \"metadata_n_spot_checked\": 1041,\n          \"metadata_mean_adapted_param\": 1.0,\n          \"metadata_redundant_calls_avoided\": 3687,\n          \"metadata_regime_breakdown\": \"{\\\"static\\\": {\\\"n\\\": 4226, \\\"hit_rate\\\": 0.6644581164221486, \\\"stale_rate_of_served\\\": 0.002492877492877493}, \\\"periodic\\\": {\\\"n\\\": 995, \\\"hit_rate\\\": 0.8140703517587939, \\\"stale_rate_of_served\\\": 0.4604938271604938}...\",\n          \"metadata_is_baseline\": true,\n          \"predict_fixed_ttl\": \"{\\\"hit_rate\\\": 0.6947427925381572, \\\"stale_rate_of_served\\\": 0.11282885815025766, \\\"mean_adapted_param\\\": 1.0}\"\n        },\n        {\n          \"input\": \"{\\\"data_source\\\": \\\"real_corpus\\\", \\\"policy_name\\\": \\\"fixed_ttl\\\", \\\"knob_value\\\": 1, \\\"spot_check_rate\\\": 0.2, \\\"seed\\\": 1, \\\"n_episodes\\\": 30, \\\"n_calls\\\":\n---\n<class 'dict'> ['metadata', 'datasets']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-08-10 06:05:07 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/ 2>/dev/null && ls -la || find /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/ -maxdepth 1
```

### [15] TOOL RESULT — Bash · 2026-08-10 06:05:07 UTC

```
{"stdout": "total 18380\ndrwxr-xr-x 5 root   root   3000442 Aug  9 23:45 .\ndrwxr-xr-x 5 root   root   3000485 Aug  9 22:54 ..\n-rw-r--r-- 1 231072 231072 1201434 Aug  9 23:45 .repl_agent.ptylog\n-rw-r--r-- 1 231072 231072    4371 Aug  9 23:45 .terminal_claude_agent_struct_out.json\ndrwxr-xr-x 4 231072 231072 1048539 Aug  9 23:40 .venv\n-rw-rw-rw- 1 231072 231072   20179 Aug  9 23:43 data.py\n-rw-r--r-- 1 root   root   6535022 Aug  9 23:44 full_data_out.json\ndrwxr-xr-x 2 231072 231072 1000580 Aug  9 23:40 logs\n-rw-r--r-- 1 root   root      2838 Aug  9 23:44 mini_data_out.json\n-rw-r--r-- 1 root   root      2703 Aug  9 23:44 preview_data_out.json\n-rw-r--r-- 1 231072 231072     124 Aug  9 23:44 pyproject.toml\ndrwxr-xr-x 4 231072 231072 3000442 Aug  9 23:37 temp", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-08-10 06:05:13 UTC

```
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'))
ds=d['datasets']
print(len(ds))
ex=ds[0]['examples']
print(len(ex))
print(ex[0])
regimes={}
episodes=set()
for e in ex:
    r=e['metadata_volatility_regime']
    regimes[r]=regimes.get(r,0)+1
    inp=json.loads(e['input'])
    episodes.add(inp['episode_id'])
print(regimes)
print(len(episodes))
"
```

### [17] TOOL RESULT — Bash · 2026-08-10 06:05:13 UTC

```
{"stdout": "1\n5307\n{'input': '{\"episode_id\": \"ep_000\", \"call_index\": 0, \"timestamp_tick\": 1, \"call_site_signature\": \"web_search(query=\\'What happens after you die? (Human Being)\\')\", \"resource_id\": \"snip_qqp_0109\"}', 'output': 'snip_qqp_0109_v0', 'metadata_resource_class': 'search_snippet', 'metadata_volatility_regime': 'static', 'metadata_timing_provenance': 'real_single_snapshot', 'metadata_content_now': 'What happens after you die? (Human Being)', 'metadata_version_schedule': '[{\"version_id\": \"snip_qqp_0109_v0\", \"content_hash\": \"09ff427a59ee5644\", \"valid_from_tick\": 0, \"valid_until_tick\": 29}]', 'metadata_checked': False, 'metadata_sim_days': 30}\n{'static': 4226, 'periodic': 995, 'bursty': 86}\n30", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-08-10 06:05:19 UTC

```
Now let me build a mini subset with a handful of full episodes (to preserve realistic replay dynamics) covering all three regimes.
```

### [19] TOOL CALL — Bash · 2026-08-10 06:05:19 UTC

```
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'))
ex=d['datasets'][0]['examples']
from collections import defaultdict
by_ep=defaultdict(list)
ep_regimes={}
for e in ex:
    inp=json.loads(e['input'])
    by_ep[inp['episode_id']].append(e)
    ep_regimes.setdefault(inp['episode_id'], set()).add(e['metadata_volatility_regime'])
# pick episodes with mixed regimes and reasonably small
sizes=sorted(((len(v), k) for k,v in by_ep.items()))
print(sizes[:10])
for k in list(by_ep.keys())[:5]:
    print(k, len(by_ep[k]), ep_regimes[k])
"
```

### [20] TOOL RESULT — Bash · 2026-08-10 06:05:19 UTC

```
{"stdout": "[(139, 'ep_019'), (148, 'ep_024'), (149, 'ep_017'), (153, 'ep_025'), (158, 'ep_001'), (158, 'ep_007'), (161, 'ep_020'), (162, 'ep_000'), (164, 'ep_023'), (165, 'ep_013')]\nep_000 162 {'static', 'bursty', 'periodic'}\nep_001 158 {'static', 'periodic'}\nep_002 198 {'static', 'periodic'}\nep_003 219 {'static', 'bursty', 'periodic'}\nep_004 191 {'static', 'periodic'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-08-10 06:05:21 UTC

```
Every episode is already small (~150-220 rows). I'll pick 3 episodes covering all regimes, keeping total under 100... actually the task says "no more than 100 diverse examples" — let me pick one smallest episode with all three regimes.
```

### [22] TOOL CALL — Bash · 2026-08-10 06:05:21 UTC

```
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'))
ex=d['datasets'][0]['examples']
from collections import defaultdict
by_ep=defaultdict(list)
for e in ex:
    inp=json.loads(e['input'])
    by_ep[inp['episode_id']].append(e)
# ep_019 smallest at 139, check regimes
for k in ['ep_019','ep_024','ep_017']:
    regs=set(e['metadata_volatility_regime'] for e in by_ep[k])
    print(k, len(by_ep[k]), regs)
"
```

### [23] TOOL RESULT — Bash · 2026-08-10 06:05:21 UTC

```
{"stdout": "ep_019 139 {'static', 'periodic'}\nep_024 148 {'static', 'periodic'}\nep_017 149 {'static', 'periodic'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — ToolSearch · 2026-08-10 06:05:27 UTC

```
{'query': 'select:TaskCreate,TaskUpdate'}
```

### [25] TOOL RESULT — ToolSearch · 2026-08-10 06:05:27 UTC

```
{"matches": ["TaskCreate", "TaskUpdate"], "query": "select:TaskCreate,TaskUpdate", "total_deferred_tools": 22}
```

### [26] TOOL CALL — Bash · 2026-08-10 06:05:27 UTC

```
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'))
ex=d['datasets'][0]['examples']
from collections import defaultdict
by_ep=defaultdict(list)
for e in ex:
    inp=json.loads(e['input'])
    by_ep[inp['episode_id']].append(e)
sel = by_ep['ep_000'] + by_ep['ep_003']
regs=defaultdict(int)
for e in sel: regs[e['metadata_volatility_regime']]+=1
print(len(sel), regs)
mini = {'datasets':[{'dataset':'cache_replay_source_rows','examples':sel}]}
import pathlib
out='/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json'
json.dump(mini, open(out,'w'), indent=2)
print('wrote', out)
"
```

### [27] TOOL RESULT — Bash · 2026-08-10 06:05:27 UTC

```
{"stdout": "381 defaultdict(<class 'int'>, {'static': 298, 'periodic': 77, 'bursty': 6})\nwrote /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-08-10 06:05:37 UTC

```
python3 -c "
import json
from collections import defaultdict
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'))
ex=d['datasets'][0]['examples']
by_ep=defaultdict(list)
for e in ex:
    inp=json.loads(e['input'])
    by_ep[inp['episode_id']].append((inp['call_index'], e))
sel = sorted(by_ep['ep_000'], key=lambda x: x[0])[:100]
sel = [e for _,e in sel]
regs=defaultdict(int)
for e in sel: regs[e['metadata_volatility_regime']]+=1
print(len(sel), regs)
mini = {'datasets':[{'dataset':'cache_replay_source_rows','examples':sel}]}
out='/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json'
json.dump(mini, open(out,'w'), indent=2)
print('wrote', out)
"
ls -la /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json
```

### [29] TOOL RESULT — Bash · 2026-08-10 06:05:37 UTC

```
{"stdout": "100 defaultdict(<class 'int'>, {'static': 79, 'periodic': 18, 'bursty': 3})\nwrote /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json\n-rw-r--r-- 1 root root 125736 Aug 10 06:05 /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-08-10 06:05:41 UTC

```
Good, 100 examples covering all three volatility regimes, 122KB. Now let's build the notebook.
```

### [31] TOOL CALL — ToolSearch · 2026-08-10 06:05:41 UTC

```
{'query': 'select:NotebookEdit'}
```

### [32] TOOL RESULT — ToolSearch · 2026-08-10 06:05:41 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit", "total_deferred_tools": 22}
```

### [33] TOOL CALL — Write · 2026-08-10 06:05:47 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb

{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# placeholder"]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.12"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

### [34] TOOL RESULT — Write · 2026-08-10 06:05:47 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "content": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"]\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [35] TOOL CALL — Read · 2026-08-10 06:05:47 UTC

```
/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb
```

### [36] TOOL RESULT — Read · 2026-08-10 06:05:47 UTC

```
{"type": "notebook", "file": {"filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "cells": [{"cellType": "markdown", "source": "# placeholder", "cell_id": "cell-0"}]}}
```

### [37] ASSISTANT · 2026-08-10 06:05:57 UTC

```
Now building out the full notebook cell by cell.
```

### [38] TOOL CALL — NotebookEdit · 2026-08-10 06:05:57 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'cell-0', 'new_source': '# Real-Data Cache Policy Replay Comparison\n\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\n\nIt loads a real-content corpus of versioned "resources" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\n\n- **FixedTTL** — naive fixed time-to-live baseline\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource\'s *class* (fixes small-sample calibration)\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\n\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\n\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.'}
```

### [39] TOOL RESULT — NotebookEdit · 2026-08-10 06:05:57 UTC

```
{"new_source": "# Real-Data Cache Policy Replay Comparison\n\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\n\nIt loads a real-content corpus of versioned \"resources\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\n\n- **FixedTTL** — naive fixed time-to-live baseline\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\n\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\n\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.", "old_source": "# placeholder", "cell_type": "code", "language": "python", "edit_mode": "replace", "cell_id": "cell-0", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"]\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [40] TOOL CALL — NotebookEdit · 2026-08-10 06:06:01 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'cell-0', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru -- not pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\nif 'google.colab' not in sys.modules:\n    _pip('matplotlib==3.10.0')"}
```

### [41] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:01 UTC

```
{"new_source": "import subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru -- not pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\nif 'google.colab' not in sys.modules:\n    _pip('matplotlib==3.10.0')", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "784e6813", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [42] TOOL CALL — NotebookEdit · 2026-08-10 06:06:13 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '784e6813', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'import json\nimport random\nimport sys\nfrom collections import defaultdict\n\nfrom loguru import logger\nimport matplotlib.pyplot as plt\n\nlogger.remove()\nlogger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")'}
```

### [43] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:13 UTC

```
{"new_source": "import json\nimport random\nimport sys\nfrom collections import defaultdict\n\nfrom loguru import logger\nimport matplotlib.pyplot as plt\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "a3925155", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [44] TOOL CALL — NotebookEdit · 2026-08-10 06:06:13 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'a3925155', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json"\nimport os\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception:\n        pass\n    if os.path.exists("mini_demo_data.json"):\n        with open("mini_demo_data.json") as f:\n            return json.load(f)\n    raise FileNotFoundError("Could not load mini_demo_data.json")'}
```

### [45] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:13 UTC

```
{"new_source": "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\"\nimport os\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception:\n        pass\n    if os.path.exists(\"mini_demo_data.json\"):\n        with open(\"mini_demo_data.json\") as f:\n            return json.load(f)\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "4ea43811", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [46] TOOL CALL — NotebookEdit · 2026-08-10 06:06:17 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '4ea43811', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'data = load_data()\nprint(f"Loaded {sum(len(ds[\'examples\']) for ds in data[\'datasets\'])} rows from {len(data[\'datasets\'])} dataset(s)")'}
```

### [47] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:17 UTC

```
{"new_source": "data = load_data()\nprint(f\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "176e7fa4", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [48] ASSISTANT · 2026-08-10 06:06:29 UTC

```
Now the config cell and markdown before it.
```

### [49] TOOL CALL — NotebookEdit · 2026-08-10 06:06:29 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '176e7fa4', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Configuration\n\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).'}
```

### [50] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:29 UTC

```
{"new_source": "## Configuration\n\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "7f68f6e6", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [51] TOOL CALL — NotebookEdit · 2026-08-10 06:06:35 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '7f68f6e6', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': '# N_REPLICATES = 20  # original full-run value\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\n\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\n\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\n\nSYNTH_SEED = 12345\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\nSYNTH_SIM_DAYS = 30'}
```

### [52] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:35 UTC

```
{"new_source": "# N_REPLICATES = 20  # original full-run value\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\n\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\n\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\n\nSYNTH_SEED = 12345\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\nSYNTH_SIM_DAYS = 30", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "f43d1a5b", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [53] ASSISTANT · 2026-08-10 06:06:39 UTC

```
Now the parsing section (loading + parsing rows into episodes).
```

### [54] TOOL CALL — NotebookEdit · 2026-08-10 06:06:39 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'f43d1a5b', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## 0. Parse rows into per-episode call streams\n\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above)."}
```

### [55] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:39 UTC

```
{"new_source": "## 0. Parse rows into per-episode call streams\n\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "73b4de9c", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"73b4de9c\",\n   \"source\": \"## 0. Parse rows into per-episode call streams\\n\\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [56] TOOL CALL — NotebookEdit · 2026-08-10 06:06:45 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '73b4de9c', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def parse_rows_into_episodes(rows):\n    episodes = defaultdict(list)\n    resource_schedules = {}\n    regime_counts = defaultdict(int)\n    malformed = 0\n    for r in rows:\n        try:\n            inp = json.loads(r["input"])\n            sched = json.loads(r["metadata_version_schedule"])\n        except (json.JSONDecodeError, KeyError):\n            malformed += 1\n            continue\n        resource_schedules[inp["resource_id"]] = sched\n        regime = r["metadata_volatility_regime"]\n        regime_counts[regime] += 1\n        episodes[inp["episode_id"]].append(\n            {\n                "call_index": inp["call_index"],\n                "timestamp_tick": inp["timestamp_tick"],\n                "call_site_signature": inp["call_site_signature"],\n                "resource_id": inp["resource_id"],\n                "ground_truth_version_id": r["output"],\n                "volatility_regime": regime,\n                "resource_class": r["metadata_resource_class"],\n            }\n        )\n    frac_malformed = malformed / max(1, len(rows))\n    if frac_malformed > 0.01:\n        logger.warning(\n            f"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- "\n            f"exceeds 1% threshold, but continuing with the rows that did parse."\n        )\n    for ep in episodes:\n        episodes[ep].sort(key=lambda c: (c["timestamp_tick"], c["call_index"]))\n    logger.info(f"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources")\n    logger.info(f"Volatility regime distribution: {dict(regime_counts)}")\n    missing_regimes = {"static", "periodic", "bursty"} - set(regime_counts)\n    if missing_regimes:\n        logger.warning(f"Missing volatility regimes in parsed data: {missing_regimes}")\n    return dict(episodes), resource_schedules\n\n\nrows_raw = [ex for ds in data["datasets"] for ex in ds["examples"]]\nepisodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)'}
```

### [57] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:45 UTC

```
{"new_source": "def parse_rows_into_episodes(rows):\n    episodes = defaultdict(list)\n    resource_schedules = {}\n    regime_counts = defaultdict(int)\n    malformed = 0\n    for r in rows:\n        try:\n            inp = json.loads(r[\"input\"])\n            sched = json.loads(r[\"metadata_version_schedule\"])\n        except (json.JSONDecodeError, KeyError):\n            malformed += 1\n            continue\n        resource_schedules[inp[\"resource_id\"]] = sched\n        regime = r[\"metadata_volatility_regime\"]\n        regime_counts[regime] += 1\n        episodes[inp[\"episode_id\"]].append(\n            {\n                \"call_index\": inp[\"call_index\"],\n                \"timestamp_tick\": inp[\"timestamp_tick\"],\n                \"call_site_signature\": inp[\"call_site_signature\"],\n                \"resource_id\": inp[\"resource_id\"],\n                \"ground_truth_version_id\": r[\"output\"],\n                \"volatility_regime\": regime,\n                \"resource_class\": r[\"metadata_resource_class\"],\n            }\n        )\n    frac_malformed = malformed / max(1, len(rows))\n    if frac_malformed > 0.01:\n        logger.warning(\n            f\"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- \"\n            f\"exceeds 1% threshold, but continuing with the rows that did parse.\"\n        )\n    for ep in episodes:\n        episodes[ep].sort(key=lambda c: (c[\"timestamp_tick\"], c[\"call_index\"]))\n    logger.info(f\"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources\")\n    logger.info(f\"Volatility regime distribution: {dict(regime_counts)}\")\n    missing_regimes = {\"static\", \"periodic\", \"bursty\"} - set(regime_counts)\n    if missing_regimes:\n        logger.warning(f\"Missing volatility regimes in parsed data: {missing_regimes}\")\n    return dict(episodes), resource_schedules\n\n\nrows_raw = [ex for ds in data[\"datasets\"] for ex in ds[\"examples\"]]\nepisodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "e946423a", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"73b4de9c\",\n   \"source\": \"## 0. Parse rows into per-episode call streams\\n\\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"73b4de9c\",\n   \"source\": \"## 0. Parse rows into per-episode call streams\\n\\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e946423a\",\n   \"source\": \"def parse_rows_into_episodes(rows):\\n    episodes = defaultdict(list)\\n    resource_schedules = {}\\n    regime_counts = defaultdict(int)\\n    malformed = 0\\n    for r in rows:\\n        try:\\n            inp = json.loads(r[\\\"input\\\"])\\n            sched = json.loads(r[\\\"metadata_version_schedule\\\"])\\n        except (json.JSONDecodeError, KeyError):\\n            malformed += 1\\n            continue\\n        resource_schedules[inp[\\\"resource_id\\\"]] = sched\\n        regime = r[\\\"metadata_volatility_regime\\\"]\\n        regime_counts[regime] += 1\\n        episodes[inp[\\\"episode_id\\\"]].append(\\n            {\\n                \\\"call_index\\\": inp[\\\"call_index\\\"],\\n                \\\"timestamp_tick\\\": inp[\\\"timestamp_tick\\\"],\\n                \\\"call_site_signature\\\": inp[\\\"call_site_signature\\\"],\\n                \\\"resource_id\\\": inp[\\\"resource_id\\\"],\\n                \\\"ground_truth_version_id\\\": r[\\\"output\\\"],\\n                \\\"volatility_regime\\\": regime,\\n                \\\"resource_class\\\": r[\\\"metadata_resource_class\\\"],\\n            }\\n        )\\n    frac_malformed = malformed / max(1, len(rows))\\n    if frac_malformed > 0.01:\\n        logger.warning(\\n            f\\\"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- \\\"\\n            f\\\"exceeds 1% threshold, but continuing with the rows that did parse.\\\"\\n        )\\n    for ep in episodes:\\n        episodes[ep].sort(key=lambda c: (c[\\\"timestamp_tick\\\"], c[\\\"call_index\\\"]))\\n    logger.info(f\\\"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources\\\")\\n    logger.info(f\\\"Volatility regime distribution: {dict(regime_counts)}\\\")\\n    missing_regimes = {\\\"static\\\", \\\"periodic\\\", \\\"bursty\\\"} - set(regime_counts)\\n    if missing_regimes:\\n        logger.warning(f\\\"Missing volatility regimes in parsed data: {missing_regimes}\\\")\\n    return dict(episodes), resource_schedules\\n\\n\\nrows_raw = [ex for ds in data[\\\"datasets\\\"] for ex in ds[\\\"examples\\\"]]\\nepisodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [58] ASSISTANT · 2026-08-10 06:06:53 UTC

```
Now the synthetic Zipf simulator section (section 1).
```

### [59] TOOL CALL — NotebookEdit · 2026-08-10 06:06:53 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'e946423a', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## 1. Synthetic Zipf-popularity simulator\n\nAs a second, explicitly-labeled `data_source` (never a silent fallback for the real corpus), the original script also builds a synthetic corpus: resources with `static`/`periodic`/`bursty` version schedules, and episodes that draw resources with Zipf(s=1.2) popularity weights. This is run side-by-side with the real corpus so the comparison isn't purely single-source."}
```

### [60] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:53 UTC

```
{"new_source": "## 1. Synthetic Zipf-popularity simulator\n\nAs a second, explicitly-labeled `data_source` (never a silent fallback for the real corpus), the original script also builds a synthetic corpus: resources with `static`/`periodic`/`bursty` version schedules, and episodes that draw resources with Zipf(s=1.2) popularity weights. This is run side-by-side with the real corpus so the comparison isn't purely single-source.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "1b7a7a5f", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"73b4de9c\",\n   \"source\": \"## 0. Parse rows into per-episode call streams\\n\\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e946423a\",\n   \"source\": \"def parse_rows_into_episodes(rows):\\n    episodes = defaultdict(list)\\n    resource_schedules = {}\\n    regime_counts = defaultdict(int)\\n    malformed = 0\\n    for r in rows:\\n        try:\\n            inp = json.loads(r[\\\"input\\\"])\\n            sched = json.loads(r[\\\"metadata_version_schedule\\\"])\\n        except (json.JSONDecodeError, KeyError):\\n            malformed += 1\\n            continue\\n        resource_schedules[inp[\\\"resource_id\\\"]] = sched\\n        regime = r[\\\"metadata_volatility_regime\\\"]\\n        regime_counts[regime] += 1\\n        episodes[inp[\\\"episode_id\\\"]].append(\\n            {\\n                \\\"call_index\\\": inp[\\\"call_index\\\"],\\n                \\\"timestamp_tick\\\": inp[\\\"timestamp_tick\\\"],\\n                \\\"call_site_signature\\\": inp[\\\"call_site_signature\\\"],\\n                \\\"resource_id\\\": inp[\\\"resource_id\\\"],\\n                \\\"ground_truth_version_id\\\": r[\\\"output\\\"],\\n                \\\"volatility_regime\\\": regime,\\n                \\\"resource_class\\\": r[\\\"metadata_resource_class\\\"],\\n            }\\n        )\\n    frac_malformed = malformed / max(1, len(rows))\\n    if frac_malformed > 0.01:\\n        logger.warning(\\n            f\\\"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- \\\"\\n            f\\\"exceeds 1% threshold, but continuing with the rows that did parse.\\\"\\n        )\\n    for ep in episodes:\\n        episodes[ep].sort(key=lambda c: (c[\\\"timestamp_tick\\\"], c[\\\"call_index\\\"]))\\n    logger.info(f\\\"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources\\\")\\n    logger.info(f\\\"Volatility regime distribution: {dict(regime_counts)}\\\")\\n    missing_regimes = {\\\"static\\\", \\\"periodic\\\", \\\"bursty\\\"} - set(regime_counts)\\n    if missing_regimes:\\n        logger.warning(f\\\"Missing volatility regimes in parsed data: {missing_regimes}\\\")\\n    return dict(episodes), resource_schedules\\n\\n\\nrows_raw = [ex for ds in data[\\\"datasets\\\"] for ex in ds[\\\"examples\\\"]]\\nepisodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"metadata\": {},\n   \"source\": \"# Real-Data Cache Policy Replay Comparison\\n\\nThis notebook is a runnable demo of `method.py`, which asks: **does a simple, well-specified cache-refresh policy measurably reduce redundant LLM tool calls, and what does it cost in staleness?**\\n\\nIt loads a real-content corpus of versioned \\\"resources\\\" (tool-call results whose ground-truth content changes over time on `static` / `periodic` / `bursty` schedules), reconstructs the original per-episode call streams, and replays **six cache policies** against those streams:\\n\\n- **FixedTTL** — naive fixed time-to-live baseline\\n- **d-TTL** — literal Robbins-Monro stochastic-approximation TTL targeting a hit rate\\n- **EWMA-adaptive TTL** — TTL driven by an exponentially-weighted moving average of observed staleness\\n- **FreshCache (raw)** — per-call-site exponential-hazard gate on reuse probability\\n- **FreshCache (pooled)** — same hazard gate, but hazard stats pooled across a resource's *class* (fixes small-sample calibration)\\n- **AIMD** — additive-increase/multiplicative-decrease window adaptation\\n\\nAll six share one `PolicyBase.decide/update` interface keyed by `call_site_signature`, so the only difference between them is the adaptation rule -- eliminating implementation confounds. Staleness feedback is only revealed when a call is refreshed or hits a randomly-drawn spot-check, mimicking a realistic partial-observability setting.\\n\\nThis demo uses a small curated subset of the real corpus (`mini_demo_data.json`, 100 rows from one episode spanning all three volatility regimes) so it runs in seconds, plus the full synthetic Zipf-popularity simulator run side-by-side exactly as in the original script.\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"784e6813\",\n   \"source\": \"import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# loguru -- not pre-installed on Colab, always install\\n_pip('loguru==0.7.3')\\n\\n# matplotlib -- pre-installed on Colab, install locally only (to match Colab's exact version)\\nif 'google.colab' not in sys.modules:\\n    _pip('matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"a3925155\",\n   \"source\": \"import json\\nimport random\\nimport sys\\nfrom collections import defaultdict\\n\\nfrom loguru import logger\\nimport matplotlib.pyplot as plt\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"4ea43811\",\n   \"source\": \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception:\\n        pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f:\\n            return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"176e7fa4\",\n   \"source\": \"data = load_data()\\nprint(f\\\"Loaded {sum(len(ds['examples']) for ds in data['datasets'])} rows from {len(data['datasets'])} dataset(s)\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"7f68f6e6\",\n   \"source\": \"## Configuration\\n\\nAll tunable parameters are gathered here. `N_REPLICATES` controls how many random seeds each (policy, knob, spot-check-rate) cell is replayed with (the original defaults to 20 for a full run); `MAX_CELLS` caps how many distinct (policy, knob, spot_rate) cells actually get replayed, keeping this demo fast. Both are set to the smallest values that still produce a meaningful comparison across all six policies; increase them to scale up towards the original full-run values (commented below).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"f43d1a5b\",\n   \"source\": \"# N_REPLICATES = 20  # original full-run value\\nN_REPLICATES = 2       # replicate seeds per (policy, knob, spot_check_rate) cell -- minimal demo value\\n\\nMAX_CELLS = None       # cap on number of distinct (policy, knob, spot_rate) cells to run (None = no cap)\\n\\nSPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # spot-check ablation grid (unchanged from original)\\nHEADLINE_RATE = 0.20                     # headline spot-check rate swept for every policy\\n\\nSYNTH_SEED = 12345\\nSYNTH_N_EPISODES = 30   # synthetic Zipf simulator episode count (unchanged from original -- already fast)\\nSYNTH_SIM_DAYS = 30\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"73b4de9c\",\n   \"source\": \"## 0. Parse rows into per-episode call streams\\n\\nThe real corpus is a flat list of rows, each row a single tool-call event whose `input` (JSON string) carries the episode/call/resource identifiers and whose `metadata_version_schedule` carries that resource's full version history. `parse_rows_into_episodes` groups rows back into per-episode, time-ordered call streams and per-resource version schedules -- this is exactly the logic `method.py` runs after its fail-fast dependency loader confirms the corpus file is present and non-truncated (the loud fail-fast check itself is omitted here since `data` is already loaded from `mini_demo_data.json` above).\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e946423a\",\n   \"source\": \"def parse_rows_into_episodes(rows):\\n    episodes = defaultdict(list)\\n    resource_schedules = {}\\n    regime_counts = defaultdict(int)\\n    malformed = 0\\n    for r in rows:\\n        try:\\n            inp = json.loads(r[\\\"input\\\"])\\n            sched = json.loads(r[\\\"metadata_version_schedule\\\"])\\n        except (json.JSONDecodeError, KeyError):\\n            malformed += 1\\n            continue\\n        resource_schedules[inp[\\\"resource_id\\\"]] = sched\\n        regime = r[\\\"metadata_volatility_regime\\\"]\\n        regime_counts[regime] += 1\\n        episodes[inp[\\\"episode_id\\\"]].append(\\n            {\\n                \\\"call_index\\\": inp[\\\"call_index\\\"],\\n                \\\"timestamp_tick\\\": inp[\\\"timestamp_tick\\\"],\\n                \\\"call_site_signature\\\": inp[\\\"call_site_signature\\\"],\\n                \\\"resource_id\\\": inp[\\\"resource_id\\\"],\\n                \\\"ground_truth_version_id\\\": r[\\\"output\\\"],\\n                \\\"volatility_regime\\\": regime,\\n                \\\"resource_class\\\": r[\\\"metadata_resource_class\\\"],\\n            }\\n        )\\n    frac_malformed = malformed / max(1, len(rows))\\n    if frac_malformed > 0.01:\\n        logger.warning(\\n            f\\\"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- \\\"\\n            f\\\"exceeds 1% threshold, but continuing with the rows that did parse.\\\"\\n        )\\n    for ep in episodes:\\n        episodes[ep].sort(key=lambda c: (c[\\\"timestamp_tick\\\"], c[\\\"call_index\\\"]))\\n    logger.info(f\\\"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources\\\")\\n    logger.info(f\\\"Volatility regime distribution: {dict(regime_counts)}\\\")\\n    missing_regimes = {\\\"static\\\", \\\"periodic\\\", \\\"bursty\\\"} - set(regime_counts)\\n    if missing_regimes:\\n        logger.warning(f\\\"Missing volatility regimes in parsed data: {missing_regimes}\\\")\\n    return dict(episodes), resource_schedules\\n\\n\\nrows_raw = [ex for ds in data[\\\"datasets\\\"] for ex in ds[\\\"examples\\\"]]\\nepisodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"1b7a7a5f\",\n   \"source\": \"## 1. Synthetic Zipf-popularity simulator\\n\\nAs a second, explicitly-labeled `data_source` (never a silent fallback for the real corpus), the original script also builds a synthetic corpus: resources with `static`/`periodic`/`bursty` version schedules, and episodes that draw resources with Zipf(s=1.2) popularity weights. This is run side-by-side with the real corpus so the comparison isn't purely single-source.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [61] TOOL CALL — NotebookEdit · 2026-08-10 06:07:05 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '1b7a7a5f', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def build_synthetic_zipf_episodes(seed: int = 12345, n_episodes: int = 30, sim_days: int = 30):\n    rng = random.Random(seed)\n    n_resources_per_regime = {"static": 90, "periodic": 60, "bursty": 20}\n    resource_schedules = {}\n    resource_meta = {}\n    rid_counter = 0\n    for regime, n_res in n_resources_per_regime.items():\n        for _ in range(n_res):\n            rid = f"synth_{regime}_{rid_counter:04d}"\n            rid_counter += 1\n            if regime == "static":\n                sched = [\n                    {\n                        "version_id": f"{rid}_v0",\n                        "content_hash": "synthetic",\n                        "valid_from_tick": 0,\n                        "valid_until_tick": sim_days - 1,\n                    }\n                ]\n            elif regime == "periodic":\n                period = rng.choice([3, 5, 7])\n                sched = []\n                t = 0\n                v = 0\n                while t <= sim_days - 1:\n                    nxt = min(sim_days - 1, t + period - 1)\n                    sched.append(\n                        {\n                            "version_id": f"{rid}_v{v}",\n                            "content_hash": "synthetic",\n                            "valid_from_tick": t,\n                            "valid_until_tick": nxt,\n                        }\n                    )\n                    t = nxt + 1\n                    v += 1\n            else:  # bursty: heavy-tailed irregular intervals (Pareto-ish via exponential mix)\n                sched = []\n                t = 0\n                v = 0\n                while t <= sim_days - 1:\n                    gap = max(1, int(rng.expovariate(1 / 2.0)))\n                    nxt = min(sim_days - 1, t + gap - 1)\n                    sched.append(\n                        {\n                            "version_id": f"{rid}_v{v}",\n                            "content_hash": "synthetic",\n                            "valid_from_tick": t,\n                            "valid_until_tick": nxt,\n                        }\n                    )\n                    t = nxt + 1\n                    v += 1\n            resource_schedules[rid] = sched\n            resource_meta[rid] = regime\n    resource_ids = list(resource_schedules.keys())\n\n    def version_at(rid, tick):\n        for entry in resource_schedules[rid]:\n            if entry["valid_from_tick"] <= tick <= entry["valid_until_tick"]:\n                return entry["version_id"]\n        return resource_schedules[rid][-1]["version_id"]\n\n    # Zipf popularity ranking over resources -> episodes draw with Zipf(s=1.2) weights\n    ranks = list(range(1, len(resource_ids) + 1))\n    weights = [1.0 / (r ** 1.2) for r in ranks]\n    total_w = sum(weights)\n    probs = [w / total_w for w in weights]\n\n    episodes = defaultdict(list)\n    for ep_i in range(n_episodes):\n        ep_id = f"synth_ep_{ep_i:03d}"\n        n_resources_in_ep = rng.randint(10, 20)\n        chosen = rng.choices(resource_ids, weights=probs, k=n_resources_in_ep)\n        chosen = list(dict.fromkeys(chosen))  # dedupe preserving order/popularity draw\n        call_idx = 0\n        for rid in chosen:\n            n_reuse = rng.randint(3, 8)\n            tick = rng.randint(0, 3)\n            for _ in range(n_reuse):\n                sig = f"tool_call({rid})"\n                episodes[ep_id].append(\n                    {\n                        "call_index": call_idx,\n                        "timestamp_tick": min(sim_days - 1, tick),\n                        "call_site_signature": sig,\n                        "resource_id": rid,\n                        "ground_truth_version_id": version_at(rid, min(sim_days - 1, tick)),\n                        "volatility_regime": resource_meta[rid],\n                        "resource_class": "synthetic",\n                    }\n                )\n                call_idx += 1\n                tick += rng.choice([1, 3, 7, 14])\n        episodes[ep_id].sort(key=lambda c: (c["timestamp_tick"], c["call_index"]))\n    logger.info(\n        f"Built synthetic Zipf corpus: {len(episodes)} episodes, "\n        f"{sum(len(v) for v in episodes.values())} calls, {len(resource_ids)} resources"\n    )\n    return dict(episodes), resource_schedules\n\n\nepisodes_synth, resource_schedules_synth = build_synthetic_zipf_episodes(\n    seed=SYNTH_SEED, n_episodes=SYNTH_N_EPISODES, sim_days=SYNTH_SIM_DAYS\n)'}
```

### [62] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:05 UTC

```
{"new_source": "def build_synthetic_zipf_episodes(seed: int = 12345, n_episodes: int = 30, sim_days: int = 30):\n    rng = random.Random(seed)\n    n_resources_per_regime = {\"static\": 90, \"periodic\": 60, \"bursty\": 20}\n    resource_schedules = {}\n    resource_meta = {}\n    rid_counter = 0\n    for regime, n_res in n_resources_per_regime.items():\n        for _ in range(n_res):\n            rid = f\"synth_{regime}_{rid_counter:04d}\"\n            rid_counter += ... [truncated, 28242 chars total]
```

### [63] ASSISTANT · 2026-08-10 06:07:11 UTC

```
Now the policy classes section (2).
```

### [64] TOOL CALL — NotebookEdit · 2026-08-10 06:07:11 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'd67991ab', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## 2. Cache policy implementations\n\nSix policies, one shared `PolicyBase.decide/update` interface keyed by `call_site_signature`. `decide` returns `serve_cache` or `refresh`; `update` is called after every call with whether it was served from cache, whether staleness was observed (`None` if unobserved), and whether it was spot-checked.'}
```

### [65] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:11 UTC

```
{"new_source": "## 2. Cache policy implementations\n\nSix policies, one shared `PolicyBase.decide/update` interface keyed by `call_site_signature`. `decide` returns `serve_cache` or `refresh`; `update` is called after every call with whether it was served from cache, whether staleness was observed (`None` if unobserved), and whether it was spot-checked.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "b7909c28", "error": "", "notebook... [truncated, 29472 chars total]
```

### [66] TOOL CALL — NotebookEdit · 2026-08-10 06:07:33 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'b7909c28', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'class PolicyBase:\n    name = "base"\n\n    def __init__(self, knob):\n        self.knob = knob\n        self.cache = {}  # key -> {"version": str, "last_fetch_tick": int}\n\n    def decide(self, call, now_tick):\n        key = call["call_site_signature"]\n        entry = self.cache.get(key)\n        if entry is None:\n            return "refresh", None\n        if self._is_stale_by_policy(key, entry, now_tick):\n            return "refresh", entry["version"]\n        return "serve_cache", entry["version"]\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        raise NotImplementedError\n\n    def update(self, call, served_from_cache, observed_stale, spot_checked):\n        key = call["call_site_signature"]\n        if not served_from_cache:\n            self.cache[key] = {"version": call["ground_truth_version_id"], "last_fetch_tick": call["timestamp_tick"]}\n\n    def current_param(self, key):\n        raise NotImplementedError\n\n\nclass FixedTTL(PolicyBase):\n    name = "fixed_ttl"\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        return (now_tick - entry["last_fetch_tick"]) >= self.knob\n\n    def current_param(self, key):\n        return self.knob\n\n\nclass DTTL(PolicyBase):\n    """Literal reimplementation of stochastic-approximation TTL-toward-target-hit-rate\n    (Basu et al.-style Robbins-Monro update): ttl += eta*(hit_observed - target_hit_rate)/k."""\n\n    name = "d_ttl"\n    ETA = 6.0\n    TTL_MIN, TTL_MAX = 1.0, 60.0\n\n    def __init__(self, knob):\n        super().__init__(knob)\n        self.ttl = defaultdict(lambda: 3.0)\n        self.k = defaultdict(int)\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        return (now_tick - entry["last_fetch_tick"]) >= self.ttl[key]\n\n    def update(self, call, served_from_cache, observed_stale, spot_checked):\n        key = call["call_site_signature"]\n        self.k[key] += 1\n        hit_observed = 1.0 if served_from_cache else 0.0\n        step = self.ETA * (hit_observed - self.knob) / self.k[key]\n        self.ttl[key] = min(self.TTL_MAX, max(self.TTL_MIN, self.ttl[key] + step))\n        super().update(call, served_from_cache, observed_stale, spot_checked)\n\n    def current_param(self, key):\n        return self.ttl[key]\n\n\nclass EWMAAdaptive(PolicyBase):\n    """EWMA of confirmed-stale rate drives TTL up/down toward a target tolerable staleness."""\n\n    name = "ewma_adaptive"\n    TARGET_STALE = 0.05\n    GAIN = 1.5\n    TTL_MIN, TTL_MAX = 1.0, 60.0\n\n    def __init__(self, knob):\n        super().__init__(knob)\n        self.ttl = defaultdict(lambda: 3.0)\n        self.ewma = defaultdict(float)\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        return (now_tick - entry["last_fetch_tick"]) >= self.ttl[key]\n\n    def update(self, call, served_from_cache, observed_stale, spot_checked):\n        key = call["call_site_signature"]\n        if observed_stale is not None:\n            obs = 1.0 if observed_stale else 0.0\n            self.ewma[key] = self.knob * obs + (1 - self.knob) * self.ewma[key]\n            factor = 1 + self.GAIN * (self.TARGET_STALE - self.ewma[key])\n            self.ttl[key] = min(self.TTL_MAX, max(self.TTL_MIN, self.ttl[key] * factor))\n        super().update(call, served_from_cache, observed_stale, spot_checked)\n\n    def current_param(self, key):\n        return self.ttl[key]\n\n\nclass FreshCacheGate(PolicyBase):\n    """Exponential-decay hazard model fit from accumulated spot-check labels, gating reuse\n    against an error_budget. `pooled=True` shares hazard statistics across all call-sites of\n    the same resource_class (fixes small-sample calibration on low-repeat sites)."""\n\n    name = "freshcache_raw"\n    pooled = False\n    PRIOR_LAMBDA = 0.02\n\n    def __init__(self, knob):\n        super().__init__(knob)\n        self.stale_events = defaultdict(float)\n        self.total_age_ticks = defaultdict(float)\n\n    def _group_key(self, call):\n        return call["resource_class"] if self.pooled else call["call_site_signature"]\n\n    def decide(self, call, now_tick):\n        key = call["call_site_signature"]\n        entry = self.cache.get(key)\n        if entry is None:\n            return "refresh", None\n        age = now_tick - entry["last_fetch_tick"]\n        gkey = self._group_key(call)\n        lam = (self.stale_events[gkey] + 1e-6) / (self.total_age_ticks[gkey] + 1e-6 / self.PRIOR_LAMBDA)\n        prob_stale = 1 - pow(2.718281828, -lam * max(age, 0))\n        if prob_stale > self.knob:\n            return "refresh", entry["version"]\n        return "serve_cache", entry["version"]\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        raise NotImplementedError\n\n    def update(self, call, served_from_cache, observed_stale, spot_checked):\n        key = call["call_site_signature"]\n        if observed_stale is not None:\n            gkey = self._group_key(call)\n            entry = self.cache.get(key)\n            age = (call["timestamp_tick"] - entry["last_fetch_tick"]) if entry else 0\n            self.total_age_ticks[gkey] += max(age, 1e-3)\n            if observed_stale:\n                self.stale_events[gkey] += 1.0\n        super().update(call, served_from_cache, observed_stale, spot_checked)\n\n    def current_param(self, key):\n        gkey = key\n        return (self.stale_events[gkey] + 1e-6) / (self.total_age_ticks[gkey] + 1e-6 / self.PRIOR_LAMBDA)\n\n    def current_hazard(self, key):\n        return self.current_param(key)\n\n\nclass FreshCacheGateRaw(FreshCacheGate):\n    name = "freshcache_raw"\n    pooled = False\n\n\nclass FreshCacheGatePooled(FreshCacheGate):\n    name = "freshcache_pooled"\n    pooled = True\n\n    def current_param(self, key):\n        return None  # pooled stat is per resource_class, not per call-site; reported separately\n\n\nclass AIMD(PolicyBase):\n    """Additive-increase/multiplicative-decrease window per call_site_signature."""\n\n    name = "aimd"\n    W_MIN, W_MAX = 1.0, 60.0\n    W_INIT = 3.0\n\n    def __init__(self, knob):\n        super().__init__(knob)\n        self.a, self.b = knob\n        self.window = defaultdict(lambda: self.W_INIT)\n\n    def _is_stale_by_policy(self, key, entry, now_tick):\n        return (now_tick - entry["last_fetch_tick"]) >= self.window[key]\n\n    def update(self, call, served_from_cache, observed_stale, spot_checked):\n        key = call["call_site_signature"]\n        if observed_stale is not None:\n            if observed_stale:\n                self.window[key] = max(self.W_MIN, self.window[key] * self.b)\n            else:\n                self.window[key] = min(self.W_MAX, self.window[key] + self.a)\n        super().update(call, served_from_cache, observed_stale, spot_checked)\n\n    def current_param(self, key):\n        return self.window[key]\n\n\nPOLICIES = {\n    "fixed_ttl": (FixedTTL, [1, 3, 7, 14, 30]),\n    "d_ttl": (DTTL, [0.5, 0.7, 0.9]),\n    "ewma_adaptive": (EWMAAdaptive, [0.1, 0.3, 0.5]),\n    "freshcache_raw": (FreshCacheGateRaw, [0.10, 0.20, 0.35]),\n    "freshcache_pooled": (FreshCacheGatePooled, [0.10, 0.20, 0.35]),\n    "aimd": (AIMD, [(a, b) for a in [0.1, 0.25, 0.5] for b in [0.5, 0.7, 0.9]]),\n}'}
```

### [67] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:33 UTC

```
{"new_source": "class PolicyBase:\n    name = \"base\"\n\n    def __init__(self, knob):\n        self.knob = knob\n        self.cache = {}  # key -> {\"version\": str, \"last_fetch_tick\": int}\n\n    def decide(self, call, now_tick):\n        key = call[\"call_site_signature\"]\n        entry = self.cache.get(key)\n        if entry is None:\n            return \"refresh\", None\n        if self._is_stale_by_policy(key, entry, now_tick):\n            return \"refresh\"... [truncated, 44855 chars total]
```

### [68] ASSISTANT · 2026-08-10 06:07:41 UTC

```
Now section 3 (replay engine) and section 4 (grid driver + output rows).
```

### [69] TOOL CALL — NotebookEdit · 2026-08-10 06:07:41 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '66b156de', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## 3. Replay engine\n\nShared across both data sources: replay one policy instance against one episode set, aggregating hit-rate / staleness metrics into a single replicate row. Staleness is only *observed* (fed back to the policy) when a call is refreshed or hits a randomly-drawn spot-check -- `ground_truth_stale` is always computed for scoring, but `observed_stale` (what the policy sees) is `None` otherwise.'}
```

### [70] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:41 UTC

```
{"new_source": "## 3. Replay engine\n\nShared across both data sources: replay one policy instance against one episode set, aggregating hit-rate / staleness metrics into a single replicate row. Staleness is only *observed* (fed back to the policy) when a call is refreshed or hits a randomly-drawn spot-check -- `ground_truth_stale` is always computed for scoring, but `observed_stale` (what the policy sees) is `None` otherwise.", "cell_type": "markdown", "language": "pyt... [truncated, 46388 chars total]
```

### [71] TOOL CALL — NotebookEdit · 2026-08-10 06:07:51 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '88c0f46c', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def replay_aggregate(episodes, policy_factory, knob, spot_check_rate, seed):\n    rng = random.Random(seed)\n    policy = policy_factory(knob)\n\n    n_calls = 0\n    n_served = 0\n    n_stale_served = 0\n    n_spot_checked = 0\n    param_sum = 0.0\n    param_n = 0\n    regime_stats = defaultdict(lambda: {"n": 0, "served": 0, "stale": 0})\n\n    for episode_id, calls in episodes.items():\n        for call in calls:\n            now_tick = call["timestamp_tick"]\n            decision, cached_version = policy.decide(call, now_tick)\n            served_from_cache = decision == "serve_cache"\n            spot_checked = rng.random() < spot_check_rate\n            true_version = call["ground_truth_version_id"]\n            ground_truth_stale = served_from_cache and (cached_version != true_version)\n            observed_stale = ground_truth_stale if (spot_checked or not served_from_cache) else None\n\n            n_calls += 1\n            regime = call["volatility_regime"]\n            regime_stats[regime]["n"] += 1\n            if served_from_cache:\n                n_served += 1\n                regime_stats[regime]["served"] += 1\n                if ground_truth_stale:\n                    n_stale_served += 1\n                    regime_stats[regime]["stale"] += 1\n            if spot_checked:\n                n_spot_checked += 1\n\n            try:\n                p = policy.current_param(call["call_site_signature"])\n                if p is not None:\n                    param_sum += p\n                    param_n += 1\n            except NotImplementedError:\n                pass\n\n            policy.update(call, served_from_cache, observed_stale, spot_checked)\n\n    hit_rate = n_served / n_calls if n_calls else 0.0\n    stale_rate_of_served = n_stale_served / n_served if n_served else 0.0\n    stale_rate_of_calls = n_stale_served / n_calls if n_calls else 0.0\n    mean_adapted_param = param_sum / param_n if param_n else None\n\n    regime_breakdown = {}\n    for regime, s in regime_stats.items():\n        regime_breakdown[regime] = {\n            "n": s["n"],\n            "hit_rate": s["served"] / s["n"] if s["n"] else 0.0,\n            "stale_rate_of_served": s["stale"] / s["served"] if s["served"] else 0.0,\n        }\n\n    return {\n        "n_calls": n_calls,\n        "n_served_from_cache": n_served,\n        "n_stale_served": n_stale_served,\n        "n_spot_checked": n_spot_checked,\n        "hit_rate": hit_rate,\n        "stale_rate_of_served": stale_rate_of_served,\n        "stale_rate_of_calls": stale_rate_of_calls,\n        "mean_adapted_param": mean_adapted_param,\n        "redundant_calls_avoided": n_served,\n        "regime_breakdown": regime_breakdown,\n    }'}
```

### [72] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:51 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [73] TOOL CALL — NotebookEdit · 2026-08-10 06:07:57 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '75795ffc', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## 4. Experiment grid driver\n\nSweeps every (data_source, policy, knob, spot_check_rate, seed) combination. Following the original scoping decision, the full spot-check-rate ablation is only run for AIMD; every other policy is only run at the headline rate (0.20) -- this bounds grid size while still covering the ablation's purpose."}
```

### [74] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:57 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [75] TOOL CALL — NotebookEdit · 2026-08-10 06:08:05 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '5fbd8ad4', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def run_grid(data_sources, n_replicates, spot_check_rates, headline_rate=0.20, max_cells=None):\n    rows = []\n    n_cells = 0\n    for data_source, (episodes, n_calls_total) in data_sources.items():\n        for policy_key, (factory, knobs) in POLICIES.items():\n            for knob in knobs:\n                for spot_rate in spot_check_rates:\n                    if spot_rate != headline_rate and policy_key != "aimd":\n                        continue  # ablation scoped to AIMD + headline rate for other policies\n                    n_cells += 1\n                    if max_cells is not None and n_cells > max_cells:\n                        continue\n                    for seed in range(n_replicates):\n                        agg = replay_aggregate(episodes, factory, knob, spot_rate, seed)\n                        knob_value = list(knob) if isinstance(knob, tuple) else knob\n                        row = {\n                            "data_source": data_source,\n                            "policy_name": policy_key,\n                            "knob_value": knob_value,\n                            "spot_check_rate": spot_rate,\n                            "seed": seed,\n                            "n_episodes": len(episodes),\n                            **agg,\n                        }\n                        rows.append(row)\n    logger.info(f"run_grid produced {len(rows)} replicate rows across {n_cells} cells")\n    return rows, n_cells\n\n\ndata_sources = {\n    "real_corpus": (episodes_real, sum(len(v) for v in episodes_real.values())),\n    "synthetic_zipf": (episodes_synth, sum(len(v) for v in episodes_synth.values())),\n}\nfor name, (eps, n_calls) in data_sources.items():\n    logger.info(f"data_source={name}: {len(eps)} episodes, {n_calls} calls")\n\nrows, n_cells = run_grid(\n    data_sources, n_replicates=N_REPLICATES, spot_check_rates=SPOT_CHECK_RATES,\n    headline_rate=HEADLINE_RATE, max_cells=MAX_CELLS,\n)'}
```

### [76] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:05 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [77] ASSISTANT · 2026-08-10 06:08:11 UTC

```
Now the results/visualization cell.
```

### [78] TOOL CALL — NotebookEdit · 2026-08-10 06:08:11 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': '7b114749', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Results\n\nAggregate each policy's headline-rate replicate rows (per data source) into a mean hit-rate / stale-rate-of-served, then plot the hit-rate vs. staleness tradeoff -- this is the same Pareto-frontier view (hit-rate vs. staleness) that the full pipeline's evaluation stage builds from `method_out.json`."}
```

### [79] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:11 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [80] TOOL CALL — NotebookEdit · 2026-08-10 06:08:21 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/code_demo.ipynb', 'cell_id': 'd48f444a', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'headline_rows = [r for r in rows if r["spot_check_rate"] == HEADLINE_RATE]\n\nsummary = defaultdict(lambda: defaultdict(list))\nfor r in headline_rows:\n    summary[r["data_source"]][r["policy_name"]].append(r)\n\nprint(f"{\'data_source\':<16} {\'policy\':<18} {\'n_cells\':>8} {\'hit_rate\':>10} {\'stale_rate\':>11}")\nprint("-" * 68)\nplot_points = defaultdict(list)\nfor data_source, policies in summary.items():\n    for policy_name, prows in policies.items():\n        hit_rates = [r["hit_rate"] for r in prows]\n        stale_rates = [r["stale_rate_of_served"] for r in prows]\n        mean_hit = sum(hit_rates) / len(hit_rates)\n        mean_stale = sum(stale_rates) / len(stale_rates)\n        n_knobs = len(set(json.dumps(r["knob_value"]) for r in prows))\n        print(f"{data_source:<16} {policy_name:<18} {n_knobs:>8} {mean_hit:>10.3f} {mean_stale:>11.3f}")\n        plot_points[data_source].append((policy_name, mean_hit, mean_stale))\n\nfig, axes = plt.subplots(1, len(plot_points), figsize=(6 * len(plot_points), 5), squeeze=False)\nfor ax, (data_source, pts) in zip(axes[0], plot_points.items()):\n    for policy_name, hit, stale in pts:\n        ax.scatter(stale, hit, s=80, label=policy_name)\n        ax.annotate(policy_name, (stale, hit), fontsize=8, xytext=(4, 4), textcoords="offset points")\n    ax.set_xlabel("stale_rate_of_served (mean over knobs & seeds)")\n    ax.set_ylabel("hit_rate (mean over knobs & seeds)")\n    ax.set_title(f"Hit-rate vs. staleness tradeoff — {data_source}")\n    ax.grid(alpha=0.3)\nplt.tight_layout()\nplt.show()'}
```

### [81] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:21 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [82] ASSISTANT · 2026-08-10 06:08:27 UTC

```
Now let's test-run the notebook in a clean environment.
```

### [83] TOOL CALL — Bash · 2026-08-10 06:08:27 UTC

```
\
/usr/local/bin/python3.12 -m venv .nb_env && \
.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -5
```

### [84] TOOL RESULT — Bash [ERROR] · 2026-08-10 06:10:25 UTC

```
Error: Exit code 143
Command timed out after 2m 0s
```

### [85] TOOL CALL — Bash · 2026-08-10 06:10:33 UTC

```
ls .nb_env 2>/dev/null && .nb_env/bin/pip list 2>/dev/null | head -20
```

### [86] TOOL RESULT — Bash · 2026-08-10 06:10:33 UTC

```
{"stdout": "bin\netc\ninclude\nlib\nlib64\npyvenv.cfg\nshare\nPackage             Version\n------------------- ---------\nbleach              6.4.0\ncertifi             2026.7.22\ncharset-normalizer  3.4.9\ncomm                0.2.3\ndebugpy             1.8.21\ndefusedxml          0.7.1\nexecuting           2.2.1\nfastjsonschema      2.22.1\nfqdn                1.5.1\nh11                 0.16.0\nidna                3.18\njson5               0.15.0\njsonpointer         3.1.1\njupyterlab_pygments 0.3.0\njupyterlab_widgets  3.0.16\nlark                1.3.1\nMarkupSafe          3.0.3\nmistune             3.3.4", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [87] ASSISTANT · 2026-08-10 06:10:37 UTC

```
Install actually completed (jupyter seems fully present already), just the command timed out reporting. Let's proceed to execute the notebook.
```

### [88] TOOL CALL — Bash · 2026-08-10 06:10:37 UTC

```
.nb_env/bin/pip show jupyter nbconvert 2>&1 | head -20
```

### [89] TOOL RESULT — Bash · 2026-08-10 06:10:37 UTC

```
{"stdout": "WARNING: Package(s) not found: jupyter, nbconvert", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [90] ASSISTANT · 2026-08-10 06:10:41 UTC

```
Not fully installed. Let's finish it with a longer timeout in background.
```

### [91] TOOL CALL — Bash · 2026-08-10 06:10:41 UTC

```
.nb_env/bin/pip install -q pip jupyter ipykernel > /tmp/pipinstall.log 2>&1 & echo $!
```

### [92] TOOL RESULT — Bash · 2026-08-10 06:10:41 UTC

```
{"stdout": "272", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [93] TOOL CALL — Bash · 2026-08-10 06:10:45 UTC

```
for i in $(seq 1 30); do kill -0 272 2>/dev/null || { echo done; break; }; sleep 10; done; tail -20 /tmp/pipinstall.log
```

### [94] TOOL RESULT — Bash · 2026-08-10 06:14:03 UTC

```
{"stdout": "done\n\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [95] TOOL CALL — Bash · 2026-08-10 06:14:11 UTC

```
.nb_env/bin/jupyter --version 2>&1 | head -5
\
timeout 590 .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=580 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -80
```

### [96] TOOL RESULT — Bash · 2026-08-10 06:16:11 UTC

```
{"stdout": "Selected Jupyter core packages...\nIPython          : 9.16.1\nipykernel        : 7.3.0\nipywidgets       : 8.1.8\njupyter_client   : 8.9.1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_2/art_tceB4eOwcBAO/.nb_env/lib/python3.12/site-packages/nbformat/validator.py:434: MissingIDFieldWarning: Cell is missing an id field, this will become a hard error in future nbformat versions. You may want to use `normalize()` on your notebooks before validations (available since nbformat 5.1.4). Previous versions of nbformat are fixing this issue transparently, and will stop doing so in the future.\n  _validate(nbdict, ref, version, version_minor, relax_add_props)\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 103765 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [97] ASSISTANT · 2026-08-10 06:16:19 UTC

```
Notebook executed successfully. Let's verify the outputs look sane and clean up the test env.
```

### [98] TOOL CALL — Bash · 2026-08-10 06:16:19 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='code':
        for o in c.get('outputs',[]):
            if o.get('output_type')=='error':
                print('ERROR CELL:', ''.join(o.get('traceback',[]))[:2000])
print('total cells', len(nb['cells']))
"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
# print last code cell outputs
for c in nb['cells'][-3:]:
    print(c['cell_type'])
    for o in c.get('outputs',[]):
        if 'text' in o: print(''.join(o['text'])[:1500])
"
rm -rf .nb_env
```

### [99] TOOL RESULT — Bash · 2026-08-10 06:16:41 UTC

```
{"stdout": "total cells 19\ncode\n06:16:08|INFO   |data_source=real_corpus: 1 episodes, 100 calls\n\n06:16:08|INFO   |data_source=synthetic_zipf: 30 episodes, 1626 calls\n\n06:16:08|INFO   |run_grid produced 176 replicate rows across 88 cells\n\nmarkdown\ncode\ndata_source      policy              n_cells   hit_rate  stale_rate\n--------------------------------------------------------------------\nreal_corpus      fixed_ttl                 5      0.422       0.094\nreal_corpus      d_ttl                     3      0.150       0.000\nreal_corpus      ewma_adaptive             3      0.390       0.103\nreal_corpus      freshcache_raw            3      0.630       0.143\nreal_corpus      freshcache_pooled         3      0.612       0.103\nreal_corpus      aimd                      9      0.393       0.102\nsynthetic_zipf   fixed_ttl                 5      0.836       0.030\nsynthetic_zipf   d_ttl                     3      0.722       0.011\nsynthetic_zipf   ewma_adaptive             3      0.816       0.022\nsynthetic_zipf   freshcache_raw            3      0.945       0.049\nsynthetic_zipf   freshcache_pooled         3      0.948       0.055\nsynthetic_zipf   aimd                      9      0.815       0.022", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [100] ASSISTANT · 2026-08-10 06:16:45 UTC

```
No errors, results are meaningful (FreshCache achieving best hit-rate on real corpus, matching the artifact's reported finding). Now final verification checks.
```

### [101] TOOL CALL — Bash · 2026-08-10 06:16:45 UTC

```
grep -c "GITHUB_DATA_URL = \"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\"" code_demo.ipynb
ls -la mini_demo_data.json code_demo.ipynb
python3 -c "import json; json.load(open('mini_demo_data.json')); json.load(open('code_demo.ipynb')); print('both valid JSON')"
```

### [102] TOOL RESULT — Bash · 2026-08-10 06:16:45 UTC

```
{"stdout": "0\n-rw-r--r-- 1 root root 103779 Aug 10 06:16 code_demo.ipynb\n-rw-r--r-- 1 root root 125736 Aug 10 06:05 mini_demo_data.json\nboth valid JSON", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [103] TOOL CALL — Bash · 2026-08-10 06:16:47 UTC

```
grep -o "GITHUB_DATA_URL.*" code_demo.ipynb | head -3
```

### [104] TOOL RESULT — Bash · 2026-08-10 06:16:47 UTC

```
{"stdout": "GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-2/experiment-1/demo/mini_demo_data.json\\\"\\n\",\nGITHUB_DATA_URL) as response:\\n\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [105] ASSISTANT · 2026-08-10 06:16:51 UTC

```
Confirmed — the URL string is present (grep just needed unescaped quotes). All checks pass. Now writing the required output JSON.
```

### [106] TOOL CALL — Bash · 2026-08-10 06:16:51 UTC

```
cat > ./.terminal_claude_agent_struct_out.json << 'EOF'
{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
EOF
cat ./.terminal_claude_agent_struct_out.json
```

### [107] TOOL RESULT — Bash · 2026-08-10 06:16:51 UTC

```
{"stdout": "{\n  \"out_expected_files\": {\n    \"notebook\": \"code_demo.ipynb\",\n    \"mini_data_file\": \"mini_demo_data.json\"\n  }\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [108] ASSISTANT · 2026-08-10 06:16:53 UTC

```
Done. Created `code_demo.ipynb` (minimal-change notebook version of `method.py`, split into markdown-annotated cells for the fail-fast loader, episode parsing, synthetic Zipf simulator, six cache-policy classes, replay engine, grid driver, and a results/plot cell) plus `mini_demo_data.json` (100 real-corpus rows from one episode spanning all three volatility regimes). Tested end-to-end in a clean venv simulating Colab — it executes with no errors and reproduces the artifact's headline finding (FreshCache achieving the best hit-rate on the real corpus). Output struct file written.
```
