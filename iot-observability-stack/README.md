# IoT Observability Stack

This project implements an observability stack for collecting and visualizing metrics from IoT devices using OpenTelemetry and Grafana. The stack includes components for data collection, processing, and visualization.

## Project Structure

- **src/**: Contains the source code for the application.
  - **collector/**: Module responsible for collecting metrics from IoT devices.
    - `__init__.py`: Initializes the collector module.
    - `metrics.py`: Functions for collecting specific metrics (temperature, humidity, pressure).
    - `telemetry.py`: Handles telemetry data processing.
  - **sensors/**: Simulates IoT devices.
    - `simulator.py`: Generates random metrics for testing.
  - `app.py`: Entry point for the application, initializes OpenTelemetry SDK and starts data collection.

- **configs/**: Configuration files for the observability stack.
  - `otel-collector-config.yaml`: Configuration for the OpenTelemetry Collector.
  - `grafana-datasource.yaml`: Data source configuration for Grafana.
  - `prometheus.yml`: Configuration for Prometheus to scrape metrics.

- **dashboards/**: Contains Grafana dashboard configurations.
  - `iot-metrics-dashboard.json`: JSON configuration for visualizing IoT metrics.
  - `monsoon-efficiency-dashboard.json`: Dashboard for PUE, pPUE, seasonal error budget, and efficiency burn-rate.
  - `water-stewardship-dashboard.json`: Dashboard for WUE, rainwater harvesting, water source mix, and tanker dependency alerts.
  - `grid-carbon-pathway-dashboard.json`: Dashboard for CUE, renewable energy fraction, DG runtime, and carbon-aware workload windows.
  - `governance-command-center-dashboard.json`: Dashboard for BRSR readiness, heat stress exposure, data localisation, and filing deadlines.

- `docker-compose.yml`: Defines services for the observability stack, including OpenTelemetry Collector, Prometheus, and Grafana.
- `run_simulator.py`: A wrapper script to run the app locally with the project source path configured.
- `health_checks.py`: Prometheus health-check script for the new simulated metrics.
- `requirements.txt`: Lists Python dependencies required for the project.

## Setup Instructions

### Prerequisites

- Install Docker Desktop for Windows.
- Enable WSL 2 integration if prompted.
- Ensure Docker is running before starting the stack.
- Optional: install `uv` if you want to use the Python task runner for local commands.

### Clone the repository

```bash
git clone <repository-url>
cd iot-observability-stack
```

### Install Python dependencies

If you are using `uv`:

```bash
uv sync
```

Or with pip inside your Python environment:

```bash
python -m pip install -r requirements.txt
```

### Build and start the full stack

This launches the OpenTelemetry Collector, Prometheus, Grafana, and the IoT app container.

```bash
docker compose up -d --build
```

### Verify the stack is running

```bash
docker compose ps
```

You should see services for:

- `iot-app`
- `otel-collector`
- `prometheus`
- `grafana`

### Start the simulator locally (optional)

If you want to run the Python app directly instead of the Docker app container:

```bash
python run_simulator.py
```

### Verify metrics health

Use the health check helper to confirm the new simulated metrics are visible in Prometheus:

```bash
python health_checks.py
```

This script checks metrics such as:

- `pue`
- `ppue`
- `wue`
- `cue`
- `brsr_core_kpi_completeness_ratio`

### Access the dashboards

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

Grafana default admin password is set to `admin` in `docker-compose.yml`.

### Dump metrics directly

To read raw metric values from Prometheus:

```bash
uv run python src/dump_metrics.py
```

## Recent changes

- Added four new Grafana dashboards covering:
  - Monsoon efficiency and PUE
  - Water stewardship and compliance
  - Grid carbon and Net Zero 2047 pathway
  - Social & governance command center
- Added metric simulators for the new SLI metrics in `src/sensors/simulator.py`.
- Extended collector logic in `src/collector/metrics.py` and `src/app.py` to emit the new metrics.
- Added `run_simulator.py` for direct local simulation execution.
- Added `health_checks.py` for Prometheus health verification of the new metrics.
- Updated `prometheus.yml` and `otel-collector-config.yaml` so the collector scrapes the app and exports metrics to Prometheus.

## Usage Guidelines

- The application simulates IoT devices and collects metrics which are processed and sent to the observability stack.
- Use the provided Grafana dashboard to visualize the collected metrics.

### Dumping Collected Metrics

To query and dump the collected metrics from the Prometheus endpoint (OTEL exporter), run the following script:

```
uv run python src/dump_metrics.py
```

This will output the current values for temperature, humidity, and pressure metrics.

## Overview of the Observability Stack

This observability stack leverages OpenTelemetry for data collection, Prometheus for scraping metrics, and Grafana for visualization, providing a comprehensive solution for monitoring IoT devices.