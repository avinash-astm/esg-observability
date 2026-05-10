
#!/usr/bin/env python3
"""
Script to query the Prometheus endpoint (OTEL exporter) and dump collected metrics.
"""

import requests
import json
import sys

# Prometheus endpoint
PROMETHEUS_URL = "http://localhost:9090"

def query_prometheus(query):
    """Query Prometheus API for a given query."""
    url = f"{PROMETHEUS_URL}/api/v1/query"
    params = {"query": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying Prometheus: {response.status_code} - {response.text}")
        return None

def dump_metrics():
    """Dump collected IoT metrics."""
    metrics = [
        "temperature",
        "humidity",
        "pressure",
        "pue",
        "ppue",
        "it_load",
        "efficiency_error_budget_burn_rate",
        "wue",
        "rainwater_harvested_liters",
        "water_source_mix",
        "tanker_dependency_ratio",
        "cue",
        "re_fraction",
        "dg_runtime_ratio",
        "carbon_aware_workload_heatmap",
        "brsr_core_kpi_completeness_ratio",
        "worker_hours_wbgt_above_32",
        "data_localisation_pct",
        "upcoming_filing_deadline_seconds",
    ]
    for metric in metrics:
        print(f"\nDumping {metric}:")
        data = query_prometheus(metric)
        if data and data.get("status") == "success":
            results = data["data"]["result"]
            if results:
                for result in results:
                    metric_name = result["metric"].get("__name__", metric)
                    value = result["value"][1]
                    labels = ", ".join([f"{k}={v}" for k, v in result["metric"].items() if k != "__name__"])
                    print(f"  {metric_name}{{ {labels} }} = {value}")
            else:
                print(f"  No data for {metric}")
        else:
            print(f"  Failed to retrieve {metric}")

if __name__ == "__main__":
    dump_metrics()