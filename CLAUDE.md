# Ansible Proxmox

Configure the Proxmox VE host itself (not applications).

## This Repo Owns

- Kernel tuning (vm.swappiness, hugepages)
- ZFS swap configuration
- System ulimits
- Proxmox monitoring (healthchecks)
- Crash diagnostics
- Common system packages

## Pipeline Role

This repo has **no direct pipeline role**. It ensures
the Proxmox host is stable and properly configured so
that VMs/containers (managed by other repos) can run
reliably.

Firewall rules for pipeline ports (1514-1518, 8088,
2055) are managed by `terraform-proxmox/modules/firewall/`.

## Required Environment Variables

| Variable | Purpose |
| --- | --- |
| `PROXMOX_VE_HOSTNAME` | Proxmox VE hostname |
| `PROXMOX_SSH_KEY_PATH` | SSH key path |
| `PROXMOX_VE_GATEWAY` | Network gateway |
| `PROXMOX_DOMAIN` | Internal DNS domain |
| `HEALTHCHECK_PING_KEY` | Healthchecks.io key |

## Commands

```bash
# Run full playbook
doppler run -- pipx run ansible-playbook \
  -i inventory/hosts.yml playbooks/site.yml

# Dry run
doppler run -- pipx run ansible-playbook \
  -i inventory/hosts.yml playbooks/site.yml \
  --check --diff

# Lint
pipx run ansible-lint
```

## Related Repositories

| Repo | Relationship |
| --- | --- |
| terraform-proxmox | Peer: provisions VMs/containers |
| ansible-proxmox-apps | Peer: configures apps on VMs |
| ansible-splunk | Peer: configures Splunk on VM |
