# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0](https://github.com/JacobPEvans/ansible-proxmox/compare/v1.0.0...v1.1.0) (2026-03-11)


### Features

* add daily repo health audit agentic workflow ([#75](https://github.com/JacobPEvans/ansible-proxmox/issues/75)) ([061bc4a](https://github.com/JacobPEvans/ansible-proxmox/commit/061bc4a6feff2ecb7f695086a8e9a65b8e1a0f64))
* add GitHub Copilot agentic workflows ([#56](https://github.com/JacobPEvans/ansible-proxmox/issues/56)) ([677f02a](https://github.com/JacobPEvans/ansible-proxmox/commit/677f02a51fb056c0116b8b97f358857a803b3152))
* add per-repo devShell ([#54](https://github.com/JacobPEvans/ansible-proxmox/issues/54)) ([aea563b](https://github.com/JacobPEvans/ansible-proxmox/commit/aea563be1b180d9efb4e194335a5e8f956d680fa))
* add proxmox_monitoring role for crash investigation ([#32](https://github.com/JacobPEvans/ansible-proxmox/issues/32)) ([da6bc18](https://github.com/JacobPEvans/ansible-proxmox/commit/da6bc181b966cf39f98e87b72738b9ef9971fea3))
* add scheduled AI workflow callers ([#65](https://github.com/JacobPEvans/ansible-proxmox/issues/65)) ([70ce9dd](https://github.com/JacobPEvans/ansible-proxmox/commit/70ce9dd6ddc3aea6ccf459a9fa8422555ca88666))
* crash diagnostics role with kdump and kernel panic settings ([#31](https://github.com/JacobPEvans/ansible-proxmox/issues/31)) ([d9dcb5f](https://github.com/JacobPEvans/ansible-proxmox/commit/d9dcb5fa09164ace9f76731f7543fe16d3e231d6))
* disable automatic triggers on Claude-executing workflows ([1e2be59](https://github.com/JacobPEvans/ansible-proxmox/commit/1e2be59c8801f631ca736d41001c78b98998d568))
* **kernel_tuning:** add C-state disable option for AMD stability ([#38](https://github.com/JacobPEvans/ansible-proxmox/issues/38)) ([b1c2a09](https://github.com/JacobPEvans/ansible-proxmox/commit/b1c2a09dd0a160d3a3896bfd255e1c26ddb25291))
* **kernel_tuning:** add Proxmox boot params for AMD Zen1 stability ([#36](https://github.com/JacobPEvans/ansible-proxmox/issues/36)) ([43de2de](https://github.com/JacobPEvans/ansible-proxmox/commit/43de2de45b9b3258310cda02d2433bf74c625704))
* **lxc:** add lxc_features role to manage container features as code ([#51](https://github.com/JacobPEvans/ansible-proxmox/issues/51)) ([a9c4ee7](https://github.com/JacobPEvans/ansible-proxmox/commit/a9c4ee720576d22c6ac50932cceeec2afcadee09))
* **monitoring:** add MCE/EDAC hardware error detection ([#34](https://github.com/JacobPEvans/ansible-proxmox/issues/34)) ([e67d0ce](https://github.com/JacobPEvans/ansible-proxmox/commit/e67d0ce06a9f8c9ea45aa20ade4da5ae5bb9d207))
* **renovate:** extend shared preset, remove duplicated rules ([ffc73cc](https://github.com/JacobPEvans/ansible-proxmox/commit/ffc73cc1328a59501c3114bcc3231db85a8f6324))


### Bug Fixes

* change .docs symlink to relative path ([#40](https://github.com/JacobPEvans/ansible-proxmox/issues/40)) ([a78c87d](https://github.com/JacobPEvans/ansible-proxmox/commit/a78c87d3cf938e8255ac2e0e9b7a8f20a891cc37))
* **kernel_tuning:** re-enable SMT in boot parameters ([#41](https://github.com/JacobPEvans/ansible-proxmox/issues/41)) ([8cb11b7](https://github.com/JacobPEvans/ansible-proxmox/commit/8cb11b73edb799e806524f61635451ec70068f2d))
* **kernel_tuning:** support both UEFI and Legacy BIOS boot methods ([#37](https://github.com/JacobPEvans/ansible-proxmox/issues/37)) ([1ede20e](https://github.com/JacobPEvans/ansible-proxmox/commit/1ede20e8ef6f1e5aa49cb5dfd93cac9244e8183d))

## [Unreleased]

## [1.0.0] - 2025-01-12

### Added

- Initial repository structure
- Role: `common` - Base packages and SSH configuration
- Role: `zfs_swap` - ZFS ZVOL swap configuration (96 GB default)
- Role: `kernel_tuning` - Sysctl settings for NVMe and memory management
- Role: `ulimits` - System-wide file descriptor and process limits
- Role: `crash_diagnostics` - Kernel crash diagnostics and hardware error monitoring
- Role: `proxmox_monitoring` - System monitoring (sysstat, atop, crash-monitor, healthchecks.io)
- Role: `lxc_features` - LXC container feature flags (fuse, nesting, keyctl)
- GitHub Actions workflow for ansible-lint
- GitHub Actions workflow for Molecule tests
- Molecule test configuration for role validation
- Renovate configuration for automated dependency updates
- Pre-commit hooks configuration

[Unreleased]: https://github.com/JacobPEvans/ansible-proxmox/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/JacobPEvans/ansible-proxmox/releases/tag/v1.0.0
