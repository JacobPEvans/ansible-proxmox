# nas_storage

Provisions a ZFS dataset and Samba share on the Proxmox host for centralized NAS storage.

## What it does

1. Creates a ZFS dataset at `rpool/data/nas` with a 1T quota, mounted at `/mnt/nas`
2. Creates subdirectories for HuggingFace models, Ollama models, media, and backups
3. Installs Samba and configures a share accessible to members of the `nas` group

## Requirements

- Ansible 2.9+
- Proxmox VE with ZFS (`rpool` pool must exist)
- Root/sudo access

## Installation

This role is included in `playbooks/site.yml`. To apply only this role:

```bash
doppler run -- uv run ansible-playbook playbooks/site.yml --tags nas_storage
```

## Usage

Run the full site playbook with the `nas_storage` tag:

```bash
doppler run -- uv run ansible-playbook playbooks/site.yml --tags nas_storage --check
doppler run -- uv run ansible-playbook playbooks/site.yml --tags nas_storage
```

After provisioning, add users to the `nas` group and set their Samba password:

```bash
usermod -aG nas <username>
smbpasswd -a <username>
```

## Role Variables

| Variable | Default | Description |
| --- | --- | --- |
| `nas_storage_zfs_dataset` | `rpool/data/nas` | ZFS dataset path |
| `nas_storage_zfs_quota` | `1T` | ZFS quota |
| `nas_storage_mount_point` | `/mnt/nas` | Mount point |
| `nas_storage_smb_share_name` | `nas` | Samba share name |
| `nas_storage_smb_workgroup` | `WORKGROUP` | Samba workgroup |
| `nas_storage_smb_valid_users` | `@nas` | Samba valid users (group prefix `@`) |
| `nas_storage_directories` | (see defaults) | Subdirectories to create under mount point |

## Notes

- ZFS and systemd tasks are skipped in Docker containers (molecule testing)
- The `nas` group is created automatically; add users to it manually as needed
