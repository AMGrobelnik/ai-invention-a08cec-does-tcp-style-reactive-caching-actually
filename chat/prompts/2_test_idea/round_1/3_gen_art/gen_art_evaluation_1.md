# gen_art_evaluation_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_evaluation_1` (terminal_claude_agent)

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

<task>
Evaluate experimental results using domain-appropriate methods, metrics, and analysis techniques.
When in doubt, prefer more metrics over fewer — but only ones that make sense for the domain.
</task>

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
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/results/out.json`
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
id: gen_plan_evaluation_1_idx3
type: evaluation
title: Pareto Frontier and Convergence Speed of AIMD Caching
summary: >-
  Evaluate the per-call logs produced by the AIMD-vs-fixed-TTL-vs-d-TTL-vs-FreshCache-gate cache experiment. Compute, per
  policy/knob/volatility regime, the fraction of calls served from cache vs. the empirical stale-serve rate, fit and compare
  reduction-vs-staleness Pareto frontiers with bootstrap CIs, define and measure per-policy convergence (confirmed-staleness
  feedback events needed until the adapted parameter stabilizes within a tolerance band), and run paired statistical tests
  across episodes/seeds to render an explicit CONFIRMS/DISCONFIRMS verdict against the hypothesis's stated success criteria.
runpod_compute_profile: gpu
metrics_descriptions: |-
  INPUTS EXPECTED FROM THE EXPERIMENT ARTIFACT: a per-call event log (JSON/CSV/parquet) with, at minimum, one row per tool call carrying: episode_id, seed, volatility_regime, call_site_id (function+argument signature hash), timestamp/step_index, policy_name (fixed_ttl | d_ttl | aimd | freshcache_gate), knob_value (the specific TTL seconds / target-hit-rate / (a,b) AIMD pair / error-budget used for that run), served_from_cache (bool), spot_checked (bool, whether a live re-query was forced for this hit), ground_truth_stale (bool or null if not checked/not applicable — cache misses always execute live so are trivially non-stale), and, for adaptive policies, the current per-site adapted value (aimd window w_i, d-TTL's TTL_i, freshcache's fitted per-entry/tier staleness probability or threshold) logged at every update event.

  1) REDUCTION-VS-STALENESS OPERATING POINTS. For each (policy, knob_value, volatility_regime) triple, aggregate across episodes/seeds: cache_hit_fraction = served_from_cache / total_calls (redundant-call reduction); empirical_stale_rate = ground_truth_stale / spot_checked among served_from_cache rows, inverse-probability-reweighted by the spot-check sampling rate per call_site_id/time-bucket to correct for the fact that only a sampled subset of hits get a live re-query (report both the raw spot-checked-only rate and the reweighted estimate; note if they diverge materially, that is itself a validity finding). Bootstrap (≥2,000 resamples, resampling at the episode level to preserve within-episode correlation, not the row level) a 95% CI on both coordinates for every operating point.

  2) PARETO FRONTIER CONSTRUCTION AND COMPARISON. Per volatility regime, plot cache_hit_fraction (x) vs empirical_stale_rate (y) for every knob value swept per policy, connect each policy's own non-dominated points into its frontier, and report: (a) frontier-AUC (area under the reduction-axis integrated against the minimum achievable stale rate up to each hit-fraction level, via trapezoidal integration over the non-dominated point set) per policy per regime, with bootstrap CI; (b) a non-dominated-point count/fraction test — for each AIMD operating point, check whether any fixed-TTL or d-TTL point achieves both >= cache_hit_fraction and <= empirical_stale_rate (strict dominance), and report the fraction of AIMD points that are Pareto-dominated by each baseline; (c) at matched stale-rate targets (e.g., the same 3-5 stale-rate bands used in FreshCache's own per-tier error budgets: ~0.1%, 1%, 3.3%, 10%), report each policy's achieved cache_hit_fraction via linear interpolation between adjacent knob points on its own frontier, with bootstrap CI on the difference AIMD-vs-each-baseline.

  3) CONVERGENCE / SAMPLE-EFFICIENCY. Define stabilization per policy explicitly and apply the SAME tolerance-band logic uniformly: (a) AIMD -- per call_site_id, the window w_i is 'stabilized' at the first update step after which w_i stays within +/-10% of its own trailing-20-update mean for at least 10 consecutive updates (or the full remaining trace if fewer than 10 updates occur before the episode ends -- flag those sites as 'insufficient data' rather than silently excluding); record the number of confirmed-staleness feedback events (spot-checked hits with ground_truth_stale observed, valid or stale) consumed by that call_site_id up to the stabilization step. (b) d-TTL -- same tolerance-band rule applied to its adapted TTL_i trace. (c) FreshCache-style gate -- 'trustworthy calibration' operationalized as: the per-entry/tier fitted staleness-probability model's parameter estimates satisfy the same +/-10%/10-consecutive-update stability rule AND the number of labeled (spot-checked) observations feeding that entry/tier's model has crossed a minimum-sample floor (justify the floor from the model's own confidence-interval width, e.g. Wilson interval half-width < 0.05 on the fitted probability -- report the floor value used and why). Aggregate per policy: median and IQR of confirmed-staleness-events-to-convergence across call sites, stratified by call-site repeat-count bucket (low: <=5 occurrences/episode, medium: 6-20, high: >20) -- the low-repeat-count bucket is the hypothesis's central claim, so report it separately and explicitly, not just pooled. Report the fraction of call sites in each bucket that FAIL to converge/calibrate at all within the observed trace length, per policy -- this failure rate is itself a key result, especially for FreshCache in the low-repeat-count bucket.

  4) STATISTICAL TESTS FOR THE VERDICT. Paired (by episode+seed) Wilcoxon signed-rank tests (or paired bootstrap difference-in-means with BCa CIs if the sample of episodes is small, e.g. <20) comparing: AIMD's frontier-AUC vs fixed-TTL's and vs d-TTL's per volatility regime; AIMD's median convergence-events vs d-TTL's and vs FreshCache's, per repeat-count bucket. Apply Holm-Bonferroni correction across the family of these comparisons. Report effect sizes (rank-biserial correlation or standardized mean difference) alongside p-values, not p-values alone.

  5) EXPLICIT VERDICT MAPPING. Re-state the hypothesis's own CONFIRMS/DISCONFIRMS criteria as a checklist and mechanically mark each: (a) AIMD frontier comparable-or-better than fixed-TTL and d-TTL (non-dominated fraction >= baseline's, or frontier-AUC CI overlapping/exceeding, in >= half of volatility regimes) -- PASS/FAIL with the numbers cited; (b) AIMD converges using substantially fewer confirmed-staleness events than FreshCache needs to calibrate, specifically in the low-repeat-count bucket (report the ratio of medians and whether FreshCache's low-repeat-count non-convergence rate is materially higher) -- PASS/FAIL with numbers cited. State the overall verdict as CONFIRMS only if both (a) and (b) pass; otherwise DISCONFIRMS/MIXED with the specific criterion that failed named. If d-TTL turns out to dominate AIMD on the frontier, or AIMD needs comparable/more staleness feedback than FreshCache to stabilize, report this plainly as the hypothesis's own stated disconfirming outcome, not as an experiment failure.

  6) ROBUSTNESS AND VALIDITY CHECKS. (a) Sensitivity of the Pareto/convergence results to the spot-check sampling rate used in the experiment (if the experiment logged multiple spot-check rates or if it can be sub-sampled post hoc from a higher logged rate, recompute frontiers/convergence at a lower simulated spot-check rate to see whether AIMD's fewer-events advantage holds when feedback is even sparser -- this directly stress-tests the hypothesis's central low-data claim); (b) check for confounds between volatility regime and call-site repeat-count distribution (e.g. if high-volatility regimes happen to also have fewer repeats, stratify rather than pool); (c) sanity-check the FreshCache reimplementation's calibration quality independent of the comparison (e.g. reliability diagram / Brier score of its fitted staleness probabilities against ground truth on a held-out spot-check split) so a weak reimplementation isn't mistaken for a genuine mechanism-level finding -- report this as a caveat if the reimplementation underperforms the published FreshCache numbers materially; (d) report missingness -- how many call sites per policy/regime had zero spot-checks at all (making convergence undefined) and exclude them transparently rather than imputing.
metrics_justification: >-
  The hypothesis's success criteria are stated as two explicit, falsifiable comparisons: (a) AIMD's position on the reduction-vs-staleness
  frontier relative to fixed-TTL and d-TTL, and (b) AIMD's confirmed-staleness-feedback sample-efficiency to converge relative
  to FreshCache's sample requirement to calibrate, especially in the low-repeat-count regime that motivates the whole hypothesis.
  The Pareto-frontier-AUC and non-dominated-point metrics operationalize (a) directly as a single comparable number per regime
  while still preserving the full tradeoff curve (rather than collapsing to one arbitrary operating point, which would hide
  exactly the knob-sweep behavior the experiment was designed to produce). Bootstrap CIs at the episode level (not row level)
  are required because tool calls within an episode are correlated (repeated visits to the same call sites), so naive row-level
  resampling would understate variance and manufacture false significance. The convergence metric is defined identically (a
  tolerance-band stabilization rule) across all three adaptive policies so the comparison is apples-to-apples rather than
  each policy getting a favorable bespoke definition of 'ready' -- this matters because the whole hypothesis rests on AIMD
  needing fewer events, and a biased convergence definition could manufacture that result. Stratifying by call-site repeat-count
  bucket is essential rather than optional: the hypothesis is explicitly a claim about the low-repeat-count regime ('agent
  loops are exactly the setting where...many call sites are visited only a handful of times'), so a pooled-only result that
  averages over easy high-repeat sites would dilute or mask the very effect being tested. Paired statistical tests (by episode+seed)
  with multiple-comparison correction and effect sizes are needed because the plan compares several policy pairs across several
  regimes/buckets simultaneously, and unpaired or uncorrected tests would inflate false-positive risk on a hypothesis whose
  paper-worthy claim rests on these specific comparisons. The robustness checks -- spot-check-rate sensitivity, volatility/repeat-count
  confound check, and independent calibration-quality sanity check of the FreshCache reimplementation -- exist because the
  two closest prior mechanisms (FreshCache, d-TTL) are being reimplemented rather than run as published systems, so a null
  or negative result for AIMD must be distinguishable from a weak reimplementation of the baseline, and a positive result
  must be distinguishable from an artifact of how heavily the spot-check budget was set in the experiment.
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
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for evaluation metrics, agent orchestration patterns, benchmark design.

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
TODO 2. Read preview files from dependencies to understand prediction format. Evaluate ALL experiments provided — do not skip or select a subset. Avoid re-training or re-executing the method unless absolutely necessary; prefer loading predictions from each dependency's method_out.json / predict_* fields. Read domain handbook if applicable (see <available_domain_handbooks>). Decide evaluation metrics based on artifact plan. Test basic functionality with 'uv run'.
TODO 3. Fully implement evaluation as described in artifact plan in './eval.py'. Use exp_eval_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant metrics or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-08-09 23:25:23 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [3] SYSTEM-USER prompt · 2026-08-09 23:25:43 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/file.py`, `/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/results/out.json`
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
id: gen_plan_evaluation_1_idx3
type: evaluation
title: Pareto Frontier and Convergence Speed of AIMD Caching
summary: >-
  Evaluate the per-call logs produced by the AIMD-vs-fixed-TTL-vs-d-TTL-vs-FreshCache-gate cache experiment. Compute, per
  policy/knob/volatility regime, the fraction of calls served from cache vs. the empirical stale-serve rate, fit and compare
  reduction-vs-staleness Pareto frontiers with bootstrap CIs, define and measure per-policy convergence (confirmed-staleness
  feedback events needed until the adapted parameter stabilizes within a tolerance band), and run paired statistical tests
  across episodes/seeds to render an explicit CONFIRMS/DISCONFIRMS verdict against the hypothesis's stated success criteria.
runpod_compute_profile: gpu
metrics_descriptions: |-
  INPUTS EXPECTED FROM THE EXPERIMENT ARTIFACT: a per-call event log (JSON/CSV/parquet) with, at minimum, one row per tool call carrying: episode_id, seed, volatility_regime, call_site_id (function+argument signature hash), timestamp/step_index, policy_name (fixed_ttl | d_ttl | aimd | freshcache_gate), knob_value (the specific TTL seconds / target-hit-rate / (a,b) AIMD pair / error-budget used for that run), served_from_cache (bool), spot_checked (bool, whether a live re-query was forced for this hit), ground_truth_stale (bool or null if not checked/not applicable — cache misses always execute live so are trivially non-stale), and, for adaptive policies, the current per-site adapted value (aimd window w_i, d-TTL's TTL_i, freshcache's fitted per-entry/tier staleness probability or threshold) logged at every update event.

  1) REDUCTION-VS-STALENESS OPERATING POINTS. For each (policy, knob_value, volatility_regime) triple, aggregate across episodes/seeds: cache_hit_fraction = served_from_cache / total_calls (redundant-call reduction); empirical_stale_rate = ground_truth_stale / spot_checked among served_from_cache rows, inverse-probability-reweighted by the spot-check sampling rate per call_site_id/time-bucket to correct for the fact that only a sampled subset of hits get a live re-query (report both the raw spot-checked-only rate and the reweighted estimate; note if they diverge materially, that is itself a validity finding). Bootstrap (≥2,000 resamples, resampling at the episode level to preserve within-episode correlation, not the row level) a 95% CI on both coordinates for every operating point.

  2) PARETO FRONTIER CONSTRUCTION AND COMPARISON. Per volatility regime, plot cache_hit_fraction (x) vs empirical_stale_rate (y) for every knob value swept per policy, connect each policy's own non-dominated points into its frontier, and report: (a) frontier-AUC (area under the reduction-axis integrated against the minimum achievable stale rate up to each hit-fraction level, via trapezoidal integration over the non-dominated point set) per policy per regime, with bootstrap CI; (b) a non-dominated-point count/fraction test — for each AIMD operating point, check whether any fixed-TTL or d-TTL point achieves both >= cache_hit_fraction and <= empirical_stale_rate (strict dominance), and report the fraction of AIMD points that are Pareto-dominated by each baseline; (c) at matched stale-rate targets (e.g., the same 3-5 stale-rate bands used in FreshCache's own per-tier error budgets: ~0.1%, 1%, 3.3%, 10%), report each policy's achieved cache_hit_fraction via linear interpolation between adjacent knob points on its own frontier, with bootstrap CI on the difference AIMD-vs-each-baseline.

  3) CONVERGENCE / SAMPLE-EFFICIENCY. Define stabilization per policy explicitly and apply the SAME tolerance-band logic uniformly: (a) AIMD -- per call_site_id, the window w_i is 'stabilized' at the first update step after which w_i stays within +/-10% of its own trailing-20-update mean for at least 10 consecutive updates (or the full remaining trace if fewer than 10 updates occur before the episode ends -- flag those sites as 'insufficient data' rather than silently excluding); record the number of confirmed-staleness feedback events (spot-checked hits with ground_truth_stale observed, valid or stale) consumed by that call_site_id up to the stabilization step. (b) d-TTL -- same tolerance-band rule applied to its adapted TTL_i trace. (c) FreshCache-style gate -- 'trustworthy calibration' operationalized as: the per-entry/tier fitted staleness-probability model's parameter estimates satisfy the same +/-10%/10-consecutive-update stability rule AND the number of labeled (spot-checked) observations feeding that entry/tier's model has crossed a minimum-sample floor (justify the floor from the model's own confidence-interval width, e.g. Wilson interval half-width < 0.05 on the fitted probability -- report the floor value used and why). Aggregate per policy: median and IQR of confirmed-staleness-events-to-convergence across call sites, stratified by call-site repeat-count bucket (low: <=5 occurrences/episode, medium: 6-20, high: >20) -- the low-repeat-count bucket is the hypothesis's central claim, so report it separately and explicitly, not just pooled. Report the fraction of call sites in each bucket that FAIL to converge/calibrate at all within the observed trace length, per policy -- this failure rate is itself a key result, especially for FreshCache in the low-repeat-count bucket.

  4) STATISTICAL TESTS FOR THE VERDICT. Paired (by episode+seed) Wilcoxon signed-rank tests (or paired bootstrap difference-in-means with BCa CIs if the sample of episodes is small, e.g. <20) comparing: AIMD's frontier-AUC vs fixed-TTL's and vs d-TTL's per volatility regime; AIMD's median convergence-events vs d-TTL's and vs FreshCache's, per repeat-count bucket. Apply Holm-Bonferroni correction across the family of these comparisons. Report effect sizes (rank-biserial correlation or standardized mean difference) alongside p-values, not p-values alone.

  5) EXPLICIT VERDICT MAPPING. Re-state the hypothesis's own CONFIRMS/DISCONFIRMS criteria as a checklist and mechanically mark each: (a) AIMD frontier comparable-or-better than fixed-TTL and d-TTL (non-dominated fraction >= baseline's, or frontier-AUC CI overlapping/exceeding, in >= half of volatility regimes) -- PASS/FAIL with the numbers cited; (b) AIMD converges using substantially fewer confirmed-staleness events than FreshCache needs to calibrate, specifically in the low-repeat-count bucket (report the ratio of medians and whether FreshCache's low-repeat-count non-convergence rate is materially higher) -- PASS/FAIL with numbers cited. State the overall verdict as CONFIRMS only if both (a) and (b) pass; otherwise DISCONFIRMS/MIXED with the specific criterion that failed named. If d-TTL turns out to dominate AIMD on the frontier, or AIMD needs comparable/more staleness feedback than FreshCache to stabilize, report this plainly as the hypothesis's own stated disconfirming outcome, not as an experiment failure.

  6) ROBUSTNESS AND VALIDITY CHECKS. (a) Sensitivity of the Pareto/convergence results to the spot-check sampling rate used in the experiment (if the experiment logged multiple spot-check rates or if it can be sub-sampled post hoc from a higher logged rate, recompute frontiers/convergence at a lower simulated spot-check rate to see whether AIMD's fewer-events advantage holds when feedback is even sparser -- this directly stress-tests the hypothesis's central low-data claim); (b) check for confounds between volatility regime and call-site repeat-count distribution (e.g. if high-volatility regimes happen to also have fewer repeats, stratify rather than pool); (c) sanity-check the FreshCache reimplementation's calibration quality independent of the comparison (e.g. reliability diagram / Brier score of its fitted staleness probabilities against ground truth on a held-out spot-check split) so a weak reimplementation isn't mistaken for a genuine mechanism-level finding -- report this as a caveat if the reimplementation underperforms the published FreshCache numbers materially; (d) report missingness -- how many call sites per policy/regime had zero spot-checks at all (making convergence undefined) and exclude them transparently rather than imputing.
metrics_justification: >-
  The hypothesis's success criteria are stated as two explicit, falsifiable comparisons: (a) AIMD's position on the reduction-vs-staleness
  frontier relative to fixed-TTL and d-TTL, and (b) AIMD's confirmed-staleness-feedback sample-efficiency to converge relative
  to FreshCache's sample requirement to calibrate, especially in the low-repeat-count regime that motivates the whole hypothesis.
  The Pareto-frontier-AUC and non-dominated-point metrics operationalize (a) directly as a single comparable number per regime
  while still preserving the full tradeoff curve (rather than collapsing to one arbitrary operating point, which would hide
  exactly the knob-sweep behavior the experiment was designed to produce). Bootstrap CIs at the episode level (not row level)
  are required because tool calls within an episode are correlated (repeated visits to the same call sites), so naive row-level
  resampling would understate variance and manufacture false significance. The convergence metric is defined identically (a
  tolerance-band stabilization rule) across all three adaptive policies so the comparison is apples-to-apples rather than
  each policy getting a favorable bespoke definition of 'ready' -- this matters because the whole hypothesis rests on AIMD
  needing fewer events, and a biased convergence definition could manufacture that result. Stratifying by call-site repeat-count
  bucket is essential rather than optional: the hypothesis is explicitly a claim about the low-repeat-count regime ('agent
  loops are exactly the setting where...many call sites are visited only a handful of times'), so a pooled-only result that
  averages over easy high-repeat sites would dilute or mask the very effect being tested. Paired statistical tests (by episode+seed)
  with multiple-comparison correction and effect sizes are needed because the plan compares several policy pairs across several
  regimes/buckets simultaneously, and unpaired or uncorrected tests would inflate false-positive risk on a hypothesis whose
  paper-worthy claim rests on these specific comparisons. The robustness checks -- spot-check-rate sensitivity, volatility/repeat-count
  confound check, and independent calibration-quality sanity check of the FreshCache reimplementation -- exist because the
  two closest prior mechanisms (FreshCache, d-TTL) are being reimplemented rather than run as published systems, so a null
  or negative result for AIMD must be distinguishable from a weak reimplementation of the baseline, and a positive result
  must be distinguishable from an artifact of how heavily the spot-check budget was set in the experiment.
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
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for evaluation metrics, agent orchestration patterns, benchmark design.

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
TODO 1. Use aii-json skill's format script with `--input eval_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to eval_out.json and full_eval_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "EvaluationExpectedFiles": {
      "description": "All expected output files from evaluation artifact.",
      "properties": {
        "script": {
          "description": "Path to eval.py script. Example: 'eval.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full evaluation JSON file. Example: 'full_eval_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini evaluation JSON file. Example: 'mini_eval_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview evaluation JSON file. Example: 'preview_eval_out.json'",
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
      "title": "EvaluationExpectedFiles",
      "type": "object"
    }
  },
  "description": "Evaluation artifact \u2014 structured output + file metadata.\n\nEvaluates both proposed and baseline methods with appropriate metrics.\nProduces eval.py and eval_out.json files.",
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
      "$ref": "#/$defs/EvaluationExpectedFiles",
      "description": "All output files you created. Must include eval.py script plus full/mini/preview evaluation JSON files."
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
  "title": "EvaluationArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [4] SYSTEM-USER prompt · 2026-08-09 23:25:53 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [5] SKILL-INPUT — aii-json · 2026-08-09 23:26:01 UTC

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

### [6] SKILL-INPUT — aii-file-size-limit · 2026-08-09 23:26:01 UTC

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
