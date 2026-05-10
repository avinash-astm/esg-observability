#!/usr/bin/env python3
"""
Scrape metrics directly from the OTEL Prometheus endpoint exposed by app.py and print them.
"""

import argparse
import requests
import sys

DEFAULT_METRICS_URL = "http://localhost:8000/metrics"


def fetch_metrics(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape and print metrics from app.py's Prometheus endpoint.")
    parser.add_argument(
        "--url",
        default=DEFAULT_METRICS_URL,
        help=f"Metrics endpoint to scrape (default: {DEFAULT_METRICS_URL})",
    )
    args = parser.parse_args()

    try:
        metrics_text = fetch_metrics(args.url)
        print(metrics_text)
        return 0
    except requests.exceptions.RequestException as exc:
        print(f"Failed to scrape metrics from {args.url}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())