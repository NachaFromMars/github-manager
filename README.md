# 🐙 GitHub Manager

[![Release](https://img.shields.io/github/v/release/NachaFromMars/github-manager?label=release)](https://github.com/NachaFromMars/github-manager/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

> **Let your AI agent manage GitHub for you — create repos, push code, open issues, cut releases, and auto-polish a repo into a presentable product. Pure REST API, no `gh` CLI, token never printed.**

```bash
# create + push + describe + topics + release — in ONE command
python3 scripts/gh_manager.py publish \
  --path ./my-skill --repo OWNER/my-skill --create \
  --desc "What this does in one line" \
  --tag v0.1.0 --notes "First release"
```

---

## Why it exists

Opening the GitHub web UI to create a repo, push files, set a description, add topics, and draft a release is slow and repetitive. GitHub Manager lets an agent do all of it from chat, safely, with the token kept out of logs and scrubbed from git config.

It also turns "just push the code" into "publish a presentable repo": the `publish` command optimizes the repo (description + topics + optional release) every time you ship.

## Features

- 📦 **One-shot `publish`** — ensure repo → push files → set description → set topics → optional release.
- 🔼 **Push via REST Contents API** — robust even when git-over-HTTPS auth is restricted.
- 🏷️ **Auto repo polish** — `set-topics`, `set-meta` (description/homepage) so the repo is discoverable.
- 🐛 Issues, 🚀 releases, 📋 repo info, 📒 list repos.
- 🗑️ Guarded `delete-repo` (must confirm exact `OWNER/NAME`).
- 🔒 Token resolved from env/file, **never printed**, scrubbed from any git remote.

## Quickstart

```bash
# 1) store a fine-grained PAT safely (see references/setup-pat.md)
mkdir -p ~/.config/tt-github && chmod 700 ~/.config/tt-github
cat > ~/.config/tt-github/env <<'EOF'
GITHUB_USER=your_login
GH_TOKEN=github_pat_xxx
EOF
chmod 600 ~/.config/tt-github/env

# 2) verify
python3 scripts/gh_manager.py whoami

# 3) publish a folder as a polished repo
python3 scripts/gh_manager.py publish \
  --path ./my-skill --repo your_login/my-skill --create \
  --desc "One-line value proposition" \
  --topics "openclaw,ai-agent,automation" \
  --tag v0.1.0 --release-name "v0.1.0" --notes "Initial release"
```

## Commands

```bash
S=scripts/gh_manager.py
python3 $S whoami
python3 $S list-repos --limit 30
python3 $S create-repo --name X --desc "..."
python3 $S push --path ./dir --repo OWNER/X --create --message "init"
python3 $S publish --path ./dir --repo OWNER/X --create --desc "..." --topics "a,b" --tag v0.1.0
python3 $S set-topics --repo OWNER/X --topics "openclaw,ai-agent,automation"
python3 $S set-meta --repo OWNER/X --desc "..." --homepage "https://..."
python3 $S repo-info --repo OWNER/X
python3 $S create-issue --repo OWNER/X --title "Bug" --body "..."
python3 $S list-issues --repo OWNER/X --state open
python3 $S create-release --repo OWNER/X --tag v1.0 --name "v1.0"
python3 $S delete-repo --repo OWNER/X --confirm OWNER/X
```

## Safety model

- 🔑 **Token never printed.** Resolved from `GH_TOKEN`/`GITHUB_TOKEN` env or `~/.config/tt-github/env`.
- 🧹 **Scrubbed from git.** When `push` embeds a token in a remote URL, it is removed right after.
- 🛑 **Destructive ops are guarded.** `delete-repo` requires `--confirm OWNER/NAME` exactly.
- 🪪 **Least privilege.** Use a fine-grained PAT scoped to the repos you manage (see `references/setup-pat.md`).

## Example workflows

- **Publish an OpenClaw skill:** `examples/publish-skill.sh /path/to/skill OWNER/repo`
- **Re-polish an existing repo:** `set-topics` + `set-meta` to refresh discoverability.
- **Ship a version:** `publish ... --tag vX.Y.Z --notes "..."`.

## Install as an OpenClaw skill

Drop this folder into your OpenClaw `skills/` directory. The agent loads `SKILL.md` and can drive every command above from chat.

## Roadmap

- README quality lint before publish (warn on missing tagline/quickstart/license).
- Auto-generate release notes from git diff / changelog.
- Branch protection + PR-based publish option.
- Multi-repo batch publish.

## License

MIT — free to use, fork, and share.

## My Repo Library

Published or curated repositories are remembered locally in:

```text
~/.config/tt-github/repos.json
```

Use it as a lightweight catalog of repos the agent has uploaded or managed:

```bash
python3 scripts/gh_manager.py library-list
python3 scripts/gh_manager.py library-list --query openclaw
python3 scripts/gh_manager.py library-add --repo OWNER/NAME --desc "Important repo" --topics openclaw,automation
python3 scripts/gh_manager.py library-remove --repo OWNER/NAME
```

`create-repo`, `push`, and `update-repo` automatically save useful metadata to the library.

## Repo metadata and topics

```bash
python3 scripts/gh_manager.py update-repo \
  --repo OWNER/NAME \
  --desc "Short repo pitch" \
  --topics openclaw,ai-agent,automation \
  --homepage https://github.com/OWNER/NAME
```

## Optional visual polish

For public-facing repos, the agent should ask before creating images:

> “Do you want me to generate a banner/logo/screenshot package before release?”

Only after approval should it create assets such as `assets/banner.png`, `assets/logo.png`, or terminal screenshots. This keeps media generation intentional instead of automatic.
