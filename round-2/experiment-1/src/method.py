#!/usr/bin/env python3
"""Cache-policy replay comparison over a real-content versioned corpus + a synthetic Zipf simulator.

Implements 5 cache policies (fixed TTL, literal d-TTL, EWMA-adaptive TTL, FreshCache
hazard-gate [raw + resource-class-pooled variants], AIMD window) and replays them against
a per-call event stream reconstructed from the versioned-resource corpus produced upstream
(art_T0onLH9xokqw), plus an explicit synthetic Zipf-popularity simulator run side-by-side
(not as a silent fallback). Output is written in exp_gen_sol_out.json schema: one row per
(data_source, policy, knob, spot_check_rate, seed) replicate, with aggregate hit-rate /
staleness metrics needed downstream to build Pareto frontiers and Wilson-interval CIs.
"""

import argparse
import json
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WORKSPACE = Path(__file__).parent
DEP_WORKSPACE = Path(
    "/ai-inventor/aii_data/runs/run_MmmgOkQFZ5uI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1"
)


# ---------------------------------------------------------------------------
# 0. Loud, fail-fast dependency load (fixes iter-1's silent-synthetic-fallback bug)
# ---------------------------------------------------------------------------
def resolve_dependency_path(filename: str) -> Path:
    env_key = "DEP_ART_T0onLH9xokqw_FULL_DATA"
    candidates = []
    if os.environ.get(env_key):
        candidates.append(Path(os.environ[env_key]))
    candidates.append(DEP_WORKSPACE / filename)
    for c in candidates:
        logger.info(f"Checking dependency candidate path: {c}")
        if c.exists():
            logger.info(f"Resolved dependency file at: {c}")
            return c
    raise FileNotFoundError(
        f"HARD FAIL: could not locate {filename} for dependency art_T0onLH9xokqw. "
        f"Tried: {[str(c) for c in candidates]}. This is a genuine infra/wiring bug -- "
        f"do NOT silently fall back to synthetic-only data."
    )


def load_real_corpus(filename: str = "full_data_out.json"):
    dep_path = resolve_dependency_path(filename)
    raw = json.loads(dep_path.read_text())
    assert isinstance(raw, dict) and "datasets" in raw, (
        f"HARD FAIL: unexpected schema shape in {dep_path}: "
        f"top-level keys={list(raw)[:10] if isinstance(raw, dict) else type(raw)}"
    )
    rows = []
    for ds in raw["datasets"]:
        rows.extend(ds["examples"])
    logger.info(f"Loaded {len(rows)} real-content rows from {dep_path}")
    if filename == "full_data_out.json":
        assert len(rows) >= 5000, (
            f"HARD FAIL: expected ~5307 rows, got {len(rows)} -- dependency file looks truncated/wrong"
        )
    return rows, dep_path


def parse_rows_into_episodes(rows):
    episodes = defaultdict(list)
    resource_schedules = {}
    regime_counts = defaultdict(int)
    malformed = 0
    for r in rows:
        try:
            inp = json.loads(r["input"])
            sched = json.loads(r["metadata_version_schedule"])
        except (json.JSONDecodeError, KeyError):
            malformed += 1
            continue
        resource_schedules[inp["resource_id"]] = sched
        regime = r["metadata_volatility_regime"]
        regime_counts[regime] += 1
        episodes[inp["episode_id"]].append(
            {
                "call_index": inp["call_index"],
                "timestamp_tick": inp["timestamp_tick"],
                "call_site_signature": inp["call_site_signature"],
                "resource_id": inp["resource_id"],
                "ground_truth_version_id": r["output"],
                "volatility_regime": regime,
                "resource_class": r["metadata_resource_class"],
            }
        )
    frac_malformed = malformed / max(1, len(rows))
    if frac_malformed > 0.01:
        logger.warning(
            f"{malformed}/{len(rows)} ({frac_malformed:.1%}) rows failed to parse -- "
            f"exceeds 1% threshold, but continuing with the rows that did parse."
        )
    for ep in episodes:
        episodes[ep].sort(key=lambda c: (c["timestamp_tick"], c["call_index"]))
    logger.info(f"Parsed {len(episodes)} episodes, {len(resource_schedules)} resources")
    logger.info(f"Volatility regime distribution: {dict(regime_counts)}")
    missing_regimes = {"static", "periodic", "bursty"} - set(regime_counts)
    if missing_regimes:
        logger.warning(f"Missing volatility regimes in parsed data: {missing_regimes}")
    return dict(episodes), resource_schedules


# ---------------------------------------------------------------------------
# 1. Synthetic Zipf-popularity simulator (explicit secondary run, not a fallback)
# ---------------------------------------------------------------------------
def build_synthetic_zipf_episodes(seed: int = 12345, n_episodes: int = 30, sim_days: int = 30):
    rng = random.Random(seed)
    n_resources_per_regime = {"static": 90, "periodic": 60, "bursty": 20}
    resource_schedules = {}
    resource_meta = {}
    rid_counter = 0
    for regime, n_res in n_resources_per_regime.items():
        for _ in range(n_res):
            rid = f"synth_{regime}_{rid_counter:04d}"
            rid_counter += 1
            if regime == "static":
                sched = [
                    {
                        "version_id": f"{rid}_v0",
                        "content_hash": "synthetic",
                        "valid_from_tick": 0,
                        "valid_until_tick": sim_days - 1,
                    }
                ]
            elif regime == "periodic":
                period = rng.choice([3, 5, 7])
                sched = []
                t = 0
                v = 0
                while t <= sim_days - 1:
                    nxt = min(sim_days - 1, t + period - 1)
                    sched.append(
                        {
                            "version_id": f"{rid}_v{v}",
                            "content_hash": "synthetic",
                            "valid_from_tick": t,
                            "valid_until_tick": nxt,
                        }
                    )
                    t = nxt + 1
                    v += 1
            else:  # bursty: heavy-tailed irregular intervals (Pareto-ish via exponential mix)
                sched = []
                t = 0
                v = 0
                while t <= sim_days - 1:
                    gap = max(1, int(rng.expovariate(1 / 2.0)))
                    nxt = min(sim_days - 1, t + gap - 1)
                    sched.append(
                        {
                            "version_id": f"{rid}_v{v}",
                            "content_hash": "synthetic",
                            "valid_from_tick": t,
                            "valid_until_tick": nxt,
                        }
                    )
                    t = nxt + 1
                    v += 1
            resource_schedules[rid] = sched
            resource_meta[rid] = regime
    resource_ids = list(resource_schedules.keys())

    def version_at(rid, tick):
        for entry in resource_schedules[rid]:
            if entry["valid_from_tick"] <= tick <= entry["valid_until_tick"]:
                return entry["version_id"]
        return resource_schedules[rid][-1]["version_id"]

    # Zipf popularity ranking over resources -> episodes draw with Zipf(s=1.2) weights
    ranks = list(range(1, len(resource_ids) + 1))
    weights = [1.0 / (r ** 1.2) for r in ranks]
    total_w = sum(weights)
    probs = [w / total_w for w in weights]

    episodes = defaultdict(list)
    for ep_i in range(n_episodes):
        ep_id = f"synth_ep_{ep_i:03d}"
        n_resources_in_ep = rng.randint(10, 20)
        chosen = rng.choices(resource_ids, weights=probs, k=n_resources_in_ep)
        chosen = list(dict.fromkeys(chosen))  # dedupe preserving order/popularity draw
        call_idx = 0
        for rid in chosen:
            n_reuse = rng.randint(3, 8)
            tick = rng.randint(0, 3)
            for _ in range(n_reuse):
                sig = f"tool_call({rid})"
                episodes[ep_id].append(
                    {
                        "call_index": call_idx,
                        "timestamp_tick": min(sim_days - 1, tick),
                        "call_site_signature": sig,
                        "resource_id": rid,
                        "ground_truth_version_id": version_at(rid, min(sim_days - 1, tick)),
                        "volatility_regime": resource_meta[rid],
                        "resource_class": "synthetic",
                    }
                )
                call_idx += 1
                tick += rng.choice([1, 3, 7, 14])
        episodes[ep_id].sort(key=lambda c: (c["timestamp_tick"], c["call_index"]))
    logger.info(
        f"Built synthetic Zipf corpus: {len(episodes)} episodes, "
        f"{sum(len(v) for v in episodes.values())} calls, {len(resource_ids)} resources"
    )
    return dict(episodes), resource_schedules


# ---------------------------------------------------------------------------
# 2. Cache policy implementations (shared interface, stateful per call_site_signature)
# ---------------------------------------------------------------------------
class PolicyBase:
    name = "base"

    def __init__(self, knob):
        self.knob = knob
        self.cache = {}  # key -> {"version": str, "last_fetch_tick": int}

    def decide(self, call, now_tick):
        key = call["call_site_signature"]
        entry = self.cache.get(key)
        if entry is None:
            return "refresh", None
        if self._is_stale_by_policy(key, entry, now_tick):
            return "refresh", entry["version"]
        return "serve_cache", entry["version"]

    def _is_stale_by_policy(self, key, entry, now_tick):
        raise NotImplementedError

    def update(self, call, served_from_cache, observed_stale, spot_checked):
        key = call["call_site_signature"]
        if not served_from_cache:
            self.cache[key] = {"version": call["ground_truth_version_id"], "last_fetch_tick": call["timestamp_tick"]}

    def current_param(self, key):
        raise NotImplementedError


class FixedTTL(PolicyBase):
    name = "fixed_ttl"

    def _is_stale_by_policy(self, key, entry, now_tick):
        return (now_tick - entry["last_fetch_tick"]) >= self.knob

    def current_param(self, key):
        return self.knob


class DTTL(PolicyBase):
    """Literal reimplementation of stochastic-approximation TTL-toward-target-hit-rate
    (Basu et al.-style Robbins-Monro update): ttl += eta*(hit_observed - target_hit_rate)/k."""

    name = "d_ttl"
    ETA = 6.0
    TTL_MIN, TTL_MAX = 1.0, 60.0

    def __init__(self, knob):
        super().__init__(knob)
        self.ttl = defaultdict(lambda: 3.0)
        self.k = defaultdict(int)

    def _is_stale_by_policy(self, key, entry, now_tick):
        return (now_tick - entry["last_fetch_tick"]) >= self.ttl[key]

    def update(self, call, served_from_cache, observed_stale, spot_checked):
        key = call["call_site_signature"]
        self.k[key] += 1
        hit_observed = 1.0 if served_from_cache else 0.0
        step = self.ETA * (hit_observed - self.knob) / self.k[key]
        self.ttl[key] = min(self.TTL_MAX, max(self.TTL_MIN, self.ttl[key] + step))
        super().update(call, served_from_cache, observed_stale, spot_checked)

    def current_param(self, key):
        return self.ttl[key]


class EWMAAdaptive(PolicyBase):
    """EWMA of confirmed-stale rate drives TTL up/down toward a target tolerable staleness."""

    name = "ewma_adaptive"
    TARGET_STALE = 0.05
    GAIN = 1.5
    TTL_MIN, TTL_MAX = 1.0, 60.0

    def __init__(self, knob):
        super().__init__(knob)
        self.ttl = defaultdict(lambda: 3.0)
        self.ewma = defaultdict(float)

    def _is_stale_by_policy(self, key, entry, now_tick):
        return (now_tick - entry["last_fetch_tick"]) >= self.ttl[key]

    def update(self, call, served_from_cache, observed_stale, spot_checked):
        key = call["call_site_signature"]
        if observed_stale is not None:
            obs = 1.0 if observed_stale else 0.0
            self.ewma[key] = self.knob * obs + (1 - self.knob) * self.ewma[key]
            factor = 1 + self.GAIN * (self.TARGET_STALE - self.ewma[key])
            self.ttl[key] = min(self.TTL_MAX, max(self.TTL_MIN, self.ttl[key] * factor))
        super().update(call, served_from_cache, observed_stale, spot_checked)

    def current_param(self, key):
        return self.ttl[key]


class FreshCacheGate(PolicyBase):
    """Exponential-decay hazard model fit from accumulated spot-check labels, gating reuse
    against an error_budget. `pooled=True` shares hazard statistics across all call-sites of
    the same resource_class (fixes small-sample calibration on low-repeat sites)."""

    name = "freshcache_raw"
    pooled = False
    PRIOR_LAMBDA = 0.02

    def __init__(self, knob):
        super().__init__(knob)
        self.stale_events = defaultdict(float)
        self.total_age_ticks = defaultdict(float)

    def _group_key(self, call):
        return call["resource_class"] if self.pooled else call["call_site_signature"]

    def decide(self, call, now_tick):
        key = call["call_site_signature"]
        entry = self.cache.get(key)
        if entry is None:
            return "refresh", None
        age = now_tick - entry["last_fetch_tick"]
        gkey = self._group_key(call)
        lam = (self.stale_events[gkey] + 1e-6) / (self.total_age_ticks[gkey] + 1e-6 / self.PRIOR_LAMBDA)
        prob_stale = 1 - pow(2.718281828, -lam * max(age, 0))
        if prob_stale > self.knob:
            return "refresh", entry["version"]
        return "serve_cache", entry["version"]

    def _is_stale_by_policy(self, key, entry, now_tick):
        raise NotImplementedError

    def update(self, call, served_from_cache, observed_stale, spot_checked):
        key = call["call_site_signature"]
        if observed_stale is not None:
            gkey = self._group_key(call)
            entry = self.cache.get(key)
            age = (call["timestamp_tick"] - entry["last_fetch_tick"]) if entry else 0
            self.total_age_ticks[gkey] += max(age, 1e-3)
            if observed_stale:
                self.stale_events[gkey] += 1.0
        super().update(call, served_from_cache, observed_stale, spot_checked)

    def current_param(self, key):
        gkey = key
        return (self.stale_events[gkey] + 1e-6) / (self.total_age_ticks[gkey] + 1e-6 / self.PRIOR_LAMBDA)

    def current_hazard(self, key):
        return self.current_param(key)


class FreshCacheGateRaw(FreshCacheGate):
    name = "freshcache_raw"
    pooled = False


class FreshCacheGatePooled(FreshCacheGate):
    name = "freshcache_pooled"
    pooled = True

    def current_param(self, key):
        return None  # pooled stat is per resource_class, not per call-site; reported separately


class AIMD(PolicyBase):
    """Additive-increase/multiplicative-decrease window per call_site_signature."""

    name = "aimd"
    W_MIN, W_MAX = 1.0, 60.0
    W_INIT = 3.0

    def __init__(self, knob):
        super().__init__(knob)
        self.a, self.b = knob
        self.window = defaultdict(lambda: self.W_INIT)

    def _is_stale_by_policy(self, key, entry, now_tick):
        return (now_tick - entry["last_fetch_tick"]) >= self.window[key]

    def update(self, call, served_from_cache, observed_stale, spot_checked):
        key = call["call_site_signature"]
        if observed_stale is not None:
            if observed_stale:
                self.window[key] = max(self.W_MIN, self.window[key] * self.b)
            else:
                self.window[key] = min(self.W_MAX, self.window[key] + self.a)
        super().update(call, served_from_cache, observed_stale, spot_checked)

    def current_param(self, key):
        return self.window[key]


POLICIES = {
    "fixed_ttl": (FixedTTL, [1, 3, 7, 14, 30]),
    "d_ttl": (DTTL, [0.5, 0.7, 0.9]),
    "ewma_adaptive": (EWMAAdaptive, [0.1, 0.3, 0.5]),
    "freshcache_raw": (FreshCacheGateRaw, [0.10, 0.20, 0.35]),
    "freshcache_pooled": (FreshCacheGatePooled, [0.10, 0.20, 0.35]),
    "aimd": (AIMD, [(a, b) for a in [0.1, 0.25, 0.5] for b in [0.5, 0.7, 0.9]]),
}


# ---------------------------------------------------------------------------
# 3. Replay engine (shared across real-corpus and synthetic runs), aggregated per replicate
# ---------------------------------------------------------------------------
def replay_aggregate(episodes, policy_factory, knob, spot_check_rate, seed):
    rng = random.Random(seed)
    policy = policy_factory(knob)

    n_calls = 0
    n_served = 0
    n_stale_served = 0
    n_spot_checked = 0
    param_sum = 0.0
    param_n = 0
    regime_stats = defaultdict(lambda: {"n": 0, "served": 0, "stale": 0})

    for episode_id, calls in episodes.items():
        for call in calls:
            now_tick = call["timestamp_tick"]
            decision, cached_version = policy.decide(call, now_tick)
            served_from_cache = decision == "serve_cache"
            spot_checked = rng.random() < spot_check_rate
            true_version = call["ground_truth_version_id"]
            ground_truth_stale = served_from_cache and (cached_version != true_version)
            observed_stale = ground_truth_stale if (spot_checked or not served_from_cache) else None

            n_calls += 1
            regime = call["volatility_regime"]
            regime_stats[regime]["n"] += 1
            if served_from_cache:
                n_served += 1
                regime_stats[regime]["served"] += 1
                if ground_truth_stale:
                    n_stale_served += 1
                    regime_stats[regime]["stale"] += 1
            if spot_checked:
                n_spot_checked += 1

            try:
                p = policy.current_param(call["call_site_signature"])
                if p is not None:
                    param_sum += p
                    param_n += 1
            except NotImplementedError:
                pass

            policy.update(call, served_from_cache, observed_stale, spot_checked)

    hit_rate = n_served / n_calls if n_calls else 0.0
    stale_rate_of_served = n_stale_served / n_served if n_served else 0.0
    stale_rate_of_calls = n_stale_served / n_calls if n_calls else 0.0
    mean_adapted_param = param_sum / param_n if param_n else None

    regime_breakdown = {}
    for regime, s in regime_stats.items():
        regime_breakdown[regime] = {
            "n": s["n"],
            "hit_rate": s["served"] / s["n"] if s["n"] else 0.0,
            "stale_rate_of_served": s["stale"] / s["served"] if s["served"] else 0.0,
        }

    return {
        "n_calls": n_calls,
        "n_served_from_cache": n_served,
        "n_stale_served": n_stale_served,
        "n_spot_checked": n_spot_checked,
        "hit_rate": hit_rate,
        "stale_rate_of_served": stale_rate_of_served,
        "stale_rate_of_calls": stale_rate_of_calls,
        "mean_adapted_param": mean_adapted_param,
        "redundant_calls_avoided": n_served,
        "regime_breakdown": regime_breakdown,
    }


# ---------------------------------------------------------------------------
# 4. Experiment grid driver
# ---------------------------------------------------------------------------
def run_grid(data_sources, n_replicates, spot_check_rates, headline_rate=0.20, max_cells=None):
    rows = []
    n_cells = 0
    for data_source, (episodes, n_calls_total) in data_sources.items():
        for policy_key, (factory, knobs) in POLICIES.items():
            for knob in knobs:
                for spot_rate in spot_check_rates:
                    if spot_rate != headline_rate and policy_key != "aimd":
                        continue  # ablation scoped to AIMD + headline rate for other policies
                    n_cells += 1
                    if max_cells is not None and n_cells > max_cells:
                        continue
                    for seed in range(n_replicates):
                        agg = replay_aggregate(episodes, factory, knob, spot_rate, seed)
                        knob_value = list(knob) if isinstance(knob, tuple) else knob
                        row = {
                            "data_source": data_source,
                            "policy_name": policy_key,
                            "knob_value": knob_value,
                            "spot_check_rate": spot_rate,
                            "seed": seed,
                            "n_episodes": len(episodes),
                            **agg,
                        }
                        rows.append(row)
    logger.info(f"run_grid produced {len(rows)} replicate rows across {n_cells} cells")
    return rows, n_cells


def rows_to_gen_sol_dataset(rows, dataset_name):
    examples = []
    for row in rows:
        inp = {
            "data_source": row["data_source"],
            "policy_name": row["policy_name"],
            "knob_value": row["knob_value"],
            "spot_check_rate": row["spot_check_rate"],
            "seed": row["seed"],
            "n_episodes": row["n_episodes"],
            "n_calls": row["n_calls"],
        }
        out = {
            "hit_rate": row["hit_rate"],
            "stale_rate_of_served": row["stale_rate_of_served"],
            "mean_adapted_param": row["mean_adapted_param"],
        }
        example = {
            "input": json.dumps(inp),
            "output": json.dumps(out),
            "metadata_policy_name": row["policy_name"],
            "metadata_knob_value": json.dumps(row["knob_value"]),
            "metadata_data_source": row["data_source"],
            "metadata_spot_check_rate": row["spot_check_rate"],
            "metadata_seed": row["seed"],
            "metadata_n_calls": row["n_calls"],
            "metadata_n_served_from_cache": row["n_served_from_cache"],
            "metadata_hit_rate": row["hit_rate"],
            "metadata_n_stale_served": row["n_stale_served"],
            "metadata_stale_rate_of_served": row["stale_rate_of_served"],
            "metadata_stale_rate_of_calls": row["stale_rate_of_calls"],
            "metadata_n_spot_checked": row["n_spot_checked"],
            "metadata_mean_adapted_param": row["mean_adapted_param"],
            "metadata_redundant_calls_avoided": row["redundant_calls_avoided"],
            "metadata_regime_breakdown": json.dumps(row["regime_breakdown"]),
            "metadata_is_baseline": row["policy_name"] == "fixed_ttl",
            f"predict_{row['policy_name']}": json.dumps(out),
        }
        examples.append(example)
    return {"dataset": dataset_name, "examples": examples}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
@logger.catch(reraise=True)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mini", "small", "full"], default="full")
    parser.add_argument("--n-episodes-cap", type=int, default=None)
    parser.add_argument("--n-replicates", type=int, default=None)
    parser.add_argument("--max-cells", type=int, default=None)
    parser.add_argument("--data-filename", type=str, default="full_data_out.json")
    args = parser.parse_args()

    if args.mode == "mini":
        n_replicates = 1
        max_cells = 1  # smoke test: exactly one policy/knob cell
        data_filename = "mini_data_out.json"
    elif args.mode == "small":
        n_replicates = args.n_replicates or 2
        max_cells = args.max_cells
        data_filename = args.data_filename
    else:
        n_replicates = args.n_replicates or 20
        max_cells = args.max_cells
        data_filename = args.data_filename

    logger.info(f"=== method.py starting: mode={args.mode} n_replicates={n_replicates} max_cells={max_cells} ===")

    rows_raw, dep_path = load_real_corpus(data_filename)
    episodes_real, resource_schedules_real = parse_rows_into_episodes(rows_raw)
    if args.n_episodes_cap:
        keys = list(episodes_real.keys())[: args.n_episodes_cap]
        episodes_real = {k: episodes_real[k] for k in keys}
        logger.info(f"Capped real episodes to {len(episodes_real)} for this run")

    logger.info("Building synthetic Zipf-popularity corpus (explicit secondary run)")
    episodes_synth, resource_schedules_synth = build_synthetic_zipf_episodes()
    if args.n_episodes_cap:
        keys = list(episodes_synth.keys())[: args.n_episodes_cap]
        episodes_synth = {k: episodes_synth[k] for k in keys}

    data_sources = {
        "real_corpus": (episodes_real, sum(len(v) for v in episodes_real.values())),
        "synthetic_zipf": (episodes_synth, sum(len(v) for v in episodes_synth.values())),
    }
    for name, (eps, n_calls) in data_sources.items():
        logger.info(f"data_source={name}: {len(eps)} episodes, {n_calls} calls")

    spot_check_rates = [0.10, 0.20, 0.40]
    rows, n_cells = run_grid(
        data_sources, n_replicates=n_replicates, spot_check_rates=spot_check_rates,
        headline_rate=0.20, max_cells=max_cells,
    )

    datasets = []
    for data_source in data_sources:
        subset = [r for r in rows if r["data_source"] == data_source]
        if subset:
            datasets.append(rows_to_gen_sol_dataset(subset, dataset_name=f"cache_policy_replay_{data_source}"))

    output = {
        "metadata": {
            "description": (
                "Cache-policy replay comparison (fixed TTL, d-TTL, EWMA-adaptive, "
                "FreshCache raw+pooled, AIMD) over the real versioned-resource corpus "
                "(art_T0onLH9xokqw) and an explicit synthetic Zipf-popularity simulator run "
                "side-by-side. Each example is one (data_source, policy, knob, spot_check_rate, "
                "seed) replicate's aggregate hit-rate / staleness metrics."
            ),
            "policies_and_knobs": {k: (v[1] if not isinstance(v[1][0], tuple) else [list(t) for t in v[1]])
                                    for k, v in POLICIES.items()},
            "n_replicates": n_replicates,
            "spot_check_rates_tested": spot_check_rates,
            "headline_spot_check_rate": 0.20,
            "data_sources": list(data_sources.keys()),
            "dependency_verified": {"path": str(dep_path), "n_rows_loaded": len(rows_raw)},
            "n_cells": n_cells,
            "n_total_replicate_rows": len(rows),
            "mode": args.mode,
        },
        "datasets": datasets,
    }

    out_path = WORKSPACE / "method_out.json"
    out_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Wrote {out_path} with {len(rows)} replicate rows across {len(datasets)} dataset groups")


if __name__ == "__main__":
    main()
