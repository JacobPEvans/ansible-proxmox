# Tool Execution — Nix Dev Shell

This repo provides all tools via a Nix dev shell (flake.nix + .envrc).

## Rules

- Run ansible, ansible-lint, molecule, and all Python tools as bare commands
- If a tool is not found on PATH, use `direnv exec . <command>` — never install globally
- NEVER use `pipx`, `pip install`, or `uv pip install` to install tools
- NEVER prefix commands with `uv run` — tools are on PATH from the dev shell

## Why

pipx/uv venvs reference Nix store Python interpreters that get garbage-collected.
Any globally-installed Python tool WILL break after the next nix-collect-garbage.
