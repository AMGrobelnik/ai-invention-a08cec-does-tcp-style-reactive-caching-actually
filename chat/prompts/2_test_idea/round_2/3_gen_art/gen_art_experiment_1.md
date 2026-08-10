# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-10 02:57:43 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

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
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx1
type: experiment
title: Real-Corpus Replay Fix for Cache Policy Comparison
summary: >-
  Re-run the five-policy cache-replay comparison (fixed TTL, literal d-TTL, EWMA-adaptive, FreshCache raw+pooled, AIMD) against
  the real-content-grounded versioned corpus (art_T0onLH9xokqw, 5,307 rows) instead of the synthetic fallback that was silently
  used last iteration. Fix the artifact-wiring bug with a loud fail-fast dependency load, keep the synthetic Zipf simulator
  as an explicit side-by-side secondary run (not a fallback), widen the AIMD (a,b) sweep to give n>=20 replicates per (regime,policy,knob)
  cell for the low-repeat convergence comparison, add a spot-check-rate ablation (10%/20%/40%), and emit method_out.json in
  the exact per-call event-log schema the (already-implemented) evaluation artifact requires so no further schema fixes are
  needed downstream.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  ```
  # method.py

  import json, os, sys, random, hashlib
  from pathlib import Path
  from dataclasses import dataclass, asdict, field

  # ---------- 0. LOUD dependency load (fixes the iter-1 wiring bug) ----------
  DEP_PATH = os.environ.get('DEP_ART_T0onLH9xokqw_FULL_DATA') or find_in_out_dependency_files('art_T0onLH9xokqw', 'full_data_out.json')
  assert DEP_PATH is not None, 'HARD FAIL: art_T0onLH9xokqw full_data_out.json path not supplied in out_dependency_files -- do NOT fall back to synthetic silently'
  assert Path(DEP_PATH).exists(), f'HARD FAIL: dependency file does not exist at {DEP_PATH}'
  raw = json.loads(Path(DEP_PATH).read_text())
  assert isinstance(raw, dict) and 'examples' in raw or isinstance(raw, list), f'HARD FAIL: unexpected schema shape in {DEP_PATH}: top-level keys={list(raw)[:10] if isinstance(raw,dict) else type(raw)}'
  rows = raw['examples'] if isinstance(raw, dict) and 'examples' in raw else raw
  assert len(rows) >= 5000, f'HARD FAIL: expected ~5307 rows, got {len(rows)} -- dependency file looks truncated/wrong'
  log.info(f'Loaded {len(rows)} real-content rows from {DEP_PATH}')

  # ---------- 1. Parse rows into per-resource version schedules + call stream ----------
  # Each row: input=JSON{episode_id, call_index, timestamp_tick, call_site_signature, resource_id}
  #           output=ground_truth_version_id
  #           metadata_resource_class, metadata_volatility_regime (static/periodic/bursty),
  #           metadata_timing_provenance, metadata_content_now, metadata_version_schedule (JSON str),
  #           metadata_checked (bool, 15% spot-check flag from dataset -- IGNORE this fixed value,
  #           re-derive spot-check flags ourselves per spot_check_rate ablation value instead, see step 4)

  episodes = defaultdict(list)  # episode_id -> list of calls sorted by timestamp_tick
  resource_schedules = {}       # resource_id -> parsed version_schedule list
  for r in rows:
      inp = json.loads(r['input'])
      sched = json.loads(r['metadata_version_schedule'])
      resource_schedules[inp['resource_id']] = sched
      episodes[inp['episode_id']].append({
          'call_index': inp['call_index'],
          'timestamp_tick': inp['timestamp_tick'],
          'call_site_signature': inp['call_site_signature'],
          'resource_id': inp['resource_id'],
          'ground_truth_version_id': r['output'],
          'volatility_regime': r['metadata_volatility_regime'],
          'resource_class': r['metadata_resource_class'],
      })
  for ep in episodes: episodes[ep].sort(key=lambda c: c['timestamp_tick'])
  assert set of volatility_regime values == {'static','periodic','bursty'}, log distribution counts

  # ---------- 2. Cache policy implementations (identical interface, stateful per call_site) ----------
  class PolicyBase:
      def decide(self, call, now_tick) -> ('serve_cache'|'refresh'), cached_version_id_or_None
      def update(self, call, served_from_cache, ground_truth_stale, spot_checked)

  class FixedTTL(PolicyBase):      # knob: ttl_ticks in {1,3,7,14,30}
  class DTTL(PolicyBase):          # literal reimplementation of Basu et al. stochastic-approximation
                                     # TTL-toward-target-hit-rate; knob: target_hit_rate in {0.5,0.7,0.9}
                                     # Robbins-Monro step: ttl += eta*(hit_observed - target_hit_rate)/k
  class EWMAAdaptive(PolicyBase):  # corrected baseline from iter1: EWMA of confirmed-stale rate
                                     # drives ttl up/down; knob: ewma_alpha in {0.1,0.3,0.5}
  class FreshCacheGate(PolicyBase):# fits exponential-decay + logistic staleness-prob per call_site
                                     # from accumulated spot-check labels; gates reuse vs error_budget
                                     # in {0.10,0.20,0.35}; report BOTH raw per-site fit ("raw") and
                                     # a resource_class-pooled fit ("pooled") sharing data across sites
                                     # of the same class to fix small-sample calibration
  class AIMD(PolicyBase):          # window w_i per call_site_id, w_i += a on confirmed/presumed-valid
                                     # hit, w_i *= b on confirmed-stale hit, floor=1 tick, ceil=60 ticks
                                     # knobs: a in {0.1, 0.25, 0.5} x b in {0.5, 0.7, 0.9}  (9 combos,
                                     # widened from iter1's single a=0.25)

  # ---------- 3. Replay engine (shared across real-corpus and synthetic runs) ----------
  def replay(episodes, resource_schedules, policy_factory, knob, spot_check_rate, seed):
      rng = random.Random(seed)
      policy = policy_factory(knob)
      event_log = []
      for episode_id, calls in episodes.items():
          for call in calls:
              decision, cached_version = policy.decide(call, call['timestamp_tick'])
              served_from_cache = (decision == 'serve_cache')
              spot_checked = rng.random() < spot_check_rate
              true_version = call['ground_truth_version_id']
              ground_truth_stale = served_from_cache and (cached_version != true_version)
              # feedback only observed if spot_checked OR policy always re-queries on 'refresh'
              observed_stale = ground_truth_stale if (spot_checked or not served_from_cache) else None
              policy.update(call, served_from_cache, observed_stale, spot_checked)
              event_log.append({
                  'episode_id': episode_id, 'seed': seed,
                  'volatility_regime': call['volatility_regime'],
                  'call_site_id': call['call_site_signature'],
                  'timestamp_tick': call['timestamp_tick'], 'step_index': call['call_index'],
                  'policy_name': policy.name, 'knob_value': knob,
                  'served_from_cache': served_from_cache, 'spot_checked': spot_checked,
                  'ground_truth_stale': ground_truth_stale,
                  'adapted_window_or_ttl': policy.current_param(call['call_site_signature']),
                  'adapted_hazard': policy.current_hazard(call['call_site_signature']) if hasattr(policy,'current_hazard') else None,
              })
      return event_log

  # ---------- 4. Experiment grid ----------
  POLICIES = {
    'fixed_ttl': (FixedTTL, [1,3,7,14,30]),
    'd_ttl': (DTTL, [0.5,0.7,0.9]),
    'ewma_adaptive': (EWMAAdaptive, [0.1,0.3,0.5]),
    'freshcache_raw': (FreshCacheGate_raw, [0.10,0.20,0.35]),
    'freshcache_pooled': (FreshCacheGate_pooled, [0.10,0.20,0.35]),
    'aimd': (AIMD, [(a,b) for a in [0.1,0.25,0.5] for b in [0.5,0.7,0.9]]),
  }
  SPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # ablation; 0.20 is the headline/documented rate matching the paper
  N_REPLICATES = 20   # up from iter1's 4-15, seeded 0..19 (bootstrapping episode order / rng draws)

  all_events = []
  for data_source in ['real_corpus', 'synthetic_zipf']:   # BOTH run and reported, not fallback
      eps, scheds = (episodes, resource_schedules) if data_source == 'real_corpus' else build_synthetic_zipf_episodes()
      for policy_key, (factory, knobs) in POLICIES.items():
          for knob in knobs:
              for spot_rate in SPOT_CHECK_RATES:
                  if spot_rate != 0.20 and policy_key != 'aimd':
                      continue   # ablation only needs to be swept for AIMD + the headline rate for others,
                                 # to keep grid size bounded; log this scoping decision explicitly
                  for seed in range(N_REPLICATES):
                      ev = replay(eps, scheds, factory, knob, spot_rate, seed)
                      for e in ev: e['data_source'] = data_source; e['spot_check_rate'] = spot_rate
                      all_events.extend(ev)

  # ---------- 5. Write method_out.json in eval.py's exact required schema ----------
  # Required columns per artifact_direction: episode_id, seed, volatility_regime, call_site_id,
  # timestamp/step_index, policy_name, knob_value, served_from_cache, spot_checked,
  # ground_truth_stale, plus per-update adapted-value fields (window/ttl/hazard trajectories).
  # knob_value must be JSON-serializable (tuple->list for AIMD's (a,b)).
  write_json('method_out.json', {
    'event_log': all_events,
    'grid_summary': {policy: knobs for policy,(_,knobs) in POLICIES.items()},
    'n_replicates': N_REPLICATES, 'spot_check_rates_tested': SPOT_CHECK_RATES,
    'headline_spot_check_rate': 0.20,
    'data_sources': ['real_corpus','synthetic_zipf'],
    'dependency_verified': {'path': DEP_PATH, 'n_rows_loaded': len(rows)},
  })
  # then run aii-json skill validation against exp_sel schema expected by eval.py BEFORE finishing
  ```
fallback_plan: >-
  1) If art_T0onLH9xokqw's out_dependency_files path is genuinely absent from the runtime environment (not just missing from
  a wrong lookup key), do NOT silently fall back to synthetic-only as iter1 did -- instead print every environment variable
  and out_dependency_files-related path candidate, try the workspace_path 'full_data_out.json' directly as a last resort (workspace_path
  is given in the dependency block above), and only if that also fails, hard-abort with a clear error message identifying
  this as a genuine infra bug to report, rather than quietly producing another synthetic-only result. 2) If parsing the real
  corpus's metadata_version_schedule JSON strings fails for a nontrivial fraction of rows (>1%), log the exact malformed examples
  and fall back to treating just those resources as 'always-valid single-version' rather than dropping the whole run. 3) If
  the full n>=20 replicate x widened-AIMD-grid x 2-data-source runtime exceeds the compute budget, first drop spot_check_rate
  ablation for non-AIMD policies (already scoped that way in the pseudocode), then reduce replicates to n=12 (still well above
  iter1's 4-15) before reducing the AIMD (a,b) grid, since convergence-event sample size is the specific weakness flagged
  for fixing. 4) If FreshCache's per-call-site raw fit cannot converge on genuinely low-repeat real-corpus call sites (too
  few observations, matching the finding that motivated the pooled variant), keep both raw and pooled results and let the
  evaluation artifact's Wilson-interval sample-floor check classify them, exactly as iter1 already does -- do not hide this
  by only reporting pooled. 5) If runtime is CPU-light-insufficient (event log construction is pure Python dict/list manipulation
  over ~5,307 rows x up to 2 sources x ~30 knobs x 20 replicates, which is at most a few million lightweight iterations --
  should comfortably fit in minutes on cpu_light; if profiling shows otherwise, vectorize the replay loop with numpy/pandas
  grouped-by-call_site_id operations instead of pure Python objects).
testing_plan: >-
  1) Schema smoke test first: load only mini_data_out.json (the small preview variant of art_T0onLH9xokqw) or the first 200
  rows of full_data_out.json, run ONE policy (fixed_ttl) at ONE knob with N_REPLICATES=1, and assert the resulting event_log
  entries contain every required column (episode_id, seed, volatility_regime, call_site_id, timestamp_tick/step_index, policy_name,
  knob_value, served_from_cache, spot_checked, ground_truth_stale, adapted_window_or_ttl) with correct types before scaling
  up -- this directly targets the schema-mismatch bug that caused eval.py to BLOCK on iter1's output. 2) Dependency-load assertion
  test: deliberately verify the assertions fire correctly by checking DEP_PATH resolves to a real, existing file with >=5000
  rows and log the first 3 parsed rows to confirm resource_id/version_schedule/ground_truth_version_id fields look sane (e.g.
  a Wikipedia-content resource_id maps to a version_schedule with exactly 1 entry when timing_provenance='real_single_snapshot',
  matching the dataset's documented design). 3) Sanity-check volatility regime distribution: confirm all three regimes (static/periodic/bursty)
  appear in the loaded real-corpus episodes with roughly the proportions implied by the dataset description (180 documents=static-ish,
  120 search_snippets=static-ish, 50 computed_values split across periodic/bursty via OWID series) -- if one regime is empty,
  that's a parsing bug, not a data limitation, since the dependency artifact guarantees all three exist. 4) Run the full AIMD
  grid (9 knob combos) at N_REPLICATES=2 first and manually inspect 2-3 per-site window trajectories to confirm additive-increase/multiplicative-decrease
  behavior is visible and floor/ceiling bounds are respected, before committing to the full N_REPLICATES=20 run. 5) Cross-check
  the synthetic Zipf path still reproduces iter1's headline numbers (Pareto frontier ordering, AIMD median convergence 14-15.5
  events) at matching knob values, as a regression test that the shared replay engine refactor didn't silently change synthetic-path
  behavior while fixing the real-corpus path. 6) Before declaring done, run the actual downstream eval.py (or its schema validator)
  against a small slice of method_out.json to confirm it no longer reports BLOCKED_NO_DATA / schema mismatch -- this is the
  single most important acceptance test since it was the iter1 failure this plan exists to fix. 7) Only after all of the above
  pass, launch the full grid (2 data sources x ~30 total knob settings x up to 3 spot-check rates for AIMD x 20 replicates)
  and monitor wall-clock via PID-based checks per the process-isolation rules.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_T0onLH9xokqw
type: dataset
title: Versioned Resource Corpus for Agent Cache Testing
summary: >-
  This artifact (full_data_out.json, 6.3MB, 5307 examples, schema exp_sel_data_out.json, single dataset group 'cache_corpus')
  is a versioned-resource tool-call log for offline evaluation of agent-side caching policies. It is built entirely from real
  seed content: 180 'document' resources are distinct Wikipedia passages (SQuAD 'context' field, 200-400 words each); 120
  'search_snippet' resources are Quora Question Pairs duplicate-question groups, where the near-duplicate query variant used
  for search-then-refine repetition is QQP's own genuine is_duplicate=1 label (not a hand-written or code-generated paraphrase);
  50 'computed_value' resources are real Our World in Data indicator series (population per country, coal-energy TWh per country
  -- both real annual cadence, remapped onto a 30-day simulated timeline -- and COVID daily new_cases per country for 5 countries,
  which use their real day-for-tick cadence directly, giving a genuinely bursty/irregular volatility regime with no injected
  timing). Every resource carries an explicit version_schedule (list of {version_id, content_hash, valid_from_tick, valid_until_tick})
  and a timing_provenance field marking whether its update timing is 'real_single_snapshot' (static, SQuAD/QQP content that
  only exists at one real snapshot -- no fabricated edits were backfilled), or 'real_owid_cadence_remapped_to_window' / 'real_owid_daily_cadence'
  (empirically grounded real update cadence). The corpus is flattened into 5307 per-tool-call log rows across 30 episodes,
  generated by three documented, deterministic repetition templates: read-then-reread (10-16 documents per episode, each revisited
  4-10 times with gaps drawn from {1,3,7,14} simulated days), search-then-refine (8-14 snippet groups per episode, 3-6 near-duplicate
  query calls each, alternating the canonical QQP question and its real duplicate), and compute-then-reuse (6-10 computed-value
  resources per episode, each reused 3-6 times). Each example's 'input' field is a JSON string {episode_id, call_index, timestamp_tick,
  call_site_signature, resource_id}; the 'output' field is the ground_truth_version_id valid at that call's timestamp; metadata_*
  fields carry resource_class, volatility_regime (static/periodic/bursty), timing_provenance, the real content valid at that
  call time (metadata_content_now, truncated to 600 chars), the resource's full version_schedule as a JSON string (so downstream
  experiment code can score any cache policy's staleness/validity for any timestamp with zero live re-querying), and a metadata_checked
  boolean (15% random spot-check subsample flag) for simulating partial verification feedback. Median call-site (resource_id)
  recurrence is well above the target of 4, giving AIMD/TTL-style cache policies room to adapt. Two candidate snippet sources
  were built and compared (MS MARCO passages with code-derived paraphrases vs. QQP's dataset-native near-duplicate query pairs);
  QQP was selected because it satisfies the artifact plan's explicit preference for dataset-provided near-duplicate queries
  over invented paraphrases. All source datasets (SQuAD: rajpurkar/squad on HuggingFace, 208k downloads; Quora Question Pairs:
  canonical 2017 Quora release mirrored as AlekseyKorshuk/quora-question-pairs; OWID population/energy_mix/covid tables from
  the official Our World in Data catalog) are well-documented, widely used benchmarks verified via web search before use.
  Downstream EXPERIMENT code can replay the call stream in timestamp order against any cache policy (LRU, TTL, AIMD, etc.),
  score redundant-call reduction (via call_site_signature/resource_id repetition) and stale-serve rate (via ground_truth_version_id
  vs. the version a policy would have served) purely from this file, with no live re-querying of any source ever required.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [2] HUMAN-USER prompt · 2026-08-10 02:57:43 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [3] SKILL-INPUT — aii-python · 2026-08-10 02:57:47 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-08-10 02:57:47 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-08-10 03:00:25 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SYSTEM-USER prompt · 2026-08-10 03:01:05 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx1
type: experiment
title: Real-Corpus Replay Fix for Cache Policy Comparison
summary: >-
  Re-run the five-policy cache-replay comparison (fixed TTL, literal d-TTL, EWMA-adaptive, FreshCache raw+pooled, AIMD) against
  the real-content-grounded versioned corpus (art_T0onLH9xokqw, 5,307 rows) instead of the synthetic fallback that was silently
  used last iteration. Fix the artifact-wiring bug with a loud fail-fast dependency load, keep the synthetic Zipf simulator
  as an explicit side-by-side secondary run (not a fallback), widen the AIMD (a,b) sweep to give n>=20 replicates per (regime,policy,knob)
  cell for the low-repeat convergence comparison, add a spot-check-rate ablation (10%/20%/40%), and emit method_out.json in
  the exact per-call event-log schema the (already-implemented) evaluation artifact requires so no further schema fixes are
  needed downstream.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  ```
  # method.py

  import json, os, sys, random, hashlib
  from pathlib import Path
  from dataclasses import dataclass, asdict, field

  # ---------- 0. LOUD dependency load (fixes the iter-1 wiring bug) ----------
  DEP_PATH = os.environ.get('DEP_ART_T0onLH9xokqw_FULL_DATA') or find_in_out_dependency_files('art_T0onLH9xokqw', 'full_data_out.json')
  assert DEP_PATH is not None, 'HARD FAIL: art_T0onLH9xokqw full_data_out.json path not supplied in out_dependency_files -- do NOT fall back to synthetic silently'
  assert Path(DEP_PATH).exists(), f'HARD FAIL: dependency file does not exist at {DEP_PATH}'
  raw = json.loads(Path(DEP_PATH).read_text())
  assert isinstance(raw, dict) and 'examples' in raw or isinstance(raw, list), f'HARD FAIL: unexpected schema shape in {DEP_PATH}: top-level keys={list(raw)[:10] if isinstance(raw,dict) else type(raw)}'
  rows = raw['examples'] if isinstance(raw, dict) and 'examples' in raw else raw
  assert len(rows) >= 5000, f'HARD FAIL: expected ~5307 rows, got {len(rows)} -- dependency file looks truncated/wrong'
  log.info(f'Loaded {len(rows)} real-content rows from {DEP_PATH}')

  # ---------- 1. Parse rows into per-resource version schedules + call stream ----------
  # Each row: input=JSON{episode_id, call_index, timestamp_tick, call_site_signature, resource_id}
  #           output=ground_truth_version_id
  #           metadata_resource_class, metadata_volatility_regime (static/periodic/bursty),
  #           metadata_timing_provenance, metadata_content_now, metadata_version_schedule (JSON str),
  #           metadata_checked (bool, 15% spot-check flag from dataset -- IGNORE this fixed value,
  #           re-derive spot-check flags ourselves per spot_check_rate ablation value instead, see step 4)

  episodes = defaultdict(list)  # episode_id -> list of calls sorted by timestamp_tick
  resource_schedules = {}       # resource_id -> parsed version_schedule list
  for r in rows:
      inp = json.loads(r['input'])
      sched = json.loads(r['metadata_version_schedule'])
      resource_schedules[inp['resource_id']] = sched
      episodes[inp['episode_id']].append({
          'call_index': inp['call_index'],
          'timestamp_tick': inp['timestamp_tick'],
          'call_site_signature': inp['call_site_signature'],
          'resource_id': inp['resource_id'],
          'ground_truth_version_id': r['output'],
          'volatility_regime': r['metadata_volatility_regime'],
          'resource_class': r['metadata_resource_class'],
      })
  for ep in episodes: episodes[ep].sort(key=lambda c: c['timestamp_tick'])
  assert set of volatility_regime values == {'static','periodic','bursty'}, log distribution counts

  # ---------- 2. Cache policy implementations (identical interface, stateful per call_site) ----------
  class PolicyBase:
      def decide(self, call, now_tick) -> ('serve_cache'|'refresh'), cached_version_id_or_None
      def update(self, call, served_from_cache, ground_truth_stale, spot_checked)

  class FixedTTL(PolicyBase):      # knob: ttl_ticks in {1,3,7,14,30}
  class DTTL(PolicyBase):          # literal reimplementation of Basu et al. stochastic-approximation
                                     # TTL-toward-target-hit-rate; knob: target_hit_rate in {0.5,0.7,0.9}
                                     # Robbins-Monro step: ttl += eta*(hit_observed - target_hit_rate)/k
  class EWMAAdaptive(PolicyBase):  # corrected baseline from iter1: EWMA of confirmed-stale rate
                                     # drives ttl up/down; knob: ewma_alpha in {0.1,0.3,0.5}
  class FreshCacheGate(PolicyBase):# fits exponential-decay + logistic staleness-prob per call_site
                                     # from accumulated spot-check labels; gates reuse vs error_budget
                                     # in {0.10,0.20,0.35}; report BOTH raw per-site fit ("raw") and
                                     # a resource_class-pooled fit ("pooled") sharing data across sites
                                     # of the same class to fix small-sample calibration
  class AIMD(PolicyBase):          # window w_i per call_site_id, w_i += a on confirmed/presumed-valid
                                     # hit, w_i *= b on confirmed-stale hit, floor=1 tick, ceil=60 ticks
                                     # knobs: a in {0.1, 0.25, 0.5} x b in {0.5, 0.7, 0.9}  (9 combos,
                                     # widened from iter1's single a=0.25)

  # ---------- 3. Replay engine (shared across real-corpus and synthetic runs) ----------
  def replay(episodes, resource_schedules, policy_factory, knob, spot_check_rate, seed):
      rng = random.Random(seed)
      policy = policy_factory(knob)
      event_log = []
      for episode_id, calls in episodes.items():
          for call in calls:
              decision, cached_version = policy.decide(call, call['timestamp_tick'])
              served_from_cache = (decision == 'serve_cache')
              spot_checked = rng.random() < spot_check_rate
              true_version = call['ground_truth_version_id']
              ground_truth_stale = served_from_cache and (cached_version != true_version)
              # feedback only observed if spot_checked OR policy always re-queries on 'refresh'
              observed_stale = ground_truth_stale if (spot_checked or not served_from_cache) else None
              policy.update(call, served_from_cache, observed_stale, spot_checked)
              event_log.append({
                  'episode_id': episode_id, 'seed': seed,
                  'volatility_regime': call['volatility_regime'],
                  'call_site_id': call['call_site_signature'],
                  'timestamp_tick': call['timestamp_tick'], 'step_index': call['call_index'],
                  'policy_name': policy.name, 'knob_value': knob,
                  'served_from_cache': served_from_cache, 'spot_checked': spot_checked,
                  'ground_truth_stale': ground_truth_stale,
                  'adapted_window_or_ttl': policy.current_param(call['call_site_signature']),
                  'adapted_hazard': policy.current_hazard(call['call_site_signature']) if hasattr(policy,'current_hazard') else None,
              })
      return event_log

  # ---------- 4. Experiment grid ----------
  POLICIES = {
    'fixed_ttl': (FixedTTL, [1,3,7,14,30]),
    'd_ttl': (DTTL, [0.5,0.7,0.9]),
    'ewma_adaptive': (EWMAAdaptive, [0.1,0.3,0.5]),
    'freshcache_raw': (FreshCacheGate_raw, [0.10,0.20,0.35]),
    'freshcache_pooled': (FreshCacheGate_pooled, [0.10,0.20,0.35]),
    'aimd': (AIMD, [(a,b) for a in [0.1,0.25,0.5] for b in [0.5,0.7,0.9]]),
  }
  SPOT_CHECK_RATES = [0.10, 0.20, 0.40]   # ablation; 0.20 is the headline/documented rate matching the paper
  N_REPLICATES = 20   # up from iter1's 4-15, seeded 0..19 (bootstrapping episode order / rng draws)

  all_events = []
  for data_source in ['real_corpus', 'synthetic_zipf']:   # BOTH run and reported, not fallback
      eps, scheds = (episodes, resource_schedules) if data_source == 'real_corpus' else build_synthetic_zipf_episodes()
      for policy_key, (factory, knobs) in POLICIES.items():
          for knob in knobs:
              for spot_rate in SPOT_CHECK_RATES:
                  if spot_rate != 0.20 and policy_key != 'aimd':
                      continue   # ablation only needs to be swept for AIMD + the headline rate for others,
                                 # to keep grid size bounded; log this scoping decision explicitly
                  for seed in range(N_REPLICATES):
                      ev = replay(eps, scheds, factory, knob, spot_rate, seed)
                      for e in ev: e['data_source'] = data_source; e['spot_check_rate'] = spot_rate
                      all_events.extend(ev)

  # ---------- 5. Write method_out.json in eval.py's exact required schema ----------
  # Required columns per artifact_direction: episode_id, seed, volatility_regime, call_site_id,
  # timestamp/step_index, policy_name, knob_value, served_from_cache, spot_checked,
  # ground_truth_stale, plus per-update adapted-value fields (window/ttl/hazard trajectories).
  # knob_value must be JSON-serializable (tuple->list for AIMD's (a,b)).
  write_json('method_out.json', {
    'event_log': all_events,
    'grid_summary': {policy: knobs for policy,(_,knobs) in POLICIES.items()},
    'n_replicates': N_REPLICATES, 'spot_check_rates_tested': SPOT_CHECK_RATES,
    'headline_spot_check_rate': 0.20,
    'data_sources': ['real_corpus','synthetic_zipf'],
    'dependency_verified': {'path': DEP_PATH, 'n_rows_loaded': len(rows)},
  })
  # then run aii-json skill validation against exp_sel schema expected by eval.py BEFORE finishing
  ```
fallback_plan: >-
  1) If art_T0onLH9xokqw's out_dependency_files path is genuinely absent from the runtime environment (not just missing from
  a wrong lookup key), do NOT silently fall back to synthetic-only as iter1 did -- instead print every environment variable
  and out_dependency_files-related path candidate, try the workspace_path 'full_data_out.json' directly as a last resort (workspace_path
  is given in the dependency block above), and only if that also fails, hard-abort with a clear error message identifying
  this as a genuine infra bug to report, rather than quietly producing another synthetic-only result. 2) If parsing the real
  corpus's metadata_version_schedule JSON strings fails for a nontrivial fraction of rows (>1%), log the exact malformed examples
  and fall back to treating just those resources as 'always-valid single-version' rather than dropping the whole run. 3) If
  the full n>=20 replicate x widened-AIMD-grid x 2-data-source runtime exceeds the compute budget, first drop spot_check_rate
  ablation for non-AIMD policies (already scoped that way in the pseudocode), then reduce replicates to n=12 (still well above
  iter1's 4-15) before reducing the AIMD (a,b) grid, since convergence-event sample size is the specific weakness flagged
  for fixing. 4) If FreshCache's per-call-site raw fit cannot converge on genuinely low-repeat real-corpus call sites (too
  few observations, matching the finding that motivated the pooled variant), keep both raw and pooled results and let the
  evaluation artifact's Wilson-interval sample-floor check classify them, exactly as iter1 already does -- do not hide this
  by only reporting pooled. 5) If runtime is CPU-light-insufficient (event log construction is pure Python dict/list manipulation
  over ~5,307 rows x up to 2 sources x ~30 knobs x 20 replicates, which is at most a few million lightweight iterations --
  should comfortably fit in minutes on cpu_light; if profiling shows otherwise, vectorize the replay loop with numpy/pandas
  grouped-by-call_site_id operations instead of pure Python objects).
testing_plan: >-
  1) Schema smoke test first: load only mini_data_out.json (the small preview variant of art_T0onLH9xokqw) or the first 200
  rows of full_data_out.json, run ONE policy (fixed_ttl) at ONE knob with N_REPLICATES=1, and assert the resulting event_log
  entries contain every required column (episode_id, seed, volatility_regime, call_site_id, timestamp_tick/step_index, policy_name,
  knob_value, served_from_cache, spot_checked, ground_truth_stale, adapted_window_or_ttl) with correct types before scaling
  up -- this directly targets the schema-mismatch bug that caused eval.py to BLOCK on iter1's output. 2) Dependency-load assertion
  test: deliberately verify the assertions fire correctly by checking DEP_PATH resolves to a real, existing file with >=5000
  rows and log the first 3 parsed rows to confirm resource_id/version_schedule/ground_truth_version_id fields look sane (e.g.
  a Wikipedia-content resource_id maps to a version_schedule with exactly 1 entry when timing_provenance='real_single_snapshot',
  matching the dataset's documented design). 3) Sanity-check volatility regime distribution: confirm all three regimes (static/periodic/bursty)
  appear in the loaded real-corpus episodes with roughly the proportions implied by the dataset description (180 documents=static-ish,
  120 search_snippets=static-ish, 50 computed_values split across periodic/bursty via OWID series) -- if one regime is empty,
  that's a parsing bug, not a data limitation, since the dependency artifact guarantees all three exist. 4) Run the full AIMD
  grid (9 knob combos) at N_REPLICATES=2 first and manually inspect 2-3 per-site window trajectories to confirm additive-increase/multiplicative-decrease
  behavior is visible and floor/ceiling bounds are respected, before committing to the full N_REPLICATES=20 run. 5) Cross-check
  the synthetic Zipf path still reproduces iter1's headline numbers (Pareto frontier ordering, AIMD median convergence 14-15.5
  events) at matching knob values, as a regression test that the shared replay engine refactor didn't silently change synthetic-path
  behavior while fixing the real-corpus path. 6) Before declaring done, run the actual downstream eval.py (or its schema validator)
  against a small slice of method_out.json to confirm it no longer reports BLOCKED_NO_DATA / schema mismatch -- this is the
  single most important acceptance test since it was the iter1 failure this plan exists to fix. 7) Only after all of the above
  pass, launch the full grid (2 data sources x ~30 total knob settings x up to 3 spot-check rates for AIMD x 20 replicates)
  and monitor wall-clock via PID-based checks per the process-isolation rules.
</artifact_plan>

<dependencies>
Read the files in these dependency workspaces to understand what's available, then copy any you need into your working directory.

--- Dependency 1 ---
id: art_T0onLH9xokqw
type: dataset
title: Versioned Resource Corpus for Agent Cache Testing
summary: >-
  This artifact (full_data_out.json, 6.3MB, 5307 examples, schema exp_sel_data_out.json, single dataset group 'cache_corpus')
  is a versioned-resource tool-call log for offline evaluation of agent-side caching policies. It is built entirely from real
  seed content: 180 'document' resources are distinct Wikipedia passages (SQuAD 'context' field, 200-400 words each); 120
  'search_snippet' resources are Quora Question Pairs duplicate-question groups, where the near-duplicate query variant used
  for search-then-refine repetition is QQP's own genuine is_duplicate=1 label (not a hand-written or code-generated paraphrase);
  50 'computed_value' resources are real Our World in Data indicator series (population per country, coal-energy TWh per country
  -- both real annual cadence, remapped onto a 30-day simulated timeline -- and COVID daily new_cases per country for 5 countries,
  which use their real day-for-tick cadence directly, giving a genuinely bursty/irregular volatility regime with no injected
  timing). Every resource carries an explicit version_schedule (list of {version_id, content_hash, valid_from_tick, valid_until_tick})
  and a timing_provenance field marking whether its update timing is 'real_single_snapshot' (static, SQuAD/QQP content that
  only exists at one real snapshot -- no fabricated edits were backfilled), or 'real_owid_cadence_remapped_to_window' / 'real_owid_daily_cadence'
  (empirically grounded real update cadence). The corpus is flattened into 5307 per-tool-call log rows across 30 episodes,
  generated by three documented, deterministic repetition templates: read-then-reread (10-16 documents per episode, each revisited
  4-10 times with gaps drawn from {1,3,7,14} simulated days), search-then-refine (8-14 snippet groups per episode, 3-6 near-duplicate
  query calls each, alternating the canonical QQP question and its real duplicate), and compute-then-reuse (6-10 computed-value
  resources per episode, each reused 3-6 times). Each example's 'input' field is a JSON string {episode_id, call_index, timestamp_tick,
  call_site_signature, resource_id}; the 'output' field is the ground_truth_version_id valid at that call's timestamp; metadata_*
  fields carry resource_class, volatility_regime (static/periodic/bursty), timing_provenance, the real content valid at that
  call time (metadata_content_now, truncated to 600 chars), the resource's full version_schedule as a JSON string (so downstream
  experiment code can score any cache policy's staleness/validity for any timestamp with zero live re-querying), and a metadata_checked
  boolean (15% random spot-check subsample flag) for simulating partial verification feedback. Median call-site (resource_id)
  recurrence is well above the target of 4, giving AIMD/TTL-style cache policies room to adapt. Two candidate snippet sources
  were built and compared (MS MARCO passages with code-derived paraphrases vs. QQP's dataset-native near-duplicate query pairs);
  QQP was selected because it satisfies the artifact plan's explicit preference for dataset-provided near-duplicate queries
  over invented paraphrases. All source datasets (SQuAD: rajpurkar/squad on HuggingFace, 208k downloads; Quora Question Pairs:
  canonical 2017 Quora release mirrored as AlekseyKorshuk/quora-question-pairs; OWID population/energy_mix/covid tables from
  the official Our World in Data catalog) are well-documented, widely used benchmarks verified via web search before use.
  Downstream EXPERIMENT code can replay the call stream in timestamp order against any cache policy (LRU, TTL, AIMD, etc.),
  score redundant-call reduction (via call_site_signature/resource_id repetition) and stale-serve rate (via ground_truth_version_id
  vs. the version a policy would have served) purely from this file, with no live re-querying of any source ever required.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</dependencies>

<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Free-first web search (general + scholarly modes), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-concept-fig-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [7] SKILL-INPUT — aii-file-size-limit · 2026-08-10 03:01:17 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [8] SYSTEM-USER prompt · 2026-08-10 03:01:49 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 1/10).
</verification_failed>

<schema_errors>
JSON SCHEMA / CODE VALIDATION ERRORS:
  - full_method_out.json: No predict_* fields found in any of the sampled examples (at least one required)
  - mini_method_out.json: No predict_* fields found in any of the sampled examples (at least one required)
  - preview_method_out.json: No predict_* fields found in any of the sampled examples (at least one required)

Fix: Your JSON files must follow the datasets-grouped exp_gen_sol_out.json schema:
     {
       "datasets": [
         {
           "dataset": "dataset_name",
           "examples": [
             {
               "input": "string (required)",
               "output": "string (required)",
               "metadata_fold": 2,
               "predict_<method_name>": "string - prediction per method"
             }
           ]
         }
       ]
     }

     NO 'split', 'dataset', or 'context' per-example. Dataset name at group level.
     Metadata via flat metadata_<name> fields.
     Read exp_gen_sol_out.json schema in aii-json skill.
     Then update method.py and regenerate the output files.

     If Python syntax errors: fix the syntax in method.py
</schema_errors>

<task>
FIX THESE ISSUES:
2. Fix schema/syntax errors in method.py
3. Re-run method.py to regenerate output files
4. Validate with aii-json skill: validate method_out.json against exp_gen_sol_out schema

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```
