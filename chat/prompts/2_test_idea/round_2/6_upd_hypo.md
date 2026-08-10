# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-08-10 04:55:06 UTC

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

--- Item 4 ---
id: art_tceB4eOwcBAO
type: experiment
in_dependencies:
- id: art_T0onLH9xokqw
  label: dataset
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

--- Item 5 ---
id: art_tXld0p2SGjtU
type: evaluation
in_dependencies:
- id: art_qtEtMpLZuRGI
  label: experiment
- id: art_T0onLH9xokqw
  label: dataset
title: Statistical Re-Check of AIMD Cache Results
summary: >-
  This evaluation independently re-verifies every self-reported number in the AIMD-vs-TTL/d-TTL/EWMA/FreshCache cache-policy
  experiment (art_qtEtMpLZuRGI) using eval.py. It imports method.py directly, reproduces its exact simulator and seeds, and
  replays the full 150-cell (regime x policy_family x knob) grid with per-episode instrumentation (method_out.json only stored
  per-run aggregates, so per-episode granularity had to be re-derived from the raw generative process rather than bootstrapped
  from an aggregate). It computes episode-level bootstrap 95% CIs (n=10,000 resamples) on hit_rate/stale_rate for all 150
  cells, Pareto-frontier trapezoidal AUC and a bootstrap-CI'd non-dominated-fraction per regime, convergence-event median/p10/p90
  CIs plus Wilson-CI'd FreshCache calibrated fractions, and 27 Holm-Bonferroni-corrected paired significance tests (AIMD vs
  each baseline, per regime, on frontier AUC and convergence-event count, with automatic fallback to paired bootstrap difference-of-medians
  when n<6 for Wilcoxon validity). A full sample-size audit accompanies every cell (all 150 had n=40 episodes, none flagged
  low-confidence). Two concrete, previously undocumented bugs were found and root-caused during cross-validation against the
  original method_raw.json per-run results: (1) a genuine dataset-wiring bug -- method.py never references full_data_out.json/mini_data_out.json
  anywhere in its source (confirmed by direct string grep), so the real-content corpus (art_T0onLH9xokqw) never entered the
  evaluated event log at all; a field-by-field schema-compatibility table documents exactly what a real re-run would need
  (chiefly: mapping the dataset's string version_id ground truth to method.py's integer schedule-index via the resource's
  version_schedule intervals). (2) A seed-reproducibility bug: method.py seeds each replay job with hash((regime,family,kidx))
  % 2**31, but Python's hash() of str/tuple objects is randomized per-process (PYTHONHASHSEED unset), so AIMD/FreshCache/FreshCachePooled
  (whose state updates are gated on the stochastic spot-check flag) cannot be bit-reproduced across separate process runs,
  while FixedTTL/d-TTL/EWMA (which update unconditionally every call) are seed-invariant and matched the original run's numbers
  exactly to 1e-9 -- this was isolated as the root cause by checking which families mismatched and confirming it against the
  theory. An ecological-validity proxy comparison against the real corpus's actual version_schedule and revisit statistics
  found the real corpus is heavily static-dominated (84.8% of 329 resources, only 1.5% bursty), which sits inside the synthetic
  low_volatility regime's parameters but is far less volatile than the synthetic medium/high_volatility regimes -- meaning
  the strongest synthetic evidence for AIMD's frontier advantage comes from the regime least representative of the real corpus.
  Final mechanical verdicts: criterion (a) frontier non-domination DISCONFIRMS on this re-derived synthetic run (mean non-dominated
  fraction 0.0, CIs including zero in all three regimes -- a materially different, less favorable, result than method_out.json's
  self-reported 0.67, illustrating exactly why independent CIs matter); criterion (b) low-repeat convergence speed + FreshCache
  calibration failure is MIXED (AIMD was slower than baselines in all 3 regimes, but FreshCache's calibrated fraction was
  genuinely low with tight CIs, supporting that half). Both criteria's real-content robustness is explicitly marked UNRESOLVED_BLOCKED_ON_REEXECUTION
  given the confirmed wiring bug. Outputs are eval.py (the complete evaluation script) and eval_out.json (full/mini/preview
  variants), schema-validated against exp_eval_sol_out.json, containing 9 dataset groups: schema_diff_report, seed_reproducibility_finding,
  episode_bootstrap_cells (150), frontier_auc_dominance (21), convergence_event_ci (18), significance_tests_holm_corrected
  (27), ecological_validity_proxy, sample_size_audit (150), and final_verdicts.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

--- Item 6 ---
id: art_iY6kMoc-uEE6
type: research
title: Has AIMD TTL Adaptation Been Done Before Agents?
summary: >-
  This research artifact closes the paper's remaining novelty gap around AIMD-for-cache-TTL by systematically searching CDN,
  database/materialized-view, DNS, and browser/HTTP caching literature (scholarly + general web search across nine query angles,
  plus full-text PDF grep) for prior work applying a literal additive-increase/multiplicative-decrease control law to cache
  TTL, freshness, or expiration outside the LLM-agent setting. It confirms and precisely characterizes the two near-hits flagged
  during planning -- ClepsydraCache (Thoma et al., USENIX Security 2023, arXiv:2104.11469), whose authors themselves state
  their TTL-reduction-rate schedule 'is comparable to TCP congestion control', triggered by hardware security conflicts not
  content staleness; and Vincent Cate's 1992 Alex filesystem / RFC 7234 heuristic freshness, an age-proportional (not loss-event-reactive)
  TTL rule -- and surfaces one new, more directly relevant hit not in the original plan: Concur (Chen et al., ICML 2025, arXiv:2601.22705),
  which applies genuine two-sided AIMD INSIDE an LLM-agent inference-serving system, but to admission control of concurrent
  agents gated on KV-cache pressure, never to any object's TTL or content freshness. d-TTL/f-TTL (Basu et al., SIGMETRICS
  2017) and FreshCache (Mansoor et al., arXiv:2607.04281) are confirmed via full-text grep and abstract review to use non-AIMD
  control laws (Robbins-Monro stochastic approximation and a fitted probabilistic gate, respectively). No hit was found in
  database materialized-view, DNS, or browser/HTTP caching literature. The deliverable is a citation-backed Related Work paragraph
  narrowing the paper's novelty claim: no prior work applies AIMD to a per-object/per-call-site TTL triggered by confirmed
  content staleness in any caching domain surveyed, and the one genuine within-agent-setting AIMD precedent (Concur) targets
  a categorically different variable (concurrency admission, not freshness) -- strengthening rather than undermining the paper's
  positioning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

id: art_tceB4eOwcBAO
type: experiment
in_dependencies:
- id: art_T0onLH9xokqw
  label: dataset
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

id: art_tXld0p2SGjtU
type: evaluation
in_dependencies:
- id: art_qtEtMpLZuRGI
  label: experiment
- id: art_T0onLH9xokqw
  label: dataset
title: Statistical Re-Check of AIMD Cache Results
summary: >-
  This evaluation independently re-verifies every self-reported number in the AIMD-vs-TTL/d-TTL/EWMA/FreshCache cache-policy
  experiment (art_qtEtMpLZuRGI) using eval.py. It imports method.py directly, reproduces its exact simulator and seeds, and
  replays the full 150-cell (regime x policy_family x knob) grid with per-episode instrumentation (method_out.json only stored
  per-run aggregates, so per-episode granularity had to be re-derived from the raw generative process rather than bootstrapped
  from an aggregate). It computes episode-level bootstrap 95% CIs (n=10,000 resamples) on hit_rate/stale_rate for all 150
  cells, Pareto-frontier trapezoidal AUC and a bootstrap-CI'd non-dominated-fraction per regime, convergence-event median/p10/p90
  CIs plus Wilson-CI'd FreshCache calibrated fractions, and 27 Holm-Bonferroni-corrected paired significance tests (AIMD vs
  each baseline, per regime, on frontier AUC and convergence-event count, with automatic fallback to paired bootstrap difference-of-medians
  when n<6 for Wilcoxon validity). A full sample-size audit accompanies every cell (all 150 had n=40 episodes, none flagged
  low-confidence). Two concrete, previously undocumented bugs were found and root-caused during cross-validation against the
  original method_raw.json per-run results: (1) a genuine dataset-wiring bug -- method.py never references full_data_out.json/mini_data_out.json
  anywhere in its source (confirmed by direct string grep), so the real-content corpus (art_T0onLH9xokqw) never entered the
  evaluated event log at all; a field-by-field schema-compatibility table documents exactly what a real re-run would need
  (chiefly: mapping the dataset's string version_id ground truth to method.py's integer schedule-index via the resource's
  version_schedule intervals). (2) A seed-reproducibility bug: method.py seeds each replay job with hash((regime,family,kidx))
  % 2**31, but Python's hash() of str/tuple objects is randomized per-process (PYTHONHASHSEED unset), so AIMD/FreshCache/FreshCachePooled
  (whose state updates are gated on the stochastic spot-check flag) cannot be bit-reproduced across separate process runs,
  while FixedTTL/d-TTL/EWMA (which update unconditionally every call) are seed-invariant and matched the original run's numbers
  exactly to 1e-9 -- this was isolated as the root cause by checking which families mismatched and confirming it against the
  theory. An ecological-validity proxy comparison against the real corpus's actual version_schedule and revisit statistics
  found the real corpus is heavily static-dominated (84.8% of 329 resources, only 1.5% bursty), which sits inside the synthetic
  low_volatility regime's parameters but is far less volatile than the synthetic medium/high_volatility regimes -- meaning
  the strongest synthetic evidence for AIMD's frontier advantage comes from the regime least representative of the real corpus.
  Final mechanical verdicts: criterion (a) frontier non-domination DISCONFIRMS on this re-derived synthetic run (mean non-dominated
  fraction 0.0, CIs including zero in all three regimes -- a materially different, less favorable, result than method_out.json's
  self-reported 0.67, illustrating exactly why independent CIs matter); criterion (b) low-repeat convergence speed + FreshCache
  calibration failure is MIXED (AIMD was slower than baselines in all 3 regimes, but FreshCache's calibrated fraction was
  genuinely low with tight CIs, supporting that half). Both criteria's real-content robustness is explicitly marked UNRESOLVED_BLOCKED_ON_REEXECUTION
  given the confirmed wiring bug. Outputs are eval.py (the complete evaluation script) and eval_out.json (full/mini/preview
  variants), schema-validated against exp_eval_sol_out.json, containing 9 dataset groups: schema_diff_report, seed_reproducibility_finding,
  episode_bootstrap_cells (150), frontier_auc_dominance (21), convergence_event_ci (18), significance_tests_holm_corrected
  (27), ecological_validity_proxy, sample_size_audit (150), and final_verdicts.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json

id: art_iY6kMoc-uEE6
type: research
title: Has AIMD TTL Adaptation Been Done Before Agents?
summary: >-
  This research artifact closes the paper's remaining novelty gap around AIMD-for-cache-TTL by systematically searching CDN,
  database/materialized-view, DNS, and browser/HTTP caching literature (scholarly + general web search across nine query angles,
  plus full-text PDF grep) for prior work applying a literal additive-increase/multiplicative-decrease control law to cache
  TTL, freshness, or expiration outside the LLM-agent setting. It confirms and precisely characterizes the two near-hits flagged
  during planning -- ClepsydraCache (Thoma et al., USENIX Security 2023, arXiv:2104.11469), whose authors themselves state
  their TTL-reduction-rate schedule 'is comparable to TCP congestion control', triggered by hardware security conflicts not
  content staleness; and Vincent Cate's 1992 Alex filesystem / RFC 7234 heuristic freshness, an age-proportional (not loss-event-reactive)
  TTL rule -- and surfaces one new, more directly relevant hit not in the original plan: Concur (Chen et al., ICML 2025, arXiv:2601.22705),
  which applies genuine two-sided AIMD INSIDE an LLM-agent inference-serving system, but to admission control of concurrent
  agents gated on KV-cache pressure, never to any object's TTL or content freshness. d-TTL/f-TTL (Basu et al., SIGMETRICS
  2017) and FreshCache (Mansoor et al., arXiv:2607.04281) are confirmed via full-text grep and abstract review to use non-AIMD
  control laws (Robbins-Monro stochastic approximation and a fitted probabilistic gate, respectively). No hit was found in
  database materialized-view, DNS, or browser/HTTP caching literature. The deliverable is a citation-backed Related Work paragraph
  narrowing the paper's novelty claim: no prior work applies AIMD to a per-object/per-call-site TTL triggered by confirmed
  content staleness in any caching domain surveyed, and the one genuine within-agent-setting AIMD precedent (Concur) targets
  a categorically different variable (concurrency admission, not freshness) -- strengthening rather than undermining the paper's
  positioning.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

LLM agent loops -- an LLM repeatedly invoking tools (file reads, web search, code execution, retrieval)
inside a control loop that observes each result and decides the next action -- routinely re-issue calls
whose arguments exactly or near-exactly match a call already made earlier in the same episode. An agent
re-reads a file it opened three turns ago to re-check a detail, re-runs a search query it already ran with
a slightly reworded phrasing, or recomputes an aggregate statistic it already derived. Caching these calls
is an obvious latency and cost win, but it introduces a correctness risk that plain LRU or fixed-TTL
request caching does not confront directly: if the underlying resource has changed since it was cached,
the agent silently reasons over stale content, and because the agent has no external signal telling it the
cache lied, the error propagates into everything downstream of that tool call. To be direct about scope
from the outset: no live LLM agent, real tool invocation, or production agent trace is used anywhere in
this study -- every result below comes from an offline replay of either a controllable synthetic call
stream or a versioned corpus built from real seed content but injected with an explicit, known version
schedule, precisely so that staleness ground truth can be scored without any live re-querying. The central
design question for agent-side tool caching is therefore not "how do we maximize the hit rate" but "how do
we maximize the hit rate *subject to* keeping the fraction of stale-serves low," and doing so per call
site, since different tool-call sites in the same agent episode change at wildly different rates -- a
static reference document, a periodically-refreshed dataset, and a rapidly-changing live metric all appear
in the same trace but demand different reuse policies.

This tradeoff is interesting and important because it sits directly on the cost/latency-versus-correctness
frontier that determines whether tool caching is safe to deploy in agent systems at all: aggressive caching
that ignores staleness saves calls but corrupts the agent's world model, while conservative caching that
never reuses anything forfeits the savings caching exists to provide. It is hard because the right reuse
window for a given call site is neither known in advance (volatility is a property of the underlying
resource, not something the agent framework can inspect) nor stationary, so a caching policy has to *learn*
the right window from observed outcomes, online, per site, cheaply.

It has not been solved by existing adaptive-caching mechanisms for two different reasons. The strongest
adaptive-TTL result from content-delivery research, d-TTL [1], uses a Robbins-Monro stochastic-approximation
update to converge a per-object TTL toward a *target hit rate*; this objective has no notion of correctness
at all -- it optimizes for how often a cached value is served, not for whether that value was still valid
when served, which is exactly backwards for a safety-relevant agent tool call. The strongest staleness-
*aware* caches, FreshCache [2] and vCache [3], instead fit an explicit probabilistic staleness or
match-correctness model per cached entry and gate reuse against a fixed error budget; this directly targets
correctness, but the fit requires enough labeled calibration observations per entry to be trustworthy,
which is precisely what is scarce in agent loops, where a given call-site signature is often seen only a
handful of times in an episode. Nearer-term agent-specific caches sidestep the staleness question
altogether: ToolCacheAgent [4] assigns each tool a static caching plan once, from the tool's semantics, and
never updates it from observed outcomes; TVCACHE [5] caches by exact trajectory-prefix match, which has no
notion of graded, time-based staleness at all.

We investigate a third option, taken directly from a different field that solved a structurally similar
problem: TCP congestion control's additive-increase, multiplicative-decrease (AIMD) rule [6, 7] adapts a
resource-usage window under noisy, sparse, delayed feedback about an unknown, shifting environment, without
ever fitting a model of that environment. We reframe a confirmed-stale cache hit as the "loss event" AIMD
reacts to: each call site keeps a reuse window that grows additively by a fixed increment after every
confirmed-valid spot-checked hit, and is cut multiplicatively after every confirmed-stale spot-checked hit.
A systematic literature search across CDN, database materialized-view, DNS, and browser/HTTP caching
literature, described in full in Section 2, confirms that no prior work in any of these domains applies
this loss-event-triggered AIMD control law to an object's time-to-live or freshness window, including the
two closest non-agent near-hits (a security-conflict-triggered AIMD-shaped eviction schedule, and an
age-proportional, non-reactive freshness heuristic) [8, 9, 10]. [FIGURE:fig_architecture]

The present iteration of this investigation is, in large part, a story about what happens when a claimed
result is independently checked rather than taken at self-reported face value -- a discipline the previous
iteration's reviewer explicitly demanded. The prior iteration built a versioned, volatility-labeled
tool-call corpus and a five-policy replay harness, but two dependency bugs meant its headline claim (AIMD
non-dominated on 8/12 and 12/12 knob settings at medium and high volatility) was generated entirely by an
in-process synthetic simulator, never by the purpose-built real-content corpus, and was never independently
re-verified with confidence intervals. This iteration fixes both problems and reports what changes as a
result: with the wiring bug fixed and the real corpus actually loaded, AIMD is Pareto-dominated by a fitted
staleness gate on real data; and with the statistics independently re-derived with bootstrap confidence
intervals, the previous iteration's own self-reported 0.67 mean non-dominated fraction collapses to 0.0.
We report this reversal in full, including the two concrete bugs responsible for the discrepancy, because a
caching policy's practical value is exactly the kind of claim that should not survive on a single
self-reported number.

**Summary of Contributions**

- A real-data cache-policy replay experiment that fixes the previous iteration's silent dataset-wiring
  failure with a loud fail-fast dependency loader, widens the AIMD knob grid threefold (from 3 to 9
  (a, b) combinations), and runs a matched real-corpus-vs-synthetic-simulator comparison for all six
  policy families: on the real corpus, AIMD (hit rate 0.794-0.803, stale rate 0.106-0.109 across its full
  grid) is dominated outright by FreshCache (hit rate 0.898-0.906, stale rate 0.096-0.112) and matched, not
  beaten, by the much simpler EWMA-adaptive baseline (hit rate 0.797-0.799 at stale rate 0.106-0.107)
  (Section 4) [ARTIFACT:art_tceB4eOwcBAO].
- An independent, bootstrap-CI'd, Holm-Bonferroni-corrected statistical re-derivation of the previous
  iteration's synthetic replay that overturns its own self-reported result: mean non-dominated fraction
  falls from a self-reported 0.67 to an independently re-derived 0.0, with 95% confidence intervals
  excluding majority non-domination in all three volatility regimes, and that traces the discrepancy to
  two concrete, previously undocumented bugs -- a confirmed dataset-wiring failure and a seed-
  reproducibility failure from unset `PYTHONHASHSEED` affecting exactly the three stochastic policy
  families (AIMD, FreshCache, FreshCache-pooled) and none of the deterministic ones (Section 5.1)
  [ARTIFACT:art_tXld0p2SGjtU].
- A resolved account of AIMD's convergence-speed shortfall, now with confidence intervals and an
  ecological-validity check: AIMD's median low-repeat convergence-event count (12.0-16.0 across regimes,
  95% CI up to 27.0 in high volatility) remains slower than d-TTL (11.0-12.0), EWMA (7.0-8.0), and
  FreshCache's raw 5.0-event figure, even though FreshCache's own calibrated fraction is a tightly-bounded
  0.29-0.41 across regimes -- and an ecological-validity proxy against the real corpus's actual
  version-change statistics (329 resources, 84.8% static, 1.5% bursty) shows that only the *low*-volatility
  synthetic regime resembles the real corpus at all, so the high-volatility regime where AIMD looked
  strongest is also the regime least representative of real agent-tool traffic (Section 5.2)
  [ARTIFACT:art_tXld0p2SGjtU].
- A systematic non-agent-domain literature search (CDN, database materialized-view, DNS, browser/HTTP
  caching) confirming no prior work applies a confirmed-staleness-triggered AIMD control law to per-object
  TTL in any of these domains, precisely characterizing the two closest near-hits and one new closer-in-spirit
  hit inside LLM-agent serving that targets a different control variable, closing the paper's remaining
  novelty gap (Section 2) [ARTIFACT:art_iY6kMoc-uEE6].

# Related Work

**Hit-rate-targeted adaptive TTL.** Basu et al.'s d-TTL and f-TTL [1] adapt a per-object TTL toward a
target cache hit rate using a Robbins-Monro stochastic-approximation update, with provable convergence
demonstrated on a 500M+ request CDN trace. The objective is entirely hit-rate-based: nothing in the update
rule depends on whether a served hit was actually still valid. We reimplement d-TTL literally, port it to
per-call-site agent traffic, and compare against it directly.

**Fitted probabilistic staleness gating.** FreshCache [2] fits an exponential-decay-plus-MLP
staleness-probability model per cached entry/tier and gates reuse against a fixed per-tier error budget,
evaluated on 8,072-31,201 real open-web RAG queries, reporting 97-98% search savings at 0.1-3.3%
stale-serve error. This is the closest prior mechanism to what we study, but the model must be fit from a
substantial labeled calibration set per entry class, and the present work targets exactly the regime
(per-call-site agent tool caching, low repeat counts) where that calibration set is thin. vCache [3] is a
related online Bayesian learning algorithm for semantic *match*-correctness rather than time-based
staleness. We reimplement FreshCache's fitted-gate mechanism in both a raw per-site variant and a
partial-pooling-by-resource-schedule-family variant as the calibrated-model reference point.

**Semantic and agent-specific tool caching.** GPTCache [16] and SCALM [17] popularize semantic
similarity caching for LLM query/response pairs, matching near-duplicate prompts rather than tracking
time-based staleness. ToolCacheAgent [4] uses an LLM planner to assign each tool a static caching plan once
from the tool's semantics, but the plan never updates from observed outcomes during execution. TVCACHE [5]
caches by exact longest-prefix match over the full preceding tool-call trajectory, targeting RL
post-training rollouts with high trajectory overlap, with no graded notion of time-based staleness at all.
Neither addresses the online, per-site, outcome-driven adaptation this paper studies.

**Congestion control as a reactive control law, and whether AIMD-for-TTL has been tried before.** AIMD is
the core mechanism of TCP congestion avoidance [6, 7]: additively probe for more bandwidth on success,
multiplicatively retreat on a detected loss event, converging toward an efficient operating point without a
model of the network. This iteration closes a novelty gap the previous iteration's reviewer flagged: does
AIMD-style adaptation for cache TTL exist outside the agent setting, since d-TTL itself is a different
reactive-adaptation family (Robbins-Monro, not AIMD)? A systematic search across CDN, database
materialized-view, DNS, and browser/HTTP caching literature (nine query angles across scholarly and general
search, plus full-text PDF grep of the two most load-bearing candidates) surfaces two genuine near-hits and
one closer-in-spirit hit, none of which pre-empt this paper's claim [11]. ClepsydraCache [8] is the closest
non-agent near-hit: its authors state their global TTL-reduction-rate schedule "is comparable to TCP
congestion control," slowly decaying between hardware cache-set conflicts and sharply increasing upon one,
but the triggering event is a security side-channel conflict, not confirmed content staleness, and the
adaptation is global rather than per-object. Cate's 1992 Alex filesystem and its descendant, RFC 7234's
heuristic freshness rule [9, 10], adapt TTL as a function of a file's own age (commonly 10% of
time-since-last-modified, as implemented by production browsers), but this is proportional-to-age control
with no loss-event feedback loop at all -- there is no "bad outcome" that triggers a cut. Full-text grep of
the d-TTL PDF for AIMD/additive/multiplicative/congestion/TCP returns zero matches, confirming its
Robbins-Monro update is not framed as, or related to, AIMD in the original source. Database materialized-view
refresh, DNS TTL adaptation, and browser/HTTP caching literature surface no AIMD-framed prior art at all.
One new, more directly relevant hit -- not anticipated when this investigation began -- surfaces inside the
LLM-agent-serving literature itself: Concur [12] applies genuine two-sided AIMD inside an agentic
batch-inference server, additively growing the number of concurrently admitted agents when KV-cache
pressure is low and multiplicatively cutting it when pressure is high and the hit rate degrades, to prevent
cascading cache-eviction thrashing. Concur establishes that AIMD is already a live control pattern in
exactly this research community, but for agent-level admission/concurrency control gated on aggregate
capacity pressure, never for any single object's TTL or per-call-site freshness -- an orthogonal control
variable to the one this paper studies. To our knowledge, and now confirmed against non-agent caching
domains specifically rather than only the agent setting, no prior work applies a confirmed-staleness-triggered
AIMD control law to a per-object or per-call-site TTL, in any caching domain surveyed.

# Methods

## Problem setup

Each tool-call *site* is a (function, argument-signature) pair; every time the agent loop issues a call
matching a previously cached site, a cache policy must decide whether to serve the cached result or
re-execute the call. A subset of served hits is *spot-checked* -- a live re-query is issued in the
background and diffed against the cached value, producing a binary confirmed-valid / confirmed-stale label
for that hit -- mirroring the same kind of after-the-fact ground-truth signal that FreshCache and vCache
also require to calibrate, so no policy in our comparison gets access to more raw information than any
other; they differ only in how they *use* it. This iteration's real-data experiment sweeps the spot-check
rate itself over {0.10, 0.20, 0.40} with a 0.20 headline rate, as a policy-external configuration parameter
of the replay harness, independent of and not to be confused with the versioned-corpus dataset's own
`metadata_checked` field -- a static 15% random-subsample flag baked into each dataset row at construction
time for a different purpose (simulating partial verification coverage of the dataset itself). The two
numbers previously appeared side by side without reconciliation; they describe unrelated things, and only
the harness's own spot-check-rate parameter governs what any policy in our replay actually observes.

## AIMD reuse-window policy (proposed)

Each call site $i$ maintains a reuse window $w_i$ (initialized to $w_{\text{init}}=1.0$, bounded to
$[w_{\min}, w_{\max}] = [0.01, 10^4]$ simulated ticks). A call at site $i$ at time $t$ is served from cache
if a cached value exists and $t - t_{\text{cached}} \le w_i$; otherwise the call is re-executed and the
result is (re-)cached. When a served hit is spot-checked and confirmed valid, the window grows additively,
$w_i \leftarrow \min(w_i + a,\, w_{\max})$; when a served hit is spot-checked and confirmed stale, the
window collapses multiplicatively, $w_i \leftarrow \max(w_i \cdot b,\, w_{\min})$, with $b < 1$. Unchecked
hits do not move the window ($\texttt{presumed\_valid\_weight}=0$ by default), with an ablation testing
partial credit for unchecked hits. This iteration widens the grid the previous iteration used ($a=0.25$
paired with $b\in\{0.3,0.5,0.7\}$, 12 knob settings) to $a\in\{0.1,0.25,0.5\}\times b\in\{0.5,0.7,0.9\}$, a
9-point grid run against 20 replicate seeds per (data source, spot-check rate) cell, directly responding to
the previous reviewer's methodology critique that a single fixed $a$ under-powers any eventual statistical
comparison [ARTIFACT:art_tceB4eOwcBAO].

## Baseline policies

**Fixed TTL.** A single, non-adapting time-to-live applied uniformly to every call site, swept over
$\text{TTL}\in\{1,3,7,14,30\}$ simulated days on real-corpus data (with a 9-point boundary-probing grid
including TTL=0 and TTL$\to\infty$ used in the earlier synthetic-only boundary sanity checks).

**d-TTL.** A literal reimplementation of Basu et al.'s [1] Robbins-Monro stochastic-approximation update,
swept over $h_{\text{target}}\in\{0.5,0.7,0.9\}$. This literal update rule was found in the previous
iteration to get permanently trapped at the TTL floor when initialized low, a failure mode we continue to
report rather than silently patch.

**EWMA-adaptive (secondary baseline).** A correctly-signed, fixed-step exponentially-weighted-moving-average
policy that also targets a hit rate, swept over $\alpha\in\{0.1,0.3,0.5\}$, and recovers from a low initial
TTL where d-TTL does not.

**FreshCache-style fitted gate.** A per-site maximum-likelihood exponential staleness-hazard model,
$P(\text{stale}\mid\text{age}) = 1 - e^{-\lambda \cdot \text{age}}$, fit from spot-check outcomes once a
site has accumulated at least 5 confirmed observations, gating reuse against a per-run error budget swept
over $\{0.10, 0.20, 0.35\}$, in both a raw per-site variant and a resource-class-partial-pooling variant
(\texttt{FreshCachePooled}) that borrows statistical strength across sites sharing the same resource
volatility-schedule family.

All six policies share one `PolicyBase` decide/update interface keyed by call-site signature, so the only
difference between methods is the adaptation rule itself, eliminating implementation confounds
[ARTIFACT:art_tceB4eOwcBAO].

## Workload: real corpus and matched synthetic simulator

This iteration's central methodological fix is loading the real-content-grounded versioned corpus that the
previous iteration built but never consumed. A companion dataset artifact independently constructed a
5,307-row versioned resource corpus from exclusively real seed content -- 180 Wikipedia/SQuAD passages [13],
120 Quora Question Pairs near-duplicate query groups [14], and 50 real Our World in Data population,
coal-energy, and COVID-19 indicator series [15] -- with explicit version schedules and timing-provenance
labels per resource, replayed across 30 episodes with three documented, deterministic repetition templates
(read-then-reread, search-then-refine, compute-then-reuse) [ARTIFACT:art_T0onLH9xokqw]. The previous
iteration's experiment code never referenced this file at all -- confirmed by direct string grep of its
source in the independent re-verification below -- so every result it reported came from an in-process
synthetic Zipf-skewed simulator instead, silently. This iteration's `method.py` fixes that with a *loud*
fail-fast dependency loader: it asserts the corpus file exists and contains at least 5,000 rows, aborting
hard rather than silently substituting synthetic data if the assertion fails, and parses each row's JSON
input and version-schedule fields into per-episode call streams and per-resource ground-truth version
schedules [ARTIFACT:art_tceB4eOwcBAO]. The dependency loader's own metadata confirms the corpus was
actually read at experiment run time (`n_rows_loaded: 5307`), unlike the previous iteration's silent
fallback. An explicit synthetic Zipf-popularity simulator (30 episodes, approximately 1,600 calls,
static/periodic/bursty resources) is run side by side as a second, clearly-labeled data source -- never
again as an unacknowledged fallback for the real corpus. The full grid (2 data sources $\times$ 44 scoped
(policy, knob, spot-check-rate) cells $\times$ 20 replicate seeds = 1,760 replicate rows) replays in under 8
seconds on CPU with zero LLM/OpenRouter calls, since cache-policy decisions do not depend on query-text
diversity.

# Experiments

## Setup

We report two independent lines of evidence, deliberately kept separate because they answer different
questions the previous review raised. First, Section 4 reports the real-data-vs-synthetic replay
(`art_tceB4eOwcBAO`), which answers whether AIMD's advantage survives contact with content the previous
iteration's corpus was purpose-built to provide. Second, Section 5 reports an independent statistical
re-derivation of the *previous* iteration's synthetic-only run (`art_tXld0p2SGjtU`), which answers whether
that run's self-reported dominance numbers survive independent bootstrap confidence intervals and
significance testing. We present both rather than only the newer run because the discrepancy between them
-- and its diagnosed root causes -- is itself part of the paper's evidence about the reliability of
self-reported caching-policy benchmarks.

## Real-data result: AIMD is dominated, not non-dominated

[FIGURE:fig_frontier]

Table 1 reports mean hit rate and mean stale-rate-of-served (mean over 20 replicate seeds at the headline
0.20 spot-check rate) for each policy family's best- and worst-performing knob setting on the real corpus.

| Policy | Hit rate range | Stale rate range |
|---|---|---|
| Fixed TTL (ttl=1..30) | 0.695 - 0.916 | 0.113 - 0.173 |
| d-TTL ($h_{\text{target}}=0.5..0.9$) | 0.707 - 0.721 | 0.109 - 0.111 |
| EWMA-adaptive ($\alpha=0.1..0.5$) | 0.797 - 0.799 | 0.106 - 0.107 |
| **AIMD** ($a,b$ full 9-point grid) | **0.794 - 0.803** | **0.106 - 0.109** |
| FreshCache (raw) | 0.902 - 0.905 | 0.112 - 0.121 |
| FreshCache (pooled) | 0.898 - 0.906 | 0.096 - 0.112 |

This is a materially different picture from the previous iteration's synthetic-only frontier. On real
data, AIMD's entire 9-point knob grid clusters tightly in a 0.794-0.803 hit-rate band at 0.106-0.109 stale
rate -- and FreshCache (both raw and pooled) reaches 0.90-0.91 hit rate at a comparable or lower stale rate
(pooled reaches 0.096 stale rate at its lowest-hit-rate knob, actually *below* AIMD's best stale rate),
Pareto-dominating every AIMD knob setting outright rather than trading off against it
[ARTIFACT:art_tceB4eOwcBAO]. AIMD is also not distinguishable in any practical sense from the far simpler
EWMA-adaptive baseline, which reaches an almost identical operating point (0.797-0.799 hit rate at
0.106-0.107 stale rate) with a fixed step size and no multiplicative-cut machinery at all. Fixed TTL at
ttl=3 (0.774 hit rate, 0.107 stale rate) sits close to AIMD's band without the adaptation overhead,
though AIMD edges it out slightly on hit rate at a similar stale rate. Running the identical policy grid
on the synthetic simulator shows the same qualitative pattern is not an artifact of real content
specifically: FreshCache reaches 0.940-0.949 hit rate there too, though with a genuine tradeoff against a
higher stale rate (0.042-0.056) than AIMD's 0.021-0.022 -- meaning FreshCache dominates AIMD on real data
outright, but only trades off against it on synthetic data. The real corpus's higher inherent staleness
(FixedTTL reaches 0.113 stale rate at ttl=1 on real data versus 0.011 on synthetic, at comparable hit
rates) reflects genuinely churning periodic and bursty resources -- the Our World in Data COVID-19 series
in particular -- that the synthetic Zipf simulator's schedules did not fully reproduce.

## Independent statistical re-verification of the previous iteration's synthetic claim

The previous iteration's self-reported claim (AIMD non-dominated on 8/12 medium-volatility and 12/12
high-volatility knob settings, mean fraction 0.67) was never independently checked: the evaluation
artifact built to compute bootstrap confidence intervals and a mechanical verdict returned
`BLOCKED_NO_DATA` because neither the experiment nor dataset artifact's outputs were discoverable in the
expected per-call event-log schema. This iteration's evaluation artifact fixes that by directly importing
the previous iteration's `method.py`, reproducing its exact simulator and seeds, and re-deriving
per-episode instrumentation for the full 150-cell (regime $\times$ policy family $\times$ knob) grid
[ARTIFACT:art_tXld0p2SGjtU].

The re-derived result overturns the self-reported one. Table 2 reports the bootstrap-CI'd (10,000
resamples) non-dominated fraction per regime, alongside the original self-reported figures.

| Volatility regime | Self-reported (iter. 1) | Independently re-derived | 95% CI |
|---|---|---|---|
| Low | 0.333 | **0.0** | [0.0, 0.167] |
| Medium | 0.667 | **0.0** | [0.0, 0.0] |
| High | 1.000 | **0.0** | [0.0, 0.210] |
| Mean | 0.667 | **0.0** | -- |

Every regime's independently re-derived non-dominated fraction is 0.0, with confidence intervals that
exclude majority non-domination in all three cases, and the medium-volatility regime's CI is a point mass
at exactly 0.0. The mechanical verdict against the hypothesis's frontier-non-domination criterion changes
from CONFIRMS to DISCONFIRMS on the same underlying simulator. Table 3 breaks this down by baseline
family and regime, reporting the fraction of AIMD's 12 original knob points not dominated by each specific
baseline family individually.

| Regime | vs. Fixed TTL | vs. d-TTL | vs. EWMA | vs. FreshCache | vs. FreshCache-pooled |
|---|---|---|---|---|---|
| Low | 0.500 | 1.000 | 0.417 | 0.833 | **0.000** |
| Medium | 0.917 | 1.000 | 0.917 | 0.417 | **0.000** |
| High | 1.000 | 1.000 | 1.000 | 0.500 | **0.083** |

AIMD is never dominated by d-TTL in any regime, and rarely dominated by fixed TTL or EWMA-adaptive TTL,
which is consistent with the previous iteration's narrative of beating hit-rate-targeted adaptation. What
changes the overall verdict entirely is FreshCachePooled: it dominates every one of AIMD's 12 knob points
in low and medium volatility (0.000 non-dominated fraction) and all but one in high volatility (0.083),
because a partial-pooling fitted gate reaches a strictly better hit-rate/stale-rate combination once its
sparse per-site fits borrow strength across resource-schedule families. The previous iteration's headline
"12/12 non-dominated in high volatility" statistic counted domination only pairwise-per-baseline and never
constructed the *joint* Pareto frontier across all four baseline families simultaneously; a single point
being non-dominated by three of four families does not make it non-dominated by the frontier as a whole,
and the independent re-derivation makes that joint comparison correctly for the first time.

Root-causing why the self-reported and re-derived numbers diverge surfaces two concrete, previously
undocumented bugs. First, a genuine dataset-wiring bug: direct string grep of `method.py`'s source confirms
it never references `full_data_out.json` or `mini_data_out.json` anywhere, so the real-content corpus
never entered the evaluated event log at either iteration's original run -- consistent with, and now
formally confirmed alongside, this iteration's decision to build a fresh real-data experiment
(`art_tceB4eOwcBAO`) rather than attempt to patch the original script in place. Second, a seed-reproducibility
bug: `method.py` seeds each replay job with `hash((regime, family, knob_idx)) % 2**31`, but Python's
`hash()` of string and tuple objects is randomized per-process when `PYTHONHASHSEED` is unset, so the three
stochastic policy families whose state updates are gated on a random spot-check flag (AIMD, FreshCache,
FreshCachePooled) cannot be bit-reproduced across separate process runs, while the three families that
update unconditionally every call (FixedTTL, d-TTL, EWMA) are seed-invariant and matched the original run's
numbers to within $10^{-9}$. This was isolated as the root cause by checking exactly which families
mismatched (60 of 150 cells) and confirming the pattern matches the theory precisely -- all and only the
three stochastic families [ARTIFACT:art_tXld0p2SGjtU].

## Convergence sample-efficiency, with confidence intervals

[FIGURE:fig_convergence]

The hypothesis's second success criterion required AIMD to stabilize using substantially fewer
confirmed-staleness feedback events than the fitted FreshCache gate needs to calibrate. Table 4 reports
median convergence-event counts with bootstrap 95% CIs, aggregated over the low-repeat-count call-site
bucket, now independently re-derived rather than self-reported.

| Policy | Low volatility | Medium volatility | High volatility |
|---|---|---|---|
| d-TTL | 12.0 [11.0, 12.0] | 12.0 [11.0, 12.0] | 11.0 [11.0, 12.0] |
| EWMA-adaptive | 7.0 [5.0, 9.0] | 8.0 [7.0, 9.0] | 8.0 [6.0, 9.0] |
| FreshCache (raw) | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| FreshCache (pooled) | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] | 5.0 [5.0, 5.0] |
| **AIMD** | **12.0 [9.0, 19.5]** | **12.0 [10.0, 16.0]** | **16.0 [10.0, 27.0]** |

AIMD remains the slowest of the five families to reach a stable operating point by this definition in
every regime, and its confidence intervals are the widest of any policy (up to [10.0, 27.0] in high
volatility, versus FreshCache's degenerate [5.0, 5.0] point interval), reflecting a genuinely low sample
count (n=6-9 low-repeat AIMD sites per regime, flagged `low_n_flag` in low volatility) rather than a
precisely estimated slow convergence. As before, this does not mean FreshCache's fast nominal convergence
is trustworthy: its Wilson-interval calibrated fraction is a tight 0.346 [0.289, 0.408] in low volatility,
0.363 [0.304, 0.425] in medium, and 0.350 [0.292, 0.412] in high -- meaning roughly two-thirds of the
low-repeat sites FreshCache "converges" on in 5.0 events are fit on too few observations to be judged
statistically trustworthy by a Wilson-interval sample-floor check, with confidence intervals now tight
enough to state this as a genuinely low, not merely point-estimated, calibration rate.

An ecological-validity proxy sharpens which regime this evidence should be weighted toward. The real
corpus's own resources (329 total, spanning the three real timing-provenance categories) are
overwhelmingly static: 84.8% static, 13.7% periodic, and only 1.5% bursty by resource count, with a median
of 5.0 revisits per resource per episode [ARTIFACT:art_tXld0p2SGjtU]. This mix sits *inside* the synthetic
low-volatility regime's parameters ($p_{\text{static}}=0.70$) but is far more static-dominated than either
the medium ($p_{\text{static}}=0.35$) or high-volatility ($p_{\text{static}}=0.10$) synthetic regimes --
meaning the high-volatility regime, where AIMD's frontier position looked strongest in the previous
iteration's self-reported analysis (and where, per Table 3 above, it remains least-dominated even after
correction), is also the regime deliberately constructed to be more adversarial than anything the real
corpus actually contains.

## Ablations

[FIGURE:fig_ablation]

**Unchecked-hit crediting.** AIMD's `presumed_valid_weight` knob controls whether an unchecked served hit
is treated as presumed-valid and allowed to grow the window, versus the conservative default of only
moving the window on spot-checked outcomes. Under low volatility, the conservative default reaches a 0.298
hit rate at 0.014 stale rate with a low-repeat convergence median around 10-15 events; crediting unchecked
hits at weight 0.25 raises the hit rate to 0.380 at a comparable 0.024 stale rate but pushes the
convergence-event median out to 67, and weight 0.5 pushes it further to 84 -- because presumed-valid credit
lets the window grow past what the sparse spot-check stream can confirm, so more total events are needed
before growth and confirmed correction reach the tolerance band. This same effect appears at every
volatility level (medium: convergence median 10 to 73 to 78 across the three weights; high: 15 to 49.5 to
49) and stale rate scales with volatility as expected (high-volatility stale rate reaches 0.19 at weight 0
and 0.32 at weight 0.5), confirming the credit-unchecked-hits knob trades hit rate for both convergence
speed and staleness risk continuously, not just at the single default setting reported previously.

**Spot-check-rate sensitivity.** This ablation, present in the underlying artifact since the previous
iteration but never reported in the paper text, directly tests the paper's own mechanistic explanation for
AIMD's slow convergence -- that its window grows between confirmations faster than the sparse spot-check
stream can confirm it. Sweeping the spot-check rate from 0.05 to 0.8 (at fixed $a=0.5$, $b=0.5$) shows
hit rate rising monotonically with spot-check density in every regime (low volatility: 0.191 at rate 0.05
to 0.439 at rate 0.8; medium: 0.199 to 0.362; high: 0.229 to 0.305), while stale rate stays roughly flat or
rises only slightly (low: 0.006 to 0.018; medium: 0.060 to 0.081; high: 0.191 to 0.176) -- a denser spot-check
stream lets the window confirm its growth faster and safely reuse the cache more often, without a
correspondingly large increase in stale-serve risk. This is direct, independent confirmation of the
mechanism proposed to explain AIMD's convergence-speed shortfall: convergence is gated by spot-check
density, not by the AIMD update rule's intrinsic responsiveness, and a system willing to spend a higher
spot-check budget can materially close AIMD's hit-rate gap against FreshCache without paying much
additional staleness risk [ARTIFACT:art_qtEtMpLZuRGI].

# Discussion

**A result that reversed under independent scrutiny, not merely a mixed one.** The previous iteration
reported a "genuinely mixed" outcome: frontier non-domination held (self-reported mean fraction 0.67) while
convergence speed did not. This iteration's evidence goes further and reverses the frontier claim itself.
Independent statistical re-derivation of the exact same underlying synthetic simulator run finds a mean
non-dominated fraction of 0.0, not 0.67, with confidence intervals that rule out majority non-domination in
every volatility regime; and a freshly executed real-data replay, using the corpus purpose-built for this
study and never previously consumed, finds AIMD Pareto-dominated outright by a fitted staleness gate.
Both new pieces of evidence point the same direction independently, which is stronger support for the
reversal than either alone: the previous headline result was an artifact of never having constructed the
correct joint Pareto frontier across all four baselines simultaneously (Section 5.1), compounded by never
having tested against the real content the corpus was built to provide (Section 4).

**Why the reversal happened, mechanistically.** Two concrete, now-diagnosed causes explain the gap between
self-reported and independently verified numbers. The dataset-wiring bug meant every synthetic-only claim
was never checked against real content; when it finally was, in this iteration, FreshCache's fitted gate
turned out to generalize better to the real corpus's genuinely bursty, churning resources (particularly the
Our World in Data COVID-19 series, whose real daily cadence is far noisier than the synthetic simulator's
injected schedules) than AIMD's reactive window does. The pairwise-versus-joint dominance-counting error
meant the previous iteration's headline "12/12 non-dominated in high volatility" statistic was true only
against each baseline family checked in isolation, never against the frontier those families jointly define
-- and once FreshCachePooled's own frontier is constructed correctly, it alone dominates 11-12 of AIMD's 12
knob points in every regime. Neither cause reflects a flaw in AIMD's underlying mechanism so much as a flaw
in how the previous iteration measured it, which is exactly the class of error independent statistical
verification exists to catch.

**Convergence speed remains genuinely unresolved in AIMD's favor.** Unlike the frontier claim, the
convergence-speed finding is unchanged by independent re-verification and, if anything, sharpened: AIMD's
median low-repeat convergence-event count (12.0-16.0, now with confidence intervals as wide as [10.0, 27.0]
in high volatility) remains slower than every baseline, and the spot-check-rate ablation (Section 4.4)
mechanistically confirms why -- AIMD's window continues probing upward via additive increase between
confirmations, so a sparse spot-check stream delays entry into our stabilization tolerance band regardless
of how quickly the window itself starts moving. FreshCache's raw 5.0-event convergence figure remains
qualified by a tightly-bounded 0.29-0.41 calibrated fraction across all three regimes, meaning roughly
two-thirds of the sites it nominally converges on so quickly are not judged statistically trustworthy;
this qualification is now stated with confidence intervals rather than a single point estimate, and does
not change with volatility.

**Limitations.** First, the real-data experiment in Section 4 widened the AIMD grid to 9 knob settings but
restricted the fixed-TTL sweep to 5 values and each baseline family to 3 knob values, in order to keep the
full (2 data sources $\times$ 44 cells $\times$ 20 seeds) grid tractable; a wider baseline sweep on real
data, matching the earlier synthetic-only 9-15 point grids, is left for future work and could narrow or
widen the FreshCache-versus-AIMD gap reported here. Second, the independent statistical re-derivation in
Section 5 re-verifies the *previous* iteration's synthetic simulator, not this iteration's real-data
experiment; a full bootstrap-CI'd, Holm-corrected re-derivation of the real-corpus numbers in Table 1 has
not yet been run and is the most direct remaining gap between "AIMD is dominated on real data" as a point
estimate and as a statistically confirmed claim. Third, the ecological-validity proxy in Section 5.2
compares aggregate static/periodic/bursty fractions between the real corpus and the synthetic simulator's
regime parameters, but the real corpus's own volatility labels are assigned per-resource rather than
per-simulated-regime-scenario, so this is a proxy comparison, not a literal parameter match -- a caveat the
underlying artifact states explicitly and this paper preserves rather than overclaims. Fourth, our
convergence-event stabilization definition (a fixed tolerance band held for 10 consecutive updates) remains
a single reasonable choice among several plausible ones; the qualitative finding that AIMD is *responsive*
early (its window visibly moves after four observations where FreshCache's fitted hazard stays pinned to
its prior) but *stabilizes* late is robust to this choice, but the precise event counts in Table 4 are not.
Fifth, as stated at the outset of the Introduction, this entire study is an offline replay against synthetic
and real-content-grounded but pre-scripted call streams -- no live LLM agent or production trace was
involved at any point, and the absolute numbers reported here characterize the policies under these
controlled replay conditions, not real agent-loop traffic in deployment.

# Conclusion

We tested whether reframing an LLM agent tool cache's per-site reuse window as a TCP-style AIMD congestion
window would match or beat both fixed TTL and hit-rate-targeted adaptive TTL on the redundant-call-reduction-
versus-staleness tradeoff, while needing substantially fewer confirmed-staleness events than a fitted
probabilistic staleness gate to stabilize. This iteration's central contribution is methodological as much
as empirical: fixing a silent dataset-wiring bug and adding independent, bootstrap-CI'd statistical
re-verification -- both directly requested by the previous review -- overturns the previous iteration's own
self-reported headline result. Replayed against the real-content corpus purpose-built for this study, AIMD
is Pareto-dominated outright by a fitted staleness gate (FreshCache reaches 0.90-0.91 hit rate at 0.10-0.12
stale rate versus AIMD's 0.79-0.80 hit rate at 0.106-0.109 stale rate across its full 9-point knob grid) and
matched, not beaten, by a far simpler EWMA-adaptive baseline. Independently re-deriving the previous
iteration's synthetic-only result with 10,000-resample bootstrap confidence intervals finds a mean
non-dominated fraction of 0.0, not the self-reported 0.67, with confidence intervals excluding majority
non-domination in every volatility regime -- a reversal traced to two concrete bugs, a confirmed
dataset-wiring failure and a seed-reproducibility failure from unset `PYTHONHASHSEED`. The convergence-speed
finding is unchanged by this correction: AIMD's median low-repeat convergence-event count (12.0-16.0)
remains slower than d-TTL (11.0-12.0), EWMA (7.0-8.0), and FreshCache's raw 5.0-event figure, even though
FreshCache's own calibrated fraction is a tightly-bounded 0.29-0.41 across all three regimes. A systematic
literature search closes the paper's remaining novelty gap, confirming no prior work in CDN, database,
DNS, or browser caching applies a confirmed-staleness-triggered AIMD rule to per-object TTL. The net
picture, now grounded in independently verified numbers and real content rather than self-reported
synthetic-only figures, is that AIMD's reactive, model-free control law does not earn a practical advantage
over a fitted probabilistic gate on the axis it was hypothesized to win, and remains slower to stabilize on
the axis it was also hypothesized to win -- a genuinely negative result for the specific hypothesis tested,
though one that surfaces a broader, transferable lesson: self-reported caching-policy benchmarks that have
not been checked against both real content and independent statistics should not be trusted at face value.

**Future work:**

- Run a full bootstrap-CI'd, Holm-corrected statistical re-derivation of this iteration's real-data
  experiment (Section 4), matching the rigor already applied to the previous iteration's synthetic run in
  Section 5, to attach formal significance to the real-corpus dominance finding.
- Widen the real-data baseline sweep (fixed TTL, d-TTL, EWMA, FreshCache) to match the earlier
  synthetic-only 9-15 point grids, now that the dataset-wiring bug is fixed and the full corpus is
  confirmed loadable.
- Test a decaying additive-increase schedule for AIMD (mirroring TCP's own slow-start-to-congestion-avoidance
  transition) as a targeted fix for the convergence-speed shortfall the spot-check-rate ablation
  mechanistically confirms, rather than a constant per-regime increment.
- Investigate why FreshCache's fitted hazard model generalizes better than AIMD's reactive window to the
  real corpus's genuinely bursty resources (e.g., the Our World in Data COVID-19 series), to determine
  whether this is a property of real-world staleness distributions in general or specific to the resource
  classes sampled here.

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

[8] J. P. Thoma, C. Niesler, D. R. E. Funke, G. Leander, P. Mayr, N. Pohl, L. Davi, and T. Gueneysu.
ClepsydraCache -- Preventing Cache Attacks with Time-Based Evictions. In *32nd USENIX Security Symposium
(USENIX Security 23)*, 2023.

[9] V. Cate. The Alex Global Filesystem. *USENIX File Systems Workshop*, Ann Arbor, 1992.

[10] R. T. Fielding, M. Nottingham, and J. F. Reschke. Hypertext Transfer Protocol (HTTP/1.1): Caching.
RFC 7234, IETF, 2014.

[11] (Systematic novelty search across CDN, database materialized-view, DNS, and browser/HTTP caching
literature; see Related Work for full methodology and findings.)

[12] Z. Chen, R. Ye, W. Tang, Y. Sun, H. Tian, X. Wang, Y. Li, H. Wen, S. Han, and C. Zhang. Concur:
Proactive Agent-Level Admission Control for Efficient Agentic Batch Inference. In *International Conference
on Machine Learning (ICML)*, 2025.

[13] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang. SQuAD: 100,000+ Questions for Machine Comprehension
of Text. In *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing*, 2016.

[14] S. Iyer, N. Dandekar, and K. Csernai. First Quora Dataset Release: Question Pairs. Quora Data blog,
2017.

[15] Our World in Data. Our World in Data Catalog: Population, Energy Mix, and COVID-19 Data.
ourworldindata.org, 2024.

[16] F. Bang. GPTCache: An Open-Source Semantic Cache for LLM Applications Enabling Faster Answers and Cost
Savings. In *Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software
(NLP-OSS 2023)*, 2023.

[17] J. Li, C. Xu, F. Wang, I. M. von Riedemann, C. Zhang, and J. Liu. SCALM: Towards Semantic Caching for
Automated Chat Services with Large Language Models. In *2024 IEEE/ACM 32nd International Symposium on
Quality of Service (IWQoS)*, 2024.
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (rigor) The real-data headline result (Table 1, Section 4 -- AIMD dominated by FreshCache, matched by EWMA) is reported as bare point estimates over 20 replicate seeds, with no bootstrap confidence intervals or significance testing, even though the paper's own Section 5 argues at length that self-reported point estimates without independent statistical verification should not be trusted (the exact standard this new result fails to meet). The Limitations section acknowledges this gap explicitly, but the abstract, contributions list, and Conclusion all state the real-data dominance finding as a flat, unqualified fact.
  Action: Run the already-built bootstrap-CI/Holm-correction evaluation machinery (used in Section 5 against the synthetic run) against the real-data replicate rows in art_tceB4eOwcBAO -- 20 seeds per cell already exist, so this does not require new data collection. Report Table 1 with CIs and at minimum a Pareto-dominance significance test between AIMD and FreshCache/EWMA. If infeasible before the next iteration, move the caveat from Limitations to the first sentence of Section 4 and soften 'dominated outright' to 'point-estimate dominance, not yet independently statistically confirmed' throughout the abstract and Conclusion.
- [MINOR] (methodology) The real-data experiment widens AIMD's knob grid to 9 (a,b) combinations but restricts every baseline family (Fixed TTL, d-TTL, EWMA, FreshCache) to only 3-5 knob values, down from the 9-15 point grids used in earlier synthetic-only runs. Since the paper's dominance claim rests on FreshCache's best knob beating AIMD's best knob, an asymmetric search budget (3x more configurations tried for AIMD than for FreshCache) could understate FreshCache's own achievable hit-rate/stale-rate tradeoff or overstate AIMD's, in either direction, independent of which policy is actually better.
  Action: Either widen the real-data baseline sweeps to match AIMD's 9-point grid (the paper already lists this as future work; doing it now would materially strengthen the dominance claim) or add an explicit sentence in Section 4 justifying why the narrower baseline grids are already saturating each policy's achievable frontier (e.g., cite the synthetic-only run's finding that additional knob points did not move the frontier materially past 3-5 values).
- [MINOR] (evidence) FreshCache's real-data dominance in Table 1 is not broken out by call-site repeat count, even though the paper's own convergence analysis (Table 4, Section 5.2) argues AIMD is specifically disadvantaged at low repeat counts while FreshCache needs at least 5 confirmed observations to fit at all -- precisely the regime where a fitted model should be weakest. The paper never checks whether FreshCache's overall real-data win survives when restricted to the low-repeat bucket, which is the regime the paper elsewhere identifies as diagnostically important and as most representative of real agent-tool-call sites (median 5 revisits per resource in the real corpus).
  Action: Report Table 1's hit-rate/stale-rate figures separately for the low-repeat-count bucket already used in Table 4 (sites visited <=5 times), to check whether FreshCache's dominance holds, narrows, or reverses in the specific regime the paper argues is most representative of real agent tool-call traffic.
- [MINOR] (novelty) The systematic novelty search (Section 2, art_iY6kMoc-uEE6) covers CDN, database materialized-view, DNS, and browser/HTTP caching literature plus one LLM-agent-serving hit (Concur), but does not search adjacent control-theoretic domains where AIMD-style reactive resource-window adaptation is a long-established pattern outside caching entirely -- e.g., autoscaling/admission-control systems (Kubernetes HPA-style policies, TCP-inspired rate limiters in API gateways) that have occasionally been adapted to freshness-adjacent problems. This does not undermine the paper's core claim (agent-side per-call-site TTL specifically) but the novelty framing implicitly claims a broader search than was actually performed.
  Action: Either scope the novelty claim explicitly to 'caching literature specifically' in the Related Work closing sentence (a small wording change), or add one additional query angle covering AIMD-style adaptive-window control in adjacent systems domains (rate limiting, autoscaling) to close this narrower gap with the same rigor applied to the caching-specific search.
- [MINOR] (scope) As in the previous iteration, no live LLM agent, real tool invocation, or production agent trace is used anywhere in the study -- this iteration's real-content corpus improves ground-truth fidelity for the underlying resources but the call streams themselves are still generated by three fixed, deterministic repetition templates (read-then-reread, search-then-refine, compute-then-reuse) rather than sampled from actual agent behavior. This is now disclosed clearly and early (first paragraph of the Introduction), which resolves the previous review's clarity concern, but the external-validity gap itself remains unaddressed as a methodological limitation.
  Action: No further paper-text action needed for clarity (this is already well-disclosed up front); for future work, note that validating the relative policy ranking against even a small sample of real agent-loop call traces (not full deployment, just trace collection) would be the natural next step to establish ecological validity beyond the proxy comparison in Section 5.2.
- [MINOR] (clarity) The paper states AIMD 'edges out' Fixed-TTL(ttl=3) on hit rate at a similar stale rate but is 'matched, not beaten' by EWMA at an overlapping operating point, without a consistent quantitative threshold distinguishing 'edges out' from 'matched' from 'dominated' -- three different verbal verdicts applied to numerically similar-magnitude gaps (AIMD vs. ttl=3: 0.794 vs 0.774, a 0.02 gap; AIMD vs. EWMA: 0.794-0.803 vs 0.797-0.799, an overlapping band).
  Action: Define a single operational rule up front (e.g., 'matched' = ranges overlap; 'edges out' = point estimate higher but ranges overlap; 'dominated' = every point in A's range is strictly worse than some point in B's range) and apply it consistently across all three comparisons in Section 4.
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

### [2] HUMAN-USER prompt · 2026-08-10 04:55:07 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```
