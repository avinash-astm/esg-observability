# Water SLO Breach Alert Configuration Summary

## ✅ Configuration Complete

Alert notifications have been configured for Water SLO breaches. Here's what was set up:

## Alert Configuration

### Primary Alert: Water SLO Breach
- **Trigger Condition**: Water Usage Effectiveness (WUE) > 3.0
- **Duration**: 2 minutes (must sustain breach)
- **Notification**: Email to `avinashvp@gmail.com`
- **Severity**: Warning

### Additional Alerts Configured
- **Critical Water Breach**: WUE > 4.0 (1 minute)
- **High Tanker Dependency**: Tanker ratio > 30% (5 minutes)
- **Low Rainwater Harvesting**: < 1000 liters (10 minutes)

## Files Created/Modified

### New Files
1. **`configs/prometheus-alerts.yml`** - Alert rules for water metrics
2. **`configs/alertmanager.yml`** - Email routing and SMTP configuration
3. **`configs/grafana-notifier.yaml`** - Grafana notification channel
4. **`ALERT-SETUP-GUIDE.md`** - Complete setup documentation

### Modified Files
1. **`configs/prometheus.yml`** - Added alert rules and Alertmanager target
2. **`docker-compose.yml`** - Added Alertmanager service, fixed port binding (8888)

## Services Added

- **Alertmanager** (prom/alertmanager:latest) on port 9093
  - Manages alert routing
  - Handles email notifications
  - Provides alert grouping and deduplication

## Email Configuration Required

Before running, you must update `configs/alertmanager.yml` with email credentials:

```yaml
global:
  smtp_from: 'your-email@gmail.com'
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_auth_username: 'your-email@gmail.com'
  smtp_auth_password: 'your-app-password'  # Gmail app password
```

## Quick Start

1. **Get Gmail App Password** (if using Gmail):
   - Enable 2FA on Gmail account
   - Visit https://myaccount.google.com/apppasswords
   - Generate password for "Mail" and "Windows"

2. **Update `configs/alertmanager.yml`**:
   - Replace email and password placeholders
   - Verify recipient email is correct (avinashvp@gmail.com)

3. **Start the stack**:
   ```bash
   cd iot-observability-stack
   docker-compose up -d
   ```

4. **Run the application**:
   ```bash
   uv run python src/app.py
   ```

5. **Monitor alerts**:
   - Prometheus: http://localhost:9090/alerts
   - Alertmanager: http://localhost:9093
   - Grafana: http://localhost:3000

## Alert Flow

```
IoT App Metrics (port 8000)
    ↓
Prometheus (port 9090) - Evaluates alert rules every 30s
    ↓
Alertmanager (port 9093) - Routes and sends notifications
    ↓
Email (avinashvp@gmail.com) - Receives notifications
```

## Testing

To test alerts:
1. Modify WUE value in simulation to exceed 3.0
2. Wait 2 minutes for alert to fire
3. Check email for notification
4. View alert status in Alertmanager dashboard

## Key Features

- ✅ Threshold-based alerting (WUE > 3.0)
- ✅ Email notifications
- ✅ Alert grouping and deduplication
- ✅ Severity-based routing (warning vs critical)
- ✅ Alert inhibition (critical suppresses warnings)
- ✅ Repeat intervals (avoid alert fatigue)
- ✅ Custom templates with metric values

## Documentation

Complete setup and troubleshooting guide: **`ALERT-SETUP-GUIDE.md`**

Topics covered:
- Detailed SMTP configuration for various providers
- Testing procedures
- Alerting rules explanation
- Customization options
- Troubleshooting common issues

## Architecture Benefits

1. **Prometheus-native**: Uses industry-standard Prometheus alerting
2. **Scalable**: Easily add more alert rules for other metrics
3. **Reliable**: Alert deduplication prevents notification spam
4. **Flexible**: Supports multiple notification channels
5. **Observable**: Full dashboards for monitoring alert system itself

## Next Steps

1. Update email credentials in `alertmanager.yml`
2. Deploy the updated stack
3. Test alert triggering
4. Add more alert rules for other SLO metrics as needed
5. Set up escalation policies if required
