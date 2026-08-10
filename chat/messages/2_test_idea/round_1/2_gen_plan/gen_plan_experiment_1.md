# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_MmmgOkQFZ5uI` — Does TCP-Style Reactive Caching Actually Beat Fitted Staleness Models?
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-08-09 22:52:23 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1
```

### [2] SYSTEM-USER prompt · 2026-08-09 22:52:29 UTC

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
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
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

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

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

id: experiment_iter1_dir2
type: experiment
objective: >-
  Implement and run the three core cache policies (fixed TTL swept, d-TTL-style stochastic-approximation hit-rate targeting,
  and the proposed AIMD reuse-window rule) plus a FreshCache-style fitted staleness-probability gate as an upper reference,
  replaying the volatility-labeled workload and logging every call's cache decision, spot-check outcome, and ground-truth
  validity.
approach: >-
  Reimplement Basu et al.'s d-TTL mechanism (Robbins-Monro-style TTL update toward a target hit rate) and a FreshCache-style
  per-entry staleness-probability model (e.g. exponential-decay/logistic fit against observed valid/stale outcomes with a
  fixed error budget), both ported to per-call-site agent traffic. Implement the AIMD rule: window w_i += a on confirmed-valid
  or presumed-valid hits (background spot-check rate controls how many hits get checked), w_i *= b (b<1) immediately on confirmed-stale
  hits, with floor/ceiling bounds. Replay the dataset's episodes through all four policies across all volatility regimes,
  sweeping each policy's tunable knob (TTL values / target hit rates / AIMD a,b pairs / error-budget levels), logging per-call
  cache-hit/miss decisions, ground-truth validity, and running counts of confirmed-staleness events consumed per call-site.
  Use OpenRouter only if any LLM-driven step is needed (e.g. simulating agent task variety); the core caching/statistics logic
  is pure Python and needs no LLM calls, keeping cost near $0.
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
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
  "description": "Plan for an EXPERIMENT artifact.",
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
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-08-09 22:52:29 UTC

```
Investigate whether a simple, well-specified caching strategy measurably reduces redundant LLM tool calls in an agent loop, and quantify the tradeoff against staleness.
```

### [4] TOOL CALL — Write · 2026-08-09 22:53:42 UTC

```
File: /ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json

{
  "title": "AIMD Cache Windows vs TTL Baselines for Agents",
  "summary": "Simulate an LLM agent tool-call loop with a versioned, volatility-labeled resource corpus, and implement four per-call-site caching policies -- fixed TTL, d-TTL-style stochastic-approximation hit-rate targeting, a FreshCache-style fitted staleness-probability gate, and the proposed AIMD reuse-window rule. Replay the same episode traces through all four policies across multiple volatility regimes and multiple knob settings each, logging every cache decision plus ground-truth validity, to produce (i) each policy's reduction-vs-staleness Pareto frontier and (ii) each adaptive policy's confirmed-staleness-events-to-convergence curve. This is pure Python/NumPy simulation logic -- no LLM calls are required for the core result, so cost is $0; OpenRouter is only touched optionally to diversify simulated task/query text.",
  "runpod_compute_profile": "cpu_light",
  "implementation_pseudocode": "# ============================================================\n# STAGE 0 -- Load dependency dataset\n# ============================================================\n# This experiment REQUIRES a DATASET dependency artifact providing the\n# versioned resource corpus + episode call traces + volatility schedule.\n# Load method_out.json (or equivalent) from the DATASET artifact's output.\n# Expected fields (adapt to whatever the actual dataset artifact emits --\n# inspect its schema first and fail loudly with a clear error if a required\n# field is absent, do not silently invent data):\n#   resources: {resource_id: {schedule: 'static'|'periodic'|'bursty', ...}}\n#   episodes: [ {episode_id, calls: [ {call_site_id (fn+arg signature hash),\n#                                       timestamp, resource_id, true_value_version} ] } ]\n#   volatility_regimes: list of regime labels each episode is tagged with\n# If the dataset artifact instead only gives raw resources/tools without\n# pre-simulated call traces, this experiment must itself run the simulated\n# agent loop (Stage 1) to generate traces -- do this only if traces are\n# genuinely absent from the dependency, not as a default.\n\n# ============================================================\n# STAGE 1 -- Agent-loop call harness (if traces not already in dataset)\n# ============================================================\ndef simulate_episode(resources, rng, n_calls, repeat_bias=0.6):\n    # Simulate an agent revisiting the same handful of call sites (file\n    # reads, repeated near-duplicate searches, repeated computations)\n    # with realistic skew: draw call_site from a Zipf-like distribution\n    # over a small per-episode working set so repeats actually occur.\n    working_set = rng.choice(list(resources), size=max(5, n_calls // 4), replace=False)\n    calls = []\n    t = 0.0\n    for _ in range(n_calls):\n        if rng.random() < repeat_bias and calls:\n            site = rng.choice([c['call_site_id'] for c in calls])\n        else:\n            site = rng.choice(working_set)\n        t += rng.exponential(scale=1.0)  # inter-call time, arbitrary sim units\n        true_version = resources[site].value_version_at(t)\n        calls.append({'call_site_id': site, 'timestamp': t, 'true_version': true_version})\n    return calls\n\nclass Resource:\n    # schedule in {'static', 'periodic', 'bursty'}\n    def value_version_at(self, t):\n        if self.schedule == 'static': return 0\n        if self.schedule == 'periodic': return int(t // self.period)\n        if self.schedule == 'bursty': return self.poisson_change_count(t)  # precompute change times, count how many precede t\n\n# Only invoke OpenRouter (aii-openrouter-llms skill) if task/query TEXT\n# diversity is needed for realism (e.g., generating varied search-query\n# strings for the 'repeated near-duplicate search' call type). This is\n# cosmetic content generation, NOT used for any cache-policy logic --\n# cap at a few hundred cheap calls (e.g. gpt-4o-mini or similar low-cost\n# OpenRouter model) well under $10, and skip entirely if the dataset\n# artifact already supplies call traces.\n\n# ============================================================\n# STAGE 2 -- Cache policy implementations (per call_site_id state)\n# ============================================================\n\nclass FixedTTLPolicy:\n    def __init__(self, ttl): self.ttl = ttl; self.cache = {}  # site -> (version, cached_at)\n    def on_call(self, site, t, true_version, spot_check_fn):\n        if site in self.cache:\n            version, cached_at = self.cache[site]\n            if t - cached_at <= self.ttl:\n                is_hit = True\n                # ground truth validity always computable in simulation (we know true_version)\n                valid = (version == true_version)\n                return 'hit', valid\n        self.cache[site] = (true_version, t)\n        return 'miss', True\n\nclass DTTLPolicy:\n    # Basu et al. 2017 (arXiv:1704.04448): Robbins-Monro update of TTL\n    # toward a target hit rate h*. On each request at a site, whether\n    # served as hit or miss, update:\n    #   ttl_i <- ttl_i + gamma_k * (observed_hit_indicator - h_target)\n    # with gamma_k = c / (k+1) (diminishing step size, k = update count\n    # for that site) per the paper's stochastic-approximation convergence\n    # argument. Clip ttl_i to [ttl_min, ttl_max].\n    def __init__(self, h_target, c=1.0, ttl_min=0.01, ttl_max=1e4, ttl_init=1.0):\n        self.h_target = h_target; self.c = c\n        self.ttl = defaultdict(lambda: ttl_init)\n        self.k = defaultdict(int)\n        self.cache = {}\n    def on_call(self, site, t, true_version, spot_check_fn):\n        hit_indicator = 0\n        valid = True\n        if site in self.cache:\n            version, cached_at = self.cache[site]\n            if t - cached_at <= self.ttl[site]:\n                hit_indicator = 1\n                valid = (version == true_version)\n        else:\n            valid = True\n        self.k[site] += 1\n        gamma = self.c / (self.k[site] + 1)\n        self.ttl[site] = clip(self.ttl[site] + gamma * (hit_indicator - self.h_target), ttl_min, ttl_max)\n        if hit_indicator == 0:\n            self.cache[site] = (true_version, t)\n        return ('hit' if hit_indicator else 'miss'), valid\n\nclass FreshCacheGatePolicy:\n    # Fitted per-call-site staleness-probability gate, ported from\n    # Mansoor/Ahmad/Yoon 2026 FreshCache's exponential-decay staleness\n    # model: P(stale | age=a) = 1 - exp(-lambda_i * a). Fit lambda_i per\n    # site via MLE/method-of-moments over observed (age, valid/stale)\n    # spot-check pairs collected so far for that site (needs several\n    # observations before it is meaningfully calibrated -- this is the\n    # exact 'requires labeled calibration data' property under test).\n    # Gate: serve from cache only if P(stale | age) <= error_budget.\n    def __init__(self, error_budget, lambda_prior=0.1, min_obs_to_fit=5):\n        self.error_budget = error_budget\n        self.lambda_est = defaultdict(lambda: lambda_prior)\n        self.obs = defaultdict(list)  # site -> [(age, was_stale)]\n        self.cache = {}\n    def predicted_stale_prob(self, site, age):\n        return 1 - math.exp(-self.lambda_est[site] * age)\n    def on_call(self, site, t, true_version, spot_check_fn):\n        if site in self.cache:\n            version, cached_at = self.cache[site]\n            age = t - cached_at\n            if self.predicted_stale_prob(site, age) <= self.error_budget:\n                valid = (version == true_version)\n                if spot_check_fn(site):  # background spot-check updates the fit\n                    self.obs[site].append((age, not valid))\n                    self._refit(site)\n                return 'hit', valid\n        self.cache[site] = (true_version, t)\n        return 'miss', True\n    def _refit(self, site):\n        # MLE for exponential rate from (age, stale) pairs; refit only once\n        # min_obs_to_fit observations exist, else keep the prior lambda.\n        ...\n\nclass AIMDPolicy:\n    # THE PROPOSED METHOD.\n    # w_i: reuse WINDOW (units = simulation time, analogous to a TTL but\n    # driven by outcomes not fit). a = additive increase step,\n    # b in (0,1) = multiplicative decrease factor, floor/ceiling bounds.\n    def __init__(self, a, b, w_min=0.01, w_max=1e4, w_init=1.0, spot_check_rate=0.2):\n        self.a = a; self.b = b; self.w_min = w_min; self.w_max = w_max\n        self.w = defaultdict(lambda: w_init)\n        self.cache = {}\n        self.spot_check_rate = spot_check_rate\n        self.confirmed_stale_count = defaultdict(int)\n        self.confirmed_valid_count = defaultdict(int)\n    def on_call(self, site, t, true_version, spot_check_fn):\n        if site in self.cache:\n            version, cached_at = self.cache[site]\n            if t - cached_at <= self.w[site]:\n                valid = (version == true_version)\n                checked = spot_check_fn(site)  # bernoulli(spot_check_rate) in simulation\n                if checked:\n                    if valid:\n                        self.w[site] = min(self.w[site] + self.a, self.w_max)\n                        self.confirmed_valid_count[site] += 1\n                    else:\n                        self.w[site] = max(self.w[site] * self.b, self.w_min)\n                        self.confirmed_stale_count[site] += 1\n                # presumed-valid unchecked hits: leave window unchanged\n                # (conservative variant) -- ALSO run an ablation variant\n                # where unchecked hits get a smaller additive bump\n                # (a * presumed_valid_weight, e.g. 0.25*a) to test\n                # sensitivity to this design choice.\n                return 'hit', valid\n        self.cache[site] = (true_version, t)\n        return 'miss', True\n\n# ============================================================\n# STAGE 3 -- Replay driver\n# ============================================================\nPOLICY_GRID = {\n    'fixed_ttl':   [FixedTTLPolicy(ttl=v) for v in [0.5, 1, 2, 4, 8, 16, 32]],\n    'd_ttl':       [DTTLPolicy(h_target=h, c=c) for h in [0.5,0.6,0.7,0.8,0.9] for c in [0.5,1.0,2.0]],\n    'freshcache':  [FreshCacheGatePolicy(error_budget=e) for e in [0.05,0.10,0.20,0.35]],\n    'aimd':        [AIMDPolicy(a=a, b=b) for a in [0.25,0.5,1.0,2.0] for b in [0.3,0.5,0.7]],\n}\n\nresults = []\nfor regime in volatility_regimes:\n    for policy_family, policy_instances in POLICY_GRID.items():\n        for policy in policy_instances:\n            policy_state = fresh_copy(policy)  # reset per-episode-set state per (regime, knob) run\n            log = []\n            for episode in episodes_in_regime(regime):\n                for call in episode['calls']:\n                    decision, valid = policy_state.on_call(\n                        call['call_site_id'], call['timestamp'], call['true_version'],\n                        spot_check_fn=make_spot_checker(rate=SPOT_CHECK_RATE, rng=rng))\n                    log.append({'site': call['call_site_id'], 'decision': decision, 'valid': valid,\n                                'stale_events_so_far': cumulative_stale_count(policy_state, call['call_site_id'])})\n            hit_rate = fraction(log, lambda r: r['decision']=='hit')\n            stale_rate = fraction(log, lambda r: r['decision']=='hit' and not r['valid'])\n            convergence_point = find_convergence_index(log, policy_family)  # see Stage 4\n            results.append({'regime': regime, 'policy_family': policy_family,\n                             'knob': describe_knob(policy), 'hit_rate': hit_rate,\n                             'stale_rate': stale_rate, 'convergence_events': convergence_point})\n\n# ============================================================\n# STAGE 4 -- Convergence detection (only meaningful for adaptive policies)\n# ============================================================\ndef find_convergence_index(log, policy_family):\n    # For d_ttl / aimd / freshcache: track the per-site window/ttl/lambda\n    # trajectory over time; define 'converged' as the first point after\n    # which the value stays within +/-10% of its own trailing mean for\n    # the rest of the episode set (a simple rolling-band stability test).\n    # Report convergence in units of CONFIRMED-STALENESS FEEDBACK EVENTS\n    # consumed up to that point (not raw calls), since that is the\n    # hypothesis's actual currency. For freshcache, additionally report\n    # whether min_obs_to_fit was ever reached per site (some low-repeat\n    # sites may NEVER calibrate -- this is an expected, reportable failure\n    # mode, not a bug).\n    ...\n\n# ============================================================\n# STAGE 5 -- Frontier + comparison outputs\n# ============================================================\n# For each (regime, policy_family): sort knob sweep points by hit_rate,\n# take the Pareto-efficient subset (max hit_rate for given stale_rate).\n# Compute frontier dominance: for each aimd point, does some d_ttl/fixed\n# point dominate it (>= hit_rate AND <= stale_rate)? Aggregate a\n# 'fraction of aimd points non-dominated' summary per regime.\n# Compare median/IQR of convergence_events across policy families,\n# per regime, especially in a LOW-REPEAT-COUNT sub-slice of episodes\n# (call sites visited <= 5 times) -- this is the decisive regime named\n# in success_criteria.\n\n# ============================================================\n# STAGE 6 -- Write method_out.json\n# ============================================================\n# {\n#   'per_run_results': results,                # full grid, all regimes/knobs\n#   'frontiers': {regime: {policy_family: [(hit_rate, stale_rate), ...]}},\n#   'dominance_summary': {...},\n#   'convergence_summary': {regime: {policy_family: {median, p10, p90}}},\n#   'low_repeat_slice_summary': {...},          # the headline comparison\n#   'ablations': {'aimd_presumed_valid_weight': [...], 'spot_check_rate_sensitivity': [...]},\n#   'config': {grid definitions, rng seeds, spot_check_rate, n_episodes, ...},\n#   'verdict': 'CONFIRMS' | 'DISCONFIRMS' | 'MIXED',   # per success_criteria (a) and (b) separately\n# }",
  "fallback_plan": "1) If the dependency DATASET artifact does not already contain pre-simulated agent call traces with a controllable volatility schedule (only raw resources/tools), fall back to generating the traces in-house inside this experiment using Stage 1's pure-Python simulator (Zipf-skewed call-site revisits over a small per-episode working set, resources with static/periodic/bursty version-change schedules) -- this needs no LLM calls and no dataset beyond a list of resource IDs, so it degrades gracefully to a fully synthetic but still controllable workload. 2) If Basu et al.'s exact d-TTL update is ambiguous or its provable-convergence step-size schedule (gamma_k = c/(k+1)) proves numerically unstable (oscillation, divergence) on this shorter agent-episode traffic (their paper assumes CDN-scale request volume, orders of magnitude more requests per object than an agent call site gets), document the instability as a finding rather than hiding it, and additionally report a simplified fixed-step EWMA-toward-target-hit-rate variant as a secondary, better-behaved SOTA-adaptive baseline so the AIMD-vs-adaptive-baseline comparison is not vacated by one baseline collapsing. 3) If the FreshCache-style fit never reaches min_obs_to_fit for most call sites (very plausible given the low-repeat-count regime is the whole point), this is not a failure to fix -- it IS the expected result supporting the hypothesis; report the fraction of sites that never calibrate as a headline number, alongside a version of FreshCache with a shared cross-site prior (partial pooling of lambda across all sites of the same resource-schedule type) as a fairer reference so the comparison isn't a strawman. 4) If ground-truth validity is expensive/impossible to compute for some resource type, restrict volatility injection to schedules where ground truth is always analytically known (as in Stage 1's Resource classes) rather than trying to reconstruct it after the fact. 5) If the full knob grid (7 TTL x 15 d-TTL x 4 freshcache x 12 AIMD x N regimes) is too slow, first cut grid density (fewer knob values) before cutting episode count or regime count -- convergence-speed and frontier-shape claims need enough episodes per cell, not enough knob resolution. 6) If time runs short, prioritize completing all four policies on ONE volatility regime with a full knob sweep and convergence analysis before adding more regimes -- a complete single-regime comparison is a valid, reportable result; a partial multi-regime sweep with missing cells is not.",
  "testing_plan": "1) Unit-test each policy class in isolation on a tiny hand-constructed trace (e.g., 20 calls to 2 sites with a known version-change schedule) and manually verify the expected cache hit/miss/window trajectory by hand-computation before running any large sweep -- especially verify AIMD's window actually grows on repeated confirmed-valid hits and collapses sharply after an injected confirmed-stale hit, and that d-TTL's TTL moves toward target hit rate over enough iterations on a synthetic all-static (never-stale) resource. 2) Run one mini end-to-end pass: 1 regime, 2-3 episodes, 1 knob value per policy family, confirm method_out.json fields populate without errors and hit_rate/stale_rate are in [0,1] and sane (e.g., fixed TTL=0 should give ~0% hit rate; TTL=infinity on a fully static resource should give ~100% hit rate and 0% stale rate -- these are sanity boundary checks, verify them explicitly). 3) Check for a known pathology before scaling: AIMD window collapsing to w_min and never recovering (should recover via additive increase after enough confirmed-valid hits -- verify this happens within a bounded number of calls in the mini test) and d-TTL oscillating without settling (plot/print the TTL trajectory for a few sites in the mini run and inspect). 4) Verify the low-repeat-count slice logic on synthetic data with call sites visited exactly 3-5 times, confirming FreshCache's fit legitimately fails to calibrate there (lambda stays at prior) while AIMD's window has visibly moved from its init value -- this is the core hypothesis mechanism and must be checked BEFORE trusting full-scale numbers. 5) Only after all mini checks pass, scale to the full regime x knob-grid x episode-count sweep, and re-run the same boundary sanity checks (TTL=0 and TTL=infinity behavior) on the full run as a regression check that nothing broke when scaling up."
}
```

### [5] TOOL RESULT — Write · 2026-08-09 22:53:42 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"AIMD Cache Windows vs TTL Baselines for Agents\",\n  \"summary\": \"Simulate an LLM agent tool-call loop with a versioned, volatility-labeled resource corpus, and implement four per-call-site caching policies -- fixed TTL, d-TTL-style stochastic-approximation hit-rate targeting, a FreshCache-style fitted staleness-probability gate, and the proposed AIMD reuse-window rule. Replay the same episode traces through all four policies across multiple volatility regimes and multiple knob settings each, logging every cache decision plus ground-truth validity, to produce (i) each policy's reduction-vs-staleness Pareto frontier and (ii) each adaptive policy's confirmed-staleness-events-to-convergence curve. This is pure Python/NumPy simulation logic -- no LLM calls are required for the core result, so cost is $0; OpenRouter is only touched optionally to diversify simulated task/query text.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"implementation_pseudocode\": \"# ============================================================\\n# STAGE 0 -- Load dependency dataset\\n# ============================================================\\n# This experiment REQUIRES a DATASET dependency artifact providing the\\n# versioned resource corpus + episode call traces + volatility schedule.\\n# Load method_out.json (or equivalent) from the DATASET artifact's output.\\n# Expected fields (adapt to whatever the actual dataset artifact emits --\\n# inspect its schema first and fail loudly with a clear error if a required\\n# field is absent, do not silently invent data):\\n#   resources: {resource_id: {schedule: 'static'|'periodic'|'bursty', ...}}\\n#   episodes: [ {episode_id, calls: [ {call_site_id (fn+arg signature hash),\\n#                                       timestamp, resource_id, true_value_version} ] } ]\\n#   volatility_regimes: list of regime labels each episode is tagged with\\n# If the dataset artifact instead only gives raw resources/tools without\\n# pre-simulated call traces, this experiment must itself run the simulated\\n# agent loop (Stage 1) to generate traces -- do this only if traces are\\n# genuinely absent from the dependency, not as a default.\\n\\n# ============================================================\\n# STAGE 1 -- Agent-loop call harness (if traces not already in dataset)\\n# ============================================================\\ndef simulate_episode(resources, rng, n_calls, repeat_bias=0.6):\\n    # Simulate an agent revisiting the same handful of call sites (file\\n    # reads, repeated near-duplicate searches, repeated computations)\\n    # with realistic skew: draw call_site from a Zipf-like distribution\\n    # over a small per-episode working set so repeats actually occur.\\n    working_set = rng.choice(list(resources), size=max(5, n_calls // 4), replace=False)\\n    calls = []\\n    t = 0.0\\n    for _ in range(n_calls):\\n        if rng.random() < repeat_bias and calls:\\n            site = rng.choice([c['call_site_id'] for c in calls])\\n        else:\\n            site = rng.choice(working_set)\\n        t += rng.exponential(scale=1.0)  # inter-call time, arbitrary sim units\\n        true_version = resources[site].value_version_at(t)\\n        calls.append({'call_site_id': site, 'timestamp': t, 'true_version': true_version})\\n    return calls\\n\\nclass Resource:\\n    # schedule in {'static', 'periodic', 'bursty'}\\n    def value_version_at(self, t):\\n        if self.schedule == 'static': return 0\\n        if self.schedule == 'periodic': return int(t // self.period)\\n        if self.schedule == 'bursty': return self.poisson_change_count(t)  # precompute change times, count how many precede t\\n\\n# Only invoke OpenRouter (aii-openrouter-llms skill) if task/query TEXT\\n# diversity is needed for realism (e.g., generating varied search-query\\n# strings for the 'repeated near-duplicate search' call type). This is\\n# cosmetic content generation, NOT used for any cache-policy logic --\\n# cap at a few hundred cheap calls (e.g. gpt-4o-mini or similar low-cost\\n# OpenRouter model) well under $10, and skip entirely if the dataset\\n# artifact already supplies call traces.\\n\\n# ============================================================\\n# STAGE 2 -- Cache policy implementations (per call_site_id state)\\n# ============================================================\\n\\nclass FixedTTLPolicy:\\n    def __init__(self, ttl): self.ttl = ttl; self.cache = {}  # site -> (version, cached_at)\\n    def on_call(self, site, t, true_version, spot_check_fn):\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.ttl:\\n                is_hit = True\\n                # ground truth validity always computable in simulation (we know true_version)\\n                valid = (version == true_version)\\n                return 'hit', valid\\n        self.cache[site] = (true_version, t)\\n        return 'miss', True\\n\\nclass DTTLPolicy:\\n    # Basu et al. 2017 (arXiv:1704.04448): Robbins-Monro update of TTL\\n    # toward a target hit rate h*. On each request at a site, whether\\n    # served as hit or miss, update:\\n    #   ttl_i <- ttl_i + gamma_k * (observed_hit_indicator - h_target)\\n    # with gamma_k = c / (k+1) (diminishing step size, k = update count\\n    # for that site) per the paper's stochastic-approximation convergence\\n    # argument. Clip ttl_i to [ttl_min, ttl_max].\\n    def __init__(self, h_target, c=1.0, ttl_min=0.01, ttl_max=1e4, ttl_init=1.0):\\n        self.h_target = h_target; self.c = c\\n        self.ttl = defaultdict(lambda: ttl_init)\\n        self.k = defaultdict(int)\\n        self.cache = {}\\n    def on_call(self, site, t, true_version, spot_check_fn):\\n        hit_indicator = 0\\n        valid = True\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.ttl[site]:\\n                hit_indicator = 1\\n                valid = (version == true_version)\\n        else:\\n            valid = True\\n        self.k[site] += 1\\n        gamma = self.c / (self.k[site] + 1)\\n        self.ttl[site] = clip(self.ttl[site] + gamma * (hit_indicator - self.h_target), ttl_min, ttl_max)\\n        if hit_indicator == 0:\\n            self.cache[site] = (true_version, t)\\n        return ('hit' if hit_indicator else 'miss'), valid\\n\\nclass FreshCacheGatePolicy:\\n    # Fitted per-call-site staleness-probability gate, ported from\\n    # Mansoor/Ahmad/Yoon 2026 FreshCache's exponential-decay staleness\\n    # model: P(stale | age=a) = 1 - exp(-lambda_i * a). Fit lambda_i per\\n    # site via MLE/method-of-moments over observed (age, valid/stale)\\n    # spot-check pairs collected so far for that site (needs several\\n    # observations before it is meaningfully calibrated -- this is the\\n    # exact 'requires labeled calibration data' property under test).\\n    # Gate: serve from cache only if P(stale | age) <= error_budget.\\n    def __init__(self, error_budget, lambda_prior=0.1, min_obs_to_fit=5):\\n        self.error_budget = error_budget\\n        self.lambda_est = defaultdict(lambda: lambda_prior)\\n        self.obs = defaultdict(list)  # site -> [(age, was_stale)]\\n        self.cache = {}\\n    def predicted_stale_prob(self, site, age):\\n        return 1 - math.exp(-self.lambda_est[site] * age)\\n    def on_call(self, site, t, true_version, spot_check_fn):\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            age = t - cached_at\\n            if self.predicted_stale_prob(site, age) <= self.error_budget:\\n                valid = (version == true_version)\\n                if spot_check_fn(site):  # background spot-check updates the fit\\n                    self.obs[site].append((age, not valid))\\n                    self._refit(site)\\n                return 'hit', valid\\n        self.cache[site] = (true_version, t)\\n        return 'miss', True\\n    def _refit(self, site):\\n        # MLE for exponential rate from (age, stale) pairs; refit only once\\n        # min_obs_to_fit observations exist, else keep the prior lambda.\\n        ...\\n\\nclass AIMDPolicy:\\n    # THE PROPOSED METHOD.\\n    # w_i: reuse WINDOW (units = simulation time, analogous to a TTL but\\n    # driven by outcomes not fit). a = additive increase step,\\n    # b in (0,1) = multiplicative decrease factor, floor/ceiling bounds.\\n    def __init__(self, a, b, w_min=0.01, w_max=1e4, w_init=1.0, spot_check_rate=0.2):\\n        self.a = a; self.b = b; self.w_min = w_min; self.w_max = w_max\\n        self.w = defaultdict(lambda: w_init)\\n        self.cache = {}\\n        self.spot_check_rate = spot_check_rate\\n        self.confirmed_stale_count = defaultdict(int)\\n        self.confirmed_valid_count = defaultdict(int)\\n    def on_call(self, site, t, true_version, spot_check_fn):\\n        if site in self.cache:\\n            version, cached_at = self.cache[site]\\n            if t - cached_at <= self.w[site]:\\n                valid = (version == true_version)\\n                checked = spot_check_fn(site)  # bernoulli(spot_check_rate) in simulation\\n                if checked:\\n                    if valid:\\n                        self.w[site] = min(self.w[site] + self.a, self.w_max)\\n                        self.confirmed_valid_count[site] += 1\\n                    else:\\n                        self.w[site] = max(self.w[site] * self.b, self.w_min)\\n                        self.confirmed_stale_count[site] += 1\\n                # presumed-valid unchecked hits: leave window unchanged\\n                # (conservative variant) -- ALSO run an ablation variant\\n                # where unchecked hits get a smaller additive bump\\n                # (a * presumed_valid_weight, e.g. 0.25*a) to test\\n                # sensitivity to this design choice.\\n                return 'hit', valid\\n        self.cache[site] = (true_version, t)\\n        return 'miss', True\\n\\n# ============================================================\\n# STAGE 3 -- Replay driver\\n# ============================================================\\nPOLICY_GRID = {\\n    'fixed_ttl':   [FixedTTLPolicy(ttl=v) for v in [0.5, 1, 2, 4, 8, 16, 32]],\\n    'd_ttl':       [DTTLPolicy(h_target=h, c=c) for h in [0.5,0.6,0.7,0.8,0.9] for c in [0.5,1.0,2.0]],\\n    'freshcache':  [FreshCacheGatePolicy(error_budget=e) for e in [0.05,0.10,0.20,0.35]],\\n    'aimd':        [AIMDPolicy(a=a, b=b) for a in [0.25,0.5,1.0,2.0] for b in [0.3,0.5,0.7]],\\n}\\n\\nresults = []\\nfor regime in volatility_regimes:\\n    for policy_family, policy_instances in POLICY_GRID.items():\\n        for policy in policy_instances:\\n            policy_state = fresh_copy(policy)  # reset per-episode-set state per (regime, knob) run\\n            log = []\\n            for episode in episodes_in_regime(regime):\\n                for call in episode['calls']:\\n                    decision, valid = policy_state.on_call(\\n                        call['call_site_id'], call['timestamp'], call['true_version'],\\n                        spot_check_fn=make_spot_checker(rate=SPOT_CHECK_RATE, rng=rng))\\n                    log.append({'site': call['call_site_id'], 'decision': decision, 'valid': valid,\\n                                'stale_events_so_far': cumulative_stale_count(policy_state, call['call_site_id'])})\\n            hit_rate = fraction(log, lambda r: r['decision']=='hit')\\n            stale_rate = fraction(log, lambda r: r['decision']=='hit' and not r['valid'])\\n            convergence_point = find_convergence_index(log, policy_family)  # see Stage 4\\n            results.append({'regime': regime, 'policy_family': policy_family,\\n                             'knob': describe_knob(policy), 'hit_rate': hit_rate,\\n                             'stale_rate': stale_rate, 'convergence_events': convergence_point})\\n\\n# ============================================================\\n# STAGE 4 -- Convergence detection (only meaningful for adaptive policies)\\n# ============================================================\\ndef find_convergence_index(log, policy_family):\\n    # For d_ttl / aimd / freshcache: track the per-site window/ttl/lambda\\n    # trajectory over time; define 'converged' as the first point after\\n    # which the value stays within +/-10% of its own trailing mean for\\n    # the rest of the episode set (a simple rolling-band stability test).\\n    # Report convergence in units of CONFIRMED-STALENESS FEEDBACK EVENTS\\n    # consumed up to that point (not raw calls), since that is the\\n    # hypothesis's actual currency. For freshcache, additionally report\\n    # whether min_obs_to_fit was ever reached per site (some low-repeat\\n    # sites may NEVER calibrate -- this is an expected, reportable failure\\n    # mode, not a bug).\\n    ...\\n\\n# ============================================================\\n# STAGE 5 -- Frontier + comparison outputs\\n# ============================================================\\n# For each (regime, policy_family): sort knob sweep points by hit_rate,\\n# take the Pareto-efficient subset (max hit_rate for given stale_rate).\\n# Compute frontier dominance: for each aimd point, does some d_ttl/fixed\\n# point dominate it (>= hit_rate AND <= stale_rate)? Aggregate a\\n# 'fraction of aimd points non-dominated' summary per regime.\\n# Compare median/IQR of convergence_events across policy families,\\n# per regime, especially in a LOW-REPEAT-COUNT sub-slice of episodes\\n# (call sites visited <= 5 times) -- this is the decisive regime named\\n# in success_criteria.\\n\\n# ============================================================\\n# STAGE 6 -- Write method_out.json\\n# ============================================================\\n# {\\n#   'per_run_results': results,                # full grid, all regimes/knobs\\n#   'frontiers': {regime: {policy_family: [(hit_rate, stale_rate), ...]}},\\n#   'dominance_summary': {...},\\n#   'convergence_summary': {regime: {policy_family: {median, p10, p90}}},\\n#   'low_repeat_slice_summary': {...},          # the headline comparison\\n#   'ablations': {'aimd_presumed_valid_weight': [...], 'spot_check_rate_sensitivity': [...]},\\n#   'config': {grid definitions, rng seeds, spot_check_rate, n_episodes, ...},\\n#   'verdict': 'CONFIRMS' | 'DISCONFIRMS' | 'MIXED',   # per success_criteria (a) and (b) separately\\n# }\",\n  \"fallback_plan\": \"1) If the dependency DATASET artifact does not already contain pre-simulated agent call traces with a controllable volatility schedule (only raw resources/tools), fall back to generating the traces in-house inside this experiment using Stage 1's pure-Python simulator (Zipf-skewed call-site revisits over a small per-episode working set, resources with static/periodic/bursty version-change schedules) -- this needs no LLM calls and no dataset beyond a list of resource IDs, so it degrades gracefully to a fully synthetic but still controllable workload. 2) If Basu et al.'s exact d-TTL update is ambiguous or its provable-convergence step-size schedule (gamma_k = c/(k+1)) proves numerically unstable (oscillation, divergence) on this shorter agent-episode traffic (their paper assumes CDN-scale request volume, orders of magnitude more requests per object than an agent call site gets), document the instability as a finding rather than hiding it, and additionally report a simplified fixed-step EWMA-toward-target-hit-rate variant as a secondary, better-behaved SOTA-adaptive baseline so the AIMD-vs-adaptive-baseline comparison is not vacated by one baseline collapsing. 3) If the FreshCache-style fit never reaches min_obs_to_fit for most call sites (very plausible given the low-repeat-count regime is the whole point), this is not a failure to fix -- it IS the expected result supporting the hypothesis; report the fraction of sites that never calibrate as a headline number, alongside a version of FreshCache with a shared cross-site prior (partial pooling of lambda across all sites of the same resource-schedule type) as a fairer reference so the comparison isn't a strawman. 4) If ground-truth validity is expensive/impossible to compute for some resource type, restrict volatility injection to schedules where ground truth is always analytically known (as in Stage 1's Resource classes) rather than trying to reconstruct it after the fact. 5) If the full knob grid (7 TTL x 15 d-TTL x 4 freshcache x 12 AIMD x N regimes) is too slow, first cut grid density (fewer knob values) before cutting episode count or regime count -- convergence-speed and frontier-shape claims need enough episodes per cell, not enough knob resolution. 6) If time runs short, prioritize completing all four policies on ONE volatility regime with a full knob sweep and convergence analysis before adding more regimes -- a complete single-regime comparison is a valid, reportable result; a partial multi-regime sweep with missing cells is not.\",\n  \"testing_plan\": \"1) Unit-test each policy class in isolation on a tiny hand-constructed trace (e.g., 20 calls to 2 sites with a known version-change schedule) and manually verify the expected cache hit/miss/window trajectory by hand-computation before running any large sweep -- especially verify AIMD's window actually grows on repeated confirmed-valid hits and collapses sharply after an injected confirmed-stale hit, and that d-TTL's TTL moves toward target hit rate over enough iterations on a synthetic all-static (never-stale) resource. 2) Run one mini end-to-end pass: 1 regime, 2-3 episodes, 1 knob value per policy family, confirm method_out.json fields populate without errors and hit_rate/stale_rate are in [0,1] and sane (e.g., fixed TTL=0 should give ~0% hit rate; TTL=infinity on a fully static resource should give ~100% hit rate and 0% stale rate -- these are sanity boundary checks, verify them explicitly). 3) Check for a known pathology before scaling: AIMD window collapsing to w_min and never recovering (should recover via additive increase after enough confirmed-valid hits -- verify this happens within a bounded number of calls in the mini test) and d-TTL oscillating without settling (plot/print the TTL trajectory for a few sites in the mini run and inspect). 4) Verify the low-repeat-count slice logic on synthetic data with call sites visited exactly 3-5 times, confirming FreshCache's fit legitimately fails to calibrate there (lambda stays at prior) while AIMD's window has visibly moved from its init value -- this is the core hypothesis mechanism and must be checked BEFORE trusting full-scale numbers. 5) Only after all mini checks pass, scale to the full regime x knob-grid x episode-count sweep, and re-run the same boundary sanity checks (TTL=0 and TTL=infinity behavior) on the full run as a regression check that nothing broke when scaling up.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-08-09 22:53:44 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json` — an AIMD cache-window vs fixed-TTL/d-TTL/FreshCache experiment plan with full pseudocode for all four policies, a replay/sweep driver, convergence-detection logic, fallback strategies, and a staged testing plan.
```
