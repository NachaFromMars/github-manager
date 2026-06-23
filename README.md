# github-manager — GitHub management via pure-Python REST API

> Drive the GitHub REST API directly in Python — no `gh` CLI required. Create repos, push code, open issues, cut releases, and manage metadata from a single script.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blueviolet)](https://github.com/NachaFromMars)

## Overview
github-manager handles GitHub operations through its REST API using pure Python — no external `gh` CLI dependency. It reads a fine-grained PAT from `GH_TOKEN` env or `~/.config/tt-github/env` and supports the full repo lifecycle. Destructive actions like repo deletion are gated behind an explicit `--confirm` guard. Tokens are never printed to chat or logs.

## Features
- `whoami` — verify token and login
- `list-repos`, `create-repo`, `repo-info` — repo management
- `push` — push code with `--create` flag and `--method api/git`
- `create-issue`, `list-issues` — issue management
- `create-release` — cut GitHub releases
- `set-topics`, `set-meta`, `publish` — metadata management
- `delete-repo` — guarded with `--confirm` match

## Usage / Quick Start
```bash
# Token setup
export GH_TOKEN="***"
# or store in ~/.config/tt-github/env

python3 scripts/gh_manager.py whoami
python3 scripts/gh_manager.py create-repo --name my-skill --desc "..."
python3 scripts/gh_manager.py push --path ./skill --repo USER/NAME --create
python3 scripts/gh_manager.py create-release --repo USER/NAME --tag v1.0
```

## Trigger Keywords (OpenClaw)
push to GitHub, create repo, github repo, open issue, create release, manage github, list repos

---
Part of the [NachaFromMars](https://github.com/NachaFromMars) OpenClaw skill ecosystem.
