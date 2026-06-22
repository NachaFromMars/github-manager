# 🐙 GitHub Manager (OpenClaw skill)

Manage GitHub from an OpenClaw agent via the REST API — **no `gh` CLI required**.
Create repos, push code, open/read issues, cut releases, inspect repos, manage many repos.

## Token (never printed)
Resolved from env `GH_TOKEN`/`GITHUB_TOKEN`, or `~/.config/tt-github/env`.
Use a fine-grained PAT with **Administration + Contents = Read and write** (see `references/setup-pat.md`).

## Usage
```bash
S=scripts/gh_manager.py
python3 $S whoami
python3 $S list-repos --limit 30
python3 $S create-repo --name my-skill --desc "..."
python3 $S push --path ./my-skill --repo OWNER/my-skill --create --message "init"
python3 $S repo-info --repo OWNER/NAME
python3 $S create-issue --repo OWNER/NAME --title "Bug" --body "..."
python3 $S list-issues --repo OWNER/NAME
python3 $S create-release --repo OWNER/NAME --tag v1.0 --name "v1.0"
python3 $S delete-repo --repo OWNER/NAME --confirm OWNER/NAME
```

## Safety
- Token never logged; scrubbed from git remote after push.
- `delete-repo` requires `--confirm OWNER/NAME` exact match.
- Destructive ops should be confirmed with the user.

## License
MIT
