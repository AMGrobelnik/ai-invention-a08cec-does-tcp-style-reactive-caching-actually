# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-09 23:25:23 UTC

```
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
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
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
id: gen_plan_experiment_1_idx2
type: experiment
title: AIMD Cache Windows vs TTL Baselines for Agents
summary: >-
  Simulate an LLM agent tool-call loop with a versioned, volatility-labeled resource corpus, and implement four per-call-site
  caching policies -- fixed TTL, d-TTL-style stochastic-approximation hit-rate targeting, a FreshCache-style fitted staleness-probability
  gate, and the proposed AIMD reuse-window rule. Replay the same episode traces through all four policies across multiple
  volatility regimes and multiple knob settings each, logging every cache decision plus ground-truth validity, to produce
  (i) each policy's reduction-vs-staleness Pareto frontier and (ii) each adaptive policy's confirmed-staleness-events-to-convergence
  curve. This is pure Python/NumPy simulation logic -- no LLM calls are required for the core result, so cost is $0; OpenRouter
  is only touched optionally to diversify simulated task/query text.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ============================================================
  # STAGE 0 -- Load dependency dataset
  # ============================================================
  # This experiment REQUIRES a DATASET dependency artifact providing the
  # versioned resource corpus + episode call traces + volatility schedule.
  # Load method_out.json (or equivalent) from the DATASET artifact's output.
  # Expected fields (adapt to whatever the actual dataset artifact emits --
  # inspect its schema first and fail loudly with a clear error if a required
  # field is absent, do not silently invent data):
  #   resources: {resource_id: {schedule: 'static'|'periodic'|'bursty', ...}}
  #   episodes: [ {episode_id, calls: [ {call_site_id (fn+arg signature hash),
  #                                       timestamp, resource_id, true_value_version} ] } ]
  #   volatility_regimes: list of regime labels each episode is tagged with
  # If the dataset artifact instead only gives raw resources/tools without
  # pre-simulated call traces, this experiment must itself run the simulated
  # agent loop (Stage 1) to generate traces -- do this only if traces are
  # genuinely absent from the dependency, not as a default.

  # ============================================================
  # STAGE 1 -- Agent-loop call harness (if traces not already in dataset)
  # ============================================================
  def simulate_episode(resources, rng, n_calls, repeat_bias=0.6):
      # Simulate an agent revisiting the same handful of call sites (file
      # reads, repeated near-duplicate searches, repeated computations)
      # with realistic skew: draw call_site from a Zipf-like distribution
      # over a small per-episode working set so repeats actually occur.
      working_set = rng.choice(list(resources), size=max(5, n_calls // 4), replace=False)
      calls = []
      t = 0.0
      for _ in range(n_calls):
          if rng.random() < repeat_bias and calls:
              site = rng.choice([c['call_site_id'] for c in calls])
          else:
              site = rng.choice(working_set)
          t += rng.exponential(scale=1.0)  # inter-call time, arbitrary sim units
          true_version = resources[site].value_version_at(t)
          calls.append({'call_site_id': site, 'timestamp': t, 'true_version': true_version})
      return calls

  class Resource:
      # schedule in {'static', 'periodic', 'bursty'}
      def value_version_at(self, t):
          if self.schedule == 'static': return 0
          if self.schedule == 'periodic': return int(t // self.period)
          if self.schedule == 'bursty': return self.poisson_change_count(t)  # precompute change times, count how many precede t

  # Only invoke OpenRouter (aii-openrouter-llms skill) if task/query TEXT
  # diversity is needed for realism (e.g., generating varied search-query
  # strings for the 'repeated near-duplicate search' call type). This is
  # cosmetic content generation, NOT used for any cache-policy logic --
  # cap at a few hundred cheap calls (e.g. gpt-4o-mini or similar low-cost
  # OpenRouter model) well under $10, and skip entirely if the dataset
  # artifact already supplies call traces.

  # ============================================================
  # STAGE 2 -- Cache policy implementations (per call_site_id state)
  # ============================================================

  class FixedTTLPolicy:
      def __init__(self, ttl): self.ttl = ttl; self.cache = {}  # site -> (version, cached_at)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.ttl:
                  is_hit = True
                  # ground truth validity always computable in simulation (we know true_version)
                  valid = (version == true_version)
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True

  class DTTLPolicy:
      # Basu et al. 2017 (arXiv:1704.04448): Robbins-Monro update of TTL
      # toward a target hit rate h*. On each request at a site, whether
      # served as hit or miss, update:
      #   ttl_i <- ttl_i + gamma_k * (observed_hit_indicator - h_target)
      # with gamma_k = c / (k+1) (diminishing step size, k = update count
      # for that site) per the paper's stochastic-approximation convergence
      # argument. Clip ttl_i to [ttl_min, ttl_max].
      def __init__(self, h_target, c=1.0, ttl_min=0.01, ttl_max=1e4, ttl_init=1.0):
          self.h_target = h_target; self.c = c
          self.ttl = defaultdict(lambda: ttl_init)
          self.k = defaultdict(int)
          self.cache = {}
      def on_call(self, site, t, true_version, spot_check_fn):
          hit_indicator = 0
          valid = True
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.ttl[site]:
                  hit_indicator = 1
                  valid = (version == true_version)
          else:
              valid = True
          self.k[site] += 1
          gamma = self.c / (self.k[site] + 1)
          self.ttl[site] = clip(self.ttl[site] + gamma * (hit_indicator - self.h_target), ttl_min, ttl_max)
          if hit_indicator == 0:
              self.cache[site] = (true_version, t)
          return ('hit' if hit_indicator else 'miss'), valid

  class FreshCacheGatePolicy:
      # Fitted per-call-site staleness-probability gate, ported from
      # Mansoor/Ahmad/Yoon 2026 FreshCache's exponential-decay staleness
      # model: P(stale | age=a) = 1 - exp(-lambda_i * a). Fit lambda_i per
      # site via MLE/method-of-moments over observed (age, valid/stale)
      # spot-check pairs collected so far for that site (needs several
      # observations before it is meaningfully calibrated -- this is the
      # exact 'requires labeled calibration data' property under test).
      # Gate: serve from cache only if P(stale | age) <= error_budget.
      def __init__(self, error_budget, lambda_prior=0.1, min_obs_to_fit=5):
          self.error_budget = error_budget
          self.lambda_est = defaultdict(lambda: lambda_prior)
          self.obs = defaultdict(list)  # site -> [(age, was_stale)]
          self.cache = {}
      def predicted_stale_prob(self, site, age):
          return 1 - math.exp(-self.lambda_est[site] * age)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              age = t - cached_at
              if self.predicted_stale_prob(site, age) <= self.error_budget:
                  valid = (version == true_version)
                  if spot_check_fn(site):  # background spot-check updates the fit
                      self.obs[site].append((age, not valid))
                      self._refit(site)
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True
      def _refit(self, site):
          # MLE for exponential rate from (age, stale) pairs; refit only once
          # min_obs_to_fit observations exist, else keep the prior lambda.
          ...

  class AIMDPolicy:
      # THE PROPOSED METHOD.
      # w_i: reuse WINDOW (units = simulation time, analogous to a TTL but
      # driven by outcomes not fit). a = additive increase step,
      # b in (0,1) = multiplicative decrease factor, floor/ceiling bounds.
      def __init__(self, a, b, w_min=0.01, w_max=1e4, w_init=1.0, spot_check_rate=0.2):
          self.a = a; self.b = b; self.w_min = w_min; self.w_max = w_max
          self.w = defaultdict(lambda: w_init)
          self.cache = {}
          self.spot_check_rate = spot_check_rate
          self.confirmed_stale_count = defaultdict(int)
          self.confirmed_valid_count = defaultdict(int)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.w[site]:
                  valid = (version == true_version)
                  checked = spot_check_fn(site)  # bernoulli(spot_check_rate) in simulation
                  if checked:
                      if valid:
                          self.w[site] = min(self.w[site] + self.a, self.w_max)
                          self.confirmed_valid_count[site] += 1
                      else:
                          self.w[site] = max(self.w[site] * self.b, self.w_min)
                          self.confirmed_stale_count[site] += 1
                  # presumed-valid unchecked hits: leave window unchanged
                  # (conservative variant) -- ALSO run an ablation variant
                  # where unchecked hits get a smaller additive bump
                  # (a * presumed_valid_weight, e.g. 0.25*a) to test
                  # sensitivity to this design choice.
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True

  # ============================================================
  # STAGE 3 -- Replay driver
  # ============================================================
  POLICY_GRID = {
      'fixed_ttl':   [FixedTTLPolicy(ttl=v) for v in [0.5, 1, 2, 4, 8, 16, 32]],
      'd_ttl':       [DTTLPolicy(h_target=h, c=c) for h in [0.5,0.6,0.7,0.8,0.9] for c in [0.5,1.0,2.0]],
      'freshcache':  [FreshCacheGatePolicy(error_budget=e) for e in [0.05,0.10,0.20,0.35]],
      'aimd':        [AIMDPolicy(a=a, b=b) for a in [0.25,0.5,1.0,2.0] for b in [0.3,0.5,0.7]],
  }

  results = []
  for regime in volatility_regimes:
      for policy_family, policy_instances in POLICY_GRID.items():
          for policy in policy_instances:
              policy_state = fresh_copy(policy)  # reset per-episode-set state per (regime, knob) run
              log = []
              for episode in episodes_in_regime(regime):
                  for call in episode['calls']:
                      decision, valid = policy_state.on_call(
                          call['call_site_id'], call['timestamp'], call['true_version'],
                          spot_check_fn=make_spot_checker(rate=SPOT_CHECK_RATE, rng=rng))
                      log.append({'site': call['call_site_id'], 'decision': decision, 'valid': valid,
                                  'stale_events_so_far': cumulative_stale_count(policy_state, call['call_site_id'])})
              hit_rate = fraction(log, lambda r: r['decision']=='hit')
              stale_rate = fraction(log, lambda r: r['decision']=='hit' and not r['valid'])
              convergence_point = find_convergence_index(log, policy_family)  # see Stage 4
              results.append({'regime': regime, 'policy_family': policy_family,
                               'knob': describe_knob(policy), 'hit_rate': hit_rate,
                               'stale_rate': stale_rate, 'convergence_events': convergence_point})

  # ============================================================
  # STAGE 4 -- Convergence detection (only meaningful for adaptive policies)
  # ============================================================
  def find_convergence_index(log, policy_family):
      # For d_ttl / aimd / freshcache: track the per-site window/ttl/lambda
      # trajectory over time; define 'converged' as the first point after
      # which the value stays within +/-10% of its own trailing mean for
      # the rest of the episode set (a simple rolling-band stability test).
      # Report convergence in units of CONFIRMED-STALENESS FEEDBACK EVENTS
      # consumed up to that point (not raw calls), since that is the
      # hypothesis's actual currency. For freshcache, additionally report
      # whether min_obs_to_fit was ever reached per site (some low-repeat
      # sites may NEVER calibrate -- this is an expected, reportable failure
      # mode, not a bug).
      ...

  # ============================================================
  # STAGE 5 -- Frontier + comparison outputs
  # ============================================================
  # For each (regime, policy_family): sort knob sweep points by hit_rate,
  # take the Pareto-efficient subset (max hit_rate for given stale_rate).
  # Compute frontier dominance: for each aimd point, does some d_ttl/fixed
  # point dominate it (>= hit_rate AND <= stale_rate)? Aggregate a
  # 'fraction of aimd points non-dominated' summary per regime.
  # Compare median/IQR of convergence_events across policy families,
  # per regime, especially in a LOW-REPEAT-COUNT sub-slice of episodes
  # (call sites visited <= 5 times) -- this is the decisive regime named
  # in success_criteria.

  # ============================================================
  # STAGE 6 -- Write method_out.json
  # ============================================================
  # {
  #   'per_run_results': results,                # full grid, all regimes/knobs
  #   'frontiers': {regime: {policy_family: [(hit_rate, stale_rate), ...]}},
  #   'dominance_summary': {...},
  #   'convergence_summary': {regime: {policy_family: {median, p10, p90}}},
  #   'low_repeat_slice_summary': {...},          # the headline comparison
  #   'ablations': {'aimd_presumed_valid_weight': [...], 'spot_check_rate_sensitivity': [...]},
  #   'config': {grid definitions, rng seeds, spot_check_rate, n_episodes, ...},
  #   'verdict': 'CONFIRMS' | 'DISCONFIRMS' | 'MIXED',   # per success_criteria (a) and (b) separately
  # }
fallback_plan: >-
  1) If the dependency DATASET artifact does not already contain pre-simulated agent call traces with a controllable volatility
  schedule (only raw resources/tools), fall back to generating the traces in-house inside this experiment using Stage 1's
  pure-Python simulator (Zipf-skewed call-site revisits over a small per-episode working set, resources with static/periodic/bursty
  version-change schedules) -- this needs no LLM calls and no dataset beyond a list of resource IDs, so it degrades gracefully
  to a fully synthetic but still controllable workload. 2) If Basu et al.'s exact d-TTL update is ambiguous or its provable-convergence
  step-size schedule (gamma_k = c/(k+1)) proves numerically unstable (oscillation, divergence) on this shorter agent-episode
  traffic (their paper assumes CDN-scale request volume, orders of magnitude more requests per object than an agent call site
  gets), document the instability as a finding rather than hiding it, and additionally report a simplified fixed-step EWMA-toward-target-hit-rate
  variant as a secondary, better-behaved SOTA-adaptive baseline so the AIMD-vs-adaptive-baseline comparison is not vacated
  by one baseline collapsing. 3) If the FreshCache-style fit never reaches min_obs_to_fit for most call sites (very plausible
  given the low-repeat-count regime is the whole point), this is not a failure to fix -- it IS the expected result supporting
  the hypothesis; report the fraction of sites that never calibrate as a headline number, alongside a version of FreshCache
  with a shared cross-site prior (partial pooling of lambda across all sites of the same resource-schedule type) as a fairer
  reference so the comparison isn't a strawman. 4) If ground-truth validity is expensive/impossible to compute for some resource
  type, restrict volatility injection to schedules where ground truth is always analytically known (as in Stage 1's Resource
  classes) rather than trying to reconstruct it after the fact. 5) If the full knob grid (7 TTL x 15 d-TTL x 4 freshcache
  x 12 AIMD x N regimes) is too slow, first cut grid density (fewer knob values) before cutting episode count or regime count
  -- convergence-speed and frontier-shape claims need enough episodes per cell, not enough knob resolution. 6) If time runs
  short, prioritize completing all four policies on ONE volatility regime with a full knob sweep and convergence analysis
  before adding more regimes -- a complete single-regime comparison is a valid, reportable result; a partial multi-regime
  sweep with missing cells is not.
testing_plan: >-
  1) Unit-test each policy class in isolation on a tiny hand-constructed trace (e.g., 20 calls to 2 sites with a known version-change
  schedule) and manually verify the expected cache hit/miss/window trajectory by hand-computation before running any large
  sweep -- especially verify AIMD's window actually grows on repeated confirmed-valid hits and collapses sharply after an
  injected confirmed-stale hit, and that d-TTL's TTL moves toward target hit rate over enough iterations on a synthetic all-static
  (never-stale) resource. 2) Run one mini end-to-end pass: 1 regime, 2-3 episodes, 1 knob value per policy family, confirm
  method_out.json fields populate without errors and hit_rate/stale_rate are in [0,1] and sane (e.g., fixed TTL=0 should give
  ~0% hit rate; TTL=infinity on a fully static resource should give ~100% hit rate and 0% stale rate -- these are sanity boundary
  checks, verify them explicitly). 3) Check for a known pathology before scaling: AIMD window collapsing to w_min and never
  recovering (should recover via additive increase after enough confirmed-valid hits -- verify this happens within a bounded
  number of calls in the mini test) and d-TTL oscillating without settling (plot/print the TTL trajectory for a few sites
  in the mini run and inspect). 4) Verify the low-repeat-count slice logic on synthetic data with call sites visited exactly
  3-5 times, confirming FreshCache's fit legitimately fails to calibrate there (lambda stays at prior) while AIMD's window
  has visibly moved from its init value -- this is the core hypothesis mechanism and must be checked BEFORE trusting full-scale
  numbers. 5) Only after all mini checks pass, scale to the full regime x knob-grid x episode-count sweep, and re-run the
  same boundary sanity checks (TTL=0 and TTL=infinity behavior) on the full run as a regression check that nothing broke when
  scaling up.
</artifact_plan>



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
```

### [2] HUMAN-USER prompt · 2026-08-09 23:25:23 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [3] SKILL-INPUT — aii-python · 2026-08-09 23:25:29 UTC

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

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-08-09 23:25:29 UTC

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

### [5] SKILL-INPUT — aii-json · 2026-08-09 23:25:29 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-08-09 23:25:29 UTC

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

### [7] SKILL-INPUT — aii-use-hardware · 2026-08-09 23:25:29 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [8] SKILL-INPUT — aii-parallel-computing · 2026-08-09 23:25:29 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SYSTEM-USER prompt · 2026-08-09 23:34:42 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
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
id: gen_plan_experiment_1_idx2
type: experiment
title: AIMD Cache Windows vs TTL Baselines for Agents
summary: >-
  Simulate an LLM agent tool-call loop with a versioned, volatility-labeled resource corpus, and implement four per-call-site
  caching policies -- fixed TTL, d-TTL-style stochastic-approximation hit-rate targeting, a FreshCache-style fitted staleness-probability
  gate, and the proposed AIMD reuse-window rule. Replay the same episode traces through all four policies across multiple
  volatility regimes and multiple knob settings each, logging every cache decision plus ground-truth validity, to produce
  (i) each policy's reduction-vs-staleness Pareto frontier and (ii) each adaptive policy's confirmed-staleness-events-to-convergence
  curve. This is pure Python/NumPy simulation logic -- no LLM calls are required for the core result, so cost is $0; OpenRouter
  is only touched optionally to diversify simulated task/query text.
runpod_compute_profile: gpu
implementation_pseudocode: |-
  # ============================================================
  # STAGE 0 -- Load dependency dataset
  # ============================================================
  # This experiment REQUIRES a DATASET dependency artifact providing the
  # versioned resource corpus + episode call traces + volatility schedule.
  # Load method_out.json (or equivalent) from the DATASET artifact's output.
  # Expected fields (adapt to whatever the actual dataset artifact emits --
  # inspect its schema first and fail loudly with a clear error if a required
  # field is absent, do not silently invent data):
  #   resources: {resource_id: {schedule: 'static'|'periodic'|'bursty', ...}}
  #   episodes: [ {episode_id, calls: [ {call_site_id (fn+arg signature hash),
  #                                       timestamp, resource_id, true_value_version} ] } ]
  #   volatility_regimes: list of regime labels each episode is tagged with
  # If the dataset artifact instead only gives raw resources/tools without
  # pre-simulated call traces, this experiment must itself run the simulated
  # agent loop (Stage 1) to generate traces -- do this only if traces are
  # genuinely absent from the dependency, not as a default.

  # ============================================================
  # STAGE 1 -- Agent-loop call harness (if traces not already in dataset)
  # ============================================================
  def simulate_episode(resources, rng, n_calls, repeat_bias=0.6):
      # Simulate an agent revisiting the same handful of call sites (file
      # reads, repeated near-duplicate searches, repeated computations)
      # with realistic skew: draw call_site from a Zipf-like distribution
      # over a small per-episode working set so repeats actually occur.
      working_set = rng.choice(list(resources), size=max(5, n_calls // 4), replace=False)
      calls = []
      t = 0.0
      for _ in range(n_calls):
          if rng.random() < repeat_bias and calls:
              site = rng.choice([c['call_site_id'] for c in calls])
          else:
              site = rng.choice(working_set)
          t += rng.exponential(scale=1.0)  # inter-call time, arbitrary sim units
          true_version = resources[site].value_version_at(t)
          calls.append({'call_site_id': site, 'timestamp': t, 'true_version': true_version})
      return calls

  class Resource:
      # schedule in {'static', 'periodic', 'bursty'}
      def value_version_at(self, t):
          if self.schedule == 'static': return 0
          if self.schedule == 'periodic': return int(t // self.period)
          if self.schedule == 'bursty': return self.poisson_change_count(t)  # precompute change times, count how many precede t

  # Only invoke OpenRouter (aii-openrouter-llms skill) if task/query TEXT
  # diversity is needed for realism (e.g., generating varied search-query
  # strings for the 'repeated near-duplicate search' call type). This is
  # cosmetic content generation, NOT used for any cache-policy logic --
  # cap at a few hundred cheap calls (e.g. gpt-4o-mini or similar low-cost
  # OpenRouter model) well under $10, and skip entirely if the dataset
  # artifact already supplies call traces.

  # ============================================================
  # STAGE 2 -- Cache policy implementations (per call_site_id state)
  # ============================================================

  class FixedTTLPolicy:
      def __init__(self, ttl): self.ttl = ttl; self.cache = {}  # site -> (version, cached_at)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.ttl:
                  is_hit = True
                  # ground truth validity always computable in simulation (we know true_version)
                  valid = (version == true_version)
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True

  class DTTLPolicy:
      # Basu et al. 2017 (arXiv:1704.04448): Robbins-Monro update of TTL
      # toward a target hit rate h*. On each request at a site, whether
      # served as hit or miss, update:
      #   ttl_i <- ttl_i + gamma_k * (observed_hit_indicator - h_target)
      # with gamma_k = c / (k+1) (diminishing step size, k = update count
      # for that site) per the paper's stochastic-approximation convergence
      # argument. Clip ttl_i to [ttl_min, ttl_max].
      def __init__(self, h_target, c=1.0, ttl_min=0.01, ttl_max=1e4, ttl_init=1.0):
          self.h_target = h_target; self.c = c
          self.ttl = defaultdict(lambda: ttl_init)
          self.k = defaultdict(int)
          self.cache = {}
      def on_call(self, site, t, true_version, spot_check_fn):
          hit_indicator = 0
          valid = True
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.ttl[site]:
                  hit_indicator = 1
                  valid = (version == true_version)
          else:
              valid = True
          self.k[site] += 1
          gamma = self.c / (self.k[site] + 1)
          self.ttl[site] = clip(self.ttl[site] + gamma * (hit_indicator - self.h_target), ttl_min, ttl_max)
          if hit_indicator == 0:
              self.cache[site] = (true_version, t)
          return ('hit' if hit_indicator else 'miss'), valid

  class FreshCacheGatePolicy:
      # Fitted per-call-site staleness-probability gate, ported from
      # Mansoor/Ahmad/Yoon 2026 FreshCache's exponential-decay staleness
      # model: P(stale | age=a) = 1 - exp(-lambda_i * a). Fit lambda_i per
      # site via MLE/method-of-moments over observed (age, valid/stale)
      # spot-check pairs collected so far for that site (needs several
      # observations before it is meaningfully calibrated -- this is the
      # exact 'requires labeled calibration data' property under test).
      # Gate: serve from cache only if P(stale | age) <= error_budget.
      def __init__(self, error_budget, lambda_prior=0.1, min_obs_to_fit=5):
          self.error_budget = error_budget
          self.lambda_est = defaultdict(lambda: lambda_prior)
          self.obs = defaultdict(list)  # site -> [(age, was_stale)]
          self.cache = {}
      def predicted_stale_prob(self, site, age):
          return 1 - math.exp(-self.lambda_est[site] * age)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              age = t - cached_at
              if self.predicted_stale_prob(site, age) <= self.error_budget:
                  valid = (version == true_version)
                  if spot_check_fn(site):  # background spot-check updates the fit
                      self.obs[site].append((age, not valid))
                      self._refit(site)
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True
      def _refit(self, site):
          # MLE for exponential rate from (age, stale) pairs; refit only once
          # min_obs_to_fit observations exist, else keep the prior lambda.
          ...

  class AIMDPolicy:
      # THE PROPOSED METHOD.
      # w_i: reuse WINDOW (units = simulation time, analogous to a TTL but
      # driven by outcomes not fit). a = additive increase step,
      # b in (0,1) = multiplicative decrease factor, floor/ceiling bounds.
      def __init__(self, a, b, w_min=0.01, w_max=1e4, w_init=1.0, spot_check_rate=0.2):
          self.a = a; self.b = b; self.w_min = w_min; self.w_max = w_max
          self.w = defaultdict(lambda: w_init)
          self.cache = {}
          self.spot_check_rate = spot_check_rate
          self.confirmed_stale_count = defaultdict(int)
          self.confirmed_valid_count = defaultdict(int)
      def on_call(self, site, t, true_version, spot_check_fn):
          if site in self.cache:
              version, cached_at = self.cache[site]
              if t - cached_at <= self.w[site]:
                  valid = (version == true_version)
                  checked = spot_check_fn(site)  # bernoulli(spot_check_rate) in simulation
                  if checked:
                      if valid:
                          self.w[site] = min(self.w[site] + self.a, self.w_max)
                          self.confirmed_valid_count[site] += 1
                      else:
                          self.w[site] = max(self.w[site] * self.b, self.w_min)
                          self.confirmed_stale_count[site] += 1
                  # presumed-valid unchecked hits: leave window unchanged
                  # (conservative variant) -- ALSO run an ablation variant
                  # where unchecked hits get a smaller additive bump
                  # (a * presumed_valid_weight, e.g. 0.25*a) to test
                  # sensitivity to this design choice.
                  return 'hit', valid
          self.cache[site] = (true_version, t)
          return 'miss', True

  # ============================================================
  # STAGE 3 -- Replay driver
  # ============================================================
  POLICY_GRID = {
      'fixed_ttl':   [FixedTTLPolicy(ttl=v) for v in [0.5, 1, 2, 4, 8, 16, 32]],
      'd_ttl':       [DTTLPolicy(h_target=h, c=c) for h in [0.5,0.6,0.7,0.8,0.9] for c in [0.5,1.0,2.0]],
      'freshcache':  [FreshCacheGatePolicy(error_budget=e) for e in [0.05,0.10,0.20,0.35]],
      'aimd':        [AIMDPolicy(a=a, b=b) for a in [0.25,0.5,1.0,2.0] for b in [0.3,0.5,0.7]],
  }

  results = []
  for regime in volatility_regimes:
      for policy_family, policy_instances in POLICY_GRID.items():
          for policy in policy_instances:
              policy_state = fresh_copy(policy)  # reset per-episode-set state per (regime, knob) run
              log = []
              for episode in episodes_in_regime(regime):
                  for call in episode['calls']:
                      decision, valid = policy_state.on_call(
                          call['call_site_id'], call['timestamp'], call['true_version'],
                          spot_check_fn=make_spot_checker(rate=SPOT_CHECK_RATE, rng=rng))
                      log.append({'site': call['call_site_id'], 'decision': decision, 'valid': valid,
                                  'stale_events_so_far': cumulative_stale_count(policy_state, call['call_site_id'])})
              hit_rate = fraction(log, lambda r: r['decision']=='hit')
              stale_rate = fraction(log, lambda r: r['decision']=='hit' and not r['valid'])
              convergence_point = find_convergence_index(log, policy_family)  # see Stage 4
              results.append({'regime': regime, 'policy_family': policy_family,
                               'knob': describe_knob(policy), 'hit_rate': hit_rate,
                               'stale_rate': stale_rate, 'convergence_events': convergence_point})

  # ============================================================
  # STAGE 4 -- Convergence detection (only meaningful for adaptive policies)
  # ============================================================
  def find_convergence_index(log, policy_family):
      # For d_ttl / aimd / freshcache: track the per-site window/ttl/lambda
      # trajectory over time; define 'converged' as the first point after
      # which the value stays within +/-10% of its own trailing mean for
      # the rest of the episode set (a simple rolling-band stability test).
      # Report convergence in units of CONFIRMED-STALENESS FEEDBACK EVENTS
      # consumed up to that point (not raw calls), since that is the
      # hypothesis's actual currency. For freshcache, additionally report
      # whether min_obs_to_fit was ever reached per site (some low-repeat
      # sites may NEVER calibrate -- this is an expected, reportable failure
      # mode, not a bug).
      ...

  # ============================================================
  # STAGE 5 -- Frontier + comparison outputs
  # ============================================================
  # For each (regime, policy_family): sort knob sweep points by hit_rate,
  # take the Pareto-efficient subset (max hit_rate for given stale_rate).
  # Compute frontier dominance: for each aimd point, does some d_ttl/fixed
  # point dominate it (>= hit_rate AND <= stale_rate)? Aggregate a
  # 'fraction of aimd points non-dominated' summary per regime.
  # Compare median/IQR of convergence_events across policy families,
  # per regime, especially in a LOW-REPEAT-COUNT sub-slice of episodes
  # (call sites visited <= 5 times) -- this is the decisive regime named
  # in success_criteria.

  # ============================================================
  # STAGE 6 -- Write method_out.json
  # ============================================================
  # {
  #   'per_run_results': results,                # full grid, all regimes/knobs
  #   'frontiers': {regime: {policy_family: [(hit_rate, stale_rate), ...]}},
  #   'dominance_summary': {...},
  #   'convergence_summary': {regime: {policy_family: {median, p10, p90}}},
  #   'low_repeat_slice_summary': {...},          # the headline comparison
  #   'ablations': {'aimd_presumed_valid_weight': [...], 'spot_check_rate_sensitivity': [...]},
  #   'config': {grid definitions, rng seeds, spot_check_rate, n_episodes, ...},
  #   'verdict': 'CONFIRMS' | 'DISCONFIRMS' | 'MIXED',   # per success_criteria (a) and (b) separately
  # }
fallback_plan: >-
  1) If the dependency DATASET artifact does not already contain pre-simulated agent call traces with a controllable volatility
  schedule (only raw resources/tools), fall back to generating the traces in-house inside this experiment using Stage 1's
  pure-Python simulator (Zipf-skewed call-site revisits over a small per-episode working set, resources with static/periodic/bursty
  version-change schedules) -- this needs no LLM calls and no dataset beyond a list of resource IDs, so it degrades gracefully
  to a fully synthetic but still controllable workload. 2) If Basu et al.'s exact d-TTL update is ambiguous or its provable-convergence
  step-size schedule (gamma_k = c/(k+1)) proves numerically unstable (oscillation, divergence) on this shorter agent-episode
  traffic (their paper assumes CDN-scale request volume, orders of magnitude more requests per object than an agent call site
  gets), document the instability as a finding rather than hiding it, and additionally report a simplified fixed-step EWMA-toward-target-hit-rate
  variant as a secondary, better-behaved SOTA-adaptive baseline so the AIMD-vs-adaptive-baseline comparison is not vacated
  by one baseline collapsing. 3) If the FreshCache-style fit never reaches min_obs_to_fit for most call sites (very plausible
  given the low-repeat-count regime is the whole point), this is not a failure to fix -- it IS the expected result supporting
  the hypothesis; report the fraction of sites that never calibrate as a headline number, alongside a version of FreshCache
  with a shared cross-site prior (partial pooling of lambda across all sites of the same resource-schedule type) as a fairer
  reference so the comparison isn't a strawman. 4) If ground-truth validity is expensive/impossible to compute for some resource
  type, restrict volatility injection to schedules where ground truth is always analytically known (as in Stage 1's Resource
  classes) rather than trying to reconstruct it after the fact. 5) If the full knob grid (7 TTL x 15 d-TTL x 4 freshcache
  x 12 AIMD x N regimes) is too slow, first cut grid density (fewer knob values) before cutting episode count or regime count
  -- convergence-speed and frontier-shape claims need enough episodes per cell, not enough knob resolution. 6) If time runs
  short, prioritize completing all four policies on ONE volatility regime with a full knob sweep and convergence analysis
  before adding more regimes -- a complete single-regime comparison is a valid, reportable result; a partial multi-regime
  sweep with missing cells is not.
testing_plan: >-
  1) Unit-test each policy class in isolation on a tiny hand-constructed trace (e.g., 20 calls to 2 sites with a known version-change
  schedule) and manually verify the expected cache hit/miss/window trajectory by hand-computation before running any large
  sweep -- especially verify AIMD's window actually grows on repeated confirmed-valid hits and collapses sharply after an
  injected confirmed-stale hit, and that d-TTL's TTL moves toward target hit rate over enough iterations on a synthetic all-static
  (never-stale) resource. 2) Run one mini end-to-end pass: 1 regime, 2-3 episodes, 1 knob value per policy family, confirm
  method_out.json fields populate without errors and hit_rate/stale_rate are in [0,1] and sane (e.g., fixed TTL=0 should give
  ~0% hit rate; TTL=infinity on a fully static resource should give ~100% hit rate and 0% stale rate -- these are sanity boundary
  checks, verify them explicitly). 3) Check for a known pathology before scaling: AIMD window collapsing to w_min and never
  recovering (should recover via additive increase after enough confirmed-valid hits -- verify this happens within a bounded
  number of calls in the mini test) and d-TTL oscillating without settling (plot/print the TTL trajectory for a few sites
  in the mini run and inspect). 4) Verify the low-repeat-count slice logic on synthetic data with call sites visited exactly
  3-5 times, confirming FreshCache's fit legitimately fails to calibrate there (lambda stays at prior) while AIMD's window
  has visibly moved from its init value -- this is the core hypothesis mechanism and must be checked BEFORE trusting full-scale
  numbers. 5) Only after all mini checks pass, scale to the full regime x knob-grid x episode-count sweep, and re-run the
  same boundary sanity checks (TTL=0 and TTL=infinity behavior) on the full run as a regression check that nothing broke when
  scaling up.
</artifact_plan>



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
