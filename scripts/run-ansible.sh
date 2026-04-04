#!/usr/bin/env bash
# Ansible runner - loads SSH key into ssh-agent (in-memory only), runs playbook.
# The key NEVER touches disk. Prefers PROXMOX_SSH_KEY_PATH (file path) when
# available; falls back to loading PROXMOX_SSH_PRIVATE_KEY into ssh-agent.
set -euo pipefail

usage() {
    echo "Usage: $0 <playbook> [ansible-playbook args...]"
    echo "Example: $0 playbooks/monitoring.yml --check"
    exit 1
}

[[ $# -lt 1 ]] && usage

PLAYBOOK="$1"
shift

AGENT_STARTED=false

cleanup() {
    if [[ "$AGENT_STARTED" == true ]]; then
        ssh-agent -k >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

# If no key file exists at PROXMOX_SSH_KEY_PATH, load key content into ssh-agent
if [[ -n "${PROXMOX_SSH_KEY_PATH:-}" ]] && [[ -f "${PROXMOX_SSH_KEY_PATH/#\~/$HOME}" ]]; then
    export ANSIBLE_PRIVATE_KEY_FILE="${PROXMOX_SSH_KEY_PATH/#\~/$HOME}"
elif [[ -n "${PROXMOX_SSH_PRIVATE_KEY:-}" ]]; then
    eval "$(ssh-agent -s)" >/dev/null
    AGENT_STARTED=true
    echo "$PROXMOX_SSH_PRIVATE_KEY" | ssh-add - 2>/dev/null
    # Ansible uses the agent automatically when no key file is specified
    unset ANSIBLE_PRIVATE_KEY_FILE
else
    echo "ERROR: No SSH key available."
    echo "Set PROXMOX_SSH_KEY_PATH (file path) or PROXMOX_SSH_PRIVATE_KEY (key content) via Doppler."
    exit 1
fi

# Run ansible-playbook - prefer NIX_SHELL if set, otherwise use PATH
if [[ -n "${NIX_SHELL:-}" ]]; then
    nix develop "$NIX_SHELL" --command ansible-playbook "$PLAYBOOK" "$@"
elif command -v ansible-playbook &>/dev/null; then
    ansible-playbook "$PLAYBOOK" "$@"
else
    echo "ERROR: ansible-playbook not found on PATH and NIX_SHELL not set"
    echo "Either activate direnv or set NIX_SHELL to your nix flake path"
    exit 1
fi
