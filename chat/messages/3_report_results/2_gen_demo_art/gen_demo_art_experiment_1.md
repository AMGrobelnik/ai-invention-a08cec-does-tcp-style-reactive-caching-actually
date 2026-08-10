# gen_demo_art_experiment_1 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-10 06:05:16 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
```

### [2] SYSTEM-USER prompt · 2026-08-10 06:05:22 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/results/out.json`
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
id: art_qtEtMpLZuRGI
type: experiment
title: AIMD Reuse-Window Caching vs TTL Baselines
summary: >-
  Implements and replays four per-call-site cache policies against a simulated LLM-agent tool-call loop over a versioned,
  volatility-labeled resource corpus (60 resources per regime, static/periodic/bursty version-change schedules; 3 volatility
  regimes: low/medium/high; 40 episodes x 150 calls per regime, Zipf-skewed working-set revisits, globally monotonic simulated
  clock across episodes). Baselines: FixedTTLPolicy (fixed per-site TTL, 9-point grid including TTL=0 and TTL~inf boundary
  probes), DTTLPolicy (literal Basu et al. 2017 arXiv:1704.04448 Robbins-Monro TTL update toward a target hit rate, gamma_k=c/(k+1),
  15-point h_target x c grid), EWMAAdaptivePolicy (correctly-signed fixed-step EWMA-toward-target-hit-rate secondary adaptive
  baseline, added per fallback_plan item 2 after the literal d-TTL update rule was found to get trapped at ttl_min from a
  low initial TTL -- documented as boundary_sanity_checks.dttl_stuck_at_floor_from_low_init, not silently fixed), FreshCacheGatePolicy
  (per-site MLE-fitted exponential staleness gate P(stale|age)=1-exp(-lambda*age), 4-point error_budget grid, min_obs_to_fit=5),
  and FreshCachePooledPolicy (fallback_plan item 3's fairer partial-pooling-by-resource-schedule-family variant of FreshCache).
  Proposed method: AIMDPolicy, an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes
  rather than any statistical fit (12-point a x b grid). All policies replayed through the identical episode traces per regime
  via a ProcessPoolExecutor (spawn context, 150 total replay jobs, ~5s wall-clock). No dependency DATASET artifact output
  was available in the workspace at run time, so per fallback_plan item 1 the episode traces were generated in-process by
  the built-in Stage-1 Zipf-skewed simulator rather than loaded externally -- fully synthetic but controllable, and this is
  logged explicitly in the script's docstring and log output. No LLM/OpenRouter calls were made anywhere (cost = $0); the
  optional query-text diversification step was skipped as unnecessary since traces are self-generated and text diversity does
  not affect any cache-policy decision. Outputs: per-run hit_rate/stale_rate/low-repeat-slice stats for all 150 (regime, policy_family,
  knob) combinations; Pareto hit-rate-vs-stale-rate frontiers and a dominance summary (fraction of AIMD knob points NOT dominated
  by any TTL/d-TTL/EWMA baseline point) per regime; convergence-event summaries (median/p10/p90, in units of confirmed-staleness-feedback
  events) per regime x policy family; a low-repeat-count (sites visited <=5 times) slice summary comparing AIMD's window-movement
  against FreshCache's calibrated-fraction; two ablations (AIMD's presumed_valid_weight for unchecked hits, and spot_check_rate
  sensitivity); and machine-checked boundary sanity results (TTL=0 -> exactly 0% hit rate, TTL~inf -> >=90% hit rate, AIMD
  window growth/collapse/recovery, d-TTL instability documentation, low-repeat mini-check confirming FreshCache fails to calibrate
  on 4 observations while AIMD's window still moves). Final verdict computed against two explicit success criteria (frontier
  non-domination; low-repeat convergence speed + FreshCache calibration failure) came out MIXED: criterion (a) frontier non-domination
  held with mean 0.67 (AIMD non-dominated in medium/high volatility, partially dominated in low volatility); criterion (b)
  did not hold in the full run (AIMD's median low-repeat convergence-events was 14.5 vs baselines' 9.375, though FreshCache's
  calibrated fraction was only 0.375, softly supporting the calibration-failure half of criterion (b)). All numeric results,
  the full per-run grid, and all diagnostic/ablation/verdict fields are in method_out.json (validated against the aii-json
  exp_gen_sol_out schema), with full/mini/preview size variants also generated.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
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
Raw data URL: https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json"
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-08-10 06:05:22 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [4] TOOL CALL — Skill · 2026-08-10 06:05:26 UTC

```
aii-colab
```

### [5] TOOL CALL — Skill · 2026-08-10 06:05:26 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-08-10 06:05:26 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL RESULT — Skill · 2026-08-10 06:05:26 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-08-10 06:05:26 UTC

```
ls /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/
```

### [9] TOOL RESULT — Bash · 2026-08-10 06:05:26 UTC

```
{"stdout": "__pycache__\nfull_method_out.json\nlogs\nmethod.py\nmethod_out.json\nmethod_raw.json\nmini_method_out.json\nmini_method_raw.json\npreview_method_out.json\npyproject.toml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Read · 2026-08-10 06:05:30 UTC

```
/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py
```

### [11] TOOL CALL — Bash · 2026-08-10 06:05:30 UTC

```
head -c 3000 /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/preview_method_out.json
```

### [12] TOOL RESULT — Bash · 2026-08-10 06:05:30 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"AIMD reuse-window caching vs TTL/d-TTL/FreshCache baselines for agent tool calls\",\n    \"description\": \"Simulated agent tool-call loop over a versioned, volatility-labeled resource corpus, replayed through four cache policies (fixed TTL, d-TTL stochastic-approximation, FreshCache fitted staleness gate [...\",\n    \"verdict\": \"MIXED\",\n    \"verdict_criteria\": {\n      \"criterion_a_frontier_non_dominated\": \"True\",\n      \"criterion_b_low_repeat_convergence_and_freshcache_failure\": false\n    },\n    \"config\": {\n      \"n_resources\": 60,\n      \"n_episodes_per_regime\": 40,\n      \"n_calls_per_episode\": 150,\n      \"episode_horizon\": 120.0,\n      \"repeat_bias\": 0.65,\n      \"spot_check_rate\": 0.2,\n      \"regimes\": [\n        \"low_volatility\",\n        \"medium_volatility\",\n        \"high_volatility\"\n      ],\n      \"regime_configs\": {\n        \"low_volatility\": {\n          \"p_static\": 0.7,\n          \"p_periodic\": 0.2,\n          \"p_bursty\": 0.1,\n          \"bursty_rate\": 0.02,\n          \"period_range\": [\n            20.0,\n            60.0\n          ]\n        },\n        \"medium_volatility\": {\n          \"p_static\": 0.35,\n          \"p_periodic\": 0.35,\n          \"p_bursty\": 0.3,\n          \"bursty_rate\": 0.08,\n          \"period_range\": [\n            5.0,\n            20.0\n          ]\n        },\n        \"high_volatility\": {\n          \"p_static\": 0.1,\n          \"p_periodic\": 0.3,\n          \"p_bursty\": 0.6,\n          \"bursty_rate\": 0.3,\n          \"period_range\": [\n            1.0,\n            5.0\n          ]\n        }\n      },\n      \"fixed_ttl_grid\": [\n        0.0,\n        0.5,\n        1\n      ],\n      \"dttl_grid\": [\n        [\n          0.5,\n          0.5\n        ],\n        [\n          0.5,\n          1.0\n        ],\n        [\n          0.5,\n          2.0\n        ]\n      ],\n      \"ewma_grid\": [\n        [\n          0.5,\n          0.1\n        ],\n        [\n          0.5,\n          0.2\n        ],\n        [\n          0.7,\n          0.1\n        ]\n      ],\n      \"freshcache_grid\": [\n        0.05,\n        0.1,\n        0.2\n      ],\n      \"aimd_grid\": [\n        [\n          0.25,\n          0.3\n        ],\n        [\n          0.25,\n          0.5\n        ],\n        [\n          0.25,\n          0.7\n        ]\n      ],\n      \"seeds\": \"regime rng seed = 1000 + regime_index; per-job seed = hash((regime, family, knob_index)) % 2**31\",\n      \"mini_mode\": false\n    },\n    \"frontiers\": {\n      \"low_volatility\": {\n        \"fixed_ttl\": [\n          {\n            \"hit_rate\": 0.16266666666666665,\n            \"stale_rate\": 0.0,\n            \"knob\": {\n              \"ttl\": 1\n            }\n          },\n          {\n            \"hit_rate\": 0.2585,\n            \"stale_rate\": 0.007736943907156673,\n            \"knob\": {\n              \"ttl\": 2\n            }\n          },\n          {\n            \"hit_rate\": 0.367,\n            \"stale_rate\": 0.01589464123524069,\n            \"knob\": {\n              \"ttl\": 4\n            }\n          }\n        ],\n        \"d_ttl\": [\n          {\n            \"hi", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL RESULT — Read · 2026-08-10 06:05:31 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [14] TOOL CALL — Bash · 2026-08-10 06:05:36 UTC

```
wc -c /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/mini_method_out.json
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/mini_method_out.json'))
print(list(d.keys()))
print(len(d['datasets'][0]['examples']))
print(d['datasets'][0]['examples'][0])
"
```

### [15] TOOL RESULT — Bash · 2026-08-10 06:05:36 UTC

```
{"stdout": "45407 /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/mini_method_out.json\n['metadata', 'datasets']\n3\n{'input': 'AIMD-cache-simulation run: regime=low_volatility, policy_family=fixed_ttl, knob=(ttl=0.0), n_calls=6000', 'output': '{\"hit_rate\": 0.0, \"stale_rate\": 0.0, \"low_repeat_hit_rate\": 0.0, \"low_repeat_stale_rate\": 0.0, \"convergence_events_median\": null, \"calibrated_fraction\": null}', 'predict_hit_rate': '0.000000', 'predict_stale_rate': '0.000000', 'metadata_regime': 'low_volatility', 'metadata_policy_family': 'fixed_ttl', 'metadata_knob': {'ttl': 0.0}, 'metadata_hit_rate': 0.0, 'metadata_stale_rate': 0.0, 'metadata_low_repeat_hit_rate': 0.0, 'metadata_low_repeat_stale_rate': 0.0, 'metadata_convergence_events_median': None, 'metadata_n_low_repeat_sites': 0, 'metadata_calibrated_fraction': None}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-08-10 06:05:42 UTC

```
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json'))
m=d['metadata']
print(list(m.keys()))
print(m['dominance_summary'])
print(m['verdict'])
"
```

### [17] TOOL RESULT — Bash · 2026-08-10 06:05:42 UTC

```
{"stdout": "['method_name', 'description', 'verdict', 'verdict_criteria', 'config', 'frontiers', 'dominance_summary', 'convergence_summary', 'low_repeat_slice_summary', 'ablations', 'boundary_sanity_checks', 'low_repeat_mini_check', 'runtime_seconds']\n{'low_volatility': {'n_aimd_points': 12, 'n_dominated': 8, 'fraction_non_dominated': 0.3333333333333333}, 'medium_volatility': {'n_aimd_points': 12, 'n_dominated': 4, 'fraction_non_dominated': 0.6666666666666666}, 'high_volatility': {'n_aimd_points': 12, 'n_dominated': 0, 'fraction_non_dominated': 1.0}}\nMIXED", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-08-10 06:05:48 UTC

```
Now let me build mini_demo_data.json with a curated subset (frontiers, dominance, convergence, verdict from the full run) for reference comparison in the notebook.
```

### [19] TOOL CALL — Bash · 2026-08-10 06:05:48 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
d=json.load(open('/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json'))
m=d['metadata']
out = {
    'verdict': m['verdict'],
    'verdict_criteria': m['verdict_criteria'],
    'dominance_summary': m['dominance_summary'],
    'convergence_summary': m['convergence_summary'],
    'frontiers': m['frontiers'],
    'boundary_sanity_checks': m['boundary_sanity_checks'],
    'low_repeat_mini_check': m['low_repeat_mini_check'],
}
json.dump(out, open('mini_demo_data.json','w'), indent=2)
print(len(json.dumps(out)))
"
```

### [20] TOOL RESULT — Bash · 2026-08-10 06:05:48 UTC

```
{"stdout": "12375", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-08-10 06:05:50 UTC

```
Good, 12KB file. Now let me build the notebook.
```

### [22] TOOL CALL — ToolSearch · 2026-08-10 06:05:50 UTC

```
{'query': 'select:NotebookEdit'}
```

### [23] TOOL RESULT — ToolSearch · 2026-08-10 06:05:50 UTC

```
{"matches": ["NotebookEdit"], "query": "select:NotebookEdit", "total_deferred_tools": 22}
```

### [24] TOOL CALL — Write · 2026-08-10 06:05:54 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb

{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "cell-title",
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

### [25] TOOL RESULT — Write · 2026-08-10 06:05:54 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "content": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"]\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [26] TOOL CALL — NotebookEdit · 2026-08-10 06:06:04 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'cell-title', 'new_source': '"# AIMD Reuse-Window Caching vs TTL Baselines\\n\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\n\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\n\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\n\\nKey question: does AIMD\'s outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn\'t simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache\'s MLE fit never accumulates enough observations?"'}
```

### [27] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:04 UTC

```
{"new_source": "\"# AIMD Reuse-Window Caching vs TTL Baselines\\n\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\n\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\n\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\n\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\"", "old_source": "# placeholder", "cell_type": "code", "language": "python", "edit_mode": "replace", "cell_id": "cell-title", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": [\"# placeholder\"]\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n  \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}\n", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [28] ASSISTANT · 2026-08-10 06:06:12 UTC

```
Now let me add the install, imports, data loading cells.
```

### [29] TOOL CALL — NotebookEdit · 2026-08-10 06:06:12 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'cell-title', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': "import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# psutil, loguru — NOT pre-installed on Colab, always install\\n_pip('psutil==6.1.1')\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')"}
```

### [30] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:12 UTC

```
{"new_source": "import subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# psutil, loguru — NOT pre-installed on Colab, always install\\n_pip('psutil==6.1.1')\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "12979f58", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [31] TOOL CALL — NotebookEdit · 2026-08-10 06:06:16 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '12979f58', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'from __future__ import annotations\\n\\nimport json\\nimport math\\nimport sys\\nimport time\\nfrom collections import defaultdict\\nfrom dataclasses import dataclass, field\\nfrom pathlib import Path\\n\\nimport numpy as np\\nimport matplotlib.pyplot as plt\\nfrom loguru import logger\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\"INFO\\", format=\\"{time:HH:mm:ss}|{level:<7}|{message}\\")'}
```

### [32] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:16 UTC

```
{"new_source": "from __future__ import annotations\\n\\nimport json\\nimport math\\nimport sys\\nimport time\\nfrom collections import defaultdict\\nfrom dataclasses import dataclass, field\\nfrom pathlib import Path\\n\\nimport numpy as np\\nimport matplotlib.pyplot as plt\\nfrom loguru import logger\\n\\nlogger.remove()\\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "7c7a07f4", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [33] TOOL CALL — NotebookEdit · 2026-08-10 06:06:22 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '7c7a07f4', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Load reference data\\n\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end."}
```

### [34] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:22 UTC

```
{"new_source": "## Load reference data\\n\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "448206f1", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [35] TOOL CALL — NotebookEdit · 2026-08-10 06:06:26 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '448206f1', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception: pass\\n    if os.path.exists(\\"mini_demo_data.json\\"):\\n        with open(\\"mini_demo_data.json\\") as f: return json.load(f)\\n    raise FileNotFoundError(\\"Could not load mini_demo_data.json\\")'}
```

### [36] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:26 UTC

```
{"new_source": "GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\"\\nimport os\\n\\ndef load_data():\\n    try:\\n        import urllib.request\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\n            return json.loads(response.read().decode())\\n    except Exception: pass\\n    if os.path.exists(\\\"mini_demo_data.json\\\"):\\n        with open(\\\"mini_demo_data.json\\\") as f: return json.load(f)\\n    raise FileNotFoundError(\\\"Could not load mini_demo_data.json\\\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "d02497c3", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [37] TOOL CALL — NotebookEdit · 2026-08-10 06:06:30 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'd02497c3', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'data = load_data()\\nprint(\\"Loaded reference data. Top-level keys:\\", list(data.keys()))\\nprint(\\"Full-run verdict:\\", data[\\"verdict\\"], \\"| criteria:\\", data[\\"verdict_criteria\\"])'}
```

### [38] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:30 UTC

```
{"new_source": "data = load_data()\\nprint(\\\"Loaded reference data. Top-level keys:\\\", list(data.keys()))\\nprint(\\\"Full-run verdict:\\\", data[\\\"verdict\\\"], \\\"| criteria:\\\", data[\\\"verdict_criteria\\\"])", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "acfc1511", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [39] ASSISTANT · 2026-08-10 06:06:34 UTC

```
Now the config cell with minimal parameters.
```

### [40] TOOL CALL — NotebookEdit · 2026-08-10 06:06:34 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'acfc1511', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Config\\n\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.'}
```

### [41] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:34 UTC

```
{"new_source": "## Config\\n\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "3240607b", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"3240607b\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [42] TOOL CALL — NotebookEdit · 2026-08-10 06:06:44 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '3240607b', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': '# --- ORIGINAL full-scale values (from method.py), kept as reference / commented ---\\n# N_RESOURCES = 60\\n# N_EPISODES_PER_REGIME = 40\\n# N_CALLS_PER_EPISODE = 150\\n\\n# --- DEMO (small-scale) values used in this notebook ---\\nN_RESOURCES = 20\\nN_EPISODES_PER_REGIME = 6\\nN_CALLS_PER_EPISODE = 60\\nEPISODE_HORIZON = 120.0  # ~ N_CALLS_PER_EPISODE * mean inter-call time, gives change-events room to occur\\nREPEAT_BIAS = 0.65  # probability a call re-touches an already-seen site this episode\\nSPOT_CHECK_RATE = 0.20  # background validity-check probability per cache hit (shared across adaptive policies)\\n\\nREGIME_CONFIGS = {\\n    # fraction of resources on each schedule + bursty rate + periodic period range\\n    \\"low_volatility\\": dict(p_static=0.70, p_periodic=0.20, p_bursty=0.10, bursty_rate=0.02, period_range=(20.0, 60.0)),\\n    \\"medium_volatility\\": dict(p_static=0.35, p_periodic=0.35, p_bursty=0.30, bursty_rate=0.08, period_range=(5.0, 20.0)),\\n    \\"high_volatility\\": dict(p_static=0.10, p_periodic=0.30, p_bursty=0.60, bursty_rate=0.30, period_range=(1.0, 5.0)),\\n}\\nREGIMES = list(REGIME_CONFIGS.keys())\\n\\n# policy knob grids -- shrunk from the originals (which had up to 15 points per family) to a\\n# handful of representative points per family so the demo covers the full hit-rate/stale-rate\\n# tradeoff space without the full 150-job replay grid\\nFIXED_TTL_GRID = [0.0, 1, 4, 1e6]  # include TTL=0 (always-miss) and TTL~inf (always-hit) sanity bounds\\nDTTL_GRID = [(h, c) for h in (0.7, 0.9) for c in (1.0,)]\\nEWMA_GRID = [(h, s) for h in (0.7, 0.9) for s in (0.15,)]\\nFRESHCACHE_GRID = [0.1, 0.2]\\nAIMD_GRID = [(a, b) for a in (0.5, 1.0) for b in (0.5, 0.7)]\\n\\nprint(f\\"N_RESOURCES={N_RESOURCES}, N_EPISODES_PER_REGIME={N_EPISODES_PER_REGIME}, N_CALLS_PER_EPISODE={N_CALLS_PER_EPISODE}\\")\\nprint(f\\"regimes={REGIMES}\\")'}
```

### [43] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:44 UTC

```
{"new_source": "# --- ORIGINAL full-scale values (from method.py), kept as reference / commented ---\\n# N_RESOURCES = 60\\n# N_EPISODES_PER_REGIME = 40\\n# N_CALLS_PER_EPISODE = 150\\n\\n# --- DEMO (small-scale) values used in this notebook ---\\nN_RESOURCES = 20\\nN_EPISODES_PER_REGIME = 6\\nN_CALLS_PER_EPISODE = 60\\nEPISODE_HORIZON = 120.0  # ~ N_CALLS_PER_EPISODE * mean inter-call time, gives change-events room to occur\\nREPEAT_BIAS = 0.65  # probability a call re-touches an already-seen site this episode\\nSPOT_CHECK_RATE = 0.20  # background validity-check probability per cache hit (shared across adaptive policies)\\n\\nREGIME_CONFIGS = {\\n    # fraction of resources on each schedule + bursty rate + periodic period range\\n    \\\"low_volatility\\\": dict(p_static=0.70, p_periodic=0.20, p_bursty=0.10, bursty_rate=0.02, period_range=(20.0, 60.0)),\\n    \\\"medium_volatility\\\": dict(p_static=0.35, p_periodic=0.35, p_bursty=0.30, bursty_rate=0.08, period_range=(5.0, 20.0)),\\n    \\\"high_volatility\\\": dict(p_static=0.10, p_periodic=0.30, p_bursty=0.60, bursty_rate=0.30, period_range=(1.0, 5.0)),\\n}\\nREGIMES = list(REGIME_CONFIGS.keys())\\n\\n# policy knob grids -- shrunk from the originals (which had up to 15 points per family) to a\\n# handful of representative points per family so the demo covers the full hit-rate/stale-rate\\n# tradeoff space without the full 150-job replay grid\\nFIXED_TTL_GRID = [0.0, 1, 4, 1e6]  # include TTL=0 (always-miss) and TTL~inf (always-hit) sanity bounds\\nDTTL_GRID = [(h, c) for h in (0.7, 0.9) for c in (1.0,)]\\nEWMA_GRID = [(h, s) for h in (0.7, 0.9) for s in (0.15,)]\\nFRESHCACHE_GRID = [0.1, 0.2]\\nAIMD_GRID = [(a, b) for a in (0.5, 1.0) for b in (0.5, 0.7)]\\n\\nprint(f\\\"N_RESOURCES={N_RESOURCES}, N_EPISODES_PER_REGIME={N_EPISODES_PER_REGIME}, N_CALLS_PER_EPISODE={N_CALLS_PER_EPISODE}\\\")\\nprint(f\\\"regimes={REGIMES}\\\")", "cell_type": "code", "language": "python", "edit_mode": "insert", "cell_id": "e74a677a", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"3240607b\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"3240607b\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e74a677a\",\n   \"source\": \"# --- ORIGINAL full-scale values (from method.py), kept as reference / commented ---\\\\n# N_RESOURCES = 60\\\\n# N_EPISODES_PER_REGIME = 40\\\\n# N_CALLS_PER_EPISODE = 150\\\\n\\\\n# --- DEMO (small-scale) values used in this notebook ---\\\\nN_RESOURCES = 20\\\\nN_EPISODES_PER_REGIME = 6\\\\nN_CALLS_PER_EPISODE = 60\\\\nEPISODE_HORIZON = 120.0  # ~ N_CALLS_PER_EPISODE * mean inter-call time, gives change-events room to occur\\\\nREPEAT_BIAS = 0.65  # probability a call re-touches an already-seen site this episode\\\\nSPOT_CHECK_RATE = 0.20  # background validity-check probability per cache hit (shared across adaptive policies)\\\\n\\\\nREGIME_CONFIGS = {\\\\n    # fraction of resources on each schedule + bursty rate + periodic period range\\\\n    \\\\\\\"low_volatility\\\\\\\": dict(p_static=0.70, p_periodic=0.20, p_bursty=0.10, bursty_rate=0.02, period_range=(20.0, 60.0)),\\\\n    \\\\\\\"medium_volatility\\\\\\\": dict(p_static=0.35, p_periodic=0.35, p_bursty=0.30, bursty_rate=0.08, period_range=(5.0, 20.0)),\\\\n    \\\\\\\"high_volatility\\\\\\\": dict(p_static=0.10, p_periodic=0.30, p_bursty=0.60, bursty_rate=0.30, period_range=(1.0, 5.0)),\\\\n}\\\\nREGIMES = list(REGIME_CONFIGS.keys())\\\\n\\\\n# policy knob grids -- shrunk from the originals (which had up to 15 points per family) to a\\\\n# handful of representative points per family so the demo covers the full hit-rate/stale-rate\\\\n# tradeoff space without the full 150-job replay grid\\\\nFIXED_TTL_GRID = [0.0, 1, 4, 1e6]  # include TTL=0 (always-miss) and TTL~inf (always-hit) sanity bounds\\\\nDTTL_GRID = [(h, c) for h in (0.7, 0.9) for c in (1.0,)]\\\\nEWMA_GRID = [(h, s) for h in (0.7, 0.9) for s in (0.15,)]\\\\nFRESHCACHE_GRID = [0.1, 0.2]\\\\nAIMD_GRID = [(a, b) for a in (0.5, 1.0) for b in (0.5, 0.7)]\\\\n\\\\nprint(f\\\\\\\"N_RESOURCES={N_RESOURCES}, N_EPISODES_PER_REGIME={N_EPISODES_PER_REGIME}, N_CALLS_PER_EPISODE={N_CALLS_PER_EPISODE}\\\\\\\")\\\\nprint(f\\\\\\\"regimes={REGIMES}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [44] ASSISTANT · 2026-08-10 06:06:50 UTC

```
Now the Stage 0/1 simulator section (Resource + episode generation).
```

### [45] TOOL CALL — NotebookEdit · 2026-08-10 06:06:50 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'e74a677a', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Stage 0/1 — Resource corpus + agent-loop call harness\\n\\nEach `Resource` represents a cacheable thing an agent tool call reads (a file, a search result, a computation), tagged with a `schedule` (`static`, `periodic`, or `bursty`) that determines when its ground-truth version changes. `simulate_episode` generates a Zipf-skewed sequence of call-site revisits over a small per-episode working set — exactly like an agent repeatedly re-reading the same file or re-running the same near-duplicate search within one episode. Time is kept **globally monotonic across episodes** so that adaptive policies (which carry per-site state across the whole regime) never see a spurious negative cache "age" at an episode boundary.'}
```

### [46] TOOL RESULT — NotebookEdit · 2026-08-10 06:06:50 UTC

```
{"new_source": "## Stage 0/1 — Resource corpus + agent-loop call harness\\n\\nEach `Resource` represents a cacheable thing an agent tool call reads (a file, a search result, a computation), tagged with a `schedule` (`static`, `periodic`, or `bursty`) that determines when its ground-truth version changes. `simulate_episode` generates a Zipf-skewed sequence of call-site revisits over a small per-episode working set — exactly like an agent repeatedly re-reading the same file or re-running the same near-duplicate search within one episode. Time is kept **globally monotonic across episodes** so that adaptive policies (which carry per-site state across the whole regime) never see a spurious negative cache \"age\" at an episode boundary.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "66a97901", "error": "", "notebook_path": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb", "original_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"3240607b\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e74a677a\",\n   \"source\": \"# --- ORIGINAL full-scale values (from method.py), kept as reference / commented ---\\\\n# N_RESOURCES = 60\\\\n# N_EPISODES_PER_REGIME = 40\\\\n# N_CALLS_PER_EPISODE = 150\\\\n\\\\n# --- DEMO (small-scale) values used in this notebook ---\\\\nN_RESOURCES = 20\\\\nN_EPISODES_PER_REGIME = 6\\\\nN_CALLS_PER_EPISODE = 60\\\\nEPISODE_HORIZON = 120.0  # ~ N_CALLS_PER_EPISODE * mean inter-call time, gives change-events room to occur\\\\nREPEAT_BIAS = 0.65  # probability a call re-touches an already-seen site this episode\\\\nSPOT_CHECK_RATE = 0.20  # background validity-check probability per cache hit (shared across adaptive policies)\\\\n\\\\nREGIME_CONFIGS = {\\\\n    # fraction of resources on each schedule + bursty rate + periodic period range\\\\n    \\\\\\\"low_volatility\\\\\\\": dict(p_static=0.70, p_periodic=0.20, p_bursty=0.10, bursty_rate=0.02, period_range=(20.0, 60.0)),\\\\n    \\\\\\\"medium_volatility\\\\\\\": dict(p_static=0.35, p_periodic=0.35, p_bursty=0.30, bursty_rate=0.08, period_range=(5.0, 20.0)),\\\\n    \\\\\\\"high_volatility\\\\\\\": dict(p_static=0.10, p_periodic=0.30, p_bursty=0.60, bursty_rate=0.30, period_range=(1.0, 5.0)),\\\\n}\\\\nREGIMES = list(REGIME_CONFIGS.keys())\\\\n\\\\n# policy knob grids -- shrunk from the originals (which had up to 15 points per family) to a\\\\n# handful of representative points per family so the demo covers the full hit-rate/stale-rate\\\\n# tradeoff space without the full 150-job replay grid\\\\nFIXED_TTL_GRID = [0.0, 1, 4, 1e6]  # include TTL=0 (always-miss) and TTL~inf (always-hit) sanity bounds\\\\nDTTL_GRID = [(h, c) for h in (0.7, 0.9) for c in (1.0,)]\\\\nEWMA_GRID = [(h, s) for h in (0.7, 0.9) for s in (0.15,)]\\\\nFRESHCACHE_GRID = [0.1, 0.2]\\\\nAIMD_GRID = [(a, b) for a in (0.5, 1.0) for b in (0.5, 0.7)]\\\\n\\\\nprint(f\\\\\\\"N_RESOURCES={N_RESOURCES}, N_EPISODES_PER_REGIME={N_EPISODES_PER_REGIME}, N_CALLS_PER_EPISODE={N_CALLS_PER_EPISODE}\\\\\\\")\\\\nprint(f\\\\\\\"regimes={REGIMES}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}", "updated_file": "{\n \"cells\": [\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"cell-title\",\n   \"metadata\": {},\n   \"source\": \"\\\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a simulated **LLM-agent tool-call loop** over a versioned, volatility-labeled resource corpus, replayed through several per-call-site cache policies:\\\\n\\\\n- **FixedTTLPolicy** — a hand-set fixed TTL per call site (standard-practice baseline).\\\\n- **DTTLPolicy** — the literal Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-approximation TTL update toward a target hit rate.\\\\n- **EWMAAdaptivePolicy** — a correctly-signed fixed-step EWMA-toward-target-hit-rate fallback baseline (added because the literal d-TTL update was found to get trapped at its TTL floor from a low initial TTL).\\\\n- **FreshCacheGatePolicy** / **FreshCachePooledPolicy** — a per-site MLE-fitted exponential staleness gate `P(stale|age) = 1 - exp(-lambda*age)`, with a partial-pooling variant for fairness across low-repeat sites.\\\\n- **AIMDPolicy (proposed)** — an additive-increase/multiplicative-decrease reuse window driven by confirmed spot-check outcomes rather than any statistical fit.\\\\n\\\\nAll policies are replayed through identical synthetic episode traces (Zipf-skewed working-set revisits over a small per-episode set of resources, with `static`/`periodic`/`bursty` version-change schedules) across three volatility regimes (low/medium/high). The notebook re-runs a small-scale version of this simulation directly (it is pure Python/NumPy — no LLM calls, no external dataset dependency, cost = $0) and compares it against a curated summary of the full-scale run (60 resources, 40 episodes/regime, 150 calls/episode) loaded from `mini_demo_data.json`.\\\\n\\\\nKey question: does AIMD's outcome-driven reuse window achieve a hit-rate/staleness tradeoff that isn't simply dominated by TTL/d-TTL/EWMA baselines, and does it adapt faster than FreshCache in the low-repeat-count regime where FreshCache's MLE fit never accumulates enough observations?\\\"\"\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"12979f58\",\n   \"source\": \"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\n_pip('loguru==0.7.3')\\\\n\\\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\\\nif 'google.colab' not in sys.modules:\\\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"7c7a07f4\",\n   \"source\": \"from __future__ import annotations\\\\n\\\\nimport json\\\\nimport math\\\\nimport sys\\\\nimport time\\\\nfrom collections import defaultdict\\\\nfrom dataclasses import dataclass, field\\\\nfrom pathlib import Path\\\\n\\\\nimport numpy as np\\\\nimport matplotlib.pyplot as plt\\\\nfrom loguru import logger\\\\n\\\\nlogger.remove()\\\\nlogger.add(sys.stdout, level=\\\\\\\"INFO\\\\\\\", format=\\\\\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"448206f1\",\n   \"source\": \"## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **full-scale run's** results (frontiers, dominance summary, convergence summary, and boundary sanity checks for all three volatility regimes at 60 resources / 40 episodes / 150 calls per episode). We load it here so the small-scale simulation this notebook runs below can be compared against the full-scale reference numbers at the end.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"d02497c3\",\n   \"source\": \"GITHUB_DATA_URL = \\\\\\\"https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\\\\\\\"\\\\nimport os\\\\n\\\\ndef load_data():\\\\n    try:\\\\n        import urllib.request\\\\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\\\\n            return json.loads(response.read().decode())\\\\n    except Exception: pass\\\\n    if os.path.exists(\\\\\\\"mini_demo_data.json\\\\\\\"):\\\\n        with open(\\\\\\\"mini_demo_data.json\\\\\\\") as f: return json.load(f)\\\\n    raise FileNotFoundError(\\\\\\\"Could not load mini_demo_data.json\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"acfc1511\",\n   \"source\": \"data = load_data()\\\\nprint(\\\\\\\"Loaded reference data. Top-level keys:\\\\\\\", list(data.keys()))\\\\nprint(\\\\\\\"Full-run verdict:\\\\\\\", data[\\\\\\\"verdict\\\\\\\"], \\\\\\\"| criteria:\\\\\\\", data[\\\\\\\"verdict_criteria\\\\\\\"])\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"3240607b\",\n   \"source\": \"## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in one place. Start at the smallest values that still produce a meaningful comparison across all three volatility regimes and all six policy families; scale up from here if time permits.\",\n   \"metadata\": {}\n  },\n  {\n   \"cell_type\": \"code\",\n   \"id\": \"e74a677a\",\n   \"source\": \"# --- ORIGINAL full-scale values (from method.py), kept as reference / commented ---\\\\n# N_RESOURCES = 60\\\\n# N_EPISODES_PER_REGIME = 40\\\\n# N_CALLS_PER_EPISODE = 150\\\\n\\\\n# --- DEMO (small-scale) values used in this notebook ---\\\\nN_RESOURCES = 20\\\\nN_EPISODES_PER_REGIME = 6\\\\nN_CALLS_PER_EPISODE = 60\\\\nEPISODE_HORIZON = 120.0  # ~ N_CALLS_PER_EPISODE * mean inter-call time, gives change-events room to occur\\\\nREPEAT_BIAS = 0.65  # probability a call re-touches an already-seen site this episode\\\\nSPOT_CHECK_RATE = 0.20  # background validity-check probability per cache hit (shared across adaptive policies)\\\\n\\\\nREGIME_CONFIGS = {\\\\n    # fraction of resources on each schedule + bursty rate + periodic period range\\\\n    \\\\\\\"low_volatility\\\\\\\": dict(p_static=0.70, p_periodic=0.20, p_bursty=0.10, bursty_rate=0.02, period_range=(20.0, 60.0)),\\\\n    \\\\\\\"medium_volatility\\\\\\\": dict(p_static=0.35, p_periodic=0.35, p_bursty=0.30, bursty_rate=0.08, period_range=(5.0, 20.0)),\\\\n    \\\\\\\"high_volatility\\\\\\\": dict(p_static=0.10, p_periodic=0.30, p_bursty=0.60, bursty_rate=0.30, period_range=(1.0, 5.0)),\\\\n}\\\\nREGIMES = list(REGIME_CONFIGS.keys())\\\\n\\\\n# policy knob grids -- shrunk from the originals (which had up to 15 points per family) to a\\\\n# handful of representative points per family so the demo covers the full hit-rate/stale-rate\\\\n# tradeoff space without the full 150-job replay grid\\\\nFIXED_TTL_GRID = [0.0, 1, 4, 1e6]  # include TTL=0 (always-miss) and TTL~inf (always-hit) sanity bounds\\\\nDTTL_GRID = [(h, c) for h in (0.7, 0.9) for c in (1.0,)]\\\\nEWMA_GRID = [(h, s) for h in (0.7, 0.9) for s in (0.15,)]\\\\nFRESHCACHE_GRID = [0.1, 0.2]\\\\nAIMD_GRID = [(a, b) for a in (0.5, 1.0) for b in (0.5, 0.7)]\\\\n\\\\nprint(f\\\\\\\"N_RESOURCES={N_RESOURCES}, N_EPISODES_PER_REGIME={N_EPISODES_PER_REGIME}, N_CALLS_PER_EPISODE={N_CALLS_PER_EPISODE}\\\\\\\")\\\\nprint(f\\\\\\\"regimes={REGIMES}\\\\\\\")\",\n   \"metadata\": {},\n   \"execution_count\": null,\n   \"outputs\": []\n  },\n  {\n   \"cell_type\": \"markdown\",\n   \"id\": \"66a97901\",\n   \"source\": \"## Stage 0/1 — Resource corpus + agent-loop call harness\\\\n\\\\nEach `Resource` represents a cacheable thing an agent tool call reads (a file, a search result, a computation), tagged with a `schedule` (`static`, `periodic`, or `bursty`) that determines when its ground-truth version changes. `simulate_episode` generates a Zipf-skewed sequence of call-site revisits over a small per-episode working set — exactly like an agent repeatedly re-reading the same file or re-running the same near-duplicate search within one episode. Time is kept **globally monotonic across episodes** so that adaptive policies (which carry per-site state across the whole regime) never see a spurious negative cache \\\"age\\\" at an episode boundary.\",\n   \"metadata\": {}\n  }\n ],\n \"metadata\": {\n  \"kernelspec\": {\n   \"display_name\": \"Python 3\",\n   \"language\": \"python\",\n   \"name\": \"python3\"\n  },\n  \"language_info\": {\n   \"name\": \"python\",\n   \"version\": \"3.12\"\n  }\n },\n \"nbformat\": 4,\n \"nbformat_minor\": 5\n}"}
```

### [47] TOOL CALL — NotebookEdit · 2026-08-10 06:07:12 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '66a97901', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': '@dataclass\\nclass Resource:\\n    \\"\\"\\"A cacheable resource an agent tool call reads (file, search result, computation).\\n\\n    schedule in {\'static\', \'periodic\', \'bursty\'}. value_version_at(t) is the\\n    ground-truth version id in force at simulated time t -- this is exactly\\n    known in simulation (unlike in a live deployment), which is what lets us\\n    score every cache decision\'s validity without any oracle ambiguity.\\n    \\"\\"\\"\\n\\n    resource_id: str\\n    schedule: str\\n    period: float = 1.0\\n    change_times: tuple = field(default_factory=tuple)  # precomputed for \'bursty\'\\n\\n    def value_version_at(self, t: float) -> int:\\n        if self.schedule == \\"static\\":\\n            return 0\\n        if self.schedule == \\"periodic\\":\\n            return int(t // self.period)\\n        if self.schedule == \\"bursty\\":\\n            # count of precomputed Poisson change-points at/before t\\n            lo, hi = 0, len(self.change_times)\\n            while lo < hi:\\n                mid = (lo + hi) // 2\\n                if self.change_times[mid] <= t:\\n                    lo = mid + 1\\n                else:\\n                    hi = mid\\n            return lo\\n        raise ValueError(f\\"unknown schedule {self.schedule}\\")\\n\\n\\ndef build_resource_corpus(regime: str, rng: np.random.Generator, total_horizon: float = EPISODE_HORIZON) -> dict[str, Resource]:\\n    \\"\\"\\"total_horizon must cover the FULL multi-episode timeline this corpus\\n    will be replayed against (n_episodes * EPISODE_HORIZON), since time is\\n    kept globally monotonic across episodes (see simulate_episode) -- a\\n    \'bursty\' resource\'s precomputed change-points need to span that whole\\n    range or later episodes would see a stale, un-extended change schedule.\\"\\"\\"\\n    cfg = REGIME_CONFIGS[regime]\\n    schedules = rng.choice(\\n        [\\"static\\", \\"periodic\\", \\"bursty\\"],\\n        size=N_RESOURCES,\\n        p=[cfg[\\"p_static\\"], cfg[\\"p_periodic\\"], cfg[\\"p_bursty\\"]],\\n    )\\n    resources: dict[str, Resource] = {}\\n    for i, sched in enumerate(schedules):\\n        rid = f\\"res_{i:03d}\\"\\n        if sched == \\"periodic\\":\\n            period = float(rng.uniform(*cfg[\\"period_range\\"]))\\n            resources[rid] = Resource(rid, \\"periodic\\", period=period)\\n        elif sched == \\"bursty\\":\\n            # Poisson process change-points over a long horizon covering all episodes\\n            horizon = total_horizon\\n            expected_events = max(1, int(cfg[\\"bursty_rate\\"] * horizon))\\n            change_times = np.sort(rng.uniform(0, horizon, size=expected_events)).tolist()\\n            resources[rid] = Resource(rid, \\"bursty\\", change_times=tuple(change_times))\\n        else:\\n            resources[rid] = Resource(rid, \\"static\\")\\n    return resources\\n\\n\\ndef simulate_episode(resources: dict[str, Resource], rng: np.random.Generator, n_calls: int, t_start: float = 0.0) -> list[dict]:\\n    \\"\\"\\"Zipf-skewed call-site revisits over a small per-episode working set.\\n\\n    t_start offsets this episode\'s clock so that, when many episodes are\\n    replayed through the SAME long-lived policy instance (the point of this\\n    experiment -- adaptive policies accumulate per-site state across\\n    episodes), simulated time stays globally monotonic across episode\\n    boundaries. Without this, a new episode\'s clock restarting at 0 while a\\n    stale cache entry still holds a LARGER timestamp from the prior episode\\n    produces a negative \\"age\\" (t - cached_at < 0), which satisfies \\"age <=\\n    ttl\\" for ANY ttl >= 0 -- a false hit that silently inflates every\\n    policy\'s measured hit rate, independent of its actual caching logic.\\n    \\"\\"\\"\\n    resource_ids = list(resources.keys())\\n    working_set_size = max(5, n_calls // 6)\\n    working_set = rng.choice(resource_ids, size=working_set_size, replace=False)\\n    # per call_site \\"signature\\" = resource touched via a specific (fn, arg) pattern;\\n    # in this simulation each working-set resource maps 1:1 to a call_site_id\\n    # (multiple *distinct* call sites can share a resource in richer setups, but\\n    # a 1:1 mapping is sufficient and keeps ground-truth validity unambiguous).\\n    calls: list[dict] = []\\n    t = t_start\\n    mean_gap = EPISODE_HORIZON / n_calls\\n    for _ in range(n_calls):\\n        if calls and rng.random() < REPEAT_BIAS:\\n            # Zipf-like skew: prefer sites already called, weighted toward earlier/more-frequent ones\\n            seen_sites = [c[\\"call_site_id\\"] for c in calls]\\n            counts = defaultdict(int)\\n            for s in seen_sites:\\n                counts[s] += 1\\n            uniq = list(counts.keys())\\n            weights = np.array([counts[s] for s in uniq], dtype=float) ** 1.3\\n            weights /= weights.sum()\\n            site = rng.choice(uniq, p=weights)\\n        else:\\n            site = rng.choice(working_set)\\n        t += float(rng.exponential(scale=mean_gap))\\n        true_version = resources[site].value_version_at(t)\\n        calls.append({\\"call_site_id\\": str(site), \\"timestamp\\": t, \\"true_version\\": int(true_version)})\\n    return calls\\n\\n\\n# Per-episode call gaps are exponential(mean=EPISODE_HORIZON/n_calls), so the\\n# SUM of n_calls gaps has mean EPISODE_HORIZON and std ~ EPISODE_HORIZON/sqrt(n_calls)\\n# (~8% of the mean at n_calls=150). A 5x slot margin puts episode-boundary\\n# overlap many standard deviations out, so consecutive episodes\' timelines\\n# cannot interleave and falsely produce negative cache \\"age\\" at the seam.\\nEPISODE_SLOT = EPISODE_HORIZON * 5.0\\n\\n\\ndef build_episodes(regime: str, seed: int, n_episodes: int) -> tuple[dict[str, Resource], list[list[dict]]]:\\n    \\"\\"\\"Build a resource corpus plus n_episodes worth of call traces with a\\n    GLOBALLY MONOTONIC clock across episode boundaries (see simulate_episode).\\"\\"\\"\\n    rng = np.random.default_rng(seed)\\n    total_horizon = n_episodes * EPISODE_SLOT\\n    resources = build_resource_corpus(regime, rng, total_horizon=total_horizon)\\n    episodes = [simulate_episode(resources, rng, N_CALLS_PER_EPISODE, t_start=i * EPISODE_SLOT) for i in range(n_episodes)]\\n    return resources, episodes'}
```

### [48] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:14 UTC

```
{"new_source": "@dataclass\\nclass Resource:\\n    \\\"\\\"\\\"A cacheable resource an agent tool call reads (file, search result, computation).\\n\\n    schedule in {'static', 'periodic', 'bursty'}. value_version_at(t) is the\\n    ground-truth version id in force at simulated time t -- this is exactly\\n    known in simulation (unlike in a live deployment), which is what lets us\\n    score every cache decision's validity without any oracle ambiguity.\\n    \\\"\\\"\... [truncated, 31356 chars total]
```

### [49] ASSISTANT · 2026-08-10 06:07:54 UTC

```
Now the Stage 2 cache policy classes (copy verbatim).
```

### [50] TOOL CALL — NotebookEdit · 2026-08-10 06:07:54 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'ea22c97e', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Stage 2 — Cache policy implementations\\n\\nEach policy exposes the same `on_call(site, t, true_version, checked)` interface, returning `(\\"hit\\"|\\"miss\\", valid)`. `checked` marks whether this particular hit happens to be a background spot-check (probability `SPOT_CHECK_RATE`), which is the only source of ground-truth feedback the adaptive policies get.'}
```

### [51] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:54 UTC

```
{"new_source": "## Stage 2 — Cache policy implementations\\n\\nEach policy exposes the same `on_call(site, t, true_version, checked)` interface, returning `(\\\"hit\\\"|\\\"miss\\\", valid)`. `checked` marks whether this particular hit happens to be a background spot-check (probability `SPOT_CHECK_RATE`), which is the only source of ground-truth feedback the adaptive policies get.", "cell_type": "markdown", "language": "python", "edit_mode": "insert", "cell_id": "d9637... [truncated, 32930 chars total]
```

### [52] TOOL CALL — NotebookEdit · 2026-08-10 06:07:54 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'd96377fb', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def clip(x: float, lo: float, hi: float) -> float:\\n    return max(lo, min(hi, x))\\n\\n\\nclass FixedTTLPolicy:\\n    \\"\\"\\"Standard-practice baseline: a single, hand-set TTL for every call site.\\"\\"\\"\\n\\n    name = \\"fixed_ttl\\"\\n\\n    def __init__(self, ttl: float):\\n        self.ttl = ttl\\n        self.cache: dict[str, tuple[int, float]] = {}\\n\\n    def knob_desc(self) -> dict:\\n        return {\\"ttl\\": self.ttl}\\n\\n    def on_call(self, site: str, t: float, true_version: int, checked: bool) -> tuple[str, bool]:\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.ttl:\\n                valid = version == true_version\\n                return \\"hit\\", valid\\n        self.cache[site] = (true_version, t)\\n        return \\"miss\\", True\\n\\n\\nclass DTTLPolicy:\\n    \\"\\"\\"d-TTL: Basu et al. 2017 (arXiv:1704.04448) Robbins-Monro stochastic-\\n    approximation TTL update toward a target hit rate h*, gamma_k=c/(k+1).\\"\\"\\"\\n\\n    name = \\"d_ttl\\"\\n\\n    def __init__(self, h_target: float, c: float = 1.0, ttl_min: float = 0.01, ttl_max: float = 1e4, ttl_init: float = 1.0):\\n        self.h_target = h_target\\n        self.c = c\\n        self.ttl_min = ttl_min\\n        self.ttl_max = ttl_max\\n        self.ttl: dict[str, float] = defaultdict(lambda: ttl_init)\\n        self.k: dict[str, int] = defaultdict(int)\\n        self.cache: dict[str, tuple[int, float]] = {}\\n        self.ttl_trajectory: dict[str, list[float]] = defaultdict(list)\\n\\n    def knob_desc(self) -> dict:\\n        return {\\"h_target\\": self.h_target, \\"c\\": self.c}\\n\\n    def on_call(self, site: str, t: float, true_version: int, checked: bool) -> tuple[str, bool]:\\n        hit_indicator = 0\\n        valid = True\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.ttl[site]:\\n                hit_indicator = 1\\n                valid = version == true_version\\n        self.k[site] += 1\\n        gamma = self.c / (self.k[site] + 1)\\n        self.ttl[site] = clip(self.ttl[site] + gamma * (hit_indicator - self.h_target), self.ttl_min, self.ttl_max)\\n        self.ttl_trajectory[site].append(self.ttl[site])\\n        if hit_indicator == 0:\\n            self.cache[site] = (true_version, t)\\n        return (\\"hit\\" if hit_indicator else \\"miss\\"), valid\\n\\n\\nclass EWMAAdaptivePolicy:\\n    \\"\\"\\"Fallback secondary adaptive baseline (fallback_plan item 2): a fixed-step\\n    EWMA-toward-target-hit-rate TTL update, used alongside d-TTL in case d-TTL\'s\\n    diminishing step size proves unstable at agent-episode (low-volume) traffic.\\"\\"\\"\\n\\n    name = \\"ewma_ttl\\"\\n\\n    def __init__(self, h_target: float, step: float = 0.15, ttl_min: float = 0.01, ttl_max: float = 1e4, ttl_init: float = 1.0):\\n        self.h_target = h_target\\n        self.step = step\\n        self.ttl_min = ttl_min\\n        self.ttl_max = ttl_max\\n        self.ttl: dict[str, float] = defaultdict(lambda: ttl_init)\\n        self.cache: dict[str, tuple[int, float]] = {}\\n        self.ttl_trajectory: dict[str, list[float]] = defaultdict(list)\\n\\n    def knob_desc(self) -> dict:\\n        return {\\"h_target\\": self.h_target, \\"step\\": self.step}\\n\\n    def on_call(self, site: str, t: float, true_version: int, checked: bool) -> tuple[str, bool]:\\n        hit_indicator = 0\\n        valid = True\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.ttl[site]:\\n                hit_indicator = 1\\n                valid = version == true_version\\n        # NOTE sign: (target - hit_indicator), the reverse of DTTLPolicy\'s literal\\n        # (hit_indicator - target). TTL and hit rate are monotonically related\\n        # (bigger TTL -> more hits), so root-finding \\"observed_hit_rate == target\\"\\n        # via stochastic approximation needs ttl to move UP when observed hit rate\\n        # is below target. DTTLPolicy above implements the artifact plan\'s update\\n        # literally as written (and that sign traps it at ttl_min from a low init,\\n        # see boundary_sanity_checks/dttl_stuck_at_floor_from_low_init) -- this\\n        # policy is the correctly-signed, fixed-step fallback (fallback_plan #2)\\n        # precisely so the AIMD-vs-adaptive-baseline comparison has one adaptive\\n        # baseline that isn\'t vacated by a sign instability from a bad init.\\n        self.ttl[site] = clip(self.ttl[site] + self.step * (self.h_target - hit_indicator), self.ttl_min, self.ttl_max)\\n        self.ttl_trajectory[site].append(self.ttl[site])\\n        if hit_indicator == 0:\\n            self.cache[site] = (true_version, t)\\n        return (\\"hit\\" if hit_indicator else \\"miss\\"), valid\\n\\n\\nclass FreshCacheGatePolicy:\\n    \\"\\"\\"Fitted per-call-site staleness-probability gate (FreshCache-style,\\n    Mansoor/Ahmad/Yoon 2026 exponential-decay staleness model):\\n    P(stale|age=a) = 1 - exp(-lambda_i * a), fit per site via MLE over\\n    observed (age, was_stale) spot-check pairs. Serves from cache only if\\n    predicted P(stale) <= error_budget.\\"\\"\\"\\n\\n    name = \\"freshcache\\"\\n\\n    def __init__(self, error_budget: float, lambda_prior: float = 0.1, min_obs_to_fit: int = 5):\\n        self.error_budget = error_budget\\n        self.lambda_prior = lambda_prior\\n        self.min_obs_to_fit = min_obs_to_fit\\n        self.lambda_est: dict[str, float] = defaultdict(lambda: lambda_prior)\\n        self.obs: dict[str, list[tuple[float, bool]]] = defaultdict(list)\\n        self.cache: dict[str, tuple[int, float]] = {}\\n        self.calibrated_sites: set[str] = set()\\n\\n    def knob_desc(self) -> dict:\\n        return {\\"error_budget\\": self.error_budget}\\n\\n    def predicted_stale_prob(self, site: str, age: float) -> float:\\n        return 1 - math.exp(-self.lambda_est[site] * age)\\n\\n    def _refit(self, site: str) -> None:\\n        obs = self.obs[site]\\n        if len(obs) < self.min_obs_to_fit:\\n            return\\n        ages = np.array([a for a, _ in obs])\\n        stale = np.array([1.0 if s else 0.0 for _, s in obs])\\n        # MLE for exponential-hazard rate: lambda solving mean predicted stale\\n        # prob matches observed stale fraction, via Newton\'s method on\\n        # sum(stale - (1-exp(-lambda*age))) = 0\\n        lam = self.lambda_est[site]\\n        for _ in range(25):\\n            pred = 1 - np.exp(-lam * ages)\\n            resid = np.sum(stale - pred)\\n            grad = np.sum(ages * np.exp(-lam * ages))\\n            if abs(grad) < 1e-12:\\n                break\\n            lam_new = lam + 0.05 * resid / (grad + 1e-9)\\n            lam = clip(lam_new, 1e-6, 100.0)\\n        self.lambda_est[site] = lam\\n        self.calibrated_sites.add(site)\\n\\n    def on_call(self, site: str, t: float, true_version: int, checked: bool) -> tuple[str, bool]:\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            age = t - cached_at\\n            if self.predicted_stale_prob(site, age) <= self.error_budget:\\n                valid = version == true_version\\n                if checked:\\n                    self.obs[site].append((age, not valid))\\n                    self._refit(site)\\n                return \\"hit\\", valid\\n        self.cache[site] = (true_version, t)\\n        return \\"miss\\", True\\n\\n\\nclass FreshCachePooledPolicy(FreshCacheGatePolicy):\\n    \\"\\"\\"Fairer reference variant (fallback_plan item 3): partial pooling of\\n    lambda across all sites sharing a resource-schedule \'family\' tag, so\\n    low-repeat sites still benefit from other sites\' calibration data.\\"\\"\\"\\n\\n    name = \\"freshcache_pooled\\"\\n\\n    def __init__(self, error_budget: float, site_to_family: dict[str, str], lambda_prior: float = 0.1, min_obs_to_fit: int = 5):\\n        super().__init__(error_budget, lambda_prior, min_obs_to_fit)\\n        self.site_to_family = site_to_family\\n        self.family_obs: dict[str, list[tuple[float, bool]]] = defaultdict(list)\\n        self.family_lambda: dict[str, float] = defaultdict(lambda: lambda_prior)\\n\\n    def predicted_stale_prob(self, site: str, age: float) -> float:\\n        fam = self.site_to_family.get(site, \\"default\\")\\n        lam = self.lambda_est[site] if site in self.calibrated_sites else self.family_lambda[fam]\\n        return 1 - math.exp(-lam * age)\\n\\n    def _refit(self, site: str) -> None:\\n        fam = self.site_to_family.get(site, \\"default\\")\\n        self.family_obs[fam].extend(self.obs[site][-1:])  # incremental pooled update\\n        super()._refit(site)\\n        pooled = self.family_obs[fam]\\n        if len(pooled) >= self.min_obs_to_fit:\\n            ages = np.array([a for a, _ in pooled])\\n            stale = np.array([1.0 if s else 0.0 for _, s in pooled])\\n            lam = self.family_lambda[fam]\\n            for _ in range(25):\\n                pred = 1 - np.exp(-lam * ages)\\n                resid = np.sum(stale - pred)\\n                grad = np.sum(ages * np.exp(-lam * ages))\\n                if abs(grad) < 1e-12:\\n                    break\\n                lam = clip(lam + 0.05 * resid / (grad + 1e-9), 1e-6, 100.0)\\n            self.family_lambda[fam] = lam\\n\\n\\nclass AIMDPolicy:\\n    \\"\\"\\"PROPOSED METHOD: additive-increase/multiplicative-decrease reuse window.\\n    Confirmed-valid spot-checked hits grow the window additively; a confirmed-\\n    stale spot-checked hit collapses it multiplicatively. No fitting needed --\\n    it is outcome-driven, so it should adapt even at low repeat counts where\\n    FreshCache\'s MLE fit never accumulates enough observations.\\"\\"\\"\\n\\n    name = \\"aimd\\"\\n\\n    def __init__(\\n        self,\\n        a: float,\\n        b: float,\\n        w_min: float = 0.01,\\n        w_max: float = 1e4,\\n        w_init: float = 1.0,\\n        presumed_valid_weight: float = 0.0,\\n    ):\\n        self.a = a\\n        self.b = b\\n        self.w_min = w_min\\n        self.w_max = w_max\\n        self.presumed_valid_weight = presumed_valid_weight  # ablation knob: 0 = conservative (default)\\n        self.w: dict[str, float] = defaultdict(lambda: w_init)\\n        self.cache: dict[str, tuple[int, float]] = {}\\n        self.confirmed_stale_count: dict[str, int] = defaultdict(int)\\n        self.confirmed_valid_count: dict[str, int] = defaultdict(int)\\n        self.w_trajectory: dict[str, list[float]] = defaultdict(list)\\n\\n    def knob_desc(self) -> dict:\\n        return {\\"a\\": self.a, \\"b\\": self.b, \\"presumed_valid_weight\\": self.presumed_valid_weight}\\n\\n    def on_call(self, site: str, t: float, true_version: int, checked: bool) -> tuple[str, bool]:\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.w[site]:\\n                valid = version == true_version\\n                if checked:\\n                    if valid:\\n                        self.w[site] = min(self.w[site] + self.a, self.w_max)\\n                        self.confirmed_valid_count[site] += 1\\n                    else:\\n                        self.w[site] = max(self.w[site] * self.b, self.w_min)\\n                        self.confirmed_stale_count[site] += 1\\n                    self.w_trajectory[site].append(self.w[site])\\n                elif self.presumed_valid_weight > 0:\\n                    self.w[site] = min(self.w[site] + self.presumed_valid_weight * self.a, self.w_max)\\n                    self.w_trajectory[site].append(self.w[site])\\n                return \\"hit\\", valid\\n        self.cache[site] = (true_version, t)\\n        return \\"miss\\", True'}
```

### [53] TOOL RESULT — NotebookEdit · 2026-08-10 06:07:55 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [54] ASSISTANT · 2026-08-10 06:08:01 UTC

```
Now the replay driver and dominance/frontier analysis section, followed by boundary sanity checks and main execution.
```

### [55] TOOL CALL — NotebookEdit · 2026-08-10 06:08:01 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'c07b4c6e', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Stage 3 — Replay driver\\n\\n`run_one_policy` replays every episode of a regime through one fresh policy instance and computes hit-rate/stale-rate statistics, including a low-repeat-count slice (sites visited &le;5 times overall) and a convergence-event summary (how many confirmed-feedback events it took for the policy's per-site knob — TTL, lambda, or window — to settle). This notebook runs the replay **sequentially** (no `ProcessPoolExecutor`) since the small demo grid finishes in well under a second per job."}
```

### [56] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:01 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [57] TOOL CALL — NotebookEdit · 2026-08-10 06:08:21 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '1d09b26a', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def make_policy_grid(site_to_family: dict[str, str]) -> dict[str, list]:\\n    grid: dict[str, list] = {\\n        \\"fixed_ttl\\": [FixedTTLPolicy(ttl=v) for v in FIXED_TTL_GRID],\\n        \\"d_ttl\\": [DTTLPolicy(h_target=h, c=c) for h, c in DTTL_GRID],\\n        \\"ewma_ttl\\": [EWMAAdaptivePolicy(h_target=h, step=s) for h, s in EWMA_GRID],\\n        \\"freshcache\\": [FreshCacheGatePolicy(error_budget=e) for e in FRESHCACHE_GRID],\\n        \\"freshcache_pooled\\": [FreshCachePooledPolicy(error_budget=e, site_to_family=site_to_family) for e in FRESHCACHE_GRID],\\n        \\"aimd\\": [AIMDPolicy(a=a, b=b) for a, b in AIMD_GRID],\\n    }\\n    return grid\\n\\n\\ndef rolling_band_convergence(trajectory: list[float], window: int = 8, tol: float = 0.10) -> int | None:\\n    \\"\\"\\"First index i such that for all j>=i, trajectory[j] stays within\\n    +/-tol of the trailing mean over [j-window, j). Returns None if never\\n    converges within the observed trajectory.\\"\\"\\"\\n    n = len(trajectory)\\n    if n < window + 1:\\n        return None\\n    for i in range(window, n):\\n        trailing = trajectory[max(0, i - window) : i]\\n        mean = sum(trailing) / len(trailing)\\n        if mean == 0:\\n            continue\\n        rest = trajectory[i:]\\n        if all(abs(v - mean) <= tol * abs(mean) for v in rest):\\n            return i\\n    return None\\n\\n\\ndef run_one_policy(regime: str, family: str, policy, resources: dict[str, Resource], episodes: list[list[dict]], seed: int) -> dict:\\n    \\"\\"\\"Replay all episodes of a regime through one (already-instantiated,\\n    fresh-state) policy instance and compute all summary statistics.\\"\\"\\"\\n    rng = np.random.default_rng(seed)\\n    site_visit_count: dict[str, int] = defaultdict(int)\\n    site_hit_count: dict[str, int] = defaultdict(int)\\n    site_stale_hit_count: dict[str, int] = defaultdict(int)\\n    site_confirmed_feedback_count: dict[str, int] = defaultdict(int)  # cumulative confirmed spot-check events, per site\\n    total_calls = 0\\n    total_hits = 0\\n    total_stale_hits = 0\\n    low_repeat_calls = 0\\n    low_repeat_hits = 0\\n    low_repeat_stale_hits = 0\\n\\n    for episode in episodes:\\n        for call in episode:\\n            site = call[\\"call_site_id\\"]\\n            checked = bool(rng.random() < SPOT_CHECK_RATE)\\n            decision, valid = policy.on_call(site, call[\\"timestamp\\"], call[\\"true_version\\"], checked)\\n            site_visit_count[site] += 1\\n            total_calls += 1\\n            if decision == \\"hit\\":\\n                total_hits += 1\\n                site_hit_count[site] += 1\\n                if not valid:\\n                    total_stale_hits += 1\\n                    site_stale_hit_count[site] += 1\\n            if checked and decision == \\"hit\\":\\n                site_confirmed_feedback_count[site] += 1\\n\\n    hit_rate = total_hits / total_calls if total_calls else 0.0\\n    stale_rate = total_stale_hits / total_hits if total_hits else 0.0  # staleness AMONG served hits (the risk actually incurred)\\n\\n    # low-repeat-count sub-slice: recompute stats restricted to calls at sites visited <=5 times overall\\n    low_repeat_sites = {s for s, n in site_visit_count.items() if n <= 5}\\n    for episode in episodes:\\n        for call in episode:\\n            if call[\\"call_site_id\\"] in low_repeat_sites:\\n                low_repeat_calls += 1\\n    # second pass needed for hit/stale counts restricted to those sites -- reuse per-site totals (decision-independent of order within a site\'s own trajectory would require replay; instead approximate via per-site aggregates which are exact since hit/stale are already accumulated per-site above)\\n    for s in low_repeat_sites:\\n        low_repeat_hits += site_hit_count[s]\\n        low_repeat_stale_hits += site_stale_hit_count[s]\\n    low_repeat_hit_rate = low_repeat_hits / low_repeat_calls if low_repeat_calls else 0.0\\n    low_repeat_stale_rate = low_repeat_stale_hits / low_repeat_hits if low_repeat_hits else 0.0\\n\\n    # convergence: for adaptive families, use per-site trajectories (window/ttl/lambda)\\n    convergence_events_per_site: list[int] = []\\n    calibrated_fraction = None\\n    if family in (\\"d_ttl\\", \\"ewma_ttl\\"):\\n        for site, traj in policy.ttl_trajectory.items():\\n            idx = rolling_band_convergence(traj)\\n            if idx is not None:\\n                # convergence reported in units of CONFIRMED feedback events consumed (currency the hypothesis cares about)\\n                convergence_events_per_site.append(min(idx, site_confirmed_feedback_count.get(site, idx)))\\n    elif family == \\"aimd\\":\\n        for site, traj in policy.w_trajectory.items():\\n            idx = rolling_band_convergence(traj)\\n            if idx is not None:\\n                convergence_events_per_site.append(idx)  # w_trajectory only appends on confirmed events already\\n    elif family in (\\"freshcache\\", \\"freshcache_pooled\\"):\\n        n_sites_seen = len(site_visit_count)\\n        n_calibrated = len(policy.calibrated_sites)\\n        calibrated_fraction = n_calibrated / n_sites_seen if n_sites_seen else 0.0\\n        for site in policy.calibrated_sites:\\n            # calibration point = when len(obs[site]) first reached min_obs_to_fit\\n            n_obs_needed = policy.min_obs_to_fit\\n            convergence_events_per_site.append(n_obs_needed)\\n\\n    convergence_events = float(np.median(convergence_events_per_site)) if convergence_events_per_site else None\\n\\n    return {\\n        \\"regime\\": regime,\\n        \\"policy_family\\": family,\\n        \\"knob\\": policy.knob_desc(),\\n        \\"total_calls\\": total_calls,\\n        \\"hit_rate\\": hit_rate,\\n        \\"stale_rate\\": stale_rate,\\n        \\"low_repeat_calls\\": low_repeat_calls,\\n        \\"low_repeat_hit_rate\\": low_repeat_hit_rate,\\n        \\"low_repeat_stale_rate\\": low_repeat_stale_rate,\\n        \\"n_low_repeat_sites\\": len(low_repeat_sites),\\n        \\"n_sites_total\\": len(site_visit_count),\\n        \\"convergence_events_median\\": convergence_events,\\n        \\"convergence_events_per_site\\": convergence_events_per_site,\\n        \\"calibrated_fraction\\": calibrated_fraction,\\n    }'}
```

### [58] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:21 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [59] ASSISTANT · 2026-08-10 06:08:27 UTC

```
Now the Stage 4/5 frontier/dominance analysis functions.
```

### [60] TOOL CALL — NotebookEdit · 2026-08-10 06:08:27 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'd00415ec', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Stage 4/5 — Pareto frontier + dominance + convergence summaries\\n\\n`pareto_frontier` finds the non-dominated (hit_rate, stale_rate) points per policy family. `compute_dominance` checks, per regime, whether every AIMD knob point is dominated by *some* fixed-TTL/d-TTL/EWMA baseline point — the core "does AIMD\'s tradeoff curve stand on its own" question (success criterion a).'}
```

### [61] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:27 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [62] TOOL CALL — NotebookEdit · 2026-08-10 06:08:43 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '36bb2d88', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def pareto_frontier(points: list[tuple[float, float, dict]]) -> list[dict]:\\n    \\"\\"\\"points: list of (hit_rate, stale_rate, full_result). A point is\\n    Pareto-efficient if no other point has >= hit_rate AND <= stale_rate\\n    (with at least one strict).\\"\\"\\"\\n    frontier = []\\n    for i, (h_i, s_i, r_i) in enumerate(points):\\n        dominated = False\\n        for j, (h_j, s_j, r_j) in enumerate(points):\\n            if i == j:\\n                continue\\n            if h_j >= h_i and s_j <= s_i and (h_j > h_i or s_j < s_i):\\n                dominated = True\\n                break\\n        if not dominated:\\n            frontier.append(r_i)\\n    return frontier\\n\\n\\ndef compute_dominance(results: list[dict]) -> dict:\\n    \\"\\"\\"For each regime: does some fixed_ttl/d_ttl/ewma_ttl point dominate each\\n    aimd point (>= hit_rate AND <= stale_rate)? Aggregate fraction non-dominated.\\"\\"\\"\\n    by_regime: dict[str, list[dict]] = defaultdict(list)\\n    for r in results:\\n        by_regime[r[\\"regime\\"]].append(r)\\n\\n    dominance_summary = {}\\n    for regime, rs in by_regime.items():\\n        aimd_points = [r for r in rs if r[\\"policy_family\\"] == \\"aimd\\"]\\n        baseline_points = [r for r in rs if r[\\"policy_family\\"] in (\\"fixed_ttl\\", \\"d_ttl\\", \\"ewma_ttl\\")]\\n        n_dominated = 0\\n        for a in aimd_points:\\n            for b in baseline_points:\\n                if b[\\"hit_rate\\"] >= a[\\"hit_rate\\"] and b[\\"stale_rate\\"] <= a[\\"stale_rate\\"] and (\\n                    b[\\"hit_rate\\"] > a[\\"hit_rate\\"] or b[\\"stale_rate\\"] < a[\\"stale_rate\\"]\\n                ):\\n                    n_dominated += 1\\n                    break\\n        n_total = len(aimd_points)\\n        dominance_summary[regime] = {\\n            \\"n_aimd_points\\": n_total,\\n            \\"n_dominated\\": n_dominated,\\n            \\"fraction_non_dominated\\": (n_total - n_dominated) / n_total if n_total else None,\\n        }\\n    return dominance_summary\\n\\n\\ndef compute_frontiers(results: list[dict]) -> dict:\\n    by_regime_family: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))\\n    for r in results:\\n        by_regime_family[r[\\"regime\\"]][r[\\"policy_family\\"]].append((r[\\"hit_rate\\"], r[\\"stale_rate\\"], r))\\n    frontiers = {}\\n    for regime, fam_points in by_regime_family.items():\\n        frontiers[regime] = {}\\n        for family, points in fam_points.items():\\n            eff = pareto_frontier(points)\\n            frontiers[regime][family] = sorted(\\n                [{\\"hit_rate\\": r[\\"hit_rate\\"], \\"stale_rate\\": r[\\"stale_rate\\"], \\"knob\\": r[\\"knob\\"]} for r in eff],\\n                key=lambda d: d[\\"hit_rate\\"],\\n            )\\n    return frontiers\\n\\n\\ndef compute_convergence_summary(results: list[dict]) -> dict:\\n    by_regime_family: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))\\n    for r in results:\\n        if r[\\"convergence_events_median\\"] is not None:\\n            by_regime_family[r[\\"regime\\"]][r[\\"policy_family\\"]].append(r[\\"convergence_events_median\\"])\\n    summary = {}\\n    for regime, fam_vals in by_regime_family.items():\\n        summary[regime] = {}\\n        for family, vals in fam_vals.items():\\n            arr = np.array(vals)\\n            summary[regime][family] = {\\n                \\"median\\": float(np.median(arr)),\\n                \\"p10\\": float(np.percentile(arr, 10)),\\n                \\"p90\\": float(np.percentile(arr, 90)),\\n                \\"n\\": len(arr),\\n            }\\n    return summary\\n\\n\\ndef compute_low_repeat_slice_summary(results: list[dict]) -> dict:\\n    by_regime_family: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))\\n    for r in results:\\n        by_regime_family[r[\\"regime\\"]][r[\\"policy_family\\"]].append(r)\\n    summary = {}\\n    for regime, fam_results in by_regime_family.items():\\n        summary[regime] = {}\\n        for family, rs in fam_results.items():\\n            # best-hit-rate-at-lowest-stale-rate knob per family, restricted to low-repeat slice\\n            best = min(rs, key=lambda r: (r[\\"low_repeat_stale_rate\\"], -r[\\"low_repeat_hit_rate\\"]))\\n            conv_vals = [r[\\"convergence_events_median\\"] for r in rs if r[\\"convergence_events_median\\"] is not None]\\n            cal_vals = [r[\\"calibrated_fraction\\"] for r in rs if r[\\"calibrated_fraction\\"] is not None]\\n            summary[regime][family] = {\\n                \\"best_low_repeat_hit_rate\\": best[\\"low_repeat_hit_rate\\"],\\n                \\"best_low_repeat_stale_rate\\": best[\\"low_repeat_stale_rate\\"],\\n                \\"median_convergence_events_low_repeat_context\\": float(np.median(conv_vals)) if conv_vals else None,\\n                \\"median_calibrated_fraction\\": float(np.median(cal_vals)) if cal_vals else None,\\n                \\"n_low_repeat_sites_typical\\": int(np.median([r[\\"n_low_repeat_sites\\"] for r in rs])),\\n            }\\n    return summary'}
```

### [63] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:43 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [64] ASSISTANT · 2026-08-10 06:08:51 UTC

```
Now boundary sanity checks and the main execution cell (running episodes, replaying grid, computing verdict).
```

### [65] TOOL CALL — NotebookEdit · 2026-08-10 06:08:51 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '0a8adade', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': '## Sanity / boundary checks\\n\\nBefore trusting any of the grid results, verify a few machine-checkable invariants: TTL=0 must give exactly 0% hit rate, TTL~inf on a static resource must give ~100% hit rate with 0% staleness, and the AIMD window must grow on confirmed-valid hits and collapse on a confirmed-stale hit (then recover). This also documents the d-TTL sign-instability finding (`dttl_stuck_at_floor_from_low_init`) rather than silently patching around it.'}
```

### [66] TOOL RESULT — NotebookEdit · 2026-08-10 06:08:51 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [67] TOOL CALL — NotebookEdit · 2026-08-10 06:09:15 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '5f88f065', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'def run_boundary_sanity_checks() -> dict:\\n    \\"\\"\\"TTL=0 -> ~0% hit rate; TTL~inf on fully-static resource -> ~100% hit\\n    rate & 0% stale rate. Also: AIMD window grows on repeated confirmed-valid\\n    hits and collapses after an injected confirmed-stale hit; d-TTL\'s TTL\\n    moves toward target hit rate on a never-stale synthetic resource.\\"\\"\\"\\n    logger.info(\\"Running boundary sanity checks...\\")\\n    checks = {}\\n\\n    # TTL=0 -> every call is a miss\\n    pol = FixedTTLPolicy(ttl=0.0)\\n    hits = 0\\n    for i in range(20):\\n        decision, valid = pol.on_call(\\"s1\\", float(i), 0, checked=True)\\n        hits += decision == \\"hit\\"\\n    checks[\\"ttl_zero_hit_rate\\"] = hits / 20\\n    assert checks[\\"ttl_zero_hit_rate\\"] == 0.0, \\"TTL=0 must give exactly 0% hit rate\\"\\n\\n    # TTL~inf on a fully static resource -> after first miss, all hits, all valid\\n    pol = FixedTTLPolicy(ttl=1e6)\\n    hits, valid_hits = 0, 0\\n    for i in range(20):\\n        decision, valid = pol.on_call(\\"s1\\", float(i), 0, checked=True)  # true_version always 0 (static)\\n        hits += decision == \\"hit\\"\\n        valid_hits += decision == \\"hit\\" and valid\\n    checks[\\"ttl_inf_hit_rate\\"] = hits / 20\\n    checks[\\"ttl_inf_stale_rate\\"] = 1 - (valid_hits / hits if hits else 1)\\n    assert checks[\\"ttl_inf_hit_rate\\"] >= 0.9, \\"TTL~inf on static resource should give ~100% hit rate\\"\\n    assert checks[\\"ttl_inf_stale_rate\\"] == 0.0, \\"TTL~inf on static resource should give 0% stale rate\\"\\n\\n    # AIMD window grows on repeated confirmed-valid hits\\n    pol = AIMDPolicy(a=1.0, b=0.5, w_init=1.0)\\n    pol.on_call(\\"s1\\", 0.0, 0, checked=True)  # miss, seeds cache\\n    w_before = pol.w[\\"s1\\"]\\n    for i in range(1, 6):\\n        pol.on_call(\\"s1\\", float(i) * 0.1, 0, checked=True)  # still version 0 -> confirmed valid\\n    w_after_growth = pol.w[\\"s1\\"]\\n    checks[\\"aimd_window_grows_on_valid_hits\\"] = w_after_growth > w_before\\n    assert checks[\\"aimd_window_grows_on_valid_hits\\"], \\"AIMD window must grow on confirmed-valid hits\\"\\n\\n    # AIMD window collapses after an injected confirmed-stale hit, then recovers\\n    pol.on_call(\\"s1\\", float(6) * 0.1, 1, checked=True)  # version changed to 1 -> confirmed stale\\n    w_after_collapse = pol.w[\\"s1\\"]\\n    checks[\\"aimd_window_collapses_on_stale_hit\\"] = w_after_collapse < w_after_growth\\n    assert checks[\\"aimd_window_collapses_on_stale_hit\\"], \\"AIMD window must collapse on confirmed-stale hit\\"\\n    # recovery: enough confirmed-valid hits afterward should grow it back above the post-collapse value\\n    t = 0.7\\n    for _ in range(10):\\n        t += 0.05\\n        pol.on_call(\\"s1\\", t, 1, checked=True)  # now version stably 1 -> valid again\\n    checks[\\"aimd_window_recovers_after_collapse\\"] = pol.w[\\"s1\\"] > w_after_collapse\\n    assert checks[\\"aimd_window_recovers_after_collapse\\"], \\"AIMD window must recover via additive increase\\"\\n\\n    # d-TTL trajectory sanity on a never-stale (static) resource: the artifact\\n    # plan\'s literal update rule is ttl += gamma*(hit_indicator - h_target).\\n    # With h_target=0.8 and a never-stale resource, this converges toward the\\n    # ttl_min FLOOR rather than growing (an increasing hit_indicator subtracts\\n    # a fixed positive h_target once TTL is small enough that the fresh miss\\n    # keeps hit_indicator=0, so the term stays negative and pushes down until\\n    # it hits ttl_min and sticks -- a genuine instability of the literal\\n    # Robbins-Monro sign convention at low ttl_init, exactly the kind of\\n    # instability fallback_plan item 2 anticipates). We do NOT silently flip\\n    # the sign to hide this -- we document it and additionally report the\\n    # EWMAAdaptivePolicy as the better-behaved secondary adaptive baseline.\\n    pol = DTTLPolicy(h_target=0.8, c=1.0, ttl_init=0.01, ttl_min=0.01, ttl_max=1e4)\\n    t = 0.0\\n    for i in range(200):\\n        t += 0.05\\n        pol.on_call(\\"s1\\", t, 0, checked=True)\\n    checks[\\"dttl_ttl_final_low_init\\"] = pol.ttl[\\"s1\\"]\\n    checks[\\"dttl_stuck_at_floor_from_low_init\\"] = pol.ttl[\\"s1\\"] <= pol.ttl_min * 1.5\\n\\n    # From a HIGH init (TTL already large enough to serve hits), the same\\n    # literal update rule is well-behaved: hit_indicator=1 most of the time,\\n    # (1 - 0.8) > 0 keeps nudging TTL further up, so it stabilizes at ttl_max\\n    # rather than oscillating -- confirming the direction-of-motion issue is\\n    # specific to the \\"TTL too small to ever hit\\" regime, not a universal bug.\\n    pol_hi = DTTLPolicy(h_target=0.8, c=1.0, ttl_init=50.0, ttl_min=0.01, ttl_max=1e4)\\n    t = 0.0\\n    for i in range(200):\\n        t += 0.05\\n        pol_hi.on_call(\\"s1\\", t, 0, checked=True)\\n    checks[\\"dttl_ttl_final_high_init\\"] = pol_hi.ttl[\\"s1\\"]\\n    checks[\\"dttl_well_behaved_from_high_init\\"] = pol_hi.ttl[\\"s1\\"] >= 50.0\\n    # EWMA secondary baseline: confirm it recovers from the same low init that traps d-TTL\\n    pol_ewma = EWMAAdaptivePolicy(h_target=0.8, step=0.15, ttl_init=0.01, ttl_min=0.01, ttl_max=1e4)\\n    t = 0.0\\n    for i in range(200):\\n        t += 0.05\\n        pol_ewma.on_call(\\"s1\\", t, 0, checked=True)\\n    checks[\\"ewma_ttl_final_low_init\\"] = pol_ewma.ttl[\\"s1\\"]\\n    checks[\\"ewma_recovers_from_low_init_where_dttl_gets_stuck\\"] = pol_ewma.ttl[\\"s1\\"] > checks[\\"dttl_ttl_final_low_init\\"]\\n\\n    logger.info(f\\"Boundary sanity checks PASSED: {checks}\\")\\n    return checks\\n\\n\\ndef run_low_repeat_mini_check(seed: int = 12345) -> dict:\\n    \\"\\"\\"Verify the low-repeat-count mechanism directly: on synthetic sites\\n    visited exactly 3-5 times, FreshCache\'s fit should fail to calibrate\\n    (lambda stays at prior) while AIMD\'s window should visibly move.\\"\\"\\"\\n    rng = np.random.default_rng(seed)\\n    fresh = FreshCacheGatePolicy(error_budget=0.2, min_obs_to_fit=5)\\n    aimd = AIMDPolicy(a=0.5, b=0.5, w_init=1.0)\\n    t = 0.0\\n    n_visits = 4  # within the 3-5 low-repeat band\\n    true_version = 0\\n    for i in range(n_visits):\\n        t += 1.0\\n        if i == 2:\\n            true_version = 1  # inject one staleness event\\n        fresh.on_call(\\"low_site\\", t, true_version, checked=True)\\n        aimd.on_call(\\"low_site\\", t, true_version, checked=True)\\n    result = {\\n        \\"freshcache_lambda_final\\": fresh.lambda_est[\\"low_site\\"],\\n        \\"freshcache_lambda_prior\\": fresh.lambda_prior,\\n        \\"freshcache_calibrated\\": \\"low_site\\" in fresh.calibrated_sites,\\n        \\"aimd_window_final\\": aimd.w[\\"low_site\\"],\\n        \\"aimd_window_init\\": 1.0,\\n        \\"aimd_window_moved\\": aimd.w[\\"low_site\\"] != 1.0,\\n    }\\n    assert not result[\\"freshcache_calibrated\\"], \\"FreshCache should NOT calibrate with only 4 observations < min_obs_to_fit=5\\"\\n    assert result[\\"aimd_window_moved\\"], \\"AIMD window should have moved even with only 4 observations\\"\\n    logger.info(f\\"Low-repeat mini-check PASSED: {result}\\")\\n    return result\\n\\n\\nt_start = time.time()\\nboundary_checks = run_boundary_sanity_checks()\\nlow_repeat_check = run_low_repeat_mini_check()'}
```

### [68] TOOL RESULT — NotebookEdit · 2026-08-10 06:09:15 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [69] ASSISTANT · 2026-08-10 06:09:43 UTC

```
Now the main run: build episodes for all regimes, replay the grid, compute frontiers/dominance/convergence/verdict.
```

### [70] TOOL CALL — NotebookEdit · 2026-08-10 06:09:43 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'cdb84a07', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Main run — build episodes, replay the policy grid, compute the verdict\\n\\nBuilds a resource corpus + episode traces per regime, then replays every (regime, policy_family, knob) combination in the shrunk demo grid and computes the frontier/dominance/convergence/low-repeat-slice summaries and the final MIXED/CONFIRMS/DISCONFIRMS verdict, exactly as in `main()` of the original script (minus the CLI arg parsing and `ProcessPoolExecutor`, which aren't needed for a small sequential demo run)."}
```

### [71] TOOL RESULT — NotebookEdit · 2026-08-10 06:09:43 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [72] TOOL CALL — NotebookEdit · 2026-08-10 06:09:43 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '0e9f2404', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'regimes = REGIMES\\nlogger.info(f\\"STEP: build resource corpora + episode traces for regimes={regimes}, n_episodes={N_EPISODES_PER_REGIME}\\")\\n\\nregime_data: dict[str, tuple[dict[str, Resource], list[list[dict]]]] = {}\\nfor ridx, regime in enumerate(regimes):\\n    resources, episodes = build_episodes(regime, seed=1000 + ridx, n_episodes=N_EPISODES_PER_REGIME)\\n    regime_data[regime] = (resources, episodes)\\n    n_calls = sum(len(e) for e in episodes)\\n    logger.info(f\\"  regime={regime}: {len(resources)} resources, {len(episodes)} episodes, {n_calls} calls\\")\\n\\nlogger.info(\\"STEP: build policy grid and replay\\")\\n\\nresults: list[dict] = []\\nfor regime in regimes:\\n    resources, episodes = regime_data[regime]\\n    site_to_family = {rid: r.schedule for rid, r in resources.items()}\\n    grid = {\\n        \\"fixed_ttl\\": [FixedTTLPolicy(ttl=v) for v in FIXED_TTL_GRID],\\n        \\"d_ttl\\": [DTTLPolicy(h_target=h, c=c) for h, c in DTTL_GRID],\\n        \\"ewma_ttl\\": [EWMAAdaptivePolicy(h_target=h, step=s) for h, s in EWMA_GRID],\\n        \\"freshcache\\": [FreshCacheGatePolicy(error_budget=e) for e in FRESHCACHE_GRID],\\n        \\"freshcache_pooled\\": [FreshCachePooledPolicy(error_budget=e, site_to_family=site_to_family) for e in FRESHCACHE_GRID],\\n        \\"aimd\\": [AIMDPolicy(a=a, b=b) for a, b in AIMD_GRID],\\n    }\\n    for family, policies in grid.items():\\n        for kidx, policy in enumerate(policies):\\n            seed = hash((regime, family, kidx)) % (2**31)\\n            results.append(run_one_policy(regime, family, policy, resources, episodes, seed))\\n\\nlogger.info(f\\"All {len(results)} replay jobs completed in {time.time() - t_start:.1f}s\\")\\n\\nfor r in results:\\n    assert 0.0 <= r[\\"hit_rate\\"] <= 1.0, f\\"hit_rate out of range: {r}\\"\\n    assert 0.0 <= r[\\"stale_rate\\"] <= 1.0, f\\"stale_rate out of range: {r}\\"\\n\\nlogger.info(\\"STEP: frontier + dominance + convergence + low-repeat-slice analysis\\")\\nfrontiers = compute_frontiers(results)\\ndominance_summary = compute_dominance(results)\\nconvergence_summary = compute_convergence_summary(results)\\nlow_repeat_slice_summary = compute_low_repeat_slice_summary(results)\\n\\n# success criterion (a): AIMD\'s Pareto frontier is not dominated by adaptive/fixed baselines\\nfrac_non_dominated_vals = [\\n    d[\\"fraction_non_dominated\\"] for d in dominance_summary.values() if d[\\"fraction_non_dominated\\"] is not None\\n]\\ncriterion_a_pass = bool(frac_non_dominated_vals) and (np.mean(frac_non_dominated_vals) >= 0.5)\\n\\n# success criterion (b): in the low-repeat-count slice, AIMD converges faster (fewer confirmed-staleness\\n# feedback events) than d_ttl/ewma_ttl, AND FreshCache fails to calibrate for a majority of low-repeat sites\\naimd_conv = []\\nbaseline_conv = []\\nfreshcache_cal_fracs = []\\nfor regime, fam_summary in low_repeat_slice_summary.items():\\n    if \\"aimd\\" in fam_summary and fam_summary[\\"aimd\\"][\\"median_convergence_events_low_repeat_context\\"] is not None:\\n        aimd_conv.append(fam_summary[\\"aimd\\"][\\"median_convergence_events_low_repeat_context\\"])\\n    for fam in (\\"d_ttl\\", \\"ewma_ttl\\"):\\n        if fam in fam_summary and fam_summary[fam][\\"median_convergence_events_low_repeat_context\\"] is not None:\\n            baseline_conv.append(fam_summary[fam][\\"median_convergence_events_low_repeat_context\\"])\\n    for fam in (\\"freshcache\\", \\"freshcache_pooled\\"):\\n        if fam in fam_summary and fam_summary[fam][\\"median_calibrated_fraction\\"] is not None:\\n            freshcache_cal_fracs.append(fam_summary[fam][\\"median_calibrated_fraction\\"])\\n\\ncriterion_b_convergence = bool(aimd_conv and baseline_conv) and (float(np.median(aimd_conv)) <= float(np.median(baseline_conv)))\\ncriterion_b_freshcache_fails = bool(freshcache_cal_fracs) and (float(np.median(freshcache_cal_fracs)) < 0.5)\\ncriterion_b_pass = criterion_b_convergence and criterion_b_freshcache_fails\\n\\nif criterion_a_pass and criterion_b_pass:\\n    verdict = \\"CONFIRMS\\"\\nelif not criterion_a_pass and not criterion_b_pass:\\n    verdict = \\"DISCONFIRMS\\"\\nelse:\\n    verdict = \\"MIXED\\"\\n\\nlogger.info(f\\"criterion_a_pass(frontier)={criterion_a_pass} (mean_frac_non_dominated={np.mean(frac_non_dominated_vals) if frac_non_dominated_vals else None})\\")\\nlogger.info(\\n    f\\"criterion_b_pass(low-repeat convergence+freshcache failure)={criterion_b_pass} \\"\\n    f\\"(aimd_conv_median={np.median(aimd_conv) if aimd_conv else None}, \\"\\n    f\\"baseline_conv_median={np.median(baseline_conv) if baseline_conv else None}, \\"\\n    f\\"freshcache_calibrated_fraction_median={np.median(freshcache_cal_fracs) if freshcache_cal_fracs else None})\\"\\n)\\nlogger.info(f\\"DEMO-SCALE VERDICT: {verdict}\\")\\nlogger.info(f\\"Done in {time.time() - t_start:.1f}s total.\\")'}
```

### [73] TOOL RESULT — NotebookEdit · 2026-08-10 06:09:43 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [74] ASSISTANT · 2026-08-10 06:09:49 UTC

```
Now the visualization/results cell.
```

### [75] TOOL CALL — NotebookEdit · 2026-08-10 06:09:49 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': '6a2dbd6d', 'edit_mode': 'insert', 'cell_type': 'markdown', 'new_source': "## Results — demo-scale run vs. the full-scale reference\\n\\nBelow: a summary table of this notebook's demo-scale results, plus Pareto frontier plots (hit rate vs. stale rate) per regime comparing every policy family, and a side-by-side of this notebook's dominance summary against the full-scale reference loaded from `mini_demo_data.json`."}
```

### [76] TOOL RESULT — NotebookEdit · 2026-08-10 06:09:49 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [77] TOOL CALL — NotebookEdit · 2026-08-10 06:10:09 UTC

```
{'notebook_path': '/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/code_demo.ipynb', 'cell_id': 'f4b69719', 'edit_mode': 'insert', 'cell_type': 'code', 'new_source': 'print(f\\"{\'regime\':<18}{\'policy_family\':<18}{\'n_pts\':<8}{\'n_dominated\':<14}{\'frac_non_dominated\':<20}\\")\\nfor regime, d in dominance_summary.items():\\n    print(f\\"{regime:<18}{\'aimd\':<18}{d[\'n_aimd_points\']:<8}{d[\'n_dominated\']:<14}{str(round(d[\'fraction_non_dominated\'], 3)) if d[\'fraction_non_dominated\'] is not None else \'None\':<20}\\")\\n\\nprint()\\nprint(\\"Demo-scale verdict:\\", verdict, \\"| criteria: a(frontier)=\\", criterion_a_pass, \\" b(low-repeat)=\\", criterion_b_pass)\\nprint(\\"Full-scale reference verdict (mini_demo_data.json):\\", data[\\"verdict\\"], \\"| criteria:\\", data[\\"verdict_criteria\\"])\\n\\nfig, axes = plt.subplots(1, len(regimes), figsize=(6 * len(regimes), 5), sharey=True)\\nif len(regimes) == 1:\\n    axes = [axes]\\ncolors = {\\n    \\"fixed_ttl\\": \\"tab:blue\\", \\"d_ttl\\": \\"tab:orange\\", \\"ewma_ttl\\": \\"tab:green\\",\\n    \\"freshcache\\": \\"tab:red\\", \\"freshcache_pooled\\": \\"tab:purple\\", \\"aimd\\": \\"black\\",\\n}\\nfor ax, regime in zip(axes, regimes):\\n    rs = [r for r in results if r[\\"regime\\"] == regime]\\n    for family in colors:\\n        fam_pts = [r for r in rs if r[\\"policy_family\\"] == family]\\n        if not fam_pts:\\n            continue\\n        xs = [r[\\"hit_rate\\"] for r in fam_pts]\\n        ys = [r[\\"stale_rate\\"] for r in fam_pts]\\n        marker = \\"*\\" if family == \\"aimd\\" else \\"o\\"\\n        size = 140 if family == \\"aimd\\" else 50\\n        ax.scatter(xs, ys, label=family, color=colors[family], marker=marker, s=size, alpha=0.85, edgecolors=\\"white\\", linewidths=0.5)\\n    ax.set_title(regime)\\n    ax.set_xlabel(\\"hit rate\\")\\n    ax.set_ylabel(\\"stale rate (among served hits)\\")\\nhandles, labels = axes[0].get_legend_handles_labels()\\nfig.legend(handles, labels, loc=\\"upper center\\", ncol=len(colors), bbox_to_anchor=(0.5, 1.08))\\nfig.suptitle(\\"Demo-scale hit-rate vs. stale-rate frontier, by policy family and regime\\", y=1.15)\\nplt.tight_layout()\\nplt.show()\\n\\n# side-by-side dominance comparison: this notebook\'s demo-scale run vs. the full-scale reference\\nfig2, ax2 = plt.subplots(figsize=(7, 4))\\nregime_labels = list(dominance_summary.keys())\\ndemo_vals = [dominance_summary[r][\\"fraction_non_dominated\\"] or 0.0 for r in regime_labels]\\nref_vals = [data[\\"dominance_summary\\"][r][\\"fraction_non_dominated\\"] or 0.0 for r in regime_labels]\\nx = np.arange(len(regime_labels))\\nwidth = 0.35\\nax2.bar(x - width / 2, demo_vals, width, label=\\"demo-scale (this notebook)\\")\\nax2.bar(x + width / 2, ref_vals, width, label=\\"full-scale reference\\")\\nax2.set_xticks(x)\\nax2.set_xticklabels(regime_labels)\\nax2.set_ylabel(\\"fraction of AIMD points non-dominated\\")\\nax2.set_title(\\"AIMD frontier non-domination: demo-scale vs. full-scale reference\\")\\nax2.legend()\\nplt.tight_layout()\\nplt.show()\\n\\nprint(\\"\\\\nLow-repeat mini-check:\\", low_repeat_check)\\nprint(\\"Boundary sanity checks:\\", {k: v for k, v in boundary_checks.items() if isinstance(v, bool)})'}
```

### [78] TOOL RESULT — NotebookEdit · 2026-08-10 06:10:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [79] ASSISTANT · 2026-08-10 06:10:17 UTC

```
Now let's test-run the notebook in a clean venv.
```

### [80] TOOL CALL — Bash · 2026-08-10 06:10:17 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
/usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5
.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -10
```

### [81] TOOL RESULT — Bash · 2026-08-10 06:12:13 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bpknehqmf", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [82] ASSISTANT · 2026-08-10 06:12:19 UTC

```
I'll wait for that to finish in the background.
```

### [83] TOOL CALL — Bash · 2026-08-10 06:12:19 UTC

```
sleep 60; tail -20 /tmp/claude-0/-ai-inventor-aii-data-runs-run-MmmgOkQFZ5uI-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art-qtEtMpLZuRGI/fd6b7233-68bb-4c40-928c-20e5550cd19e/tasks/bpknehqmf.output
```

### [84] TOOL RESULT — Bash [ERROR] · 2026-08-10 06:12:19 UTC

```
Error: Blocked: sleep 60 followed by: tail -20 /tmp/claude-0/-ai-inventor-aii-data-runs-run-MmmgOkQFZ5uI-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art-qtEtMpLZuRGI/fd6b7233-68bb-4c40-928c-20e5550cd19e/tasks/bpknehqmf.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [85] TOOL CALL — ToolSearch · 2026-08-10 06:12:19 UTC

```
{'query': 'select:Monitor'}
```

### [86] TOOL RESULT — ToolSearch · 2026-08-10 06:12:19 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 22}
```

### [87] TOOL CALL — Monitor · 2026-08-10 06:12:25 UTC

```
{'command': 'until [ -f "/tmp/claude-0/-ai-inventor-aii-data-runs-run-MmmgOkQFZ5uI-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art-qtEtMpLZuRGI/fd6b7233-68bb-4c40-928c-20e5550cd19e/tasks/bpknehqmf.output" ]; do sleep 2; done\ntail -f "/tmp/claude-0/-ai-inventor-aii-data-runs-run-MmmgOkQFZ5uI-4-gen-paper-repo--3-gen-demo-art-notebook-workspaces-iter-1-art-qtEtMpLZuRGI/fd6b7233-68bb-4c40-928c-20e5550cd19e/tasks/bpknehqmf.output" &\nTAIL_PID=$!\nwhile kill -0 $TAIL_PID 2>/dev/null; do\n  if ! pgrep -f "bpknehqmf" >/dev/null 2>&1; then\n    sleep 1\n    kill $TAIL_PID 2>/dev/null\n    echo "DONE"\n    break\n  fi\n  sleep 3\ndone', 'description': 'wait for pip install of jupyter to finish', 'timeout_ms': 300000, 'persistent': False}
```

### [88] TOOL RESULT — Monitor · 2026-08-10 06:12:25 UTC

```
{"taskId": "brpcmz57a", "timeoutMs": 300000, "persistent": false}
```

### [89] TOOL CALL — Bash · 2026-08-10 06:12:29 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
ls .nb_env/bin/ 2>&1 | head -5
```

### [90] TOOL RESULT — Bash · 2026-08-10 06:12:29 UTC

```
{"stdout": "Activate.ps1\nactivate\nactivate.csh\nactivate.fish\ndebugpy", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [91] ASSISTANT · 2026-08-10 06:12:31 UTC

```
Waiting for the pip install to finish before running nbconvert.
```

### [92] TOOL CALL — TaskOutput · 2026-08-10 06:12:31 UTC

```
{'task_id': 'bpknehqmf', 'block': True, 'timeout': 30000}
```

### [93] TOOL RESULT — TaskOutput · 2026-08-10 06:13:01 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "bpknehqmf", "task_type": "local_bash", "status": "running", "description": "cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\n/usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5\n.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -10", "output": "", "exitCode": null}}
```

### [94] TOOL CALL — TaskOutput · 2026-08-10 06:15:03 UTC

```
{'task_id': 'bpknehqmf', 'block': 'true', 'timeout': 120000}
```

### [95] TOOL RESULT — TaskOutput · 2026-08-10 06:15:03 UTC

```
{"retrieval_status": "timeout", "task": {"task_id": "bpknehqmf", "task_type": "local_bash", "status": "running", "description": "cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\n/usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5\n.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -10", "output": "", "exitCode": null}}
```

### [96] TOOL CALL — TaskOutput · 2026-08-10 06:15:43 UTC

```
{'task_id': 'bpknehqmf', 'block': 'true', 'timeout': 180000}
```

### [97] TOOL RESULT — TaskOutput · 2026-08-10 06:15:43 UTC

```
{"retrieval_status": "success", "task": {"task_id": "bpknehqmf", "task_type": "local_bash", "status": "completed", "description": "cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\n/usr/local/bin/python3.12 -m venv .nb_env 2>&1 | tail -5\n.nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -10", "output": "\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n", "exitCode": 0}}
```

### [98] ASSISTANT · 2026-08-10 06:15:51 UTC

```
Good, jupyter install finished. Now run the notebook.
```

### [99] TOOL CALL — Bash · 2026-08-10 06:15:51 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbconvert.log 2>&1 &
echo $! > nbconvert.pid
sleep 2; cat nbconvert.pid
```

### [100] TOOL RESULT — Bash · 2026-08-10 06:15:51 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bchm7tpu6", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [101] TOOL CALL — TaskOutput · 2026-08-10 06:15:53 UTC

```
{'task_id': 'bchm7tpu6', 'block': 'true', 'timeout': 300000}
```

### [102] TOOL RESULT — TaskOutput · 2026-08-10 06:15:53 UTC

```
{"retrieval_status": "success", "task": {"task_id": "bchm7tpu6", "task_type": "local_bash", "status": "completed", "description": "cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\n.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbconvert.log 2>&1 &\necho $! > nbconvert.pid\nsleep 2; cat nbconvert.pid", "output": "409\n", "exitCode": 0}}
```

### [103] ASSISTANT · 2026-08-10 06:15:57 UTC

```
That's just the launcher exiting after echoing the PID; the actual nbconvert process (PID 409) runs in background. Let me poll it.
```

### [104] TOOL CALL — Monitor · 2026-08-10 06:15:57 UTC

```
{'command': 'cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\nPID=$(cat nbconvert.pid)\nwhile kill -0 $PID 2>/dev/null; do sleep 5; done\necho "NBCONVERT_DONE exit_check"\ntail -40 nbconvert.log', 'description': 'wait for notebook execution to finish', 'timeout_ms': 650000, 'persistent': False}
```

### [105] TOOL RESULT — Monitor · 2026-08-10 06:15:57 UTC

```
{"taskId": "balah2myu", "timeoutMs": 650000, "persistent": false}
```

### [106] ASSISTANT · 2026-08-10 06:16:17 UTC

```
I'll wait for that notification rather than poll further.
```

### [107] TOOL CALL — TaskOutput · 2026-08-10 06:16:17 UTC

```
{'task_id': 'balah2myu', 'block': 'true', 'timeout': 600000}
```

### [108] TOOL RESULT — TaskOutput · 2026-08-10 06:16:17 UTC

```
{"retrieval_status": "success", "task": {"task_id": "balah2myu", "task_type": "local_bash", "status": "completed", "description": "wait for notebook execution to finish", "output": "NBCONVERT_DONE exit_check\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/notebook.py\", line 36, in from_notebook_node\n    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 154, in from_notebook_node\n    nb_copy, resources = self._preprocess(nb_copy, resources)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 353, in _preprocess\n    nbc, resc = preprocessor(nbc, resc)\n                ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/base.py\", line 48, in __call__\n    return self.preprocess(nb, resources)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 103, in preprocess\n    self.preprocess_cell(cell, resources, index)\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 124, in preprocess_cell\n    cell = self.execute_cell(cell, index, store_history=True)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/jupyter_core/utils/__init__.py\", line 165, in wrapped\n    return loop.run_until_complete(inner)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/asyncio/base_events.py\", line 691, in run_until_complete\n    return future.result()\n           ^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 1062, in async_execute_cell\n    await self._check_raise_for_error(cell, cell_index, exec_reply)\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 918, in _check_raise_for_error\n    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)\nnbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:\n------------------\nimport subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# psutil, loguru — NOT pre-installed on Colab, always install\\n_pip('psutil==6.1.1')\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\n------------------\n\n\n  \u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[1]\u001b[39m\u001b[32m, line 1\u001b[39m\n\u001b[31m    \u001b[39m\u001b[31mimport subprocess, sys\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\n\\n# psutil, loguru — NOT pre-installed on Colab, always install\\n_pip('psutil==6.1.1')\\n_pip('loguru==0.7.3')\\n\\n# numpy, matplotlib — pre-installed on Colab, install locally only (to match Colab's exact versions)\\nif 'google.colab' not in sys.modules:\\n    _pip('numpy==2.0.2', 'matplotlib==3.10.0')\u001b[39m\n                           ^\n\u001b[31mSyntaxError\u001b[39m\u001b[31m:\u001b[39m unexpected character after line continuation character\n\n\n", "exitCode": 0}}
```

### [109] TOOL CALL — Bash · 2026-08-10 06:16:23 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
c=nb['cells'][1]
print(repr(c['source'][:200]))
"
```

### [110] TOOL RESULT — Bash · 2026-08-10 06:16:23 UTC

```
{"stdout": "\"import subprocess, sys\\\\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\\\\n\\\\n# psutil, loguru — NOT pre-installed on Colab, always install\\\\n_pip('psutil==6.1.1')\\\\\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [111] ASSISTANT · 2026-08-10 06:16:29 UTC

```
All code cells have literal `\n` instead of real newlines. Let me fix this by post-processing the notebook JSON directly.
```

### [112] TOOL CALL — Bash · 2026-08-10 06:16:29 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']=='code' and isinstance(c['source'], str):
        lines = c['source'].split('\\\\n')
        c['source'] = [l+'\n' for l in lines[:-1]] + [lines[-1]]
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
print('fixed')
"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
print(''.join(nb['cells'][1]['source'])[:200])
"
```

### [113] TOOL RESULT — Bash · 2026-08-10 06:16:29 UTC

```
{"stdout": "fixed\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# psutil, loguru — NOT pre-installed on Colab, always install\n_pip('psutil==6.1.1')\n_pip", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [114] ASSISTANT · 2026-08-10 06:16:31 UTC

```
Fixed. Now re-run the test.
```

### [115] TOOL CALL — Bash · 2026-08-10 06:16:31 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
bad=[i for i,c in enumerate(nb['cells']) if isinstance(c['source'], str)]
print('still-string cells:', bad)
print('total cells:', len(nb['cells']))
"
```

### [116] TOOL RESULT — Bash · 2026-08-10 06:16:31 UTC

```
{"stdout": "still-string cells: [0, 3, 6, 8, 10, 12, 14, 16, 18, 20]\ntotal cells: 22", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [117] TOOL CALL — Bash · 2026-08-10 06:16:35 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i in [0,3,6,8,10,12,14,16,18,20]:
    c=nb['cells'][i]
    print(i, c['cell_type'], repr(c['source'][:80]))
"
```

### [118] TOOL RESULT — Bash · 2026-08-10 06:16:35 UTC

```
{"stdout": "0 markdown '\"# AIMD Reuse-Window Caching vs TTL Baselines\\\\n\\\\nThis notebook demonstrates a si'\n3 markdown '## Load reference data\\\\n\\\\n`mini_demo_data.json` is a curated subset of the **ful'\n6 markdown '## Config\\\\n\\\\nAll tunable parameters from the original `method.py`, collected in '\n8 markdown '## Stage 0/1 — Resource corpus + agent-loop call harness\\\\n\\\\nEach `Resource` repr'\n10 markdown '## Stage 2 — Cache policy implementations\\\\n\\\\nEach policy exposes the same `on_ca'\n12 markdown '## Stage 3 — Replay driver\\\\n\\\\n`run_one_policy` replays every episode of a regime'\n14 markdown '## Stage 4/5 — Pareto frontier + dominance + convergence summaries\\\\n\\\\n`pareto_fr'\n16 markdown '## Sanity / boundary checks\\\\n\\\\nBefore trusting any of the grid results, verify a'\n18 markdown '## Main run — build episodes, replay the policy grid, compute the verdict\\\\n\\\\nBui'\n20 markdown '## Results — demo-scale run vs. the full-scale reference\\\\n\\\\nBelow: a summary tab'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [119] ASSISTANT · 2026-08-10 06:16:49 UTC

```
These markdown cells too. Also cell 0 has a stray leading `"` character. Let me fix all of them.
```

### [120] TOOL CALL — Bash · 2026-08-10 06:16:49 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if isinstance(c['source'], str):
        s = c['source']
        if s.startswith('\"') and s.endswith('\"'):
            s = s[1:-1]
        lines = s.split('\\\\n')
        c['source'] = [l+'\n' for l in lines[:-1]] + [lines[-1]]
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
bad=[i for i,c in enumerate(nb['cells']) if isinstance(c['source'], str)]
print('still-string cells:', bad)
print(''.join(nb['cells'][0]['source'])[:100])
"
```

### [121] TOOL RESULT — Bash · 2026-08-10 06:16:49 UTC

```
{"stdout": "still-string cells: []\n# AIMD Reuse-Window Caching vs TTL Baselines\n\nThis notebook demonstrates a simulated **LLM-agent too", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [122] ASSISTANT · 2026-08-10 06:16:49 UTC

```
Now re-run the notebook test.
```

### [123] TOOL CALL — Bash · 2026-08-10 06:16:49 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbconvert2.log 2>&1 &
echo $! > nbconvert2.pid
sleep 2; cat nbconvert2.pid
```

### [124] TOOL RESULT — Bash · 2026-08-10 06:16:49 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bxujln55l", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [125] TOOL CALL — Monitor · 2026-08-10 06:16:53 UTC

```
{'command': 'cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\nPID=$(cat nbconvert2.pid)\nwhile kill -0 $PID 2>/dev/null; do sleep 5; done\necho "NBCONVERT2_DONE"\ntail -60 nbconvert2.log', 'description': 'wait for second notebook execution attempt to finish', 'timeout_ms': 650000, 'persistent': False}
```

### [126] TOOL RESULT — Monitor · 2026-08-10 06:16:53 UTC

```
{"taskId": "bmvvvrlij", "timeoutMs": 650000, "persistent": false}
```

### [127] TOOL CALL — TaskOutput · 2026-08-10 06:19:03 UTC

```
{'task_id': 'bmvvvrlij', 'block': 'true', 'timeout': 600000}
```

### [128] TOOL RESULT — TaskOutput · 2026-08-10 06:19:03 UTC

```
{"retrieval_status": "success", "task": {"task_id": "bmvvvrlij", "task_type": "local_bash", "status": "completed", "description": "wait for second notebook execution attempt to finish", "output": "NBCONVERT2_DONE\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 201, in from_filename\n    return self.from_file(f, resources=resources, **kw)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 220, in from_file\n    return self.from_notebook_node(\n           ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/notebook.py\", line 36, in from_notebook_node\n    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 154, in from_notebook_node\n    nb_copy, resources = self._preprocess(nb_copy, resources)\n                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/exporters/exporter.py\", line 353, in _preprocess\n    nbc, resc = preprocessor(nbc, resc)\n                ^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/base.py\", line 48, in __call__\n    return self.preprocess(nb, resources)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 103, in preprocess\n    self.preprocess_cell(cell, resources, index)\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbconvert/preprocessors/execute.py\", line 124, in preprocess_cell\n    cell = self.execute_cell(cell, index, store_history=True)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/jupyter_core/utils/__init__.py\", line 165, in wrapped\n    return loop.run_until_complete(inner)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/usr/local/lib/python3.12/asyncio/base_events.py\", line 691, in run_until_complete\n    return future.result()\n           ^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 1062, in async_execute_cell\n    await self._check_raise_for_error(cell, cell_index, exec_reply)\n  File \"/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.nb_env/lib/python3.12/site-packages/nbclient/client.py\", line 918, in _check_raise_for_error\n    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)\nnbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:\n------------------\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nimport time\nfrom collections import defaultdict\nfrom dataclasses import dataclass, field\nfrom pathlib import Path\n\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom loguru import logger\n\nlogger.remove()\nlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\n------------------\n\n\n  \u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[2]\u001b[39m\u001b[32m, line 16\u001b[39m\n\u001b[31m    \u001b[39m\u001b[31mlogger.add(sys.stdout, level=\\\"INFO\\\", format=\\\"{time:HH:mm:ss}|{level:<7}|{message}\\\")\u001b[39m\n                                  ^\n\u001b[31mSyntaxError\u001b[39m\u001b[31m:\u001b[39m unexpected character after line continuation character\n\n\n", "exitCode": 0}}
```

### [129] TOOL CALL — Bash · 2026-08-10 06:19:09 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    c['source'] = [l.replace('\\\\\"', '\"').replace(chr(92)+chr(92), chr(92)) for l in c['source']]
json.dump(nb, open('code_demo.ipynb','w'), indent=1)
"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
print(''.join(nb['cells'][2]['source']))
" 
```

### [130] TOOL RESULT — Bash · 2026-08-10 06:19:09 UTC

```
{"stdout": "from __future__ import annotations\n\nimport json\nimport math\nimport sys\nimport time\nfrom collections import defaultdict\nfrom dataclasses import dataclass, field\nfrom pathlib import Path\n\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom loguru import logger\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [131] TOOL CALL — Bash · 2026-08-10 06:19:15 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json, ast
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        src=''.join(c['source'])
        try:
            ast.parse(src)
        except SyntaxError as e:
            print('CELL', i, 'ERROR', e)
"
```

### [132] TOOL RESULT — Bash · 2026-08-10 06:19:15 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [133] ASSISTANT · 2026-08-10 06:19:19 UTC

```
All cells parse cleanly now. Let's re-run the notebook test.
```

### [134] TOOL CALL — Bash · 2026-08-10 06:19:19 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbconvert3.log 2>&1 &
echo $! > nbconvert3.pid
sleep 2; cat nbconvert3.pid
```

### [135] TOOL RESULT — Bash · 2026-08-10 06:19:19 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bx5yd6b95", "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [136] TOOL CALL — Monitor · 2026-08-10 06:19:23 UTC

```
{'command': 'cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI\nPID=$(cat nbconvert3.pid)\nwhile kill -0 $PID 2>/dev/null; do sleep 5; done\necho "NBCONVERT3_DONE"\ntail -80 nbconvert3.log', 'description': 'wait for third notebook execution attempt to finish', 'timeout_ms': 650000, 'persistent': False}
```

### [137] TOOL RESULT — Monitor · 2026-08-10 06:19:23 UTC

```
{"taskId": "by8a800wf", "timeoutMs": 650000, "persistent": false}
```

### [138] TOOL CALL — TaskOutput · 2026-08-10 06:20:13 UTC

```
{'task_id': 'by8a800wf', 'block': 'true', 'timeout': 600000}
```

### [139] TOOL RESULT — TaskOutput · 2026-08-10 06:20:13 UTC

```
{"retrieval_status": "success", "task": {"task_id": "by8a800wf", "task_type": "local_bash", "status": "completed", "description": "wait for third notebook execution attempt to finish", "output": "NBCONVERT3_DONE\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 183322 bytes to code_demo.ipynb\n", "exitCode": 0}}
```

### [140] ASSISTANT · 2026-08-10 06:20:17 UTC

```
The notebook executed successfully. Let's verify outputs, especially the final results cell.
```

### [141] TOOL CALL — Bash · 2026-08-10 06:20:17 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        errs=[o for o in c.get('outputs',[]) if o.get('output_type')=='error']
        if errs:
            print('CELL',i,'ERROR:', errs[0]['ename'], errs[0]['evalue'])
print('total cells', len(nb['cells']))
print('---last code cell outputs (text) ---')
for o in nb['cells'][-1]['outputs']:
    if o.get('output_type')=='stream':
        print(''.join(o['text'])[:2000])
"
```

### [142] TOOL RESULT — Bash · 2026-08-10 06:20:17 UTC

```
{"stdout": "total cells 22\n---last code cell outputs (text) ---\nregime            policy_family     n_pts   n_dominated   frac_non_dominated  \nlow_volatility    aimd              4       4             0.0                 \nmedium_volatility aimd              4       2             0.5                 \nhigh_volatility   aimd              4       0             1.0                 \n\nDemo-scale verdict: MIXED | criteria: a(frontier)= True  b(low-repeat)= False\nFull-scale reference verdict (mini_demo_data.json): MIXED | criteria: {'criterion_a_frontier_non_dominated': 'True', 'criterion_b_low_repeat_convergence_and_freshcache_failure': False}\n\nLow-repeat mini-check: {'freshcache_lambda_final': 0.1, 'freshcache_lambda_prior': 0.1, 'freshcache_calibrated': False, 'aimd_window_final': 2.0, 'aimd_window_init': 1.0, 'aimd_window_moved': True}\nBoundary sanity checks: {'aimd_window_grows_on_valid_hits': True, 'aimd_window_collapses_on_stale_hit': True, 'aimd_window_recovers_after_collapse': True, 'dttl_stuck_at_floor_from_low_init': True, 'dttl_well_behaved_from_high_init': True, 'ewma_recovers_from_low_init_where_dttl_gets_stuck': True}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [143] ASSISTANT · 2026-08-10 06:20:23 UTC

```
No errors, and the demo-scale run reproduces the same MIXED verdict as the full-scale reference. Clean up the test venv and verify final deliverables.
```

### [144] TOOL CALL — Bash · 2026-08-10 06:20:23 UTC

```
cd /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI
rm -rf .nb_env nbconvert*.log nbconvert*.pid
grep -c "GITHUB_DATA_URL" code_demo.ipynb
grep -o "https://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json" code_demo.ipynb | head -1
ls -la mini_demo_data.json code_demo.ipynb
```

### [145] TOOL RESULT — Bash · 2026-08-10 06:20:55 UTC

```
{"stdout": "2\nhttps://raw.githubusercontent.com/AMGrobelnik/ai-invention-a08cec-does-tcp-style-reactive-caching-actually/main/round-1/experiment-1/demo/mini_demo_data.json\n-rw-r--r-- 1 root root 183358 Aug 10 06:20 code_demo.ipynb\n-rw-r--r-- 1 root root  21381 Aug 10 06:05 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [146] ASSISTANT · 2026-08-10 06:20:58 UTC

```
All verified. Now write the structured output JSON.
```

### [147] TOOL CALL — Write · 2026-08-10 06:20:58 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.terminal_claude_agent_struct_out.json

{
  "out_expected_files": {
    "notebook": "code_demo.ipynb",
    "mini_data_file": "mini_demo_data.json"
  }
}
```

### [148] TOOL RESULT — Write · 2026-08-10 06:20:58 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/4_gen_paper_repo/_3_gen_demo_art/notebook_workspaces/iter_1/art_qtEtMpLZuRGI/.terminal_claude_agent_struct_out.json", "content": "{\n  \"out_expected_files\": {\n    \"notebook\": \"code_demo.ipynb\",\n    \"mini_data_file\": \"mini_demo_data.json\"\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [149] ASSISTANT · 2026-08-10 06:21:02 UTC

```
The demo notebook is complete and verified:

- **`code_demo.ipynb`** — reproduces the AIMD vs. TTL/d-TTL/FreshCache cache-policy simulation from `method.py`, split into markdown-annotated cells (title, install, imports, data loading, config, Stage 0/1 simulator, Stage 2 policies, Stage 3 replay driver, Stage 4/5 frontier analysis, boundary sanity checks, main run, results). Runs at a shrunk scale (20 resources, 6 episodes/regime, 60 calls/episode, smaller knob grids vs. the original 60/40/150) and reproduces the same **MIXED** verdict as the full-scale run. Test-executed end-to-end in a clean Colab-mirroring venv with no errors.
- **`mini_demo_data.json`** — curated summary (verdict, dominance/convergence summaries, frontiers, boundary checks) from the full-scale run, loaded via the GitHub-URL-with-local-fallback pattern and used to compare the notebook's demo-scale results against the full-scale reference.

Struct output written to `.terminal_claude_agent_struct_out.json`.
```
