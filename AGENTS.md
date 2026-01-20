# Ansible Proxmox - AI Agent Documentation

Ansible automation for Proxmox VE host configuration.

## Purpose

Configure the Proxmox VE hypervisor itself:

- Kernel parameters and tuning
- Swap configuration
- Host monitoring
- Storage backends
- Network configuration

This is for **host-level** configuration only. Application VMs are
configured by `ansible-proxmox-apps` and `ansible-splunk`.

## Dependencies

### External Services

- **Doppler**: SSH credentials and API tokens

### Infrastructure

- Physical Proxmox VE cluster (not provisioned by Terraform)

## Key Files

| Path | Purpose |
| ---- | ------- |
| `playbooks/site.yml` | Main orchestration playbook |
| `roles/` | Configuration roles |
| `inventory/` | Proxmox host inventory |

## Agent Tasks

### Running Playbooks

```bash
doppler run -- uv run ansible-playbook playbooks/site.yml
```

### Common Operations

- **Kernel tuning**: Updates sysctl parameters
- **Swap management**: Configures swappiness
- **Monitoring setup**: Installs node_exporter

## Secrets Management

All secrets from Doppler:

```bash
doppler run -- uv run ansible-playbook playbooks/site.yml
```

## Related Repositories

- **terraform-proxmox**: VM/container provisioning
- **ansible-proxmox-apps**: Application deployment on VMs
- **ansible-splunk**: Splunk configuration
