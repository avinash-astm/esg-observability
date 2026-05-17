# Water SLO Breach Alert Configuration Guide

## Overview

This guide explains how to configure email notifications for Water SLO breaches in the IoT Observability Stack. The alert triggers when Water Usage Effectiveness (WUE) exceeds 3.0.

## Architecture

The alerting system consists of:

1. **Prometheus** - Monitors metrics and evaluates alert rules
2. **Alertmanager** - Manages alert routing and notifications
3. **Grafana** - Dashboard visualization with built-in alerting
4. **Email** - Sends notifications to configured recipients

## Configuration Files

### 1. Prometheus Alert Rules (`configs/prometheus-alerts.yml`)

Defines alert rules including:
- **WaterSLOBreachAlert**: Triggers when WUE > 3.0 for 2 minutes
- **WaterCriticalSLOBreach**: Triggers when WUE > 4.0 for 1 minute
- **TankerDependencyHigh**: Alerts when tanker dependency > 30%
- **RainwaterHarvestingLow**: Alerts when rainwater < 1000 liters

### 2. Alertmanager Configuration (`configs/alertmanager.yml`)

Handles:
- Email SMTP configuration (Gmail example)
- Alert routing to specific receivers
- Email customization per alert severity
- Alert grouping and repeat intervals

### 3. Prometheus Configuration (`configs/prometheus.yml`)

Updated to:
- Load alert rules from `prometheus-alerts.yml`
- Connect to Alertmanager on port 9093
- Scrape metrics from iot-app service

## Email Setup Instructions

### Using Gmail

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select Mail and Windows (or your device)
   - Generate a 16-character password

3. **Update `configs/alertmanager.yml`**:
   ```yaml
   global:
     smtp_smarthost: 'smtp.gmail.com:587'
     smtp_auth_username: 'your-email@gmail.com'
     smtp_auth_password: 'your-16-char-app-password'
   ```

4. **Update recipient email** in the `receivers` section:
   ```yaml
   - to: 'your-target-email@domain.com'
   ```

### Using Other Email Providers

#### Microsoft Outlook/Office365
```yaml
smtp_smarthost: 'smtp-mail.outlook.com:587'
smtp_auth_username: 'your-email@outlook.com'
smtp_auth_password: 'your-password'
```

#### SendGrid
```yaml
smtp_smarthost: 'smtp.sendgrid.net:587'
smtp_auth_username: 'apikey'
smtp_auth_password: 'your-sendgrid-api-key'
```

## Running the Stack

```bash
# Navigate to the project directory
cd iot-observability-stack

# Start Docker Compose (from the docker port fix)
docker-compose up -d

# Run the IoT application
uv run python src/app.py
```

### Service Endpoints

- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **Grafana**: http://localhost:3000
- **IoT App Metrics**: http://localhost:8000/metrics

## Testing Alerts

### Via Prometheus Console

1. Visit http://localhost:9090/alerts
2. View active alerts and their status
3. Check alert evaluation history

### Via Alertmanager

1. Visit http://localhost:9093
2. View grouped alerts
3. Check notification delivery status

### Trigger Alert Manually (for testing)

Edit `src/sensors/simulator.py` to set WUE to a value > 3.0, then:

```bash
uv run python src/app.py
```

The alert should fire within 2 minutes and send an email.

## Monitoring Alert Status

### In Prometheus
- Navigate to **Alerts** tab to see rule status
- View "Pending" and "Firing" alerts
- Check evaluation intervals and durations

### In Alertmanager
- Visit the Alertmanager dashboard
- View alert groupings and receiver assignments
- Monitor notification delivery logs

### In Grafana (optional)
- Create a dashboard panel with query: `ALERTS{alertname="WaterSLOBreachAlert"}`
- Set up Grafana alerts for even more control

## Alert Rules Explained

### WaterSLOBreachAlert
```
Expression: wue > 3.0
Duration: 2 minutes (must breach for 2 min before firing)
Severity: warning
```

### WaterCriticalSLOBreach
```
Expression: wue > 4.0
Duration: 1 minute
Severity: critical (inhibits warnings)
Repeat: Every 1 hour
```

### TankerDependencyHigh
```
Expression: tanker_dependency_ratio > 0.3
Duration: 5 minutes
```

## Advanced Configuration

### Customize Alert Thresholds

Edit `configs/prometheus-alerts.yml` and adjust the `expr` values:

```yaml
- alert: WaterSLOBreachAlert
  expr: wue > 2.5  # Change threshold from 3.0 to 2.5
```

Then restart Prometheus:
```bash
docker-compose restart prometheus
```

### Add Multiple Recipients

In `configs/alertmanager.yml`, add multiple email addresses:

```yaml
- name: 'email-notifications'
  email_configs:
    - to: 'team-lead@domain.com,operations@domain.com'
```

### Set Alert Repeat Intervals

Control how often repeat notifications are sent:

```yaml
route:
  repeat_interval: 6h  # Repeat every 6 hours
```

### Custom Alert Templates

Customize email subject and body in `configs/alertmanager.yml`:

```yaml
headers:
  Subject: '⚠️ [{{ .GroupLabels.severity | toUpper }}] Water Alert'
```

## Troubleshooting

### Alerts Not Firing

1. **Check Prometheus is scraping metrics**:
   - Visit http://localhost:9090/targets
   - Ensure iot-app target is UP

2. **Verify alert rules are loaded**:
   - Visit http://localhost:9090/rules
   - Check if WaterSLOBreachAlert rule is present

3. **Check Prometheus logs**:
   ```bash
   docker-compose logs prometheus
   ```

### Emails Not Sending

1. **Verify SMTP credentials** in `configs/alertmanager.yml`
2. **Test email with telnet**:
   ```bash
   telnet smtp.gmail.com 587
   ```
3. **Check Alertmanager logs**:
   ```bash
   docker-compose logs alertmanager
   ```
4. **Enable less secure app access** (if using Gmail):
   - Go to https://myaccount.google.com/lesssecureapps

### Alert Spam

If receiving too many alerts:
1. Increase alert `for` duration (e.g., `for: 5m`)
2. Increase `group_wait` in Alertmanager (e.g., `group_wait: 30s`)
3. Adjust `repeat_interval` in route

## Files Modified/Created

- ✅ `configs/prometheus-alerts.yml` - Alert rules
- ✅ `configs/alertmanager.yml` - Alert routing & email config
- ✅ `configs/prometheus.yml` - Added alert rules & alertmanager target
- ✅ `configs/grafana-notifier.yaml` - Grafana notification channel
- ✅ `docker-compose.yml` - Added Alertmanager service
- ✅ `ALERT-SETUP-GUIDE.md` - This guide

## Next Steps

1. Update `configs/alertmanager.yml` with your email credentials
2. Restart the Docker Compose stack
3. Test alerts by manually triggering WUE spike
4. Monitor Alertmanager dashboard to confirm notifications
5. Customize thresholds and receivers as needed

## Support

For issues with:
- **Prometheus**: https://prometheus.io/docs/
- **Alertmanager**: https://prometheus.io/docs/alerting/alertmanager/
- **Gmail**: https://support.google.com/
