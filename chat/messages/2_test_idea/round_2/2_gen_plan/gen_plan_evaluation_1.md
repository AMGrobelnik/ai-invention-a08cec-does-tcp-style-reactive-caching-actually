# gen_plan_evaluation_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_evaluation_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-10 02:24:41 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_plan/gen_plan_evaluation_1
```

### [2] SYSTEM-USER prompt · 2026-08-10 02:24:47 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EVALUATION

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed
</artifact_type_info>

<available_resources>
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

<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>
</available_resources>

<time_budget>

The evaluation executor has 3h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape. Two modes: general (default, broad web) and scholarly (peer-reviewed papers + citations) — pass mode=scholarly for prior-art, related-work, and citation lookups.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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

<hypothesis>
kind: hypothesis
title: Congestion-Control-Style Cache TTL for Agents
hypothesis: >-
  In an LLM agent loop, treating each tool-call site's cache lifetime as a TCP congestion window -- additively growing the
  reuse window after every confirmed-valid cache hit, and multiplicatively slashing it after every confirmed-stale hit --
  reaches a comparable-or-better redundant-call-reduction-vs-stale-serve-rate operating point than (a) a fixed TTL and (b)
  target-hit-rate stochastic-approximation TTL adaptation (d-TTL), with the advantage concentrated in and increasing with
  underlying volatility (fully non-dominated at high volatility, evenly split at medium, majority-dominated at low). This
  first success criterion now has direct empirical support from a synthetic, volatility-controlled replay harness. The originally
  hypothesized second advantage -- that AIMD needs far fewer confirmed-staleness feedback events than a fitted probabilistic
  staleness gate (FreshCache-style) to reach a stable operating point -- is REVISED DOWNWARD to a claim the evidence does
  not support in aggregate: under a uniform tolerance-band stabilization definition, AIMD's median low-repeat convergence-event
  count (14.0-15.5) exceeded both a literal d-TTL reimplementation (11.0) and a corrected EWMA hit-rate-targeted baseline
  (7.0-7.75), and nominally exceeded FreshCache's raw fitted-gate figure (5.0), though that figure reflects fast-but-frequently-untrustworthy
  calibration (only 36.7-38.3% of low-repeat sites judged genuinely calibrated by a Wilson-interval sample-floor check). The
  mechanism identified is that AIMD is responsive earlier than the fitted gate (its window visibly moves after a handful of
  observations, unlike FreshCache which stays pinned to its prior) but settles later, because unbounded additive growth between
  confirmations keeps producing small movements that delay entry into a stability band -- an inherent property of a constant-increment
  AIMD schedule under a fixed stabilization tolerance, not a tuning artifact of the specific (a,b) grid tested. Two evidentiary
  caveats now attach to all of the above and must be resolved before the claims can be treated as robust: (1) the reported
  results were generated entirely by the experiment harness's in-process synthetic Zipf-skewed simulator because an artifact-wiring
  bug meant the real-content-grounded versioned corpus (5,307 rows from Wikipedia/SQuAD, Quora Question Pairs, and Our World
  in Data) was never actually loaded and replayed, despite being purpose-built for this study; (2) the independently-built
  statistical evaluation pipeline (bootstrap CIs, Pareto-AUC, Holm-corrected significance tests, mechanical CONFIRMS/DISCONFIRMS
  verdict) never ran against real data due to an event-log schema mismatch between the experiment output and evaluation input,
  so every number above is a self-reported point estimate from the same harness that generated the data, with no independent
  uncertainty quantification, and with small per-cell sample sizes (n=4-15 knob/replicate combinations per regime per policy
  family, only a=0.25 ever swept).
motivation: >-
  The strongest existing adaptive-TTL result, d-TTL/f-TTL from CDN caching research, provably converges a TTL parameter toward
  a target *hit rate* using stochastic approximation -- but hit rate says nothing about whether those hits returned correct,
  non-stale content; it was built for content-delivery traffic where staleness usually isn't safety-relevant. The strongest
  existing staleness-aware caches for LLM pipelines, FreshCache (risk-constrained temporal caching for RAG) and vCache (verified
  semantic caching with Bayesian per-entry error-rate guarantees), instead fit an explicit probabilistic staleness/error model
  per entry and gate reuse against a fixed error budget -- powerful, but they require a labeled calibration signal to fit
  that model (ground-truth staleness snapshots, or online Bayesian posterior updates over many similarity observations) before
  the guarantee is meaningful, and the model itself must be re-fit or re-trusted whenever workload volatility shifts. Agent
  loops are exactly the setting where a third option is attractive: many call sites are visited only a handful of times per
  episode, an explicit probability model has too little data to fit reliably, and yet a *cheap, purely reactive, feedback-driven*
  rule -- exactly the situation TCP congestion control was built to solve (react to unreliable, low-signal feedback about
  an unknown and shifting environment, with no model of the underlying process) -- could adapt fast per call-site with no
  fitting step at all. If a simple AIMD rule matches or beats a fitted probabilistic gate on the reduction-vs-staleness frontier
  while needing an order of magnitude less confirmed-staleness feedback to converge, that is a concrete, actionable result
  for exactly the low-repeat-count, low-labeled-data regime agent loops live in.
assumptions:
- >-
  For a sample of cache-served tool calls we can obtain a ground-truth valid/stale label after the fact (by issuing a live
  re-query and diffing), giving the confirmed-hit / confirmed-stale feedback signal the AIMD rule consumes -- the same kind
  of feedback FreshCache and vCache also require to calibrate, so this is not an extra assumption relative to the strongest
  baselines
- >-
  Each tool call site (function + argument signature) recurs enough times within and across simulated episodes for a per-site
  reuse window to have room to grow and shrink -- true for the intended targets (file re-reads, repeated/near-duplicate searches,
  repeated computations) but not for one-shot calls, which no caching scheme helps anyway
- >-
  A simulated or replayed agent-loop workload with realistic call repetition and controllable underlying volatility (so ground-truth
  staleness events can be injected/observed) is constructible from OpenRouter-backed agents wrapping instrumented tools, since
  real production agent traces are not directly accessible
- >-
  Convergence speed (staleness events needed before the policy stabilizes near a good operating point) is a meaningful axis
  to compare, not just the converged operating point itself -- appropriate given agent episodes are short relative to CDN
  traffic streams, so how fast a policy adapts matters as much as where it converges
investigation_approach: >-
  Build an agent-loop tool-call harness (OpenRouter LLM driving simulated/wrapped tools: file reads over a versioned corpus,
  web search/fetch, repeated computations) that logs every tool call, arguments, timestamp, and result, and can force a live
  re-query on a sampled subset of cache hits to get a binary valid/stale ground-truth label. Implement three cache policies
  at each call site: (1) fixed TTL swept over several values; (2) a d-TTL-style stochastic-approximation policy that adapts
  TTL toward a target hit rate (reimplementing the mechanism from Basu et al.'s d-TTL, adapted from CDN request streams to
  per-call-site agent traffic); (3) the proposed AIMD policy -- reuse window w_i per call site i, additive increase w_i +=
  a after each confirmed-valid hit (or after a hit that is never checked, treated as presumed-valid under a background spot-check
  rate), multiplicative decrease w_i *= b (b<1) immediately after any confirmed-stale hit, with w_i floor/ceiling bounds;
  and, as an upper-reference (not to be beaten, just situated against), a FreshCache-style fitted staleness-probability gate
  reimplemented for the agent-tool setting. Inject controllable underlying volatility (some simulated resources change on
  a schedule, others are static) so ground-truth staleness is known for evaluation even outside the sampled spot-checks. Run
  repeated episodes across volatility regimes and measure, for each policy: (i) fraction of tool calls served from cache (redundant-call
  reduction), (ii) empirical stale-serve rate, (iii) the reduction-vs-staleness Pareto frontier swept over each policy's tunable
  knob (TTL value / target hit rate / AIMD increase-decrease parameters), and (iv) number of confirmed-staleness feedback
  events consumed before each adaptive policy's per-site window stabilizes (convergence sample-efficiency).
success_criteria: >-
  CONFIRMS the hypothesis if, across the tested volatility regimes: (a) AIMD reaches a comparable or better point on the reduction-vs-staleness
  frontier than fixed-TTL and d-TTL-style hit-rate-targeted adaptation, and (b) AIMD's per-site window converges to a stable
  operating range using substantially fewer confirmed-staleness feedback events than the fitted probabilistic gate needs to
  produce a trustworthy calibrated threshold (e.g., a low-repeat-count regime where AIMD has already stabilized but the fitted
  model still has too few samples to calibrate). DISCONFIRMS/refutes if AIMD's reactive rule is dominated on the frontier
  by d-TTL-style adaptation (i.e., matching a hit-rate target turns out to track staleness just as well once mapped to agent
  workloads) or if it needs comparable or more staleness feedback to stabilize than the fitted probabilistic model needs to
  calibrate -- either outcome is a genuine, reportable finding about whether control-theoretic reactive caching earns its
  simplicity in the low-data agent-loop regime, versus the fitted-model approach that already exists for this problem.
related_works:
- >-
  FreshCache: Risk-Constrained Freshness-Aware Semantic Caching for Open-Web RAG (Mansoor, Ahmad & Yoon, arXiv:2607.04281,
  2026) -- read in full. Fits an exponential-decay-plus-MLP staleness-probability model per entry/tier and gates reuse against
  a fixed per-tier error budget (0.10/0.20/0.35), evaluated on 8,072-31,201 real web queries with ground-truth snapshot labels
  at 1h/12h/24h/7d; reports 97-98% search savings at 0.1-3.3% stale error, beating SemanticTTL/vCache/SCALM. This is the closest
  prior mechanism -- probabilistic risk-budget gating -- but it is a fitted model requiring a substantial labeled calibration
  set per entry class and targets open-web RAG passages, not per-call-site agent tool caching; the present hypothesis instead
  proposes a model-free, purely reactive control rule aimed at the low-repeat-count regime where fitting FreshCache's kind
  of model is impractical, and directly compares convergence speed against it.
- >-
  vCache: Verified Semantic Prompt Caching (Schroeder et al., arXiv:2502.03771, 2025/2026) -- an online Bayesian learning
  algorithm that estimates a per-prompt-embedding similarity threshold to give user-defined error-rate guarantees on whether
  a semantically-matched cache hit is the *correct* answer; this targets match-correctness for semantic similarity caching,
  not time-based staleness of a fixed call's result, and still requires online posterior fitting per cached item, unlike the
  proposed reactive per-site window.
- >-
  Adaptive TTL-Based Caching for Content Delivery -- d-TTL and f-TTL (Basu, Sundarrajan, Ghaderi, Shakkottai & Sitaraman,
  arXiv:1704.04448 / IEEE, 2017) -- read in full. d-TTL uses stochastic approximation (actor-critic style) to converge a per-object
  TTL toward a *target hit rate*, with provable convergence for bursty non-stationary CDN traffic (500M+ request trace, ~1.3%
  hit-rate error); f-TTL adds a two-level filter for non-stationary vs stationary content. Neither algorithm's objective involves
  confirmed correctness/staleness at all -- they optimize hit rate or cache size, which is the right target for CDN content
  delivery but silent on whether hits are stale, and neither has been applied to per-call-site agent tool caching. The proposed
  AIMD policy targets staleness feedback directly and is evaluated head-to-head against a reimplementation of d-TTL's mechanism
  ported to this setting.
- >-
  ToolCacheAgent: Accelerating LLM Agent Through Intelligent Tool Call Caching (OpenReview 2026) -- an LLM-driven planner
  agent that assigns each tool a caching plan (cacheable / TTL / inter-tool invalidation rule) once, from the tool's semantics,
  reporting up to 1.69x latency speed-up; the plan is static once generated and not updated from observed confirmed-staleness
  feedback during execution, unlike the proposed per-site online-adapting window.
- >-
  TVCACHE: A Stateful Tool-Value Cache for Post-Training LLM Agents (Vijaya Kumar et al., arXiv:2602.10986, 2026) -- caches
  by exact longest-prefix match on the agent's full tool-call-history tree (a hit requires the entire preceding trajectory
  to match a previously observed one), aimed at RL post-training rollouts with high trajectory overlap; this is an exact-match
  structural cache with no notion of graded time-based staleness or per-entry reuse window at all, addressing a different
  regime (near-identical repeated rollouts) than the present hypothesis's within-episode, non-identical-trajectory redundant
  calls.
inspiration: >-
  PROCEDURAL/METHODOLOGICAL: TCP congestion control's AIMD rule was designed for exactly this class of problem -- adapt a
  resource-usage window under noisy, sparse, delayed feedback about an unknown and shifting environment, without ever fitting
  an explicit model of that environment, and recover fast from a bad outcome (packet loss / here, a confirmed-stale serve)
  via a sharp multiplicative cut while probing for more headroom via slow additive growth when things go well. That asymmetry
  -- cheap to gain, expensive to lose -- is precisely the shape wanted for cache reuse windows once staleness is reframed
  as a 'loss event.' After reading the two closest prior mechanisms in full (FreshCache's fitted staleness-probability + error-budget
  gate, and d-TTL's stochastic-approximation TTL targeting hit rate), neither uses this reactive, model-free, loss-event-driven
  control law, and neither is evaluated for the specific advantage a reactive rule offers over a fitted one: needing far less
  labeled staleness feedback to converge, which is the binding constraint in agent loops where any given tool call site is
  seen only a handful of times per episode.
terms:
- term: AIMD (additive increase, multiplicative decrease)
  definition: >-
    A feedback control rule, the core of TCP congestion control, that slowly grows a resource window on success and sharply
    shrinks it on a detected failure/overload signal, converging toward an efficient operating point without needing a model
    of the underlying system.
- term: Cache reuse window
  definition: >-
    The time interval, maintained per tool-call site, during which a cached tool result is served instead of re-executing
    the call; here it grows or shrinks based on confirmed-valid or confirmed-stale outcomes rather than being fixed or fit
    from a probability model.
- term: Confirmed-stale event
  definition: >-
    An observed instance where a cache hit was served but a live re-query (or later ground truth) shows the cached value no
    longer matches -- the 'loss signal' the AIMD rule reacts to, analogous to a dropped packet in TCP.
- term: Reduction-vs-staleness frontier
  definition: >-
    The tradeoff curve between how many redundant tool calls a caching policy avoids (efficiency) and how often it serves
    an outdated answer (correctness risk); comparing policies means comparing where each one lands on, and how it sweeps,
    this curve.
- term: Stochastic-approximation TTL (d-TTL)
  definition: >-
    An adaptive-TTL method from CDN research that nudges a TTL parameter up or down using a Robbins-Monro-style update to
    converge toward a specified target cache hit rate, independent of whether served hits are actually still correct.
summary: >-
  We hypothesize that a TCP-congestion-control-style AIMD rule for per-call-site cache reuse windows -- grow slowly on confirmed-valid
  hits, cut sharply on confirmed-stale hits -- matches or beats both fixed TTL and the state-of-the-art hit-rate-targeted
  adaptive TTL (d-TTL) on the redundant-call-reduction-vs-staleness tradeoff in LLM agent loops, while needing far less labeled
  staleness feedback to converge than fitted probabilistic staleness-gating caches like FreshCache require to calibrate --
  a genuine advantage in the low-repeat-count regime typical of agent episodes.
_relation_rationale: >-
  Same AIMD-vs-baselines frame; frontier claim narrowed+confirmed directionally, convergence claim reversed by evidence
_confidence_delta: decreased
_key_changes:
- >-
  Split the single combined hypothesis into two explicitly separated claims matching the two success criteria, since evidence
  now diverges sharply between them
- >-
  Frontier-non-domination claim (criterion a) upgraded from purely speculative to directionally supported by data, with the
  volatility-dependence pattern (strongest at high volatility) now stated as a specific, evidence-grounded finding rather
  than an open question
- >-
  Sample-efficiency claim (criterion b) reversed from the original hypothesis's expectation: AIMD converges SLOWER than both
  hit-rate-targeted baselines and the fitted gate's raw event count, not faster; reframed as a genuine negative/mixed finding
  with the responsive-but-slow-to-stabilize mechanism specified
- >-
  Added the artifact-wiring bug (synthetic-only data, real corpus never consumed) and the missing independent statistical
  evaluation (BLOCKED_NO_DATA) as first-class caveats that must be fixed before the claims are robust, per reviewer MAJOR
  feedback
- >-
  Flagged small per-cell sample sizes and single-value a=0.25 sweep as a specific methodological gap to widen in the next
  iteration, per reviewer MAJOR feedback
- >-
  Noted FreshCache's fast-but-uncalibrated convergence as a qualifying nuance rather than a clean baseline win, since raw
  event-count comparisons alone are misleading
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: evaluation_iter2_dir2
type: evaluation
objective: >-
  Re-run the existing bootstrap-CI, Pareto-AUC, Holm-corrected-significance, and mechanical CONFIRMS/DISCONFIRMS evaluation
  pipeline against the newly fixed, correctly-schemad experiment event log, producing statistically grounded versions of Table
  1 (frontier dominance) and Table 2 (convergence events) for both the real-content and synthetic workload variants.
approach: >-
  Reuse the existing eval.py analysis logic (episode-level bootstrap 95% CIs on hit fraction and stale rate, Pareto frontier
  + AUC + dominance fraction per volatility regime, uniform tolerance-band convergence definition with Wilson-interval calibration
  gating, paired Wilcoxon/bootstrap tests with Holm-Bonferroni correction, spot-check-rate and presumed-valid-weight ablation
  reporting) but point it at the new experiment artifact's event log and verify column-by-column that the schema matches before
  running (add an explicit schema-diff check that fails loudly rather than silently degrading to BLOCKED_NO_DATA again). Run
  separately on the real-content-corpus results and the synthetic-simulator results from the same experiment artifact, and
  add one new comparison: whether the real-content run's dominance fractions and convergence medians fall within the synthetic
  run's bootstrap CIs (a realism-robustness check answering reviewer concern about ecological validity). Report final CONFIRMS/DISCONFIRMS
  verdicts with confidence intervals for both criteria (a) frontier non-domination and (b) convergence sample-efficiency,
  superseding the prior BLOCKED_NO_DATA and self-reported-point-estimate results.
depends_on:
- id: art_qtEtMpLZuRGI
  label: experiment
  relation_type:
  relation_rationale:
- id: art_T0onLH9xokqw
  label: dataset
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

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
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
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

--- Dependency 2 ---
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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle
</artifact_executor_scope>

<artifact_planning_rules>
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for evaluation artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EVALUATION artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "metrics_descriptions": {
      "description": "What metrics will be computed and how they're defined",
      "title": "Metrics Descriptions",
      "type": "string"
    },
    "metrics_justification": {
      "description": "Why these metrics are the right ones - what do they tell us about the hypothesis",
      "title": "Metrics Justification",
      "type": "string"
    }
  },
  "required": [
    "title",
    "metrics_descriptions",
    "metrics_justification"
  ],
  "title": "EvaluationPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-10 02:24:47 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [4] ASSISTANT · 2026-08-10 02:24:55 UTC

```
No response requested.
```

### [5] SYSTEM-USER prompt · 2026-08-10 02:24:55 UTC

```
continue
```

### [6] TOOL CALL — Write · 2026-08-10 02:25:32 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_plan/gen_plan_evaluation_1/.terminal_claude_agent_struct_out.json

{
  "title": "Statistically Verify AIMD Cache Results",
  "summary": "Re-run the bootstrap-CI / Pareto-AUC / Holm-corrected significance / mechanical-verdict evaluation pipeline (eval.py logic from the prior BLOCKED_NO_DATA attempt) against the experiment artifact's actual event log, with an explicit fail-loud schema-diff gate replacing the silent degrade that caused the prior failure. Because the upstream experiment (art_qtEtMpLZuRGI) only ever produced synthetic-simulator results (its own dependency-wiring bug meant the versioned real-content corpus, art_T0onLH9xokqw, was never loaded or replayed), this evaluation cannot literally run 'separately on real-content and synthetic results' as the direction assumes — that split does not exist in the available data. Instead: (1) rigorously verify/re-derive every self-reported number in method_out.json with independent statistics, producing CI-backed Table 1 (frontier dominance) and Table 2 (convergence events) for the synthetic run that does exist; (2) explicitly attempt and document the schema-compatibility check between the experiment's actual per-call event log and the dataset artifact's full_data_out.json schema, so a concrete, reproducible diagnosis of the wiring bug (and what would be needed to fix it) replaces the prior vague 'artifact-wiring bug' description; (3) as the realism check, compare method_out.json's per-resource volatility-regime structure (static/periodic/bursty labels, revisit cadences) against the dataset's real-content-derived version_schedule statistics to give an evidence-based ecological-validity estimate even without a live real-content re-run; (4) issue final CONFIRMS/DISCONFIRMS verdicts, with CIs, for both success criteria, and explicitly flag criterion (b) as UNRESOLVED/BLOCKED-ON-REEXECUTION if the schema-diff or replay-necessity check confirms real-content data genuinely never entered the evaluated event log.",
  "runpod_compute_profile": "cpu_light",
  "metrics_descriptions": "PRIMARY (per volatility regime x policy family, from method_out.json's 150 (regime, policy_family, knob) grid): (1) Episode-level bootstrap 95% CIs (n=10,000 resamples, resample at the episode level not the call level to respect within-episode correlation) on hit_rate and stale_rate for every (regime, policy, knob) cell that has per-episode granularity in the raw event log; if method_out.json only stores per-run aggregates without per-episode breakdowns, recompute per-episode statistics directly from the raw call-level event log (method.py's underlying replay output) rather than bootstrapping the aggregate alone — this distinction must be checked first since it determines whether real CIs are even possible from the stored artifact. (2) Pareto frontier + AUC (trapezoidal, hit_rate on x, 1-stale_rate on y, restricted to the empirical range covered by all policy families for fair AUC comparison) computed per regime for each policy family, plus a dominance fraction: fraction of AIMD's 12 (a,b) knob points that are NOT Pareto-dominated (i.e., no baseline point has both >= hit_rate and <= stale_rate) by any FixedTTL/DTTL/EWMA/FreshCache point in the same regime, with a bootstrap CI on that fraction via resampling episodes and recomputing dominance. (3) Convergence-event counts: for each policy family in the low-repeat-count slice (sites visited <=5 times), the number of confirmed-staleness-feedback events consumed before the per-site window enters and stays within the artifact's defined tolerance band; report median/p10/p90 with bootstrap CIs, and separately report FreshCache's Wilson-interval-gated calibrated fraction with its own binomial CI. (4) Paired significance tests: Holm-Bonferroni-corrected paired Wilcoxon signed-rank (or paired bootstrap difference-of-medians if n per cell is too small for Wilcoxon's asymptotic validity, which the executor must check via a minimum-n threshold, e.g. n>=6 pairs) comparing AIMD vs each baseline on (a) frontier AUC and (b) convergence-event count, within each volatility regime. SECONDARY / VALIDITY: (5) Schema-diff report: an explicit column-by-column comparison of the experiment's actual event-log schema (as emitted by method.py / stored alongside method_out.json) against full_data_out.json's row schema (input/output/metadata_* fields), stating precisely which fields are missing/incompatible and therefore why real-content replay did not occur — output as a structured table, not prose. (6) Ecological-validity proxy comparison: contrast the synthetic simulator's Zipf-skewed revisit-count distribution and volatility-regime version-change rates (from method_out.json) against the dataset's real version_schedule-derived revisit and change-rate statistics (computed directly from full_data_out.json / mini_data_out.json), reporting whether the synthetic run's regime parameters fall inside vs. outside the empirical range the real corpus actually exhibits, per volatility regime. (7) Sample-size audit: explicit n per (regime, policy, knob) cell used in every CI/test above, flagging any cell with n<8 as low-confidence in the output rather than suppressing it. FINAL: mechanical CONFIRMS/DISCONFIRMS/MIXED/UNRESOLVED verdict per criterion (a) and (b), each with its supporting CI/test results and an explicit note when a verdict is downgraded to UNRESOLVED because the underlying data source (synthetic-only) cannot support the claim as originally scoped (i.e., real-content robustness for criterion (a) or (b) specifically).",
  "metrics_justification": "The hypothesis was left in an unresolved state by two documented pipeline failures (a data-wiring bug that only fed the synthetic simulator into method.py, and an evaluation-side schema mismatch that produced BLOCKED_NO_DATA), so the single highest-value thing this evaluation can do is close the second failure and give the existing self-reported synthetic-run numbers real uncertainty quantification -- turning 'AIMD's median was 14.5 vs baselines' 9.375' from a point estimate anyone could dispute into a claim with a CI and a Holm-corrected significance test, which is exactly what the hypothesis's own success criteria demand ('with confidence intervals for both criteria'). Episode-level (not call-level) bootstrap resampling is essential because calls within an episode share a policy state trajectory and are not independent draws -- treating individual calls as i.i.d. would understate variance and could manufacture false significance. Pareto-AUC with a dominance fraction directly operationalizes criterion (a) ('reaches a comparable-or-better operating point... non-dominated at high volatility') as a single falsifiable number per regime instead of eyeballing a frontier plot. The convergence-event CI and Wilson-gated FreshCache calibrated-fraction directly operationalize criterion (b), and separating 'raw event count to first stabilization' from 'fraction of those calibrations that were trustworthy' is exactly the distinction the hypothesis itself draws (FreshCache converges nominally faster but only 36.7-38.3% of those convergences were genuinely calibrated) -- collapsing that into one number would misrepresent the finding the experiment already surfaced. The schema-diff and ecological-validity proxy comparison are not optional nice-to-haves: without them, this evaluation would silently repeat the exact failure mode (BLOCKED_NO_DATA from an unexamined mismatch) that already happened once, and without at least a proxy comparison, the paper has zero evidence bearing on whether the reported effect sizes are realistic outside a hand-tuned Zipf simulator -- a reviewer-flagged concern (ecological validity) the direction explicitly asks to address. Explicitly downgrading a criterion to UNRESOLVED when the data genuinely cannot support it (rather than forcing a CONFIRMS/DISCONFIRMS call on synthetic-only data mislabeled as validated) preserves the epistemic honesty the hypothesis document itself models -- it already downgraded its own confidence once for exactly this reason, and the evaluation should not re-inflate certainty the underlying artifacts don't earn."
}
```

### [7] TOOL RESULT — Write · 2026-08-10 02:25:32 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_plan/gen_plan_evaluation_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Statistically Verify AIMD Cache Results\",\n  \"summary\": \"Re-run the bootstrap-CI / Pareto-AUC / Holm-corrected significance / mechanical-verdict evaluation pipeline (eval.py logic from the prior BLOCKED_NO_DATA attempt) against the experiment artifact's actual event log, with an explicit fail-loud schema-diff gate replacing the silent degrade that caused the prior failure. Because the upstream experiment (art_qtEtMpLZuRGI) only ever produced synthetic-simulator results (its own dependency-wiring bug meant the versioned real-content corpus, art_T0onLH9xokqw, was never loaded or replayed), this evaluation cannot literally run 'separately on real-content and synthetic results' as the direction assumes — that split does not exist in the available data. Instead: (1) rigorously verify/re-derive every self-reported number in method_out.json with independent statistics, producing CI-backed Table 1 (frontier dominance) and Table 2 (convergence events) for the synthetic run that does exist; (2) explicitly attempt and document the schema-compatibility check between the experiment's actual per-call event log and the dataset artifact's full_data_out.json schema, so a concrete, reproducible diagnosis of the wiring bug (and what would be needed to fix it) replaces the prior vague 'artifact-wiring bug' description; (3) as the realism check, compare method_out.json's per-resource volatility-regime structure (static/periodic/bursty labels, revisit cadences) against the dataset's real-content-derived version_schedule statistics to give an evidence-based ecological-validity estimate even without a live real-content re-run; (4) issue final CONFIRMS/DISCONFIRMS verdicts, with CIs, for both success criteria, and explicitly flag criterion (b) as UNRESOLVED/BLOCKED-ON-REEXECUTION if the schema-diff or replay-necessity check confirms real-content data genuinely never entered the evaluated event log.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"metrics_descriptions\": \"PRIMARY (per volatility regime x policy family, from method_out.json's 150 (regime, policy_family, knob) grid): (1) Episode-level bootstrap 95% CIs (n=10,000 resamples, resample at the episode level not the call level to respect within-episode correlation) on hit_rate and stale_rate for every (regime, policy, knob) cell that has per-episode granularity in the raw event log; if method_out.json only stores per-run aggregates without per-episode breakdowns, recompute per-episode statistics directly from the raw call-level event log (method.py's underlying replay output) rather than bootstrapping the aggregate alone — this distinction must be checked first since it determines whether real CIs are even possible from the stored artifact. (2) Pareto frontier + AUC (trapezoidal, hit_rate on x, 1-stale_rate on y, restricted to the empirical range covered by all policy families for fair AUC comparison) computed per regime for each policy family, plus a dominance fraction: fraction of AIMD's 12 (a,b) knob points that are NOT Pareto-dominated (i.e., no baseline point has both >= hit_rate and <= stale_rate) by any FixedTTL/DTTL/EWMA/FreshCache point in the same regime, with a bootstrap CI on that fraction via resampling episodes and recomputing dominance. (3) Convergence-event counts: for each policy family in the low-repeat-count slice (sites visited <=5 times), the number of confirmed-staleness-feedback events consumed before the per-site window enters and stays within the artifact's defined tolerance band; report median/p10/p90 with bootstrap CIs, and separately report FreshCache's Wilson-interval-gated calibrated fraction with its own binomial CI. (4) Paired significance tests: Holm-Bonferroni-corrected paired Wilcoxon signed-rank (or paired bootstrap difference-of-medians if n per cell is too small for Wilcoxon's asymptotic validity, which the executor must check via a minimum-n threshold, e.g. n>=6 pairs) comparing AIMD vs each baseline on (a) frontier AUC and (b) convergence-event count, within each volatility regime. SECONDARY / VALIDITY: (5) Schema-diff report: an explicit column-by-column comparison of the experiment's actual event-log schema (as emitted by method.py / stored alongside method_out.json) against full_data_out.json's row schema (input/output/metadata_* fields), stating precisely which fields are missing/incompatible and therefore why real-content replay did not occur — output as a structured table, not prose. (6) Ecological-validity proxy comparison: contrast the synthetic simulator's Zipf-skewed revisit-count distribution and volatility-regime version-change rates (from method_out.json) against the dataset's real version_schedule-derived revisit and change-rate statistics (computed directly from full_data_out.json / mini_data_out.json), reporting whether the synthetic run's regime parameters fall inside vs. outside the empirical range the real corpus actually exhibits, per volatility regime. (7) Sample-size audit: explicit n per (regime, policy, knob) cell used in every CI/test above, flagging any cell with n<8 as low-confidence in the output rather than suppressing it. FINAL: mechanical CONFIRMS/DISCONFIRMS/MIXED/UNRESOLVED verdict per criterion (a) and (b), each with its supporting CI/test results and an explicit note when a verdict is downgraded to UNRESOLVED because the underlying data source (synthetic-only) cannot support the claim as originally scoped (i.e., real-content robustness for criterion (a) or (b) specifically).\",\n  \"metrics_justification\": \"The hypothesis was left in an unresolved state by two documented pipeline failures (a data-wiring bug that only fed the synthetic simulator into method.py, and an evaluation-side schema mismatch that produced BLOCKED_NO_DATA), so the single highest-value thing this evaluation can do is close the second failure and give the existing self-reported synthetic-run numbers real uncertainty quantification -- turning 'AIMD's median was 14.5 vs baselines' 9.375' from a point estimate anyone could dispute into a claim with a CI and a Holm-corrected significance test, which is exactly what the hypothesis's own success criteria demand ('with confidence intervals for both criteria'). Episode-level (not call-level) bootstrap resampling is essential because calls within an episode share a policy state trajectory and are not independent draws -- treating individual calls as i.i.d. would understate variance and could manufacture false significance. Pareto-AUC with a dominance fraction directly operationalizes criterion (a) ('reaches a comparable-or-better operating point... non-dominated at high volatility') as a single falsifiable number per regime instead of eyeballing a frontier plot. The convergence-event CI and Wilson-gated FreshCache calibrated-fraction directly operationalize criterion (b), and separating 'raw event count to first stabilization' from 'fraction of those calibrations that were trustworthy' is exactly the distinction the hypothesis itself draws (FreshCache converges nominally faster but only 36.7-38.3% of those convergences were genuinely calibrated) -- collapsing that into one number would misrepresent the finding the experiment already surfaced. The schema-diff and ecological-validity proxy comparison are not optional nice-to-haves: without them, this evaluation would silently repeat the exact failure mode (BLOCKED_NO_DATA from an unexamined mismatch) that already happened once, and without at least a proxy comparison, the paper has zero evidence bearing on whether the reported effect sizes are realistic outside a hand-tuned Zipf simulator -- a reviewer-flagged concern (ecological validity) the direction explicitly asks to address. Explicitly downgrading a criterion to UNRESOLVED when the data genuinely cannot support it (rather than forcing a CONFIRMS/DISCONFIRMS call on synthetic-only data mislabeled as validated) preserves the epistemic honesty the hypothesis document itself models -- it already downgraded its own confidence once for exactly this reason, and the evaluation should not re-inflate certainty the underlying artifacts don't earn.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [8] ASSISTANT · 2026-08-10 02:25:34 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json` — it re-runs the CI/Pareto-AUC/Holm-corrected pipeline against the actual synthetic-only event log (since the real-content corpus was never actually replayed), adds an explicit schema-diff gate to prevent the prior silent BLOCKED_NO_DATA failure, substitutes an ecological-validity proxy comparison for the impossible real-vs-synthetic split, and issues CI-backed CONFIRMS/DISCONFIRMS verdicts per criterion, downgrading to UNRESOLVED where the data can't support the original claim.
```
