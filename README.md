# GitHub Manager for OpenClaw 🐙

**Agent-native GitHub control without the `gh` CLI.**  
Create repositories, push code, inspect repos, manage issues, and cut releases from an OpenClaw skill — safely, scriptably, and without ever printing your token.

<p>
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="OpenClaw Skill" src="https://img.shields.io/badge/OpenClaw-skill-7c3aed">
  <img alt="No gh CLI" src="https://img.shields.io/badge/gh%20CLI-not%20required-orange">
</p>

## Why this exists

Agents often need to publish work: create a repo, push a generated skill, open a tracking issue, or tag a release. The official `gh` CLI is great, but it adds another dependency and auth surface.

**GitHub Manager keeps the workflow small:** one Python script, GitHub REST API, JSON output, and guardrails for destructive actions.

## What it can do

- ✅ Verify GitHub token/account with `whoami`
- ✅ List recently updated repositories
- ✅ Create public or private repositories
- ✅ Push any local folder to GitHub, optionally creating the repo first
- ✅ Inspect repo metadata
- ✅ Create and list issues
- ✅ Create GitHub releases
- ✅ Delete repos only with an exact confirmation guard
- ✅ Keep tokens out of chat/logs and scrub temporary remotes after push

## 30-second quickstart

```bash
# 1) Configure token
mkdir -p ~/.config/tt-github
cat > ~/.config/tt-github/env <<'ENV'
GH_TOKEN=github_pat_xxx
GITHUB_USER=your-github-user
ENV
chmod 600 ~/.config/tt-github/env

# 2) Verify account
python3 scripts/gh_manager.py whoami

# 3) Create + push a folder
python3 scripts/gh_manager.py push \
  --path ./my-skill \
  --repo OWNER/my-skill \
  --create \
  --message "Initial publish" \
  --desc "My OpenClaw skill"
```

## Commands

```bash
S=scripts/gh_manager.py

python3 $S whoami
python3 $S list-repos --limit 30
python3 $S create-repo --name my-skill --desc "Agent-native GitHub automation" [--private]
python3 $S repo-info --repo OWNER/NAME

python3 $S push \
  --path /path/to/project \
  --repo OWNER/NAME \
  [--branch main] \
  [--message "update"] \
  [--create] \
  [--desc "repo description"] \
  [--private]

python3 $S create-issue --repo OWNER/NAME --title "Bug" --body "Details..."
python3 $S list-issues --repo OWNER/NAME --state open
python3 $S create-release --repo OWNER/NAME --tag v1.0.0 --name "v1.0.0" --notes "Release notes..."
python3 $S delete-repo --repo OWNER/NAME --confirm OWNER/NAME
```

## Example workflows

### Publish an OpenClaw skill

```bash
python3 scripts/gh_manager.py push \
  --path ~/.openclaw/workspace/skills/github-manager \
  --repo NachaFromMars/github-manager \
  --create \
  --message "Publish GitHub Manager skill" \
  --desc "OpenClaw skill for safe agent-native GitHub automation"
```

### Cut a release

```bash
python3 scripts/gh_manager.py create-release \
  --repo NachaFromMars/github-manager \
  --tag v0.1.0 \
  --name "v0.1.0 — First public skill release" \
  --notes "Initial release with repo, push, issue, and release management."
```

### Open an issue from an agent run

```bash
python3 scripts/gh_manager.py create-issue \
  --repo OWNER/NAME \
  --title "Add topic update support" \
  --body "Requested by user during repo polish workflow."
```

## Safety model

GitHub Manager is built for assistants that handle private credentials.

- Tokens are resolved from `GH_TOKEN`, `GITHUB_TOKEN`, or `~/.config/tt-github/env`.
- Tokens are never printed by the script.
- `push` temporarily embeds the token in the remote URL, then resets remote to `https://github.com/OWNER/NAME.git` after push.
- `delete-repo` requires `--confirm OWNER/NAME` exactly matching `--repo`.
- Destructive operations should still be confirmed with the human before running.

## Token permissions

Use a fine-grained GitHub PAT when possible:

- **Contents:** Read and write
- **Administration:** Read and write — needed to create/delete repos
- **Issues:** Read and write — if using issue commands
- **Metadata:** Read-only

See [`references/setup-pat.md`](references/setup-pat.md) for a detailed setup guide.

## OpenClaw skill install

Clone or copy this folder into your OpenClaw skills directory:

```bash
git clone https://github.com/NachaFromMars/github-manager.git \
  ~/.openclaw/workspace/skills/github-manager

openclaw skills check
```

The skill trigger is `github-manager`, and it is intended for requests like:

- “push this skill to GitHub”
- “create a repo for this project”
- “open a GitHub issue”
- “cut a release”
- “show my repos”

## Repository polish checklist

This repo is designed to be attractive and useful at a glance:

- Clear README with quickstart and examples
- MIT license
- Changelog
- Security notes
- PAT setup reference
- JSON-first command output for agent automation

## Roadmap

- [ ] Update GitHub repo description/topics from the CLI
- [ ] Pull request creation
- [ ] Branch and file-level helpers
- [ ] Safer dry-run mode for push/delete
- [ ] GitHub Actions workflow helpers

## License

MIT — see [`LICENSE`](LICENSE).
