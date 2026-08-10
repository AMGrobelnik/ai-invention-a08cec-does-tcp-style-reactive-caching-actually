#!/usr/bin/env python3
"""Build the Versioned Resource Corpus for Agent Cache Testing.

Produces full_data_out.json in exp_sel_data_out.json schema: two candidate
"datasets" (v1_ms_marco_snippets, v2_qqp_snippets), each a flattened list of
tool-call log rows (episode calls) over a shared resource pool of
documents / search-snippets / computed-values, each resource carrying a real,
ground-truth version_schedule over a simulated 30-day timeline.
"""

import hashlib
import json
import random
import sys
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

WS = Path(__file__).resolve().parent
DATASETS_DIR = WS / "temp" / "datasets"
TABLES_DIR = WS / "temp" / "tables"

RNG = random.Random(20260809)

SIM_DAYS = 30  # simulated timeline length (ticks = days)
N_DOCS = 180
N_SNIPPET_GROUPS = 120  # snippet resources
N_COMPUTED = 60
N_EPISODES = 30
GAP_CHOICES = [1, 3, 7, 14]  # simulated-day gaps for read-then-reread
CHECKED_SUBSAMPLE_RATE = 0.15  # fraction of calls with a spot-check label


def content_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------
# Real-content loaders
# --------------------------------------------------------------------------

def load_squad_docs(n: int) -> list[dict]:
    """~n distinct real Wikipedia passages (SQuAD 'context' field) -> static document resources."""
    path = DATASETS_DIR / "full_rajpurkar_squad_plain_text_train.json"
    logger.info(f"Loading SQuAD contexts from {path}")
    data = json.loads(path.read_text())
    seen: dict[str, dict] = {}
    for row in data:
        ctx = row["context"]
        if ctx not in seen and 200 <= len(ctx.split()) <= 400:
            seen[ctx] = {"title": row["title"], "context": ctx}
        if len(seen) >= n * 3:
            break
    contexts = list(seen.values())
    RNG.shuffle(contexts)
    contexts = contexts[:n]
    logger.info(f"Selected {len(contexts)} distinct SQuAD passages")
    return contexts


def load_ms_marco_snippets(n: int) -> list[dict]:
    """~n real (query, passage) pairs from MS MARCO -> search-snippet resources."""
    path = DATASETS_DIR / "full_microsoft_ms_marco_v2.1_train.json"
    logger.info(f"Loading MS MARCO passages from {path}")
    out = []
    seen_q = set()
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for row in data:
        q = row["query"].strip()
        if not q or q in seen_q:
            continue
        passages = row.get("passages", {})
        texts = passages.get("passage_text", [])
        sel = passages.get("is_selected", [])
        if not texts:
            continue
        # prefer the human-selected passage; else first
        idx = sel.index(1) if 1 in sel else 0
        snippet = texts[idx]
        sentences = snippet.split(". ")
        snippet = ". ".join(sentences[:3]).strip()
        if not snippet:
            continue
        seen_q.add(q)
        out.append({"query": q, "content": snippet})
        if len(out) >= n:
            break
    logger.info(f"Selected {len(out)} MS MARCO query/snippet pairs")
    return out


def load_qqp_snippet_groups(n: int) -> list[dict]:
    """Real Quora duplicate-question groups -> snippet resources with genuine near-duplicate
    query variants (the dataset's own is_duplicate=1 pairs), content = canonical question text."""
    path = DATASETS_DIR / "full_AlekseyKorshuk_quora-question-pairs_default_train.json"
    logger.info(f"Loading QQP duplicate pairs from {path}")
    data = json.loads(path.read_text())
    dup_pairs = [r for r in data if r.get("is_duplicate") == 1]
    RNG.shuffle(dup_pairs)
    groups = []
    seen_q1 = set()
    for r in dup_pairs:
        q1, q2 = r["question1"].strip(), r["question2"].strip()
        if not q1 or not q2 or q1 in seen_q1:
            continue
        seen_q1.add(q1)
        groups.append({"canonical_query": q1, "content": q1, "near_dup_queries": [q2]})
        if len(groups) >= n:
            break
    logger.info(f"Selected {len(groups)} QQP near-duplicate query groups")
    return groups


def load_owid_series() -> dict:
    """Real dated indicator sequences from OWID: population (slow/static-ish),
    energy_mix share (periodic, annual), covid new_cases (bursty, daily)."""
    logger.info("Loading OWID indicator series")
    pop_path = TABLES_DIR / "full_garden_demography_2024-07-15_population_population.json"
    energy_path = TABLES_DIR / "full_garden_energy_2025-06-27_energy_mix_energy_mix.json"
    covid_path = TABLES_DIR / "full_garden_owid_latest_covid_covid.json"

    pop = json.loads(pop_path.read_text())
    energy = json.loads(energy_path.read_text())

    countries_pop = {}
    for row in pop:
        if row.get("country") and 2000 <= row.get("year", 0) <= 2023 and row.get("population"):
            countries_pop.setdefault(row["country"], []).append((row["year"], row["population"]))

    countries_energy = {}
    for row in energy:
        c = row.get("country")
        y = row.get("year")
        v = row.get("coal__twh")
        if c and y and v is not None and 2000 <= y <= 2023:
            countries_energy.setdefault(c, []).append((y, round(v, 2)))

    # Bursty: grep-filter covid file (JSON-lines-per-record) for a handful of countries,
    # keeps memory bounded instead of loading the full 920MB file.
    bursty_countries = ["United States", "Germany", "Brazil", "India", "Japan"]
    countries_covid: dict[str, list] = {c: [] for c in bursty_countries}
    with covid_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().rstrip(",")
            if not line or line in ("[", "]"):
                continue
            for c in bursty_countries:
                if f'"location": "{c}"' in line:
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    nc = rec.get("new_cases")
                    date = rec.get("date")
                    if nc is not None and date and "2021-03" <= date[:7] <= "2021-05":
                        countries_covid[c].append((date[:10], int(nc)))
                    break

    logger.info(
        f"OWID series loaded: {len(countries_pop)} pop countries, "
        f"{len(countries_energy)} energy countries, "
        f"{sum(len(v) for v in countries_covid.values())} covid daily points"
    )
    return {"population": countries_pop, "energy": countries_energy, "covid": countries_covid}


# --------------------------------------------------------------------------
# Resource construction
# --------------------------------------------------------------------------

def day_to_tick(day: int) -> int:
    return max(0, min(SIM_DAYS - 1, day))


def build_document_resources(docs: list[dict]) -> list[dict]:
    """SQuAD gives a single real snapshot per passage -> mark STATIC (no fabricated edits),
    per plan Step 1 fallback rule."""
    resources = []
    for i, d in enumerate(docs):
        rid = f"doc_{i:04d}"
        vid = f"{rid}_v0"
        resources.append({
            "resource_id": rid,
            "resource_class": "document",
            "volatility_regime": "static",
            "timing_provenance": "real_single_snapshot",
            "content_by_version": {vid: d["context"]},
            "version_schedule": [
                {"version_id": vid, "content_hash": content_hash(d["context"]),
                 "valid_from_tick": 0, "valid_until_tick": SIM_DAYS - 1}
            ],
            "extra": {"title": d["title"]},
        })
    return resources


def build_snippet_resources_ms_marco(items: list[dict]) -> list[dict]:
    """Single real MS MARCO snapshot per query -> STATIC (no second snapshot available)."""
    resources = []
    for i, d in enumerate(items):
        rid = f"snip_msmarco_{i:04d}"
        vid = f"{rid}_v0"
        resources.append({
            "resource_id": rid,
            "resource_class": "search_snippet",
            "volatility_regime": "static",
            "timing_provenance": "real_single_snapshot",
            "content_by_version": {vid: d["content"]},
            "version_schedule": [
                {"version_id": vid, "content_hash": content_hash(d["content"]),
                 "valid_from_tick": 0, "valid_until_tick": SIM_DAYS - 1}
            ],
            "extra": {"canonical_query": d["query"], "near_dup_queries": []},
        })
    return resources


def build_snippet_resources_qqp(groups: list[dict]) -> list[dict]:
    """QQP gives one real content string + genuine dataset-provided near-duplicate query
    variant per group -> STATIC content (QQP has no second dated snapshot), but the
    near-duplicate QUERY pattern itself is fully real (search-then-refine, Step 2)."""
    resources = []
    for i, d in enumerate(groups):
        rid = f"snip_qqp_{i:04d}"
        vid = f"{rid}_v0"
        resources.append({
            "resource_id": rid,
            "resource_class": "search_snippet",
            "volatility_regime": "static",
            "timing_provenance": "real_single_snapshot",
            "content_by_version": {vid: d["content"]},
            "version_schedule": [
                {"version_id": vid, "content_hash": content_hash(d["content"]),
                 "valid_from_tick": 0, "valid_until_tick": SIM_DAYS - 1}
            ],
            "extra": {"canonical_query": d["canonical_query"], "near_dup_queries": d["near_dup_queries"]},
        })
    return resources


def build_computed_resources(series: dict) -> list[dict]:
    """Real OWID indicator sequences drive the version_schedule directly:
    population (slow -> periodic, few real updates in-window), energy coal share (periodic,
    annual real cadence), covid new_cases (bursty, real daily cadence w/ irregular jumps)."""
    resources = []
    idx = 0

    # PERIODIC (slow, real annual cadence): population, pick last N_YEARS years present,
    # map real years onto the 30-day simulated window in order.
    pop_countries = list(series["population"].items())[:25]
    for country, yearly in pop_countries:
        yearly = sorted(yearly)[-6:]  # last up to 6 real annual values
        if len(yearly) < 2:
            continue
        rid = f"comp_pop_{idx:04d}"
        idx += 1
        n = len(yearly)
        schedule = []
        content_by_version = {}
        for j, (year, val) in enumerate(yearly):
            vid = f"{rid}_v{j}"
            tick_from = day_to_tick(round(j * SIM_DAYS / n))
            tick_to = day_to_tick(round((j + 1) * SIM_DAYS / n) - 1) if j < n - 1 else SIM_DAYS - 1
            content_by_version[vid] = {"country": country, "year": year, "population": val}
            schedule.append({"version_id": vid, "content_hash": content_hash(f"{val}"),
                              "valid_from_tick": tick_from, "valid_until_tick": tick_to})
        resources.append({
            "resource_id": rid, "resource_class": "computed_value",
            "volatility_regime": "periodic", "timing_provenance": "real_owid_cadence_remapped_to_window",
            "content_by_version": content_by_version, "version_schedule": schedule,
            "extra": {"indicator": "population", "country": country},
        })

    # PERIODIC (annual, real cadence): energy coal TWh share, same remap approach
    energy_countries = list(series["energy"].items())[:20]
    for country, yearly in energy_countries:
        yearly = sorted(yearly)[-6:]
        if len(yearly) < 2:
            continue
        rid = f"comp_energy_{idx:04d}"
        idx += 1
        n = len(yearly)
        schedule = []
        content_by_version = {}
        for j, (year, val) in enumerate(yearly):
            vid = f"{rid}_v{j}"
            tick_from = day_to_tick(round(j * SIM_DAYS / n))
            tick_to = day_to_tick(round((j + 1) * SIM_DAYS / n) - 1) if j < n - 1 else SIM_DAYS - 1
            content_by_version[vid] = {"country": country, "year": year, "coal_twh": val}
            schedule.append({"version_id": vid, "content_hash": content_hash(f"{val}"),
                              "valid_from_tick": tick_from, "valid_until_tick": tick_to})
        resources.append({
            "resource_id": rid, "resource_class": "computed_value",
            "volatility_regime": "periodic", "timing_provenance": "real_owid_cadence_remapped_to_window",
            "content_by_version": content_by_version, "version_schedule": schedule,
            "extra": {"indicator": "coal_energy_twh", "country": country},
        })

    # BURSTY (real daily cadence, genuinely irregular jumps): covid new_cases, mapped
    # 1 real day -> 1 simulated tick directly (fully real timing, no injection needed).
    for country, daily in series["covid"].items():
        daily = sorted(daily)[:SIM_DAYS]
        if len(daily) < 5:
            continue
        rid = f"comp_covid_{idx:04d}"
        idx += 1
        schedule = []
        content_by_version = {}
        for j, (date, val) in enumerate(daily):
            vid = f"{rid}_v{j}"
            tick = day_to_tick(j)
            tick_to = day_to_tick(j + 1) - 1 if j < len(daily) - 1 else SIM_DAYS - 1
            if tick_to < tick:
                tick_to = tick
            content_by_version[vid] = {"country": country, "date": date, "new_cases": val}
            schedule.append({"version_id": vid, "content_hash": content_hash(f"{val}"),
                              "valid_from_tick": tick, "valid_until_tick": tick_to})
        resources.append({
            "resource_id": rid, "resource_class": "computed_value",
            "volatility_regime": "bursty", "timing_provenance": "real_owid_daily_cadence",
            "content_by_version": content_by_version, "version_schedule": schedule,
            "extra": {"indicator": "covid_new_cases", "country": country},
        })

    logger.info(f"Built {len(resources)} computed-value resources")
    return resources


# --------------------------------------------------------------------------
# Episode (tool-call log) generation
# --------------------------------------------------------------------------

def version_at_tick(resource: dict, tick: int) -> str:
    for v in resource["version_schedule"]:
        if v["valid_from_tick"] <= tick <= v["valid_until_tick"]:
            return v["version_id"]
    return resource["version_schedule"][-1]["version_id"]


def gen_episodes(docs: list[dict], snippets: list[dict], computed: list[dict], snippet_kind: str) -> list[dict]:
    episodes = []
    for ep_i in range(N_EPISODES):
        episode_id = f"ep_{ep_i:03d}"
        calls = []
        call_idx = 0
        start_tick = RNG.randint(0, 10)

        # Template A: read-then-reread — pick 10-16 docs, revisit each 4-10 times with gaps
        n_docs_this_ep = RNG.randint(10, 16)
        for doc in RNG.sample(docs, min(n_docs_this_ep, len(docs))):
            n_revisits = RNG.randint(4, 10)
            tick = start_tick
            for _ in range(n_revisits):
                calls.append((tick, "read_file", f"read_file(doc_id={doc['resource_id']})", doc))
                tick = day_to_tick(tick + RNG.choice(GAP_CHOICES))

        # Template B: search-then-refine — 8-14 snippet groups, 3-6 near-duplicate query calls each
        n_snip_this_ep = RNG.randint(8, 14)
        for snip in RNG.sample(snippets, min(n_snip_this_ep, len(snippets))):
            n_refines = RNG.randint(3, 6)
            tick = RNG.randint(0, SIM_DAYS - 1)
            near_dups = snip["extra"].get("near_dup_queries", [])
            for k in range(n_refines):
                q = snip["extra"]["canonical_query"] if k == 0 or not near_dups else RNG.choice(near_dups)
                calls.append((tick, "web_search", f"web_search(query={q!r})", snip))
                tick = day_to_tick(tick + RNG.choice([0, 0, 1]))

        # Template C: compute-then-reuse — 6-10 computed values, reused 3-6 times each
        n_comp_this_ep = RNG.randint(6, 10)
        for comp in RNG.sample(computed, min(n_comp_this_ep, len(computed))):
            n_reuse = RNG.randint(3, 6)
            tick = RNG.randint(0, SIM_DAYS - 1)
            inputs_sig = f"{comp['extra'].get('indicator')}_{comp['extra'].get('country')}"
            for _ in range(n_reuse):
                calls.append((tick, "compute", f"compute(inputs={inputs_sig})", comp))
                tick = day_to_tick(tick + RNG.choice(GAP_CHOICES))

        calls.sort(key=lambda c: c[0])
        for tick, fn, sig, res in calls:
            gt_vid = version_at_tick(res, tick)
            calls_obj = {
                "episode_id": episode_id, "call_index": call_idx, "timestamp_tick": tick,
                "call_site_signature": sig, "resource_id": res["resource_id"],
                "ground_truth_version_id": gt_vid, "resource": res,
            }
            episodes.append(calls_obj)
            call_idx += 1
    return episodes


def rows_to_examples(call_rows: list[dict]) -> list[dict]:
    examples = []
    for row in call_rows:
        res = row["resource"]
        content_now = res["content_by_version"][row["ground_truth_version_id"]]
        content_str = content_now if isinstance(content_now, str) else json.dumps(content_now)
        checked = RNG.random() < CHECKED_SUBSAMPLE_RATE
        input_obj = {
            "episode_id": row["episode_id"],
            "call_index": row["call_index"],
            "timestamp_tick": row["timestamp_tick"],
            "call_site_signature": row["call_site_signature"],
            "resource_id": row["resource_id"],
        }
        ex = {
            "input": json.dumps(input_obj, ensure_ascii=False),
            "output": row["ground_truth_version_id"],
            "metadata_resource_class": res["resource_class"],
            "metadata_volatility_regime": res["volatility_regime"],
            "metadata_timing_provenance": res["timing_provenance"],
            "metadata_content_now": content_str[:600],
            "metadata_version_schedule": json.dumps(res["version_schedule"], ensure_ascii=False),
            "metadata_checked": checked,
            "metadata_sim_days": SIM_DAYS,
        }
        examples.append(ex)
    return examples


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    logger.info("=== Building chosen dataset: qqp snippets (real near-duplicate queries) ===")
    docs = load_squad_docs(N_DOCS)
    series = load_owid_series()

    doc_resources = build_document_resources(docs)
    computed_resources = build_computed_resources(series)

    qqp_groups = load_qqp_snippet_groups(N_SNIPPET_GROUPS)
    snip = build_snippet_resources_qqp(qqp_groups)
    episodes = gen_episodes(doc_resources, snip, computed_resources, "qqp")
    examples = rows_to_examples(episodes)
    logger.info(f"cache_corpus: {len(examples)} call-log examples, "
                f"{len(doc_resources)} docs + {len(snip)} snippets + {len(computed_resources)} computed resources")

    output = {
        "metadata": {
            "description": "Versioned Resource Corpus for Agent Cache Testing: real-content "
                            "resources (documents/search-snippets/computed-values) with ground-truth "
                            "version schedules over a 30-day simulated timeline, flattened to "
                            "per-tool-call log rows across episodes. Search-snippet near-duplicate "
                            "queries are Quora Question Pairs' own genuine is_duplicate=1 pairs.",
            "sim_days": SIM_DAYS,
            "n_episodes": N_EPISODES,
        },
        "datasets": [
            {"dataset": "cache_corpus", "examples": examples},
        ],
    }

    out_path = WS / "full_data_out.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False))
    logger.info(f"Saved {out_path} ({out_path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
