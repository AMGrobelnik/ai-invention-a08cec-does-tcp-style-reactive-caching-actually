# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-10 01:22:57 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/upd_hypo/upd_hypo
```

### [2] SYSTEM-USER prompt · 2026-08-10 01:23:03 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Congestion-Control-Style Cache TTL for Agents
hypothesis: >-
  In an LLM agent loop, treating each tool-call site's cache lifetime as a TCP congestion window -- additively growing the
  reuse window after every confirmed-valid cache hit, and multiplicatively slashing it after every confirmed-stale hit --
  will reach a better redundant-call-reduction-vs-stale-serve-rate operating point, and reach it in far fewer observed staleness
  events, than (a) a fixed TTL, and (b) target-hit-rate stochastic-approximation TTL adaptation (the current state of the
  art for adaptive TTL), because AIMD's asymmetric response is tuned specifically to correctness violations rather than to
  a hit-rate target that is blind to whether hits were actually still valid.
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
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
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

--- Item 2 ---
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

--- Item 3 ---
id: art_3Kj8hQ_noFpY
type: evaluation
title: AIMD Cache Pareto and Convergence Evaluation
summary: >-
  This evaluation artifact implements the full analysis plan for comparing AIMD, fixed-TTL, d-TTL, and FreshCache-gate caching
  policies on a per-call agent-loop event log: (1) per (policy, knob_value, volatility_regime) reduction-vs-staleness operating
  points with episode-level bootstrap 95% CIs on both cache_hit_fraction and empirical_stale_rate (raw spot-checked and inverse-probability-reweighted),
  (2) Pareto frontier construction per volatility regime with trapezoidal frontier-AUC, Pareto-dominance fraction of AIMD
  points by each baseline, and matched-stale-rate-target hit-fraction comparisons via frontier interpolation, (3) a uniform
  tolerance-band (±10%, 10 consecutive updates) convergence/stabilization definition applied identically to AIMD's window,
  d-TTL's adapted TTL, and FreshCache's calibrated staleness probability (gated additionally on a Wilson-interval sample floor),
  aggregated by call-site repeat-count bucket (low/medium/high) with explicit failure-to-converge rates, (4) paired Wilcoxon/bootstrap
  statistical tests with Holm-Bonferroni correction and effect sizes across regimes and buckets, (5) a mechanical CONFIRMS/DISCONFIRMS
  verdict against the hypothesis's two stated success criteria, and (6) robustness checks (spot-check-rate sensitivity, volatility/repeat-count
  confound table, FreshCache calibration Brier score and reliability diagram, missingness reporting). eval.py is fully implemented,
  tested, and schema-validated (exp_eval_sol_out). However, the upstream dependencies (gen_art_experiment_1 and gen_art_dataset_1)
  contain no per-call event log, method_out.json, or any usable output — both directories hold only an empty session log file
  with zero actual data or predictions. eval.py detects this at runtime, searches all plausible file patterns and locations,
  and — rather than fabricating any metrics — produces a schema-valid, transparent 'BLOCKED_NO_DATA' result: metrics_agg.data_available=0,
  a single documented example explaining exactly what was searched and what columns were required, and metadata.blocked_reason
  with the concrete diagnosis. This means eval_out.json (and its full/mini/preview variants) currently report that evaluation
  could not be run against real data, not a real Pareto/convergence result. If the upstream experiment is re-run and produces
  a valid per-call log with the required columns (episode_id, seed, volatility_regime, call_site_id, timestamp/step_index,
  policy_name, knob_value, served_from_cache, spot_checked, ground_truth_stale, and per-update adapted-value fields), re-running
  eval.py will automatically pick it up and populate all six analysis sections with real numbers and the CONFIRMS/DISCONFIRMS
  verdict, with no code changes needed. Downstream paper-writing steps should treat this artifact's current output as evidence
  that the experiment stage did not yet produce data, not as a null/negative experimental finding.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

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

id: art_3Kj8hQ_noFpY
type: evaluation
title: AIMD Cache Pareto and Convergence Evaluation
summary: >-
  This evaluation artifact implements the full analysis plan for comparing AIMD, fixed-TTL, d-TTL, and FreshCache-gate caching
  policies on a per-call agent-loop event log: (1) per (policy, knob_value, volatility_regime) reduction-vs-staleness operating
  points with episode-level bootstrap 95% CIs on both cache_hit_fraction and empirical_stale_rate (raw spot-checked and inverse-probability-reweighted),
  (2) Pareto frontier construction per volatility regime with trapezoidal frontier-AUC, Pareto-dominance fraction of AIMD
  points by each baseline, and matched-stale-rate-target hit-fraction comparisons via frontier interpolation, (3) a uniform
  tolerance-band (±10%, 10 consecutive updates) convergence/stabilization definition applied identically to AIMD's window,
  d-TTL's adapted TTL, and FreshCache's calibrated staleness probability (gated additionally on a Wilson-interval sample floor),
  aggregated by call-site repeat-count bucket (low/medium/high) with explicit failure-to-converge rates, (4) paired Wilcoxon/bootstrap
  statistical tests with Holm-Bonferroni correction and effect sizes across regimes and buckets, (5) a mechanical CONFIRMS/DISCONFIRMS
  verdict against the hypothesis's two stated success criteria, and (6) robustness checks (spot-check-rate sensitivity, volatility/repeat-count
  confound table, FreshCache calibration Brier score and reliability diagram, missingness reporting). eval.py is fully implemented,
  tested, and schema-validated (exp_eval_sol_out). However, the upstream dependencies (gen_art_experiment_1 and gen_art_dataset_1)
  contain no per-call event log, method_out.json, or any usable output — both directories hold only an empty session log file
  with zero actual data or predictions. eval.py detects this at runtime, searches all plausible file patterns and locations,
  and — rather than fabricating any metrics — produces a schema-valid, transparent 'BLOCKED_NO_DATA' result: metrics_agg.data_available=0,
  a single documented example explaining exactly what was searched and what columns were required, and metadata.blocked_reason
  with the concrete diagnosis. This means eval_out.json (and its full/mini/preview variants) currently report that evaluation
  could not be run against real data, not a real Pareto/convergence result. If the upstream experiment is re-run and produces
  a valid per-call log with the required columns (episode_id, seed, volatility_regime, call_site_id, timestamp/step_index,
  policy_name, knob_value, served_from_cache, spot_checked, ground_truth_stale, and per-update adapted-value fields), re-running
  eval.py will automatically pick it up and populate all six analysis sections with real numbers and the CONFIRMS/DISCONFIRMS
  verdict, with no code changes needed. Downstream paper-writing steps should treat this artifact's current output as evidence
  that the experiment stage did not yet produce data, not as a null/negative experimental finding.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

LLM agent loops -- an LLM repeatedly invoking tools (file reads, web search, code execution,
retrieval) inside a control loop that observes each result and decides the next action -- routinely
re-issue calls whose arguments exactly or near-exactly match a call already made earlier in the same
episode. An agent re-reads a file it opened three turns ago to re-check a detail, re-runs a search
query it already ran with a slightly reworded phrasing, or recomputes an aggregate statistic it already
derived. Caching these calls is an obvious latency and cost win, but it introduces a correctness risk
that plain LRU or fixed-TTL request caching does not confront directly: if the underlying resource has
changed since it was cached, the agent silently reasons over stale content, and because the agent has no
external signal telling it the cache lied, the error propagates into everything downstream of that tool
call. The central design question for agent-side tool caching is therefore not "how do we maximize the
hit rate" but "how do we maximize the hit rate *subject to* keeping the fraction of stale-serves low,"
and doing so per call site, since different tool-call sites in the same agent episode change at wildly
different rates -- a static reference document, a periodically-refreshed dataset, and a rapidly-changing
live metric all appear in the same trace but demand different reuse policies.

This tradeoff is interesting and important because it sits directly on the cost/latency-versus-correctness
frontier that determines whether tool caching is safe to deploy in agent systems at all: aggressive caching
that ignores staleness saves calls but corrupts the agent's world model, while conservative caching that
never reuses anything forfeits the savings caching exists to provide. It is hard because the right reuse
window for a given call site is neither known in advance (volatility is a property of the underlying
resource, not something the agent framework can inspect) nor stationary (a resource that was static for
an episode can start changing, and vice versa), so a caching policy has to *learn* the right window from
observed outcomes, online, per site, cheaply.

It has not been solved by existing adaptive-caching mechanisms for two different reasons. The strongest
adaptive-TTL result from content-delivery research, d-TTL [1], uses a Robbins-Monro stochastic-approximation
update to converge a per-object TTL toward a *target hit rate*; this objective has no notion of correctness
at all -- it optimizes for how often a cached value is served, not for whether that value was still valid
when served, which is exactly backwards for a safety-relevant agent tool call. The strongest
staleness-*aware* caches, FreshCache [2] and vCache [3], instead fit an explicit probabilistic staleness or
match-correctness model per cached entry (an exponential-decay-plus-MLP hazard model in FreshCache's case)
and gate reuse against a fixed error budget; this directly targets correctness, but the fit requires enough
labeled calibration observations per entry (or per entry class) to be trustworthy, which is precisely what
is scarce in agent loops, where a given call-site signature is often seen only a handful of times in an
episode. Nearer-term agent-specific caches sidestep the staleness question altogether: ToolCacheAgent [4]
assigns each tool a static caching plan once, from the tool's semantics, and never updates it from observed
outcomes; TVCACHE [5] caches by exact trajectory-prefix match for RL rollouts with high trajectory overlap,
which has no notion of graded, time-based staleness at all.

We investigate a third option, taken directly from a different field that solved a structurally similar
problem: TCP congestion control's additive-increase, multiplicative-decrease (AIMD) rule [6, 7] adapts a
resource-usage window under noisy, sparse, delayed feedback about an unknown, shifting environment, without
ever fitting a model of that environment, recovering fast from a bad outcome via a sharp multiplicative cut
while probing for more headroom via slow additive growth when things go well. We reframe a confirmed-stale
cache hit as the "loss event" AIMD reacts to: each call site keeps a reuse window that grows additively by
a fixed increment after every confirmed-valid spot-checked hit, and is cut multiplicatively after every
confirmed-stale spot-checked hit. [FIGURE:fig_architecture]

We built a versioned, volatility-labeled tool-call corpus, an agent-loop cache-policy replay harness
implementing five policy families (fixed TTL, a literal d-TTL reimplementation, a corrected EWMA
hit-rate-targeted baseline, an MLE-fitted FreshCache-style staleness gate in raw and partial-pooled
variants, and the proposed AIMD policy), and ran all of them across three volatility regimes. AIMD reaches
a non-dominated point on the reduction-versus-staleness Pareto frontier for the majority of its
knob settings in medium and, especially, high volatility, but the hoped-for sample-efficiency advantage
over the fitted probabilistic gate does not hold in aggregate: AIMD needs *more* confirmed-staleness
feedback events to stabilize than either d-TTL or the EWMA baseline, even though the fitted FreshCache gate
itself frequently fails to calibrate in the same low-repeat regime. We report this mixed outcome in full,
including the specific mechanism (window growth outrunning available spot-check density) that produces it.

**Summary of Contributions**

- An AIMD-based reuse-window caching policy for per-call-site tool caching in LLM agent loops, reframing
  confirmed staleness as a congestion-control loss event (Section 3).
- A versioned, volatility-labeled tool-call corpus built entirely from real seed content (Wikipedia/SQuAD
  passages, Quora Question Pairs duplicate-query groups, and Our World in Data indicator series) with
  three timing-provenance categories and an explicit ground-truth version schedule per resource, enabling
  offline staleness scoring of any cache policy with zero live re-querying (Section 4.1) [ARTIFACT:art_T0onLH9xokqw].
- A five-policy replay harness across three volatility regimes (low/medium/high), including a literal
  reimplementation of d-TTL [1] and of the FreshCache staleness-gating mechanism [2], plus a corrected
  EWMA baseline added after the literal d-TTL update rule was found to get trapped at its TTL floor from a
  low initial condition (Section 4.2) [ARTIFACT:art_qtEtMpLZuRGI].
- An empirical Pareto-dominance and convergence-event analysis showing AIMD is non-dominated on 4/12,
  8/12, and 12/12 knob settings under low, medium, and high volatility respectively (mean fraction
  non-dominated 0.67), while needing more confirmed-staleness events to stabilize (median 14.0-15.5) than
  d-TTL (11.0) or EWMA (7.0-7.75) -- a genuinely mixed result against the hypothesis's two stated success
  criteria (Section 5).

# Related Work

**Hit-rate-targeted adaptive TTL.** Basu et al.'s d-TTL and f-TTL [1] adapt a per-object TTL toward a
target cache hit rate using a Robbins-Monro stochastic-approximation update, with provable convergence
demonstrated on a 500M+ request CDN trace (roughly 1.3% hit-rate error at convergence); f-TTL adds a
two-level filter distinguishing non-stationary from stationary content. The objective is entirely
hit-rate-based: nothing in the update rule depends on whether a served hit was actually still valid, which
is the right choice for content-delivery traffic (where staleness is rarely safety-relevant) but silent on
the axis this paper cares about. We reimplement d-TTL literally, port it to per-call-site agent traffic,
and compare against it directly (Section 4.2).

**Fitted probabilistic staleness gating.** FreshCache [2] fits an exponential-decay-plus-MLP
staleness-probability model per cached entry/tier and gates reuse against a fixed per-tier error budget
(0.10/0.20/0.35 in the original work), evaluated on 8,072-31,201 real open-web RAG queries with
ground-truth freshness snapshots at 1h/12h/24h/7d horizons, reporting 97-98% search savings at 0.1-3.3%
stale-serve error and beating SemanticTTL, vCache, and SCALM [8] on that tradeoff. This is the closest
prior mechanism to what we study -- probabilistic, error-budget-gated reuse -- but the model must be
fit from a substantial labeled calibration set per entry class, and the present work targets exactly the
regime (per-call-site agent tool caching, low repeat counts) where that calibration set is thin. vCache [3]
is a related online Bayesian learning algorithm that fits a per-prompt-embedding similarity threshold with
user-defined error-rate guarantees, but for semantic *match*-correctness in similarity caching rather than
time-based staleness of a fixed call's result, and it likewise requires online posterior fitting per cached
item. We reimplement FreshCache's fitted-gate mechanism (both a raw per-site variant and a
partial-pooling-by-resource-schedule-family variant) as the calibrated-model reference point in our
replay harness.

**Semantic and agent-specific tool caching.** GPTCache [9] and SCALM [8] popularized semantic similarity
caching for LLM query/response pairs, matching near-duplicate prompts rather than tracking time-based
staleness of a fixed resource. ToolCacheAgent [4] uses an LLM planner to assign each tool a static caching
plan (cacheable / TTL / inter-tool invalidation rule) once from the tool's semantics, reporting up to 1.69x
latency speedup, but the plan is fixed after generation and never updates from observed outcomes during
execution. TVCACHE [5] caches by exact longest-prefix match over the full preceding tool-call trajectory,
targeting RL post-training rollouts with high trajectory overlap; a hit requires the entire trajectory
prefix to match exactly, so there is no graded notion of time-based staleness or a per-entry reuse window
at all. Neither addresses the online, per-site, outcome-driven adaptation this paper studies.

**Congestion control as a reactive control law.** AIMD is the core mechanism of TCP congestion avoidance
[6, 7]: additively probe for more bandwidth on success, multiplicatively retreat on a detected loss event,
converging toward an efficient, fair operating point without a model of the network. Its appeal for
reuse-window adaptation is structural: like TCP flows sharing an unknown, shifting bottleneck, individual
call sites face an unknown and possibly shifting update rate for their underlying resource, and AIMD is
designed exactly for adapting a resource-usage window under sparse, noisy, delayed feedback about such an
environment with no fitting step. To our knowledge, no prior work applies this control law to time-based
cache reuse windows gated on confirmed staleness feedback in an LLM agent tool-caching setting; we test
whether that structural analogy pays off empirically rather than merely asserting it.

# Methods

## Problem setup

Each tool-call *site* is a (function, argument-signature) pair; every time the agent loop issues a call
matching a previously cached site, a cache policy must decide whether to serve the cached result or
re-execute the call. A subset of served hits is *spot-checked* -- a live re-query is issued in the
background and diffed against the cached value, producing a binary confirmed-valid / confirmed-stale label
for that hit -- at a fixed spot-check rate (20% of calls in our harness), mirroring the same kind of
after-the-fact ground-truth signal that FreshCache and vCache also require to calibrate, so no policy in
our comparison gets access to more raw information than any other; they differ only in how they *use* it.

## AIMD reuse-window policy (proposed)

Each call site $i$ maintains a reuse window $w_i$ (initialized to $w_{\text{init}}=1.0$, bounded to
$[w_{\min}, w_{\max}] = [0.01, 10^4]$ simulated ticks). A call at site $i$ at time $t$ is served from cache
if a cached value exists and $t - t_{\text{cached}} \le w_i$; otherwise the call is re-executed and the
result is (re-)cached. When a served hit is spot-checked and confirmed valid, the window grows additively,
$w_i \leftarrow \min(w_i + a,\, w_{\max})$; when a served hit is spot-checked and confirmed stale, the
window collapses multiplicatively, $w_i \leftarrow \max(w_i \cdot b,\, w_{\min})$, with $b < 1$
[ARTIFACT:art_qtEtMpLZuRGI]. Unchecked hits are, by default, treated conservatively -- they do not move the
window at all ($\texttt{presumed\_valid\_weight}=0$) -- with an ablation (Section 5.4) testing a variant
that partially credits unchecked hits as presumed-valid. We sweep $a \in \{0.25\}$ paired with
$b \in \{0.3, 0.5, 0.7\}$ across three independent replicate initial windows, giving 12 (a, b, replicate)
knob settings per volatility regime.

## Baseline policies

**Fixed TTL.** A single, non-adapting time-to-live applied uniformly to every call site, swept over a
9-point grid from $\text{TTL}=0$ (a lower boundary probe that must produce exactly 0% hit rate) to
$\text{TTL}=0.99$ (a near-infinite upper boundary probe, expected to approach the ceiling hit rate set by
call repetition in the workload).

**d-TTL.** A literal reimplementation of Basu et al.'s [1] Robbins-Monro stochastic-approximation update,
which nudges a per-site TTL toward a target hit rate $h_{\text{target}}$ with a decaying step size
$\gamma_k = c/(k+1)$, swept over a 15-point $(h_{\text{target}}, c)$ grid. During development this
literal update rule was found to get permanently trapped at the TTL floor when initialized low
($\text{TTL}_{\text{final}} = 0.01$ from a low initial condition; documented in our harness as
\texttt{dttl\_stuck\_at\_floor\_from\_low\_init}), while remaining well-behaved from a high initial
condition ($\text{TTL}_{\text{final}} = 50.48$) -- we keep this literal implementation exactly as specified
in the source paper and report the failure mode rather than silently patching it.

**EWMA-adaptive (secondary baseline).** Because the literal d-TTL update proved fragile from low initial
conditions, we add a correctly-signed, fixed-step exponentially-weighted-moving-average policy that also
targets a hit rate but recovers from a low initial TTL where d-TTL does not
($\text{TTL}_{\text{final}} = 0.31$ from the same low starting point that traps d-TTL at 0.01), giving a
second, more robust hit-rate-targeted reference point.

**FreshCache-style fitted gate.** A per-site maximum-likelihood exponential staleness-hazard model,
$P(\text{stale}\mid\text{age}) = 1 - e^{-\lambda \cdot \text{age}}$, fit from spot-check outcomes once a
site has accumulated at least $\texttt{min\_obs\_to\_fit}=5$ confirmed observations, gating reuse against a
per-run error budget swept over $\{0.05, 0.1, 0.2\}$. We also implement a partial-pooling variant
(\texttt{FreshCachePooled}) that borrows statistical strength across sites sharing the same resource
volatility-schedule family, as a fairer comparison point for sites with too few individual observations to
fit alone.

## Simulated agent-loop workload

Because ground-truth staleness must be knowable at evaluation time without live re-querying, and real
production agent traces are not accessible to us, we replay a controllable simulated agent-loop tool-call
stream: 60 resources per volatility regime spanning three regime configurations (low volatility: 70%
static / 20% periodic / 10% bursty resources; medium: 35% / 35% / 30%; high: 10% / 30% / 60%, with bursty
event rate and periodic-refresh period tightened correspondingly), 40 episodes of 150 calls each per
regime, Zipf-skewed working-set revisits (repeat bias 0.65) so that call-site recurrence is heavy-tailed
rather than uniform, and a globally monotonic simulated clock shared across episodes so injected version
schedules are consistent [ARTIFACT:art_qtEtMpLZuRGI]. A companion dataset artifact independently builds a
5,307-row versioned resource corpus from exclusively real seed content -- 180 Wikipedia/SQuAD passages
[10], 120 Quora Question Pairs near-duplicate query groups [11], and 50 real Our World in Data population,
coal-energy, and COVID-19 indicator series -- with explicit version schedules and timing-provenance labels
per resource, intended to let downstream experiment code replay a real-content-grounded call stream with
zero live re-querying [ARTIFACT:art_T0onLH9xokqw]. At experiment run time this dataset artifact's output
was not present in the replay harness's workspace, so, per the harness's documented fallback plan, the
reported results in Section 5 use the in-process Zipf-skewed simulator rather than the real-content corpus;
we flag this explicitly as a limitation in Section 6 rather than presenting the two as interchangeable.

# Experiments

## Setup

All five policy families are replayed through *identical* episode traces within each volatility regime,
so any difference in outcomes is attributable to the caching policy alone and not to different underlying
workloads. Replay uses a process pool (150 total (regime, policy, knob) replay jobs, roughly 5.6 seconds of
wall-clock time in total); no LLM or OpenRouter calls are made anywhere in this stage, since the workload is
self-generated and cache-policy decisions do not depend on query text diversity, so the total experiment
cost is $0 [ARTIFACT:art_qtEtMpLZuRGI]. For each (policy, knob, regime) combination we record the overall
cache-hit fraction (redundant-call reduction) and the empirical stale-serve rate (fraction of served hits
whose cached version did not match the ground-truth version active at call time), plus, for the adaptive
policies, the number of confirmed-staleness feedback events consumed before the per-site adapted quantity
(AIMD's window, d-TTL/EWMA's TTL, or FreshCache's fitted hazard) stabilizes.

## Main result: reduction-versus-staleness frontier

[FIGURE:fig_frontier]

Table 1 summarizes the Pareto-dominance analysis: for each volatility regime, we count how many of
AIMD's 12 (hit-rate, stale-rate) operating points are *not* dominated (in the sense of no baseline point
achieving both a higher hit rate and a lower stale rate) by any point from any of the four baseline
policy families.

| Volatility regime | AIMD points | Dominated | Non-dominated fraction |
|---|---|---|---|
| Low | 12 | 8 | 0.333 |
| Medium | 12 | 4 | 0.667 |
| High | 12 | 0 | **1.000** |
| Mean across regimes | -- | -- | **0.667** |

AIMD's frontier position improves monotonically as volatility increases: it is majority-dominated under
low volatility, evenly split under medium volatility, and *fully* non-dominated under high volatility
[ARTIFACT:art_qtEtMpLZuRGI]. This ordering is consistent with the mechanism AIMD is built for -- a
reactive, loss-triggered rule has the most to offer exactly when the environment changes fastest and a
fitted model has the least stable ground to fit on, and the least to offer when a resource barely changes
at all and a wide fixed TTL is already close to free (in the low-volatility regime, fixed TTL alone reaches
0.99 hit rate at only 0.320 stale rate, a point no adaptive policy in our sweep dominates on both axes
simultaneously). Concretely, in the high-volatility regime AIMD's 12 knob settings span hit rates from
0.206 to 0.360 at stale rates from 0.136 to 0.359, while the fitted FreshCache gate spans a narrower,
strictly worse-positioned band (hit rate 0.154-0.355, stale rate 0.076-0.267) and the literal d-TTL
baseline collapses almost entirely (hit rate 0.006-0.071) because its Robbins-Monro update cannot track
the fast-changing target under this regime's short refresh periods.

## Convergence sample-efficiency

[FIGURE:fig_convergence]

The hypothesis's second success criterion required AIMD to stabilize using *substantially fewer*
confirmed-staleness feedback events than the fitted FreshCache gate needs to calibrate. Table 2 reports the
median number of confirmed-staleness-feedback events consumed before each adaptive policy's per-site
adapted quantity enters and stays within a tolerance band, aggregated over the low-repeat-count call-site
bucket (sites visited five or fewer times, the regime this criterion specifically targets)
[ARTIFACT:art_3Kj8hQ_noFpY].

| Policy | Low volatility | Medium volatility | High volatility |
|---|---|---|---|
| d-TTL | 11.0 | 11.0 | 11.0 |
| EWMA-adaptive | 7.5 | 7.75 | 7.0 |
| FreshCache (raw) | 5.0 | 5.0 | 5.0 |
| FreshCache (pooled) | 5.0 | 5.0 | 5.0 |
| **AIMD** | **15.5** | **14.5** | **14.0** |

AIMD is the *slowest* of the five families to reach a stable operating point by this convergence
definition, not the fastest -- the opposite of what the hypothesis's second criterion required. This does
not, however, mean the fitted gates are actually well-calibrated in the low-repeat regime they nominally
"converge" fastest in: FreshCache's own \texttt{calibrated\_fraction} diagnostic (the share of low-repeat
sites for which the exponential hazard fit is judged trustworthy by a Wilson-interval sample-floor check)
is only 0.367 in the low-volatility regime and averages roughly 0.375-0.38 across regimes, meaning the
"5.0-event" convergence figure above reflects a fast but frequently *unreliable* fit rather than a fast and
trustworthy one. An isolated four-observation stress test makes the same point directly: with only four
spot-checked observations at a single site, FreshCache's fitted hazard rate never moves off its 0.1 prior
($\lambda_{\text{final}} = \lambda_{\text{prior}} = 0.1$, \texttt{calibrated=false}), while AIMD's window at
the same site has already moved from its 1.0 initial value to 2.0 [ARTIFACT:art_3Kj8hQ_noFpY]. AIMD is
therefore *responsive* earlier than FreshCache in the truly-sparse regime -- its window visibly changes
after a handful of observations -- but by our uniform tolerance-band stabilization definition (±10% for 10
consecutive updates) it takes more total events to settle into a *stable* range than the coarser adaptive
TTL baselines do, because AIMD's window continues probing upward via additive increase for longer before a
staleness event forces a correction that brings it inside the band. The second success criterion is
therefore not supported in aggregate, though the picture is more nuanced than a simple "slower" verdict:
AIMD moves early but settles late, while FreshCache settles early but frequently on a number it should not
yet trust.

## Boundary sanity checks

We machine-verify four structural properties before trusting the comparative numbers above
[ARTIFACT:art_qtEtMpLZuRGI]. (1) $\text{TTL}=0$ yields exactly 0.0 hit rate, confirming the fixed-TTL
policy never serves from cache with a zero window. (2) $\text{TTL}\to\infty$ (the 0.99 grid point) yields a
0.95 hit rate at 0.0 stale rate in the boundary-check configuration, confirming the workload's inherent
call-repetition ceiling is reachable and that an infinite window is not itself unsafe in a workload with no
version changes. (3) AIMD's window is confirmed to grow on repeated valid hits, collapse on a stale hit,
and recover afterward (all three booleans true), validating the core AIMD mechanic operates as specified
rather than only in aggregate statistics. (4) The literal d-TTL instability documented above
($\text{TTL}_{\text{final}}=0.01$ from a low initial condition versus $50.48$ from a high one) is reproduced
deterministically, confirming it is a property of the Robbins-Monro update itself under this workload and
not a one-off artifact of a particular random seed.

## Ablations

[FIGURE:fig_ablation]

We test AIMD's \texttt{presumed\_valid\_weight} knob -- whether an *unchecked* served hit should be treated
as presumed-valid and allowed to grow the window, versus the conservative default of only moving the
window on spot-checked outcomes. Under low volatility, the conservative default
($\texttt{presumed\_valid\_weight}=0$) reaches a 0.298 hit rate at 0.014 stale rate with a low-repeat
convergence median around 10-15 events, while crediting unchecked hits at weight 0.25 raises the hit rate
to 0.380 at a comparable 0.024 stale rate but pushes the convergence-event median out to 67 -- because
presumed-valid credit lets the window grow past what the sparse spot-check stream can confirm, so more
total events are needed before growth and confirmed correction reach the tolerance band. This is the same
mechanism, at a different knob setting, behind AIMD's slower-than-baseline aggregate convergence in Section
5.3: any AIMD variant that grows its window between confirmations rather than strictly gating growth on
them buys hit rate at the cost of convergence speed, and the credit-unchecked-hits ablation shows this
trade-off is continuous and controllable rather than fixed.

# Discussion

**A genuinely mixed result, not a clean confirmation or refutation.** The hypothesis specified two
independent success criteria, and our evidence splits them: criterion (a), frontier non-domination, holds
with a three-regime mean fraction non-dominated of 0.67, and holds *most strongly precisely where it
matters most* -- full non-domination (1.0) under high volatility, the regime AIMD's reactive design targets.
Criterion (b), substantially faster low-repeat convergence than the fitted probabilistic gate, does not
hold: AIMD's median convergence-event count (14.0-15.5) exceeds both hit-rate-targeted baselines (7.0-11.0)
and nominally exceeds FreshCache's raw 5.0-event figure, though that figure is qualified by FreshCache
achieving genuine statistical calibration on only roughly 37-38% of the low-repeat sites it "converges" on.
Reporting this split honestly is more useful than collapsing it into a single verdict: the paper's
contribution is precisely the finding that a control-theoretic reactive rule earns its simplicity on the
correctness/efficiency trade-off itself, but not on the sample-efficiency axis the design was originally
motivated by, and that these two properties can be decoupled even in a mechanism designed with both in
mind.

**Why AIMD is slow to converge despite being fast to respond.** Section 5.3's four-observation stress test
and the presumed-valid-weight ablation together isolate the mechanism: AIMD's window moves (grows or
shrinks) after every confirmed observation, so it is *responsive* immediately, but our stabilization
definition requires ten consecutive updates within a ±10% tolerance band, and a window that is still
probing upward via additive increase produces exactly the kind of small, repeated movement that
delays entry into such a band. A hit-rate-targeted policy with a decaying step size (d-TTL's
$\gamma_k = c/(k+1)$, or a fixed small EWMA step) settles into a narrow oscillation faster by construction,
at the cost of that oscillation being centered on a target that says nothing about correctness. This
suggests AIMD's convergence-event cost is not an accident of our specific $a, b$ grid but an inherent
property of an additively-growing window under a fixed stabilization tolerance, and that a
faster-decaying additive-increase schedule (mirroring TCP's own slow-start-to-congestion-avoidance
transition, rather than a constant increment $a$ throughout) is a concrete, testable modification for
future work rather than a parameter-tuning afterthought.

**Limitations.** First, and most materially, the reported results were generated by the experiment
harness's in-process Zipf-skewed simulator, not by replaying the real-content-grounded versioned corpus the
dataset artifact built specifically for this purpose: the dataset artifact's 5,307-row corpus of real
Wikipedia/SQuAD passages, Quora Question Pairs, and Our World in Data series was not present in the replay
harness's workspace at run time, and the harness's documented fallback used its built-in synthetic
generator instead [ARTIFACT:art_qtEtMpLZuRGI]. The volatility regimes and call-repetition patterns are
therefore controlled and realistic-by-design rather than drawn from real tool-call text, and the absolute
numbers reported here should be read as characterizing the *policies* under a controllable synthetic
workload, not as characterizing real agent-loop traffic. Second, our independent statistical evaluation
artifact -- built to compute bootstrap confidence intervals, Pareto-frontier AUC, Holm-Bonferroni-corrected
significance tests, and a mechanical CONFIRMS/DISCONFIRMS verdict against the hypothesis's exact success
criteria -- could not run: at evaluation time neither the experiment nor the dataset artifact's outputs
were discoverable in the expected per-call event-log format in their respective workspaces, and the
evaluation script correctly reported a transparent \texttt{BLOCKED\_NO\_DATA} result rather than fabricating
metrics [ARTIFACT:art_3Kj8hQ_noFpY]. All numbers in Section 5 therefore come from the experiment artifact's
own self-reported summary statistics (dominance fractions, convergence-event medians, boundary sanity
checks) computed directly by the replay harness, not from an independently re-derived, confidence-interval-bearing
analysis; we report point estimates without statistical significance testing as a direct consequence, and
the "mean fraction non-dominated 0.67" and convergence-event medians above should be read with that caveat.
Third, our convergence-event stabilization definition (±10% tolerance, 10 consecutive updates) is a single
reasonable choice among several plausible ones, and Section 5.3 shows the ranking between AIMD and the
hit-rate-targeted baselines is sensitive to exactly this kind of definitional choice, since AIMD is
demonstrably more *responsive* by a raw first-movement criterion even where it is slower by the
stabilization criterion. Fourth, our spot-check rate (20%) and low-repeat-context convergence medians are
based on modest per-cell sample sizes (n = 4-15 knob/replicate combinations per regime per policy family),
which is not enough to support fine-grained confidence intervals even had the evaluation artifact been able
to run against real data.

# Conclusion

We tested whether reframing an LLM agent tool cache's per-site reuse window as a TCP-style AIMD congestion
window -- grow additively on confirmed-valid hits, cut multiplicatively on confirmed-stale hits -- would
match or beat both fixed TTL and hit-rate-targeted adaptive TTL on the redundant-call-reduction-versus-staleness
trade-off, while needing substantially fewer confirmed-staleness events than a fitted probabilistic
staleness gate to stabilize. Replayed against an identical, volatility-controlled synthetic agent-loop
tool-call workload across three volatility regimes, AIMD reached a non-dominated point on the
reduction-versus-staleness Pareto frontier for the majority of its knob settings under medium volatility
(8/12) and *all* of its knob settings under high volatility (12/12), confirming the first of the
hypothesis's two success criteria and doing so most strongly in exactly the high-churn regime the
mechanism was designed to help with. The second criterion did not hold: AIMD's median low-repeat
convergence-event count (14.0-15.5) exceeded both the literal d-TTL (11.0) and the corrected EWMA (7.0-7.75)
hit-rate-targeted baselines, even though the fitted FreshCache gate itself achieved genuine statistical
calibration on only 36.7-38.3% of the same low-repeat sites it nominally "converged" on in 5.0 events. The
net picture is that AIMD's reactive, model-free control law buys a genuinely better efficiency/correctness
operating point under volatile conditions, but not the sample-efficiency advantage that motivated importing
it from congestion control in the first place -- a result that argues for decoupling the two properties in
future adaptive-caching designs rather than assuming a reactive rule wins on both fronts.

**Future work:**

- Replay the same five-policy harness against the real-content-grounded versioned corpus built specifically
  for this purpose but not yet consumed by an experiment run, to check whether the mixed result is robust
  to workload realism rather than an artifact of the synthetic Zipf-skewed simulator.
- Re-run the independently built statistical evaluation pipeline (bootstrap CIs, Pareto-AUC, Holm-corrected
  significance tests) once a per-call event log in the expected schema is available, to attach confidence
  intervals and formal significance to the dominance fractions and convergence medians reported here.
- Test a decaying additive-increase schedule for AIMD (mirroring TCP's slow-start-to-congestion-avoidance
  transition) as a direct fix for the convergence-speed shortfall identified in Section 6, rather than a
  constant per-regime increment.
- Extend the volatility-regime sweep with intermediate points between the three tested regimes to locate
  more precisely where AIMD's frontier advantage begins to dominate the fixed-TTL and fitted-gate
  alternatives, since the current three-point sweep shows a monotonic trend but cannot pin down a crossover
  threshold.

# References

[1] S. Basu, A. Sundarrajan, J. Ghaderi, S. Shakkottai, and R. Sitaraman. Adaptive TTL-Based Caching for
Content Delivery. In *Proceedings of the 2017 ACM SIGMETRICS / International Conference on Measurement and
Modeling of Computer Systems*, 2017.

[2] M. Mansoor, T. Ahmad, and Y. Yoon. Risk-Constrained Freshness-Aware Semantic Caching for Open-Web
Retrieval-Augmented LLMs. arXiv preprint arXiv:2607.04281, 2026.

[3] L. G. Schroeder, A. Desai, A. Cuadron, K. Chu, S. Liu, M. Zhao, S. Krusche, A. Kemper, M. Zaharia, and
J. Gonzalez. vCache: Verified Semantic Prompt Caching. arXiv preprint arXiv:2502.03771, 2025.

[4] Anonymous. ToolCacheAgent: Accelerating LLM Agent Through Intelligent Tool Call Caching. OpenReview
preprint, 2026.

[5] A. Vijaya Kumar, B. Kataria, B. Oh, E. A. Manzoor, and R. Singh. TVCACHE: A Stateful Tool-Value Cache
for Post-Training LLM Agents. arXiv preprint arXiv:2602.10986, 2026.

[6] V. Jacobson. Congestion Avoidance and Control. *ACM SIGCOMM Computer Communication Review*, 18(4),
314-329, 1988.

[7] D. Chiu and R. Jain. Analysis of the Increase and Decrease Algorithms for Congestion Avoidance in
Computer Networks. *Computer Networks and ISDN Systems*, 17, 1-14, 1989.

[8] J. Li, C. Xu, F. Wang, I. M. von Riedemann, C. Zhang, and J. Liu. SCALM: Towards Semantic Caching for
Automated Chat Services with Large Language Models. In *2024 IEEE/ACM 32nd International Symposium on
Quality of Service (IWQoS)*, 2024.

[9] F. Bang. GPTCache: An Open-Source Semantic Cache for LLM Applications Enabling Faster Answers and Cost
Savings. In *Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software
(NLP-OSS 2023)*, 2023.

[10] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang. SQuAD: 100,000+ Questions for Machine Comprehension
of Text. In *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing*, 2016.

[11] S. Iyer, N. Dandekar, and K. Csernai. First Quora Dataset Release: Question Pairs. Quora Data blog,
2017.

[12] Our World in Data. Our World in Data Catalog: Population, Energy Mix, and COVID-19 Data.
ourworldindata.org, 2024.
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) The paper's real-content versioned corpus (5,307 rows, built specifically to ground the experiment in real Wikipedia/SQuAD, QQP, and OWID data) was never actually used: per the experiment artifact's own summary, 'no dependency DATASET artifact output was available in the workspace at run time,' so all Section 5 results are generated by the in-process synthetic Zipf simulator. This is disclosed in the Limitations section, but the abstract, contributions list, and Table 1/2 headline numbers are all presented as if they characterize a meaningful empirical finding without that caveat attached at the point of first mention.
  Action: Fix the artifact-wiring bug so the experiment harness actually loads and replays the dataset artifact's full_data_out.json, and re-run Sections 5.1-5.4 against the real-content-grounded call stream. If a full re-run is infeasible in the next iteration, at minimum move the synthetic-workload caveat to the first sentence of the Experiments section and the abstract, rather than leaving it as a Limitations-only disclosure.
- [MAJOR] (rigor) The independently-built statistical evaluation artifact -- which was designed to compute bootstrap 95% CIs, Pareto-frontier AUC, Holm-Bonferroni-corrected significance tests, and a mechanical CONFIRMS/DISCONFIRMS verdict -- never ran against real data and returned a BLOCKED_NO_DATA result. Every number in the paper (0.67 mean non-dominated fraction, 14.0-15.5 median convergence events, 0.367-0.38 FreshCache calibrated fraction) is instead a self-reported summary statistic computed by the same experiment harness that generated the underlying data, with no independent verification and no uncertainty quantification anywhere in the paper.
  Action: Fix the event-log schema mismatch between the experiment artifact's output and what the evaluation artifact expects (episode_id, seed, volatility_regime, call_site_id, timestamp/step_index, policy_name, knob_value, served_from_cache, spot_checked, ground_truth_stale, per-update adapted-value fields), then re-run eval.py so that Tables 1 and 2 report bootstrap CIs and Holm-corrected significance tests rather than bare point estimates.
- [MAJOR] (methodology) All headline comparisons rest on very small per-cell sample sizes: AIMD's 12 (a, b, replicate) knob settings per regime, only a single fixed a=0.25 value ever swept, and convergence-event medians computed over n=4-15 knob/replicate combinations per policy per regime. With this few observations per cell, a 'non-dominated fraction of 0.667' or a '14.0 vs. 11.0' convergence-event difference could easily be within noise, and the paper has no way to check this because of the missing statistical evaluation (see above).
  Action: Either widen the (a, b) sweep (multiple a values, not just a=0.25) and increase the number of independent replicates per knob setting to give the eventual statistical tests real power, or explicitly bound the claims in Section 5/6 to 'directional, not statistically confirmed' language until CIs are available.
- [MINOR] (novelty) The paper asserts 'to our knowledge, no prior work applies this control law to time-based cache reuse windows gated on confirmed staleness feedback in an LLM agent tool-caching setting,' which appears accurate based on the cited related work, but the novelty claim would be strengthened by explicitly addressing why AIMD-style adaptive congestion-window ideas have NOT already been tried for cache TTL adaptation more broadly (i.e., outside the agent setting) -- d-TTL itself is a Robbins-Monro scheme, a different reactive-adaptation family, and the paper does not discuss whether any CDN or database cache literature has tried a literal AIMD rule for TTL before, which is the more directly relevant prior-art question than agent-specific caching alone.
  Action: Add one sentence to Related Work explicitly noting (with a citation search) whether AIMD-style TTL adaptation has been tried in the general (non-agent) adaptive-caching literature, to close this narrower novelty gap rather than leaving the novelty claim scoped only to the agent setting.
- [MINOR] (methodology) The spot-check rate is fixed at 20% throughout the main results (Section 4.1), and while the experiment artifact mentions a 'spot_check_rate sensitivity' ablation, this ablation is not reported or discussed anywhere in the paper text -- yet spot-check density is exactly the resource the paper's own diagnosis (Section 5.4, Discussion) identifies as the bottleneck for AIMD's convergence speed. This ablation is arguably as important to the paper's central 'why does AIMD converge slowly' story as the presumed_valid_weight ablation that IS reported.
  Action: Report the spot-check-rate sensitivity ablation results in Section 5.4 alongside the presumed_valid_weight ablation, since a higher spot-check rate should directly test the paper's own explanation for AIMD's slow convergence (window growth outrunning spot-check density) and would substantially strengthen that mechanistic claim if confirmed.
- [MINOR] (clarity) The dataset artifact's 'metadata_checked' field is described as a '15% random spot-check subsample flag' in the dataset artifact summary, but the paper's Methods section states the spot-check rate is '20% of calls in our harness.' This 15% vs. 20% discrepancy is never reconciled in the paper text and could confuse a reader trying to determine the actual spot-check configuration used for the reported results (especially since Section 4.1 notes the dataset artifact's output was not actually used, so the 15% figure may be entirely moot -- but the paper does not say so).
  Action: Either remove the 15%/20% discrepancy by clarifying that the dataset artifact's 15% spot-check flag is unrelated to the 20% rate actually used in the (fallback synthetic) experiment, or reconcile the two numbers if they are meant to describe the same setting.
- [MINOR] (scope) The paper frames its investigation as testing whether 'a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop' (per the broader research goal), but the experiment never involves an actual LLM agent loop, actual tool calls, or actual LLM/OpenRouter invocations -- it is a fully offline, synthetic replay of a simulated call stream. This is a legitimate and often necessary simplification for controllable staleness ground-truth, but the paper's framing (e.g., 'LLM agent loops... routinely re-issue calls' in the intro) could mislead a reader into expecting some validation against real agent traces, which never appears.
  Action: Add one sentence early in Section 4 (not just in Limitations) clarifying that no live LLM agent, real tool calls, or real agent traces were used anywhere in this study -- the entire evaluation is an offline replay against synthetic and/or corpus-derived call streams -- so readers calibrate expectations about ecological validity from the outset.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
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
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-10 01:23:03 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [4] TOOL CALL — Write · 2026-08-10 01:23:25 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json

{
  "title": "Congestion-Control-Style Cache TTL for Agents",
  "hypothesis": "In an LLM agent loop, treating each tool-call site's cache lifetime as a TCP congestion window -- additively growing the reuse window after every confirmed-valid cache hit, and multiplicatively slashing it after every confirmed-stale hit -- reaches a comparable-or-better redundant-call-reduction-vs-stale-serve-rate operating point than (a) a fixed TTL and (b) target-hit-rate stochastic-approximation TTL adaptation (d-TTL), with the advantage concentrated in and increasing with underlying volatility (fully non-dominated at high volatility, evenly split at medium, majority-dominated at low). This first success criterion now has direct empirical support from a synthetic, volatility-controlled replay harness. The originally hypothesized second advantage -- that AIMD needs far fewer confirmed-staleness feedback events than a fitted probabilistic staleness gate (FreshCache-style) to reach a stable operating point -- is REVISED DOWNWARD to a claim the evidence does not support in aggregate: under a uniform tolerance-band stabilization definition, AIMD's median low-repeat convergence-event count (14.0-15.5) exceeded both a literal d-TTL reimplementation (11.0) and a corrected EWMA hit-rate-targeted baseline (7.0-7.75), and nominally exceeded FreshCache's raw fitted-gate figure (5.0), though that figure reflects fast-but-frequently-untrustworthy calibration (only 36.7-38.3% of low-repeat sites judged genuinely calibrated by a Wilson-interval sample-floor check). The mechanism identified is that AIMD is responsive earlier than the fitted gate (its window visibly moves after a handful of observations, unlike FreshCache which stays pinned to its prior) but settles later, because unbounded additive growth between confirmations keeps producing small movements that delay entry into a stability band -- an inherent property of a constant-increment AIMD schedule under a fixed stabilization tolerance, not a tuning artifact of the specific (a,b) grid tested. Two evidentiary caveats now attach to all of the above and must be resolved before the claims can be treated as robust: (1) the reported results were generated entirely by the experiment harness's in-process synthetic Zipf-skewed simulator because an artifact-wiring bug meant the real-content-grounded versioned corpus (5,307 rows from Wikipedia/SQuAD, Quora Question Pairs, and Our World in Data) was never actually loaded and replayed, despite being purpose-built for this study; (2) the independently-built statistical evaluation pipeline (bootstrap CIs, Pareto-AUC, Holm-corrected significance tests, mechanical CONFIRMS/DISCONFIRMS verdict) never ran against real data due to an event-log schema mismatch between the experiment output and evaluation input, so every number above is a self-reported point estimate from the same harness that generated the data, with no independent uncertainty quantification, and with small per-cell sample sizes (n=4-15 knob/replicate combinations per regime per policy family, only a=0.25 ever swept).",
  "relation_rationale": "Same AIMD-vs-baselines frame; frontier claim narrowed+confirmed directionally, convergence claim reversed by evidence",
  "confidence_delta": "decreased",
  "key_changes": [
    "Split the single combined hypothesis into two explicitly separated claims matching the two success criteria, since evidence now diverges sharply between them",
    "Frontier-non-domination claim (criterion a) upgraded from purely speculative to directionally supported by data, with the volatility-dependence pattern (strongest at high volatility) now stated as a specific, evidence-grounded finding rather than an open question",
    "Sample-efficiency claim (criterion b) reversed from the original hypothesis's expectation: AIMD converges SLOWER than both hit-rate-targeted baselines and the fitted gate's raw event count, not faster; reframed as a genuine negative/mixed finding with the responsive-but-slow-to-stabilize mechanism specified",
    "Added the artifact-wiring bug (synthetic-only data, real corpus never consumed) and the missing independent statistical evaluation (BLOCKED_NO_DATA) as first-class caveats that must be fixed before the claims are robust, per reviewer MAJOR feedback",
    "Flagged small per-cell sample sizes and single-value a=0.25 sweep as a specific methodological gap to widen in the next iteration, per reviewer MAJOR feedback",
    "Noted FreshCache's fast-but-uncalibrated convergence as a qualifying nuance rather than a clean baseline win, since raw event-count comparisons alone are misleading"
  ],
  "relation_type": "evolution",
  "artifact_relations": []
}
```

### [5] TOOL RESULT — Write · 2026-08-10 01:23:25 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Congestion-Control-Style Cache TTL for Agents\",\n  \"hypothesis\": \"In an LLM agent loop, treating each tool-call site's cache lifetime as a TCP congestion window -- additively growing the reuse window after every confirmed-valid cache hit, and multiplicatively slashing it after every confirmed-stale hit -- reaches a comparable-or-better redundant-call-reduction-vs-stale-serve-rate operating point than (a) a fixed TTL and (b) target-hit-rate stochastic-approximation TTL adaptation (d-TTL), with the advantage concentrated in and increasing with underlying volatility (fully non-dominated at high volatility, evenly split at medium, majority-dominated at low). This first success criterion now has direct empirical support from a synthetic, volatility-controlled replay harness. The originally hypothesized second advantage -- that AIMD needs far fewer confirmed-staleness feedback events than a fitted probabilistic staleness gate (FreshCache-style) to reach a stable operating point -- is REVISED DOWNWARD to a claim the evidence does not support in aggregate: under a uniform tolerance-band stabilization definition, AIMD's median low-repeat convergence-event count (14.0-15.5) exceeded both a literal d-TTL reimplementation (11.0) and a corrected EWMA hit-rate-targeted baseline (7.0-7.75), and nominally exceeded FreshCache's raw fitted-gate figure (5.0), though that figure reflects fast-but-frequently-untrustworthy calibration (only 36.7-38.3% of low-repeat sites judged genuinely calibrated by a Wilson-interval sample-floor check). The mechanism identified is that AIMD is responsive earlier than the fitted gate (its window visibly moves after a handful of observations, unlike FreshCache which stays pinned to its prior) but settles later, because unbounded additive growth between confirmations keeps producing small movements that delay entry into a stability band -- an inherent property of a constant-increment AIMD schedule under a fixed stabilization tolerance, not a tuning artifact of the specific (a,b) grid tested. Two evidentiary caveats now attach to all of the above and must be resolved before the claims can be treated as robust: (1) the reported results were generated entirely by the experiment harness's in-process synthetic Zipf-skewed simulator because an artifact-wiring bug meant the real-content-grounded versioned corpus (5,307 rows from Wikipedia/SQuAD, Quora Question Pairs, and Our World in Data) was never actually loaded and replayed, despite being purpose-built for this study; (2) the independently-built statistical evaluation pipeline (bootstrap CIs, Pareto-AUC, Holm-corrected significance tests, mechanical CONFIRMS/DISCONFIRMS verdict) never ran against real data due to an event-log schema mismatch between the experiment output and evaluation input, so every number above is a self-reported point estimate from the same harness that generated the data, with no independent uncertainty quantification, and with small per-cell sample sizes (n=4-15 knob/replicate combinations per regime per policy family, only a=0.25 ever swept).\",\n  \"relation_rationale\": \"Same AIMD-vs-baselines frame; frontier claim narrowed+confirmed directionally, convergence claim reversed by evidence\",\n  \"confidence_delta\": \"decreased\",\n  \"key_changes\": [\n    \"Split the single combined hypothesis into two explicitly separated claims matching the two success criteria, since evidence now diverges sharply between them\",\n    \"Frontier-non-domination claim (criterion a) upgraded from purely speculative to directionally supported by data, with the volatility-dependence pattern (strongest at high volatility) now stated as a specific, evidence-grounded finding rather than an open question\",\n    \"Sample-efficiency claim (criterion b) reversed from the original hypothesis's expectation: AIMD converges SLOWER than both hit-rate-targeted baselines and the fitted gate's raw event count, not faster; reframed as a genuine negative/mixed finding with the responsive-but-slow-to-stabilize mechanism specified\",\n    \"Added the artifact-wiring bug (synthetic-only data, real corpus never consumed) and the missing independent statistical evaluation (BLOCKED_NO_DATA) as first-class caveats that must be fixed before the claims are robust, per reviewer MAJOR feedback\",\n    \"Flagged small per-cell sample sizes and single-value a=0.25 sweep as a specific methodological gap to widen in the next iteration, per reviewer MAJOR feedback\",\n    \"Noted FreshCache's fast-but-uncalibrated convergence as a qualifying nuance rather than a clean baseline win, since raw event-count comparisons alone are misleading\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": []\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-08-10 01:23:27 UTC

```
Revised hypothesis written. Key change: split the original single claim into two — the frontier-non-domination claim now has direct (if synthetic-only) empirical support, strongest at high volatility, while the sample-efficiency claim is reversed: AIMD converged *slower* than baselines in aggregate, not faster as originally hypothesized. Flagged the unfixed artifact-wiring bug (real corpus never used) and missing independent statistical evaluation as blocking caveats for the next iteration.
```
