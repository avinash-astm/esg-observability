#!/usr/bin/env python3
"""Health-check script for Prometheus metrics emitted by the IoT observability stack."""

import json
import requests
import sys

PROMETHEUS_URL = "http://localhost:9090"

HEALTH_QUERIES = {
    "PUE": "pue",
    "Season Window Active": "season_window_active",
    "Cooling PUE": "ppue",
    "IT Load": "it_load",
    "Efficiency Error Budget Burn Rate": "efficiency_error_budget_burn_rate",
    "WUE": "wue",
    "Rainwater Harvested Liters": "rainwater_harvested_liters",
    "Water Source Mix": "water_source_mix",
    "Tanker Dependency Ratio": "tanker_dependency_ratio",
    "CUE": "cue",
    "Renewable Energy Fraction": "re_fraction",
    "DG Runtime Ratio": "dg_runtime_ratio",
    "BRSR Core Readiness": "brsr_core_kpi_completeness_ratio",
    "Worker Hours WBGT > 32": "worker_hours_wbgt_above_32",
    "Data Localisation %": "data_localisation_pct",
    "Upcoming Filing Deadlines": "upcoming_filing_deadline_seconds",
}


def query_prometheus(expr):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": expr}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def format_labels(metric):
    labels = [f'{k}="{v}"' for k, v in metric.items() if k != "__name__"]
    return "{" + ", ".join(labels) + "}" if labels else ""


def run_health_checks():
    print(f"Prometheus URL: {PROMETHEUS_URL}\n")
    any_missing = False

    for name, expr in HEALTH_QUERIES.items():
        print(f"Checking {name} ({expr})...")
        try:
            data = query_prometheus(expr)
        except Exception as exc:
            print(f"  ERROR: Failed to query Prometheus: {exc}\n")
            any_missing = True
            continue

        if data.get("status") != "success":
            print("  ERROR: Prometheus returned an unexpected status")
            any_missing = True
            continue

        results = data["data"]["result"]
        if not results:
            print("  MISSING: No samples returned for this metric.\n")
            any_missing = True
            continue

        print(f"  OK: {len(results)} result(s)")
        for result in results[:3]:
            value = result["value"][1]
            labels = format_labels(result["metric"])
            print(f"    {result['metric'].get('__name__', expr)}{labels} = {value}")
        if len(results) > 3:
            print(f"    ...and {len(results) - 3} more result(s)")
        print()

    if any_missing:
        print("Health check completed: SOME metrics are missing or unavailable.")
        sys.exit(1)
    print("Health check completed: all queried metrics are present.")


if __name__ == "__main__":
    run_health_checks()
