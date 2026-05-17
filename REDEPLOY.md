# Redeploy All Docker Images

Run the following command to redeploy all services:

```bash
cd iot-observability-stack
docker-compose down
docker-compose up -d --build
docker-compose ps
```

## What This Does

1. **`docker-compose down`** - Stops and removes all running containers
2. **`docker-compose up -d --build`** - Rebuilds all images and starts services in background
3. **`docker-compose ps`** - Shows status of all running services

## Services Being Deployed

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| otel-collector | otel/opentelemetry-collector:latest | 4317, 8888 | Collects telemetry |
| prometheus | prom/prometheus:latest | 9090 | Metrics storage & alerts |
| alertmanager | prom/alertmanager:latest | 9093 | Alert routing & notifications |
| iot-app | local build | 8000 | IoT metrics provider |
| grafana | grafana/grafana:latest | 3000 | Dashboard visualization |

## Verify Deployment

After running the commands, check:

```bash
# View all running containers
docker-compose ps

# Check service logs
docker-compose logs -f

# Verify services are healthy
curl http://localhost:9090/api/v1/status/config     # Prometheus
curl http://localhost:9093/api/v1/status            # Alertmanager
curl http://localhost:8000/metrics                   # IoT App
curl http://localhost:3000/api/health                # Grafana
curl http://localhost:4317                           # OTEL Collector
```

## After Deployment

1. **Start the IoT App** (in a separate terminal):
   ```bash
   uv run python src/app.py
   ```

2. **Access Dashboards**:
   - Prometheus: http://localhost:9090
   - Alertmanager: http://localhost:9093
   - Grafana: http://localhost:3000 (admin/admin)

3. **Monitor Alerts**:
   - Go to http://localhost:9090/alerts to see alert rules
   - Go to http://localhost:9093 to see fired alerts

## Troubleshooting

If containers fail to start:

```bash
# View detailed error logs
docker-compose logs <service-name>

# Example: Check prometheus logs
docker-compose logs prometheus

# Check for port conflicts
netstat -ano | findstr "9090\|9093\|8000\|3000"
```

## Clean Rebuild (if needed)

To force a complete rebuild and remove cached data:

```bash
docker-compose down -v
docker image prune -a
docker-compose up -d --build
```
