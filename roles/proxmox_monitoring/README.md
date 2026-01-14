# Proxmox Monitoring Role

Configures system monitoring tools for Proxmox VE crash investigation and
health monitoring.

## Components

### sysstat (sar)

System performance data collection every 10 minutes.

- **Data location**: `/var/log/sysstat/`
- **View CPU**: `sar -u -f /var/log/sysstat/saDD`
- **View memory**: `sar -r -f /var/log/sysstat/saDD`

### atop

Detailed per-process resource accounting with historical data.

- **Data location**: `/var/log/atop/`
- **View historical**: `atop -r /var/log/atop/atop_YYYYMMDD`

### crash-monitor

Custom script logging memory, swap, top processes, and VM/CT counts every
minute.

- **Data location**: `/var/log/crash-monitor/`
- **Format**: Daily log files (YYYY-MM-DD.log)
- **Retention**: 90 days (configurable)

### healthchecks.io

External uptime monitoring ping (optional).

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `proxmox_monitoring_enable_sysstat` | `true` | Enable sysstat |
| `proxmox_monitoring_enable_atop` | `true` | Enable atop |
| `proxmox_monitoring_enable_crash_monitor` | `true` | Enable script |
| `proxmox_monitoring_enable_healthchecks` | `true` | Enable ping |
| `proxmox_monitoring_healthchecks_ping_url` | `""` | Ping URL (secret) |
| `proxmox_monitoring_log_retention_days` | `90` | Days to retain |

## Usage

```yaml
- hosts: proxmox
  roles:
    - role: proxmox_monitoring
      vars:
        proxmox_monitoring_healthchecks_ping_url: "{{ vault_url }}"
```

## Post-Crash Investigation

After a crash/reboot, check these in order:

```bash
# 1. Check crash-monitor logs (1-minute granularity)
# Note: Replace YYYY-MM-DD with the date of the crash.
less /var/log/crash-monitor/YYYY-MM-DD.log

# 2. Check previous boot journal (if available)
journalctl -b -1 | tail -100

# 3. Check for hardware errors
ras-mc-ctl --errors

# 4. Check atop historical data
# Note: Replace YYYYMMDD with the date of the crash.
atop -r /var/log/atop/atop_YYYYMMDD

# 5. Check sar data
# Note: Replace DD with the day of the month for the crash.
sar -r -f /var/log/sysstat/saDD
```
